"""Validate collection metadata, sibling closure and self-contained skill resources."""

import argparse
import re
import sys
from pathlib import Path

import yaml

try:
    from .check_links import FRONTMATTER, links, local_target
except ImportError:
    from check_links import FRONTMATTER, links, local_target

ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
LICENSE = "Proprietary. All rights reserved."


def check(root, selected=None):
    names = selected or sorted(
        p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    known, errors = set(names), []
    if not names:
        errors.append("No skill directories found.")
    for name in names:
        directory = (root / name).resolve()
        entry = directory / "SKILL.md"

        def report(path, message):
            errors.append(f"{path}: {message}")

        try:
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError("Selected names must be skill directory names")
            content = entry.read_text(encoding="utf-8")
            match = FRONTMATTER.match(content)
            if not match:
                raise ValueError("Expected YAML frontmatter followed by skill instructions")
            data = yaml.safe_load(match[1])
            if not isinstance(data, dict):
                raise ValueError("Frontmatter must be a mapping")
            declared = data.get("name")
            if (
                not isinstance(declared, str)
                or len(declared) > 64
                or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", declared)
                or declared != name
            ):
                report(
                    entry,
                    "name must match its directory and be a lowercase hyphenated identifier of 1–64 characters",
                )
            for key, limit in (("description", 1024), ("compatibility", 500)):
                value = data.get(key)
                if key == "compatibility" and key not in data:
                    continue
                if not isinstance(value, str) or not value.strip() or len(value) > limit:
                    report(entry, f"{key} must be a nonempty string of at most {limit} characters")
            if data.get("license") != LICENSE:
                report(entry, "Include the collection's rights-reserved license notice")
            if "metadata" in data and (
                not isinstance(data["metadata"], dict)
                or any(not isinstance(v, str) for v in data["metadata"].values())
            ):
                report(entry, "metadata must map keys to strings")
            if "allowed-tools" in data and not isinstance(data["allowed-tools"], str):
                report(entry, "allowed-tools must be a string")
            for field in data.keys() - ALLOWED:
                report(entry, f"Unknown frontmatter field: {field}")
            if not content[match.end() :].strip():
                report(entry, "Skill instructions must not be empty")

            all_files, edges = set(), {}
            # Path.walk does not recurse through directory symlinks. Escapes are defects,
            # even when a Markdown edge does not mention the escaped resource.
            for parent, dirs, files in directory.walk():
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for child in dirs + files:
                    path = parent / child
                    if child.startswith("."):
                        continue
                    if not path.resolve().is_relative_to(directory):
                        report(path, "Resource symlink leaves the skill folder")
                        continue
                    if path.is_dir():
                        continue
                    all_files.add(path.resolve())
                    if path.suffix != ".md":
                        continue
                    markdown = path.read_text(encoding="utf-8")
                    edges[path.resolve()] = []
                    for target in links(markdown):
                        resolved = local_target(path, target, directory)
                        if resolved is None:
                            continue
                        dest, _ = resolved
                        if not dest.is_relative_to(directory):
                            report(
                                path,
                                f"Link leaves the skill folder: {target}. Name the other skill instead.",
                            )
                        else:
                            edges[path.resolve()].append(dest)
                    for mentioned in re.findall(r"\bluminekit-[a-z0-9]+(?:-[a-z0-9]+)*", markdown):
                        if mentioned not in known:
                            report(path, f"Names an unknown or unselected skill: {mentioned}")
            reached, queue = {entry}, [entry]
            while queue:
                for target in edges.get(queue.pop(), []):
                    if target not in reached:
                        reached.add(target)
                        queue.append(target)
            for path in sorted(all_files - reached):
                report(path, "Not reachable from SKILL.md through links inside the skill")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            report(entry, str(exc))
    return names, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1] / "skills"
    )
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    try:
        names, errors = check(args.root.resolve(), args.names)
    except OSError as exc:
        names, errors = [], [str(exc)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(names)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

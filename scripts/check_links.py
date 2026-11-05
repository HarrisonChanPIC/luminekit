"""Read-only local Markdown links/ordinary GitHub-style heading checks.

Uses CommonMark parsing (including reference links); no remote crawling, HTML/generated
anchor emulation or Markdown style gate. A leading slash uses --root, or --bundle-root
when checking an OKF bundle. Reserved-file checks are separate from link policy.
"""

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

PARSER = MarkdownIt("commonmark").enable("table")
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)


def body(text):
    return FRONTMATTER.sub("", text, count=1)


def links(text):
    """Actual inline links/images, excluding code and unused definitions."""
    targets = []
    for token in PARSER.parse(body(text)):
        for child in token.children or []:
            if child.type == "link_open":
                targets.append(child.attrGet("href"))
            elif child.type == "image":
                targets.append(child.attrGet("src"))
    return targets


def heading_ids(text):
    used = set()
    tokens = PARSER.parse(body(text))
    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        children = tokens[i + 1].children or []
        title = "".join(
            child.content if child.type in {"text", "code_inline", "image"} else ""
            for child in children
        ).lower()
        slug = "".join(
            c for c in title if c in "-_ " or unicodedata.category(c)[0] not in "PS"
        ).replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in used:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        used.add(candidate)
    return used


def markdown_files(paths):
    found = set()
    for path in paths:
        if not path.exists():
            raise ValueError(f"Input does not exist: {path}")
        if path.is_dir():
            found.update(p for p in path.rglob("*.md") if p.is_file())
        else:
            found.add(path)
    return sorted(found)


def local_target(source, target, root):
    parts = urlsplit(target)
    if parts.scheme or parts.netloc:
        return None
    path = unquote(parts.path)
    resolved = (root / path.lstrip("/")) if path.startswith("/") else source.parent / path
    if not path:
        resolved = source
    return resolved.resolve(), unquote(parts.fragment)


def check(paths, root):
    errors, headings = [], {}
    for source in markdown_files(paths):
        for target in links(source.read_text(encoding="utf-8")):
            resolved = local_target(source, target, root)
            if resolved is None:
                continue
            path, fragment = resolved
            if not path.exists():
                errors.append(f"{source}: missing target {target}")
                continue
            if path.is_dir():
                # Follow normal directory entry conventions when a fragment needs a document.
                entry = next(
                    (path / n for n in ("index.md", "README.md") if (path / n).is_file()), None
                )
                if entry is None:
                    if fragment:
                        errors.append(f"{source}: no Markdown entry for fragment {target}")
                    continue
                path = entry
            if fragment and path.suffix.lower() == ".md":
                if path not in headings:
                    headings[path] = heading_ids(path.read_text(encoding="utf-8"))
                if fragment not in headings[path]:
                    errors.append(f"{source}: missing heading {target}")
    return errors


def check_reserved(bundle):
    """§11.3 coverage the pinned upstream checker reports only as warnings."""
    errors = []
    for path in markdown_files([bundle]):
        if path.name not in {"index.md", "log.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if text.startswith("---\n") or text.startswith("---\r\n"):
            allowed = path.name == "index.md" and path.parent.resolve() == bundle.resolve()
            try:
                meta = yaml.safe_load(match[1]) if match else None
                if not allowed or not isinstance(meta, dict) or set(meta) != {"okf_version"}:
                    errors.append(f"{path}: reserved frontmatter permits only root okf_version")
            except yaml.YAMLError:
                errors.append(f"{path}: malformed root index frontmatter")
        tokens = PARSER.parse(body(text))
        if path.name == "index.md":
            if not any(t.type == "heading_open" for t in tokens) or not links(text):
                errors.append(f"{path}: index needs grouped directory entries")
        else:
            dates = []
            for i, token in enumerate(tokens):
                if token.type == "heading_open" and token.tag == "h2":
                    value = tokens[i + 1].content
                    try:
                        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                            raise ValueError
                        dates.append(date.fromisoformat(value))
                    except ValueError:
                        errors.append(f"{path}: log date heading must be YYYY-MM-DD: {value}")
            if not dates or dates != sorted(dates, reverse=True):
                errors.append(f"{path}: log needs date groups newest first")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("README.md"), Path("AGENTS.md"), Path("skills")],
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--bundle-root", type=Path, help="OKF path root; also check reserved structures"
    )
    args = parser.parse_args()
    try:
        errors = check(args.paths, args.bundle_root or args.root)
        if args.bundle_root:
            errors.extend(check_reserved(args.bundle_root))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Validated local Markdown links and ordinary heading anchors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

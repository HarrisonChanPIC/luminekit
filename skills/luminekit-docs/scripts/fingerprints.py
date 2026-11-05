"""Track file fingerprints for a folder: duplicates, moves, changes, additions, deletions.

Usage:
  python fingerprints.py scan FOLDER [--out FILE] [--exclude PATH ...] [--full]
  python fingerprints.py compare OLD.csv NEW.csv

`scan` writes a CSV (path, size, mtime_ns, sha256; sorted by path) and reports what
changed since the previous file. Only files whose size or mtime changed are rehashed
unless --full is given. The hash covers file contents only, so a copied or renamed
file keeps its hash. Hidden files and folders, Office lock files (~$*) and symlinks
are skipped. If any file or folder cannot be read, previously recorded entries that
were not seen are kept and no deletion is reported. Standard library only.
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

FIELDS = ["path", "size", "mtime_ns", "sha256"]
DEFAULT_NAME = ".fingerprints.csv"
SKIP_FILES = {"Thumbs.db", "desktop.ini"}


def read(path):
    path = Path(path)
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if rows and set(rows[0]) != set(FIELDS):
        raise ValueError(f"{path} is not a fingerprint file (columns {FIELDS})")
    return {r["path"]: {**r, "size": int(r["size"]), "mtime_ns": int(r["mtime_ns"])} for r in rows}


def write(path, entries):
    path = Path(path)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator="\n")
        writer.writeheader()
        for key in sorted(entries):
            writer.writerow(entries[key])
    temp.replace(path)


def digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def skipped(name):
    return name.startswith(".") or name.startswith("~$") or name in SKIP_FILES


def scan(root, previous=None, exclude=(), full=False):
    """Return (entries, problems). Unchanged size+mtime reuses the previous hash."""
    root = Path(root).resolve()
    previous = previous or {}
    excluded = {Path(e).resolve() for e in exclude}
    entries, problems = {}, []

    def onerror(error):
        problems.append(f"{error.filename}: {error.strerror}")

    for parent, dirs, files in os.walk(root, onerror=onerror, followlinks=False):
        here = Path(parent)
        dirs[:] = sorted(
            d
            for d in dirs
            if not skipped(d) and not (here / d).is_symlink() and (here / d) not in excluded
        )
        for name in sorted(files):
            path = here / name
            if skipped(name) or path.is_symlink() or path in excluded:
                continue
            key = path.relative_to(root).as_posix()
            try:
                stat = path.stat()
                old = previous.get(key)
                if (
                    not full
                    and old
                    and old["size"] == stat.st_size
                    and old["mtime_ns"] == stat.st_mtime_ns
                ):
                    sha = old["sha256"]
                else:
                    sha = digest(path)
            except OSError as error:
                problems.append(f"{key}: {error.strerror}")
                continue
            entries[key] = {
                "path": key,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "sha256": sha,
            }
    return entries, problems


def compare(old, new, complete=True):
    """Classify differences between two fingerprint maps."""
    old_by_hash, new_by_hash = {}, {}
    for key, row in old.items():
        old_by_hash.setdefault(row["sha256"], set()).add(key)
    for key, row in new.items():
        new_by_hash.setdefault(row["sha256"], set()).add(key)
    gone = sorted(set(old) - set(new))
    added = sorted(set(new) - set(old))
    changed = sorted(k for k in set(old) & set(new) if old[k]["sha256"] != new[k]["sha256"])
    moved, copied = [], []
    for key in added:
        sources = sorted(old_by_hash.get(new[key]["sha256"], set()))
        if not sources:
            continue
        missing = [s for s in sources if s in gone]
        (moved if missing else copied).append({"from": (missing or sources)[0], "to": key})
    matched_to = {m["to"] for m in moved + copied}
    matched_from = {m["from"] for m in moved}
    report = {
        "duplicates": sorted(sorted(keys) for keys in new_by_hash.values() if len(keys) > 1),
        "moved": moved,
        "copied": copied,
        "changed": changed,
        "added": [k for k in added if k not in matched_to],
        "deleted": [k for k in gone if k not in matched_from] if complete else [],
    }
    if not complete:
        report["not_seen"] = [k for k in gone if k not in matched_from]
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("scan", help="update the fingerprint file for a folder")
    s.add_argument("folder", type=Path)
    s.add_argument("--out", type=Path, help=f"fingerprint file (default FOLDER/{DEFAULT_NAME})")
    s.add_argument(
        "--exclude",
        type=Path,
        action="append",
        default=[],
        help="folder or file to leave out, e.g. the agent knowledge folder",
    )
    s.add_argument("--full", action="store_true", help="rehash every file")
    c = sub.add_parser("compare", help="compare two fingerprint files")
    c.add_argument("old", type=Path)
    c.add_argument("new", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            out = args.out or args.folder / DEFAULT_NAME
            previous = read(out)
            entries, problems = scan(args.folder, previous, [*args.exclude, out], args.full)
            complete = not problems
            report = compare(previous, entries, complete)
            if not complete:
                for key in report["not_seen"]:
                    entries[key] = previous[key]
                report["problems"] = problems
            write(out, entries)
            report["files"] = len(entries)
            report["fingerprints"] = str(out)
        else:
            report = compare(read(args.old), read(args.new))
    except (OSError, ValueError) as error:
        print(f"fingerprints: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report.get("problems") else 0


if __name__ == "__main__":
    sys.exit(main())

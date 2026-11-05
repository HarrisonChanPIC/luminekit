# Standalone Python scripts

Keep a focused single-file utility as a script. Use `pyproject.toml` for a multi-file application or reusable package. For a new standalone utility, use uv and Python 3.14 or newer; existing scripts retain their interpreter and runner contract.

## Inline metadata

Use [PEP 723 metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) to declare a script's Python requirement and third-party packages. For a new script:

```python
# /// script
# requires-python = ">=3.14"
# dependencies = ["httpx"]
# ///

"""Print the HTTP status for a URL supplied on the command line."""

import argparse

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args()
    with httpx.Client(timeout=10.0) as client:
        response = client.get(args.url)
        response.raise_for_status()
        print(response.status_code)


if __name__ == "__main__":
    main()
```

Keep one purpose, usage/help, type hints and explicit resource ownership. A standard-library-only script can use `dependencies = []`; it does not need a package scaffold. Metadata only declares requirements; a runner such as uv must consume it.

## Create, run and lock

```sh
uv init --script --python 3.14 fetch_status.py
uv add --script fetch_status.py httpx
uv run --script fetch_status.py https://example.com
uv remove --script fetch_status.py httpx
```

For a shared script whose dependency resolution must repeat, create and retain an adjacent lockfile:

```sh
uv lock --script fetch_status.py
uv run --locked --script fetch_status.py https://example.com
```

Commit `fetch_status.py.lock` with that workflow. Inline metadata alone does not pin transitive resolution; use uv's script locking for that. Use dependency bounds for actual compatibility requirements and the lockfile for the chosen resolution. See [uv scripts](https://docs.astral.sh/uv/guides/scripts/).

On systems supporting `env -S`, an optional executable shebang is `#!/usr/bin/env -S uv run --script`; explicit `uv run --script` remains portable across environments where the shebang is unsuitable. Configure private indexes through uv's documented script/index settings and environment-backed credentials; never embed credentials in the script.

Use temporary `uv run --with PACKAGE …` for a one-off dependency, and script metadata for an enduring script requirement. When a script needs a workspace, development groups, complex local packages or a build, use a project rather than expanding inline metadata into a second project system. Locking/installation may require network/cache access. A stub module checks CLI wiring, not the real third-party library's behavior.

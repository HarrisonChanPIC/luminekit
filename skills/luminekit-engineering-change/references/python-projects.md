# Python projects and uv

For new projects, use uv and Python 3.14 or newer. For existing projects, preserve their versions, manager, backend and layout; these examples are not a migration instruction.

## Choose a project shape

| Product | Shape |
| --- | --- |
| Focused single file | Use the [script guide](python-scripts.md); no package skeleton is needed. |
| Multi-file application | `uv init --python 3.14 example-app`; keep application metadata and dependencies in `pyproject.toml`. |
| Reusable/distributed package | `uv init --package --python 3.14 example-package`; use a `src/` layout and an explicit build backend. |

The commands use 3.14 as a concrete baseline; choose a newer stable version where appropriate. Declare `requires-python = ">=3.14"` or the selected newer floor, and record the development interpreter in `.python-version`. Keep the declared floor, CI, deployment image and tool targets consistent. Do not copy a modern floor into an older project. See uv's [project creation options](https://docs.astral.sh/uv/concepts/projects/init/).

For ordinary pure-Python packages, prefer [uv_build](https://docs.astral.sh/uv/concepts/build-backend/). Let `uv init --package` supply a compatible build-system requirement rather than guessing its version range. Native extensions or special build requirements may need a different supported backend. Keep existing backend behavior, included data, entry points and distribution metadata intact.

Use `pyproject.toml` for project metadata, build configuration and tool settings. Include useful README, license and command/entry-point information. A package generally has `src/package_name/` and `tests/`; a small application need not pretend to be a published library. A full cookiecutter template is optional only when its scaffolding is wanted, not a prerequisite for creating a project.

## Dependency ownership

Put runtime requirements in `[project.dependencies]`. Put optional consumer features in `[project.optional-dependencies]`. Put development, test, docs and audit tools in `[dependency-groups]`; groups are not published as consumer extras. See the PyPA specifications for [project metadata](https://packaging.python.org/en/latest/specifications/pyproject-toml/) and [groups](https://packaging.python.org/en/latest/specifications/dependency-groups/).

Use uv to keep declarations and resolution together:

```sh
uv add httpx
uv add --group lint ruff ty
uv add --group test pytest pytest-cov
uv remove httpx
uv sync --group lint --group test
uv run python main.py
```

For a package, use its installed module or declared entry point rather than adding `src` to `sys.path`. Workspaces and local packages use uv's source/workspace facilities instead of undocumented path hacks. Do not add runtime dependencies merely because a developer command needs them. The [dependency guide](https://docs.astral.sh/uv/concepts/projects/dependencies/) covers groups, extras, sources and workspace dependencies.

## Locks, execution and distribution

Commit `uv.lock` for reproducible development of both applications and libraries; library consumers still resolve from published dependency metadata. Keep `.venv/` out of version control. Review dependency and lock changes together. A Python range describes supported interpreters; one local run does not cover them all.

Use `uv run` for project commands rather than manually activating a virtualenv. `uv sync` reconciles the environment. In CI, use `uv sync --locked` and `uv run --locked …` to reject an outdated lock rather than updating it as a side effect. `--frozen` skips the freshness check and is a different promise. Upgrade resolution deliberately with `uv lock --upgrade` or `uv lock --upgrade-package NAME`. See [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

Use `uv build` for distributable artifacts. Package publication is a separate authorized release action; do not infer permission to run `uv publish` from a build request. Retain only supported Python/platform constraints and the public dependencies the package actually needs.

## Command reference

| Need | uv command |
| --- | --- |
| Create an application or package | `uv init`, `uv init --package` |
| Install/select a development interpreter | `uv python install 3.14`, `uv python pin 3.14` |
| Add/remove project requirements | `uv add PACKAGE`, `uv remove PACKAGE` |
| Include task dependencies | `uv add --group test PACKAGE`, `uv sync --group test` |
| Install all defined groups | `uv sync --all-groups` when the groups are mutually compatible |
| Run a project command | `uv run COMMAND` |
| Use a temporary extra dependency | `uv run --with PACKAGE COMMAND` |
| Run a standalone tool | `uvx TOOL`, or `uv tool run TOOL` |
| Manage an explicitly wanted persistent tool | `uv tool install TOOL`, `uv tool upgrade TOOL`, `uv tool uninstall TOOL`, `uv tool list` |
| Export for an external consumer | `uv export` with the required format and dependency selection |
| Build distributions | `uv build` |

Use `uv add` when the project needs the dependency, and `--with` for a one-off command. For new projects, do not substitute pip, pipx, Poetry, manually managed environments or the `uv pip` compatibility interface for uv's project workflow. The [CLI reference](https://docs.astral.sh/uv/reference/cli/) covers exact options; [tool environments](https://docs.astral.sh/uv/guides/tools/) are separate from project dependencies. Existing projects retain their established commands.

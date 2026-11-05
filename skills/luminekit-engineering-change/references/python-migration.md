# Explicit Python tooling migrations

Read this only when the user requested migration. Existing versions and tooling are fixed constraints for ordinary implementation work. Introducing a new package inside an established workspace does not automatically authorize migrating that workspace.

## Preserve the existing contract first

Inventory supported Python versions, dependency constraints and markers, private indexes, editable/local sources, optional extras, task dependencies, entry points, package data, build backend, CI and release consumers. A tooling migration does not itself authorize raising the Python floor. Preserve behavior before removing the previous owner.

| Requested move | Approach |
| --- | --- |
| pip/requirements to uv | Establish `pyproject.toml` metadata; use `uv add -r requirements.txt` when appropriate, and classify dev requirements into groups. Review constraints, hashes, markers, includes and index options rather than filtering lines with a shell loop. |
| Poetry to uv | Preserve package metadata, extras, sources, workspaces and constraints; review how uv represents each before retiring Poetry's configuration/lock. |
| setup.py/setup.cfg to pyproject | Transfer build metadata, entry points, included files and dependency roles; keep a backend that supports the actual package. Do not delete MANIFEST.in or build files until their responsibilities have a replacement. |
| Black/isort/flake8 to Ruff | Map enabled rules and exceptions, review formatting/fix churn, and update the owning commands/CI together. |
| mypy/pyright to ty | Review supported typing features/plugins, target interpreter, stubs and diagnostic differences. Passing a different checker is not automatically equivalent coverage. |
| pre-commit to prek | Preserve requested checks and pinned revisions; hook installation is a separate environment change. |

For uv, manage ongoing additions/removals with `uv add`/`uv remove`, synchronize, and retain `uv.lock`. Compare the resulting package metadata and the supported interpreter/environment matrix. See uv's [pip migration guide](https://docs.astral.sh/uv/guides/migration/pip-to-project/).

Move single-file utilities with dependencies to [inline script metadata](python-scripts.md) when that is the requested product; do not wrap them in a package unnecessarily. Reuse [quality-tool configuration](python-quality.md) only for the migrated checks in scope.

Retire old requirements, locks, configs or environments only after locating their consumers and confirming their replacement. Do not delete shared environments, unrelated packaging files or consumer exports merely because the new tool has equivalents. Update developer documentation and CI so the chosen owner is clear.

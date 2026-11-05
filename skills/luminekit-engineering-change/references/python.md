# Python implementation concerns

Follow the supported interpreter and existing runner. Keep fixtures isolated and test consequential cleanup behavior.

When a contract requires exact decimal values, retain their source representation and use appropriate decimal arithmetic rather than introducing binary-floating error. The [decimal documentation](https://docs.python.org/3/library/decimal.html) supplies arithmetic behavior; the actual contract supplies precision and rounding policy.

## Existing projects and new-project defaults

Inspect `requires-python`, packaging/build configuration, lockfiles, CI and configured formatter, checker and test runner. Use syntax and standard-library APIs supported by the declared interpreter floor, not merely the installed interpreter. Keep existing Python versions and tooling, including pip/Poetry, mypy/pyright, unittest and existing build backends. An ordinary implementation change must not upgrade the interpreter, replace tools or reorganize the package. A separately requested migration has its own scope.

For **new projects, use uv exclusively for Python environment and dependency management, and Python 3.14 or newer**. This is the project default, chosen to benefit from modern runtime and tooling performance. Use a current stable interpreter supported by the delivery environment; do not silently fall back to an older interpreter or a different manager. If a constraint conflicts, surface it before creating an incompatible project. Prefer Ruff for linting/formatting, ty for types and pytest for tests; use uv_build for ordinary packages it supports. Keep one owner per check.

Read only the relevant supporting guide:

| Task | Reference |
| --- | --- |
| Create a project/package, manage dependencies, locks or uv commands | [Projects and uv](python-projects.md) |
| Configure Ruff, ty, pytest, coverage or repository quality tools | [Quality tooling](python-quality.md) |
| Write a standalone script, declare inline dependencies or lock it | [Scripts](python-scripts.md) |
| Explicitly requested tooling migration | [Migration](python-migration.md) |

## Values and resource ownership

Construct exact decimal values from their source strings, and account for arithmetic context precision as well as construction. Round only where the domain contract calls for it; ambient context must not silently change a promised exact total.

Use context managers for owned streams and other scoped resources. Preserve caller-owned resources and useful exceptions. Validate before destructive effects where practical; a context manager closes a stream but does not undo truncation or make a multi-step operation atomic. Exercise consequential failure cleanup through the shared verification procedure.

# Python quality tooling

Apply these defaults to a new uv project. In existing projects, keep the configured formatter, linter, type checker, tests and versions; do not replace them during an ordinary code change.

## Ruff and ty

Use Ruff for both formatting and linting, including imports and supported modernization checks, rather than stacking Black/isort/flake8 equivalents. Start new projects with broad rules and explicit, explained exceptions. `ALL` enables new rules as Ruff evolves, so review tool/lock updates and resolve incompatible rules rather than broadly suppressing diagnostics. The [Ruff linter guide](https://docs.astral.sh/ruff/linter/) explains rule selection and fixes.

For a new Python 3.14 baseline, for example:

```toml
[tool.ruff]
target-version = "py314"
line-length = 100

[tool.ruff.lint]
select = ["ALL"]
# D: use the project's documentation conventions.
# COM812/ISC001: avoid competing with formatter decisions.
ignore = ["D", "COM812", "ISC001"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]  # Assertions are intentional in tests.

[tool.ty.environment]
python-version = "3.14"

[tool.ty.terminal]
error-on-warning = true

[tool.ty.rules]
possibly-unresolved-reference = "error"
unused-ignore-comment = "warn"
```

Align targets with the selected project floor, including a newer floor. Ruff's [configuration](https://docs.astral.sh/ruff/configuration/) and ty's [configuration reference](https://docs.astral.sh/ty/reference/configuration/) own exact settings. `python-version` belongs under `tool.ty.environment`, not directly under `tool.ty`. Annotate public boundaries and meaningful domain values; fix type errors instead of adding broad `Any` or ignores. Retain a narrow suppression only with its reason.

```sh
uv run ruff format --check .
uv run ruff check .
uv run ty check
```

Use `ruff format` to format and review `ruff check --fix` changes before keeping them. Neither formatting nor static checks establishes runtime correctness.

## Pytest and coverage

Use pytest with pytest-cov in new projects. Organize tests under `tests/`; prefer focused assertions, parametrized cases and scoped fixtures that release resources. Use `tmp_path` for owned temporary files, `monkeypatch` for environment changes and `capsys`/`caplog` for CLI/logging boundaries. Keep external services deterministic and use real local implementations when practical. See [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html).

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--strict-config --strict-markers"

[tool.coverage.run]
branch = true
source = ["example_package"]

[tool.coverage.report]
show_missing = true
fail_under = 80
```

Replace the coverage source with the actual import package. An 80% minimum is a starting new-project gate; add meaningful branch/failure cases rather than treating the number as sufficient. Preserve existing coverage requirements. This uses the supported [pytest TOML ini table](https://docs.pytest.org/en/stable/reference/customize.html) and [coverage configuration](https://coverage.readthedocs.io/en/latest/config.html).

Run `uv run pytest --cov --cov-report=term-missing` when coverage is configured. Shared [verification](verification.md) owns choosing meaningful checks, resource failure cases and claims about what actually ran.

## Repository quality tools

Use the following where relevant when establishing a new repository or when their setup is requested. Keep the existing suite in established projects. These are tool choices, not a requirement to install an entire suite for every change.

| Surface | Tool and purpose |
| --- | --- |
| Local check orchestration | lefthook, prek, or hk |
| Shell scripts | [ShellCheck](https://www.shellcheck.net/), static shell diagnostics |
| Accidental secrets | [detect-secrets](https://github.com/Yelp/detect-secrets), with reviewed baseline changes |
| GitHub Actions syntax | [actionlint](https://github.com/rhysd/actionlint) |
| GitHub Actions security | [zizmor](https://docs.zizmor.sh/) |
| Python dependency advisories | [pip-audit](https://pypi.org/project/pip-audit/), run against the intended resolved environment |
| Dependency update proposals | [Dependabot](https://docs.github.com/en/code-security/dependabot), for uv and relevant workflow dependencies |

Document check commands in the existing task runner or CI owner; a Makefile is useful when the project wants it, not mandatory scaffolding. For uv, lint/type/test commands should run in its environment; CI uses the locked dependency workflow. Keep local checks and CI consistent. Prefer versioned tool/hook revisions, minimal workflow permissions and protected secret handling. Review updates and alert exceptions instead of hiding them in broad baselines.

Do not install agent command-interception hooks or PATH shims. Documenting prek as a development option does not install a Git hook or change the user's environment. No extra script bundle is needed to use this guidance.

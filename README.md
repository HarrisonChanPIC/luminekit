# LumineKit

LumineKit provides reusable skills for working with AI agents on documentation, engineering and selected business tasks. Most skills share a proportional Understand → Plan → Execute → Review → Release workflow.

The collection lives in `skills/` and uses the [Agent Skills format](https://agentskills.io/specification). Install it with the [Vercel skills CLI](https://github.com/vercel-labs/skills); no LumineKit application or server is required.

## Install

Use Node.js 22.20 or later. From the project where you want to use the collection:

```sh
npx skills add arxbombus/luminekit --skill '*'
```

Choose your agents when prompted, or select them explicitly:

```sh
npx skills add arxbombus/luminekit --skill '*' -a claude-code codex qoder
```

Add `-g` to install for your user account across projects. The CLI handles each agent's destination directories. If the repository is private, recipients need repository access and configured Git authentication. Remote commands require the collection to be available at that repository; local installation works before publication.

Installation ends after installation and verification. Adopting or restructuring the receiving project's documentation requires its own requested scope.

To inspect or install a local checkout, replace the source with its path. Run installation from the receiving project:

```sh
npx skills add /path/to/luminekit --list
npx skills add /path/to/luminekit --skill '*' -a codex
```

Install complete skill folders, including `references/`. Keep their folder names and sibling layout intact. The recommended full install includes all 22 skills. Each skill folder is self-contained and names the other skills it hands off to, such as Workflow; selecting one skill does not automatically install those siblings. Named external skills must be resolved separately in the receiving environment.

For a smaller documentation collection, install these seven skills together:

```sh
npx skills add arxbombus/luminekit \
  --skill luminekit-workflow luminekit-setup luminekit-docs luminekit-docs-review \
  luminekit-docs-maintain luminekit-continue luminekit-arena
```

This selection includes every skill the documentation skills name, including Arena's conditional orchestration procedure used by Setup. For other custom selections, also include the collection skills named by the selected skills.

To create or maintain agent skills in any project, install the authoring skill with Workflow and Arena's independent-run procedure:

```sh
npx skills add arxbombus/luminekit \
  --skill luminekit-agent-skills-maintenance luminekit-workflow luminekit-arena
```

For a standalone interview skill:

```sh
npx skills add arxbombus/luminekit --skill luminekit-grill
```

## Use

Ask for the task you want to complete, naming a skill when useful. For example: “Use `luminekit-engineering-plan` to help me plan this feature.” In Codex, an installed skill can also be invoked as `$luminekit-engineering-plan`. When native discovery is unavailable, a file-capable agent can read the named skill’s `SKILL.md` in its installed folder.

The workflow is applied once per task. Specialists reuse the current context and load supporting references only when relevant. The skills do not provide external tools, credentials, company policies or approval authority; those come from the actual environment and task.

Grill works independently of Workflow and returns clarified intent and decisions in the reply. You can also invoke it directly: “Use `luminekit-grill` to grill me on this plan.” Saved documentation and implementation require their own requested scope.

The installer supports Claude Code, Codex and Qoder. Installing files does not establish identical behavior in every client; verify the workflows you rely on in your actual agent and version.

## Skills

| Task | Skill |
| --- | --- |
| Coordinate work through the five-stage workflow | [luminekit-workflow](skills/luminekit-workflow/SKILL.md) |
| Interview the user to clarify a plan, decision or idea | [luminekit-grill](skills/luminekit-grill/SKILL.md) |
| Create, revise, audit or retire agent skills in any project | [luminekit-agent-skills-maintenance](skills/luminekit-agent-skills-maintenance/SKILL.md) |
| Author/read knowledge, find and record facts in a work folder, establish catalogs or restructure documentation | [luminekit-docs](skills/luminekit-docs/SKILL.md) |
| Review documentation | [luminekit-docs-review](skills/luminekit-docs-review/SKILL.md) |
| Configure knowledge/workspace locations, catalogs and attribution | [luminekit-setup](skills/luminekit-setup/SKILL.md) |
| Maintain documentation and close work | [luminekit-docs-maintain](skills/luminekit-docs-maintain/SKILL.md) |
| Capture or resume missing work context | [luminekit-continue](skills/luminekit-continue/SKILL.md) |
| Explain code or trace a proposed change's impact | [luminekit-engineering-understand](skills/luminekit-engineering-understand/SKILL.md) |
| Diagnose a failure or ineffective changes | [luminekit-diagnose](skills/luminekit-diagnose/SKILL.md) |
| Test an assumption behind repeated failures | [luminekit-attack-the-premise](skills/luminekit-attack-the-premise/SKILL.md) |
| Compare independent approaches to a difficult decision | [luminekit-arena](skills/luminekit-arena/SKILL.md) |
| Design an engineering change | [luminekit-engineering-plan](skills/luminekit-engineering-plan/SKILL.md) |
| Implement an engineering change | [luminekit-engineering-change](skills/luminekit-engineering-change/SKILL.md) |
| Review code, a plan or a fix | [luminekit-engineering-review](skills/luminekit-engineering-review/SKILL.md) |
| Independently challenge a consequential or uncertain result | [luminekit-adversarial-review](skills/luminekit-adversarial-review/SKILL.md) |
| Prepare or perform an authorized engineering release | [luminekit-engineering-release](skills/luminekit-engineering-release/SKILL.md) |
| Plan, draft, revise or review email/chat | [luminekit-corporate-correspondence](skills/luminekit-corporate-correspondence/SKILL.md) |
| Draft an agreement, SOW or amendment | [luminekit-contract-draft](skills/luminekit-contract-draft/SKILL.md) |
| Review a contract/NDA or verify returned changes | [luminekit-contract-review](skills/luminekit-contract-review/SKILL.md) |

[Quotation](skills/luminekit-corporate-quotation/SKILL.md) and [approval](skills/luminekit-corporate-approval/SKILL.md) are experimental business skills included in the full collection. They require your actual commercial terms, forms and policies. Quotation bundles a blank company cover template and a fill script that takes every value as explicit input.

Some skills bundle Python scripts: Docs' folder fingerprinting uses only the standard library, and Quotation's template filling runs with [uv](https://docs.astral.sh/uv/), which installs its declared dependency. The agent can install uv when it is missing.

## Updates and removal

```sh
npx skills check
npx skills update
npx skills remove luminekit-docs-review
```

Use `-g` for global installations when updating or removing. Review changes before updating customized installed copies; keep reusable changes in the source repository. Removing a skill that other installed skills name leaves them without that handoff.

## Development

Edit `skills/` directly. Repository checks use uv-managed Python 3.14; their dependencies and lock are development tools, separate from the Node-based external installation CLI. Follow `luminekit-agent-skills-maintenance` for skill changes and [AGENTS.md](AGENTS.md) for project rules.

```sh
uv sync --locked
mise run check
mise run test
```

`mise run check` runs the same locked commands as CI: Ruff lint/format checks (including bundled skill scripts), skill metadata/name/license and bundle closure checks, local Markdown links/ordinary heading anchors, and the pinned OKF checker plus reserved-file checks on `tests/fixtures/okf/valid`. `mise run test` adds regression tests, including the upstream OKF tests and tests for bundled skill scripts. No installation matrix or distribution smoke test runs.

Without mise, run the individual commands in [mise.toml](mise.toml). `scripts/check_skills.py [skills-root] [skill-name ...]` checks only selected siblings when names are given. Every resource must be reachable from its `SKILL.md`; links and resource symlinks stay within the bundle. `scripts/check_links.py [paths ...]` checks actual Markdown links/images, reference links and ordinary headings, including Unicode/punctuation and duplicate suffixes. It ignores fenced/inline code and external URL availability. HTML/generated anchors and renderer-specific heading extensions are outside its coverage. For an OKF bundle, `--bundle-root PATH` resolves leading-slash paths against that bundle and checks reserved index/log structures; maintained-route link policy is stricter than OKF's tolerant consumer contract.

Initial OKF CI coverage is explicit developer fixtures, not a tracked production knowledge bundle. Missing optional metadata and unknown types/keys are accepted; warnings remain advisory. The [vendored checker notice](scripts/vendor/README.md) records its revision, MIT license and limitations. Checks do not rewrite docs, install consumer validators, fetch linked websites or prove retrieval, freshness, native loading or runtime attestation.

[mise.toml](mise.toml) pins uv and optional Git tooling. Run `mise install` and `mise run setup` to install development dependencies and local Lefthook hooks. [lefthook.yaml](lefthook.yaml) runs content checks before commits, regression tests before pushes and Conventional Commit message checks with Cocogitto. These hooks are not installed in receiving projects by the skills. [GitHub Actions](.github/workflows/check.yml) runs the same check/test tasks on pushes and pull requests.

The Vercel CLI remains an external distribution tool. Use the installation commands above when you choose to install; source checks do not require Node. The Git repository is the distribution source; no npm package publication is needed.

## License

All rights reserved; see [LICENSE](LICENSE). This collection is not offered under an open-source license. Availability of an install command does not grant permission to use or redistribute the content.

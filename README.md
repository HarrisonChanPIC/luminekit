# LumineKit

LumineKit provides reusable skills for working with AI agents on documentation, engineering and selected business tasks. The skills share a proportional Understand → Plan → Execute → Review → Release workflow.

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

Install complete skill folders, including `references/`. Keep their folder names and sibling layout intact. The recommended full install includes all 20 skills. Each skill folder is self-contained and names the other skills it hands off to, such as Workflow; selecting one skill does not automatically install those siblings. Named external skills must be resolved separately in the receiving environment.

For a smaller documentation collection, install these five skills together:

```sh
npx skills add arxbombus/luminekit \
  --skill luminekit-workflow luminekit-docs-adopt luminekit-docs-review \
  luminekit-docs-maintain luminekit-continue
```

This selection includes every skill the documentation skills name. For other custom selections, also include the collection skills named by the selected skills.

To create or maintain agent skills in any project, install the authoring skill with Workflow:

```sh
npx skills add arxbombus/luminekit \
  --skill luminekit-agent-skills-maintainence luminekit-workflow
```

## Use

Ask for the task you want to complete, naming a skill when useful. For example: “Use `luminekit-engineering-plan` to help me plan this feature.” In Codex, an installed skill can also be invoked as `$luminekit-engineering-plan`. When native discovery is unavailable, a file-capable agent can read the named skill’s `SKILL.md` in its installed folder.

The workflow is applied once per task. Specialists reuse the current context and load supporting references only when relevant. The skills do not provide external tools, credentials, company policies or approval authority; those come from the actual environment and task.

The installer supports Claude Code, Codex and Qoder. Installing files does not establish identical behavior in every client; verify the workflows you rely on in your actual agent and version.

## Skills

| Task | Skill |
| --- | --- |
| Coordinate work through the five-stage workflow | [luminekit-workflow](skills/luminekit-workflow/SKILL.md) |
| Create, revise, audit or retire agent skills in any project | [luminekit-agent-skills-maintainence](skills/luminekit-agent-skills-maintainence/SKILL.md) |
| Review documentation | [luminekit-docs-review](skills/luminekit-docs-review/SKILL.md) |
| Establish or migrate documentation navigation | [luminekit-docs-adopt](skills/luminekit-docs-adopt/SKILL.md) |
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

[Quotation](skills/luminekit-corporate-quotation/SKILL.md) and [approval](skills/luminekit-corporate-approval/SKILL.md) are experimental business skills included in the full collection. They require your actual commercial terms, forms and policies.

## Updates and removal

```sh
npx skills check
npx skills update
npx skills remove luminekit-docs-review
```

Use `-g` for global installations when updating or removing. Review changes before updating customized installed copies; keep reusable changes in the source repository. Removing a skill that other installed skills name leaves them without that handoff.

## Development

Edit `skills/` directly. Node dependencies are development tools only; recipients need neither this repository's development setup nor a LumineKit executable.

For skill authoring and maintenance, follow `luminekit-agent-skills-maintainence`; repository-specific conventions remain in [AGENTS.md](AGENTS.md).

```sh
npm ci --ignore-scripts
npm run check
npm run skills:list
npm test
```

`npm run check` validates skill frontmatter and that each skill is self-contained: no local Markdown link leaves its folder, every bundled file is reachable from its `SKILL.md`, and every named `luminekit-*` skill exists. It also validates local Markdown links and heading anchors using remark. It does not fetch external websites, resolve external skill availability or prove agent behavior. `npm run skills:list` verifies discovery using the pinned skills CLI. `npm test` also tests full, documentation-only and authoring-skill installations into temporary projects, using both symlinks and copies for Claude Code, Codex and Qoder. It checks installed file contents, that each selection includes the collection skills it names and preservation of unrelated files.

Development dependencies pin patched `glob` and `minimatch` versions through npm overrides while upstream tools still request older versions. Recheck those overrides when updating the validation tools.

[mise.toml](mise.toml) pins Node and the optional Git tooling. With mise, run `mise install` and `mise run setup` to install development dependencies and local Lefthook hooks. `mise run check` runs content checks; `mise run test` also tests installations. [lefthook.yaml](lefthook.yaml) runs content checks before commits, installation tests before pushes and Conventional Commit message checks with Cocogitto. Installation does not register these development hooks in receiving projects.

[GitHub Actions](.github/workflows/check.yml) runs `npm test` on pushes and pull requests.

The Git repository is the distribution source. Publish reviewed source changes to make them available through the remote install commands; no npm package publication is needed. Keep [AGENTS.md](AGENTS.md) aligned with the source layout.

## License

All rights reserved; see [LICENSE](LICENSE). This collection is not offered under an open-source license. Availability of an install command does not grant permission to use or redistribute the content.

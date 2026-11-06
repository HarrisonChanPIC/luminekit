# Repository instructions

Follow [luminekit-workflow](skills/luminekit-workflow/SKILL.md). Read only the relevant specialist and triggered references. When a repository skill is not available through native discovery, read its `skills/<name>/SKILL.md` directly.

For agent-skill creation, maintenance, audit or retirement, follow `luminekit-agent-skills-maintenance`.

For this repository's optional delegated work, use the selected [roles and execution profile](docs/roles-and-execution.md). It is not a default for projects installing the skills.

`skills/` is the single editable source for distribution through the Vercel skills CLI. Keep the collection's rights-reserved license notice in skill metadata. Do not add an application to install the skills.

[README.md](README.md) owns installation, the skill catalog and development instructions. Keep repository-specific agent instructions here and reusable procedures in their owning skills. Do not reintroduce the retired Go application, plans or evaluation archives as prerequisites.

Run `mise run test` after changes; it includes locked Python lint/format, metadata/bundle/name, local Markdown links/anchors, OKF fixtures and regression checks. Installation matrices and distribution smoke checks are excluded by the user's direction. Report actual checks separately from unexercised agent behavior. Do not publish, push or create a release unless requested.

Local work uses root `.agent-workspace/`, ignored from distribution. Keep each real initiative's entry compact and link focused plans/evidence. Current project guidance remains usable without that local state.

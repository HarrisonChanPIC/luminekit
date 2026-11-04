# Repository instructions

Follow [luminekit-workflow](skills/luminekit-workflow/SKILL.md). Read only the relevant specialist and triggered references. When a repository skill is not available through native discovery, read its `skills/<name>/SKILL.md` directly.

`skills/` is the single editable source for distribution through the Vercel skills CLI. Keep each skill a self-contained bundle: supporting references stay with their skill and are reachable from its `SKILL.md`, links stay inside its folder, and sibling skills are named in backticks (“the `luminekit-diagnose` skill”) rather than linked. When changing a shared resource, check its callers. Do not maintain separate skill bodies for different agents or add an application to install them.

[README.md](README.md) owns installation, the skill catalog and development instructions. Keep repository-specific agent instructions here and reusable procedures in their owning skills. Do not reintroduce the retired Go application, plans or evaluation archives as prerequisites.

Run `npm run check` after changes; it validates skill metadata, bundle self-containment, skill names, and local Markdown links and anchors. Use the pinned CLI to test changed installation instructions in a temporary project, preserving existing installations. Report actual checks separately from agent behavior that was not exercised. Do not publish, push or create a release unless requested.

# Push and pull requests

For a push, resolve the actual remote URL, source revision and destination ref. A force/rewrite needs its own approved scope and an observed remote-object lease; use the project's actual hooks and inspect any hook-produced changes and resulting remote ref.

For PR wording, lead with the concrete problem and resulting behavior, then meaningful validation and material risk/limits. Use the repository's template where applicable, preserve relevant author-written content and read back a requested saved description.

For actual creation/update, verify source/target repositories, refs, revisions and provider policy. Creation, metadata editing, linked-item changes, auto-completion, deletion and merge are distinct effects under the [engineering authority rules](action-authority.md). Avoid consequential convenience flags outside the approved effect.

A branch can move between inspection and creation; before/after reads do not enforce an atomic expected revision. Where a grant or policy requires an exact revision, use a supported guard or an expressly approved tolerance allowed by that policy. Without either, hold the mutation and identify the missing capability. Do not invent a revision flag or temporary pinning branch. Compare returned identities with the approved result.

Before merging, check actual approval and current review/check/policy state, including the approved merge method and any source deletion or bypass. Use an established applicable release procedure rather than imposing an additional universal sequence.

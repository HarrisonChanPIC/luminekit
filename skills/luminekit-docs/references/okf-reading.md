# Read only the knowledge needed

Read when consuming an OKF concept or bundle. The authority is [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md); project vocabulary adds guidance without overriding its tolerant exchange contract.

Start at the supplied concept or actual project entry. Use relevant index descriptions to choose owners; a valid direct route need not restart at the root. Missing/stale/incomplete indexes permit bounded filename, frontmatter or content search. Follow necessary dependencies, possibly several owners, and stop when the reader's question is answered. Read the full relevant procedure; an index summary is not factual evidence.

For identification, filtering or cataloging, prefer filenames, index entries and the relevant frontmatter over loading concept bodies. Inspect bodies only when the selection cannot be resolved from those signals, a targeted content search is needed or the task needs their substance. Once selected, read the complete relevant claims/procedure and necessary sources; metadata-only discovery does not answer a factual question.

A bundle is a directory tree. Concept identity is its bundle path without `.md`. Every Markdown file except reserved `index.md` and `log.md` is a concept, including a README inside that boundary. `type` is the only always-required concept field. Treat unknown types as generic concepts, preserve unknown keys on round-trip and continue with missing optional fields/indexes or broken links. Report a route that prevents the requested task rather than treating broken links as universal format rejection. An unfamiliar declared version calls for best-effort consumption.

Use title/description/type/tags for selection. Open the asset named by `resource` when answering a claim that requires asset evidence, and follow the relevant `sources` entries and locators. A source `resource` can also describe a population/scope that cannot be opened: disclose that limit. Claim footnote labels join to stable `sources[].id`, independent of list order. A description, source link or generation event does not verify a claim. If an asset is inaccessible, say which claim remains unconfirmed; do not reconstruct its contents from a confident summary.

Interpret optional signals separately:

| Signal | Reading decision |
| --- | --- |
| `generated: {by, at}` | `by` identifies the producer; `at`, when present, dates the last meaningful content change. A by-only mapping supplies no change time. Neither form confirms the claims. |
| `verified` list or bare `{by, at}` mapping | Normalize a mapping to one event. Inspect checked scope/revision; later edits may be unverified. |
| No `verified`; only non-human actors; any `human:` actor | Unverified; machine-confirmed; human-reviewed, respectively. Advisory signals, never access control or proof of applicability. |
| `status` | `draft`: not yet reviewed/possibly incomplete; `stable`: ready for consumption; `deprecated`: retained but no longer current. Absent means stable. Readiness is separate from verification, implementation, transaction approval, signature and effective date. |
| `stale_after` | Stale exactly when `now >= stale_after`. Revalidate rather than silently refresh/delete. Source changes can invalidate an unexpired claim. |
| Source `author`, `usage_count`, `last_modified` | Objective authority/liveness/recency signals, not credibility scores. Counts use shared `usage_window: {from, to}` unless overridden per source; compare coarse trends, not unlike event kinds as precise rankings. |

Timestamp-valued fields are offset-aware ISO 8601 datetimes. Actors use `<producer>/<version>`, `human:<id>` or `process:<id>`. Read saved aliases as identifiers, without inferring legal names or authority. Optional absence supplies no evidence. An advisory human-reviewed tier may derive from a historical event; inspect its checked scope/revision before applying it to later content. A saved identity, `stable` status or new generation timestamp is not a new verification event. Legacy v0.1 `timestamp` may be a fallback when `generated` is absent, and legacy body Citations may still be read when needed; reading does not authorize migration.

Resolve a leading `/` in bundle links and path-valued fields against the bundle root, not filesystem root. Relative paths resolve from their document; absolute URLs remain external. This applies to `resource`, `sources[].resource`, `computation`, `executor.resource` and `attester.resource`, except non-path source scope descriptors. `references/` is a useful convention, not a required directory. Relationships derive meaning from link context, not an invented typed-edge schema.

When encountering `type: Attested Computation`, read [computations](okf-computations.md). Definition verification and per-run attestation are different. Ordinary reading does not authorize executing linked code.

For authoring, use [OKF authoring](okf-authoring.md); for an unfamiliar domain, use only the relevant [catalog guidance](catalogs.md). Native writer types such as `feedback` remain consumable alongside project-specific types. Keep contradictory/current/proposed claims explicit until the applicable authority resolves them.

# Distinguish common authoring decisions

Read for examples, not a mandatory template. All business facts below are synthetic. Optional attribution is omitted to avoid inventing a writer or verification event.

An engineering concept `development.md` in an OKF bundle:

```yaml
---
type: Guide
title: Local checks
description: Run local checks and distinguish source inspection from executed tests.
tags: [development]
sources:
  - id: task-config
    resource: ../mise.toml
---
```

Its body names only actual commands supported by task configuration, with scope and failures. The corresponding directory index entry copies the description:

```markdown
* [Local checks](development.md) - Run local checks and distinguish source inspection from executed tests.
```

A business concept may instead be:

```yaml
---
type: Reference
title: Harbor renewal
description: Entity, proposed renewal period and source limits for the Harbor engagement.
status: stable
sources:
  - id: offer-v3
    resource: ../records/Harbor-offer-v3.docx
    title: Synthetic Harbor offer, edition 3
---
```

Its supported body can say: “North Harbor Ltd is the proposed buyer for the 2027 renewal; offer edition 3 is a draft, with signature/effective date unconfirmed.[^offer-v3]” A footnote definition `[^offer-v3]: Offer edition 3, parties and term sections` joins to the source by ID. `stable` describes this accurate concept, not a signed agreement. Missing fee/currency remain unknown; a number is not supplied as zero. If the source cannot be opened, answer: “The brief reports a proposed 2027 renewal; I could not confirm edition 3 or its operative terms because the native offer is unavailable.”

The concept's bundle path supplies its concept identity. Its body and ordinary source links carry the engagement context; no extra identity field is needed. Preserve existing scoped bilingual aliases and ambiguity behavior where a real consumer uses them. The original offer remains authoritative for terms.

A native memory writer may use `type: feedback`; a domain author may use `type: RenewalWindow`. Consume both as concepts without relabeling. On updating an existing concept with an unfamiliar `retention_class: restricted`, preserve the key and its value, keep an adequate description, and change only supported content/provenance. Do not claim to understand an unknown extension's policy; consult its owner when the task depends on it.

## Generation and verification

These actors, instants and performed checks are synthetic examples, not facts to copy into a project. Suppose project instructions record a user-selected alias `human:maple`, and the writer's runtime actually identifies `reference_agent/model-v1`.

```yaml
generated: {by: reference_agent/model-v1, at: '2026-11-05T09:00:00Z'}
verified:
  - {by: reference_agent/model-v1, at: '2026-11-05T09:10:00Z'}
```

The accompanying body explains that the agent compared the documented fee and period against offer edition 3; signature/effectiveness were outside the check. Writing the brief alone would justify no `verified` event. The user's request did not make the generator `human:maple`.

If Maple later explicitly confirms those claims against edition 3, append the actual human event with its actual instant and describe its scope. A formatter pass changes neither event. A later edition-4 change updates generation when attributed and qualifies edition-3 verification as historical; it does not silently acquire Maple's review. A re-confirmation of unchanged content can add verification without changing generation. A bare `verified: {by, at}` mapping has the same meaning as a one-event list.

## A small catalog

A project convention page might record: `Guide` means a task procedure, with local checks as its example; `Reference` means factual lookup, with the renewal brief as its example; `development` is the used cross-cutting tag; attribution follows the alias saved in `AGENTS.md` and actual machine identities; source claims name the original edition and relevant section; document readiness and actual checks use the standard lifecycle/trust families. It can state that no extra fields are selected. Use actual local owner links in a real catalog. This is sufficient without a registry or a separate file per vocabulary category.

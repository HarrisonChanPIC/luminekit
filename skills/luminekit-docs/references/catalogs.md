# Choose a small useful vocabulary

Use during project setup or when an actual documentation choice needs clarification. Establish a short human-readable Markdown owner for the conventions in use. Reconcile an existing useful page before creating another. Link it from the actual project instructions and relevant authoring route, outside disposable scratch. If it is inside an OKF bundle, it is an ordinary typed concept; the word catalog introduces no new reserved filename or file format.

## Record choices that affect reading or writing

| Convention | What the small catalog records |
| --- | --- |
| Types | Used names, meaning and a distinguishing example or real owner. Reuse descriptive existing labels and native writer types; additional descriptive values need no registration. |
| Tags and aliases | Used cross-cutting labels, preferred spellings and any actual equivalent terms. Explain scope where an alias could identify two subjects. Record that tags are unused when appropriate rather than manufacturing a vocabulary. |
| Attribution | A route to the saved human alias/omission in project instructions, plus the standard agent/tool and process actor forms. Actual events carry actual actors; a list of hypothetical models adds no value. |
| Standard metadata | Which optional fields help this project and where their shared OKF semantics are documented. Identify local authoring preferences as preferences, without turning optional standard fields into universal requirements. |
| Sources and identity | How readers find originals and relevant revision/page/sheet/section evidence; reuse existing native identifiers and scoped aliases where needed. Concept identity already comes from its bundle path. |
| Lifecycle and review | The project use of `draft`, `stable`, `deprecated`, meaningful-change attribution, performed verification and revalidation. Keep document readiness distinct from delivery progress, approval and effective dates. |
| Domain terms, when used | Supported entity roles, units, currency/tax basis and period meanings that would otherwise be ambiguous. Link their existing owners rather than copying entity records into the catalog. |

Keep bundle homes, workspace choice and harness configuration in the project convention owner, with a short route here if separate. Link [standard reading](okf-reading.md), [authoring](okf-authoring.md) or an available canonical specification instead of copying a full manual. A later useful category or spelling updates this page without a setup rerun, registry or schema change.

For engineering work, familiar labels include `Guide` (accomplish a task), `Reference` (look up facts/interfaces), `Runbook` (triggered operation with checks/recovery), `Plan` (proposed work and acceptance), `ADR` (decision/rationale), `Spec` (intended requirements). Offer fitting choices, without creating every category. The same `Guide` or `Reference` can describe business work; preserve useful existing domain types rather than imposing an engineering taxonomy.

For administrative/business work, a project can be an opportunity or engagement without a signed contract. Explain entity roles, bilingual aliases, currency/units, tax basis, period, edition and effective terms only where relevant and supported. Unknown differs from zero/false/not applicable. Keep approval, signature, current/proposed and actual/proposed paths in their real source-backed owner; OKF `stable` is no business approval.

Keep original PDFs, Word documents, spreadsheets and signed records controlled with identity, revisions and access. Concepts point to relevant page/sheet/section; conversion does not silently replace originals. Preserve deterministic lookup contracts: stable IDs, scoped aliases/keywords, ambiguity behavior and native source lineage. Source code, embeddings and conversion of every original are not prerequisites.

## Keep the format portable

Use standard OKF fields and ordinary Markdown by default. Do not add project IDs, engagement IDs, custom approval states, relationship fields or creation timestamps as a starting template. Type/tag values are vocabulary within standard fields, not a reason to invent new fields. A body statement, heading, source locator or contextual link often expresses the needed fact.

An existing consumer's unfamiliar metadata must survive a round-trip. Preserving it does not adopt it as the default for new concepts. A new producer-defined key needs a separately established user requirement that standard fields/prose cannot adequately serve, an actual consuming workflow and a small plain-language definition. Keep such exceptions sparse and review their maintenance burden with the user; ordinary setup does not propose them.

Tags are optional short-string lists. Reuse established spellings; lowercase kebab-case is one authoring choice when none exists, not a standard requirement. Link context can express supersedes, implements or depends-on without a relationship schema. Keep private real-world values out of reusable examples.

Use [synthetic examples](okf-examples.md) for common distinctions. Common standard field semantics live in [reading](okf-reading.md) and [authoring](okf-authoring.md), rather than being duplicated into every domain catalog.

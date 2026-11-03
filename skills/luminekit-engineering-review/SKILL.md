---
name: luminekit-engineering-review
license: Proprietary. All rights reserved.
description: Review selected engineering code, a diff, a plan or a returned correction against requirements, applicable standards and meaningful verification evidence. Use for requested or genuinely needed review; review-only does not authorize fixes, experiments or publication.
---

# Review actual engineering work

Use the [luminekit-workflow](../luminekit-workflow/SKILL.md) skill if its instructions are not already loaded. Reuse current task state, then continue within this skill’s scope.

Resolve the actual code, plan, diff or returned correction and its independent intended behavior/standards. A non-Git snapshot can be sufficient. Compare correctness, regression/security, standards and evidence strength without letting success in one cancel a failure in another.

| Concern | Procedure |
| --- | --- |
| Substantive code/plan correctness, standards or test strength | [Review criteria](references/review-criteria.md) |
| Independent checks, supplied logs or built/generated-entry correspondence | [Verification](../luminekit-engineering-change/references/verification.md) |
| Returned changes or prior findings | [Follow-up](references/follow-up.md) |
| Explicit adversarial review or consequential uncertainty needing deliberate challenge | [Adversarial review](../luminekit-adversarial-review/SKILL.md), retaining review-only scope |

Check findings against surrounding source, callers and counterevidence. A tool/setup failure is a check failure, not proof of a product defect; a missing check is a coverage gap. Qualified source-supported defects survive unavailable execution. Deliver all supported findings, material dispositions and performed/unperformed coverage. Review approval and a source-confirmed fix do not certify the current built/deployed result.

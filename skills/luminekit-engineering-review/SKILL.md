---
name: luminekit-engineering-review
license: Proprietary. All rights reserved.
description: Review engineering code, a diff, a plan or a returned correction against requirements, applicable standards and meaningful verification evidence.
---

# Review actual engineering work

Follow the `luminekit-workflow` skill within this skill’s scope.

Resolve the actual code, plan, diff or returned correction and its independent intended behavior/standards. A non-Git snapshot can be sufficient. Compare correctness, regression/security, standards and evidence strength without letting success in one cancel a failure in another.

| Concern | Procedure |
| --- | --- |
| Substantive code/plan correctness, standards or test strength | [Review criteria](references/review-criteria.md) |
| Independent checks, supplied logs or built/generated-entry correspondence | Verification procedure of the `luminekit-engineering-change` skill, retaining review-only scope |
| Returned changes or prior findings | [Follow-up](references/follow-up.md) |
| Consequential uncertainty at boundaries, failure paths or interactions | The `luminekit-adversarial-review` skill, retaining review-only scope |

Check findings against surrounding source, callers and counterevidence. Deliver all supported findings. Review approval and a source-confirmed fix do not certify the current built/deployed result.

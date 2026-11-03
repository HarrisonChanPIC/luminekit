---
name: luminekit-engineering-change
license: Proprietary. All rights reserved.
description: Implement an authorized engineering feature, fix, refactor or prototype with a scoped diff and meaningful verification. Use for requested changes; explanation, planning and review-only requests retain their scope and do not become edits.
---

# Implement a coherent change

Use the [luminekit-workflow](../luminekit-workflow/SKILL.md) skill if its instructions are not already loaded. Reuse current task state, then continue within this skill’s scope.

Establish the outcome, independent acceptance, allowed targets and current source/dirty state. Use actual repository conventions; preserve behavior outside scope and meaningful error, cancellation and resource semantics. Do not weaken assertions, hardcode examples or swallow failures to get green.

| Concern | Procedure |
| --- | --- |
| Substantive feature/fix, refactor, migration or prototype | [Change kinds](references/change-kinds.md) |
| Practical test-first behavior change, or explicit test-first request | [Test-first cycle](references/test-first.md) before changing that behavior |
| Independent expectations, meaningful checks or source/build correspondence | [Verification](references/verification.md) |
| Unexplained failure or repeated ineffective changes | [Diagnosis](../luminekit-diagnose/SKILL.md); use its recovery branch when continued state is uncertain |
| Requested commit, publication or deployment | Use [luminekit-engineering-release](../luminekit-engineering-release/SKILL.md) |
| Language-specific behavior | Only relevant [Python](references/python.md), [TypeScript](references/typescript.md) or [Go](references/go.md) guidance |

Inspect the actual final diff/result and run applicable project gates. A harmless prose edit needs an affected content check, not a mirrored test. If a test-first path is unavailable, report that limit without resetting working user code to manufacture red-before history. A language guide supplies no migration authority.

Promote confirmed behavior/architecture into its affected documentation owner and pointers within scope. Deliver the change, actual verification and material limitations.

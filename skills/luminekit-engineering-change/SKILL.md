---
name: luminekit-engineering-change
license: Proprietary. All rights reserved.
description: Implement an engineering feature, fix, refactor or prototype with a scoped diff and meaningful verification.
---

# Implement a coherent change

Follow the `luminekit-workflow` skill within this skill’s scope.

Use actual repository conventions; preserve behavior outside scope and meaningful error, cancellation and resource semantics.

Keep existing projects on their declared language/runtime versions and established tooling. Do not upgrade or replace those as part of an ordinary implementation change. For new projects, use current stable language/tooling defaults from the relevant language guide; new Python projects require uv and Python 3.14 or newer.

| Concern | Procedure |
| --- | --- |
| Substantive feature/fix, refactor, migration or prototype | [Change kinds](references/change-kinds.md) |
| Practical test-first behavior change, or explicit test-first request | [Test-first cycle](references/test-first.md) before changing that behavior |
| Independent expectations, meaningful checks or source/build correspondence | [Verification](references/verification.md) |
| Implementing an agreed plan with multiple units | [Unit review](references/unit-review.md) |
| Unexplained failure or repeated ineffective changes | The `luminekit-diagnose` skill; use its recovery branch when continued state is uncertain |
| Language-specific behavior | Only relevant [Python](references/python.md), [TypeScript](references/typescript.md), [Go](references/go.md) or [C#](references/csharp.md) guidance |

Inspect the actual final diff/result and run applicable project gates.

Promote confirmed behavior/architecture into its affected documentation owner and pointers within scope.

---
name: luminekit-engineering-understand
license: Proprietary. All rights reserved.
description: Explain current code, diagnose a reported symptom, or trace the impact of a proposed change using relevant repository evidence. Use for understanding and investigation; a request to explain or diagnose does not authorize a fix or implementation plan.
---

# Explain, investigate or trace impact

Follow the `luminekit-workflow` skill within this skill’s scope.

Ground the question in the actual source/revision, contracts, callers and data/runtime boundaries. A clear function explanation can finish from its relevant source. For deeper work select:

| Concern | Procedure |
| --- | --- |
| Behavior flow, affected consumers or recorded rationale | [Code and impact](references/code-and-impact.md) |
| Reported failure or performance symptom | The `luminekit-diagnose` skill |
| Repeated ineffective attempts share a factual assumption | The `luminekit-attack-the-premise` skill |
| Python output/process/SQLite evidence | Python-evidence procedure of the `luminekit-diagnose` skill |

Keep this product an explanation, diagnosis or impact analysis. A method call retains that scope; it does not authorize a fix. Check the answer against current source and independent expected behavior; code establishes behavior, while claims about motivation need recorded rationale. Return the supported explanation, affected boundary, decisive evidence and remaining uncertainty.

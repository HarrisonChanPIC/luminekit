---
name: luminekit-engineering-understand
license: Proprietary. All rights reserved.
description: Explain current code, diagnose a reported symptom, or trace the impact of a proposed change using relevant repository evidence. Use for understanding and investigation; a request to explain or diagnose does not authorize a fix or implementation plan.
---

# Explain, investigate or trace impact

Use the [luminekit-workflow](../luminekit-workflow/SKILL.md) skill if its instructions are not already loaded. Reuse current task state, then continue within this skill’s scope.

Ground the question in the actual source/revision, contracts, callers and data/runtime boundaries. A clear function explanation can finish from its relevant source. For deeper work select:

| Concern | Procedure |
| --- | --- |
| Behavior flow, affected consumers or recorded rationale | [Code and impact](references/code-and-impact.md) |
| Reported failure or performance symptom | [Diagnosis](../luminekit-diagnose/SKILL.md) |
| Repeated ineffective attempts share a factual assumption | [Premise testing](../luminekit-attack-the-premise/SKILL.md) |
| Python output/process/SQLite evidence | [Python diagnostic evidence](../luminekit-diagnose/references/python-evidence.md) |

Keep this product an explanation, diagnosis or impact analysis. A method call retains that scope; it does not authorize a fix. Check the answer against current source and independent expected behavior; code establishes behavior, while claims about motivation need recorded rationale. Return the supported explanation, affected boundary, decisive evidence and remaining uncertainty.

# Roles and execution

This repository's selected personal model preferences govern optional delegated work when those responsibilities are needed. They are not defaults for projects installing LumineKit. Direct work in one harness remains primary; roles do not require separate agents, a full panel or T3 Code. No native configuration is applied by this document.

## Selected role profiles

| Role | Selected models and reasoning | Responsibility |
| --- | --- | --- |
| Orchestrator | GPT-6 Astra, medium | Scope work, assign bounded tasks, assess resources, inspect and integrate the result. |
| Architect | GPT-6.1 Sol, xhigh; Claude Opus 5.5, medium | System boundaries, shared interfaces, ownership and cross-module invariants. |
| Module designer | GPT-6.1 Sol, xhigh; Claude Opus 5.5, medium | One module's interfaces, behavior, failures, dependencies and implementable units. |
| Implementer | GPT-6.1 Sol, medium; DeepSeek V4.1 Flash, effort unspecified; Qwen3.8-Max, effort unspecified | Scoped implementation, meaningful checks and supported corrections against reviewed decisions. |
| Reviewer | GPT-6.1 Sol, xhigh for easy/medium review; GPT-6 Astra, medium for difficult plan/architecture review | Original requirements versus the actual plan/code, with supported findings or justified no-findings. |
| Verifier | GPT-6.1 Sol, medium | Independently expected results, executable acceptance and integration checks. |
| Judge / evaluator | GPT-6.1 Sol, xhigh; GPT-6 Astra, medium for hard/difficult evaluation | Assess completed alternatives and resources; select a supported base or synthesis. |

Agent discretion applies within the selected pools and effort bounds, based on the assigned question, useful independence and available budget. Alternatives have no implied preference order. Do not silently substitute an unlisted model or exceed a selected effort. Fable is excluded from this profile. Difficult implementation-only review has no separately selected assignment; resolve that case when needed rather than expanding Astra's stated review scope.

Model names do not establish provider identifiers, account allowance or exposed controls. DeepSeek V4.1 Flash's exact provider identity remains unverified; a differently labeled Flash or V4-Pro target does not establish a match. Qwen and DeepSeek effort stays unspecified unless actual supported controls and a user choice establish it. Validate live capabilities before dispatch; unavailable choices remain explicit gaps. Saving these preferences changes no running session.

## Execution through existing skills

Apply [Workflow](../skills/luminekit-workflow/SKILL.md) once. Keep simple requests direct and choose delegation only when bounded work, useful parallelism or independent judgment warrants it. An Arena candidate is an architect, designer or implementer assignment, not an additional mandatory model role.

1. Ground original requirements, actual code, constraints and independent acceptance. For consequential decisions, use [Engineering Plan](../skills/luminekit-engineering-plan/SKILL.md): system contracts before dependent module design, module contracts before dependent implementation, and review of new or supplied plans before relying on them. Stop detailing once implementation can proceed without inventing a material decision.
2. Use [Arena](../skills/luminekit-arena/SKILL.md) for consequential unresolved alternatives and [Engineering Review](../skills/luminekit-engineering-review/SKILL.md) for plan/code assessment against original requirements. Inspect actual findings and resolve blockers before dependent work; a post-code review does not establish pre-implementation review.
3. Execute reviewed units through [Engineering Change](../skills/luminekit-engineering-change/SKILL.md), carrying concrete decisions, interfaces and acceptance into bounded briefs. [Workflow's delegation procedure](../skills/luminekit-workflow/references/delegation.md) owns actual capability selection, fresh contexts, output inspection, completed-output judging and cumulative resource accounting, including coordination, failed/discarded work and integration. No numerical resource ceiling is selected here; set task-specific budgets.
4. Verify the combined revision rather than accepting worker summaries or local tests as integration evidence. Use [Continue](../skills/luminekit-continue/SKILL.md) for actual context pressure/recovery, preserving requirements, model constraints, budgets, task IDs and pending effects. Deliver only the authorized result and state actual coverage and unknown usage honestly.

To revise or establish another profile, use [Setup's roles and models procedure](../skills/luminekit-setup/references/roles-and-models.md). These preferences are independent of optional [t3-pstack design references](https://github.com/chhoumann/t3-pstack/tree/7f64e2ba7e1aedcee95cc6e3e92eb5fda62f8b6a); current host instructions own actual tools and lifecycle, and no pstack installation or model registry is required.

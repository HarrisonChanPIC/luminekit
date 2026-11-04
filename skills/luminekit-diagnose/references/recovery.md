# Determine safe continuation

Use when caught errors, retries, partial effects or unfinished background work make continuation uncertain. A causal diagnosis does not by itself establish recovery.

Trace the affected state/error to its responsible owner. Preserve stable machine error identity and causal context under the actual stack's conventions; translated display wording is not a reliable machine discriminator. Distinguish invalid upstream state from legitimate state that needs local handling. A guard, wait or retry is appropriate only when it addresses the actual condition rather than hiding it.

Identify who can establish invariants, cleanup and recovery guarantees for absent, partial, committed and unknown state. Catching an error limits propagation, not mutations; logging is not rollback. Include still-running background work. Where no owner-supported guarantee establishes safety, hold dependent work and choose supported reconciliation, scoped disposal or escalation. A cancellation request or cleanup call returning does not prove owned work has stopped; verify quiescence and resulting state.

Finite recovery attempts need a relevant budget and safe-repeat semantics. Continuing supervision needs lifecycle ownership and observable degradation. Apply the `luminekit-engineering-release` skill for actual engineering effects or the `luminekit-corporate-correspondence` skill for email/chat effects. Make invalid state and unknown outcomes visible through an available reporting path; reporting failure grants no new notification permission.

For repeated belief-preserving fixes, use the `luminekit-attack-the-premise` skill once the common factual assumption is the question. Return the state invariant, supported recovery disposition, remaining uncertainty and next action. Remove only authorized task-owned temporary instrumentation after verification.

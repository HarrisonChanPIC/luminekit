---
name: luminekit-attack-the-premise
license: Proprietary. All rights reserved.
description: Challenge a factual assumption shared by repeated ineffective attempts, or explicitly examine whether an approach rests on a false premise. Identify a discriminating observation, follow the evidence and return a supported next direction. Ordinary diagnosis and redesign remain separate; repetition alone proves neither a false premise nor bad architecture.
---

# Test the belief before another fix

Follow the `luminekit-workflow` skill within this skill’s scope.

Challenge one factual assumption shared by ineffective attempts, or an explicitly questioned approach. A premise describes the situation; a requirement or design preference belongs in planning. Failure count alone proves neither a false premise nor bad architecture.

1. Inspect current inputs and comparable failed/successful paths. State the material shared belief as a falsifiable sentence tied to the actual attempts; split unrelated failure gates.
2. Choose the smallest observation that differs if the belief is true versus false. Examine failure/success distribution across inputs, paths, environments or times; control relevant variables rather than changing another compensating parameter.
3. Perform the authorized discriminator, or return a source-supported inference with the check explicitly unperformed. Separate failed test machinery from evidence about the premise.
4. If contradicted, stop building fixes on it and follow the factor it failed to predict. If supported within scope, ask the next causal why. If inconclusive, name the missing distinguishing evidence. Current success can retire a stale theory without proving downstream effects.
5. Trace demonstrated bad state through callers/transformations to its origin. Consider removing the condition rather than recurring compensation, while distinguishing invalid state from legitimate state requiring correct handling. Retries/guards are not inherently defects, and a finding grants no broad redesign.

Return the premise, decisive evidence, supported/contradicted/inconclusive disposition and next direction. Use the `luminekit-diagnose` skill when a supported premise still leaves the cause unresolved; reuse the investigation already done.

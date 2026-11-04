---
name: luminekit-diagnose
license: Proprietary. All rights reserved.
description: Explain a reported failure, unexpected result or ineffective implementation loop using current evidence and discriminating checks. Distinguish reproduced symptoms, supported causes, hypotheses and proposed remedies from verified fixes. Use for diagnosis and recovery analysis; a diagnosis request does not authorize changing its subject.
---

# Diagnose the actual failure

Follow the `luminekit-workflow` skill within this skill’s scope.

Establish expected versus observed behavior, causal evidence and the next supported action. Stale reports, handled warnings and failed diagnostic tools do not automatically establish a current product defect.

1. Inspect the current contract, relevant artifact/source/configuration and attempts. Trace inputs toward the first divergence; compare a relevant working path.
2. Frame falsifiable explanations and independent expected observations. Choose a focused probe that still reaches the real failure boundary; the implementation under diagnosis cannot define its own oracle.
3. Run the authorized discriminator or retain qualified static analysis. Separate symptom reproduction, cause, hypothesis, candidate remedy and verified fix. Follow the input/state/error chain toward its origin rather than stopping at the last visible symptom.
4. Recommend a scoped remedy or next check with acceptance. Apply a remedy only within an implementation request; carry valid diagnosis forward instead of restarting it. If attempts share an unsupported belief, use the `luminekit-attack-the-premise` skill.

| Concern | Procedure |
| --- | --- |
| Execution unavailable, unsafe or outside scope | [Static evidence](references/static-evidence.md) |
| Code/runtime/test/CI boundary or built-source evidence | Verification procedure of the `luminekit-engineering-change` skill, within diagnosis scope |
| Python output/process/SQLite behavior | [Python evidence](references/python-evidence.md) |
| Timing/shared-resource/lifecycle/platform-related CI failure | [CI reliability](references/ci-reliability.md) |
| Partial/unknown effects, retries, failed changes or cleanup make continuation uncertain | [Recovery](references/recovery.md) |

Deliver the supported cause or explicit uncertainty/no-current-defect result, decisive evidence and next action. This method supplies investigative discipline; domain requirements still come from their actual owners.

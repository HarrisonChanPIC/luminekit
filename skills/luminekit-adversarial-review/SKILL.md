---
name: luminekit-adversarial-review
license: Proprietary. All rights reserved.
description: Challenge a high-risk or uncertain artifact against its intended behavior and independent criteria, using independent reviewers or bounded probes when supported. Verify and combine all credible findings, including qualified static defects when execution is unavailable. Use for adversarial review; ordinary review need not invoke this method.
---

# Challenge the result

Use the [luminekit-workflow](../luminekit-workflow/SKILL.md) skill if its instructions are not already loaded. Reuse current task state, then continue within this skill’s scope.

Collect and verify problems in a scoped artifact against independent requirements. Resolve the subject/revision, affected consumers, applicable domain criteria and consequential failure conditions. The method retains every supported finding rather than choosing a winning reviewer.

1. Select bounded challenge angles/probes and benign counterexamples. Independent attempts are useful where they add evidence; read [independent runs](../luminekit-arena/references/independent-runs.md) before delegating. Keep the caller's review-only effects.
2. Inspect and collect concerns from actual attempts. A synthetic reviewer fixture is supplied evidence, not live fanout. Do not patch the subject or exploit a live target because an issue was raised.
3. Verify every returned concern, including disagreements/late results, against source, requirements and counterevidence. Qualified static defects remain findings when execution is unavailable; identify the causal path and unperformed confirmation without claiming reproduction.
4. Merge duplicate causes while retaining distinct witnesses/conditions; keep separate causes separate. Resolve contradictions from evidence, not votes/confidence. Preserve material rejected, disputed and unresolved dispositions.
5. Report supported findings and missing coverage at useful priority. For returned work, retain prior finding identities and check actual fixes, regressions and new issues. A proposed remedy or accepted response is not a verified correction.

Return scoped no-findings when justified. Available methods do not invent domain policy or certify unseen behavior.

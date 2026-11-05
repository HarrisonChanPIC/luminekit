# Consume or author an attested computation

Read only for `type: Attested Computation` or a task that depends on one. Authority: [OKF v0.2 section 10](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#10-attested-computations-concept). A narrative links to one separate computation concept per independently verified computation; directory layout is a project choice. Ordinary knowledge needs no runtime machinery.

The contract is top-level frontmatter:

- `type: Attested Computation` and its required `runtime`, which defines binding semantics (SQL binds, Python arguments, dbt vars, etc.).
- `parameters`: typed named holes, each `{name, type, required}`. Consumers supply only declared parameter values.
- `computation`: a path/URI to sanctioned logic, or, when absent, a single fenced code block under body `# Computation`. Choose one form; the file form omits the inline fence.
- `executor.resource`: run instructions/code. `executor.receipt`: fields execution must return, such as job ID, actual expanded/compiled artifact and result.
- `attester.resource`: deterministic code, with no LLM, that independently checks the receipt and returns a verdict.

Preserve provenance/lifecycle/verification fields under their ordinary semantics. Resources can be absolute URLs, relative paths or leading-slash bundle-relative paths; `references/` is conventional. A Skill, script or container behind a resource is a packaging choice, not an OKF invocation ABI.

Loading a contract grants no execution authority. Within an authorized execution task, inspect actual runtime/resources and bind values according to the declared runtime. A consuming agent must not rewrite sanctioned logic, swap its file or mutate dependencies to produce a result. Authoring a changed definition is separate scoped work, with its own revalidation; it must not masquerade as executing the existing one.

The executor returns the declared receipt. The attester independently derives the expected bound/expanded artifact, compares it with what actually ran and checks displayed-value fidelity against the authoritative result, re-read by receipt identity when applicable. A rewritten query, changed dependency, missing evidence or failing verdict cannot be reported as successful attestation. If execution/attester access is unavailable, expose that gap; do not invent a receipt/verdict or silently present the number as attested.

Section 10.5's discover/load/parameterize/execute/attest/gate sequence is informative, not a new automatic-operation mandate. For an attested-value task, surface failure, refuse a failing result, and warn or withhold a stale-definition result according to the actual task policy. On success, show the verdict with a usable receipt or evidence reference so the reader can inspect the specific run supporting the displayed value. `now >= stale_after` is the exact stale boundary. Receipts/verdicts are per-call runtime artifacts, outside the bundle, not extra frontmatter or a new protocol invented by this skill.

`verified` checks the definition against policy; attestation checks a specific execution. A stale definition can attest cleanly and a freshly verified definition still needs each run checked. In the specification's income-statement example, one narrative links revenue and profit to separate contracts: each has its own freshness, verification, runtime and per-call verdict. One successful result does not validate the other or the whole report.

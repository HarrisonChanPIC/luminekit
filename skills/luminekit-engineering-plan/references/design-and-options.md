# Design and options

Ground the approach in actual entry points, ownership and caller constraints. Specify behavior, invariants, ordering, failure modes and configuration as part of an interface, beyond its type signature. Reuse useful boundaries; introduce an abstraction for a demonstrated responsibility or variation.

Trace affected storage, wire formats, runtime/version assumptions and flags. Identify the particular uncertainty and evidence that would resolve it. Compare alternatives against established criteria such as compatibility, complexity, dependency/lifecycle ownership and failure behavior. A vendor performance claim needs a comparable workload before it can decide the design. Reopen an accepted choice only for a concrete new constraint or incompatibility.

When requirements select an implementation basis, trace its retained, adapted and replaced mechanisms into the plan. Ground replacements in actual incompatibilities or missing behavior while preserving required contracts, provenance and notices. Reading or citing the basis alone does not establish reuse; an optional study reference does not become a required design. Preserve compatible existing code and boundaries rather than redesigning them without a demonstrated need.

## Review before dependent implementation

Before implementation relies on consequential interface, representation, ownership, resource or integration decisions, review the plan against original requirements, actual callers/code and required implementation bases. This applies to newly designed and supplied plans; reuse sufficient current review rather than repeating it for each implementer. Check that the chosen mechanisms satisfy the constraints, caller examples agree with interfaces, dependencies are feasible and independent acceptance can distinguish success from failure. Resolve material design choices instead of silently leaving them for implementation.

Use a separate reviewer for consequential plans when available within authorized scope and budget; otherwise perform an explicit self-review where the selected execution assignment permits it, and disclose missing independent coverage. Required independent review remains a gate when unavailable; follow the execution-assignment procedure of `luminekit-workflow` rather than absorbing the missing role. Record the actual reviewed scope/decisions, supported findings and dispositions or justified no-findings. Resolve blocking findings before dependent implementation; unaffected work may proceed. New evidence invalidating a reviewed decision reopens that decision and its affected checks.

A small, well-constrained change can use a brief plan and self-check without another document or agent.

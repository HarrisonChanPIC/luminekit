# Sketch competing architectural shapes

Use for a consequential unresolved interface, representation, ownership or module shape. Keep sketches in the permitted planning output. The [architecture starter](../assets/architecture-sketch.md) supports these outputs; fill only the parts that resolve this task's design uncertainty.

## Derive the shape from callers

Write representative usage and two or three meaningful call sites before deriving types, including a relevant boundary or failure use. Show what each caller imports, supplies, receives and must coordinate. Ground them in affected code, contracts and recorded rationale; separate fixed requirements from choices still open.

Derive inspectable signatures, core representations, ownership/effect boundaries and module responsibilities from that usage. Trace dominant reads, writes and state transitions through the proposed structure. Include failure, cancellation or disposal where the actual contract requires them. Reconcile the declarations with the caller examples; prose promises alone are not a sketch.

## Explore and compare mechanisms

For the unresolved shape, use the `luminekit-arena` skill's **design exploration**, independent-runs and comparison/synthesis procedures. Reuse its neutral candidate brief with the grounded constraints, open choices and caller needs; request the usage and shape above from each candidate. Compare structurally different feasible mechanisms, or give source-backed reasons competing shapes cannot satisfy the constraints. Renaming one mechanism provides no alternative. Fixed contracts remain constraints.

Make the comparison inspectable: trace the same caller and failure cases through each candidate's representation, signatures and owners. Assess the complexity each interface hides and the knowledge or coordination it still requires from consumers. Screen for invariants or policy repeated across callers, competing writers, mutable aliases, leaked internal representations, lifecycle gaps and public surface that adds no capability. Show the resulting consumer consequences rather than a checklist verdict.

Use Arena's selection and synthesis to choose a coherent base and recheck the combined proposal. Return the selected sketch, decisive source-supported tradeoffs, rejected mechanisms and unresolved verification needs. The [slices procedure](slices-and-acceptance.md) carries that contract into implementable units.

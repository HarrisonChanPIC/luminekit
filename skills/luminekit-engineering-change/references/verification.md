# Engineering verification

This is the shared owner for engineering test independence, runtime boundaries and built-source correspondence. Use it when selecting checks or assessing a claimed engineering result; a planning caller specifies these observations without executing them.

## Independent expected behavior

Derive expected outcomes from requirements or independently worked source facts, never the production helper or copied faulty logic under test. Specify literal membership, identities, per-record values, counts, amounts, ordering and error/state outcomes where they carry the contract. Balanced totals can conceal incorrect records. Accept alternatives the contract leaves open, such as column order or internal layout.

Exercise the actual public behavior and relevant durable/runtime state. Select discriminating alternate, benign, boundary or failure inputs that expose the defect or overfitting. A self-comparison, constant-only assertion, weakened test or mock replacing the behavior is insufficient.

Tool/setup failure is a check failure, not proof of a product defect. Import, collection, fixture, runner, selector and pre-behavior timeout errors do not establish a regression; a missing check is a coverage gap. An authorized isolated mutant can demonstrate detector sensitivity: it must reach the intended violation and fail the relevant assertion. An independent public-entry observation matters when monkeypatch/global test state could mask the implementation. Do not alter live systems to create a control.

## Match the actual boundary

Serial calls, threads, independent processes and separate CI jobs exercise different coordination claims. Match the check to real clients and persistence. A process-local mutex cannot establish independent-client coordination; independent processes may still share host ports, predictable paths, services and databases. Inspect durable rows and each returned identity when they define correctness. Use readiness/completion transitions to prove relevant overlap rather than relying on a sleep. For an existing probabilistic failure, the CI-reliability procedure of the `luminekit-diagnose` skill owns further topology diagnosis.

Performance comparisons need comparable workloads and conditions. Check visible UI, compiled/generated entry or deployed behavior only when that is the requested boundary; source inspection or in-memory success has narrower coverage.

## Bind built results to current inputs

For a built/generated/deployed claim, identify relevant source and dirty/configuration/dependency inputs, artifact or freshness identity, invoked command/target/runtime, checked scope and result. HEAD, timestamps, filenames or matching metadata establish neither faithful build correspondence nor behavior. A source test does not certify an absent compiled/deployed entry. If correspondence is missing, name the bounded rebuild or public-entry check needed for that claim.

Run relevant existing project checks and required gates at the selected boundary. A content-only edit may need just its affected content/diff check; new tests should detect meaningful behavior, not mirror the implementation.

# Engineering review criteria

Read the relevant definitions, consumers, persistent/data contracts and failure paths for the selected subject. Compare code with required behavior, compatibility, regression/security impact, failure/resource/cancellation handling and test strength. Compare plans with complete useful units, real dependencies, independent acceptance and feasible verification.

Use current project/language standards as requirements and label heuristics as such. A missing or stale documentation owner is a finding only against an actual required contract; a proposal should not be represented as current behavior. Do not substitute the reviewer's preferred patch for a correct implementation.

For test independence, actual runtime boundaries or built-source claims, use the verification procedure of the `luminekit-engineering-change` skill. Standards compliance and functional correctness are separate review dimensions: neither cancels a defect in the other. Combine findings with the same cause while retaining relevant independent witnesses and distinct consequences.

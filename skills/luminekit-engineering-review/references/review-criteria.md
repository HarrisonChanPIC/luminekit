# Engineering review criteria

Read the relevant definitions, consumers, persistent/data contracts and failure paths for the selected subject. Compare code with required behavior, compatibility, regression/security impact, failure/resource/cancellation handling and test strength. Compare plans with original requirements and required implementation bases, consistent callers and interfaces, ownership/resource tradeoffs, complete useful units, real dependencies, independent acceptance and feasible verification.

Keep original controlling requirements separate from producer-changed artifacts. Preserve an accessible version or read-only copy before producer edits when those edits could change the acceptance source. Changed documentation can describe an implementation or propose a contract change; it does not establish authorization for that change. Review against the original basis and any separately authorized revisions. Distinguish a violated requirement from an unresolved contract choice, and label a targeted recheck rather than presenting it as a full independent review.

Use current project/language standards as requirements and label heuristics as such. A missing or stale documentation owner is a finding only against an actual required contract; a proposal should not be represented as current behavior. Do not substitute the reviewer's preferred patch for a correct implementation.

For test independence, actual runtime boundaries or built-source claims, use the verification procedure of the `luminekit-engineering-change` skill. Standards compliance and functional correctness are separate review dimensions: neither cancels a defect in the other. Combine findings with the same cause while retaining relevant independent witnesses and distinct consequences.

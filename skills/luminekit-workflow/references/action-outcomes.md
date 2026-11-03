# Operation outcomes

Use before an actual effect or when reconciling/reporting an earlier attempt. Check actual capability, approved operation/targets/current payload and prerequisites. Respect ordering; approval for one effect does not grant linked transitions or notifications. The acting skill owns its class-specific authority and retry rules.

Correlate authoritative evidence to the exact request/operation/target/revision/payload. Complete required pagination and relevant readback coverage. Submission, an accepted job, timeout, success string, empty/stale/partial/eventually-consistent readback or missing ID does not alone prove delivery or nonexecution. Count attempts and actual effects separately.

| State per operation | Disposition |
| --- | --- |
| Prepared / not attempted | Report that state; it is not confirmed no effect from an attempted operation. |
| Confirmed effect | Retain matching identity/evidence; do not repeat it to complete a batch. |
| Confirmed no effect | Report nonexecution; apply the operation class's authorization/retry rule. |
| Inconclusive | Seek authorized scoped reconciliation if available; otherwise hold and state the unresolved effect. |

A mixed batch remains partial. Preserve attempted payloads separately from later revisions, report completed and held items, material limits and next supported action. A send receipt does not prove the business claims in its message; an approved revision or accepted deployment job is not a verified deployed result.

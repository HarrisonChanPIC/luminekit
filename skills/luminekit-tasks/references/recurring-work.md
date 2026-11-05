# Reconcile recurring work

Recurrence defines the responsibility and its business period. Prefer a suitable native recurrence feature and verify its identity/replay behavior. For a reminder-only responsibility, keep the existing standing task with dated notes and a next follow-up when sufficient; changing that date does not execute work or alter a scheduler.

## Visible fallback for retained period results

When separate execution/review history matters and native recurrence is unavailable, use ordinary records:

- A standing **series** describes the outcome, cadence/timezone, period definition, start/end conditions, missed-period policy, permitted run effects, evidence and output location. Keep it open while the responsibility continues.
- An **occurrence** retains one period's work, evidence and outcome, optionally as a native child. Include a visible series ID and period key in supported text, for example `CASE-80 / week-of-2026-11-09`. The native ID remains authoritative; the key is correlation, not an atomic uniqueness constraint.
- The series retains a concise **period → native ID index** so archived occurrences remain addressable. Keep current state/evidence on the occurrence rather than copying status into the index. Use ordinary text/native fields, not hidden custom frontmatter or a parallel tracker.

Define the key by business meaning. A changed appointment time does not create a second weekly report. A responsibility with multiple daily executions may need a slot as part of its period. Keep trigger time/timezone distinct from a date-only due field.

## Reconcile before work

1. Read the current series rule, actual invocation time/timezone and allowed effects. For a requested historical replay, use that explicit period; do not confuse it with today's period.
2. Resolve an existing occurrence using the index, current tasks and relevant finished/archived history. Read exact native IDs. Reuse an incomplete occurrence; return a completed period's retained result as a visible no-op. If its supposed output is missing or closure evidence conflicts, report that discrepancy rather than silently rerunning the business effect.
3. Create only after sufficient identity/coverage and coordination. Retain its returned native ID on the series before consequential period work, then execute through the actual domain procedure, retain the output and finalize against the real criteria. Completing an occurrence does not complete the series.
4. Report the period, occurrence ID, result/output, unmet requirement and next action, including no-op or blocked results.

Recover a create/link interruption by looking for the exact series/period before creating again, including archived history as needed. Repair the series index to the existing native ID. A missing index entry or empty active search does not prove no occurrence exists. Use Workflow's operation-outcome reconciliation for uncertain effects; if coverage cannot establish the outcome, hold another creation and report it as inconclusive.

## Missed periods and writers

Establish a policy: latest due period only, bounded catch-up of each required period, or skip stale periods with a visible report. Report older unfinished/gap periods under the chosen policy; do not erase them by advancing a reminder. Do not create future periods by default. An unfinished period blocks the next only if the business rule requires it.

For a new routine, resolve cadence, reporting period, timezone and ambiguous/nonexistent local-time behavior before enabling it. Start with the actual calendar routine needed, such as a weekly reporting week; this skill provides no general cron/RRULE engine.

Use one designated writer with serialized invocations for automatic materialization. Verify coordination across the actual overlapping clients/processes: search-then-create, an assignee, status, a scheduler replay key or an ID allocator alone does not prove period uniqueness. If overlap prevention or history access is insufficient, keep materialization manual with exclusive access, or provide a read-only preview; do not claim unattended safety.

For automatic invocation and delivery, read [scheduled work](scheduled-work.md).

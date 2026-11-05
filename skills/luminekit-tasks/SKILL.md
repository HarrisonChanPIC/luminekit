---
name: luminekit-tasks
license: Proprietary. All rights reserved.
description: Capture, organize, review, update or close commitments in a project's task system, including recurring work and scheduling handoffs. Use for task tracking; ordinary questions or domain work alone do not require a task record.
---

# Manage the actual commitments

Follow `luminekit-workflow` once within this scope. The task system owns commitments, status and completion evidence. Domain procedures perform the work; project guidance supplies local conventions and standing authority; the harness supplies execution and delivery. A task's text alone grants no additional authority.

## Bind to the right records

Resolve the project and task system from the request and current guidance. Identity includes the board/workspace, not just a task number. With two plausible boards, resolve the target before mutating either. Use [Backlog](references/backends/backlog.md) for Backlog.md; read [the backend contract](references/backend-contract.md) when assessing or adding another system. An unknown or read-only backend can support bounded inspection without claiming write support.

Use native fields, IDs, configured statuses and lifecycle. Keep one authoritative record, with links to documents in their existing homes. A short commitment needs only enough context to preserve its outcome; do not create records for every interaction or require optional projects, milestones and fields.

## Capture and maintain

- Find the same commitment before creating it. Use a supplied native ID, source identity, outcome and relevant period; read likely matches. Similar titles can describe different work, and one source can contain multiple commitments. Account for pagination and relevant finished/archived history before treating a search as absence. Resolve material ambiguity rather than inventing a match or another record.
- Capture the intended outcome, necessary source/context, actual dates and known responsibility. Distinguish a deadline, meeting, work session and follow-up; an exact trigger time is not necessarily a task deadline. Keep uncommitted ideas in the native draft process when appropriate.
- Read current content before updating it. Prefer targeted additions; preserve unrelated criteria, references, notes and human edits. Distinguish the accountable human from the agent doing the work. If a replacement would overwrite a conflicting edit, reconcile it first.
- Record researched execution plans when work is picked up. Link substantial designs in their knowledge owner rather than maintaining divergent copies. Progress notes should retain useful evidence and remaining work.
- Distinguish grouping from prerequisites: a parent groups an outcome, a dependency gates work, and a milestone groups a delivery target. Unknown dependencies remain unresolved. An unfinished or canceled prerequisite does not become satisfied by disappearing from the board; a completed child does not by itself complete its parent.

For a review, return the actionable commitments, genuine deadlines, blockers and decisions needing attention, with native IDs/links and enough coverage information to understand material omissions. Prioritize from current commitments and configured values.

## Establish the outcome

Compare the actual deliverable with acceptance criteria, shared Definition of Done and relevant domain requirements. A prepared draft, human confirmation, independent verification, approval and delivery are different evidence. Check only supported criteria, retain concise evidence/output links and use the native finalization procedure with readback. Leave required review or delivery pending when it has not happened.

Honor explicit administrative closure and imported historical completion, recording their basis accurately. Preserve unsupported criteria as unsupported; do not reopen owner-closed history to impose a new convention. For canceled, duplicate or superseded work, retain the reason/successor without claiming delivery. Use native archive/restore for retained history; permanent deletion requires scope that includes removal.

For actual writes and uncertain/partial results, use `luminekit-workflow`'s operation-outcome procedure. Preserve attempted identity/payload and reconcile authoritative state before repeating an effect. A timeout is not evidence that creation failed. Report confirmed changes, unresolved effects and the next supported action separately.

## Recurrence and scheduling

Read [recurring work](references/recurring-work.md) for repeating responsibilities, period reconciliation or replay. Prefer suitable native recurrence; a reminder-only task may simply retain dated notes and the next follow-up.

Read [scheduled work](references/scheduled-work.md) for registration, scheduled execution or missing results. Recurrence defines the business period; scheduling invokes the procedure. A scheduler's successful run is not evidence of completed work or delivered output.

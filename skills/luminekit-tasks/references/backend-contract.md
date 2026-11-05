# Assess or add a task backend

This is a procedural contract for maintainers, not an executable adapter API or universal task schema. Preserve useful native features and expose limits. No second database, synchronization service or installation follows from selecting a backend.

Establish the following from the actual installation's official guidance and available tools:

| Concern | Required evidence |
| --- | --- |
| Binding and identity | How to select the project/workspace/board; native record identity; ambiguous or missing target behavior. |
| Reads and coverage | Exact reads, search semantics, filters, pagination and limits; finished, archived/deleted and cross-branch scope; stale or partial reads. |
| Native meaning | Configured statuses and terminal meaning, responsibility, criteria/DoD, dates, source links and supported relationships. Preserve optional fields rather than requiring a common schema. |
| Writes and outcomes | Supported create/update/finalize/archive/restore operations, returned identities, readback and partial/uncertain effects; actual read-only restrictions. |
| Coordination | Actual conflict handling and uniqueness guarantees across relevant clients/processes. Status and assignee fields alone establish no claim/lock. |
| Optional features | Drafts, milestones, projects, recurrence, automation and UI access; suitable native behavior takes precedence over fallback conventions. |

Classify each relevant capability as **native**, **visible convention**, **unsupported** or **unknown**. Separately record whether it is **documented**, **inspected** or **exercised**, and whether the current transport can use it. A product feature or similarly named MCP method does not establish client parity or available credentials.

Ordinary calls must yield native candidates with coverage, current task context, or reconciled mutation outcomes—not an invented normalized task. An inaccessible capability leaves its dependent action pending while useful supported work continues.

To add a backend, write one focused reference, add its selection route in `SKILL.md`, and exercise ordinary capture/deduplication, targeted update, evidence-based closure and failure cases on native records. Map optional recurrence separately. A paper mapping can reveal Backlog assumptions but does not certify another integration; synchronization and migration require their own requested scope.

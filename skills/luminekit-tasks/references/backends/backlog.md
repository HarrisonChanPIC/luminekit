# Operate a Backlog.md board

Use the installed product's instructions and command help. Prefer the canonical CLI when available; use an MCP transport only where its guidance and operations cover the request.

## Discover this installation

Run commands with the intended project as the working directory; account for an existing `BACKLOG_CWD` override. Inspect actual configuration and `backlog config list`. Storage may be selected by root `backlog.config.yml` or folder configuration, with a custom directory and task prefix. Do not assume `.backlog/`, `backlog/` or `TASK-`, and do not initialize a replacement board merely because binding failed. Use current help when a command or configuration location differs.

Read `backlog instructions overview` once per conversation and the matching installed guide before its lifecycle action:

- `backlog instructions task-creation` for creation or splitting.
- `backlog instructions task-execution` for execution, plans, status, assignment or notes.
- `backlog instructions task-finalization` for checked criteria, final summaries or finished status.

Reuse sufficient current reads. Inspect `backlog <command> --help` for unfamiliar fields/operations and use the actual configuration's values. Project authority and business ownership still govern; the execution guide's coding-agent assignment example does not require replacing a responsible human.

## Read and mutate through native operations

Use `backlog task view <id>` for a known ID; search/list for candidates, with scoped filters and complete relevant pages. Structured reads return versioned JSON envelopes. Follow the response's pagination fields, such as `total` and `nextSkip`, and command help to retrieve the required scope. JSON watch emits replacement snapshots and may coalesce edits; it is neither a durable event log nor a scheduler.

All semantic record writes use native commands, including tasks, drafts, documents, decisions and milestones. Retain returned IDs; do not allocate them manually or edit their Markdown. Configuration changes are separate from ordinary task maintenance and do not justify enabling remotes, auto-commit, hooks or repairs.

Prefer additive operations where supported: `--append-notes`, `--add-ref`, `--add-doc` and `--add-label`. Replacement flags may replace whole lists/sections. Read the current task, preserve applicable entries and read back the intended changes. Pass multiline values as real newlines and literal text through safely quoted/structured arguments; native help covers shell hazards.

Use actual dependencies/readiness and inspect unresolved graph identities. `backlog doctor` is a diagnostic; repair options require their own scope. Do not rely on an unknown/ambiguous dependency as satisfied. Native task IDs and status/assignment do not supply business-period uniqueness or verified multi-writer arbitration.

## Lifecycle and history coverage

Mark finished work with the configured final status. Use `backlog task archive <id>` to move a task off the board while preserving its ID, status and links. Archived tasks are read-only; read them with `backlog task view <id>` and restore them with `backlog task restore <id>` before editing. Permanent delete follows archive, removes relationships and may release the ID; reserve it for authorized removal rather than routine cleanup.

`backlog task list` reads local editable tasks. Check command help for archive coverage; active list/search alone does not establish archived absence. Use known IDs and the recurring series index to read archived occurrences. When native reads cannot enumerate the history needed for recovery, locate native IDs through a scoped read-only archive inventory, then read each selected task with `backlog task view <id>`. Keep semantic writes native. If relevant history cannot be covered, hold a potentially duplicate creation and state the limit.

Use the recurrence convention only when suitable native recurrence is not established; consult [recurring work](../recurring-work.md). A date-only due field does not encode an exact-time trigger. Keeping the native UI available, including running a browser service, does not schedule agent execution.

# Schedule invocation and retain results

The actual harness owns wakeups, process availability, run history and delivery. Use its available documented tools; the task skill adds no scheduler, daemon or cloud runtime. Load [recurring work](recurring-work.md) when a run materializes a recurring occurrence. A read-only review can be scheduled without creating occurrence tasks.

## Make the requested schedule concrete

Before registration, bind the actual machine/environment, project directory, board/series identity, trigger and interpreted timezone, start/missed-period policy, access, permitted effects, input/output locations, serialization/recovery, visible result destination and pause/disable operation. Resolve material unknowns; a vague reminder is not an execution contract.

Choose coordination for the permitted effects. Concurrent read-only briefs can be acceptable snapshots; lack of an exclusive-writer guarantee alone need not block them. Establish any necessary duplicate-notification or ordering policy separately. Automatic recurring task creation and business effects still need the relevant verified serialization/reconciliation; a harmless review does not establish that stronger capability.

Prepare a self-contained prompt that loads current project guidance, `luminekit-tasks` and the actual domain procedure. Include those bindings and required result delivery so a fresh run can act without this chat. For example, adapt these fields to known values rather than registering placeholders:

```text
Project / machine / task system:
Task or series and intended-period rule / timezone / missed-period policy:
Read current project guidance and the installed luminekit-tasks skill.
Work and actual domain procedure:
Allowed effects and input/output locations:
Single-writer/overlap and uncertain-prior-run handling:
Result destination and retained history:
Return period, native ID, result, output link, unmet requirement and next action.
Return a visible result even for no-op, blocked or failed work.
```

First execute the permitted procedure manually and verify its output. When registration is requested, save through the harness and read back the schedule ID, enabled state, next run with interpreted timezone, project/machine and delivery destination. A series edit does not update an existing schedule; reconcile differing cadence/scope before acting. A scheduling-only request does not authorize running its prompt immediately.

In T3 Code, use `schedule_task` to register or update a schedule, `list_scheduled_tasks` to read it back, and `delete_scheduled_task` to remove it. Set `enabled=false` to pause an existing schedule. Choose the supported trigger and conversation binding from the tool schema. Verify timezone, coordination and missed-wakeup behavior separately. `run_scheduled_task_now` returning a thread means started, not completed. Use each harness's own binding/history semantics.

## Verify the result boundary

Each invoked run returns a human-readable result:

```text
Task/series and intended period
Result: prepared / needs review / completed / no-op / blocked / inconclusive
Native occurrence ID/link, if any
Output location/link, if produced
Evidence and material unmet requirement
Next action and owner
```

Retain the primary result in the configured run conversation/history and link useful deliverables from the task. These task-facing results coexist with Workflow's per-operation effect states: a draft can be prepared while a task write is inconclusive. A runtime success flag does not prove business completion or accessible delivery. Verify the actual result at the expected destination; a toast or “ran” flag is insufficient.

Before claiming a desktop automation works, exercise manual success, an actual scheduled invocation, no-op, domain failure, accessible results, the required overlap policy and pause/disable on that harness. Test timezone, missed wakeups, sleep/closed-client and restart behavior at the real device boundary. Document only observed guarantees. The skill cannot log a run that never launched; discovering those gaps belongs to the harness on resume.

If the harness cannot establish a required execution/delivery guarantee, keep the dependent automation pending and offer a manual invocation or read-only scheduled review where supported. Do not install services or substitute cloud execution merely to hide that gap.

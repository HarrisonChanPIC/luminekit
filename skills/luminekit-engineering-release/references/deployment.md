# Deployment and migration

Resolve the approved environment/account, exact build or migration identity, current target state, prerequisites, gates and expected effect using the existing runbook. Before a state change, make compatibility, ordering, data-loss, interruption and recovery implications reviewable. Identify the actual recovery path and its prerequisites rather than assuming every migration is reversible. Preparation may identify these unresolved owner decisions without executing a backup or experiment.

After the approved operation, inspect service health or the data invariant at the real target. Recovery/rollback has its own scope and consequences; preserve diagnostics rather than reversing an uncertain change automatically.

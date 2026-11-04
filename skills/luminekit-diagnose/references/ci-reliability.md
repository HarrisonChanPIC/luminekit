# Diagnose probabilistic test or CI failure

Use for actual timing, resource, lifecycle or platform uncertainty. Inspect the owning test policy, runner configuration and job topology. Apply the verification procedure of the `luminekit-engineering-change` skill for independent expectations and coordination boundaries.

## Classify supported evidence

Keep the relevant workflow/job/runner/platform, command, timestamps and first stable failure signature. Separate test assertions from runner infrastructure, timeout, cancellation/signal and exit status. Compare failing and passing runs with equivalent relevant inputs; one green rerun does not establish infrastructure blame or a resolved cause.

Investigate mechanisms supported by the evidence:

- **Resource collision:** jobs/processes acquire the same port, socket, path, database or external namespace.
- **Incomplete lifecycle:** owned work/children/callbacks continue beyond cleanup and affect later work.
- **Global contamination:** environment, working directory, clock, locale, mock or module state makes order matter.
- **Synchronization:** assumed scheduling/readiness fails under load.
- **Platform/entry mismatch:** the failure follows OS, shell, filesystem, source/build mode or executable.
- **Product concurrency:** controlled resources and explicit overlap expose the shipped race.
- **External transience:** the actual provider boundary and documented retry policy account for failure.
- **Runner infrastructure:** independent checkout/download/disk/host/service evidence explains the event. Missing metrics remain a limit; recurring signatures across unrelated branches on one pool can support qualified contention analysis.

Retain multiple supported signals rather than collapsing assertion, timeout and exit into one guessed cause.

## Reach the relevant topology

Expand the focused check only to the first boundary needed to reproduce the failure: workers, independent processes, gate or jobs sharing a resource. Match source/build mode, runner/platform and knobs. Passing on another platform or inaccessible topology is not reproduction.

Prove overlap or readiness/completion at the implicated boundary. For collisions, inspect simultaneous identifier acquisition or an authorized comparison against the owner's atomic allocator. For leaks, inspect restoration and quiescence after abort/close/kill, not just calls to those methods. Stress supplements a discriminator; arbitrary load or deadline changes may create a different failure.

When a remedy is authorized, target the actual allocator, readiness, global-state or teardown owner. Compare pre-fix or negative-control and corrected behavior at that same topology. A justified budget adjustment or documented provider retry may be legitimate, but weakening assertions, blanket serialization or unexplained timeout inflation does not establish a fix.

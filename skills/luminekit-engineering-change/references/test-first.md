# Test the behavior before changing it

Use for a substantive behavior change with a practical focused regression path, or an explicit test-first request. This procedure owns the ordering of test and implementation. Use [engineering verification](verification.md) for independent expectations, controls and actual runtime/build boundaries; follow the project's existing runner and applicable language guidance.

## Ordered cycle

1. **Save a focused regression against unfixed behavior.** Select the next small useful behavior slice, add or adapt a test that exercises it, and preserve applicable existing assertions. An existing failure can be reused when it reaches the requested behavior; it does not replace a missing regression for a different case.
2. **Run and inspect the intended failure.** The test must load, reach the target behavior and reject its independent expectation. Record the relevant invocation, source/test/input state and decisive assertion. A proposed test or supplied log is not an observed red.
3. **Resolve check failures before interpreting the result.** Repair permitted test setup and rerun against the still-unfixed product. If the first valid run is green, check whether the behavior already works, the wrong path ran or the assertion cannot disagree. Preserve the result's real history.
4. **Implement the smallest coherent behavior.** Fix the behavior rather than hardcoding the first example. Preserve nearby contracts and failure/cancellation/resource semantics. Do not weaken assertions, discard still-valid tests, swallow an error or add retries to manufacture green.
5. **Observe corrected behavior.** Rerun the regression and affected required checks on the changed state. If it fails, distinguish a bad remedy, mistaken expectation, missing fact and broken machinery before continuing. Use the `luminekit-diagnose` skill for unexplained failure rather than repeating until green.
6. **Refactor if useful, then verify the final state.** A behavior-preserving improvement is optional; affected checks must cover its resulting source. Review the saved source/tests/diff and useful controls, then continue another small behavior cycle only when the task needs it.

Test-first is an order claim: saved test → intended failure on unfixed behavior → product change → observed corrected behavior. Implementation followed by tests can be useful verification but cannot be relabeled test-first.

## Unavailable or impractical path

Use the closest meaningful regression boundary rather than a brittle mock-only test or unrelated infrastructure project. Name the actual missing seam/tool/access or cost boundary. If the requested sequence cannot be executed, hold its completion claim and distinguish supported static analysis or an independently authorized correction from unperformed red/green. The static-evidence procedure of the `luminekit-diagnose` skill specifies a useful unchanged-current-subject observation separately from future post-remedy checks.

Deliver the focused change, observed failing-before assertion and passing-after invocation, relevant controls/required checks, post-refactor evidence where applicable and remaining limits.

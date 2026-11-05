# Modern Go idioms by task

Select only idioms supported by the existing module's Go floor and build targets. Do not raise versions or replace established tools. New projects prefer the current stable release. The tables cover features through Go 1.27; minimum versions are feature gates, not an upgrade request.

## Collections and comparison

| Since | Prefer | Preserve/check |
| --- | --- | --- |
| 1.21 | `slices.Contains`, `Index`, `IndexFunc` | Use the comparison/predicate that matches the contract; index helpers return `-1` when absent. |
| 1.21 | `slices.Sort` | In-place ordering for ordered values; aliases observe mutation. |
| 1.21 | `slices.SortFunc` with `cmp.Compare` | A typed comparator replaces index closures; use `SortStableFunc` when equal entries must keep their order. |
| 1.21 | `slices.Min`, `Max` | Empty input panics; retain an explicit empty-input contract. |
| 1.21 | `slices.Reverse` | In-place reversal, not a copy. |
| 1.21 | `slices.Compact` | Removes adjacent duplicates in place; grouping/sorting changes order and may be inappropriate. Use the returned slice. |
| 1.21 | `slices.Clip` | Limits capacity to length; it does not copy or release the retained backing array. |
| 1.21 | `slices.Clone`, `maps.Clone` | Shallow copies; preserve nil and clone nested mutable data separately when needed. |
| 1.21 | `maps.Copy` | Copies entries into an initialized destination, overwriting matching keys; it does not recursively copy values. |
| 1.21 | `maps.DeleteFunc` | Express a deletion predicate without a manual deletion loop. |
| 1.21 | `min`, `max` | Concise ordered comparisons; inspect floating-point/NaN semantics before replacing custom logic. |
| 1.21 | `clear` | Deletes map entries or zeros slice elements; it does not reset slice length or allocate fresh storage. |
| 1.22 | `cmp.Or` | First nonzero value, not first non-nil/valid value in every domain; arguments are evaluated eagerly. |
| 1.23 | `maps.Keys`, `maps.Values` | Iterate directly when no materialized slice is needed; map order remains unspecified. |
| 1.23 | `slices.Collect` | Materialize an iterator when a slice is actually needed. |
| 1.23 | `slices.Sorted`, `SortedFunc`, `SortedStableFunc` | Collect and sort in one operation; choose ordering and stability deliberately. |

For example, on Go 1.23+:

```go
keys := slices.Sorted(maps.Keys(counts))
```

For Go 1.21+, a stable field sort uses:

```go
slices.SortStableFunc(rows, func(a, b Row) int {
	return cmp.Compare(a.Priority, b.Priority)
})
```

See [slices](https://pkg.go.dev/slices), [maps](https://pkg.go.dev/maps) and [cmp](https://pkg.go.dev/cmp) for exact mutation, empty-input and comparison behavior.

## Iteration, strings and time

| Since | Prefer | Preserve/check |
| --- | --- | --- |
| 1.22 | `for i := range n` | Zero-based fixed count; retain ordinary loops for other starts, steps or changing bounds. |
| 1.22 | Per-iteration `:=` loop variables | Remove redundant capture copies only under the effective newer language version. Predeclared-variable assignment and original-element pointers are different cases. |
| 1.23 | Range over iterator functions | Consume lazily when appropriate; respect the iterator's stop/lifetime contract. |
| 1.24 | `strings.SplitSeq`, `FieldsSeq`; `bytes.SplitSeq`, `FieldsSeq` | Iterate parts without allocating a slice of all parts; retain materialization when required. |
| 1.18 | `strings.Cut`, `bytes.Cut` | Split at the first separator and handle `found`; byte slices can alias their input. |
| 1.20 | `strings.CutPrefix`, `CutSuffix` | Combine matching and trimming while preserving the unmatched-input behavior. |
| 1.27 | `strings.CutLast`, `bytes.CutLast` | Split at the last separator without repeated index arithmetic. |
| 1.18 | `strings.Clone` | Copy a retained small substring when otherwise it would keep a large backing string alive; avoid pointless copies. |
| 1.20 | `bytes.Clone` | Explicit byte-slice copy with nil preservation. |
| 1.19 | `fmt.Appendf` | Append formatting directly to an existing byte buffer without an intermediate formatted string. |
| 1.0 / 1.8 | `time.Since(start)` / `time.Until(deadline)` | State elapsed/remaining time directly. |
| 1.23 | `time.Tick` when only its channel is needed | Unreferenced tickers can be collected under the newer timer implementation. Use `NewTicker` when Stop/Reset or explicit lifecycle control is needed; keep worker cancellation independent. |

Check [Go 1.22](https://go.dev/doc/go1.22), [1.23](https://go.dev/doc/go1.23) and [1.24](https://go.dev/doc/go1.24) for language and timer changes, including compatibility settings that retain earlier timer behavior.

## Errors, cancellation and concurrency

| Since | Prefer | Preserve/check |
| --- | --- | --- |
| 1.13 | `errors.Is` | Recognize wrapped sentinels and custom matching, rather than relying on direct equality. |
| 1.20 | `errors.Join` | Preserve matching across multiple causes; nil-only inputs yield nil. Do not unintentionally change the caller's error contract. |
| 1.26 | `errors.AsType[T]` | Return the typed match plus a boolean without a separate pointer-to-target variable. |
| 1.20 | `context.WithCancelCause`, `context.Cause` | Record a useful cancellation reason in addition to the broad context error. |
| 1.21 | `WithTimeoutCause`, `WithDeadlineCause` | Give a timeout/deadline a specific cause when callers need it; still release owned resources. |
| 1.21 | `context.AfterFunc` | Register cancellation-triggered work instead of a goroutine waiting only on Done; stopping the callback does not wait for one already started. |
| 1.21 | `sync.OnceFunc`, `OnceValue` | Express one-time work/memoization with their concurrency and panic semantics. |
| 1.25 | `sync.WaitGroup.Go` | Pair spawning with tracking; the function must not panic. It does not collect errors, propagate cancellation or remove the need to Wait. |
| 1.19 | Typed atomics (`atomic.Bool`, `Int64`, `Pointer[T]`, etc.) | Avoid mixed atomic/non-atomic accesses. A field migration can change layout; do not copy atomic values after first use. `atomic.Value` and `Pointer` have different nil/type contracts. |

Go 1.26 error matching:

```go
if pathErr, ok := errors.AsType[*os.PathError](err); ok {
	handlePathError(pathErr)
}
```

An explicit error channel/result owner and cancellation propagation are still needed around worker helpers. Review [context](https://pkg.go.dev/context), [sync](https://pkg.go.dev/sync) and [atomic](https://pkg.go.dev/sync/atomic) contracts rather than mechanically shortening code.

## Tests, HTTP and JSON

| Since | Prefer | Preserve/check |
| --- | --- | --- |
| 1.24 | `t.Context()` | Canceled before Cleanup callbacks run; cleanup needing a live context must use another appropriate context. |
| 1.24 | `b.Loop()` | Modern benchmark loop; fixtures sized from `b.N` before the loop need redesign because the final count is available afterward. |
| 1.22 | Method-aware `http.ServeMux` patterns and `r.PathValue` | Standard routing such as `GET /items/{id}`; preserve externally visible matching, status and redirect behavior. |
| 1.24 | JSON `omitzero` | Omit Go zero values, including suitable structs/time values; `omitempty` expresses different empty-value rules. Preserve existing wire formats. |
| 1.27 | `encoding/json/v2` for new JSON code | Prefer stricter defaults in new code. Leave existing v1 code unchanged unless migration is explicitly requested. |

For an authorized JSON v1→v2 migration, start with `jsonv1.DefaultOptionsV1()` and review accepted inputs and serialized outputs before adopting v2 options. Duplicate keys, invalid UTF-8 and nil slice/map encoding are consequential differences. See the [Go 1.27 release notes](https://go.dev/doc/go1.27). A compiling import change does not establish wire compatibility.

## Types and small utilities

| Since | Prefer | Preserve/check |
| --- | --- | --- |
| 1.18 | `any` | Modern spelling of the `interface{}` alias, not permission to discard useful types. |
| 1.22 | `reflect.TypeFor[T]()` | Obtain a known type without pointer/Elem boilerplate. |
| 1.26 | `new(expression)` | Allocate an initialized pointer; untyped constants use their default types, so use `new(int32(3))` for `*int32`. Keep helpers that supply extra behavior. |
| 1.27 | Generic methods | Put a generic operation on a receiver when that type owns it; keep package functions for other operations. Interface methods cannot declare their own type parameters. |
| 1.27 | Promoted fields in keyed struct literals | Initialize promoted fields directly where supported; do not mix a promoted field and its embedding field or assume pointer-embedded paths work. |
| 1.27 | Standard `uuid` | Prefer it for new generation/parsing needs covered by its API; retain existing dependencies and public types unless migration is in scope. |
| 1.27 | `url.URL.Clone`, `url.Values.Clone` | Use the standard deep copies instead of partial manual copying. |

Feature gates follow [Go 1.21](https://go.dev/doc/go1.21), [1.25](https://go.dev/doc/go1.25), [1.26](https://go.dev/doc/go1.26) and [1.27](https://go.dev/doc/go1.27), plus package documentation. No extra CLI, wrapper, installer or downloaded analyzer is needed.

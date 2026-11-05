# Go behavior and boundaries

Use the module's effective `go`/`toolchain` version and configured tools. Keep pure decisions separate from filesystem/process effects where useful, and introduce interfaces for actual substitutable boundaries.

## Version-aware choices

Inspect the affected module, workspace, file/build constraints and CI targets. Keep existing Go versions, directives and tooling; do not upgrade them for a newer idiom. The [`go` directive](https://go.dev/doc/modules/gomod-ref#go) establishes a minimum version; `toolchain` suggests a toolchain, not permission to raise every module's compatibility floor. A newer installed compiler can expose library APIs unavailable to supported consumers. For new projects, prefer the current stable Go release and standard tooling, with explicit module/deployment requirements; avoid preview/experimental features by default.

Read the relevant section of the [modern idiom catalog](go-modern-idioms.md) when choosing collection helpers, iteration, concurrency, errors, JSON, HTTP or newer syntax. It gives minimum versions and semantic caveats. Use supported idioms in the code being changed without unrelated modernization churn.

For collection changes, [`slices.Clone`](https://pkg.go.dev/slices#Clone) is shallow: clone nested mutable data separately when independent mutation is required. Select `SortStableFunc` when ties must keep their order. A convenient helper does not establish equivalent behavior, and an unordered map traversal does not become ordered by collecting it.

Use configured formatters, vet and analyzers as applicable. A language-guidance change does not require an installer, downloaded wrapper or newly installed analysis suite.

## Values and lifetimes

Determine whether an operation needs a value copy, shared storage or the actual element. A slice-of-structs range value is a copy; its address is not the original element's address. Go 1.22's fresh variables for `:=` loops change capture behavior, not that distinction; assignment to predeclared variables differs. Slices may still share an underlying array. Check the effective version and [language specification](https://go.dev/ref/spec#For_statements) for the relevant case.

Preserve the caller's error contract and useful cause/state. Close owned resources and inspect consequential write/close errors. Propagate cancellation through actual operations and establish worker completion when required: [CancelFunc](https://pkg.go.dev/context#CancelFunc) does not wait for work to stop.

## Filesystem and checks

For scoped filesystem work, lexical cleaning or `os.DirFS` alone does not confine symlink traversal. Consider [os.Root](https://pkg.go.dev/os#Root) where supported and inspect its platform/operation limits. It supplies neither application authorization nor multi-file transactions.

Use existing `testing` conventions through the behavior selected by [engineering verification](verification.md). Isolate temporary and shared resources, especially in parallel cases. Use the [race detector](https://go.dev/doc/articles/race_detector) when relevant and supported; a pass covers executed paths rather than all interleavings, independent processes or durable effects.

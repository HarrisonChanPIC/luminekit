# Go behavior and boundaries

Use the module's effective `go`/`toolchain` version and configured tools. Keep pure decisions separate from filesystem/process effects where useful, and introduce interfaces for actual substitutable boundaries.

## Values and lifetimes

Determine whether an operation needs a value copy, shared storage or the actual element. A slice-of-structs range value is a copy; its address is not the original element's address. Go 1.22's fresh variables for `:=` loops change capture behavior, not that distinction; assignment to predeclared variables differs. Slices may still share an underlying array. Check the effective version and [language specification](https://go.dev/ref/spec#For_statements) for the relevant case.

Preserve the caller's error contract and useful cause/state. Close owned resources and inspect consequential write/close errors. Propagate cancellation through actual operations and establish worker completion when required: [CancelFunc](https://pkg.go.dev/context@go1.26.6#CancelFunc) does not wait for work to stop.

## Filesystem and checks

For scoped filesystem work, lexical cleaning or `os.DirFS` alone does not confine symlink traversal. Consider [os.Root](https://pkg.go.dev/os@go1.26.6#Root) where supported and inspect its platform/operation limits. It supplies neither application authorization nor multi-file transactions.

Use existing `testing` conventions through the behavior selected by [engineering verification](verification.md). [Go's testing introduction](https://go.dev/doc/tutorial/add-a-test) describes `_test.go` and `go test`. Isolate temporary and shared resources, especially in parallel cases. Use the [race detector](https://go.dev/doc/articles/race_detector) when relevant and supported; a pass covers executed paths rather than all interleavings, independent processes or durable effects.

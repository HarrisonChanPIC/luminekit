# TypeScript guidance

Preserve public types, runtime behavior and the project's error/nullability contract. A broad cast, unchecked assertion or relaxed compiler setting does not repair a runtime defect. Use relevant [type narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) where it expresses a supported guarantee.

A `number` annotation or type assertion does not establish a nonnegative runtime value. Validate the actual contract at an untrusted boundary and retain useful narrowed guarantees internally. [Type assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions) add no runtime validation. Typechecking and visible UI behavior exercise different boundaries under [engineering verification](verification.md).

## Existing and new projects

Read the effective compiler version, inherited tsconfig, runtime target, module resolution and package exports before choosing syntax or APIs. Preserve existing versions, package tooling, strictness and nullability; do not upgrade them to use a newer example. A newer editor compiler does not establish compatibility with the project's supported compiler. Distinguish a compiler feature from a runtime API or required polyfill. For a new project, choose current stable TypeScript and maintained runtime/tooling, with strict checking and a module configuration appropriate to deployment.

## Practices for TypeScript and TSX changes

Apply these practices when reading, writing or reviewing TypeScript. Read [modeling and boundary patterns](typescript-patterns.md) for the relevant examples and detailed choices.

| Practice | Decision |
| --- | --- |
| Discriminated unions | Give each variant a unique literal under a consistent `kind`, `type` or `tag` field; avoid bags of optional fields that permit contradictory states. |
| Branded primitives | Use `T & { readonly __brand: "Name" }` for domain distinctions that prevent values being mixed. Establish the brand with a verifying guard at the boundary rather than a cast. Preserve an established equivalent brand convention in existing code. |
| Constructive modeling | Represent nonempty collections with `[T, ...T[]]`, pairs with `[T, T][]`, and ranges with start plus validated duration when these encode the contract. |
| Simplest total type | Keep ordinary arrays/primitives when their operations already handle every input. Strengthen inputs or make results optional when a use site otherwise needs `!`, a cast or an impossible-state throw. |
| `unknown` over `any` | External data starts as `unknown`; narrow it before use. |
| Schemas before guards | Reuse the repository's runtime schema and infer its types; avoid duplicate schema/interface/guard contracts. Do not add a dependency just for one guard. |
| Assertions | Remove unchecked `as` and non-null assertions by modeling, narrowing or parsing. Any unavoidable assertion follows an established guarantee; it supplies no runtime check. |
| Narrowing hierarchy | Prefer discriminant branches, then `in`, then `typeof`/`instanceof`, then a verifying user guard; assertions are a last resort. |
| Honest guards | Name guards `isX`/`hasX` and check every fact their predicate promises. A plausible name does not make an incomplete check safe. |
| Exhaustiveness | Use a `never` assignment in exhaustive switch defaults so a new variant forces affected consumers to change. |
| `satisfies` | On TypeScript 4.9+, check configuration/table shapes without an `as` assertion or an unnecessarily wide annotation; this is compile-time checking. |
| Boundary validation | Parse untrusted data into named domain types once at entry. Raw `Record<string, unknown>` data stops there; trust the validated types internally. |
| Derived types | Reuse generated schema types and `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited` and `typeof` before duplicating a shape. |
| Object arguments | Prefer a named argument object when multiple arguments could be confused; preserve public APIs and avoid allocation-sensitive hot-path churn. |
| Real checks | Use the framework's real test primitives, disposal/leak checks and runnable dependencies where available. Verify UI behavior in a running build when applicable; shared [verification](verification.md) owns the procedure. |
| Structured telemetry | Use the project's structured logger with useful identifiers and diagnostic context. Avoid ad-hoc `console.log` in shipped code; preserve intentional CLI output. |

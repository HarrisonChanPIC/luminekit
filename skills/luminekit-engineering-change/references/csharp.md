# C# implementation decisions

## Resolve the supported configuration

Inspect target frameworks, SDK selection (`global.json`), inherited `Directory.Build.props`/targets, `LangVersion`, nullable settings and CI. Multi-target projects must work for every supported target. Keep existing frameworks, language/SDK versions and tooling; do not upgrade them for a new feature. Microsoft's [language-version guidance](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version) explains framework defaults and why `latest` can make builds vary by machine. For a new project, prefer the current stable supported .NET SDK/framework and its default stable C# version, with nullable checking enabled. .NET 10/C# 14 is the modern baseline covered here; select a newer stable pairing when appropriate, not preview features.

Use the [language history](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history) to check feature availability. Compiler support and runtime/library support are separate constraints.

| Feature | Language floor | Use when |
| --- | --- | --- |
| Records and `init` | C# 9 | Value equality or initialization-time assignment fits the public model |
| Record structs | C# 10 | A value type with generated equality fits the model and copying cost |
| `required`, raw string literals | C# 11 | Callers must initialize members; or a literal becomes clearer with fewer escapes |
| Primary constructors, collection expressions | C# 12 | Constructor scope or a target-typed collection expression simplifies the actual code |
| `field`, extension members | C# 14 | The supported compiler/framework pairing permits them and they clarify an existing API |

Read [modern C# patterns](csharp-patterns.md) for examples of primary constructors, collection expressions, records, pattern matching, raw strings, spans, `field` accessors and extension blocks. Use only the sections supported by the affected targets.

## Preserve model semantics

Choose a class, record or struct from identity, equality, mutation and copying requirements. Converting a class used as an identity key into a record can change dictionary behavior. A struct is copied by value and is not universally faster or always stack allocated.

[Records](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record) provide value-oriented equality; `init` and positional readonly record structs restrict assignment, not mutation of referenced objects. `with` copies are shallow. Clone nested mutable collections explicitly when independence is required, and preserve serialization/public-constructor behavior where consumers depend on it.

[`required`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/required) asks callers to initialize members. It does not validate their values or replace runtime null checks. Nullable annotations likewise express a static contract; they do not reject runtime nulls from every caller.

Keep validation and state mutation in the right order. Normalize and validate a candidate value before assigning a backing field so a rejected setter leaves the existing object valid. C# 14's [`field`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/field) reduces boilerplate without supplying this invariant:

```csharp
public string Name
{
    get;
    set
    {
        ArgumentNullException.ThrowIfNull(value);
        var candidate = value.Trim();
        if (candidate.Length == 0)
            throw new ArgumentException("Name must not be blank.", nameof(value));
        field = candidate;
    }
} = "Unnamed";
```

On older targets, the same validate-then-assign order works with an explicit backing field. Check both constructor failure and failed assignment to an existing instance when the invariant matters.

## Patterns, collections and lifetimes

Use patterns to make branching and null handling clear while preserving prior behavior; a shorter expression must not introduce a dereference before its null check. Primary-constructor parameters do not automatically create public properties for ordinary classes. Collection expressions need a suitable target type and preserve the required collection's mutation/ownership contract; they do not make its contents immutable.

Use `Span<T>` and ref structs when measured needs and lifetime restrictions fit the code. Inspect supported compiler/runtime rules around escaping references, async and iterators instead of broadly replacing collections or allocating on the stack.

Preserve lazy initialization's concurrency and failure semantics. [`Lazy<T>`](https://learn.microsoft.com/en-us/dotnet/api/system.lazy-1) can coordinate initialization and cache a factory exception according to its mode. A getter using `??=` does not provide the same concurrency or exception-caching contract. Verify the actual public behaviors through [engineering verification](verification.md); framework architecture and project setup remain separate decisions.

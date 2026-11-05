# Modern C# patterns

Use the existing project's framework, language version and style. New projects prefer current stable .NET/C# tooling. Read the applicable sections rather than loading every example; this guide does not authorize changing existing versions or public model semantics.

## Choosing a construct

| Need | Preferred starting point | Available since |
| --- | --- | --- |
| Data contract/value equality | `record`, immutable members where the contract permits | C# 9 |
| Small copied value | `readonly record struct` when value semantics fit | C# 10 |
| Caller-supplied initialization | `required` with `init`; runtime validation remains separate | C# 11 |
| DI/service constructor | Primary constructor | C# 12 |
| Collection creation/spread | Target-typed collection expression | C# 12 |
| Validated property | `field` accessor, or backing field on older targets | C# 14 |
| Extension properties/static members | Extension blocks; ordinary extension methods remain supported | C# 14 |
| Multi-line SQL/JSON/XML | Raw string literal | C# 11 |
| Branching/extraction | `is` and switch patterns; list patterns where useful | C# 7–11, depending on pattern |
| Allocation-sensitive slicing | `Span<T>` / `ReadOnlySpan<T>` when lifetime rules fit | C# 7.2+ and a supporting API/runtime |

Prefer readability over dense nesting. Use `var` when the initializer makes the type apparent; use an explicit type when an opaque method result otherwise hides it. Avoid changing nearby unrelated syntax just to modernize it.

## Primary constructors and collections

```csharp
public sealed class OrderService(IOrderRepository repository, TimeProvider clock)
{
    public DateTimeOffset Now => clock.GetUtcNow();
    public Order Load(Guid id) => repository.Load(id);
}

int[] first = [1, 2];
int[] all = [..first, 3];
List<string> names = ["Ada", "Lin"];
```

Primary constructors simplify dependencies, but ordinary class parameters do not automatically become public properties. Preserve necessary null validation and dependency lifetimes. Collection expressions need a target type; `var values = [1, 2]` alone supplies none. Choose the collection type for ownership/mutation and supported construction, not just shorter syntax. See [primary constructors](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/tutorials/primary-constructors) and [collection expressions](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/collection-expressions).

## Records, initialization and copying

```csharp
public sealed record Money(decimal Amount, string Currency);
public readonly record struct RgbColor(byte Red, byte Green, byte Blue);

public sealed record Endpoint
{
    public required Uri Address { get; init; }
}
```

Use a named domain type rather than an anonymous tuple for a durable contract. Choose records for value equality and classes for identity when appropriate. A small value object can use a readonly record struct; value types are not always stack allocated or automatically faster. `required` enforces initialization by supported callers, not valid values. `init`, `readonly` and record `with` copies do not recursively freeze/copy referenced lists. Preserve mutable collections or clone them explicitly according to the domain contract.

## Patterns and raw strings

```csharp
string Tier(Order? order) => order switch
{
    null => "Unknown",
    { Total: > 1000m } => "Premium",
    _ => "Standard"
};

string Describe(int[] values) => values switch
{
    [] => "Empty",
    [var only] => $"One: {only}",
    [var first, .., var last] => $"{first}..{last}"
};

string json = """
    {"mode": "standard", "enabled": true}
    """;
```

Use property/list patterns for clear branches and extraction. Break deeply nested patterns into named predicates or sequential null-safe checks; a direct dereference chain does not preserve a null-rejecting pattern's behavior. Raw strings simplify literals; interpolated raw strings choose enough `$` characters to distinguish content braces from interpolation. Raw SQL literals do not replace parameterized queries. See [patterns](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns) and [raw strings](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/tokens/raw-string).

## `field` accessors and notifications

C# 14 can use `field` for the compiler-generated storage. Normalize/validate before assignment as shown in the [C# guide](csharp.md#preserve-model-semantics). Older targets retain explicit backing fields.

```csharp
public sealed class OrderViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    public decimal Total
    {
        get;
        set
        {
            if (field == value) return;
            field = value;
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Total)));
        }
    }
}
```

This example needs `System.ComponentModel`. Preserve required thread-affinity, validation, equality comparison and notification order. A lazy getter `get => field ??= Load();` can simplify a single-threaded cache, but does not reproduce `Lazy<T>`'s concurrent publication and exception caching. Keep `Lazy<T>` when those are part of the contract.

## Extension members

```csharp
public static class OrderExtensions
{
    extension(Order order)
    {
        public bool IsHighValue => order.Total > 1000m;
        public string ToSummary() => $"Order {order.Id}: {order.Total}";
    }

    extension(Order)
    {
        public static bool IsPremiumTotal(decimal total) => total > 1000m;
    }
}
```

Extension blocks live inside static classes. They support properties and static extension members as well as grouping instance operations. Use ordinary `this` extension methods on older targets or when one method is clearer. Avoid unexpected member names or hidden domain-policy changes. See [extension members](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/extension-methods).

## Spans and lifetimes

```csharp
ReadOnlySpan<char> text = input.AsSpan().Trim();
if (text.StartsWith("id:".AsSpan()) && int.TryParse(text[3..], out int id))
{
    UseId(id);
}
```

Use span-based APIs for measured or evident allocation-sensitive parsing/slicing, not as a default replacement for ordinary strings/collections. Keep backing storage alive and references within allowed lifetimes. Stack allocation must be bounded; ref structs/spans have version-dependent restrictions around fields, escaping, async and iterators. Read the supported [ref struct rules](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/ref-struct).

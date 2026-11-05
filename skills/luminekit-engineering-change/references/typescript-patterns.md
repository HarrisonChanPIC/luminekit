# TypeScript modeling and boundary patterns

Read the sections relevant to the changed types or boundaries. All examples must fit the existing project's compiler/runtime; they do not authorize upgrades.

## Variants and exhaustiveness

A boolean plus optional payloads permits missing data and contradictory states. A discriminated union puts each payload with its actual state:

```ts
type Download =
  | { kind: "queued" }
  | { kind: "complete"; path: string }
  | { kind: "failed"; message: string };

function summary(download: Download): string {
  switch (download.kind) {
    case "queued": return "Queued";
    case "complete": return download.path;
    case "failed": return download.message;
    default: {
      const exhaustive: never = download;
      return exhaustive;
    }
  }
}
```

Use a consistent discriminant name. In a statement/void switch, consume the default's `never` local with `void exhaustive` rather than inventing a return value. Keep the exhaustiveness check at consumers that need to reconsider a new variant.

## Brands with a verifying boundary

```ts
type AccountId = string & { readonly __brand: "AccountId" };

function isAccountId(value: string): value is AccountId {
  return /^acct_[0-9a-f]{16}$/.test(value);
}

function parseAccountId(value: unknown): AccountId {
  if (typeof value !== "string" || !isAccountId(value)) {
    throw new TypeError("Invalid account ID");
  }
  return value;
}
```

The format above is illustrative; use the real domain's format. After parsing, internal APIs take `AccountId`, not another string-shaped bag. The guard performs the verification; `as AccountId` would merely claim it happened. Use the `readonly __brand` convention in new code unless an existing project already owns an equivalent convention. Brand meaningful units/identifiers rather than every primitive.

## Constructive models and total operations

```ts
type NonEmpty<T> = [T, ...T[]];
type Pairs<T> = [T, T][];

function isNonEmpty<T>(items: T[]): items is NonEmpty<T> {
  return items.length > 0;
}

function first<T>(items: NonEmpty<T>): T {
  return items[0];
}

function total(items: number[]): number {
  return items.reduce((sum, item) => sum + item, 0);
}
```

Narrow a plain array once when nonemptiness is required. Keep `number[]` for a sum: empty input has a valid result. For a lookup that can legitimately fail, `T | undefined` can be the honest total result instead of strengthening the input. A randomly computed array index is not statically in bounds merely because the array is nonempty; with `noUncheckedIndexedAccess`, account for that separately rather than adding `!`.

Pairs encode even-length structure without repeating length checks. A range expressed as `{ start: Date; durationMs: number }` avoids independently stored endpoints drifting apart, but `number` still admits negative, infinite and fractional values. Validate the actual duration contract at entry; use a guarded duration brand if internal callers could otherwise bypass that distinction. Validate dates too, and derive the end from start plus duration. `readonly` is shallow: it neither freezes a Date nor prevents mutation through another alias. Tuple syntax must fit the compiler; variadic tuples require TypeScript 4.0+.

## Parse external data once

RPC, JSON, IPC, messages, files, environment variables and database results cross a trust boundary. Treat their raw values as `unknown`. Do not silence that boundary with `any`, `as User`, or a guard that checks only one of several required fields.

When the repository already uses Zod, for example:

```ts
import { z } from "zod";

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  role: z.enum(["admin", "member"]),
});
type User = z.infer<typeof UserSchema>;

function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}
```

Use `safeParse` for an expected failure branch. Use equivalent facilities in the installed schema library and its supported version. If an existing public type owns the contract first, annotate the validator with that type, such as `z.ZodType<User>`, so a missing field is a compile-time incompatibility. Do not maintain a second hand-written interface and guard alongside the schema.

Parse into a named domain type. After that point, pass trusted values internally instead of rechecking each call. For wire formats intended to tolerate forward-compatible fields, configure the parser to ignore unknown fields (for example `ignoreUnknownFields` where supported). Preserve protocols that deliberately reject extras. Persisted JSON needs a versioned representation and a parse/validation failure path; a `try/catch` alone does not validate shape or authorize dropping corrupt data.

## Narrow instead of asserting

Prefer, in order: discriminant switch/if; property membership with `in`; `typeof`/`instanceof`; a user-defined guard that verifies its predicate; and only then a necessary assertion backed by validation. Check for a non-null object before using `in` on external values. Property existence alone does not establish a property's type or value constraints.

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  if ("radius" in shape) return Math.PI * shape.radius ** 2;
  return shape.width * shape.height;
}

function isCircle(shape: Shape): shape is Extract<Shape, { kind: "circle" }> {
  return shape.kind === "circle";
}
```

For an existing cast, identify the inference gap: missing discriminant, over-wide source type, or unparsed boundary. Repair that model or parse rather than replacing the cast with a lying predicate. A brand can carry an independently verified domain fact; it cannot make an arbitrary claim true.

## Derive shapes and use `satisfies`

Generated protocol/OpenAPI/GraphQL/database types already own their shapes. Derive a view with `Pick`/`Omit` rather than restating fields; derive function inputs/results with `Parameters`, `ReturnType` and `Awaited`, or a value's shape with `typeof` where supported.

```ts
type CheckMessage = { total: number; names: string[]; revision: string };
type CheckView = Pick<CheckMessage, "total" | "names">;
```

On TypeScript 4.9+, prefer `satisfies` over an assertion when an expression must conform to a shape:

```ts
type Config = { theme: "dark" | "light"; columns: number };
const config = { theme: "dark", columns: 3 } satisfies Config;
```

It checks assignability while retaining useful inference (`theme` remains `"dark"` here). It performs no runtime validation and does not universally freeze every literal type. Older projects use compatible annotations/helpers without a compiler upgrade. See the official [4.9 notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html).

## Arguments, checks and diagnostics

Prefer `openFile({ uri, selection })` to arguments whose meaning depends on order. Named options are especially useful for multiple values with the same type. Preserve existing public signatures; skip fresh argument-object allocation on tight render/tokenizer/parser paths when it matters.

Use real framework primitives and locally runnable dependencies for checks, including disposal/leak detection and the running UI when affected. Reserve mocks for unavailable boundaries, and distinguish what they exercise. Use structured logger fields such as request/entity IDs, operation and failure cause so one identifier can lead to useful diagnostics. Keep intentional user-facing CLI output separate from application logging. The shared [verification reference](verification.md) owns general test procedure.

# TypeScript boundaries

Preserve public types, runtime behavior and the project's error/nullability contract. A broad cast, unchecked assertion or relaxed compiler setting does not repair a runtime defect. Use relevant [type narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) where it expresses a supported guarantee.

A `number` annotation or type assertion does not establish a nonnegative runtime value. Validate the actual contract at an untrusted boundary and retain useful narrowed guarantees internally. [Type assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions) add no runtime validation. Typechecking and visible UI behavior exercise different boundaries under [engineering verification](verification.md).

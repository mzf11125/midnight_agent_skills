# Compact Type System

## Overview

Compact is **strongly statically typed** with a rich type system designed for zero-knowledge circuits. Every expression has a static type, and the compiler rejects programs that don't type check.

## Primitive Types

### Boolean
```compact
const flag: Boolean = true;
const check: Boolean = false;
```
- **Values**: `true`, `false`
- **Default**: `false`
- **TypeScript**: `boolean`

### Unsigned Integers

#### Bounded Integers
```compact
const age: Uint<0..150> = 25;        // 0 to 150
const percentage: Uint<0..100> = 75; // 0 to 100
```
- **Syntax**: `Uint<m..n>` where `m` is lower bound (currently must be 0), `n` is upper bound
- **Default**: `0`
- **TypeScript**: `bigint` with runtime bounds checks

#### Sized Integers
```compact
const value: Uint<32> = 4294967295;  // 32-bit (0 to 2^32-1)
const small: Uint<8> = 255;          // 8-bit (0 to 255)
```
- **Syntax**: `Uint<n>` where `n` is number of bits
- **Equivalent**: `Uint<32>` = `Uint<0..4294967295>` (2^32-1)
- **Common sizes**: 8, 16, 32, 64, 128, 256
- **Default**: `0`

### Field
```compact
const element: Field = 12345;
```
- **Purpose**: Scalar field elements for ZK circuits
- **Range**: 0 to maximum field value (very large prime)
- **Default**: `0`
- **TypeScript**: `bigint` with runtime bounds checks
- **Note**: Arithmetic wraps modulo field size

### Tuples
```compact
const pair: [Field, Boolean] = [42, true];
const triple: [Uint<8>, Uint<16>, Uint<32>] = [1, 2, 3];
const empty: [] = [];  // Unit type
```
- **Syntax**: `[T1, T2, ...]` where each `T` is a type
- **Heterogeneous**: Elements can have different types
- **Length**: Fixed at compile time
- **Default**: Tuple of default values for each element
- **TypeScript**: `[T1, T2, ...]` or `T[]` with length checks

### Vectors
```compact
const vec: Vector<5, Field> = [1, 2, 3, 4, 5];
```
- **Syntax**: `Vector<n, T>` where `n` is length, `T` is element type
- **Shorthand**: `Vector<5, Field>` = `[Field, Field, Field, Field, Field]`
- **Homogeneous**: All elements same type
- **Default**: Vector of default values
- **TypeScript**: `T[]` with runtime length checks

### Bytes
```compact
const hash: Bytes<32> = "midnight";  // UTF-8 encoded, padded to 32
const data: Bytes<64> = pad(64, "hello");
```
- **Syntax**: `Bytes<n>` where `n` is length in bytes
- **Purpose**: Byte arrays for hashing, cryptography
- **String literals**: Automatically UTF-8 encoded
- **Default**: All zero bytes
- **TypeScript**: `Uint8Array` with length checks

### Opaque Types
```compact
const text: Opaque<"string"> = "hello";
const buffer: Opaque<"Uint8Array"> = new Uint8Array([1, 2, 3]);
```
- **Syntax**: `Opaque<"tag">` where tag is `"string"` or `"Uint8Array"`
- **Purpose**: Values manipulated in witnesses but opaque to circuits
- **In circuits**: Represented as hash
- **Default**: Empty string or zero-length array
- **TypeScript**: `string` or `Uint8Array`

## User-Defined Types

### Structures
```compact
struct Point {
  x: Field,
  y: Field
}

struct Person {
  name: Bytes<32>;
  age: Uint<0..150>;
  active: Boolean;
}
```
- **Syntax**: `struct Name { field: Type, ... }`
- **Separators**: Comma or semicolon (consistent within struct)
- **Default**: All fields set to their default values
- **TypeScript**: `{ field: Type, ... }`

#### Generic Structures
```compact
struct Pair<T> {
  first: T,
  second: T
}

struct Container<#n, T> {
  items: Vector<n, T>,
  count: Uint<0..n>
}
```
- **Type parameters**: `<T>` for types
- **Size parameters**: `<#n>` for compile-time numbers
- **Specialization**: `Pair<Field>`, `Container<10, Uint<32>>`
- **Must be fully specialized**: All parameters provided

### Enumerations
```compact
enum Status {
  pending,
  approved,
  rejected
}

enum Color { red, green, blue }
```
- **Syntax**: `enum Name { value1, value2, ... }`
- **Values**: `Status.pending`, `Status.approved`, etc.
- **Default**: First value in declaration
- **TypeScript**: `number` with runtime membership checks

## Subtyping

### Subtyping Rules

```compact
// Uint subtyping
Uint<0..10> <: Uint<0..100>  // ✅ Smaller range is subtype
Uint<0..100> <: Field         // ✅ All Uints are subtypes of Field

// Tuple subtyping (covariant)
[Uint<0..10>, Boolean] <: [Uint<0..100>, Boolean]  // ✅ Element-wise

// Reflexive
T <: T  // ✅ Every type is subtype of itself
```

### Implicit Conversions
```compact
const small: Uint<0..10> = 5;
const large: Uint<0..100> = small;  // ✅ Implicit upcast

const num: Uint<0..1000> = 42;
const field: Field = num;  // ✅ Implicit conversion to Field
```

### Least Upper Bound
```compact
// For tuples/vectors with mixed types
const mixed = [1, 2, 3];  // Type: [Uint<0..1>, Uint<0..2>, Uint<0..3>]
// Least upper bound: Uint<0..3>
// Can be used as: Vector<3, Uint<0..3>>
```

## Type Annotations

### Required Annotations
```compact
// Circuit parameters: REQUIRED
circuit process(x: Field, y: Boolean): Uint<32> { ... }

// Witness parameters: REQUIRED
witness getData(id: Uint<64>): Bytes<32>;
```

### Optional Annotations
```compact
// Const bindings: OPTIONAL
const x = 42;              // Inferred: Uint<0..42>
const y: Field = 42;       // Explicit: Field

// Anonymous circuits: OPTIONAL
const f = (x, y) => x + y;           // Inferred
const g = (x: Field, y: Field): Field => x + y;  // Explicit
```

## Default Values

Every type has a default value:

```compact
default<Boolean>           // false
default<Uint<0..100>>      // 0
default<Field>             // 0
default<[Field, Boolean]>  // [0, false]
default<Bytes<32>>         // 32 zero bytes
default<Opaque<"string">>  // ""
default<Point>             // Point { x: 0, y: 0 }
default<Status>            // Status.pending (first value)
```

## Type Conversions

### Allowed Casts

```compact
// Upcasts (always safe)
const small: Uint<0..10> = 5;
const large = small as Uint<0..100>;  // ✅ Static cast

// Field conversions
const num: Uint<32> = 42;
const field = num as Field;  // ✅ Static cast

// Boolean conversions
const zero: Field = 0;
const flag = zero as Boolean;  // ✅ 0→false, others→true

// Checked downcasts
const big: Uint<0..1000> = 42;
const small = big as Uint<0..100>;  // ✅ Runtime check

// Bytes to Field
const bytes: Bytes<32> = "data";
const field = bytes as Field;  // ✅ Interpret as field element
```

### Conversion Table

| From | To | Type | Notes |
|------|-----|------|-------|
| `Uint<0..m>` | `Uint<0..n>` (m≤n) | Static | Safe upcast |
| `Uint<0..m>` | `Uint<0..n>` (m>n) | Checked | Runtime validation |
| `Uint<0..n>` | `Field` | Static | Always safe |
| `Field` | `Uint<0..n>` | Checked | Validates range |
| `Field` | `Boolean` | Conversion | 0→false, else→true |
| `Field` | `Bytes<n>` | Checked | Validates fits in n bytes |
| `Boolean` | `Uint<0..n>` | Conversion | false→0, true→1 |
| `Boolean` | `Field` | Conversion | false→0, true→1 |
| `Bytes<m>` | `Bytes<n>` (m=n) | Static | Same length |
| `Bytes<m>` | `Field` | Checked | Validates field range |
| `enum` | `Field` | Conversion | Enum value to number |

## TypeScript Mappings

### Primitive Types
```typescript
// Compact → TypeScript
Boolean          → boolean
Field            → bigint
Uint<n>          → bigint
Bytes<n>         → Uint8Array
Opaque<"string"> → string
Opaque<"Uint8Array"> → Uint8Array
```

### Compound Types
```typescript
// Tuples
[Field, Boolean] → [bigint, boolean] or Array<bigint | boolean>

// Vectors
Vector<5, Field> → bigint[] (with length check)

// Structs
struct Point { x: Field, y: Field }
→ { x: bigint, y: bigint }

// Enums
enum Status { pending, approved }
→ number (0 for pending, 1 for approved)
```

### Runtime Type Constructors
```typescript
import { CompactTypeBoolean, CompactTypeField, CompactTypeUnsignedInteger } from '@midnight-ntwrk/compact-runtime';

const boolType = new CompactTypeBoolean();
const fieldType = new CompactTypeField();
const uint32Type = new CompactTypeUnsignedInteger(4294967295, 4);
const bytesType = new CompactTypeBytes(32);
const vectorType = new CompactTypeVector(5, fieldType);
```

## Generic Types

### Generic Structures
```compact
struct Box<T> {
  value: T
}

// Specialization
const intBox: Box<Uint<32>> = Box { value: 42 };
const fieldBox: Box<Field> = Box { value: 100 };
```

### Generic Circuits
```compact
circuit identity<T>(x: T): T {
  return x;
}

// Usage (type inferred)
const result = identity(42);  // T = Uint<0..42>
```

### Size Parameters
```compact
struct FixedArray<#n, T> {
  data: Vector<n, T>
}

// Specialization
const arr: FixedArray<10, Field> = FixedArray {
  data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
};
```

## Type Inference

### Automatic Inference
```compact
// Literals
const x = 42;           // Uint<0..42>
const y = true;         // Boolean
const z = "hello";      // Bytes<5>

// Expressions
const sum = x + y;      // Inferred from operands
const result = f(x);    // Inferred from f's return type
```

### Inference Limitations
```compact
// ❌ Cannot infer circuit parameter types
circuit process(x) { ... }  // ERROR: type annotation required

// ✅ Must annotate
circuit process(x: Field) { ... }
```

## Common Patterns

### Option Type (Maybe)
```compact
import { Maybe, some, none } from CompactStandardLibrary;

const value: Maybe<Field> = some(42);
const empty: Maybe<Field> = none();
```

### Result Type (Either)
```compact
import { Either, left, right } from CompactStandardLibrary;

const success: Either<String, Uint<32>> = right(42);
const error: Either<String, Uint<32>> = left("Error message");
```

### Newtype Pattern
```compact
struct UserId { value: Uint<64> }
struct OrderId { value: Uint<64> }

// Type-safe: can't mix UserId and OrderId
const user = UserId { value: 123 };
const order = OrderId { value: 456 };
```

## Best Practices

### 1. Use Specific Types
```compact
// ❌ Too general
const value: Field = 42;

// ✅ Specific bounds
const age: Uint<0..150> = 42;
```

### 2. Leverage Subtyping
```compact
// ✅ Accept supertypes in parameters
circuit process(value: Uint<0..1000>): [] {
  // Accepts Uint<0..100>, Uint<0..500>, etc.
}
```

### 3. Use Generics for Reusability
```compact
// ✅ Generic container
struct Container<T> {
  items: Vector<10, T>
}

// Works with any type
const numbers: Container<Uint<32>> = ...;
const flags: Container<Boolean> = ...;
```

### 4. Explicit Annotations for Clarity
```compact
// ✅ Clear intent
const hash: Bytes<32> = persistentHash(data);
const commitment: Field = transientCommit(value, randomness);
```

## Resources

- **Language Reference**: See midnight-compact skill
- **Standard Library Types**: See standard-library.md
- **TypeScript Interop**: See typescript-interop.md
- **Type Conversions**: See type-conversions.md

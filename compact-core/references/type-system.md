# Compact Type System

## Overview

Compact's type system is designed for ZK circuit programming. Types represent values in a finite field (the scalar field of the proving curve), and operations on those values translate to circuit constraints. The type system is static and checked entirely at compile time with no runtime type errors possible.

## Primitive Types

### Uint

`Uint<N>` represents an unsigned integer of N bits where N must be a power of two between 8 and 256. The most common sizes are `Uint<64>` and `Uint<128>`.

```
let small: Uint<8> = 255;
let medium: Uint<64> = 1_000_000;
let large: Uint<256> = 0;
```

Arithmetic on Uint values wraps according to modular arithmetic in the circuit field, but the compiler enforces range checks to ensure values stay within their bit width. Overflow beyond the bit width is a constraint violation and will cause proof generation to fail.

### Boolean

`Boolean` represents a truth value. It can be `true` or `false`. Boolean values are represented as field elements (1 for true, 0 for false) in the circuit.

```
let flag: Boolean = true;
let result: Boolean = x > y;
```

Boolean operations include `&&` (logical AND), `||` (logical OR), and `!` (logical NOT). Short-circuit evaluation does not apply in circuit functions because both branches of a conditional are always evaluated.

### Bytes

`Bytes<N>` represents a fixed-length sequence of N bytes. It is the type used for addresses, hashes, and arbitrary binary data.

```
let hash: Bytes<32> = zero();
let address: Bytes<32> = 0x1234...;
let data: Bytes<64> = pack(input);
```

Bytes values can be compared for equality, hashed, and used as inputs to cryptographic functions. Individual bytes cannot be accessed directly. Operations on Bytes values work on the entire value at once.

### Field

`Field` represents an element of the scalar field of the proving curve. This is the most fundamental type in the circuit because every wire carries a field element. Field values are raw field elements without any range constraints or interpretation.

```
let element: Field = 0;
let result: Field = mulField(a, b);
```

Field is rarely used directly in application code. Most application values have semantic meaning (amounts, addresses) that are better captured by Uint or Bytes types. Field is used in cryptographic operations and low-level circuit construction.

### CurvePoint

`CurvePoint` represents a point on the elliptic curve used by the proving system. It is used in signature verification and other curve operations.

```
let pk: CurvePoint = ...
let sig_valid: Boolean = verifySignature(pk, msg, sig);
```

CurvePoint values are pairs of field elements satisfying the curve equation. The compiler validates that values assigned to CurvePoint variables represent valid curve points.

## Collection Types

### Vector

`Vector<T, N>` is a fixed-size ordered collection of elements of type T. The size N must be a compile-time constant.

```
let values: Vector<Uint<64>, 10> = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
let first: Uint<64> = values[0];
```

Vector elements are accessed by index using square bracket notation. The index must be a compile-time constant or a value that the compiler can determine at compile time. Dynamic indexing (where the index depends on a witness value) is not supported because circuits have a fixed structure.

### Map

`Map<K, V>` is an associative collection mapping keys of type K to values of type V. Maps are implemented as key-value pairs with lookup constraints.

```
let balances: Map<Bytes<32>, Uint<128>> = empty();
let alice_balance: Uint<128> = balances[alice_address];
```

Map lookups in circuit functions add constraints that verify the returned value corresponds to the key. The map must contain an entry for every key that is accessed. Accessing a missing key is a constraint violation.

### Set

`Set<T>` represents a collection of unique elements of type T. Sets support membership testing and insertion.

```
let whitelist: Set<Bytes<32>> = empty();
let is_member: Boolean = whitelist.contains(address);
```

Set membership tests add constraints to the circuit. The set does not need to contain every possible element. Testing membership of an absent element simply returns false rather than causing a constraint violation.

### Cell

`Cell<T>` is a mutable container for a single value of type T. It provides a way to model mutable state within the circuit.

```
let counter: Cell<Uint<64>> = cell(0);
counter = counter + 1;
```

Cell is primarily used in ledger state operations where values need to be read, modified, and written back. The Cell pattern ensures that state transitions are properly constrained.

## Opaque Types

Opaque types hide their internal representation. They are declared with the `opaque` keyword and have no visible structure to code outside their defining module.

```
opaque Signature;
opaque Nullifier;
```

Operations on opaque types are limited to the functions defined in the type's module. This encapsulation ensures that values like signatures and nullifiers cannot be constructed or manipulated except through the approved interfaces, preventing subtle security bugs.

## Structs

Structs group related values into a single type. They are declared with the `struct` keyword and contain named fields with explicit types.

```
struct Transfer {
    amount: Uint<64>,
    sender: Bytes<32>,
    recipient: Bytes<32>,
}
```

Struct fields are accessed with dot notation. Struct values are created using struct literal syntax.

```
let t = Transfer { amount: 100, sender: alice, recipient: bob };
let amt: Uint<64> = t.amount;
```

Structs can contain any type including other structs, creating nested data structures. Structs are value types and are copied on assignment.

## Enums

Enums represent a value that can be one of several variants. Each variant can carry associated data.

```
enum Recipient {
    Address(Bytes<32>),
    Contract(Bytes<32>, Bytes<32>),
}
```

Enum values are created by naming the variant and providing the associated data. Pattern matching on enums uses `match` expressions.

```
match recipient {
    Address(addr) => transfer_to_address(addr),
    Contract(addr, method) => call_contract(addr, method),
}
```

The match expression must be exhaustive, covering all variants of the enum. The compiler checks this at compile time.

## Type Conversions

Compact supports explicit type conversions between compatible types. Implicit conversions are not allowed.

```
let small: Uint<8> = 10;
let medium: Uint<64> = small as Uint<64>;
```

Conversions between Uint types of different widths are supported. The compiler adds range checks where necessary. Conversions from larger to smaller widths require the value to fit within the target width and will fail if it does not.

Conversions between Bytes and other types require explicit packing and unpacking functions. There is no direct cast between Bytes and Uint. Use the standard library functions `pack` and `unpack` for these conversions.

## CompactType in TypeScript

The Compact compiler generates TypeScript type definitions for each Compact type. These definitions, called CompactType classes, enable type-safe interaction with contract state from TypeScript code.

### Generated Classes

For each struct and enum in the Compact source, the compiler generates a corresponding TypeScript class. The class includes methods for serializing values to the wire format expected by the contract and for deserializing values received from the contract.

```typescript
// Generated from compact struct Transfer
class Transfer extends CompactType {
    amount: bigint;
    sender: Uint8Array;
    recipient: Uint8Array;

    static create(amount: bigint, sender: Uint8Array, recipient: Uint8Array): Transfer;
    static schema(): CompactTypeSchema;
}
```

### Using CompactType Classes
CompactType classes handle argument construction and return value inspection for contract calls. A value with an incorrect field type produces a compile-time error rather than a runtime contract failure.

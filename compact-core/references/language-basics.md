# Compact Language Basics

## Overview

Compact is the domain-specific language for writing smart contracts on Midnight. It compiles to arithmetic circuits that define the constraints of a zero-knowledge proof. Compact looks familiar to developers who have worked with languages like TypeScript or Rust but differs in important ways due to its purpose as a ZK circuit description language.

## Module Structure

Every Compact file is a module. Modules organize code into named units that can be imported by other modules. A module declaration specifies the module name and optionally a version.

```
module my_contract;
```

The module name must match the filename. A file named `token.compact` must begin with `module token;`. Module names use lowercase letters and underscores.

Modules can contain function definitions, type definitions, constant declarations, and import statements. The compiler processes the module from top to bottom, and all declarations are visible throughout the module regardless of their position in the file.

## Functions

Compact has two kinds of functions: circuit functions and witness functions.

### Circuit Functions

A circuit function defines constraints that the ZK proof must satisfy. The function body describes relationships between inputs that the prover guarantees hold true. Circuit functions are declared with the `circuit` keyword.

```
circuit function transfer(amount: Uint<64>, recipient: Bytes<32>): Bytes<32> {
    // constraint logic here
}
```

Circuit functions can read from and write to ledger state. They can call other circuit functions and built-in cryptographic functions. The constraints they define become part of the proof that validators verify.

### Witness Functions

A witness function computes witness values without adding constraints to the circuit. It is used for helper computations that prepare data for use in circuit functions. Witness functions are declared with the `witness` keyword.

```
witness function compute_hash(data: Bytes<64>): Bytes<32> {
    // computation without adding constraints
}
```

Witness functions run only on the prover's machine during proof generation. They do not affect what validators verify. They are useful for computing intermediate values that would be expensive or unnecessary to encode as circuit constraints.

### Function Visibility

Functions can be marked as `public` or left private (the default). Public functions can be called from outside the module. Private functions are only callable within the module where they are defined. The contract's public functions form its external interface and correspond to the endpoints that transactions can invoke.

## Variables

### Declaring Variables

Variables in Compact are declared with the `let` keyword. The type can be specified explicitly or inferred from the initializer.

```
let amount: Uint<64> = 100;
let recipient = 0xabcdef;  // type inferred as Bytes
```

Variables are immutable by default. Once assigned, their value cannot change within the scope where they are defined. This immutability is important for ZK circuits because constraints are declarative rather than imperative. Each variable represents a fixed value in the constraint system.

### Scope and Shadowing

Variables have block scope. A variable declared inside a block is only visible within that block. Variables can be shadowed, meaning a new variable with the same name can be declared in an inner scope. The inner variable hides the outer one within its scope.

```
let x = 5;
{
    let x = 10;  // shadows outer x
    // x is 10 here
}
// x is 5 here
```

## Control Flow

### Conditional Statements

Compact supports `if` and `else` for conditional execution. Within a circuit function, both branches of a conditional are always evaluated (because circuits cannot have dynamic control flow). The result is selected based on the condition.

```
if amount > 0 {
    state = state + amount;
} else {
    state = state;
}
```

### Loops

Compact supports `for` loops with a fixed number of iterations. The loop bound must be known at compile time. Dynamic loops (where the iteration count depends on runtime values) are not allowed because circuits must have a fixed, known structure.

```
for i in 0..10 {
    // this loop runs exactly 10 times
}
```

Loops in circuit functions are unrolled at compile time. Each iteration becomes a separate set of constraints. Large loop bounds can produce very large circuits, so use them sparingly.

## Type Annotations

Type annotations in Compact use angle brackets for generic parameters and explicit type names. The language is statically typed, and the compiler checks all types at compile time.

### Explicit Annotations

```
let balance: Uint<128> = 0;
let addr: Bytes<32> = zero();
let flag: Boolean = true;
```

### Type Inference

When the type can be determined from context, the annotation can be omitted. The compiler infers types from literal values, function return types, and usage context.

```
let balance = 0;           // inferred as Uint<64>
let addr = zero();         // inferred from function signature
let hash = hash(data);     // inferred from hash return type
```

## Import and Export Patterns

### Importing Modules

The `import` statement brings declarations from another module into the current module's scope.

```
import * as token from "./token.compact";
import { transfer, mint } from "./token.compact";
import { FungibleToken } from "@openzeppelin/token.compact";
```

The first form imports everything from the module under a namespace. The second form imports specific named declarations. The third form imports from a package dependency using the package name.

### Exporting Declarations

All public functions, types, and constants are automatically available for import by other modules. There is no separate `export` keyword. Marking a function as `public` makes it both callable externally and importable.

## Code Organization

### One Module Per File

Each Compact file should contain a single module. The filename must match the module name. This convention makes it easy to find the source code for a given module and keeps the module graph aligned with the filesystem.

### Directory Structure

A typical Compact project organizes source files under a `src/` directory. Related modules can be grouped into subdirectories. The compiler resolves relative imports based on the filesystem path.

```
src/
  main.compact
  token/
    fungible.compact
    governance.compact
  utils/
    math.compact
    crypto.compact
```

### Contract Entry Point

Every deployable contract must have a module whose public functions serve as the contract's external interface. This is typically the `main` module. When a transaction targets a contract, it calls one of these public functions by name.

### Constants

Constant values are declared with the `const` keyword. They must have explicit type annotations and their values must be computable at compile time.

```
const MAX_SUPPLY: Uint<128> = 1_000_000;
const FEE_DENOMINATOR: Uint<64> = 10_000;
```

Constants can be used anywhere a compile-time value is expected, including as loop bounds and type parameters.

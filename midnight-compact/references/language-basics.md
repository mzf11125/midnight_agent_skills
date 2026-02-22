# Compact Language Basics

## Overview

Compact is a statically-typed, functional programming language designed specifically for zero-knowledge smart contracts.

## Basic Syntax

### Comments
```compact
// Single-line comment
/* Multi-line
   comment */
```

### Variables
```compact
let x = 42;              // Immutable by default
let mut y = 10;          // Mutable variable
y = 20;                  // Reassignment
```

## Types

### Primitive Types
```compact
Bool                     // true, false
Field                    // Field element (cryptographic)
Bytes                    // Byte arrays
String                   // Text strings
Unit                     // () - no value
```

### Numeric Types
```compact
U8, U16, U32, U64       // Unsigned integers
I8, I16, I32, I64       // Signed integers
```

### Compound Types
```compact
// Tuples
let pair: (U32, Bool) = (42, true);

// Arrays
let arr: [U32; 5] = [1, 2, 3, 4, 5];

// Structs
struct Point {
  x: Field,
  y: Field
}

// Enums
enum Option<T> {
  Some(T),
  None
}
```

## Functions

### Basic Functions
```compact
fn add(a: U32, b: U32) -> U32 {
  a + b
}

// Call function
let result = add(5, 3);
```

### Circuit Functions
```compact
circuit privateAdd(private a: Field, public b: Field) -> Field {
  a + b  // a is hidden, b is public, result is public
}
```

### Privacy Annotations
```compact
private   // Hidden in zero-knowledge proof
public    // Visible to all
witness   // Private input for proof generation
```

## Control Flow

### If Expressions
```compact
let max = if x > y { x } else { y };

// If without else returns Unit
if condition {
  doSomething();
}
```

### Match Expressions
```compact
match value {
  Some(x) => x,
  None => 0
}

match number {
  0 => "zero",
  1 => "one",
  _ => "other"  // Default case
}
```

### Loops
```compact
// For loop
for i in 0..10 {
  process(i);
}

// While loop
while condition {
  doWork();
}

// Loop with break
loop {
  if done { break; }
  work();
}
```

## Operators

### Arithmetic
```compact
+  -  *  /  %           // Add, subtract, multiply, divide, modulo
```

### Comparison
```compact
==  !=  <  >  <=  >=    // Equality and ordering
```

### Logical
```compact
&&  ||  !               // And, or, not
```

### Bitwise
```compact
&  |  ^  <<  >>         // And, or, xor, left shift, right shift
```

## Modules and Imports

### Defining Modules
```compact
mod math {
  pub fn square(x: U32) -> U32 {
    x * x
  }
}
```

### Importing
```compact
use std::crypto::hash;
use math::square;

// Import multiple
use std::crypto::{hash, commit};

// Import all
use math::*;
```

## Structs

### Definition
```compact
struct User {
  id: U64,
  name: String,
  balance: Field
}
```

### Construction
```compact
let user = User {
  id: 1,
  name: "Alice",
  balance: 1000
};
```

### Methods
```compact
impl User {
  fn new(id: U64, name: String) -> User {
    User { id, name, balance: 0 }
  }
  
  fn deposit(&mut self, amount: Field) {
    self.balance += amount;
  }
}
```

## Enums

### Definition
```compact
enum Result<T, E> {
  Ok(T),
  Err(E)
}
```

### Pattern Matching
```compact
match result {
  Ok(value) => handleSuccess(value),
  Err(error) => handleError(error)
}
```

## Generics

### Generic Functions
```compact
fn identity<T>(x: T) -> T {
  x
}
```

### Generic Structs
```compact
struct Container<T> {
  value: T
}
```

### Trait Bounds
```compact
fn process<T: Hashable>(item: T) -> Field {
  hash(item)
}
```

## Traits

### Definition
```compact
trait Hashable {
  fn hash(&self) -> Field;
}
```

### Implementation
```compact
impl Hashable for User {
  fn hash(&self) -> Field {
    hash(self.id)
  }
}
```

## Error Handling

### Result Type
```compact
fn divide(a: U32, b: U32) -> Result<U32, String> {
  if b == 0 {
    Err("Division by zero")
  } else {
    Ok(a / b)
  }
}
```

### Option Type
```compact
fn find(arr: [U32], target: U32) -> Option<U32> {
  for i in 0..arr.len() {
    if arr[i] == target {
      return Some(i);
    }
  }
  None
}
```

## Privacy-Specific Features

### Private Computations
```compact
circuit privateBalance(
  private balance: Field,
  public threshold: Field
) -> Bool {
  // Prove balance > threshold without revealing balance
  balance > threshold
}
```

### Commitments
```compact
let commitment = commit(secretValue, randomness);
// Commitment hides value but can be verified later
```

### Nullifiers
```compact
let nullifier = hash(secretKey, coinId);
// Prevents double-spending without revealing coin
```

## Contract Structure

### Complete Contract Example
```compact
contract Token {
  // State
  state {
    totalSupply: Field,
    balances: Map<Address, Field>
  }
  
  // Constructor
  init(initialSupply: Field) {
    totalSupply = initialSupply;
  }
  
  // Public function
  pub fn transfer(to: Address, amount: Field) {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;
    balances[to] += amount;
  }
  
  // Private function
  circuit privateTransfer(
    private from: Address,
    private to: Address,
    private amount: Field
  ) {
    // Private transfer logic with ZK proofs
  }
}
```

## Best Practices

### Naming Conventions
- Types: `PascalCase`
- Functions: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- Variables: `snake_case`

### Code Organization
```compact
// 1. Imports
use std::crypto::*;

// 2. Type definitions
struct MyType { ... }

// 3. Constants
const MAX_VALUE: U32 = 1000;

// 4. Functions
fn myFunction() { ... }

// 5. Circuits
circuit myCircuit() { ... }
```

### Documentation
```compact
/// Calculates the square of a number
/// 
/// # Arguments
/// * `x` - The number to square
/// 
/// # Returns
/// The square of x
fn square(x: U32) -> U32 {
  x * x
}
```

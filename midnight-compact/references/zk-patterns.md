# Zero-Knowledge Patterns in Compact

## Common ZK Patterns

### 1. Range Proofs
Prove a value is within a range without revealing the value.

```compact
circuit proveInRange(private value: Field, public min: Field, public max: Field) -> Bool {
  value >= min && value <= max
}
```

### 2. Membership Proofs
Prove an element is in a set without revealing which element.

```compact
circuit proveMembership(private element: Field, public set: [Field; 10]) -> Bool {
  let mut found = false;
  for item in set {
    if item == element {
      found = true;
    }
  }
  found
}
```

### 3. Equality Proofs
Prove two committed values are equal without revealing them.

```compact
circuit proveEqual(private a: Field, private b: Field, public commitA: Field, public commitB: Field) -> Bool {
  commit(a) == commitA && commit(b) == commitB && a == b
}
```

### 4. Threshold Proofs
Prove value exceeds threshold without revealing exact value.

```compact
circuit aboveThreshold(private balance: Field, public threshold: Field) -> Bool {
  balance > threshold
}
```

## Circuit Optimization

### Minimize Constraints
- Fewer operations = faster proving
- Combine operations where possible
- Use lookup tables for complex operations

### Avoid Expensive Operations
```compact
// Expensive: Division in circuits
let result = a / b;  // Avoid if possible

// Cheaper: Multiplication
let result = a * inverse(b);  // Better
```

### Batch Operations
```compact
// Instead of multiple proofs
circuit batchVerify(private values: [Field; 10]) -> Bool {
  // Verify all at once
}
```

## Privacy Patterns

### Private State, Public Transitions
```compact
contract PrivateVoting {
  circuit castVote(private vote: U32, private voterId: Field) {
    // Vote and voter hidden
    // Only fact that "a vote was cast" is public
  }
}
```

### Selective Disclosure
```compact
circuit proveProperty(private data: Field, public property: Bool) -> Bool {
  // Prove property about data without revealing data
  checkProperty(data) == property
}
```

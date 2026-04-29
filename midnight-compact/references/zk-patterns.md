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

---

## Verification Over Computation Pattern

> Source: "How Midnight Verifies Tokens Without Computing It" — Tushar Pamnani

The most general ZK circuit design principle: **don't compute expensive functions inside a circuit — verify that a claimed result satisfies the mathematical definition.**

### Example: Quadratic Voting (floor sqrt)

`sqrt` is expensive in ZK circuits. Instead of computing it, verify the claim:

`w = floor(sqrt(tokens))` iff `w² ≤ tokens < (w+1)²`

Which simplifies to two cheap inequality checks:

```compact
circuit verifySqrt(tokens: Uint<64>, w: Uint<32>, w_sq: Uint<64>): [] {
    assert(w_sq <= tokens, "Weight too large: w^2 > tokens");
    const two_w = (w as Uint<64>) + (w as Uint<64>);
    assert(tokens - w_sq < two_w + 1, "Weight too small: use floor(sqrt(tokens))");
}
```

The caller computes off-chain and passes as witnesses:

```typescript
const w = Math.floor(Math.sqrt(Number(tokens)));
const w_sq = BigInt(w) * BigInt(w);
```

The circuit never computes a square root. It only verifies two inequalities — cheap in any arithmetic circuit.

### The general pattern

Anywhere you find an expensive function (sqrt, log, hash of large input):
1. Compute it off-chain in TypeScript
2. Pass the result as a witness
3. In the circuit, verify the result satisfies cheap mathematical constraints

### Fungible Token Module

> Source: "Building a Fungible Token in Compact" — Neeraj Choubisa

Compact has no inheritance. Use module composition instead:

```compact
// WRONG (Solidity thinking)
contract MyToken is ERC20 { ... }

// CORRECT (Compact)
import "./token/FungibleToken.compact" prefix FT_;

export circuit init(): [] {
    FT_.initialize("My Token", "MTK", 18);
    const owner = left<ZswapCoinPublicKey, ContractAddress>(ownPublicKey());
    FT_._mint(owner, 1000000);
}

export circuit transfer(
    to: Either<ZswapCoinPublicKey, ContractAddress>,
    amount: Uint<128>
): Boolean {
    return FT_.transfer(to, amount);
}
```

**Key differences from ERC-20:**
- Uses `Uint<128>` not `uint256`
- No events
- No contract-to-contract transfers (yet)
- Initialization is required and must not be skipped
- Use `circuit` not `function`

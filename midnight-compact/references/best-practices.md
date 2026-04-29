# Compact Best Practices

## Mental Model: Circuits Are Not Functions

> Source: Midnight Aliit Fellowship community articles

The single most important shift when learning Compact: **circuits declare constraints, they don't execute instructions.**

```
Function:  Input → Execute steps → Output
Circuit:   Input → Declare constraints → Generate proof → Verify proof
```

### What `assert` actually is

In a function, `assert` is a runtime guard that throws on failure.
In a circuit, `assert` is a **constraint declaration** — it defines what valid inputs look like. If the condition is false, the proof cannot be generated. There is no proof to submit. The transaction doesn't happen.

```compact
// This doesn't say "check if balance is high enough, then continue"
// It says "a proof for this circuit cannot exist if balance < amount"
assert(balance >= amount, "Insufficient balance");
```

### What `return a + b` means in a circuit

In a function: compute the sum and hand it back.
In a circuit: **the output is constrained to equal a + b**. The proof proves this relationship held for the actual inputs, without revealing them.

### Why no recursion or unbounded loops

ZK proofs require **finite circuits** — a fixed structure of gates and wires determined entirely at compile time. Unbounded computation can't become a circuit. The bounds aren't restrictions; they're what makes proof generation possible at all.

Use `map` and `fold` instead of loops with early returns.

### Compact vs TypeScript vs Solidity

| Concept | TypeScript | Solidity | Compact |
|---|---|---|---|
| Private data | Convention only | On-chain (visible) | Stays local, always |
| Functions | Execute instructions | Execute instructions | Declare constraints |
| Loops | Unbounded | Unbounded (gas-limited) | Bounded at compile time |
| Recursion | Allowed | Allowed | Not allowed |
| Privacy enforcement | None | None | Type system + compiler |

### Debugging circuits vs functions

With a function: ask "what line failed?" Add logging, trace execution.
With a circuit: ask "**which constraint is unsatisfied?**" There is no execution to trace. Every failure is a constraint problem, not a runtime error.

---

## On-Chain Design Patterns (From Production Experience)

> Source: "I Hit Midnight's Block Limits Twice" — Tushar Pamnani, Midnight Aliit

Midnight has hard limits (~1MB transaction size, ~1s compute). You're not optimizing cost — you're fitting inside a box.

### ❌ EVM thinking that breaks on Midnight

**Structs are not cheap.** Reading `bets.lookup(userPk)` pulls the entire struct into the circuit — every field, every time. Then updating one field requires reconstructing and writing the whole struct back.

```compact
// EXPENSIVE: read full struct, modify one field, write full struct
const userBet = bets.lookup(disclose(userPk));
const updatedBet = Bet {
  user: userBet.user,
  amount: userBet.amount,
  // ... all fields ...
  claimed: true,  // only this changed
};
bets.insert(disclose(userPk), disclose(updatedBet));
```

**Don't store metadata on-chain.** Names, descriptions, image URLs, categories — these belong in an indexer, not ledger state.

**Don't compute rewards on-chain.** Off-chain computation + Merkle root is the correct pattern.

### ✅ Minimal on-chain state

Ask: **"What is the minimum the chain needs to enforce?"**

```compact
// BEFORE (V1): struct with 6 fields per user
export ledger bets: Map<Bytes<32>, Bet>;  // Bet has user, amount, predictedValue, rewardAmount, claimed, timestamp

// AFTER (V3): just what the chain needs to verify
export ledger bets: Map<Bytes<32>, Uint<128>>;  // only the amount
```

### ✅ Flat maps over struct maps

Store each field independently instead of as a struct. Eliminates serialization overhead.

```compact
// EXPENSIVE: struct map
export ledger distData: Map<Uint<64>, DistributionData>;

// CHEAP: flat maps
export ledger distRoots: Map<Uint<64>, Bytes<32>>;
export ledger distPools: Map<Uint<64>, Uint<128>>;
export ledger distDeadlines: Map<Uint<64>, Uint<64>>;
export ledger distStatus: Map<Uint<64>, DistStatus>;
```

### ✅ Off-chain computation + Merkle root pattern

The chain should not know *how* something was computed — only *whether* it is valid.

```compact
// Admin submits Merkle root of off-chain computed rewards
export circuit submitDistribution(
  _merkleRoot: Bytes<32>,
  _totalRewardPool: Uint<128>,
  _claimDeadline: Uint<64>
): Uint<64> {
  distRoots.insert(disclose(id), disclose(_merkleRoot));
  distPools.insert(disclose(id), disclose(_totalRewardPool));
  // ...
}

// User claims with a proof — chain only verifies leaf is in tree
export circuit claimReward(leaf: Bytes<32>): [] {
  const path = get_membership_path(disclose(leaf));
  const computed_root = merkleTreePathRoot<20, Bytes<32>>(path);
  assert(distRoots.lookup(disclose(id)) == disclose(computed_root), "Invalid proof");
  // mark claimed, transfer
}
```

### What to delete from EVM-style contracts

When porting from EVM thinking, remove:
- Full struct maps → replace with `Map<Key, SingleValue>`
- Index maps (`betKeys`, `marketById` with full config) → off-chain can reconstruct
- Computed values stored on-chain (`totalParticipants`, `rewardAmount`) → compute off-chain
- Metadata fields (`name`, `description`, `imageUrl`) → indexer
- On-chain reward computation pipelines → Merkle root + off-chain

---



### Syntax Errors

**1. Using Block Syntax for Ledger**
```compact
❌ WRONG:
ledger {
  counter: Counter;
  owner: Bytes<32>;
}

✅ CORRECT:
export ledger counter: Counter;
export ledger owner: Bytes<32>;
```

**2. Using Void Return Type**
```compact
❌ WRONG:
export circuit increment(): Void {
  counter.increment(1);
}

✅ CORRECT:
export circuit increment(): [] {
  counter.increment(1);
}
```

**3. Rust-Style Enum Access**
```compact
❌ WRONG:
if (state == GameState::playing) { ... }

✅ CORRECT:
if (state == GameState.playing) { ... }
```

**4. Witness with Body**
```compact
❌ WRONG:
witness get_key(): Bytes<32> {
  return local_secret_key();
}

✅ CORRECT:
witness local_secret_key(): Bytes<32>;
```

**5. Using counter.value()**
```compact
❌ WRONG:
const val = counter.value();

✅ CORRECT:
const val = counter.read();
```

**6. Using 'function' Keyword**
```compact
❌ WRONG:
pure function helper(x: Field): Field { ... }

✅ CORRECT:
pure circuit helper(x: Field): Field { ... }
```

**7. Missing disclose() in Conditionals**
```compact
❌ WRONG:
const secret = get_secret();
if (guess == secret) { ... }

✅ CORRECT:
const secret = get_secret();
if (disclose(guess == secret)) { ... }
```

**8. Not Exporting Enums**
```compact
❌ WRONG (not accessible from TypeScript):
enum GameState { waiting, playing }

✅ CORRECT:
export enum GameState { waiting, playing }
```

**9. Using Deprecated Cell Type**
```compact
❌ WRONG:
export ledger value: Cell<Field>;

✅ CORRECT:
export ledger value: Field;
```

**10. Wrong Pragma Version**
```compact
❌ WRONG:
pragma language_version >= 0.16.0;

✅ CORRECT:
pragma language_version >= 0.19;
```

## Security

### Input Validation
```compact
circuit transfer(amount: Uint<64>) {
  assert(amount > 0, "Amount must be positive");
  assert(amount < MAX_AMOUNT, "Amount exceeds maximum");
}
```

### Prevent Reentrancy
- Use checks-effects-interactions pattern
- Update state before external calls
- Use reentrancy guards

### Access Control
```compact
export ledger owner: Bytes<32>;

circuit authenticated_action(): [] {
  const caller = public_key(local_secret_key());
  assert(disclose(caller == owner), "Not authorized");
  // ... action
}
```

### Avoid Information Leakage
```compact
❌ WRONG (leaks information):
if (secret_value > 100) {
  return true;
}

✅ CORRECT (use disclose explicitly):
if (disclose(secret_value > 100)) {
  return true;
}
```

## Performance

### Optimize Circuits
- Minimize constraint count
- Avoid expensive operations (division, modulo)
- Use lookup tables for complex logic
- Batch operations when possible

### Gas Efficiency
- Minimize on-chain storage
- Use events for historical data
- Batch transactions

### Counter vs Map
```compact
✅ EFFICIENT (for single value):
export ledger total: Counter;

❌ INEFFICIENT (for single value):
export ledger totals: Map<Bytes<32>, Uint<64>>;
```

## Testing

### Unit Tests
Test individual functions and circuits with various inputs.

### Integration Tests
Test contract interactions and state transitions.

### Property-Based Testing
Test invariants hold across all inputs.

### ZK-Specific Tests
- Verify proofs are generated correctly
- Test privacy properties
- Ensure no information leakage

## Code Quality

### Documentation
- Document all public functions
- Explain privacy properties
- Provide usage examples

### Code Organization
- Separate concerns (state, logic, circuits)
- Use modules for large contracts
- Keep functions small and focused

### Error Handling
- Use Result types for fallible operations
- Provide meaningful error messages
- Handle all edge cases

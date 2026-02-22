# Compact Best Practices

## Common Mistakes (v0.19+)

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

# Private State & Commitment Patterns

> Source: "You're Probably Using export ledger Wrong" + "Advanced Compact Patterns" — Midnight Aliit

## The Two Worlds

Every piece of state in a Compact contract lives in one of two worlds:

| | `export ledger` | Private state |
|---|---|---|
| Where it lives | Every node on the network | User's local storage |
| Who can read it | Anyone | Only the owner |
| On-chain representation | Plaintext value | Cryptographic commitment |
| Solidity equivalent | `public` storage variable | No equivalent |

**Privacy is the default. Disclosure is an explicit exception you must declare.**

## `disclose()` is a Waiver, Not Encryption

`disclose()` does not encrypt or protect data. It is a compile-time annotation that tells the compiler: "I know this witness data is going public, and I am doing it on purpose."

Without it, the compiler rejects your program:

```
Exception: line 6 char 11:
  potential witness-value disclosure must be declared but is not
```

The compiler tracks witness data through arithmetic, type conversions, and function calls. You cannot obfuscate your way past it:

```compact
// Still caught — arithmetic on witness data is still witness data
circuit obfuscate(x: Field): Field { return x + 73; }
export circuit record(): [] {
    balance = obfuscate(getBalance()) as Bytes<32>;  // compiler error
}
```

**Best practice:** Put `disclose()` as close to the disclosure point as possible.

## When to Use Each

| If your data... | Use... |
|---|---|
| Defines market price or global invariants | `export ledger` |
| Needs to be read by your frontend directly | `export ledger` |
| Is per-user and sensitive | Private state + commitment in ledger |
| Is a temporary computation input | Witness (no ledger at all) |
| Proves membership without revealing value | `persistentCommit` in `export ledger` |
| Is an identity you're intentionally publishing | `disclose()` + `export ledger` |

**Quick heuristic:** If removing this field from the chain would break another user's ability to interact with the contract, it belongs in `export ledger`. If it belongs only to one user, it belongs in private state.

## The Commitment Pattern

Store a commitment in the ledger instead of the value. Keep the actual value in private state.

```compact
// WRONG: fully public balances (Solidity-style)
export ledger balances: Map<Bytes<32>, Uint<64>>;

// RIGHT: commitments on-chain, values stay private
export ledger balanceCommitments: Map<Bytes<32>, Bytes<32>>;
```

In the circuit, prove the old commitment and assert the new one:

```compact
export circuit buy(n: Uint<64>): [] {
    const caller = disclose(callerAddress());
    const prevBalance = localBalance();   // witness: private
    const nonce = localNonce();           // witness: private
    const newNonce = freshNonce();        // witness: new random nonce

    // verify existing commitment
    const oldCommit = persistentCommit(prevBalance, nonce);
    assert(balanceCommitments[caller] == oldCommit, "Commitment mismatch");

    // write new commitment — balance stays private
    const newBalance = prevBalance + n;
    balanceCommitments.insert(caller, disclose(persistentCommit(newBalance, newNonce)));
}
```

## `transientCommit` vs `persistentCommit`

```compact
circuit transientCommit<T>(value: T, rand: Field): Field;    // within-proof only
circuit persistentCommit<T>(value: T, rand: Bytes<32>): Bytes<32>;  // safe for ledger storage
```

- Use `persistentCommit` for anything stored in `export ledger`
- Use `transientCommit` only for intermediate values within a single proof
- **Never reuse nonces** — two commitments with the same nonce and value are identical on-chain, breaking privacy

Note: `transientCommit(e)` is treated as non-witness data even if `e` contains witness data (the nonce hides the input). `transientHash(e)` is still tracked as witness-tainted.

## Derived Identity Pattern

Never store raw secret keys on-chain. Derive a public identifier inside the circuit:

```compact
circuit deriveKey(sk: Bytes<32>): Bytes<32> {
  return persistentHash<Vector<2, Bytes<32>>>(
    [pad(32, "midnight:escrow:key"), sk]
  );
}

export circuit createEscrow(sellerPk: Bytes<32>): [] {
  const sk = secretKey();    // private witness — never leaves the proof
  const pk = deriveKey(sk);  // computed inside the circuit
  buyer = disclose(pk);      // only the derived key goes on-chain
}
```

The domain separator (`"midnight:escrow:key"`) namespace-isolates key derivation. Without it, the same `secretKey` in two different contracts produces the same derived key, creating cross-contract linkage.

Authorization is proven in ZK: the caller demonstrates they know the secret whose derived key matches the on-chain value. No separate signature scheme needed.

## Multi-Party Coordination (Escrow Pattern)

> Source: "How Midnight Coordinates Two-Party Transfers" — Tushar Pamnani

The core problem: Alice's private balance lives on Alice's machine. Bob's lives on Bob's. There is no shared namespace for private values.

Solution: three interlocking mechanisms:
1. A **commitment scheme** that binds transfer terms cryptographically
2. A **derived identity system** that ties authorization to private keys
3. A **state machine** that enforces ordering

```compact
export ledger buyer: Bytes<32>;          // H(buyerSk) — pseudonym only
export ledger seller: Bytes<32>;         // sellerPk as passed
export ledger termsCommitment: Bytes<32>; // commit([amount, H(secret)], nonce)
export ledger state: EscrowState;
```

The buyer commits to `[amount, hash(releaseSecret)]` with a nonce. The seller must recompute the same commitment to prove they received the correct terms off-chain. The ZK proof verifies the handshake happened correctly without the chain ever seeing what was exchanged.

**State machine as security property:**

```compact
enum EscrowState { EMPTY, FUNDED, RELEASED, REFUNDED }

// Every circuit opens with a state assertion
assert(state == EscrowState.FUNDED, "Invalid state");
```

Once `RELEASED`, the escrow is frozen. No double-release, no re-creation. Enforced by the proof system, not application logic.

## ZK Membership Proofs (Allowlist Pattern)

> Source: "ZK Membership Proofs on Midnight" — Tushar Pamnani

Prove membership in a set without revealing which member you are.

```compact
export ledger merkle_root: Bytes<32>;         // single commitment to entire set
export ledger admin_commitment: Bytes<32>;    // H(adminSecret) — identity never on-chain
export ledger used_nullifiers: Set<Bytes<32>>; // replay protection

witness getSecret(): Bytes<32>;
witness getSiblings(): Vector<20, Bytes<32>>;
witness getPathIndices(): Vector<20, Boolean>;
```

The circuit reconstructs the Merkle root from a private path and asserts it matches the on-chain value:

```compact
export circuit verifyAndUse(nullifier: Bytes<32>): [] {
    // Step 1: compute leaf from secret
    const leaf = persistentHash<Vector<2, Bytes<32>>>([
        pad(32, "zk-allowlist:leaf:v1"), getSecret()
    ]);

    // Step 2: verify nullifier was computed from this secret
    const computed_nullifier = persistentHash<Vector<3, Bytes<32>>>([
        pad(32, "zk-allowlist:nullifier:v1"), getSecret(), getContext()
    ]);
    assert(computed_nullifier == nullifier, "Nullifier mismatch");

    // Step 3: reconstruct root (20 levels, manually unrolled)
    const h0 = hashLevelNode(path_indices[0], leaf, siblings[0]);
    // ... 19 more levels ...
    assert(calculated_root == merkle_root.read(), "Not a member");

    // Step 4: prevent replay
    assert(!used_nullifiers.member(disclose(nullifier)), "Already used");
    used_nullifiers.insert(disclose(nullifier));
}
```

**Why the nullifier is a circuit argument (not purely internal):** Making it explicit lets the TypeScript client query `used_nullifiers` before generating an expensive ZK proof, failing fast if already used.

**Why loops are manually unrolled:** ZK circuits must compile to a fixed-size constraint system. A loop over a runtime-length vector is impossible in any ZK system. Manual unrolling is verbose but compiles cleanly every time.

**The concatenation bug:** `hash("alice" + "ctx1") == hash("alic" + "ectx1")`. Always use fixed-length types (`Bytes<32>`) or length-prefix variable-length inputs to prevent hash collisions across field boundaries.

## What's Actually On-Chain (Allowlist Example)

| Data | On-chain | Observer learns |
|---|---|---|
| Merkle root | Yes | The set has this root — nothing about members |
| Admin commitment | Yes | Someone controls this — not who |
| Nullifier (after use) | Yes | Some secret+context was used — not which |
| Secret | No | Nothing |
| Leaf hash | No | Nothing |
| Merkle path | No | Nothing |

## Advanced: Metadata Leaks

Even with encrypted data, call patterns can leak information. Mitigate with dummy batching:

```compact
// Leaks: specific assetIds correlate with specific users
export circuit buyAsset(assetId: Uint<64>): Bytes<32> { ... }

// Mitigated: batch with dummy calls to hide which asset was actually bought
export circuit batchBuyAssets<#N>(
  assetIds: Vector<#N, Uint<64>>,
  isReal: Vector<#N, Boolean>
): Vector<#N, Bytes<32>> { ... }
```

## Sources

- [You're Probably Using export ledger Wrong](https://dev.to/midnight-aliit/youre-probably-using-export-ledger-wrong-4j1c) — Tushar Pamnani
- [How Midnight Coordinates Two-Party Transfers](https://dev.to/midnight-aliit/how-midnight-coordinates-two-party-transfers-3dfh) — Tushar Pamnani
- [ZK Membership Proofs on Midnight](https://dev.to/midnight-aliit/zk-membership-proofs-on-midnight-1e29) — Tushar Pamnani
- [Advanced Compact Patterns for Web3 Developers](https://dev.to/midnight-aliit/advanced-compact-patterns-for-web3-developers-4m9i) — Nasihudeen Jimoh

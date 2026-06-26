# Smart Contract Security

## Overview

Security for Compact contracts spans two distinct concerns. The first is traditional smart contract security: preventing unauthorized state changes, protecting funds, and ensuring correct business logic. The second is privacy security: preventing accidental disclosure of private data, protecting witness confidentiality, and ensuring that the zero-knowledge properties of the system are not compromised. Both concerns must be addressed for a contract to be secure.

## Privacy Leak Prevention

Privacy leaks occur when a contract inadvertently reveals private information through public channels. Preventing these leaks requires careful attention to what data appears in public disclosures and how state is managed.

### Disclosure Audit

Every value placed in the disclosure section of a circuit becomes permanently public. Before deploying a contract, audit every disclosure to confirm that it reveals only what is strictly necessary. Ask these questions for each disclosed value:

- Does this value need to be public for the application to function?
- Could this value be replaced with a commitment or a range proof?
- Does this value, combined with other public information, allow an observer to infer private data?

Values that pass through multiple functions may accumulate disclosure. A value that seems harmless in isolation may become identifying when combined with other disclosed values across different transactions.

### State Placement

Choose carefully between persistent and transient state. Persistent state is visible to validators and persists forever. Use persistent state only for values that genuinely need to survive across transactions and for which visibility is acceptable. Use transient state for intermediate values that do not need to persist.

Consider whether a value should be stored at all. If a computation can be verified without storing the intermediate results, avoid storing them. Every piece of stored state is a potential source of information leakage.

### Commitment Hygiene

When creating commitments to private data, ensure that the commitment scheme includes enough entropy to prevent brute-force attacks. A commitment to a small value (like a boolean or a small integer) is vulnerable to precomputation attacks unless a random salt is included.

```
// unsafe: commitment to small value
let bad: Bytes<32> = persistentHash(booleanValue);

// safer: commitment with random salt
let ok: Bytes<32> = persistentHash((booleanValue, randomSalt));
```

Always include a random salt when committing to values with limited entropy. The salt should be at least 128 bits of randomness.

## Witness Trust Boundaries

The witness contains all private inputs to the circuit. The circuit defines constraints that the witness must satisfy, but the circuit cannot enforce that the witness values are meaningful or honest. Understanding the trust boundary around witnesses is essential.

### What Witnesses Prove

Witnesses prove that the prover knows values that satisfy the circuit constraints. They do not prove that those values correspond to anything real. For example, a circuit that constrains `hash(x) == h` proves that the prover knows some x with hash h. It does not prove that x is a valid address, a real balance, or anything else about x.

### What Witnesses Do Not Prove

Witnesses do not prove that the prover actually possesses the assets they claim to have. An attacker who knows (or can compute) values that satisfy the circuit constraints can generate a valid proof even if those values do not correspond to any real on-chain state. The circuit must explicitly constrain witness values against on-chain state (through commitments, Merkle proofs, or other verifiable references) to prevent this.

### The Input Validation Principle

Every witness input that affects state changes must be validated against on-chain data. If a witness claims a balance of 1000, the circuit must verify that balance against the stored state. If a witness claims membership in a set, the circuit must verify a Merkle proof. Trust nothing from the witness that is not verified.

```
// unsafe: trusting witness value
let claimedBalance: Uint<128> = witness_input();
write(balances, user, claimedBalance);

// safer: verifying against stored state
let storedBalance: Uint<128> = read(balances, user);
let newBalance: Uint<128> = storedBalance + deposit;
write(balances, user, newBalance);
```

## Replay Protection

Replay attacks occur when a valid transaction is submitted to the network multiple times, causing its effects to be applied more than once. Compact contracts must implement replay protection to prevent this.

### Nullifier-Based Protection

The most common replay protection mechanism uses nullifiers. Each transaction includes a unique nullifier that is checked against persistent state. Once a nullifier is used, it cannot be reused.

```
ledger usedNullifiers: StateMap<Bytes<32>, Boolean>;

circuit function protectedAction(nullifier: Bytes<32>) {
    let wasUsed: Boolean = read(usedNullifiers, nullifier);
    constrain(!wasUsed);
    write(usedNullifiers, nullifier, true);
    // transaction logic here
}
```

The nullifier should be derived from transaction-specific data such as a nonce, a timestamp, or a hash of the transaction contents. This ensures that each transaction produces a unique nullifier.

### Nonce-Based Protection

For accounts that have a public nonce, replay protection can use an incrementing counter.

```
ledger nonces: StateMap<Bytes<32>, Uint<64>>;

circuit function nonceProtected(nonce: Uint<64>, sender: Bytes<32>) {
    let expectedNonce: Uint<64> = read(nonces, sender);
    constrain(nonce == expectedNonce);
    write(nonces, sender, expectedNonce + 1);
}
```

Nonce-based protection requires the nonce to be public (visible to validators) so they can verify the increment without executing the full circuit. This is acceptable for some applications but may reveal transaction frequency.

## Front-Running Resistance

Front-running occurs when an observer sees a pending transaction and submits their own transaction with higher fees to execute first, extracting value from the original transaction. On Midnight, the private nature of transactions provides natural front-running resistance because transaction details are not visible in the mempool.

### Commit-Reveal Patterns

For applications that require public state changes, consider a commit-reveal pattern. The user first submits a commitment to their intended action. After the commitment is included in a block, they reveal the action. This prevents front-runners from seeing the action before it is committed to.

```
ledger commitments: StateMap<Bytes<32>, Bytes<32>>;

circuit function commit(commitment: Bytes<32>) {
    write(commitments, sender, commitment);
}

circuit function reveal(action: Bytes<32>, salt: Bytes<32>) {
    let stored: Bytes<32> = read(commitments, sender);
    constrain(stored == persistentHash((action, salt)));
    // execute the action here
}
```

### Batching and Atomicity

Design operations to be atomic where possible. If a sequence of state changes must happen together or not at all, encode them in a single circuit function. This prevents partial execution attacks where an attacker interrupts a sequence between steps.

## Nullifier Safety

Nullifiers prevent double spending in the shielded pool. Incorrect nullifier implementation can lead to loss of funds or privacy.

### Use Standard Library Functions

Always use `createNullifier` from the standard library rather than implementing custom nullifier derivation. The standard library function includes domain separation and uses the correct cryptographic primitives.

### Uniqueness Guarantees

Ensure that each coin produces a truly unique nullifier. The nullifier derivation must include a unique serial number for the coin and the owner's secret key. Two different coins must never produce the same nullifier (which would prevent legitimate spending) and the same coin must always produce the same nullifier for the same owner (which enables double-spend detection).

### Nullifier Storage

Store nullifiers in persistent state (a StateMap or StateBoundedMerkleTree). Check for nullifier existence before allowing a spend. This is the mechanism that prevents double spending.

```
ledger spentNullifiers: StateMap<Bytes<32>, Boolean>;

circuit function spend(coin: Coin, secretKey: Bytes<32>) {
    let nf: Bytes<32> = createNullifier(coin.serial, secretKey);
    let alreadySpent: Boolean = read(spentNullifiers, nf);
    constrain(!alreadySpent);
    write(spentNullifiers, nf, true);
    // proceed with spend
}
```

## Domain Separation

Domain separation ensures that values from one context cannot be reused in a different context. Without domain separation, an attacker might be able to use a proof or commitment from one contract in another contract.

### Hashing with Context

When computing hashes or commitments, include a domain separator that identifies the contract and the specific purpose of the hash. The standard library's specialized hash functions (leafHash, entryPointHash) include domain separators automatically. For custom hashes, include a domain tag.

```
let safeHash: Bytes<32> = persistentHash((DOMAIN_TAG, data));
```

### Contract Identity

Use the contract's address as a domain separator when creating commitments that should be specific to a particular contract instance. This prevents commitments from one deployment from being used with a different deployment of the same contract code.

## Compiler Enforced vs Developer Responsibility

The Compact compiler enforces several security properties automatically, but many security properties remain the developer's responsibility.

### Compiler Enforced

The compiler enforces type safety, ensures that all circuit branches are satisfiable, prevents direct access to private state from outside the circuit, and guarantees that state reads and writes follow the atomicity model.

### Developer Responsibility

The developer is responsible for designing correct business logic, auditing disclosures for privacy leaks, implementing replay protection, validating witness inputs against on-chain state, and ensuring nullifiers are derived and used correctly.

## Security Checklist

Before deploying a Compact contract, verify each item on this checklist.

1. Every disclosed value has been audited and is strictly necessary.
2. All witness inputs that affect state are validated against on-chain data.
3. Replay protection is implemented for every state-changing operation.
4. Nullifiers use the standard library createNullifier function.
5. Spent nullifiers are stored persistently and checked before every spend.
6. Domain separation is used for all hashes and commitments.
7. Commitments to low-entropy values include random salts.
8. Persistent state is used only for values that need to survive across transactions.
9. The contract does not store private data in persistent state.
10. All enum match expressions are exhaustive and arithmetic operations include overflow protection.
11. Testing covers both valid and invalid witnesses and a third party has reviewed all disclosures.

# Ledger Operations in Compact

## Overview

Ledger operations in Compact manage the persistent state of a contract. The Midnight ledger stores data that survives across transactions and blocks, providing the durable memory that contracts need to track balances, ownership, and other application state. Compact provides three ledger storage abstractions with different tradeoffs.

## StateValue

`StateValue<T>` stores a single value of type T in the ledger. It is the simplest state abstraction and is appropriate for storing scalar values like a single counter, a total supply, or a single owner address.

### Declaration

StateValue is declared as a module-level variable with an explicit type parameter.

```
ledger totalSupply: StateValue<Uint<128>>;
ledger owner: StateValue<Bytes<32>>;
```

The `ledger` keyword indicates that the variable is stored in persistent blockchain state rather than in the circuit's transient memory.

### Reading

Reading a StateValue returns a Cell containing the current value. The Cell wrapper enables the modify-and-write-back pattern.

```
let current: Cell<Uint<128>> = read(totalSupply);
let value: Uint<128> = current;  // the actual value
```

### Writing

Writing a StateValue updates the stored value. The new value must be explicitly provided.

```
write(totalSupply, newSupply);
```

### Atomic Read and Write

The read-then-write pattern is atomic. Between reading and writing in the same circuit function, no other transaction can modify the value. This atomicity is guaranteed by the consensus protocol and eliminates race conditions that plague other smart contract platforms.

## StateMap

`StateMap<K, V>` stores a mapping from keys of type K to values of type V. It is the workhorse state abstraction for most contracts, used for balance maps, allowance maps, and any other key-value storage.

### Declaration

```
ledger balances: StateMap<Bytes<32>, Uint<128>>;
ledger allowances: StateMap<Bytes<32>, StateMap<Bytes<32>, Uint<128>>>;
```

StateMap keys can be any fixed-size type (Uint, Bytes, or a struct of fixed-size fields). Nested StateMaps are allowed, as shown in the allowances example above.

### Reading

Reading from a StateMap requires a key. The read returns the value associated with that key or a default value if the key has never been written.

```
let balance: Uint<128> = read(balances, alice_address);
```

If the key does not exist in the map, the read returns the type's zero value (0 for Uint types, 0x00... for Bytes types). There is no way to distinguish between a key that has never been written and a key that was written with the zero value. If this distinction matters, use a separate StateMap to track which keys exist.

### Writing

Writing to a StateMap associates a value with a key.

```
write(balances, alice_address, newBalance);
```

Writing a value of zero is allowed and is indistinguishable from a key that has never been written. If the application requires distinguishing absent keys from zero values, consider using a non-zero sentinel or a separate existence map.

### Iteration

StateMap does not support iteration. The set of keys in a StateMap is not directly available to circuit functions. If the contract needs to operate on all entries, the caller must supply the list of keys as a witness input and the circuit can verify each one individually.

## StateBoundedMerkleTree

`StateBoundedMerkleTree<K, V>` stores key-value pairs in a Merkle tree structure. It supports membership proofs (proving that a key-value pair exists in the tree) and non-membership proofs (proving that a key does not exist in the tree). It is used for the shielded UTXO set and other applications requiring efficient cryptographic proofs of inclusion.

### Declaration

```
ledger coinTree: StateBoundedMerkleTree<Bytes<32>, Bytes<64>>;
```

The first type parameter is the key type and the second is the value type. The tree has a fixed maximum depth specified at contract deployment time.

### Insertion

Inserting a key-value pair into the Merkle tree requires providing the key, the value, and the leaf index where the pair should be inserted.

```
insert(coinTree, leafIndex, key, value);
```

The insertion operation modifies the Merkle root stored in the ledger. The new root commits to the updated set of entries.

### Membership Proofs

A membership proof demonstrates that a particular key-value pair exists at a specific leaf index in the tree. The proof includes the Merkle path from the leaf to the root.

```
let isMember: Boolean = isMember(coinTree, key, value, merklePath);
```

The circuit can constrain `isMember` to be true, ensuring that the claimed key-value pair genuinely exists in the tree before proceeding with operations that depend on that pair.

### Non-Membership Proofs

A non-membership proof demonstrates that a particular leaf index contains either no entry or a different entry than the one claimed.

```
let notMember: Boolean = isNonMember(coinTree, key, merklePath);
```

Non-membership proofs are important for nullifier schemes. They prove that a particular leaf position does not already contain a spent coin commitment.

## Hash and Commit Patterns

Compact provides four hashing modes for state operations, each with different properties regarding persistence and visibility.

### persistentHash

`persistentHash` hashes data and stores the result permanently in the ledger. The hash is visible to validators and persists across transactions.

```
let commitment: Bytes<32> = persistentHash(data);
```

Use persistentHash when the commitment must be available for verification by any future transaction. Coin commitments and contract state roots use persistentHash.

### persistentCommit

`persistentCommit` is similar to persistentHash but specifically for committing to private state values. The commitment is stored on chain, and the original data can be proven against it later.

```
let stateCommitment: Bytes<32> = persistentCommit(privateState);
```

### transientHash

`transientHash` hashes data but does not store the result. The hash exists only during the current circuit execution and is useful for intermediate computations.

```
let tempHash: Bytes<32> = transientHash(intermediateData);
```

TransientHashe are not stored on chain and cannot be referenced by future transactions. They are purely for use within the current circuit's constraint system.

### transientCommit

`transientCommit` creates a commitment that exists only for the current transaction. It is used when the commitment is needed for constraint purposes but does not need to persist.

```
let tempCommitment: Bytes<32> = transientCommit(ephemeralData);
```

## State Lifecycle

### degradeToTransient

`degradeToTransient` converts a persistent state value to transient. The value is removed from persistent storage and becomes available only within the current transaction.

```
degradeToTransient(myState);
```

This operation is useful for archiving old state or for transitioning state from persistent to ephemeral.

### upgradeFromTransient

`upgradeFromTransient` converts a transient state value to persistent. The value is written to the ledger and becomes available to future transactions.

```
upgradeFromTransient(myState);
```

This operation is used when ephemeral computations produce results that should be preserved.

## Alignment and Encoding

### Data Alignment

State values must be aligned to their natural boundaries. The Compact compiler handles alignment automatically based on the type's size. Misaligned values are rejected at compile time.

### Encoding

State values are encoded in a canonical binary format before being written to the ledger. The encoding scheme is deterministic: the same value always produces the same bytes. This ensures that state commitments are consistent across different provers and validators.

The default encoding for Uint values is big-endian. Bytes values are stored as-is. Structs are encoded by concatenating the encodings of their fields in order. The CompactType TypeScript classes use the same encoding scheme, ensuring consistency between the Compact layer and the TypeScript layer.

### State Commitment Root

The ledger maintains a single state commitment root that commits to all persistent state. Every read and write operation contributes to this root through Merkle hashing. The root changes when state is written and remains constant when state is only read. The state root is included in every block header, enabling light clients to verify state inclusion without downloading the full state.

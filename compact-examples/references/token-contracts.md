# Token Contracts for Compact

OpenZeppelin style token implementations targeting the Midnight Network privacy preserving runtime.

## FungibleToken

The FungibleToken contract models a standard token with transferability and balance tracking using Compact ledger types.

### Ledger State

Tokens are stored as a `Map<Bytes, Uint<256>>` mapping address hashes to balances. The total supply lives in a single `Uint<256>` cell. An additional `Map<Bytes, Map<Bytes, Uint<256>>>` tracks allowances for the approval system.

### Transfer Flow

A transfer circuit consumes the sender witness and recipient address. It checks the sender balance against the transfer amount, subtracts from the sender, and adds to the recipient. The guaranteed phase commits both balance mutations atomically so no partial state can leak through.

### Approval Pattern

The approve circuit stores an allowance from the owner to a spender in the nested allowance map. TransferFrom reads that allowance, validatesthe spender witness matches, deducts from both allowance and owner balance, and credits the destination. This pattern mirrors the ERC-20 approval model but wraps each mutation in ZK guarantees.

### Privacy Considerations

Balances and allowances stored in ledger Maps are publicly visible to indexer queries. To hide individual holdings implement a commitment based balance scheme where each user stores a hash commitment to their balance and opens it in circuit witnesses. This increases circuit complexity but eliminates on-chain balance enumeration.

## NonFungibleToken

The NonFungibleToken contract handles unique digital assets with ownership tracking and metadata.

### Ledger State

A `Map<Uint<256>, Bytes>` maps token IDs to owner hashes. A `Map<Uint<256>, String>` holds metadata URIs. An ownership counter tracks the number of tokens each address holds via `Map<Bytes, Uint<256>>`.

### Minting Circuit

The mint circuit requires a minter witness checked against a stored minter role. It assigns a new token ID, sets the owner to the target address, stores the metadata URI, and increments the ownership counter. Token IDs are sequential or derived from a content hash depending on the implementation choice.

### Transfer Circuit

NFT transfer validates owner witness, updates the token ID owner mapping, decrements the sender ownership counter, and increments the recipient counter. The metadata URI remains immutable after mint.

### Metadata Extension

An optional metadata update circuit allows the current owner to change the URI string. This supports reveals, content refresh, or IPFS gateway migration. The owner witness guards the mutation.

### Privacy Considerations

Ownership records are inherently public for standard NFTs. For anonymous ownership use a nullifier based registry where each token transfer consumes an old nullifier and emits a new one, keeping the owner address off the public ledger entirely.

## MultiToken

The MultiToken contract unifies fungible and non-fungible asset management under a single contract interface.

### Ledger State

A `Map<Bytes, Map<Bytes, Uint<256>>>` stores balances keyed by both token class and owner. Token class metadata lives in a `Map<Bytes, TokenClass>` struct holding the class type (fungible or non-fungible), total supply, and URI.

### Batch Operations

The batchTransfer circuit processes an array of token class and recipient pairs in a single transaction. Each iteration validates the sender has sufficient balance for that class, deducts, and credits. This reduces transaction count when moving multiple asset types at once.

### Class Creation

The createTokenClass circuit initializes a new token class with type, initial supply, and metadata. A creator role witness controls who may mint new classes. The class ID is derived from the creator address and a nonce.

### Privacy Considerations

MultiToken exposes the same surface area as FungibleToken and NonFungibleToken combined. The batch transfer reveals which classes moved together which may correlate user activity. Separate transactions for sensitive asset classes can reduce this linkage.

## Contract Code Structure Overview

A well organized Compact contract follows this layout.

1. Import statements pulling in standard library modules
2. Type aliases and constants at the top of the file
3. Ledger state declarations annotated with visibility intent
4. Circuit definitions each wrapped with a clear name and purpose comment
5. Witness declarations grouped by the circuits that consume them
6. Guaranteed phase operations appearing before fallible phase logic
7. Error handling via Compact assertions with descriptive messages

## State Design Patterns

### Map Based Registries

Use `Map<K, V>` for most token storage needs. Maps support O(1) lookup in the ZK circuit and produce compact ZKIR. Avoid deeply nested maps as each nesting level multiplies circuit complexity.

### Struct Encapsulation

Wrap related fields into `struct` types imported from a shared types module. Token metadata, user profiles, and configuration parameters all benefit from struct grouping. Structs must be serializable into the ledger storage format.

### Counter Nonces

Sequential counters prevent replay attacks and enable deterministic address derivation. Each user and contract maintains a nonce that must be incremented inside each transaction. The circuit witnesses the current nonce and outputs the incremented value.

### Access Control Through Roles

Store role definitions as `Map<Bytes, Bool>` indicating whether an address holds admin, minter, or pauser privileges. Circuit guards check the role map before allowing privileged operations. Role changes themselves require an admin witness.

## Summary

These token contract patterns provide a foundation for building privacy aware assets on Midnight. Choose FungibleToken for currencies, NonFungibleToken for unique items, and MultiToken for platforms managing diverse asset types. Always evaluate what data becomes public through ledger storage and apply commitment or nullifier patterns where privacy is required.

# Kachina Protocol

## Overview

Kachina is Midnight's **foundational smart contract protocol** that enables data-protecting smart contracts. It's not just a feature—it's THE architecture that makes Midnight's privacy-preserving smart contracts possible.

## Core Concept

Kachina bridges the gap between **public blockchain state** and **private local state** using zero-knowledge proofs.

### The Two-State Model

```
┌─────────────────────────────────────────────────────────┐
│                    KACHINA ARCHITECTURE                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  PUBLIC STATE    │         │  PRIVATE STATE   │     │
│  │  (On-Chain)      │◄───────►│  (Local)         │     │
│  │                  │   ZK    │                  │     │
│  │  - Visible to all│  Proofs │  - User's device │     │
│  │  - Blockchain    │         │  - Never shared  │     │
│  │  - Immutable     │         │  - Encrypted     │     │
│  └──────────────────┘         └──────────────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Public State (On-Chain)
- **Location**: Midnight blockchain
- **Visibility**: Everyone can see
- **Content**: Transaction proofs, contract code, public data
- **Examples**: Vote counts, token balances (if public), contract addresses

### Private State (Local)
- **Location**: User's device
- **Visibility**: Only the user
- **Content**: Personal data, secrets, private inputs
- **Examples**: Individual votes, private keys, medical records

## How Kachina Works

### 1. Reactive State Machines

Contracts are **reactive state machines** that respond to user transactions:

```
User Transaction → Contract Processes → Updates Both States
```

### 2. Zero-Knowledge Bridge

The magic happens through **ZK-SNARKs**:

```typescript
// User proves locally (private)
const proof = generateProof({
  privateInput: userSecret,
  publicInput: contractState
});

// Blockchain verifies (public)
const valid = verifyProof(proof);
if (valid) {
  updatePublicState();
  // User updates private state locally
}
```

### 3. Simultaneous Updates

Kachina contracts update **both states simultaneously**:
- **Public state**: Updated on blockchain
- **Private state**: Updated on user's device

## The Transcript Mechanism

### What Are Transcripts?

Transcripts record the **operations performed** on contract state:

```
Transcript = [
  query(state, "balance"),
  update(state, "balance", newValue),
  query(state, "owner")
]
```

### Why Transcripts Matter

1. **Concurrency**: Multiple users can interact without blocking
2. **Privacy**: Queries don't reveal actual data
3. **Verification**: Proofs validate transcript correctness

### Transcript Validation

```
User creates transcript → Generates ZK proof → Blockchain validates
```

The proof shows:
- ✅ Transcript is valid
- ✅ User knows required private data
- ❌ WITHOUT revealing the private data

## Concurrency in Kachina

### The Problem
Traditional smart contracts process transactions sequentially, creating bottlenecks.

### Kachina's Solution

**Transcript-based concurrency**:
- Multiple users create transcripts in parallel
- Conflicting transactions are reordered
- Non-conflicting transactions process simultaneously

```
User A: Transfer 10 tokens (UTXO #1)
User B: Transfer 5 tokens (UTXO #2)
↓
Both process in parallel (different UTXOs)
```

### Conflict Resolution

When conflicts occur:
```
User A: Spend UTXO #1
User B: Spend UTXO #1 (same!)
↓
Kachina reorders or rejects to maintain consistency
```

## Security Model

### Universally Composable (UC) Framework

Kachina is proven secure under the **UC security framework**:
- **Formal verification**: Mathematical proof of security
- **Composability**: Secure when combined with other protocols
- **Strong guarantees**: Protects against all polynomial-time adversaries

### What's Protected

✅ **Private state confidentiality**: Never revealed  
✅ **Proof soundness**: Can't fake valid proofs  
✅ **State consistency**: Public/private states stay synchronized  
✅ **Transaction atomicity**: All-or-nothing updates  

### What's NOT Protected

❌ **Witness data**: Witnesses are untrusted (by design)  
❌ **Timing information**: Transaction timing may leak info  
❌ **Public state**: Intentionally visible  

## Practical Example: Private Voting

### Setup
```compact
// Public state (on-chain)
ledger voteCount: Counter;
ledger votingOpen: Boolean;

// Private state (local)
witness hasVoted(): Boolean;
witness voterSecret(): Bytes<32>;
```

### Voting Process

1. **User creates transcript locally**:
```
- Check votingOpen == true
- Check hasVoted() == false
- Increment voteCount
- Mark hasVoted() = true
```

2. **Generate ZK proof**:
```
Proof: "I know a voterSecret that hasn't voted yet"
```

3. **Submit to blockchain**:
```
- Blockchain verifies proof
- Updates voteCount (public)
- User updates hasVoted (private)
```

### Result
- ✅ Vote counted publicly
- ✅ Individual vote remains private
- ✅ Double-voting prevented
- ✅ No voter identity revealed

## Kachina vs Traditional Smart Contracts

| Aspect | Traditional (Ethereum) | Kachina (Midnight) |
|--------|----------------------|-------------------|
| **State** | All public | Public + Private |
| **Execution** | On-chain (redundant) | Off-chain + ZK proof |
| **Privacy** | None | Built-in |
| **Concurrency** | Sequential | Parallel (via transcripts) |
| **Verification** | Re-execute code | Verify ZK proof |
| **Cost** | High (all nodes execute) | Lower (proof verification) |

## Key Advantages

### 1. Privacy by Design
Not bolted on—privacy is fundamental to the architecture.

### 2. Efficient Verification
Verifying a ZK proof is faster than re-executing code.

### 3. Selective Disclosure
Choose exactly what to reveal:
```compact
// Reveal only the count, not individual votes
export circuit getVoteCount(): Uint<64> {
  return voteCount.read();
}

// Individual votes stay private
witness myVote(): Boolean; // Never exported
```

### 4. Compliance-Friendly
Can prove compliance without revealing data:
```
Proof: "My transaction follows KYC rules"
(without revealing identity)
```

## Compact Language Integration

Kachina concepts map directly to Compact:

```compact
// Public state = ledger declarations
ledger publicData: Field;

// Private state = witness functions
witness privateData(): Field;

// ZK bridge = circuit definitions
export circuit processData(): [] {
  const private = privateData();  // Local
  const public = publicData;      // On-chain
  
  // Proof generated automatically
  publicData = disclose(private + public);
}
```

## Use Cases Enabled by Kachina

### 1. Private DeFi
- Trade without revealing positions
- Prove solvency without revealing balances
- Confidential order books

### 2. Healthcare
- Share medical data with access control
- Prove eligibility without revealing records
- HIPAA-compliant blockchain apps

### 3. Governance
- Private voting with public results
- Prove membership without revealing identity
- Confidential proposals

### 4. Supply Chain
- Track goods without revealing suppliers
- Prove authenticity without revealing sources
- Confidential business relationships

## Technical Deep Dive

### Transcript Structure

```typescript
type Transcript = {
  queries: Query[],      // State reads
  updates: Update[],     // State writes
  assertions: Assert[]   // Validity checks
};

type Query = {
  field: string,
  expectedValue: Value  // Committed, not revealed
};

type Update = {
  field: string,
  newValue: Value
};
```

### Proof Generation

```
1. User creates transcript locally
2. Compact compiler generates circuit
3. Circuit takes private inputs + transcript
4. Proof shows: "This transcript is valid for some private state"
5. Blockchain verifies proof + applies public updates
```

### State Synchronization

```
┌─────────────────────────────────────────┐
│  Transaction Lifecycle                   │
├─────────────────────────────────────────┤
│                                          │
│  1. User: Create transcript (local)      │
│  2. User: Generate proof (local)         │
│  3. User: Submit tx (to blockchain)      │
│  4. Blockchain: Verify proof             │
│  5. Blockchain: Update public state      │
│  6. User: Update private state (local)   │
│                                          │
│  States stay synchronized via proofs     │
└─────────────────────────────────────────┘
```

## Limitations and Considerations

### 1. Proof Generation Cost
- Generating ZK proofs is computationally expensive
- Requires proof server or local proving
- Trade-off: Privacy vs computation time

### 2. State Size
- Private state grows with user activity
- Users must manage local storage
- Pruning strategies needed for long-term use

### 3. Transcript Complexity
- Complex contracts = complex transcripts
- More queries/updates = larger proofs
- Design for efficiency

### 4. Concurrency Limits
- Conflicts still require resolution
- High contention can reduce parallelism
- Design for minimal shared state

## Best Practices

### 1. Minimize Public State
```compact
// ❌ Too much public
ledger userBalance: Map<Address, Uint<64>>;

// ✅ Keep private
witness myBalance(): Uint<64>;
ledger totalSupply: Uint<64>; // Only aggregate
```

### 2. Design for Concurrency
```compact
// ✅ Independent UTXOs = parallel processing
ledger coins: MerkleTree<32, Coin>;

// ❌ Shared counter = sequential bottleneck
ledger globalCounter: Counter;
```

### 3. Batch Operations
```compact
// ✅ Batch updates in one transaction
export circuit batchProcess(items: Vector<10, Item>): [] {
  for (const i of 0..10) {
    processItem(items[i]);
  }
}
```

### 4. Optimize Transcripts
```compact
// ❌ Many queries
const a = field1.read();
const b = field2.read();
const c = field3.read();

// ✅ Batch reads
const data = readAll(); // Single query
```

## Resources

- **Research Paper**: [Kachina - Foundations of Private Smart Contracts](https://eprint.iacr.org/2020/543.pdf)
- **Compact Language**: See midnight-compact skill
- **ZK Proofs**: See zk-proofs.md reference
- **Use Cases**: See use-cases.md reference

## Summary

Kachina is Midnight's **secret sauce**:
- Enables public + private state
- Uses ZK proofs as the bridge
- Provides transcript-based concurrency
- Proven secure under UC framework
- Powers all Midnight smart contracts

Understanding Kachina is essential for building on Midnight—it's not just a feature, it's the foundation.

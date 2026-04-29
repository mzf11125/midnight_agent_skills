# Midnight Network Architecture

## Overview

Midnight is a partner chain to Cardano, designed to provide privacy-preserving smart contract capabilities while inheriting Cardano's security and decentralization.

## Partner Chain Architecture

### What is a Partner Chain?

A partner chain is a separate blockchain that connects to and inherits security from a main chain (Cardano), rather than being completely independent.

### Benefits of Partner Chain Design

**Security Inheritance**:
- Leverages Cardano's proven consensus mechanism
- Benefits from Cardano's validator network
- Inherits economic security model

**Specialized Capabilities**:
- Optimized for privacy (ZK proofs, Zswap)
- Custom virtual machine for Compact contracts
- Privacy-specific features not possible on main chain

**Interoperability**:
- Bridge assets between Cardano and Midnight
- Leverage Cardano's ecosystem
- Unified security model

### How It Works

1. **Cardano Main Chain**: Provides security anchor
2. **Midnight Partner Chain**: Executes privacy-preserving contracts
3. **Bridge**: Enables asset transfer between chains
4. **Shared Validators**: Can validate both chains

## Consensus Mechanism

### Ouroboros-Based Consensus

Midnight uses a variant of Ouroboros, Cardano's proof-of-stake consensus protocol.

**Key Properties**:
- Provably secure (peer-reviewed research)
- Energy efficient (proof-of-stake)
- Decentralized validator selection
- Finality guarantees

### Validator Participation

**Staking**:
- Validators stake tokens to participate
- Economic incentive for honest behavior
- Slashing for misbehavior

**Block Production**:
- Validators selected based on stake
- Produce blocks in assigned slots
- Include transactions and proofs

**Rewards**:
- Block rewards for validators
- Transaction fees
- Distributed based on stake and performance

## Network Layers

### Layer 1: Blockchain Layer

**Components**:
- Block production and validation
- Transaction ordering
- State commitment
- Consensus

**Responsibilities**:
- Maintain global state
- Verify zero-knowledge proofs
- Enforce protocol rules
- Distribute rewards

### Layer 2: State Channels (Hydra)

**Components**:
- Off-chain transaction processing
- State channel management
- Dispute resolution

**Responsibilities**:
- Enable high-throughput transactions
- Provide instant finality off-chain
- Settle final state on Layer 1

## Core Components

### Midnight Node

The core network software that:
- Validates transactions and blocks
- Maintains blockchain state
- Participates in consensus
- Serves network data

**Key Functions**:
- Block production (for validators)
- Transaction validation
- Proof verification
- State synchronization

### Midnight Indexer

Database service that:
- Indexes blockchain data
- Provides query interface
- Tracks contract state
- Enables efficient data access

**Use Cases**:
- DApp data queries
- Historical transaction lookup
- Contract state inspection
- Analytics and monitoring

### Proof Server

Specialized service for:
- Generating zero-knowledge proofs
- Optimized proving hardware
- Proof caching
- Delegated proving

**Benefits**:
- Offload computation from clients
- Faster proof generation
- Better user experience
- Shared infrastructure

## Virtual Machine

### Compact VM

Purpose-built virtual machine for executing Compact smart contracts.

**Design Goals**:
- Efficient ZK proof generation
- Deterministic execution
- Gas metering for resource control
- Security and isolation

**Execution Model**:
1. Compile Compact to VM bytecode
2. Execute contract logic
3. Generate ZK proofs of execution
4. Verify proofs on-chain

### State Management

**On-Chain State**:
- Contract storage
- Zswap coin commitments
- Nullifier set (prevent double-spending)
- Global parameters

**Off-Chain State**:
- User wallet state
- Private keys and secrets
- Unspent coin information
- Local transaction history

## Security Model

### Cryptographic Security

**Assumptions**:
- Elliptic curve discrete logarithm hardness
- Collision-resistant hash functions
- Secure ZK proof system

**Guarantees**:
- Transaction validity
- Privacy preservation
- Double-spend prevention
- State integrity

### Economic Security

**Stake-Based Security**:
- Validators have economic stake
- Misbehavior results in slashing
- Rewards incentivize honest behavior

**Attack Costs**:
- 51% attack requires majority stake
- Economically infeasible for well-staked network
- Slashing increases attack cost

### Network Security

**Peer-to-Peer Network**:
- Decentralized node communication
- Gossip protocol for transaction propagation
- DDoS resistance
- Sybil attack protection

## Cardano Integration

### Asset Bridge

**Bridging Mechanism**:
- Lock assets on Cardano
- Mint equivalent on Midnight
- Burn on Midnight to unlock on Cardano

**Security**:
- Cryptographic proofs of lock/unlock
- Validator consensus on bridge operations
- No trusted intermediaries

### Shared Security

**Validator Overlap**:
- Cardano validators can also validate Midnight
- Shared economic security
- Coordinated upgrades

**Checkpoint System**:
- Midnight state checkpointed on Cardano
- Additional security layer
- Recovery mechanism

## Development by IOG

### Research-First Approach

**Process**:
1. Peer-reviewed academic research
2. Formal specification
3. Implementation
4. Formal verification

**Benefits**:
- High assurance of correctness
- Proven security properties
- Academic rigor
- Long-term thinking

### Open Source

**Philosophy**:
- All code publicly available
- Community review and contribution
- Transparent development
- No hidden backdoors

**Repositories**:
- Midnight node
- Compact compiler
- SDKs and tools
- Documentation

### Team Expertise

**Cryptographers**:
- Zero-knowledge proof systems
- Privacy-preserving protocols
- Formal security analysis

**Programming Language Researchers**:
- Compact language design
- Type systems
- Compiler optimization

**Distributed Systems Experts**:
- Consensus protocols
- Network architecture
- Scalability solutions

## Network Topology

### Node Types

**Validator Nodes**:
- Participate in consensus
- Produce blocks
- Require stake

**Full Nodes**:
- Validate all transactions
- Maintain full blockchain state
- Don't produce blocks

**Light Clients**:
- Verify block headers only
- Query full nodes for data
- Minimal resource requirements

### Network Communication

**Gossip Protocol**:
- Efficient transaction propagation
- Block distribution
- Peer discovery

**RPC Interface**:
- Query blockchain data
- Submit transactions
- Monitor network status

## Scalability

### Current Approach

**Layer 1**:
- Optimized block size and timing
- Efficient proof verification
- Parallel transaction processing

**Layer 2**:
- State channels (Hydra)
- Off-chain computation
- Batch settlement

### Future Enhancements

**Sharding** (Potential):
- Parallel chain execution
- Increased throughput
- Maintained security

**Rollups** (Potential):
- Batch transactions off-chain
- Submit proofs on-chain
- Scalability with security

## Governance

### Protocol Upgrades

**Process**:
- Proposal submission
- Community discussion
- Validator voting
- Coordinated activation

**Considerations**:
- Backward compatibility
- Security implications
- Community consensus

### Parameter Adjustment

**Adjustable Parameters**:
- Block size and timing
- Fee structure
- Reward distribution
- Consensus parameters

**Governance Mechanism**:
- On-chain voting
- Stake-weighted decisions
- Gradual parameter changes

## Comparison to Other Architectures

### vs. Ethereum L2s
- **Midnight**: Partner chain with own consensus
- **L2s**: Rely on Ethereum for security
- **Trade-off**: More independence vs simpler security model

### vs. Independent Chains
- **Midnight**: Inherits Cardano security
- **Independent**: Build security from scratch
- **Trade-off**: Shared security vs full autonomy

### vs. Privacy Coins (Zcash, Monero)
- **Midnight**: Programmable privacy (smart contracts)
- **Privacy Coins**: Transaction privacy only
- **Trade-off**: Flexibility vs simplicity

---

## DUST vs NIGHT: The Dual-Token Model

> Source: "DUST vs NIGHT: Rethinking How Blockchains Handle Value and Fees" — Neeraj Choubisa

Most blockchains use one token for everything (ETH pays gas AND stores value). Midnight splits these responsibilities.

### NIGHT — the asset layer

- Fixed supply (24 billion)
- Public (unshielded)
- Used for: governance, staking, consensus, block rewards, exchange trading
- Think of it as solar panels

### DUST — the resource layer

- Not a traditional token — it's a resource generated by NIGHT
- You don't buy or trade it; you earn it by holding NIGHT
- Used exclusively to pay transaction fees
- Leftover DUST returns to you after a transaction
- Non-transferable between users
- Decays to zero if you stop backing it with NIGHT (prevents hoarding)
- Think of it as electricity generated by the solar panels

### Why this matters for developers

- Transaction costs are **predictable** — DUST regenerates at a fixed rate from NIGHT holdings, decoupled from market speculation
- Enterprises can budget for on-chain compute in advance
- Protects against MEV attacks
- DUST transactions are **shielded** — no public fee tracking, no visible activity graph

### Shielded vs Unshielded tokens

Developers choose per-contract:
- **Unshielded** → public (like ETH), good for DeFi composability
- **Shielded** → private via ZK proofs, good for sensitive data

### Viewing keys

Share a viewing key to give selective read access to your private transactions (for compliance/auditing). **Irreversible once shared.**

---

## Mainnet Architecture & Roadmap

> Source: "Midnight Mainnet Is Live. The Privacy Stack Just Got Real." — Barnabas

Mainnet genesis block: **March 30, 2026**. Launched in a federated model ("guarded era") with 9 institutional validator partners.

### Current stable versions (mainnet launch)

- Compact: 0.28.0
- midnight-js: 3.0.0
- wallet-sdk: 1.0.0
- Proof Server: 7.0.0

### Architecture highlights

**Hybrid dual-state model**: UTXO + account-based in a single atomic step. Public state on-chain (unshielded), private state in off-chain execution environment. The Kachina Protocol bridges them.

**Client-side proofs**: ZK proofs generated on the user's device via a local proof server. Sensitive data never leaves the user's machine.

**Selective disclosure**: Developers control what's public vs private at the contract level. Example: verify KYC status without storing personal data on-chain.

### Roadmap phases

| Phase | Timing | Key milestone |
|---|---|---|
| Kūkolu | Now | Federated mainnet live, first production DApps |
| Mōhalu | Mid-2026 | Cardano SPOs as block producers, DUST Capacity Exchange, staking rewards |
| Hua | Late 2026 | Hybrid DApps — Midnight privacy layer embeddable into other chains |

### AI coding tools and Midnight

General-purpose AI assistants (Claude, Cursor, Copilot) don't have Compact training data and generate hallucinated code. Use the **Midnight MCP server** to give AI tools structured access to Compact docs and static analysis. Downloaded 6,000+ times via npm.

---

## AI Agent Identity on Midnight

> Source: "Selective Disclosure & Self-Managing DIDs for AI Agents" — Alex Pestchanker

AI agents increasingly act autonomously — executing transactions, accessing sensitive data, representing users. But there's no standardized identity or trust framework for agents.

### The problem

| Capability | Maturity |
|---|---|
| Autonomy | High |
| Intelligence | High |
| Access to sensitive data | High |
| Identity & trust model | Extremely low |

Agents commonly store API keys in plain text, access personal data, and execute transactions — with no formal identity layer.

### Midnight as the identity execution layer

Midnight's programmable privacy makes it suited for agent identity:
- Confidential smart contracts
- Shielded data handling
- Selective disclosure primitives (prove attributes without revealing raw data)

### Core components for agent identity

**Agent DID**: Each agent has a unique DID with public/private key pair and associated verifiable credentials.

**Agent Vault**: A secure execution boundary — the agent never directly handles raw secrets, it requests controlled access from the vault. Stores private keys, credentials, API keys, and enforces access policies.

**Selective Disclosure Engine**: Generates proofs instead of raw data. Examples:
- "Payment Authorized" without revealing wallet balance
- "KYC verified" without sharing identity
- "Valid Agent Identity" without exposing owner

**Policy Engine**: Defines what the agent is allowed to do, under what conditions, with which credentials.

### MVP

Prototype: https://github.com/apestchanker/midnight-agent-did-manager

⚠️ Research prototype, not production-ready. Demonstrates DID generation, VC association, and selective disclosure preparation.

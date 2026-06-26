# Midnight Architecture

## Overview

Midnight is a Layer 1 blockchain that combines public verification with private computation. The network uses a novel three-part contract model and a hybrid state architecture to achieve data protection by default while preserving the guarantees of a decentralized ledger.

## Three-Part Contract Structure

Every Midnight application consists of three distinct components that work together.

### Replicated Component

The replicated component runs on every validator node and operates on public state. It handles deterministic logic that must be visible to all network participants. Public ledger updates, token transfers involving unshielded balances, and contract initialization all happen within the replicated component. This component executes in the standard blockchain execution environment and produces state transitions that validators can independently verify.

### Zero-Knowledge Circuit

The ZK circuit encodes the private computation rules of the application. It defines what witnesses (private inputs) the prover must supply and what constraints the computation must satisfy. The circuit itself is public and is stored on chain. Anyone can inspect it to understand what rules govern the private computation. The circuit produces a proof that attests to correct execution without revealing the private inputs.

### Local Component

The local component runs exclusively on the user's machine. It manages witness generation, interfaces with private state providers, and orchestrates proof creation. This component never executes on chain. It holds the user's private data, constructs the witness values needed by the circuit, and submits proofs for verification. The local component is the bridge between the user's private world and the public blockchain.

## Kachina Protocol

Kachina is the underlying protocol that separates application logic into the three-component model described above. It defines how the replicated component, ZK circuit, and local component communicate through standardized interfaces. Kachina ensures that the public execution environment never sees private data while still being able to verify that private computations follow the rules.

The protocol defines a strict boundary between what runs on chain and what runs off chain. State transitions that touch public state happen in the replicated component. State transitions that involve private data produce ZK proofs in the local component and submit only the proof (not the data) to the chain.

## Hybrid UTXO and Account Model

Midnight uses a hybrid state model that combines features of both the UTXO model and the account model.

### UTXO Layer

The UTXO layer manages shielded transactions. Each shielded coin is represented as a commitment on chain with a corresponding nullifier that marks it as spent. When a user sends a shielded transaction, they consume existing coin commitments by revealing nullifiers, and they create new coin commitments for the recipient. The amounts, sender, and recipient remain hidden.

### Account Layer

The account layer manages public state through traditional account-based storage. Contracts have persistent storage slots that the replicated component can read and write. This layer handles unshielded token balances, contract code, and any application state that does not require privacy.

### Interaction Between Layers

Users can move value between the shielded UTXO pool and the unshielded account layer. Moving from unshielded to shielded (a shielding operation) creates a new coin commitment. Moving from shielded to unshielded (an unshielding operation) reveals the amount publicly while preserving the sender's privacy through the nullifier mechanism.

## Impact VM

The Impact VM is Midnight's execution environment for the replicated component. It is a deterministic virtual machine that processes public state transitions in every block.

### Execution Model

The Impact VM follows a simple execution loop. For each block, it processes a sequence of transactions in order. Each transaction specifies a contract to call and the public inputs to provide. The VM loads the contract's replicated component code, executes it against the current public state, and produces new public state as output.

### Proof Verification

When a transaction includes a ZK proof (from a private computation), the Impact VM verifies the proof before allowing any public state changes that depend on it. This ensures that private computations satisfy the circuit constraints before they can affect public state.

### Gas and Fees

The Impact VM meters computation through a gas model. Each operation consumes a predetermined amount of gas. Proof verification is a significant cost factor. Users pay fees in the network's native currency, and these fees compensate validators for the computational work of executing transactions and verifying proofs.

## Network Layers

Midnight's network architecture divides responsibilities across five layers.

### Consensus Layer

The consensus layer runs the proof-of-stake protocol that determines which validator produces the next block. Validators stake the native token, and the protocol selects block producers based on stake weight. The consensus layer produces finalized blocks that contain ordered sets of transactions.

### Peer-to-Peer Layer

The P2P layer handles node discovery, connection management, and message propagation. Nodes find each other through a distributed hash table and maintain persistent connections to a set of peers. Transactions, blocks, and proofs propagate across the network through this layer.

### Storage Layer

The storage layer maintains the blockchain state. Public state lives in a key-value store indexed by contract address and storage key. The UTXO set lives in a separate commitment tree that supports efficient membership proofs. Historical blocks and their associated proofs are archived for full nodes.

### RPC Layer

The RPC layer exposes APIs for clients to interact with the network. Clients submit transactions through this layer, query public state, and request proof generation status. The RPC layer also serves as the entry point for indexer queries that provide structured access to on-chain data.

### Transaction Layer

The transaction layer handles transaction validation, ordering within blocks, and the mempool that holds pending transactions before inclusion. Transactions are cryptographically signed and include the necessary public inputs, proofs (if applicable), and fee information.

## Privacy by Default

A core design principle of Midnight is that privacy is the default, not an opt-in feature. The architecture enforces this in several ways.

All user balances in the shielded pool are private by construction. Contract state is public by default (consistent with blockchain transparency requirements), but the architecture encourages developers to keep sensitive data off chain and submit only proofs. The three-part contract model makes it natural to separate public verification from private data.

The Zswap protocol handles shielded transactions automatically. Developers building token contracts do not need to implement their own privacy mechanisms. The network provides privacy at the protocol level rather than requiring each application to build it from scratch.

## Validator and Prover Separation

Midnight separates the roles of validators and provers. Validators run the consensus protocol, execute the replicated component, verify proofs, and maintain the blockchain state. Provers (the local component) run on user machines, generate witnesses, and create proofs.

This separation is important for scalability. Proof generation is computationally intensive but can be done in parallel by many users. Proof verification is relatively fast and can be handled by validators as part of block processing. Users with more powerful hardware can generate proofs faster, but all validators can verify those proofs with the same efficiency.

## Network Configuration

Midnight supports multiple deployment environments. The local development environment runs a full stack (consensus, P2P, storage, RPC) in Docker containers for testing. The pre-production network provides a staging environment for integration testing before mainnet deployment. The mainnet is the production network with real economic value at stake.

Each environment has its own chain ID, genesis block, and network parameters. Applications should parameterize their network configuration so they can switch between environments without code changes.

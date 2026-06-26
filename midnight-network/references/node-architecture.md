# Midnight Node Architecture

## Overview

The Midnight node is built on a Substrate based blockchain framework. It provides the foundational layer for privacy preserving smart contracts via zero knowledge proofs. The architecture is modular with clearly separated concerns across runtime, consensus, networking, storage, and RPC layers.

## Runtime Layer

The runtime contains the onchain business logic implemented as Substrate pallets. Each pallet handles a discrete domain of functionality.

### Core Pallets

The contract execution pallet manages Compact smart contract deployment, state transitions, and witness verification. It coordinates with the ZK proof system to validate shielded computations without revealing private inputs.

The token pallet governs the native NIGHT token including transfers, balances, and fee accounting. It supports both shielded and unshielded token operations through separate sub pallets.

The governance pallet enables onchain decision making through proposal submission, voting, and enactment of protocol upgrades. Token holders participate directly or delegate their voting power.

The identity pallet manages SPO identities, validator registration, and reputation tracking. It links onchain activity to known block producer identities.

The zswap pallet handles the privacy preserving asset swap protocol. It coordinates multi party shielded transactions and maintains the zswap ledger state.

### State Management

Runtime state is stored in a Merkle Patricia trie. This provides efficient state proofs and enables light client verification. The state is divided between public ledger state visible to all nodes and private state accessible only with proper authorization.

Public state includes account balances, contract metadata, governance proposals, and validator information. Private state encompasses shielded balances, contract witnesses, and zswap participant data.

## Consensus Engine

### Proof of Stake Protocol

Midnight uses a proof of stake consensus mechanism. Stake Pool Operators stake tokens to participate in block production. The protocol selects block producers through a verifiable random function based process.

### Committee Selection

A subset of active validators forms a committee for each epoch. Committee members are selected proportionally to their stake. The selection algorithm uses a deterministic randomness beacon derived from previous epoch VRF outputs.

### Epochs

Time is divided into epochs of a fixed number of slots. Each slot has a designated block producer from the current committee. Epoch transitions trigger validator set rotation, rewards distribution, and protocol parameter updates.

### The D Parameter

The D parameter controls the decentralization rate by limiting how many blocks a single validator can produce within a window. A lower D value enforces stricter distribution of block production opportunities. The parameter adjusts dynamically based on network conditions and governance decisions.

### Finality

The consensus provides probabilistic finality. Blocks gain confidence as subsequent blocks are built on top. A Byzantine fault tolerant finality gadget may be added in future iterations to provide deterministic finality guarantees.

## P2P Networking

Nodes communicate over a gossip based peer to peer network. The networking layer uses libp2p for transport abstraction across TCP, WebSocket, and QUIC protocols. Nodes maintain a distributed hash table for peer discovery and use Kademlia routing.

Transaction propagation follows a flood and prune model. Blocks propagate via a compact block relay mechanism that minimizes redundant data transfer. Private witness data is encrypted and sent only to designated committee members.

## Storage Layer

### Database Backend

The node uses RocksDB as the primary key value store. It maintains separate column families for state trie nodes, block bodies, transaction indices, and chain metadata.

### State Pruning

Nodes can configure pruning modes to control disk usage. Archive mode retains all historical state. Pruned mode keeps only recent state and discards historical trie nodes. Light mode stores only headers and minimal state needed for verification.

## RPC Interface

The node exposes a JSON RPC interface over HTTP and WebSocket transports. Standard methods include submitting transactions, querying blocks, accessing chain state, and subscribing to events. A rate limiter protects against resource exhaustion. Authentication tokens can gate access to administrative endpoints.

## Node Types

### Full Node

A full node validates all blocks, maintains recent state, and participates in transaction propagation. It does not produce blocks but serves as the backbone of the network by relaying data and serving RPC requests.

### Archive Node

An archive node retains the complete historical state trie and all block bodies. This node type enables deep historical queries, data analytics, and indexing services. Archive nodes require significant disk capacity.

### RPC Node

An RPC node is optimized for serving client requests. It typically runs with a larger transaction pool, higher connection limits, and configured rate limiting. RPC nodes may disable certain peer to peer functions to focus resources on query throughput.

### Boot Node

A boot node provides initial peer discovery. It does not validate blocks or store state. Its sole purpose is to answer peer routing requests so new nodes can find active peers and join the network.

### Validator Node

A validator node participates in block production and committee operations. It runs with enhanced security measures including hardware backed key storage and restricted RPC access. Validator nodes require careful monitoring and redundancy planning.

## Component Interactions

The runtime communicates with consensus through the block authoring interface. The networking layer feeds transactions to the transaction pool. The RPC interface reads from storage and submits extrinsics to the transaction pool. All components share access to the key value database through the storage abstraction layer.

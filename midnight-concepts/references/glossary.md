# Midnight Network Glossary

## Core Concepts

### Midnight Network
A zero-knowledge partner chain to Cardano that enables privacy-preserving blockchain applications through advanced cryptography.

### Partner Chain
A blockchain that connects to and inherits security from a main chain (Cardano) while providing specialized capabilities.

### Zero-Knowledge Proof (ZK Proof)
A cryptographic method that proves a statement is true without revealing any information beyond the statement's validity.

### Selective Disclosure
The ability to choose exactly what information to reveal and what to keep private in a blockchain application.

## Privacy Technologies

### Zswap
Midnight's privacy-preserving token protocol that hides transaction amounts, sender/receiver identities, and token types.

### Shielded Transaction
A transaction where amounts, parties, and token types are hidden using zero-knowledge proofs.

### Unshielded Transaction
A transaction where amounts and parties are publicly visible on the blockchain.

### Coin Commitment
A cryptographic commitment that hides a coin's value, type, and owner while proving its validity.

### Nullifier
A unique identifier generated when spending a coin that prevents double-spending without revealing which coin was spent.

### State Channel
An off-chain mechanism allowing parties to conduct many transactions privately, settling only the final state on-chain.

### Hydra
Cardano's state channel protocol, integrated with Midnight for high-throughput private transactions.

## Cryptographic Primitives

### Circuit
A representation of a computation as arithmetic operations, used for generating zero-knowledge proofs.

### Witness
Private input data to a zero-knowledge proof that is not revealed to verifiers.

### Proof
Cryptographic evidence that a computation was performed correctly without revealing the computation's inputs.

### Commitment
A cryptographic binding to a value that hides the value but can later be revealed and verified.

### Hash Function
A one-way function that produces a fixed-size output from arbitrary input, used extensively in cryptography.

### Elliptic Curve
A mathematical structure used for efficient cryptographic operations in Midnight.

### Merkle Tree
A tree structure where each leaf is a hash of data and each node is a hash of its children, enabling efficient proofs of inclusion.

## Blockchain Components

### Validator
A network participant that validates transactions, produces blocks, and participates in consensus.

### Node
Software that participates in the Midnight network, validating transactions and maintaining blockchain state.

### Indexer
A database service that indexes blockchain data and provides efficient query interfaces for applications.

### Proof Server
A specialized service that generates zero-knowledge proofs, often with optimized hardware.

### Block
A collection of transactions and state updates, produced by validators and added to the blockchain.

### Transaction
An atomic operation that modifies blockchain state, such as transferring tokens or calling a contract.

### Gas
A measure of computational resources required to execute a transaction, used for fee calculation.

## Smart Contracts

### Compact
Midnight's purpose-built programming language for writing privacy-preserving smart contracts.

### Contract
A program deployed on the blockchain that executes according to predefined rules.

### Circuit Context
The execution environment for a zero-knowledge circuit, including public inputs and outputs.

### Witness Context
The private inputs to a circuit that are not revealed in the zero-knowledge proof.

### Contract State
The on-chain data storage for a smart contract.

### State Value
A piece of data stored in a contract's on-chain state.

## Token System

### Token Type
An identifier for a specific type of token (e.g., native token, custom tokens).

### Native Token (Night)
Midnight's native cryptocurrency used for transaction fees and staking.

### Dust Token
A special token type used specifically for paying transaction fees.

### Coin
A unit of value in the Zswap system, represented as a cryptographic commitment.

### Qualified Coin Info
Information about a coin including its position in the Merkle tree, used for spending.

### Coin Info
Basic information about a coin: token type, value, and nonce.

## Transaction Structure

### Offer
A component of a Zswap transaction consisting of inputs, outputs, and transients.

### Input
A coin being spent (burned) in a transaction.

### Output
A new coin being created in a transaction.

### Transient
A coin that is created and spent within the same transaction.

### Guaranteed Phase
The part of a transaction that always executes (fee payments, fast operations).

### Fallible Phase
The part of a transaction that may fail atomically (contract calls, complex operations).

## Network Operations

### Consensus
The mechanism by which network participants agree on the blockchain's state.

### Ouroboros
The proof-of-stake consensus protocol used by Cardano and Midnight.

### Staking
Locking tokens to participate in consensus and earn rewards.

### Slashing
Penalty for validator misbehavior, resulting in loss of staked tokens.

### Finality
The point at which a transaction is considered irreversible.

### Fork
A divergence in the blockchain where different validators produce conflicting blocks.

## Development Tools

### Midnight.js
The official TypeScript SDK for building Midnight applications.

### Wallet SDK
SDK for building custom wallets and managing keys, transactions, and state.

### DApp Connector API
Interface for connecting decentralized applications to Midnight wallets.

### Compact Runtime API
Runtime primitives for executing Compact contracts and generating proofs.

### Ledger API
Interface for interacting with the Midnight ledger (transactions, tokens).

## API Components

### Circuit Results
The output of executing a zero-knowledge circuit.

### Query Context
An interface for querying contract state and running on-chain VM programs.

### Compact Type
Runtime representation of Compact programming language data types.

### Network ID
Identifier for different Midnight networks (mainnet, testnet, etc.).

### Proof Stage
The state of a transaction component: unproven, proven, or proof-erased.

## Wallet Concepts

### Shielded Address
An address for receiving shielded (private) tokens.

### Unshielded Address
An address for receiving unshielded (public) tokens.

### Dust Address
An address for receiving dust tokens (for fees).

### Private Key
Secret cryptographic key used to authorize transactions.

### Public Key
Public cryptographic key derived from private key, used to receive funds.

### Seed Phrase
A human-readable representation of a private key, used for wallet recovery.

## Security Concepts

### Double-Spend
An attack where the same coin is spent multiple times (prevented by nullifiers).

### Front-Running
Observing pending transactions and submitting competing transactions first.

### MEV (Miner Extractable Value)
Value that can be extracted by reordering, including, or excluding transactions.

### Sybil Attack
Creating many fake identities to gain disproportionate influence.

### 51% Attack
Controlling majority of network stake/power to manipulate the blockchain.

## Compliance & Regulation

### KYC (Know Your Customer)
Identity verification process required by regulations.

### AML (Anti-Money Laundering)
Regulations to prevent money laundering and terrorist financing.

### Audit Trail
A record of transactions and operations that can be reviewed for compliance.

### Regulatory Compliance
Adhering to legal requirements while maintaining privacy.

## Performance Metrics

### Throughput
Number of transactions processed per unit of time.

### Latency
Time delay between transaction submission and confirmation.

### Proving Time
Time required to generate a zero-knowledge proof.

### Verification Time
Time required to verify a zero-knowledge proof.

### Block Time
Average time between block production.

## Development Concepts

### Testnet
A test network for development and testing without real value.

### Mainnet
The production network with real value and live operations.

### Faucet
A service that provides free test tokens for development.

### Deployment
Publishing a smart contract to the blockchain.

### Migration
Updating a deployed contract or moving to a new version.

## IOG & Cardano

### IOG (Input Output Global)
The research and development company behind Cardano and Midnight.

### Cardano
The main blockchain to which Midnight is a partner chain.

### ADA
Cardano's native cryptocurrency.

### Formal Verification
Mathematical proof that code behaves correctly according to specifications.

### Peer Review
Academic review process applied to Midnight's research and protocols.

## Advanced Concepts

### Polynomial Commitment
A cryptographic commitment to a polynomial, used in zero-knowledge proof systems.

### Fiat-Shamir Heuristic
A technique for making interactive proofs non-interactive.

### Trusted Setup
A one-time cryptographic ceremony required by some ZK proof systems (Midnight minimizes this).

### Circuit Optimization
Techniques to reduce the size and complexity of zero-knowledge circuits.

### Proof Composition
Combining multiple proofs into a single proof for efficiency.

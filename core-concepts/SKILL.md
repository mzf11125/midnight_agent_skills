---
name: core-concepts
description: Foundational knowledge about Midnight Network concepts including architecture, Kachina Protocol, zero-knowledge proofs, Zswap protocol, selective disclosure, DUST tokenomics, partner chain design, ledger models, Impact VM, privacy mechanisms, network architecture, contract structure, and Web3 integration. Use when users need to understand how Midnight works at a fundamental level, how privacy is achieved, how assets flow, how consensus operates, and how all components fit together. Core reference for any Midnight development task.
---

# Core Concepts

Complete reference for Midnight Network foundational concepts, privacy technology, and architectural design.

## What is Midnight

Midnight is a zero-knowledge partner chain to Cardano that enables privacy-preserving blockchain applications. It solves the fundamental tension between transparency and privacy in blockchain technology through advanced zero-knowledge cryptography.

**Key Innovation**: Selective disclosure. Applications can choose exactly what information to make public and what to keep private while maintaining cryptographic verifiability.

**Core Features**:
- Privacy-preserving smart contracts via Compact language
- Selective disclosure of contract state
- Hybrid UTXO and Account model
- Zswap for private token transfers
- Integration with Cardano security
- DUST dual-token economics
- Proof server delegation for light clients

**Why Midnight Exists**:
- Traditional blockchains make all data public by default
- Many real-world applications require confidentiality
- Existing privacy solutions add complexity to public chains
- Midnight provides native privacy without sacrificing verifiability

## The Kachina Protocol

Kachina is Midnight's foundational smart contract protocol that enables data-protecting smart contracts. It is not just a feature. It is the architecture that makes privacy-preserving smart contracts possible.

### The Two-State Model

Kachina bridges the gap between public blockchain state and private local state using zero-knowledge proofs.

**Public State (On-Chain)**:
- Located on the Midnight blockchain
- Visible to all network participants
- Contains transaction proofs and contract code
- Examples include vote counts, public token balances, contract addresses
- Stored in the replicated ledger component

**Private State (Local)**:
- Located on the user's device
- Only visible to the user who owns it
- Contains personal data and secrets
- Examples include individual votes, private keys, medical records
- Stored in the local component of contracts
- Never broadcast to the network

### The Zero-Knowledge Proof Bridge

The magic of Kachina happens through ZK-SNARKs:
1. User proves locally using private inputs plus public state
2. ZK proof is generated that asserts valid state transition
3. Proof is submitted to the blockchain
4. Blockchain verifies the proof without seeing private inputs
5. If valid public state is updated
6. User updates private state locally

### Transcript-Based Concurrency

**What Are Transcripts**:
- Ordered sequences of contract interactions
- Similar to transaction receipts on Ethereum
- Record the public trace of all contract calls
- Enable concurrent access to contracts

**How Transcripts Work**:
- Each contract call creates a transcript entry
- Transcripts record the public inputs and outputs
- Private data is never recorded in transcripts
- Transcripts enable deterministic state transitions
- Multiple users can interact with the same contract simultaneously

**Concurrency Properties**:
- Public state transitions are atomic and ordered
- Private state updates are local and independent
- ZK proofs ensure private transitions are valid without revealing them
- No global lock required for contract state

### Universally Composable (UC) Security

**What UC Security Means**:
- Security guarantees hold even when contracts interact
- Composition does not weaken individual contract security
- Contracts remain secure in any execution environment
- Formal cryptographic proof of security properties

**Why UC Security Matters**:
- Contracts can safely call other contracts
- Composability enables complex DeFi applications
- Security properties are mathematically proven
- Enterprise-grade security guarantees
- No unexpected interactions between contracts

## Zero-Knowledge Proofs

### What Are Zero-Knowledge Proofs

Zero-knowledge proofs (ZKPs) are cryptographic methods that allow one party (the prover) to prove to another party (the verifier) that a statement is true without revealing any information beyond the validity of the statement itself.

### Three Essential Properties

**Completeness**:
If the statement is true an honest prover can convince an honest verifier. The proof always verifies when generated correctly.

**Soundness**:
If the statement is false no cheating prover can convince the verifier except with negligible probability. This is the security guarantee.

**Zero-Knowledge**:
The verifier learns nothing beyond the truth of the statement. No information about private data is ever revealed.

### How ZKPs Work on Midnight

**Circuit Representation**:
- Computations are represented as arithmetic circuits
- Each circuit defines what valid state transitions look like
- The Compact language compiles to these circuits automatically
- Circuits are finite structures determined at compile time

**Proof Generation**:
- Prover takes public inputs and private witnesses
- Generates a cryptographic proof using zkSNARKs
- Proof is constant size regardless of circuit complexity
- Proving can be delegated to proof servers or done locally
- Proof generation is computationally intensive

**Proof Verification**:
- Verifier takes public inputs and the proof
- Verification is fast and constant time
- Much faster than re-executing the computation
- Verification happens on-chain by all nodes
- No private data is needed for verification

### zkSNARKs in Midnight

**What zkSNARKs Provide**:
- Zero-Knowledge: the proof reveals nothing about private inputs
- Succinct: proof size is small and constant
- Non-interactive: no back-and-forth communication needed
- Argument of Knowledge: proves the prover knows valid inputs

**Elliptic Curve Foundation**:
- Built on pairing-friendly elliptic curves
- Enables efficient cryptographic operations
- Mathematical hardness assumptions provide security

**Practical Example: Private Voting**:

Without ZKPs on a traditional blockchain:
- All votes are publicly visible
- Anyone can see who voted for what
- Privacy is impossible

With ZKPs on Midnight:
- Each voter proves they have the right to vote without revealing identity
- Each voter proves they voted for a valid candidate without revealing the choice
- The final tally is publicly verifiable
- Individual votes remain secret forever

## Zswap Protocol

### What is Zswap

Zswap is Midnight's privacy-preserving token system that hides transaction amounts sender identities receiver identities and the token types being transferred. It provides cryptographic guarantees that transactions are valid without revealing sensitive financial data.

### How Zswap Works

**Traditional Blockchain Transaction**:
```
Alice sends 100 tokens to Bob
[Publicly visible: sender=Alice, receiver=Bob, amount=100]
```

**Zswap Transaction**:
```
Someone sent some amount of some token to someone
[Publicly visible: cryptographic commitments proving validity]
[Private: actual sender, receiver, amount, token type]
```

### Shielded Tokens

**Full Privacy**:
- Amounts are hidden using cryptographic commitments
- Sender and receiver identities are concealed
- Token type is obscured
- ZK proofs validate all operations
- Maximum privacy for sensitive transactions

**How Shielding Works**:
1. Tokens are represented as coin commitments
2. Each commitment hides value type and owner
3. Commitments are stored in a Merkle tree on-chain
4. Only the owner can spend a commitment
5. Spending reveals nothing about the commitment

### Unshielded Tokens

**Public Visibility**:
- Amounts and owners are visible on-chain
- Faster operations because no ZK proofs are needed
- Useful for public operations and transparency
- NIGHT tokens can exist in unshielded form
- Compatible with traditional blockchain patterns

### Coin Commitments

**What Commitments Are**:
- Cryptographic representations of tokens
- Hide the coin's value and owner
- Bind to specific values without revealing them
- Can be proven valid without opening the commitment
- Stored in a Merkle tree for efficient verification

**Commitment Properties**:
- Hiding: the commitment reveals nothing about the value
- Binding: the commitment cannot be changed to a different value
- The owner can prove knowledge of the opening
- Double-spending is prevented via nullifiers

### Nullifiers

**What Nullifiers Are**:
- Unique identifiers generated when spending a coin
- Prevent double-spending without revealing which coin was spent
- Each coin has exactly one nullifier
- Nullifiers are stored on-chain permanently

**How Nullifiers Work**:
1. When spending a coin the owner generates its nullifier
2. The nullifier is submitted with the transaction
3. The network checks the nullifier has not been used before
4. If the nullifier is new the spend is valid
5. The nullifier does not reveal which coin it corresponds to

### Zswap Transaction Structure

**Guaranteed Phase** (always executes):
- Fee payments in DUST
- Fast verification operations
- Must succeed or entire transaction is invalid
- Contains proof verification

**Fallible Phase** (may fail):
- Contract calls
- Operations that might logically fail
- Fails atomically within this phase
- Does not affect the guaranteed phase

### Multi-Party Zswap Transactions

**Joint Transactions**:
- Multiple participants contribute inputs and outputs
- Each participant's privacy is maintained
- Combined ZK proof validates all contributions
- Useful for DEX trades and complex transfers
- No single party learns all the details

## Selective Disclosure

### What is Selective Disclosure

Selective disclosure is Midnight's mechanism that allows applications to control exactly what data is public versus private. It is the core innovation that enables privacy-preserving applications while maintaining verifiability.

### How Selective Disclosure Works

**The Control Spectrum**:
- Applications decide per field what is public
- Some data can be fully private
- Some data can be partially disclosed
- Some data can be fully public
- Disclosure decisions are enforced by the compiler

**The `disclose()` Function**:
In Compact contracts circuit parameters are private by default. To store private data in public ledger state you must explicitly call `disclose()`.

```compact
registry.insert(user.bytes, disclose(profile_hash));
```

This explicit disclosure creates an intentional privacy boundary. Without `disclose()` the compiler rejects the code preventing accidental data leaks.

### Disclosure Patterns

**Full Privacy**:
All data stays private. Only ZK proofs are submitted. Suitable for confidential voting and private identity verification.

**Partial Disclosure**:
Some fields are disclosed while others stay private. For example disclose the result of a computation but keep the inputs private. Suitable for credit scoring and identity verification.

**Full Transparency**:
All data is publicly visible. Suitable for public ledgers and regulatory compliance where transparency is required.

### Privacy Boundaries

**What Privacy Boundaries Mean**:
- Each contract defines its own privacy boundary
- Data within the boundary is never visible externally
- The boundary is enforced by the compiler and runtime
- Crossing the boundary requires explicit disclosure

**Designing Privacy Boundaries**:
- Identify what must be private
- Identify what must be public
- Design the contract to minimize disclosures
- Use opaque types to hide data structures
- Leverage Merkle trees for efficient verification

## DUST Architecture

### Dual-Component Tokenomics

Midnight uses a dual-token model with two distinct but complementary tokens.

**NIGHT Token**:
- The governance and staking token
- Used for securing the network through staking
- Represents ownership and voting power
- Has economic value and is transferable
- Exists in both shielded and unshielded forms

**DUST Token**:
- The transaction fee token
- Used to pay for all on-chain operations
- Generated automatically through a holding mechanism
- Not tradeable or transferable independently
- Prevents spam and enables fee market

### How DUST Generation Works

**The Holding Mechanism**:
1. Users hold NIGHT tokens in their wallet
2. Over time NIGHT holdings generate DUST
3. DUST generation rate is proportional to NIGHT balance
4. DUST is automatically credited to the user's wallet
5. No active claim process is required

**DUST Generation Rate**:
- Based on NIGHT balance and holding duration
- Designed to cover normal transaction usage
- Prevents users from being unable to transact due to fee unavailability
- Dust-free user experience for wallet holders

### Why Dual Tokens

**Separation of Concerns**:
- NIGHT for value and governance
- DUST for operations and fees
- Prevents fee volatility from affecting token value
- Enables predictable transaction costs

**User Experience**:
- Users do not need to acquire DUST separately
- DUST is generated passively from NIGHT holdings
- No separate DUST purchase step required
- Reduces friction for new users

**Network Economics**:
- DUST provides anti-spam mechanism
- Fee market adjusts with network usage
- Validators earn DUST rewards for block production
- Sustainable economic model for long-term operation

## Partner Chain Architecture

### What is a Partner Chain

A partner chain is a separate blockchain that connects to and inherits security from Cardano's main chain. Midnight is not a sidechain in the traditional sense. It maintains its own consensus while anchoring to Cardano for enhanced security.

### Security Inheritance Model

**How Security Inheritance Works**:
- Midnight validators also participate in Cardano
- Cardano's Ouroboros consensus provides security guarantees
- State checkpoints can be anchored to Cardano
- Cross-chain verification is cryptographically enforced
- Economic security is shared across both chains

**Benefits**:
- Leverages Cardano's proven consensus mechanism
- Benefits from Cardano's large validator network
- Inherits economic security from Cardano's market cap
- Reduces bootstrapping requirements for Midnight

### Interoperability With Cardano

**Bridge Architecture**:
- Assets can move between Cardano and Midnight
- NIGHT tokens can bridge to Cardano Native Assets
- ADA can potentially bridge into Midnight
- Cross-chain transactions are cryptographically verifiable
- Uses Cardano's native scripting capabilities

**Shared Validator Set**:
- Validators can operate on both chains
- Shared economic incentives
- Unified security model
- Simplified validator operations

### Sidechain Model Details

**Block Production**:
- Midnight produces its own blocks independently
- Block time and parameters are optimized for ZK proofs
- Finality is achieved through Midnight's consensus
- Cardano anchoring provides additional finality guarantees

**State Commitment**:
- Periodic state commitments to Cardano
- Enables light client verification
- Provides checkpointing for recovery
- Cryptographic proofs of Midnight state on Cardano

## Ledger Models

### Hybrid UTXO and Account Model

Midnight uniquely supports both the UTXO model (Bitcoin-style) and the Account model (Ethereum-style). This is not just flexibility. It is a strategic design choice.

### Account Model (Ethereum-Style)

**Think: Bank Account**:
- Global state is one big database of accounts
- Balances are numbers that change
- Transactions touching the same account must be ordered
- Contract state is mutable

**Use Cases**:
- Smart contract token balances
- Staking contracts
- Governance voting
- Complex DeFi applications

### UTXO Model (Bitcoin-Style)

**Think: Physical Cash**:
- Discrete coins as individual unspent outputs
- Coins are consumed entirely and new ones created
- Independent coins can be spent simultaneously
- Privacy-friendly by design

**Use Cases**:
- Private transactions via Zswap
- High-volume payments
- Cross-chain bridges
- Atomic swaps

### Ledger Tokens vs Contract Tokens

**Ledger Tokens (UTXO-Based)**:
- Native to Midnight's blockchain ledger
- NIGHT tokens are ledger tokens
- Can be shielded or unshielded
- Support parallel processing
- Privacy-friendly architecture

**Contract Tokens (Account-Based)**:
- Exist inside Compact smart contracts
- Similar to ERC-20 tokens
- Managed by contract logic
- Account balances stored in contract state
- Full programmability

### Replicated vs Local State

**Replicated State**:
- Stored on-chain
- Every node has a copy
- Publicly verifiable
- Contains ledger values and Merkle roots
- The public face of the contract

**Local State**:
- Stored off-chain on user devices
- Only the owner has a copy
- Never shared with the network
- Contains private data and secrets
- The private face of the contract

## Impact VM

### What is the Impact VM

The Impact VM is Midnight's purpose-built virtual machine for executing Compact contracts. It is optimized for zero-knowledge proof verification and privacy-preserving computation.

### How the Impact VM Works

**Execution Model**:
- Executes the replicated component of contracts
- Verifies ZK proofs submitted by users
- Manages storage costs and state management
- Enforces contract privacy boundaries
- Integrates with the consensus layer

**Storage Costs**:
- Contracts pay for on-chain state storage
- Storage costs are charged in DUST
- State can be pruned when no longer needed
- Economic incentives for efficient state usage
- Similar to storage rent concepts

### Relation to Compact

**Compilation Target**:
- Compact contracts compile to Impact VM bytecode
- The VM understands privacy boundaries
- ZK circuit verification is built into the VM
- Efficient execution of Compact operations

**Runtime Features**:
- Contract-to-contract calls
- Event emission
- Balance management
- State read and write operations
- Authentication and authorization checks

## Privacy Mechanisms

### Communication Commitments

**What They Are**:
- Cryptographic commitments to communication between parties
- Enable private message passing
- Messages are encrypted and committed
- Only intended recipients can decrypt

**Usage**:
- Private notifications between users
- Off-chain coordination for contract interactions
- Secure parameter sharing for multi-party operations

### Encryption

**At-Rest Encryption**:
- Private state stored locally is encrypted
- Only the wallet can decrypt private state
- Protects data if device is compromised

**In-Transit Encryption**:
- All network communication is encrypted
- Transaction submission is private
- Proofs are transmitted securely

### Viewing Keys

**Purpose**:
- Grant selective access to private state
- Allow auditors or regulators to view specific data
- Enable compliance without sacrificing privacy for everyone
- Revocable access control mechanism

**How They Work**:
- Each user has a viewing key pair
- The public viewing key enables others to encrypt data
- The private viewing key enables decryption
- Sharing the private viewing key grants read access

### Private State Providers

**What They Are**:
- Services that maintain private state on behalf of users
- Enable light clients that cannot store full private state
- State is encrypted so the provider cannot read it
- Provider can serve state without knowing contents

**Architecture**:
- User encrypts private state before storing
- Provider stores encrypted blobs
- On contract interaction user fetches encrypted state
- User decrypts locally and generates proof
- Provider never learns the data

## Network Architecture

### Consensus Layer

**Ouroboros-Based Consensus**:
- Proof-of-stake consensus protocol
- Energy efficient with formal security proofs
- Decentralized validator selection
- Slot-based block production
- Finality guarantees through chain density

**Validator Participation**:
- Validators stake NIGHT tokens
- Selected to produce blocks based on stake
- Earn block rewards and transaction fees
- Economic security through slashing conditions
- Can operate on both Cardano and Midnight

### Cryptographic Primitives

**Hash Functions**:
- Poseidon hash for ZK-friendly operations
- Standard cryptographic hashes for non-ZK operations
- Efficient in-circuit hashing

**Elliptic Curves**:
- Pairing-friendly curves for zkSNARKs
- Standard curves for signatures
- Curve operations exposed in Compact standard library

**Commitment Schemes**:
- Pedersen commitments for value hiding
- Merkle trees for efficient membership proofs
- Nullifier derivation for double-spend prevention

### P2P Networking

**Node Discovery**:
- Distributed hash table for peer discovery
- Gossip protocol for block and transaction propagation
- Validator-specific channels for block production

**Transaction Propagation**:
- Transactions broadcast to the network
- Mempool management for pending transactions
- Priority based on DUST fees

### RPC Interface

**Available Endpoints**:
- Transaction submission
- Block queries
- Contract state queries
- Transaction status
- Network information

**Access Patterns**:
- Indexer for historical queries
- Direct RPC for real-time interaction
- Subscription endpoints for events

### Storage Layer

**Blockchain Storage**:
- Full history of all blocks
- Transaction data with proofs
- Contract state snapshots
- Merkle proofs for state verification

**State Storage**:
- Current contract state (Merkle trees)
- UTXO set for unspent outputs
- Nullifier set for spent coins
- Account balances and metadata

### Transaction Lifecycle

**Transaction Creation**:
1. User constructs transaction with inputs and outputs
2. Private witnesses are provided for ZK proof generation
3. ZK proof is generated locally or via proof server
4. Transaction is signed by the user's wallet

**Transaction Submission**:
1. Signed transaction is submitted to a node
2. Node validates the transaction structure
3. DUST fees are deducted
4. Transaction enters the mempool

**Transaction Execution**:
1. Block producer includes the transaction
2. Guaranteed phase executes (proof verification fees)
3. Fallible phase executes (contract calls)
4. Public state is updated
5. User updates private state locally

## Contract Structure

### Three-Part Architecture

Every Compact contract consists of three distinct components.

**1. Replicated Component (Public Ledger)**:
- Stored on-chain and replicated across all nodes
- Contains public state declarations
- Verifiable by anyone at any time
- Written in Compact and compiled to Impact VM bytecode
- Defines what is visible to the world

**2. Zero-Knowledge Circuit**:
- Represents the computation that must be proven
- Defines constraints on valid state transitions
- Keeps private inputs hidden inside the circuit
- Compiled from Compact circuit functions
- Generates cryptographic proofs of correct execution

**3. Local Component (Off-Chain)**:
- Runs in the DApp on the user's device
- Handles arbitrary computation without constraints
- Witness functions for private input validation
- Manages local private state
- Cannot directly modify on-chain state

### How Components Interact

**Circuit to Ledger**:
- Circuit reads public state from the replicated component
- Circuit generates proof of valid transition
- Proof is verified against the replicated component
- Public state is updated when proof is valid

**Circuit to Local**:
- Circuit receives private inputs from local component
- Local component provides witness data
- Circuit constrains what private inputs are valid
- Local component updates private state after proof

**Local to Replicated (Indirect)**:
- Local component never writes directly to replicated state
- All changes go through circuit proofs
- This ensures public state integrity
- Privacy is enforced by this indirection

## Account Model Reference

### Address Types

**Public Key Addresses**:
- Derived from Ed25519 public keys
- Standard address format for receiving tokens
- Compatible with hardware wallets
- Human-readable Bech32 encoding

**Contract Addresses**:
- Derived from the contract's verifier key
- Deterministic based on contract code
- Used to reference contracts on-chain
- Enable contract-to-contract calls

**Zswap Coin Public Keys**:
- Used in shielded token transfers
- Represent shielded coin ownership
- Derived from user's spending key
- Enable private token reception

### Balance Management

**Unshielded Balances**:
- Visible on-chain
- Accounted in ledger UTXOs
- Transferrable without ZK proofs
- Compatible with standard wallet operations

**Shielded Balances**:
- Hidden from public view
- Represented as coin commitments
- Transferable only through Zswap
- Require ZK proofs to spend

### Transaction Signing

**Signature Schemes**:
- Ed25519 for standard transactions
- Schnorr signatures for ZK-friendly operations
- Multi-signature support for shared accounts

**Signing Flow**:
1. Construct the transaction
2. Generate ZK proof if applicable
3. Sign the transaction with private key
4. Submit signed transaction to network

## Web3 Model Reference

### DApp Architecture

**Provider Model**:
- DApps connect to Midnight through providers
- Providers abstract network communication
- Similar to Ethereum's provider pattern
- Window.midnight object in browser contexts

**Connection Flow**:
1. DApp detects Midnight provider
2. User authorizes connection
3. DApp receives network and account information
4. DApp can read public state and submit transactions

### DApp Connector API

**Wallet Integration**:
- Connect and disconnect wallet
- Request account access
- Sign transactions
- Manage network selection
- Handle proof generation

**Contract Interaction**:
- Deploy contracts through the connector
- Call contract circuits
- Read contract state
- Subscribe to contract events
- Handle transaction lifecycle

### Indexer Access

**GraphQL API**:
- Query historical data
- Subscribe to real-time updates
- Monitor contract state changes
- Track transaction status
- Build efficient UIs without RPC polling

### Development Workflow

**Local Development**:
- Local devnet via Docker
- Pre-configured test accounts
- DUST pre-generation for testing
- Fast iteration without network latency

**Testnet (Preprod)**:
- Shared test environment
- Real network conditions
- Community testing
- Pre-mainnet validation

**Mainnet**:
- Production deployment
- Real economic value
- Full security guarantees
- Governance participation

## Network States and Environments

### Undeployed (Local)

**Purpose**:
- Contract development and testing
- No network interaction required
- Fastest iteration cycle
- Full control over test accounts

**Setup**:
- Docker Compose for local devnet
- Pre-built Docker images
- Development configuration files
- Automated setup scripts

### Preview (Testnet)

**Purpose**:
- Community testing
- Pre-release validation
- Integration testing
- Feedback collection

**Characteristics**:
- Shared network with other developers
- Realistic network conditions
- Regular resets possible
- No economic value

### Preprod (Staging)

**Purpose**:
- Production-like testing
- Final validation before mainnet
- Performance testing
- Security auditing

**Characteristics**:
- Stable shared network
- Production configuration
- Persistent state
- Limited economic value

### Mainnet (Production)

**Purpose**:
- Live production deployment
- Real economic transactions
- Full security guarantees
- Governance and staking

**Characteristics**:
- Immutable ledger
- Real NIGHT and DUST
- Validator consensus
- No resets or rollbacks

## Glossary of Key Terms

**Compact**: Midnight's smart contract language that compiles to ZK circuits.

**Commitment**: A cryptographic value that hides data while binding to it. Cannot be changed after creation.

**DApp Connector**: Browser extension API for Midnight DApps to interact with wallets.

**Disclosure**: The act of making private data public. Must be explicit in Compact.

**DUST**: The transaction fee token generated from holding NIGHT.

**Impact VM**: Midnight's virtual machine for executing Compact contracts.

**Indexer**: A service that indexes blockchain data for efficient querying.

**Kachina Protocol**: Midnight's foundational privacy-preserving smart contract protocol.

**Ledger**: The on-chain replicated state visible to all participants.

**Nullifier**: A unique value preventing double-spending of shielded coins.

**Proof Server**: A service that generates ZK proofs on behalf of light clients.

**Replicated Component**: The on-chain portion of a Compact contract.

**Selective Disclosure**: The ability to choose exactly what data is public.

**Shielded Token**: A token whose transactions are private via ZK proofs.

**Transcript**: An ordered record of contract interactions on-chain.

**Unshielded Token**: A token whose transactions are publicly visible.

**Viewing Key**: A cryptographic key that grants read access to private state.

**Witness**: Private input data provided to a ZK circuit.

**ZK Circuit**: A representation of computation that generates zero-knowledge proofs.

**ZK Proof**: A cryptographic proof that a computation was performed correctly without revealing inputs.

**Zswap**: Midnight's privacy-preserving token transfer protocol.

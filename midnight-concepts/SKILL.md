---
name: midnight-concepts
description: Foundational knowledge about Midnight Network zero-knowledge blockchain technology, privacy mechanisms, and architecture. Use when users need to understand zero-knowledge proofs, privacy mechanisms like Zswap and selective disclosure, partner chain architecture, real-world use cases for private DeFi and voting, when to use Midnight for privacy-preserving applications, and core concepts of the Midnight ecosystem.
---

# Midnight Concepts

Comprehensive guide to Midnight Network's foundational concepts, privacy technology, and architecture.

## What is Midnight?

Midnight is a **zero-knowledge partner chain** to Cardano that enables privacy-preserving blockchain applications. It solves the fundamental tension between transparency and privacy in blockchain technology through advanced zero-knowledge cryptography.

**Key Innovation**: Selective disclosure - applications can choose exactly what information to make public and what to keep private, while maintaining verifiability.

**Core Features**:
- Privacy-preserving smart contracts
- Selective disclosure
- UTXO + Account hybrid model
- Zswap for private token transfers
- Integration with Cardano security

## Architecture Overview

### Three-Part Contract Structure

Each Compact smart contract has three components:

1. **Replicated Component** (Public Ledger)
   - Stored on-chain
   - Verifiable by anyone
   - Contains public state

2. **Zero-Knowledge Circuit**
   - Proves correct execution
   - Keeps inputs private
   - Generates proofs

3. **Local Component** (Off-chain)
   - Runs in DApp
   - Arbitrary computation
   - Witness functions

## Core Concepts

### 1. Kachina Protocol

THE foundational smart contract architecture that enables private state management.

**How It Works**:
1. User has private state (witness)
2. Circuit proves valid transition
3. Public state updates on-chain
4. Both states stay consistent

**Key Properties**:
- Public state + Private state model
- Zero-knowledge proof bridge
- Transcript-based concurrency
- Universally Composable (UC) security

**From the whitepaper**: Kachina uses a novel combination of a public ledger and private witnesses, with circuits proving correct state transitions.

### 2. Privacy Mechanisms

#### Zswap Protocol
Privacy-preserving token system hiding:
- Transaction amounts
- Sender/recipient identities
- Token types

**Features**:
- Shielded tokens (hidden)
- Unshielded tokens (public)
- Conversion between both
- Zero-knowledge proofs for validity

```typescript
// Shielded transfer flow
1. Create input from owned shielded coin
2. Create output for recipient
3. Generate ZK proof
4. Submit to network
5. Recipient can receive and spend
```

#### Selective Disclosure
Applications control exactly what data is public vs private:

```compact
// Private comparison
export circuit verifyAge(age: Uint<32>): Boolean {
  const secretAge = witness Age();  // Private
  return disclose(secretAge >= 18);  // Only reveal boolean
}
```

### 3. Ledger Models

Midnight uses a **hybrid UTXO + Account model**:

#### UTXO Model (Ledger Tokens)
- Like Bitcoin
- Each coin spent exactly once
- Good for: privacy, parallelism

#### Account Model (Contract Tokens)
- Like Ethereum
- Mutable stored state
- Good for: complex contracts

**Decision Matrix**:

| Use Case | Recommended Model |
|---------|--------------|
| Simple transfers | UTXO |
| Token balances | Account |
| Complex state | Account |
| High privacy | UTXO |
| High throughput | UTXO |
| Smart contracts | Account |

### 4. Zero-Knowledge Proofs

Mathematical techniques proving computations are correct without revealing inputs.

**Key Concepts**:
- **Circuit**: Compiled from Compact code
- **Witness**: Private inputs
- **Public inputs**: Transparent arguments
- **Proof**: Succinct verification

**Use in Midnight**:
- Valid state transitions
- Transaction validity
- Credential verification

### 5. Partner Chain Architecture

Midnight is a **partner chain** to **Cardano**:

**Benefits**:
- Inherits Cardano security
- EUTxO model
- proven consensus
- Decentralized infrastructure

**Integration**:
- Consensus via Cardano
- State checkpointing
- Token bridging

## Privacy Model

### What Can Be Private

| Data | Privacy Level | Disclosure |
|------|-------------|-----------|
| Account balances | Optional | User choice |
| Transaction amounts | Optional | Hidden in Zswap |
| Identities | Optional | Hidden in Zswap |
| Business logic | Automatic | Circuit keeps secret |
| Credentials | Selective | Only proven facts |

### What Is Always Public

- Transaction existence
- Block order
- State updates (not values)
- Contract code

## Use Cases by Category

### Finance & DeFi

1. **Confidential Trading**
   - Hidden amounts
   - Hidden positions
   - See: [LunarSwap](https://github.com/OpenZeppelin/midnight-apps)

2. **Private Lending**
   - Hidden collateral
   - Hidden debt
   - Credit scoring proof only

3. **Liquid Staking**
   - [Hydra Stake](https://github.com/statera-protocol/hydra-stake-protocol)
   - Privacy-preserving rewards
   - LST functionality

4. **Stablecoins**
   - [Statera Protocol](https://github.com/statera-protocol/statera-protocol-midnight)
   - Over-collateralized
   - Privacy features

### Identity & Privacy

1. **ZK Identity**
   - [Midnames](https://github.com/midnames/core) - ZK DID
   - Selective attribute disclosure

2. **KYC Attestations**
   - [KYC Midnight](https://github.com/joacolinares/kyc-midnight)
   - Prove without revealing data

3. **Private Credentials**
   - [Midnight Cloak](https://github.com/subc0der/midnight-cloak)
   - Age/residence verification

4. **RWA Trading**
   - [Real World Assets](https://github.com/bricktowers/midnight-rwa)
   - Privacy-first tokenization

### Governance

1. **Private Voting**
   - Secret ballots
   - Verifiable counting
   - No vote selling

2. **Crowdfunding**
   - [FundAGoal](https://github.com/codeBigInt/fundagoal)
   - Anonymous contributions

### Gaming

1. **On-chain Gaming**
   - [Midnight Starship](https://github.com/nel349/midnight-starship)
   - ZK leaderboards
   - Privacy-first gaming

2. **Verifiable RNG**
   - [Dice Roll](https://github.com/Kali-Decoder/Midnight-Dice-Roll)
   - Fair randomness

## Tokenomics

### Native Token: NIGHT

- Used for fees
- Staking rewards
- Governance
- **Unit**: 1 NIGHT = 10^6 Stars

### DUST: Dynamic Gas System

DUST is NOT a static balance. It's a **dynamic gas system** where your DUST balance changes based on your NIGHT holdings and time.

**Analogy**:
- **NIGHT** = Solar Panel (valuable asset you hold)
- **DUST** = Electricity (generated from the Solar Panel)
- **Usage** = Consuming electricity to power operations

#### How DUST Works

1. **Registration**: Link your NIGHT address to a DUST public key via the Registration Table
2. **Generation Phase**: DUST grows linearly from creation until it hits a cap (ρ)
3. **Constant Phase**: Stays at maximum value
4. **Decay Phase**: Once NIGHT is spent, DUST decays to zero
5. **Zero Phase**: No more gas available

#### Key Properties

| Property | Description |
|----------|-------------|
| **Shielded** | DUST UTXOs are private |
| **Non-transferable** | Cannot send DUST to others |
| **Dynamic** | Value changes over time |
| **Derived** | Computed from NIGHT UTXO |

#### DUST Units

- **DUST unit**: 1 DUST = 10^15 Specks
- **Initial ratio**: ~5 DUST per NIGHT
- **Grace period**: ~3 hours (for transaction timestamp)

#### Spending Rules

- DUST can be spent multiple times
- New UTXO always created, even with zero value
- Decay continues even during spending
- Partial NIGHT spend creates fresh DUST generation

#### Full Architecture

![DUST Lifecycle](https://github.com/midnightntwrk/midnight-ledger/blob/main/spec/dust.md)

The full technical specification is available in the [DUST spec](https://github.com/midnightntwrk/midnight-ledger/blob/main/spec/dust.md).

### Programmatic DUST Generation (Preprod)

On **Preprod network**, DUST is no longer available from the faucet. DApps must programmatically generate DUST:

1. **Fund wallet**: Get tNIGHT from [Preprod faucet](https://faucet.preprod.midnight.network)
2. **Designate dust address**: Register your unshielded address to a dust address
3. **Generate DUST**: Your tNIGHT holdings automatically generate DUST for gas fees

**Reference**: [midnight-dust-generator](https://github.com/midnightntwrk/midnight-dust-generator) - Official script for Preprod

Prerequisites:
- Node.js v18+
- Docker Desktop (for proof server on port 6300)

```bash
npm install
docker compose -f proof-server.yml up  # terminal 1
npm start  # terminal 2 - interactive walkthrough
```

The script handles: wallet creation/restoration, funding detection, address designation, and registration.

### Dust: Anonymous Tokens (Legacy)

- Privacy coins
- Unlinkable
- Denominations (1, 10, 100, etc.)

## Security Model

### Consensus

- Inherited from Cardano
- Proof of Stake
- BFT-style finality

### Privacy Guarantees

**What Midnight provides**:
- Computational privacy (ZK circuits)
- Transaction unlinkability (Zswap)
- Selective disclosure

**What Midnight does NOT provide**:
- Metadata privacy (timing, size)
- Network-level privacy
- Quantum resistance (future)

## When to Use Midnight

### ✅ Best Fit For

- **Private DeFi** - Confidential trading, lending
- **Identity** - KYC, credentials, age proof
- **Voting** - Private ballots, governance
- **RWA** - Privacy-first asset tokenization
- **Gaming** - Verifiable RNG, ZK leaderboards

### ❌ Not Ideal For

- Fully public applications (use Cardano directly)
- High-throughput needs (consider Hydra)
- Simple transfers (Cardano tx is sufficient)

## Technical Deep Dives

### ZK Circuit Flow

```compact
pragma language_version >= 0.20;

// Public state
export ledger balance: Uint<64>;

// Private witness  
witness secretAmount(): Uint<64>;

// Circuit enforces rules
export circuit deposit(amount: Uint<64>): [] {
  // Verify private input
  const secret = secretAmount();
  
  // Only disclose commitment
  const commitment = disclose(persistentCommit(balance.read(), secret));
  
  // Update public
  balance.write(balance.read() + amount);
}
```

### Zswap Flow

1. **Shield coins** exist locally
2. **Create input** referencing coin
3. **Generate proof** (ownership, sufficient amount)
4. **Create outputs** (recipient + change)
5. **Submit** to network
6. **Recipients** can spend in future

### State Consistency

**Kachina Guarantees**:

1. If circuit proves valid → state updates
2. If circuit fails → no state change
3. Private state stays private
4. Public verification always possible

## Midnight Improvement Proposals (MIPs)

Formal process for proposing changes to Midnight: [midnight-improvement-proposals](https://github.com/midnightntwrk/midnight-improvement-proposals)

### Process

1. **Idea** → 2. **Draft** → 3. **Submit PR** → 4. **Review** → 5. **Accepted** → 6. **Implemented** → 7. **Deployed**

### Categories

| Category | Description |
|----------|-------------|
| **Core** | Protocol, consensus, VM changes |
| **Standards** | Smart contract interfaces, data formats |
| **Networking** | P2P communication |
| **Governance** | Decision-making processes |
| **Informational** | Guidelines, research (no change) |

### Statuses

Proposed → Review → Accepted → Implemented → Superseded/Obsolete/Rejected/Withdrawn

### MIP Template

```yaml
---
MIP: <number>
Title: <title>
Authors: <name> <github>
Status: Proposed
Category: <Core|Standards|Networking|Governance|Informational>
Created: <date>
Requires: <other MIPs>
Replaces: <MIP number>
---
```

Reference: [MIP-1: MIP Process](https://github.com/midnightntwrk/midnight-improvement-proposals)

## Glossary

| Term | Definition |
|------|-----------|
| **Circuit** | ZK program proving computation |
| **Witness** | Private input to circuit |
| **Transcript** | Ordered transaction history |
| **Zswap** | Private token system |
| **Selective Disclosure** | Explicit privacy control |
| **Partner Chain** | Secondary chain to Cardano |
| **Compact** | ZK smart contract language |
| **Shielded** | Privacy-preserving transaction |
| **UTXO** | Unspent Transaction Output |
| **DUST** | Privacy coin denominations |

## Learn More

### Official Resources

- [Midnight Docs](https://docs.midnight.network/)
- [Kachina Paper](https://docs.midnight.network/learn/understanding-midnights-technology/kachina)
- [Developer Academy](https://academy.midnight.network/)
- [Community Forum](https://forum.midnight.network)

### Awesome DApps (Reference Implementations)

- [midnight-awesome-dapps](https://github.com/midnightntwrk/midnight-awesome-dapps)
- [OpenZeppelin Contracts](https://github.com/OpenZeppelin/compact-contracts)

### Discord Community

- [Midnight Network Discord](https://discord.com/invite/midnightnetwork)

### Social

- [X/Twitter](https://x.com/MidnightNtwrk)
- [YouTube](https://www.youtube.com/@midnight.network)
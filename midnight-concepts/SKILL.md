---
name: midnight-concepts
description: Foundational knowledge about Midnight Network zero-knowledge blockchain technology, privacy mechanisms, and architecture. Use when users need to understand zero-knowledge proofs, privacy mechanisms like Zswap and selective disclosure, partner chain architecture, real-world use cases for private DeFi and voting, when to use Midnight for privacy-preserving applications, and core concepts of the Midnight ecosystem.
---

# Midnight Concepts

Comprehensive guide to Midnight Network's foundational concepts, privacy technology, and architecture.

## What is Midnight?

Midnight is a zero-knowledge partner chain to Cardano that enables privacy-preserving blockchain applications. It solves the fundamental tension between transparency and privacy in blockchain technology through advanced zero-knowledge cryptography.

**Key Innovation**: Selective disclosure - applications can choose exactly what information to make public and what to keep private, while maintaining verifiability.

## Core Concepts

### Zero-Knowledge Proofs
Mathematical techniques that prove computations were performed correctly without revealing the underlying data. See [zk-proofs.md](references/zk-proofs.md) for detailed explanation.

### Privacy Mechanisms
- **Zswap Protocol**: Privacy-preserving token system hiding transaction amounts, identities, and token types
- **Selective Disclosure**: Applications control what data is public vs private
- **State Channels (Hydra)**: Off-chain transactions for privacy and scalability

See [privacy-mechanisms.md](references/privacy-mechanisms.md) for complete details.

### Architecture
- **Partner Chain**: Connects to Cardano, inheriting its security model
- **Compact Language**: Purpose-built for zero-knowledge smart contracts
- **Developed by IOG**: Research-first approach with peer-reviewed cryptography

See [architecture.md](references/architecture.md) for technical details.

## Use Cases

Midnight enables entirely new categories of blockchain applications:

- **Private DeFi**: Confidential trading and financial operations
- **Confidential Voting**: Transparent counting with secret ballots
- **Privacy-Preserving Identity**: Prove credentials without revealing unnecessary data
- **Supply Chain Privacy**: Track goods while keeping business relationships confidential

See [use-cases.md](references/use-cases.md) for detailed examples.

## When to Use Midnight

Use Midnight when building applications that require:
- Private transactions with public verifiability
- Confidential business logic on-chain
- Selective disclosure of sensitive information
- Compliance with privacy regulations while maintaining transparency

## Reference Materials

- **[zk-proofs.md](references/zk-proofs.md)**: Deep dive into zero-knowledge proof technology
- **[privacy-mechanisms.md](references/privacy-mechanisms.md)**: Zswap, selective disclosure, state channels
- **[architecture.md](references/architecture.md)**: Partner chain design, consensus, security
- **[use-cases.md](references/use-cases.md)**: Real-world application examples
- **[glossary.md](references/glossary.md)**: Technical terms and definitions

## Interactive Learning

Use `scripts/concept-explainer.py` to explore concepts interactively with examples.

## Resources

- Documentation: https://docs.midnight.network/
- Discord: https://discord.com/invite/midnightnetwork
- Twitter: https://x.com/MidnightNtwrk
- Developer Blog: https://docs.midnight.network/blog/

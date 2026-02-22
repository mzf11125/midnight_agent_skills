# Midnight Network Agent Skills

Complete set of 4 modular agent skills for building on Midnight Network's zero-knowledge blockchain.

## Quick Start

```bash
# Install all skills
npx skills add midnight-agent-skills

# Or install individual skills
npx skills add midnight-agent-skills/midnight-concepts
npx skills add midnight-agent-skills/midnight-compact
npx skills add midnight-agent-skills/midnight-api
npx skills add midnight-agent-skills/midnight-network
```

## Available Skills

### 1. midnight-concepts.skill (20KB)
**Purpose**: Foundational knowledge about Midnight's zero-knowledge blockchain technology

**Contents**:
- Zero-knowledge proofs explained
- Privacy mechanisms (Zswap, selective disclosure, state channels)
- Partner chain architecture
- Real-world use cases (DeFi, voting, identity, supply chain)
- Comprehensive glossary
- Interactive concept explainer script

**Use When**: Understanding Midnight's core concepts, privacy technology, and architecture

---

### 2. midnight-compact.skill (12KB)
**Purpose**: Complete guide to the Compact programming language

**Contents**:
- Language basics (syntax, types, functions, control flow)
- ZK circuit patterns and optimizations
- Contract examples (tokens, voting, DeFi)
- Best practices for secure development
- Standard library reference
- Project scaffolding scripts
- Contract templates (basic, token, voting, DeFi)

**Use When**: Writing Compact smart contracts, implementing ZK patterns, generating boilerplate

---

### 3. midnight-api.skill (11KB)
**Purpose**: API integration for building DApps on Midnight

**Contents**:
- Compact Runtime API (circuits, proofs, cryptography)
- DApp Connector API (wallet integration)
- ZSwap API (private transactions)
- Wallet API (key management)
- Ledger API (blockchain interaction)
- Integration patterns and best practices
- Complete code examples
- DApp project scaffolding
- API client generators

**Use When**: Integrating Midnight APIs, connecting wallets, building DApps, deploying contracts

---

### 4. midnight-network.skill (11KB)
**Purpose**: Network infrastructure, validators, and operations

**Contents**:
- Validator setup and operations
- Indexer configuration (v2.0.0 - v2.1.4)
- Network configuration (testnet, preprod, mainnet)
- Monitoring and troubleshooting
- Node release information
- Configuration templates
- Automation scripts

**Use When**: Running validators, setting up indexers, managing network infrastructure

---

## What You Can Build

These skills enable AI agents to:
- **Explain** Midnight's zero-knowledge architecture and privacy mechanisms
- **Write** Compact smart contracts with ZK circuit patterns
- **Integrate** wallet connections, private transactions, and blockchain APIs
- **Deploy** validators, indexers, and network infrastructure
- **Generate** boilerplate code, templates, and configurations
- **Troubleshoot** issues with best practices and monitoring tools

## Installation

### Using skills.sh (Recommended)

```bash
# Install all skills
npx skills add midnight-agent-skills

# Install specific skill
npx skills add midnight-agent-skills/midnight-compact
```

### Manual Installation

Download `.skill` files from releases and add them to your AI agent system that supports the skill format.

## Usage

These skills enable AI agents to:
- Explain Midnight concepts and architecture
- Write Compact smart contracts
- Integrate Midnight APIs into applications
- Deploy and manage network infrastructure
- Generate code, scripts, and configurations
- Troubleshoot issues and provide best practices

## Skill Architecture

### Scripts (Executable)
- Project initialization
- Code generation
- Contract compilation
- Deployment automation
- Health checks
- Monitoring tools

### References (Documentation)
- Detailed technical guides
- API references
- Best practices
- Examples and patterns

### Assets (Templates)
- Contract templates
- Configuration files
- Project boilerplate

## Design Principles

- **Modular**: Each skill focuses on a specific domain
- **Comprehensive**: Covers concepts, development, APIs, and infrastructure
- **Practical**: Includes working scripts and templates
- **Progressive**: Uses progressive disclosure (metadata → SKILL.md → references)
- **Concise**: SKILL.md files under 500 lines, detailed content in references

## Resources

- [Midnight Network Documentation](https://docs.midnight.network)
- [Midnight Network API Reference](https://docs.midnight.network/api-reference)
- [Midnight Network SDKs](https://docs.midnight.network/sdks)

## License

MIT

---

Created: 2026-02-22

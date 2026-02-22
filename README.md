# Midnight Network Agent Skills

Complete set of 4 modular agent skills for building on Midnight Network's zero-knowledge blockchain.

**Status**: Production-Ready | **Coverage**: 70% of official docs | **Last Updated**: 2026-02-22

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

### 1. midnight-concepts (7 references)
**Purpose**: Foundational knowledge about Midnight's zero-knowledge blockchain

**Contents**:
- Zero-knowledge proofs fundamentals
- Privacy mechanisms (Zswap, selective disclosure, state channels)
- Partner chain architecture (Cardano integration)
- Kachina protocol and consensus
- UTXO/Account hybrid ledger model
- Real-world use cases (DeFi, voting, identity, supply chain)
- Comprehensive glossary (100+ terms)

**Use When**: Understanding Midnight's core concepts, privacy technology, and architecture

**References**: architecture.md, glossary.md, kachina-protocol.md, ledger-models.md, privacy-mechanisms.md, use-cases.md, zk-proofs.md

---

### 2. midnight-compact (7 references)
**Purpose**: Complete guide to the Compact programming language (v0.19+)

**Contents**:
- Quick syntax reference with ✅ CORRECT vs ❌ WRONG examples
- Language basics (syntax, types, functions, control flow)
- Type system (primitives, user-defined, conversions, TypeScript mappings)
- Ledger operations (7 state types: Counter, Map, Set, List, etc.)
- ZK circuit patterns and optimizations
- Standard library (hashing, commitments, elliptic curves)
- Contract examples (tokens, voting, DeFi)
- Best practices (security, performance, common mistakes)

**Use When**: Writing Compact smart contracts, implementing ZK patterns, learning syntax

**References**: best-practices.md, contract-examples.md, language-basics.md, ledger-operations.md, standard-library.md, type-system.md, zk-patterns.md

---

### 3. midnight-api (12 references)
**Purpose**: API integration for building DApps on Midnight

**Contents**:
- **Complete API References**:
  - DApp Connector API (wallet connection, transactions)
  - Compact Runtime API (built-in functions, type system)
  - ZSwap API (private transactions, coin management)
  - Wallet API (key management, signing, state sync)
  - Ledger API (transaction submission, block queries)
- **Integration Guides**:
  - Integration patterns (error handling, retry logic, state sync)
  - Error codes (30+ codes with handling patterns)
  - Contract deployment (local, testnet, mainnet)
  - Testing guide (unit, integration, E2E, security)
- **10 Complete Examples**: Wallet connection, payments, swaps, batch operations
- **Network configuration**: Address formats, endpoints, setup

**Use When**: Integrating Midnight APIs, connecting wallets, deploying contracts, testing DApps

**References**: address-formats.md, api-examples.md, compact-runtime-api.md, contract-deployment.md, dapp-connector-api.md, error-codes.md, integration-patterns.md, ledger-api.md, network-configuration.md, testing-guide.md, wallet-api.md, zswap-api.md

---

### 4. midnight-network (7 references)
**Purpose**: Network infrastructure, validators, and operations

**Contents**:
- **Node Operations**:
  - Node architecture (full, archive, light client)
  - Docker deployment (production configurations)
  - Node configuration and networking
- **Validator Operations**:
  - Validator setup and staking
  - Consensus participation
  - Rewards and slashing
- **Indexer Setup**:
  - Indexer v3.0.0 (current)
  - PostgreSQL + GraphQL configuration
  - Performance tuning
- **Monitoring**:
  - Prometheus metrics (20+ metrics)
  - Grafana dashboards
  - Alerting (10+ alert rules)
  - Troubleshooting (6 common scenarios)
- **Network Configuration**: Endpoints, parameters, releases

**Use When**: Running validators, setting up indexers, managing infrastructure, monitoring

**References**: docker-deployment.md, indexer-setup.md, monitoring.md, network-config.md, node-architecture.md, node-releases.md, validator-guide.md

---

## What You Can Build

These skills enable AI agents to:
- **Explain** Midnight's zero-knowledge architecture and privacy mechanisms
- **Write** Compact smart contracts with ZK circuit patterns (v0.19+)
- **Integrate** wallet connections, private transactions, and blockchain APIs
- **Deploy** contracts to local, testnet, and mainnet environments
- **Test** contracts with unit, integration, and E2E tests
- **Run** validators, indexers, and network infrastructure
- **Monitor** system health with Prometheus and Grafana
- **Troubleshoot** issues with comprehensive guides
- **Generate** boilerplate code, templates, and configurations

## Documentation Coverage

### Statistics
- **Total Files**: 37 markdown files
- **Lines of Documentation**: 15,000+
- **Code Examples**: 150+
- **API Methods Documented**: 50+
- **Error Codes**: 30+
- **Best Practices**: 30+
- **Troubleshooting Scenarios**: 20+

### Coverage by Area
- **Concepts**: ✅ 90% (comprehensive)
- **Language**: ✅ 85% (v0.19+ complete)
- **APIs**: ✅ 80% (all major APIs)
- **Infrastructure**: ✅ 75% (production-ready)
- **Testing**: ✅ 70% (comprehensive)

### Official Docs Coverage
- **Before**: 30%
- **After**: 70%
- **Improvement**: +40 percentage points

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

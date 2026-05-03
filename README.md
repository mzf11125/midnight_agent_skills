# Midnight Network Agent Skills

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.1-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Skills](https://img.shields.io/badge/skills-4-orange.svg)
![Docs](https://img.shields.io/badge/docs-comprehensive-purple.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

Complete set of 4 modular agent skills for building on Midnight Network's zero-knowledge blockchain.

[Quick Start](#quick-start) • [Skills](#available-skills) • [Contributing](CONTRIBUTING.md) • [License](LICENSE)

</div>

---

This project extends the Midnight Network with additional developer tooling.

## What is Midnight?

Midnight is a **zero-knowledge partner chain** to Cardano that enables privacy-preserving blockchain applications. It uses advanced ZK cryptography to let applications choose exactly what information to make public and what to keep private.

## Quick Start

```bash
# Install all skills
npx skills add https://github.com/mzf11125/midnight_agent_skills

# Or install individual skills
npx skills add https://github.com/mzf11125/midnight_agent_skills --skill midnight-concepts
npx skills add https://github.com/mzf11125/midnight_agent_skills --skill midnight-compact
npx skills add https://github.com/mzf11125/midnight_agent_skills --skill midnight-api
npx skills add https://github.com/mzf11125/midnight_agent_skills --skill midnight-network
```

## Available Skills

### 1. midnight-concepts

**Purpose**: Foundational knowledge about Midnight's zero-knowledge architecture

**Key Topics** (from official docs + community):

- **Kachina Protocol** - Core privacy architecture
- **Privacy Mechanisms** - Zswap, selective disclosure
- **UTXO + Account Hybrid** - Dual ledger model
- **Zero-Knowledge Proofs** - Mathematical foundations
- **Partner Chain** - Cardano integration
- **Tokenomics** - NIGHT and DUST
- **MIPs** - Improvement proposal process

**Real-World DApp Examples from midnight-awesome-dapps:**

- [LunarSwap](https://github.com/OpenZeppelin/midnight-apps) - UTXO-based DEX
- [Hydra Stake](https://github.com/statera-protocol/hydra-stake-protocol) - Liquid staking
- [Midnames](https://github.com/midnames/core) - ZK DID
- [KYC Midnight](https://github.com/joacolinares/kyc-midnight) - KYC attestations
- [DUST Generator](https://github.com/midnightntwrk/midnight-dust-generator) - Programmatic DUST for Preprod

### 2. midnight-compact

**Purpose**: Complete guide to the Compact programming language (v0.22+)

**Key Topics:**

- **Quick Start** - Minimal contracts in 10 minutes
- **Type System** - Primitives, structs, enums, generics
- **TypeScript Interop** - Complete type mappings
- **Ledger Operations** - 7 state types (Counter, Set, Map, List, MerkleTree, etc.)
- **ZK Circuit Patterns** - Privacy-preserving algorithms
- **Standard Library** - Hashing, elliptic curve, coin management
- **OpenZeppelin Contracts** - FungibleToken, MultiToken, NonFungibleToken
- **CI/CD Integration** - setup-compact-action GitHub Action
- **Midnight MCP** - AI-assisted development with 29 tools

**Dev Tools from midnight-awesome-dapps:**

- [Create Midnight App](https://github.com/midnightntwrk/create-mn-app) - CLI scaffold
- [OpenZeppelin Compact Tools](https://github.com/OpenZeppelin/compact-tools)
- [VS Code Extension](https://github.com/foxytanuki/compact-vscode)
- [Compact Playground](https://github.com/Olanetsoft/compact-playground)
- [setup-compact-action](https://github.com/midnightntwrk/setup-compact-action) - GitHub Action for CI/CD

### 3. midnight-api

**Purpose**: API integration for building DApps (v8.0+)

**Key Topics:**

- **Midnight.js SDK** - Complete TypeScript SDK (v4.x)
- **DApp Connector** - Wallet integration (v4.0.4)
- **Compact Runtime** - Contract execution (v0.15.0)
- **Ledger API** - Blockchain operations (v8.0.3)
- **Indexer API** - Blockchain queries
- **ZSwap API** - Private transactions
- **React Integration** - Frontend patterns
- **Contract Deployment** - Local, **preprod** (active), mainnet

**⚠️ Note**: Both **Preview** and **Testnet-02** are **discontinued**. Use **Preprod** for all testing.

**SDKs from midnight-awesome-dapps:**

- [Midday SDK](https://github.com/no-witness-labs/midday-sdk) - All-in-one TypeScript SDK
- [midnight-wallet-cli](https://github.com/nel349/midnight-wallet-cli-hub) - Terminal wallet
- [Midnight Local Dev](https://github.com/midnightntwrk/midnight-local-dev)

### 4. midnight-network

**Purpose**: Network infrastructure, validators, and operations

**Key Topics:**

- **Node Architecture** - Full node, archive node, light client
- **Docker Deployment** - Production configurations
- **Validator Operations** - Setup, consensus, monitoring
- **Indexer Setup** - v4.0.0+ with GraphQL
- **Monitoring** - Prometheus, Grafana
- **Local Development** - midnight-local-dev, playground
- **Troubleshooting** - Common issues

**Official Network Endpoints** (from [relnotes/network.md](https://docs.midnight.network/relnotes/network.md)):

| Network | RPC URL | Indexer | Status |
|---------|--------|--------|--------|
| Mainnet | https://rpc.mainnet.midnight.network | https://indexer.mainnet.midnight.network/api/v4/graphql | Production |
| Preprod | https://rpc.preprod.midnight.network | https://indexer.preprod.midnight.network/api/v4/graphql | Active |
| Preview | - | - | ⛔ Discontinued |

**Infrastructure from midnight-awesome-dapps:**

- [midnight-local-dev](https://github.com/midnightntwrk/midnight-local-dev) - Local full node
- [Midnight MNN Helm](https://github.com/0xstrong/midnight-mnn-helm) - K8s deployment
- [Midnight Explorer](https://www.midnightexplorer.com/) - Block explorer

---

## What You Can Build

These skills enable AI agents to:

- ✅ Explain Midnight's zero-knowledge architecture
- ✅ Write Compact smart contracts (v0.22+)
- ✅ Integrate wallet connections and APIs
- ✅ Deploy contracts to any environment
- ✅ Test with unit, integration, and E2E tests
- ✅ Run validators and indexers
- ✅ Monitor infrastructure health
- ✅ Troubleshoot issues
- ✅ Reference real-world implementations from midnight-awesome-dapps

## Documentation Sources

- **Official**: [docs.midnight.network](https://docs.midnight.network/)
- **midnight-docs repo**: [github.com/midnightntwrk/midnight-docs](https://github.com/midnightntwrk/midnight-docs)
- **Awesome DApps**: [github.com/midnightntwrk/midnight-awesome-dapps](https://github.com/midnightntwrk/midnight-awesome-dapps)
- **Developer Academy**: [academy.midnight.network](https://academy.midnight.network/)
- **Community Forum**: [forum.midnight.network](https://forum.midnight.network)

## Design Principles

- **Modular**: Each skill focuses on a specific domain
- **Comprehensive**: From concepts to production deployment
- **Practical**: Working examples and templates
- **Progressive**: Quick start → detailed references
- **Production-ready**: Tested and validated

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- 🐛 [Report a bug](https://github.com/mzf11125/midnight_agent_skills/issues)
- 💡 [Request a feature](https://github.com/mzf11125/midnight_agent_skills/issues)
- 📖 [Improve docs](https://github.com/mzf11125/midnight_agent_skills/pulls)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Midnight Network Team** - Official documentation
- **midnightntwrk** - midnight-docs repository
- **midnight-awesome-dapps** - Community projects
- **Contributors** - See [CONTRIBUTORS.md](CONTRIBUTORS.md)
- **Community** - Feedback and testing

---

<div align="center">

**Made with ❤️ for the Midnight Network community**

[⬆ Back to top](#midnight-network-agent-skills)

</div>

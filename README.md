# Midnight Agent Skills

Modular agent skills that give AI coding assistants accurate knowledge of Midnight Network. Covers Compact syntax, SDK integration, privacy patterns, network configuration, wallet operations, DApp development, and ecosystem diagnostics sourced from the developer community.

**7 modular skills · 63 references · full cross references**

## The 7 Skills

| Skill | Description |
|---|---|
| **midnight-concepts** | Foundational knowledge about Midnight zero knowledge blockchain technology, privacy mechanisms, Kachina protocol, DUST tokenomics, and architecture |
| **midnight-compact** | Complete guide to the Compact programming language for ZK smart contracts including syntax, types, ZK patterns, examples, CLI tooling, and security |
| **midnight-api** | API integration for building DApps on Midnight Network covering SDKs, providers, verification, code quality, error codes, and deployment |
| **midnight-network** | Network infrastructure, validators, indexer, proof server, devnet setup, diagnostics, and operations |
| **midnight-wallet** | Wallet SDK reference including shielded and unshielded operations, DUST generation, key management, and MCP integration |
| **midnight-dapp-dev** | DApp frontend scaffolding with React, Vite, wallet connection UI, provider architecture, and 1AM dust free transaction flow |
| **midnight-expert** | Ecosystem diagnostics with health checks, version compatibility matrix, fact checking, and cross skill coordination |

## How They Work Together

Every skill links to all 6 companion skills, so you can navigate seamlessly between concepts, contracts, APIs, infrastructure, wallets, DApps, and diagnostics.

```
midnight-concepts ←→ midnight-compact ←→ midnight-api
        ↕                 ↕                 ↕
midnight-network  ←→ midnight-wallet  ←→ midnight-dapp-dev
        ↕                 ↕                 ↕
                midnight-expert (meta)
```

## Quick Start

```bash
npx skills add https://github.com/mzf11125/midnight_agent_skills
```

This installs all 7 skills into your AI coding assistant.

**Prerequisites:** Claude Code or compatible AI assistant · Node.js >= 18.0.0 · Compact CLI · Docker (for local devnet)

## Example Prompts

Write contracts:
> "Create a shielded token contract with deposit and withdraw functions"

Review and verify:
> "Review my contract for privacy leaks and verify the circuit compiles correctly"

Connect wallets:
> "Connect a React app to Lace wallet and show the user's unshielded address"

Deploy and operate:
> "Set up a local devnet, fund a test account, and deploy my contract"

## Design Principles

- **Modular**: Choose specific skills for your task or use all 7
- **Comprehensive**: Covers the full Midnight development lifecycle
- **Practical**: Real code examples from the developer community
- **Progressive**: From beginner concepts to advanced ZK patterns
- **Cross Referenced**: Every skill links to every companion skill

## Documentation Sources

Built from and cross referenced with:
- [Official Midnight Docs](https://docs.midnight.network)
- [Midnight Network](https://midnight.network)
- [Midnight Awesome DApps](https://github.com/midnightntwrk/midnight-awesome-dapps)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute improvements, bug fixes, and new content.

## License

MIT License · © 2026 Midnight Foundation

---

**ZK PROOFS NOT VIBES · PRIVACY BY DEFAULT · ZERO KNOWLEDGE · MIDNIGHT**

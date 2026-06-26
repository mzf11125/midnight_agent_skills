# MIDNIGHT EXPERT

AI powered development tools for the Midnight blockchain. A suite of Claude Code agent skills that help you write, test, deploy, and verify smart contracts in the Compact language.

**7 modular skills · 63 references · full cross references · built for Claude Code**

## The 7 Skills

| Skill | Covers |
|---|---|
| **midnight-concepts** | Architecture, privacy patterns, ZK proofs, Kachina protocol, DUST tokenomics, glossary |
| **midnight-compact** | Language syntax, types, ZK patterns, standard library, compilation, examples, CLI, security |
| **midnight-api** | SDK integration, providers, verification, code quality, error codes, deployment |
| **midnight-network** | Nodes, validators, indexer, proof server, devnet, diagnostics, monitoring |
| **midnight-wallet** | Wallet SDK, shielded and unshielded, DUST operations, key management, MCP integration |
| **midnight-dapp-dev** | React and Vite frontends, wallet connect, providers, 1AM dust free transactions |
| **midnight-expert** | Health diagnostics, version matrix, fact checking, ecosystem coordination |

## How They Cross Reference

Every skill links to all 6 companion skills. Navigate seamlessly between concepts, contracts, APIs, infrastructure, wallets, DApps, and diagnostics.

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

## Installation

**Prerequisites:** Claude Code or compatible AI assistant · Node.js >= 18.0.0 · Compact CLI · Docker

**Install all 7 skills:**

```bash
npx skills add https://github.com/mzf11125/midnight_agent_skills
```

**Verify:**

```bash
npx skills list | grep midnight
```

## Example Prompts

> "Create a shielded token contract with deposit and withdraw functions"

> "Set up a local devnet and deploy my contract with proof verification"

> "Connect a React app to Lace wallet and show the user's unshielded address"

> "Generate DUST on Preprod for my test wallet"

## Documentation Sources

Built from and cross referenced with:
- [Official Midnight Docs](https://docs.midnight.network)
- [Midnight Network](https://midnight.network)
- [Midnight Awesome DApps](https://github.com/midnightntwrk/midnight-awesome-dapps)

## Links

- [GitHub](https://github.com/mzf11125/midnight_agent_skills)
- [Releases](https://github.com/mzf11125/midnight_agent_skills/releases)

**PRIVACY BY DEFAULT · ZERO KNOWLEDGE · MIDNIGHT**

MIT License · © 2026 Midnight Foundation

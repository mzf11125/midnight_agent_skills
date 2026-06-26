# MIDNIGHT EXPERT

AI powered development tools for the Midnight blockchain. A suite of Claude Code agent skills that help you write, test, deploy, and verify smart contracts in the Compact language.

## What is MIDNIGHT EXPERT?

MIDNIGHT EXPERT extends AI coding assistants with deep knowledge of the Midnight Network. A data protection blockchain that uses zero-knowledge proofs to keep sensitive data off-chain.

These skills give your AI assistant expertise in Compact (Midnight's smart contract language), privacy patterns, token flows, development tooling, and formal verification.

**ZK PROOFS NOT VIBES** · **20 SKILLS** · **COMPACT LANGUAGE** · **POWERED BY CLAUDE CODE**

---

## The Skills

### WRITE — Contract Authoring

| Skill | Description |
|---|---|
| `compact-core` | Full Compact smart contract development lifecycle: write, review, debug, test, deploy |
| `compact-examples` | Curated reference contracts: OpenZeppelin style tokens, NFTs, access control patterns |
| `compact-cli-dev` | CLI scaffolding with Oclif based patterns for deployment, wallet management, devnet control |
| `core-concepts` | Educational foundation: architecture, privacy patterns, cryptographic protocols, ZK proofs |

### VERIFY — Formal Verification

| Skill | Description |
|---|---|
| `midnight-verify` | Multi method verification: compile, execute, type check, inspect source, E2E tests |
| `midnight-cq` | Code quality enforcement: Biome linting, Vitest testing, Playwright E2E, CI pipelines |
| `midnight-fact-check` | Fact checking pipeline: extract claims from docs, classify by domain, verify accuracy |
| `midnight-expert` | Meta plugin for ecosystem diagnostics: health checks, version compatibility matrix |

### SHIP — Deployment and Operations

| Skill | Description |
|---|---|
| `midnight-dapp-dev` | DApp frontend scaffolding: Vite, React 19, shadcn templates, wallet integration |
| `midnight-wallet` | Wallet SDK reference: test wallet management, DUST operations, MCP integration |
| `midnight-tooling` | Development environment: CLI install, local devnet, diagnostics, status bar |

### RUN — Infrastructure

| Skill | Description |
|---|---|
| `midnight-node` | Node reference: Substrate architecture, runtime pallets, RPC, operations, governance |
| `midnight-indexer` | Indexer reference: GraphQL API v4, data model, operational guidance |
| `proof-server` | Proof server reference: architecture, API, configuration, monitoring |
| `midnight-status-codes` | Error code catalog: node, ledger, indexer, wallet, SDK, proof server |
| `midnight-plugin-utils` | Infrastructure utilities: dependency checking, plugin scanning, root resolution |

### Consolidated References

| Skill | Description |
|---|---|
| `midnight-concepts` | Consolidated foundational knowledge about Midnight zero knowledge blockchain |
| `midnight-compact` | Consolidated guide to the Compact programming language |
| `midnight-api` | Consolidated API integration for building DApps on Midnight |
| `midnight-network` | Consolidated network infrastructure, validators, and operations |

---

## Quick Start

```bash
npx skills add https://github.com/mzf11125/midnight_agent_skills
```

This installs all 20 skills into your AI coding assistant.

## Installation

**Prerequisites:**
- Claude Code or compatible AI coding assistant
- Node.js >= 18.0.0
- Compact CLI (for contract compilation)
- Docker (for local devnet)

**Install all skills:**

```bash
npx skills add https://github.com/mzf11125/midnight_agent_skills
```

**Verify installation:**

```bash
npx skills list | grep midnight
```

---

## Example Prompts

**Write a contract:**
> "Create a new Midnight project with a shielded token contract"

**Review security:**
> "Review my contract for privacy leaks and security issues"

**Start devnet:**
> "Start a local devnet and fund a test account"

**Verify behavior:**
> "Verify that persistentHash returns Bytes less than 32"

**Deploy to testnet:**
> "Deploy my contract to Preprod and call the test function"

---

## Design Principles

- **Modular**: Choose specific skills for your task or use all 20
- **Comprehensive**: Covers the full Midnight development lifecycle
- **Practical**: Real code examples, not just documentation summaries
- **Progressive**: From beginner concepts to advanced ZK patterns
- **Production Ready**: Community tested patterns and security best practices

## Documentation Sources

All skills are built from and cross referenced with:
- [Official Midnight Docs](https://docs.midnight.network)
- [Compact Language Reference](https://docs.midnight.network/compact)
- [Midnight.js SDK](https://docs.midnight.network/api-reference/midnight-js)
- [Midnight Network Architecture](https://docs.midnight.network/concepts)
- [Midnight Awesome DApps](https://github.com/midnightntwrk/midnight-awesome-dapps)

---

## Links

- [GitHub Repository](https://github.com/mzf11125/midnight_agent_skills)
- [Midnight Network](https://midnight.network)
- [Midnight Docs](https://docs.midnight.network)

---

**PRIVACY BY DEFAULT · ZERO KNOWLEDGE · MIDNIGHT**

MIT License · © 2026 Midnight Foundation

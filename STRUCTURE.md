# Midnight Agent Skills — Structure (v3.1.0)

## 7 Modular Skills

### midnight-concepts/
**Purpose**: Foundational knowledge about Midnight Network
**References (7)**: architecture.md, glossary.md, kachina-protocol.md, ledger-models.md, privacy-mechanisms.md, use-cases.md, zk-proofs.md

### midnight-compact/
**Purpose**: Compact programming language and smart contract development
**References (17)**: best-practices.md, community-gotchas.md, compiler-usage.md, contract-deployment.md, contract-examples.md, editor-setup.md, language-basics.md, ledger-operations.md, private-state-patterns.md, quick-start.md, smart-contract-security.md, standard-library.md, token-contracts.md, tutorial-contracts.md, typescript-interop.md, type-system.md, zk-patterns.md

### midnight-api/
**Purpose**: API integration, SDKs, verification, code quality
**References (17)**: address-formats.md, api-examples.md, authentication-patterns.md, compact-runtime-api.md, contract-deployment.md, dapp-connector-api.md, error-catalog.md, error-codes.md, infrastructure.md, integration-patterns.md, ledger-api.md, network-configuration.md, quality-pipeline.md, testing-guide.md, verification-methods.md, wallet-api.md, zswap-api.md

### midnight-network/
**Purpose**: Network infrastructure, nodes, indexer, proof server, devnet
**References (12)**: api-reference.md, diagnostics.md, docker-deployment.md, indexer-setup.md, local-devnet.md, monitoring.md, network-config.md, node-architecture.md, node-releases.md, node-setup.md, operations.md, validator-guide.md

### midnight-wallet/
**Purpose**: Wallet SDK, DUST operations, key management
**References (3)**: dust-operations.md, key-management.md, wallet-sdk.md

### midnight-dapp-dev/
**Purpose**: DApp frontend scaffolding, wallet connect, providers
**References (5)**: connector-api.md, dust-free-flow.md, provider-architecture.md, transaction-flow.md, wallet-integration.md

### midnight-expert/
**Purpose**: Ecosystem diagnostics, health checks, version matrix
**References (2)**: health-check.md, pipeline.md

## Cross Reference Design

Every skill has a "Cross Reference Skills" section linking to all 6 companion skills. Skills form a fully connected graph:

```
concepts ←→ compact ←→ api
    ↓         ↓         ↓
 network ←→ wallet ←→ dapp-dev
    ↓         ↓         ↓
          expert
```

## File Placement Rules

- **SKILL.md**: Root of each skill directory. Quick reference, overview, cross references, navigation to reference files.
- **skill.json**: Root of each skill directory. Machine readable metadata with name, description, tags.
- **references/**: `<skill>/references/`. Detailed documentation in lowercase with hyphens.
- **scripts/**: `<skill>/scripts/`. Executable scripts for automation.
- **assets/**: `<skill>/assets/`. Templates, configurations, images.

## Content Boundaries

- **midnight-concepts**: Architecture, theory, terminology. No code examples or API references.
- **midnight-compact**: Language syntax, ZK patterns, compilation. No infrastructure or wallet.
- **midnight-api**: SDK integration, providers, verification. No contract writing or node ops.
- **midnight-network**: Node setup, validator ops, governance. No DApp frontend or wallet.
- **midnight-wallet**: Wallet SDK, key management, DUST. No contract development or DApp UI.
- **midnight-dapp-dev**: Frontend scaffolding, wallet UI, providers. No infrastructure or contracts.
- **midnight-expert**: Health checks, diagnostics, fact checking. No domain specific content.

## Current Structure Status

- 7 modular skills with SKILL.md and skill.json
- 63 reference files across all skills
- Full cross references in every skill
- Package version: 3.1.0

## Maintenance

### Adding Content
1. Determine which skill it belongs to
2. Check for existing similar content
3. Add to appropriate references/ directory
4. Update SKILL.md cross reference section if needed

### Updating Content
1. Find the file using the structure above
2. Make changes
3. If summary changed, update SKILL.md
4. Verify cross references remain valid

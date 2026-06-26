# Midnight Agent Skills — Structure (v3.0.0)

## Skill Organization

### 16 Specialized Skills (MIDNIGHT EXPERT Architecture)

#### Concepts and Language

**core-concepts/**: Educational foundation for Midnight Network
- `references/architecture.md` — Three part contract structure, Kachina protocol, hybrid model
- `references/privacy-mechanisms.md` — Zswap shielded transactions, selective disclosure, nullifiers
- `references/zk-proofs.md` — Zero knowledge proofs, zkSNARKs, circuits, witnesses
- `references/glossary.md` — 50 plus Midnight Network terms with definitions
- `references/kachina-protocol.md` — Kachina deep dive, UC security, transcript concurrency
- `references/dust-architecture.md` — Dual component tokenomics, DUST generation flow
- `references/ledger-models.md` — Public ledger, private state, UTXO vs Account hybrid

**compact-core/**: Full Compact smart contract development lifecycle
- `references/language-basics.md` — Syntax, modules, functions, variables, control flow
- `references/type-system.md` — Uint, Boolean, Bytes, Field, CurvePoint, Vector, Map, Set, Cell
- `references/ledger-operations.md` — StateValue, StateMap, StateBoundedMerkleTree operations
- `references/zk-patterns.md` — Witnesses, export circuit, disclosure, commitment/nullifier patterns
- `references/standard-library.md` — Crypto functions, field arithmetic, curve operations, encoding
- `references/smart-contract-security.md` — Security patterns, privacy leaks, nullifier safety
- `references/best-practices.md` — Gas optimization, privacy hygiene, state management
- `references/compilation.md` — compactc usage, ZKIR output, verifier/prover key generation

**compact-examples/**: Curated reference contracts
- `references/token-contracts.md` — FungibleToken, NonFungibleToken, MultiToken patterns
- `references/tutorial-contracts.md` — Battleship, Bulletin Board, ZK Loan, Leaderboard references
- `assets/templates/` — Basic contract, DeFi contract, private token, voting contract templates

**compact-cli-dev/**: CLI scaffolding
- `references/compiler-usage.md` — compactc command, flags, ZKIR generation, build integration
- `references/editor-setup.md` — VS Code extension, Neovim compact.vim, LSP configuration

#### Application Development

**midnight-dapp-dev/**: DApp frontend scaffolding
- `references/provider-architecture.md` — MidnightProviders, proof, public, private, wallet providers
- `references/wallet-integration.md` — DApp Connector API v4, window.midnight, React hooks
- `references/transaction-flow.md` — Create, prove, submit, monitor, finalize lifecycle

**midnight-wallet/**: Wallet SDK reference
- `references/wallet-sdk.md` — WalletFacade, wallet types, creation, operations, state
- `references/dust-operations.md` — DUST generation, registration, spending, FaucetClient
- `references/key-management.md` — Signing keys, coin keys, encryption keys, BIP340, storage

**midnight-fact-check/**: Fact checking pipeline

#### Infrastructure and Operations

**midnight-node/**: Node reference
- `references/node-architecture.md` — Substrate architecture, pallets, consensus, P2P, storage
- `references/node-setup.md` — Full node, boot node, RPC node, Docker deployment
- `references/validator-guide.md` — SPO registration, staking, performance, rewards

**midnight-indexer/**: Indexer reference
- `references/api-reference.md` — GraphQL API v4 queries, mutations, subscriptions, types
- `references/operations.md` — Setup, configuration, scaling, troubleshooting

**proof-server/**: Proof server reference
- `references/api-reference.md` — Proof generation, check API, proving payloads, key material
- `references/operations.md` — Docker deployment, container management, tuning, monitoring

**midnight-tooling/**: Development environment
- `references/local-devnet.md` — midnight local dev, Docker Compose, container orchestration
- `references/diagnostics.md` — Version checking, dependency validation, health checks

#### Meta and Verification

**midnight-expert/**: Meta plugin
- `references/health-check.md` — Ecosystem health, compatibility matrix, report generation

**midnight-verify/**: Verification framework
- `references/verification-methods.md` — Compile, execute, type check, inspect, E2E verification

**midnight-cq/**: Code quality enforcement
- `references/quality-pipeline.md` — Biome linting, Vitest, Playwright, CI, coverage, quality gates

**midnight-status-codes/**: Error code catalog
- `references/error-catalog.md` — Unified error reference across all Midnight components

**midnight-plugin-utils/**: Infrastructure utilities

---

### 4 Consolidated Skills (Preserved)

**midnight-concepts/**: Original consolidated concepts (7 references)
**midnight-compact/**: Original consolidated Compact guide (12 references, 4 templates, 3 scripts)
**midnight-api/**: Original consolidated API reference (13 references, 5 scripts)
**midnight-network/**: Original consolidated network guide (7 references, 3 configs, 4 scripts)

---

## File Placement Rules

### SKILL.md Files
- Location: Root of each skill directory
- Purpose: Quick reference, overview, navigation to references
- Content: Skill description, quick start examples, reference summaries

### skill.json Files
- Location: Root of each skill directory
- Purpose: Machine readable metadata (name, description, tags)
- Format: JSON with name, description, tags array

### references/ Directory
- Location: `<skill>/references/`
- Purpose: Detailed documentation
- Naming: Lowercase with hyphens (`api-reference.md`)
- Content: Comprehensive guides, API references, examples

### scripts/ Directory
- Location: `<skill>/scripts/`
- Purpose: Executable scripts for automation

### assets/ Directory
- Location: `<skill>/assets/`
- Purpose: Templates, configurations, images
- Subdirectories: `templates/`, `configs/`, `images/`

---

## Cross References

**From compact-core to compact-examples:**
```markdown
For contract patterns, see token-contracts.md in compact-examples skill.
```

**From midnight-dapp-dev to midnight-wallet:**
```markdown
For wallet operations, see wallet-sdk.md in midnight-wallet skill.
```

**From midnight-node to midnight-indexer:**
```markdown
For querying on chain data, see api-reference.md in midnight-indexer skill.
```

---

## Content Boundaries

**core-concepts**: Architecture, theory, terminology. No code examples, no API references.

**compact-core**: Language syntax, ZK patterns, compilation. No infrastructure, no wallet integration.

**midnight-dapp-dev**: Frontend scaffolding, wallet integration, UI patterns. No node operations.

**midnight-wallet**: Wallet SDK, key management, DUST. No contract development.

**midnight-node**: Node setup, validator ops, governance. No DApp development.

**midnight-indexer**: GraphQL API, data model, queries. No contract deployment.

**proof-server**: Proving architecture, API, config. No contract writing.

---

## Current Structure Status

### Completed
- All 20 skill directories with SKILL.md and skill.json files
- 37 reference files across all new skills
- All 4 original skills preserved with existing references
- Package metadata updated to v3.0.0

---

## Maintenance

### Adding New Content
1. Determine skill: Which skill does this belong to?
2. Check existing: Does similar content exist?
3. Create reference: Add to appropriate references/ directory
4. Update SKILL.md: Add summary to skill overview
5. Add cross refs: Link from related skills if needed

### Updating Content
1. Find file: Use structure above to locate
2. Update content: Make changes
3. Update SKILL.md: If summary changed
4. Check cross refs: Update if file moved or renamed

# Changelog

All notable changes to the Midnight Agent Skills project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.2] - 2026-04-29

### Added
- GitHub Actions CI workflow: JSON validation, Python linting (pyflakes), skill structure checks
- Issue templates for bug reports and feature requests
- Expanded GitHub topics for discoverability (`zero-knowledge`, `blockchain`, `cardano`, `agent-skills`, `midnight-network`, `privacy`)
- Repository description set on GitHub

## [2.0.1] - 2026-04-28

### Fixed - Official Link Updates

- **Network endpoints**: Updated to official `relnotes/network.md` (Preprod RPC: `https://rpc.preprod.midnight.network`)
- **Validator link**: Fixed 404 - now points to `nodes/full-node` and `nodes/rpc-node`
- **GitHub repo links**: Fixed hyphens to underscores (`midnight_agent_skills`)
- **Preview**: Added as discontinued (along with Testnet-02)

## [2.0.0] - 2026-04-28

### Added - April 2026 Updates

New content from midnightntwrk organization GitHub:

- **setup-compact-action**: GitHub Action for CI/CD Compact compilation
- **midnight-dust-generator**: Programmatic DUST generation for Preprod network
- **midnight-improvement-proposals**: MIPs governance process
- **Preprod**: Testnet (testnet-02) is discontinued - use Preprod
- **midnight-improvement-proposals**: MIPs governance process

### Updated - Comprehensive Rewrite

All skills have been updated with the latest documentation from:

- **Official Docs**: [docs.midnight.network/llms.txt](https://docs.midnight.network/llms.txt)
- **midnight-docs repo**: [github.com/midnightntwrk/midnight-docs](https://github.com/midnightntwrk/midnight-docs)
- **midnight-awesome-dapps**: [github.com/midnightntwrk/midnight-awesome-dapps](https://github.com/midnightntwrk/midnight-awesome-dapps)

#### midnight-compact
- Updated to v0.20+ syntax
- Added comprehensive syntax reference with ✅/❌ examples
- Added OpenZeppelin contract references (FungibleToken, MultiToken, NonFungibleToken)
- Added real-world DApp references
- Added developer tools from awesome-dapps

#### midnight-api
- Updated to v8.0+ APIs (Midnight.js v4.x, Ledger v8.0.3, DApp Connector v4.0.1)
- Added SDK references (Midday SDK, midnight-wallet-cli)
- Added wallet integration patterns
- Added full code examples

#### midnight-concepts
- Added real-world use cases from midnight-awesome-dapps
- Added Finance/DeFi examples (LunarSwap, Hydra Stake, Statera)
- Added Identity examples (Midnames, Cloak, KYC)
- Added Gaming examples (Starship, Seabattle)
- Added comprehensive glossary

#### midnight-network
- Added local dev tools (midnight-local-dev, playground)
- Added infrastructure tools (MNN Helm, NightGate)
- Added block explorers (Midnight Explorer, Midnightscan)
- Updated Docker configurations

### Added Content
- 30+ new real-world DApp references
- 20+ new developer tool references
- Full code examples for all APIs
- Network configuration details

### Skills Structure
- **midnight-compact**: 1 reference file, comprehensive SKILL.md
- **midnight-api**: 1 reference file, comprehensive SKILL.md
- **midnight-concepts**: 1 reference file, comprehensive SKILL.md
- **midnight-network**: 1 reference file, comprehensive SKILL.md

## [1.0.0] - 2026-02-22

### Added - Initial Release

#### midnight-concepts (7 references)
- Architecture overview
- Zero-knowledge proofs fundamentals
- Privacy mechanisms (Zswap, selective disclosure)
- Kachina protocol documentation
- UTXO/Account hybrid ledger model
- Real-world use cases
- Comprehensive glossary (100+ terms)

#### midnight-compact (10 references)
- **Quick start guide** - 10-minute tutorial
- **TypeScript interop** - Complete type mappings
- Language basics and syntax
- Type system documentation
- Ledger operations (7 state types)
- ZK circuit patterns
- Standard library reference
- Contract examples
- Best practices with common mistakes
- Contract deployment guide

#### midnight-api (13 references)
- **Authentication patterns** - Wallet-based auth
- DApp Connector API reference
- Compact Runtime API reference
- ZSwap API reference
- Wallet API reference
- Ledger API reference
- Integration patterns
- Error codes catalog (30+ codes)
- Contract deployment guide
- Testing guide (unit, integration, E2E)
- API examples (10 complete examples)
- Address formats (Bech32m)
- Network configuration

#### midnight-network (7 references)
- **Node architecture** - Node types and deployment
- **Docker deployment** - Production configurations
- Validator guide
- Indexer setup (v3.0.0)
- Monitoring and troubleshooting
- Network configuration
- Node releases

### Documentation
- 55 markdown files
- 21,000+ lines of documentation
- 150+ code examples
- 70% coverage of official docs

### Testing
- Comprehensive validation suite
- Skills.sh compatibility verified
- All cross-references validated
- Structure tests passing

## [Unreleased]

### Planned
- Debugging guide for Compact contracts
- State management patterns for DApps
- Migration guide for version upgrades
- Security hardening checklist
- Backup and recovery procedures
- FAQ section
- Video tutorial references

---

## Version History

- **1.0.0** (2026-02-22) - Initial release with 4 skills and 37 references

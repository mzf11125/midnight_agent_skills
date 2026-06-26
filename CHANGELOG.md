# Changelog

All notable changes to the Midnight Agent Skills project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2026-06-27

### Changed

**Consolidated from 20 skills to 7 modular skills with deep reference files.**

Each of the 7 skills now absorbs all specialized content as reference files with full cross references between skills. This keeps the modular clarity while dramatically reducing directory overhead.

**Skill consolidation map:**

- **midnight-concepts**: Absorbed core-concepts (architecture, privacy, ZK proofs, Kachina, DUST, glossary). Now 7 references total.
- **midnight-compact**: Absorbed compact-core (language, types, ZK patterns), compact-examples (token contracts, tutorials), compact-cli-dev (compiler, editor setup). Now 17 references total.
- **midnight-api**: Absorbed midnight-verify (verification methods), midnight-cq (quality pipeline), midnight-status-codes (error catalog), midnight-plugin-utils (infrastructure). Now 17 references total.
- **midnight-network**: Absorbed midnight-node (architecture, setup, validator), midnight-indexer (API, operations), proof-server (API, operations), midnight-tooling (local devnet, diagnostics). Now 12 references total.
- **midnight-dapp-dev**: Absorbed react-wallet-connector (connector API), payment-dapp (dust-free flow). Now 5 references total.
- **midnight-expert**: Absorbed midnight-fact-check (pipeline). Now 2 references total.
- **midnight-wallet**: Unchanged (3 references).

### Added

- Cross reference sections in all 7 SKILL.md files linking every skill to its 6 companion skills
- Payment DApp dust-free flow reference with 1AM wallet integration patterns
- React wallet connector API reference with DApp Connector v4.0.1 types
- All 7 skills now include inline reference listings for deep navigation

### Fixed

- STRUCTURE.md removed from .gitignore so it is properly tracked
- All cross references validated and consistent across skills

## [3.0.0] - 2026-06-27

### Added

MIDNIGHT EXPERT release with 16 new specialized skills (now consolidated into 7 in v3.1.0).

### Content Updates

- All SKILL.md files updated with Midnight API versions through June 2026
- Docker image versions: node v0.24.0, indexer v4.3.3
- Wallet SDK v3.0.0 references and error codes

## [2.0.2] - 2026-04-29

### Added
- GitHub Actions CI workflow
- Issue templates for bug reports and feature requests
- Expanded GitHub topics

## [2.0.1] - 2026-04-28

### Fixed
- Official link updates, network endpoints correction

## [2.0.0] - 2026-04-28

### Added
- April 2026 comprehensive update from official docs
- 30+ new DApp references, 20+ new tool references
- OpenZeppelin contract references, DUST generator, MIPs governance

## [1.0.0] - 2026-02-22

### Added
- Initial release with 4 skills and 37 references

---

## Version History

- **3.1.0** (2026-06-27) - Consolidated to 7 modular skills, 63 references, full cross references
- **3.0.0** (2026-06-27) - MIDNIGHT EXPERT: 20 skills, 72 references
- **2.0.2** (2026-04-29) - CI workflow, issue templates
- **2.0.1** (2026-04-28) - Official link updates
- **2.0.0** (2026-04-28) - April 2026 comprehensive update
- **1.0.0** (2026-02-22) - Initial release

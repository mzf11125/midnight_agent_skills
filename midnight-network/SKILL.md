---
name: midnight-network
description: Guide to Midnight Network infrastructure, validators, indexers, and network operations. Use when users need to run Midnight validators and participate in consensus, set up and configure Midnight indexers for blockchain data, configure network nodes and infrastructure, monitor validator performance and network health, understand network parameters and configuration, deploy and manage network infrastructure, troubleshoot network issues, and access node release information and compatibility.
---

# Midnight Network Infrastructure

Complete guide to running and managing Midnight Network infrastructure.

## Overview

Midnight Network infrastructure consists of:
- **Validators**: Participate in consensus, produce blocks
- **Indexers**: Index blockchain data for efficient queries
- **Nodes**: Full nodes that validate and relay transactions
- **Proof Servers**: Generate zero-knowledge proofs

## Quick Start

### Setup Validator
```bash
python scripts/setup-validator.py --config validator-config.yaml
```

### Setup Indexer
```bash
python scripts/setup-indexer.py --config indexer-config.yaml
```

### Health Check
```bash
python scripts/network-health-check.py
```

## Reference Guides

### Validator Operations
See [validator-guide.md](references/validator-guide.md) for:
- Running validators
- Consensus participation
- Staking requirements
- Rewards and slashing
- Best practices

### Indexer Setup
See [indexer-setup.md](references/indexer-setup.md) for:
- Indexer configuration
- Database setup
- Version compatibility (2.0.0 - 2.1.4)
- Performance tuning
- Maintenance

### Network Configuration
See [network-config.md](references/network-config.md) for:
- Network IDs (mainnet, testnet, preprod)
- Node endpoints
- Configuration parameters
- Substrate URI setup

### Monitoring
See [monitoring.md](references/monitoring.md) for:
- Health checks
- Performance metrics
- Troubleshooting
- Alerting
- Best practices

### Node Releases
See [node-releases.md](references/node-releases.md) for:
- Release notes
- Version compatibility
- Upgrade procedures
- Breaking changes

## Configuration Templates

Ready-to-use configs in `assets/configs/`:
- **validator-config.yaml**: Validator configuration
- **indexer-config.yaml**: Indexer configuration
- **node-config.yaml**: Node configuration

## Automation Scripts

### Setup Scripts
- `setup-validator.py`: Automated validator setup
- `setup-indexer.py`: Automated indexer setup

### Monitoring Scripts
- `network-health-check.py`: Check network status
- `monitor-validator.py`: Monitor validator performance

## Resources

- Validator Guide: https://docs.midnight.network/validate/run-a-validator
- Indexer Docs: https://docs.midnight.network/relnotes/midnight-indexer/
- Node Releases: https://docs.midnight.network/relnotes/node/

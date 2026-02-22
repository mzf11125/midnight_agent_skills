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

### Node Architecture
See [node-architecture.md](references/node-architecture.md) for:
- **Node types**: Full node, archive node, light client
- **Architecture components**: Substrate framework, partner chain bridge
- **Deployment patterns**: Single node, HA, validator, indexer
- **Configuration**: Node config, environment variables, CLI flags
- **Networking**: Port configuration, firewall rules, load balancing
- **Storage management**: Disk planning, pruning strategies
- **Monitoring**: Health checks, metrics, logging
- **Security**: Network isolation, key management, system hardening
- **Troubleshooting**: Common issues and solutions

### Docker Deployment
See [docker-deployment.md](references/docker-deployment.md) for:
- **Quick start**: Single node, Docker Compose
- **Image variants**: Official images, tags, network-specific
- **Production deployment**: Full node, archive node, validator
- **Multi-node setup**: HA cluster with load balancing
- **Indexer deployment**: Archive node + PostgreSQL + GraphQL
- **Monitoring stack**: Prometheus + Grafana
- **Environment configuration**: .env files, secrets
- **Management commands**: Start, stop, update, backup
- **Troubleshooting**: Container issues, resource limits
- **Security**: Version pinning, port binding, health checks

### Validator Operations
See [validator-guide.md](references/validator-guide.md) for:
- Running validators
- Consensus participation
- Staking requirements
- Rewards and slashing
- Best practices

### Indexer Setup
See [indexer-setup.md](references/indexer-setup.md) for:
- **Indexer v3.0.0** (current version - Jan 2026)
- Docker deployment (recommended)
- Database configuration
- GraphQL API v3 features
- Migration from v2.x (deprecated)
- Unshielded token support
- Performance tuning
- Troubleshooting

### Network Configuration
See [network-config.md](references/network-config.md) for:
- Network IDs (mainnet, testnet, preprod)
- Node endpoints
- Configuration parameters
- Substrate URI setup

### Monitoring & Troubleshooting
See [monitoring.md](references/monitoring.md) for:
- **Health checks**: Node, indexer, validator status
- **Prometheus metrics**: 20+ key metrics with queries
- **Grafana dashboards**: Node, validator, indexer panels
- **Logging**: Configuration, rotation, log levels, queries
- **Alerting**: 10+ alert rules with Slack/Email/PagerDuty
- **Common issues**: 6 detailed troubleshooting scenarios
- **Performance tuning**: Node and PostgreSQL optimization
- **Best practices**: Continuous monitoring, backups, updates

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

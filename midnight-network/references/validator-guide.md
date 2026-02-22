# Validator Guide

## Overview

Validators secure the Midnight Network by participating in consensus, producing blocks, and validating transactions.

## Requirements

### Hardware
- CPU: 4+ cores
- RAM: 16GB+
- Storage: 500GB+ SSD
- Network: 100Mbps+

### Software
- Midnight Node software
- Linux (Ubuntu 20.04+ recommended)
- Docker (optional)

### Stake
- Minimum stake required (check current network parameters)
- Stake locked during validation
- Slashing risk for misbehavior

## Setup

### 1. Install Node Software
```bash
wget https://releases.midnight.network/node-latest.tar.gz
tar -xzf node-latest.tar.gz
cd midnight-node
```

### 2. Generate Keys
```bash
./midnight-node keys generate --output validator-keys.json
```

### 3. Configure Node
Edit `config.yaml`:
```yaml
validator:
  enabled: true
  keys: validator-keys.json
  stake: 1000000
network:
  listen: 0.0.0.0:30333
  external: your-public-ip:30333
```

### 4. Start Validator
```bash
./midnight-node --config config.yaml
```

## Staking

### Stake Tokens
```bash
./midnight-node stake --amount 1000000
```

### Unstake
```bash
./midnight-node unstake
```
Note: Unstaking has a cooldown period.

## Monitoring

### Check Status
```bash
./midnight-node status
```

### View Logs
```bash
tail -f logs/validator.log
```

### Metrics
- Block production rate
- Missed blocks
- Peer connections
- Sync status

## Rewards

- Block rewards for producing blocks
- Transaction fees
- Distributed proportionally to stake
- Claimed automatically or manually

## Slashing

Validators can be slashed for:
- Double signing blocks
- Extended downtime
- Invalid block production

Slashing results in:
- Loss of staked tokens
- Temporary or permanent ban

## Best Practices

1. **High Availability**: Use redundant infrastructure
2. **Monitoring**: Set up alerts for downtime
3. **Security**: Secure validator keys, use firewalls
4. **Updates**: Keep node software up to date
5. **Backup**: Backup keys and configuration
6. **Testing**: Test on testnet first

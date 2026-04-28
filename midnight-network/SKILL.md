---
name: midnight-network
description: Guide to Midnight Network infrastructure, validators, indexers, and network operations. Use when users need to run Midnight validators and participate in consensus, set up and configure Midnight indexers for blockchain data, configure network nodes and infrastructure, monitor validator performance and network health, understand network parameters and configuration, deploy and manage network infrastructure, troubleshoot network issues, and access node release information and compatibility.
---

# Midnight Network Infrastructure

Complete guide to running and managing Midnight Network infrastructure.

## Infrastructure Overview

| Component | Purpose | Requirements |
|-----------|---------|------------|
| **Full Node** | Validate transactions, relay blocks | 4+ CPU, 8GB RAM, 100GB SSD |
| **Archive Node** | Full history storage | 4+ CPU, 16GB RAM, 1TB SSD |
| **Validator** | Produce blocks, consensus | 8+ CPU, 16GB RAM, 100GB SSD, stake |
| **Indexer** | Query API for DApps | 4+ CPU, 8GB RAM, 500GB SSD |
| **Proof Server** | Generate ZK proofs | 8+ CPU, 32GB RAM, GPU recommended |

## Quick Start

### Local Development (Recommended for DApps)

#### Option 1: midnight-local-dev (Full Local Network)

Provides complete local network with Node, Indexer, Proof Server:

```bash
git clone https://github.com/midnightntwrk/midnight-local-dev
cd midnight-local-dev
npm install
npm start
```

**Network ID**: `undeployed`

**Services & Ports**:

| Service | Port | URL |
|---------|------|-----|
| Node | 9944 | http://localhost:9944 |
| Indexer GraphQL | 8088 | http://localhost:8088/api/v4/graphql |
| Indexer WS | 8088 | ws://localhost:8088/api/v4/graphql/ws |
| Proof Server | 6300 | http://localhost:6300 |

**Docker Images**: node 0.22.3, indexer 4.0.1, proof-server 8.0.3

**Funding**: Use interactive menu to fund wallets with 50,000 tNIGHT each.

#### Standalone Mode (No Menu)

```bash
docker compose -f standalone.yml up -d
```

#### Option 2: midnight-wallet-cli
```bash
npx midnight-wallet-cli serve
```

#### Option 3: midnight-playground
- https://midnight-playground-one.vercel.app/

### Full Node Setup
```bash
# Using Docker (recommended)
docker run -d \
  --name midnight-node \
  -p 9933:9933 \
  -p 9944:9944 \
  -v midnight-data:/data \
  midnightnetwork/node:v0.12.0 \
  --network testnet-02 \
  --pruning archive
```

### Validator Setup
```bash
# See detailed guide below
# Requires staking tokens

docker run -d \
  --name midnight-validator \
  -p 9933:9933 \
  -p 9944:9944 \
  --restart unless-stopped \
  -v validator-data:/data \
  midnightnetwork/node:v0.12.0 \
  --validator \
  --staking <stake-address>
```

### Indexer Setup
```bash
# Using Docker Compose with PostgreSQL
# v4.0.0+ required

docker run -d \
  --name midnight-indexer \
  -p 3100:3100 \
  -e DATABASE_URL=postgresql://postgres:password@db:5432/indexer \
  -e NETWORK=testnet-02 \
  --link midnight-postgres:db \
  midnightnetwork/indexer:v4.0.0
```

## Node Architecture

### Node Types

1. **Full Node**
   - Validates all blocks and transactions
   - Stores current state
   - No historical queries
   - Minimum for DApp connection

2. **Archive Node**
   - Full history storage
   - Historical state queries
   - Recommended for indexer backend

3. **Light Client**
   - Lightweight verification
   - For resource-constrained environments
   - Trust minimum

### Node Ports

| Port | Protocol | Purpose |
|------|---------|---------|
| 9933 | HTTP | RPC API |
| 9944 | WebSocket | Subscriptions |
| 9615 | Prometheus | Metrics |

## Docker Deployment

### Single Node
```yaml
# docker-compose.yaml
version: '3.8'
services:
  node:
    image: midnightnetwork/node:v0.12.0
    ports:
      - "9933:9933"
      - "9944:9944"
    environment:
      - NETWORK=testnet-02
    volumes:
      - node-data:/data
    restart: unless-stopped
```

### Full Stack (Node + Indexer + PostgreSQL)
```yaml
version: '3.8'
services:
  node:
    image: midnightnetwork/node:v0.12.0
    ports:
      - "9933:9933"
    environment:
      - NETWORK=testnet-02
    volumes:
      - node-data:/data

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: indexer
    volumes:
      - postgres-data:/var/lib/postgresql/data

  indexer:
    image: midnightnetwork/indexer:v4.0.0
    ports:
      - "3100:3100"
    environment:
      - DATABASE_URL=postgresql://postgres:secret@postgres:5432/indexer
      - NETWORK=testnet-02
    depends_on:
      - postgres
      - node

volumes:
  node-data:
  postgres-data:
```

### Production Validator
```yaml
version: '3.8'
services:
  validator:
    image: midnightnetwork/node:v0.12.0
    ports:
      - "9933:9933"
      - "9944:9944"
    environment:
      - NETWORK=mainnet
      - VALIDATOR_MODE=true
      - STAKING_ADDRESS=<your-address>
    volumes:
      - validator-keys:/keys
      - validator-data:/data
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 16G
```

## Validator Operations

### Requirements

| Role | Stake Required | Hardware |
|------|-------------|---------|
| Full Validator | TBD | 8+ CPU, 16GB RAM |

### Setup Steps

1. **Generate Keys**
```bash
# Generate staking keypair
docker run --rm -v keys:/keys midnightnetwork/node:v0.12.0 \
  keygen --output /keys/stash
```

2. **Stake Tokens**
   - Transfer NIGHT to stake address
   - Delegate to validator (if using pool)

3. **Start Validator**
```bash
docker run -d \
  --name midnight-validator \
  -v keys:/keys \
  -e NETWORK=mainnet \
  -e VALIDATOR_KEY=stash.ss58 \
  midnightnetwork/node:v0.12.0 \
  --validator
```

4. **Monitor**

### Validator Commands

```bash
# Check status
curl -X POST http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"validator_key","id":1}'

# Get producing status
curl -X POST http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"validator_producing","id":1}'

# Manual key rotation
curl -X POST http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"validator_rotate","params":["newKey"],"id":1}'
```

## Indexer Setup (v4.0.0+)

### Docker Deployment
```bash
# Start PostgreSQL first
docker run -d \
  --name midnight-postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=indexer \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:15

# Start Indexer
docker run -d \
  --name midnight-indexer \
  -p 3100:3100 \
  -e DATABASE_URL=postgresql://postgres:secret@host:5432/indexer \
  -e NETWORK=testnet-02 \
  --link midnight-postgres:db \
  midnightnetwork/indexer:v4.0.0
```

### GraphQL API

Endpoint: `http://localhost:3100/graphql`

```graphql
# Query transactions
query {
  transactions(
    first: 10,
    after: "cursor"
  ) {
    edges {
      node {
        id
        hash
        block {
          height
        }
      }
    }
  }
}

# Query contracts
query {
  contracts(filter: { hasCode: true }) {
    nodes {
      address
      codeHash
    }
  }
}
```

## Monitoring

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `midnight_blocks_produced` | Counter | Total blocks produced |
| `midnight_transactions_total` | Counter | Total transactions |
| `midnight_peer_count` | Gauge | Connected peers |
| `midnight_block_height` | Gauge | Current height |
| `midnight_sync_status` | Gauge | Syncing (0/1) |

### Health Checks

```bash
# Node health
curl http://localhost:9933/health

# Indexer health
curl http://localhost:3100/health

# Prometheus metrics
curl http://localhost:9615/metrics
```

### Useful Queries
```promql
# Block production rate
rate(midnight_blocks_produced[5m])

# Transaction throughput
rate(midnight_transactions_total[5m])

# Peer count
midnight_peer_count

# Sync progress
midnight_block_height / ignoring (job) (max by (job) (midnight_block_height))
```

## Network Configuration

### Networks

| Network | Purpose | Chain ID | RPC URL | Status |
|---------|---------|---------|--------|--------|
| mainnet | Production | NIGHT | https://rpc.mainnet.midnight.network | Active |
| preprod | Testing | preprod | https://rpc.preprod.midnight.network | Active (use this) |
| preview | Early Dev | preview | https://rpc.preview.midnight.network | ⛔ Discontinued |
| testnet-02 | Integration | testnet-02 | - | ⛔ Discontinued |

**⚠️ Important**: Both Preview and Testnet-02 are **discontinued**. Use **Preprod** for all testing.

### Environment Variables

```bash
# Node
export MIDNIGHT_NETWORK=preprod
export MIDNIGHT_RPC_PORT=9933
export MIDNIGHT_WS_PORT=9944
export MIDNIGHT_PRUNING=archive

# Indexer
export DATABASE_URL=postgresql://user:pass@host:5432/midnight
export NETWORK=preprod
export PORT=3100
```

## Troubleshooting

### Common Issues

**Node not syncing**:
```bash
# Check sync status
curl -X POST http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"system_syncStatus","id":1}'

# Check peers
curl -X POST http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"system_peers","id":1}'
```

**Indexer not syncing**:
```bash
# Check indexer logs
docker logs midnight-indexer

# Check database connection
docker exec midnight-indexer psql -U postgres -c "SELECT 1"
```

**Validator not producing**:
```bash
# Verify keys
ls -la /keys/

# Check stake balance
curl -X POST http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"validator_key","id":1}'
```

## Developer Tools Reference

### From midnight-awesome-dapps

- [midnight-wallet-cli](https://github.com/nel349/midnight-wallet-cli-hub) - Terminal wallet + DApp server
- [Midnight Local Dev](https://github.com/midnightntwrk/midnight-local-dev) - Local full node
- [Midnight Local Playground](https://github.com/0xshae/midnight-playground) - Docker dev environment
- [Midnight MNN Helm](https://github.com/0xstrong/midnight-mnn-helm) - K8s deployment
- [NightGate](https://github.com/ODATANO/NIGHTGATE) - SAP CAP plugin
- [Pelagos SDK](https://github.com/0xAtelerix/sdk) - Go SDK for appchains
- [Midnight Live View](https://github.com/Midnight-Scripts/Midnight-Live-View) - Node monitoring

### Block Explorers

- [Midnight Explorer](https://www.midnightexplorer.com/) - TexLabs
- [Midnightscan](https://github.com/mediocrehacker/Midnightscan)

## Resources

- [Node Documentation](https://docs.midnight.network/nodes)
- [Full Node Setup](https://docs.midnight.network/nodes/full-node)
- [RPC Node Setup](https://docs.midnight.network/nodes/rpc-node)
- [Indexer Release Notes](https://docs.midnight.network/relnotes/midnight-indexer)
- [Node Release Notes](https://docs.midnight.network/relnotes/node)
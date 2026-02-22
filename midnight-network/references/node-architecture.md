# Node Architecture

## Overview

Midnight Network nodes are built on Substrate (Polkadot SDK) and implement a partner chain architecture connecting to Cardano. This document covers node types, architecture, and deployment patterns.

## Node Types

### Full Node

**Purpose**: Validate and relay transactions, maintain full blockchain state.

**Requirements**:
- **CPU**: 4+ cores
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: 500GB SSD (grows ~10GB/month)
- **Network**: 100 Mbps, stable connection
- **Ports**: 30333 (P2P), 9944 (WebSocket), 9933 (HTTP RPC)

**Use Cases**:
- DApp backends
- Private RPC endpoints
- Network participation
- Development/testing

**Capabilities**:
- Full transaction validation
- Block production (if validator)
- State queries
- Historical data (recent)

### Archive Node

**Purpose**: Store complete historical blockchain data.

**Requirements**:
- **CPU**: 8+ cores
- **RAM**: 32GB minimum, 64GB recommended
- **Storage**: 2TB+ SSD (grows ~40GB/month)
- **Network**: 1 Gbps recommended
- **Ports**: Same as full node

**Use Cases**:
- Indexers
- Block explorers
- Historical queries
- Analytics platforms

**Capabilities**:
- All full node features
- Complete historical state
- State at any block height
- Full event logs

### Light Client

**Purpose**: Minimal resource blockchain access.

**Requirements**:
- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 100MB
- **Network**: Any stable connection

**Use Cases**:
- Mobile wallets
- Browser extensions
- IoT devices
- Resource-constrained environments

**Capabilities**:
- Transaction submission
- Balance queries
- Block headers only
- Relies on full nodes for data

## Architecture Components

### Substrate Framework

Midnight nodes use Substrate (Polkadot SDK) for:
- **Consensus**: BABE (block production) + GRANDPA (finality)
- **Networking**: libp2p for P2P communication
- **Storage**: RocksDB for state and blocks
- **Runtime**: WebAssembly for upgradeable logic

```
┌─────────────────────────────────────┐
│         Midnight Runtime            │
│  (WebAssembly - Upgradeable)        │
├─────────────────────────────────────┤
│         Substrate Core              │
│  - Consensus (BABE/GRANDPA)         │
│  - Networking (libp2p)              │
│  - Storage (RocksDB)                │
│  - RPC (JSON-RPC)                   │
└─────────────────────────────────────┘
```

### Partner Chain Bridge

Connects Midnight to Cardano mainnet:
- **Cardano → Midnight**: Asset transfers, governance
- **Midnight → Cardano**: Finality proofs, state commitments
- **Security**: Inherits Cardano's security guarantees

```
┌──────────────┐         ┌──────────────┐
│   Cardano    │◄───────►│   Midnight   │
│   Mainnet    │  Bridge │  Partner     │
│              │         │  Chain       │
└──────────────┘         └──────────────┘
```

### Node Services

#### P2P Network Layer
- **Protocol**: libp2p
- **Discovery**: mDNS (local), Kademlia DHT (global)
- **Transport**: TCP, WebSocket, QUIC
- **Encryption**: Noise protocol

#### RPC Services
- **HTTP RPC**: Port 9933 (JSON-RPC 2.0)
- **WebSocket**: Port 9944 (subscriptions)
- **Methods**: State queries, transaction submission, subscriptions

#### Storage Layer
- **Database**: RocksDB
- **State Trie**: Patricia Merkle Trie
- **Pruning**: Configurable (full/archive)
- **Snapshots**: Periodic state snapshots

## Deployment Architectures

### Single Node (Development)

```
┌─────────────────────────┐
│    Developer Machine    │
│  ┌──────────────────┐   │
│  │  Midnight Node   │   │
│  │  (Full Node)     │   │
│  └──────────────────┘   │
└─────────────────────────┘
```

**Use**: Local development, testing

**Setup**:
```bash
docker run -p 9944:9944 -p 9933:9933 \
  ghcr.io/midnight-ntwrk/midnight:latest \
  --dev --rpc-external --ws-external
```

### High Availability (Production)

```
┌──────────────┐     ┌──────────────┐
│ Load         │     │ Load         │
│ Balancer     │────►│ Balancer     │
└──────┬───────┘     └──────┬───────┘
       │                    │
   ┌───┴────┐          ┌────┴───┐
   │ Node 1 │          │ Node 2 │
   └────────┘          └────────┘
       │                    │
   ┌───┴────┐          ┌────┴───┐
   │ Node 3 │          │ Node 4 │
   └────────┘          └────────┘
```

**Use**: Production DApps, high traffic

**Features**:
- Load balancing across nodes
- Automatic failover
- Geographic distribution
- Health monitoring

### Validator Setup

```
┌─────────────────────────────────┐
│      Validator Node             │
│  ┌──────────────────────────┐   │
│  │  Midnight Validator      │   │
│  │  - Block production      │   │
│  │  - Consensus voting      │   │
│  │  - Staking               │   │
│  └──────────────────────────┘   │
│                                  │
│  ┌──────────────────────────┐   │
│  │  Sentry Nodes (2+)       │   │
│  │  - DDoS protection       │   │
│  │  - P2P proxy             │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

**Use**: Network validators, block production

**Security**:
- Validator behind sentry nodes
- No public RPC endpoints
- Firewall rules
- Key management

### Indexer Architecture

```
┌──────────────┐
│ Archive Node │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   Indexer    │────►│  PostgreSQL  │
│   Service    │     │   Database   │
└──────┬───────┘     └──────────────┘
       │
       ▼
┌──────────────┐
│  GraphQL API │
└──────────────┘
```

**Use**: DApp data queries, analytics

**Components**:
- Archive node for historical data
- Indexer service for processing
- PostgreSQL for indexed data
- GraphQL API for queries

## Configuration

### Node Configuration File

**Location**: `config.toml`

```toml
[network]
listen_addresses = ["/ip4/0.0.0.0/tcp/30333"]
public_addresses = []
bootnodes = [
  "/dns/bootnode-1.midnight.network/tcp/30333/p2p/12D3KooW...",
  "/dns/bootnode-2.midnight.network/tcp/30333/p2p/12D3KooW..."
]

[rpc]
http_port = 9933
ws_port = 9944
cors = ["*"]
max_connections = 100

[storage]
database_path = "/data/chains/midnight/db"
pruning = "archive"  # or "256" for full node

[telemetry]
enabled = true
url = "wss://telemetry.midnight.network/submit"
```

### Environment Variables

```bash
# Network
MIDNIGHT_NETWORK=testnet
MIDNIGHT_CHAIN=midnight-testnet-02

# Ports
MIDNIGHT_P2P_PORT=30333
MIDNIGHT_RPC_PORT=9933
MIDNIGHT_WS_PORT=9944

# Storage
MIDNIGHT_DATA_DIR=/data/midnight
MIDNIGHT_PRUNING=archive

# Validator (if applicable)
MIDNIGHT_VALIDATOR=true
MIDNIGHT_VALIDATOR_KEY=/keys/validator.key
```

### Command Line Flags

```bash
# Full node
midnight-node \
  --chain testnet \
  --base-path /data \
  --rpc-port 9933 \
  --ws-port 9944 \
  --rpc-cors all \
  --pruning archive

# Validator
midnight-node \
  --chain testnet \
  --validator \
  --name "My Validator" \
  --base-path /data \
  --rpc-methods=unsafe \
  --ws-external=false
```

## Networking

### Port Configuration

| Port  | Protocol | Purpose              | Public |
|-------|----------|----------------------|--------|
| 30333 | TCP      | P2P networking       | Yes    |
| 9933  | HTTP     | RPC API              | No*    |
| 9944  | WS       | WebSocket RPC        | No*    |
| 9615  | HTTP     | Prometheus metrics   | No     |

*Only expose for public RPC nodes

### Firewall Rules

```bash
# Allow P2P
ufw allow 30333/tcp

# Restrict RPC (internal only)
ufw allow from 10.0.0.0/8 to any port 9933
ufw allow from 10.0.0.0/8 to any port 9944

# Allow monitoring
ufw allow from 10.0.0.0/8 to any port 9615
```

### Load Balancer Configuration

**Nginx example**:
```nginx
upstream midnight_rpc {
    least_conn;
    server node1:9933 max_fails=3 fail_timeout=30s;
    server node2:9933 max_fails=3 fail_timeout=30s;
    server node3:9933 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl;
    server_name rpc.mydapp.com;
    
    location / {
        proxy_pass http://midnight_rpc;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Storage Management

### Disk Space Planning

**Full Node**:
- Initial: ~50GB
- Growth: ~10GB/month
- Recommended: 500GB SSD

**Archive Node**:
- Initial: ~200GB
- Growth: ~40GB/month
- Recommended: 2TB+ SSD

### Pruning Strategies

**Archive Mode** (no pruning):
```bash
--pruning archive
```

**Full Node** (keep last 256 blocks):
```bash
--pruning 256
```

**Custom Pruning**:
```bash
--pruning 1000  # Keep last 1000 blocks
```

### Database Maintenance

```bash
# Compact database
midnight-node purge-chain --chain testnet

# Export state snapshot
midnight-node export-state --chain testnet --at <block-hash>

# Import state snapshot
midnight-node import-state --chain testnet snapshot.json
```

## Monitoring

### Health Checks

```bash
# Check node health
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_health"}'

# Response
{
  "jsonrpc": "2.0",
  "result": {
    "peers": 50,
    "isSyncing": false,
    "shouldHavePeers": true
  }
}
```

### Metrics

**Prometheus endpoint**: `http://localhost:9615/metrics`

**Key metrics**:
- `substrate_block_height`: Current block height
- `substrate_peers_count`: Connected peers
- `substrate_sync_status`: Sync state
- `substrate_database_size`: Database size

### Logging

```bash
# Set log level
RUST_LOG=info,midnight=debug midnight-node

# Log to file
midnight-node 2>&1 | tee /var/log/midnight/node.log
```

## Security Best Practices

### 1. Network Isolation

```bash
# Validator: No public RPC
--rpc-external=false
--ws-external=false

# Use sentry nodes for P2P
--reserved-only
--reserved-nodes /ip4/sentry1/tcp/30333/p2p/...
```

### 2. Key Management

```bash
# Generate validator keys
midnight-node key generate --scheme Sr25519

# Store securely
chmod 600 /keys/validator.key
chown midnight:midnight /keys/validator.key
```

### 3. System Hardening

```bash
# Run as non-root user
useradd -m -s /bin/bash midnight

# Limit resources
systemctl edit midnight-node
[Service]
LimitNOFILE=65536
LimitNPROC=4096
```

### 4. Monitoring & Alerts

```bash
# Monitor sync status
watch -n 10 'curl -s http://localhost:9933 -H "Content-Type: application/json" \
  -d "{\"id\":1, \"jsonrpc\":\"2.0\", \"method\":\"system_health\"}"'

# Alert on peer count drop
if [ $(peers_count) -lt 10 ]; then
  alert "Low peer count"
fi
```

## Upgrade Procedures

### Runtime Upgrade (Automatic)

Substrate supports forkless upgrades:
1. Governance proposal passes
2. Runtime upgrade scheduled
3. Nodes automatically apply at target block
4. No node restart required

### Node Binary Upgrade

```bash
# 1. Download new binary
wget https://github.com/midnight-ntwrk/midnight/releases/download/v2.0.0/midnight-node

# 2. Stop node
systemctl stop midnight-node

# 3. Backup database
cp -r /data/midnight /backup/midnight-$(date +%Y%m%d)

# 4. Replace binary
mv midnight-node /usr/local/bin/
chmod +x /usr/local/bin/midnight-node

# 5. Start node
systemctl start midnight-node

# 6. Verify
journalctl -u midnight-node -f
```

## Troubleshooting

### Node Won't Sync

```bash
# Check peers
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_peers"}'

# Add bootnodes
--bootnodes /dns/bootnode-1.midnight.network/tcp/30333/p2p/...

# Reset database
midnight-node purge-chain --chain testnet
```

### High Memory Usage

```bash
# Check database size
du -sh /data/midnight/chains/*/db

# Enable pruning
--pruning 256

# Increase swap
fallocate -l 8G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

### RPC Connection Issues

```bash
# Check if RPC is listening
netstat -tlnp | grep 9933

# Test RPC
curl http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_chain"}'

# Check CORS settings
--rpc-cors all
```

## Resources

- **Validator Guide**: See validator-guide.md
- **Docker Deployment**: See docker-deployment.md
- **Monitoring**: See monitoring.md
- **Indexer Setup**: See indexer-setup.md
- **Substrate Docs**: https://docs.substrate.io

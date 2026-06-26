# Diagnostics

## Overview

The diagnostic tooling verifies that your Midnight development environment is correctly configured and all services are reachable. Run diagnostics before starting development after environment changes or when troubleshooting unexpected behavior.

## Version Checking

```bash
npx @midnight-ntwrk/midnight-local-dev --version
npx @midnight-ntwrk/compactc --version
docker --version
docker compose version
node --version
npm --version
```

Minimum requirements: Docker Engine 24.0 Docker Compose v2 Node.js 18. Older Node.js versions cause missing WebCrypto API errors.

## Dependency Validation

```bash
npm ls @midnight-ntwrk/wallet-sdk-facade
npm ls @midnight-ntwrk/midnight-js
npm ls @midnight-ntwrk/dapp-connector-api
npm ls --depth=0 | grep midnight
```

Each command should show the installed version without errors. Mixing major versions across Midnight packages causes runtime type errors.

## Network Connectivity Tests

### Node Connectivity

```bash
curl -s http://localhost:9944
curl -s https://rpc.preprod.midnight.network/health
```

A 200 response confirms connectivity.

### Indexer Connectivity

```bash
curl -s http://localhost:32888/api/graphql \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { name } } }"}'
```

A successful response contains the GraphQL schema. An error means the indexer is not running.

### Indexer WebSocket

```bash
wscat -c ws://localhost:32888/api/graphql/ws
```

## Proof Server Health Checks

```bash
# Basic health
curl -s http://localhost:6300/health

# Available circuits
curl -s http://localhost:6300/circuits

# Detailed status (queue length, memory, avg proof time)
curl -s http://localhost:6300/status
```

If your contract circuit is not listed upload artifacts using the proof server API.

## Indexer Health Checks

```bash
# Sync status
curl -s http://localhost:32888/api/graphql \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ syncStatus { synced lag latestBlock } }"}'

# Block height
curl -s http://localhost:32888/api/graphql \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ health { status blockHeight } }"}'
```

When `synced` is true and `lag` is 0 the indexer is fully caught up.

## Node Sync Status

```bash
# Block production
curl -s http://localhost:9933 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"system_syncState","params":[],"id":1}'

# Peer count
curl -s http://localhost:9933 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"system_peers","params":[],"id":1}'
```

No peers on a public network means P2P connectivity is blocked.

## Faucet Availability Checks

```bash
curl -s https://faucet.preprod.midnight.network/health

curl -s https://faucet.preprod.midnight.network/request \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"address":"mn_addr1..."}'
```

## Environment Validation

Supported: Linux (Ubuntu 20.04+) macOS 13+ Windows via WSL2.

```bash
uname -a
df -h .     # 20 GB min local devnet, 50 GB for full node
free -h     # 8 GB min local devnet, 16 GB for indexer + prover
nproc       # 4 cores recommended
```

## Doctor Command

Runs all diagnostics and produces a report:

```bash
npx @midnight-ntwrk/midnight-local-dev doctor
```

Checks performed: tool versions dependencies Docker containers network proof server indexer and environment. Each returns PASS WARN or FAIL with remediation steps.

## Report Generation

### Markdown

```bash
npx @midnight-ntwrk/midnight-local-dev doctor --format markdown > diagnostics.md
```

### JSON (CI compatible)

```bash
npx @midnight-ntwrk/midnight-local-dev doctor --format json > diagnostics.json
```

Example output:

```json
{
  "results": [
    { "check": "docker-version", "status": "pass", "message": "Docker 26.1.0" },
    { "check": "proof-server-health", "status": "fail",
      "message": "Proof server not responding on port 6300",
      "remediation": "Run: npx @midnight-ntwrk/midnight-local-dev restart" }
  ],
  "summary": { "pass": 6, "warn": 1, "fail": 1, "total": 8 }
}
```

## CI Integration

```yaml
name: Midnight Environment Check
on: [push, pull_request]
jobs:
  diagnostics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx @midnight-ntwrk/midnight-local-dev start --wait
      - run: npx @midnight-ntwrk/midnight-local-dev doctor --format json > diagnostics.json
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: diagnostics, path: diagnostics.json }
      - run: npx @midnight-ntwrk/midnight-local-dev stop
        if: always()
```

`--wait` blocks until all containers report healthy. `if: always()` ensures cleanup even on failure.

## Resources

- **Local Devnet**: See local-devnet.md
- **Provider Architecture**: See ../midnight-dapp-dev/references/provider-architecture.md

# Local Devnet

**Tool**: `@midnight-ntwrk/midnight-local-dev`

## Overview

The local devnet runs a complete Midnight Network stack using Docker Compose. It includes a node for block production an indexer for state queries and a proof server for ZK proof generation. This is the primary development environment before deploying to Preprod or Mainnet.

## Prerequisites

- Docker Engine 24.0 or later
- Docker Compose v2
- At least 8 GB RAM for containers
- At least 20 GB free disk
- Node.js 18 or later

## midnight local dev Tool

```bash
npx @midnight-ntwrk/midnight-local-dev start
npx @midnight-ntwrk/midnight-local-dev stop
npx @midnight-ntwrk/midnight-local-dev status
npx @midnight-ntwrk/midnight-local-dev logs
```

The first `start` downloads Docker images. Subsequent starts are faster.

## Stack Components

### Node

```yaml
midnight-node:
  image: ghcr.io/midnight-ntwrk/midnight-node:latest
  ports:
    - "9944:9944"
  command:
    - --dev
    - --rpc-external
    - --ws-external
```

In dev mode blocks are produced on demand rather than at fixed intervals.

### Indexer

```yaml
indexer:
  image: ghcr.io/midnight-ntwrk/indexer:latest
  ports:
    - "32888:32888"
  depends_on:
    midnight-node:
      condition: service_healthy
    postgres:
      condition: service_healthy
```

### Proof Server

```yaml
proof-server:
  image: ghcr.io/midnight-ntwrk/proof-server:latest
  ports:
    - "6300:6300"
  depends_on:
    midnight-node:
      condition: service_healthy
```

## Container Orchestration

Startup order: PostgreSQL -> Node -> Indexer & Proof Server (parallel).

## Health Checks

| Service | Endpoint | Healthy When |
|---------|----------|-------------|
| PostgreSQL | `pg_isready` | Exit code 0 |
| Node | `http://localhost:9933/health` | HTTP 200 |
| Indexer | GraphQL introspection | Returns schema |
| Proof Server | `http://localhost:6300/health` | `{"status":"ok"}` |

```bash
curl http://localhost:9933/health
curl http://localhost:6300/health
```

## Service Discovery

| Service | Protocol | Host | Port |
|---------|----------|------|------|
| Node RPC | WebSocket | localhost | 9944 |
| Node HTTP | HTTP | localhost | 9933 |
| Indexer GraphQL | HTTP | localhost | 32888 |
| Indexer WebSocket | WebSocket | localhost | 32888 |
| Proof Server | HTTP | localhost | 6300 |
| PostgreSQL | TCP | localhost | 5432 |

## Port Management

```bash
export MIDNIGHT_NODE_WS_PORT=19944
export MIDNIGHT_INDEXER_PORT=42888
export MIDNIGHT_PROVER_PORT=16300
npx @midnight-ntwrk/midnight-local-dev start
```

## LocalTestConfiguration

```typescript
interface LocalTestConfiguration {
  indexerUri: string;
  indexerWsUri: string;
  proofServerUri: string;
  nodeUri: string;
  networkId: string;
}

const localConfig: LocalTestConfiguration = {
  indexerUri: 'http://localhost:32888/api/graphql',
  indexerWsUri: 'ws://localhost:32888/api/graphql/ws',
  proofServerUri: 'http://localhost:6300',
  nodeUri: 'ws://localhost:9944',
  networkId: 'undeployed',
};
```

## LocalTestEnvironment

Wraps configuration with lifecycle management:

```typescript
interface LocalTestEnvironment {
  config: LocalTestConfiguration;
  start(): Promise<void>;
  stop(): Promise<void>;
  isHealthy(): Promise<boolean>;
}
```

## Container Endpoints

**Node RPC**:
```typescript
import { ApiPromise, WsProvider } from '@polkadot/api';
const api = await ApiPromise.create({ provider: new WsProvider('ws://localhost:9944') });
```

**Indexer GraphQL**:
```typescript
const resp = await fetch('http://localhost:32888/api/graphql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: '{ blocks(first:10) { nodes { height } } }' }),
});
```

**Proof Server**:
```typescript
const resp = await fetch('http://localhost:6300/prove', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ circuit: 'my_contract', witness: witnessData }),
});
```

## Authentication

The local devnet runs without authentication. All endpoints are accessible without tokens. Never expose the local devnet to the internet.

## getTestEnvironment

Auto detects whether the local devnet is running:

```typescript
import { getTestEnvironment } from '@midnight-ntwrk/midnight-js-testkit';

const env = await getTestEnvironment();
const config = env === 'local' ? localConfig : preprodConfig;
const providers = await initializeMidnightProviders(config);
```

## Resources

- **Diagnostics**: See diagnostics.md
- **Provider Architecture**: See ../midnight-dapp-dev/references/provider-architecture.md

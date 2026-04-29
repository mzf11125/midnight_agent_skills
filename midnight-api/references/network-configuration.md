# Network Configuration

## Overview

Proper network configuration is **critical** for all Midnight APIs. All APIs require `setNetworkId()` to be called before any operations.

## Network IDs

### Available Networks

#### Mainnet (Production)
```typescript
NetworkId('mainnet')
```
- **Status**: Not yet launched
- **Purpose**: Production network
- **Use**: Real transactions, real value

#### Preprod (Pre-production)
```typescript
NetworkId('preprod')
```
- **Status**: Active
- **Purpose**: Final testing before mainnet
- **Use**: Testing with mainnet-like conditions

#### Preprod (Development)
```typescript
NetworkId('preprod')
```
- **Status**: Active
- **Purpose**: Development and testing
- **Use**: Development, experimentation, testing
- **Faucet**: Available for test tokens

## Required Configuration

### ⚠️ CRITICAL: Set Network ID First

**All APIs fail without proper network configuration.**

### Compact Runtime API
```typescript
import { setNetworkId, NetworkId } from '@midnight-ntwrk/compact-runtime';

// MUST be called before any operations
setNetworkId(NetworkId('preprod'));

// Now safe to use runtime functions
const hash = transientHash(data);
```

### ZSwap API
```typescript
import { setNetworkId, NetworkId } from '@midnight/zswap';

// MUST be called before creating transactions
setNetworkId(NetworkId('preprod'));

// Now safe to create offers
const offer = new Offer(...);
```

### Ledger API
```typescript
import { setNetworkId, NetworkId } from '@midnight-ntwrk/ledger';

// MUST be called before transaction assembly
setNetworkId(NetworkId('preprod'));

// Now safe to create transactions
const tx = new UnprovenTransaction(...);
```

### DApp Connector API
```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

// Network ID passed to connect()
const connectedAPI = await window.midnight.wallet.connect(
  NetworkId('preprod')
);
```

## Network-Specific Configuration

### Preprod

#### Node Endpoints
```typescript
const config = {
  nodeRpcUrl: 'https://rpc.preprod.midnight.network',
  nodeWsUrl: 'wss://ws.preprod.midnight.network',
  indexerUri: 'https://indexer.preprod.midnight.network',
  indexerWsUri: 'wss://indexer-ws.preprod.midnight.network',
  proverServerUri: 'https://prover.preprod.midnight.network'
};
```

#### Chain Specification
```bash
--chain=/res/preprod/preprodRaw.json
```

#### Configuration Preset
```bash
CFG_PRESET="preprod"
```

### Preprod

#### Node Endpoints
```typescript
const config = {
  nodeRpcUrl: 'https://rpc.preprod.midnight.network',
  nodeWsUrl: 'wss://ws.preprod.midnight.network',
  indexerUri: 'https://indexer.preprod.midnight.network',
  indexerWsUri: 'wss://indexer-ws.preprod.midnight.network',
  proverServerUri: 'https://prover.preprod.midnight.network'
};
```

### Mainnet (When Available)

#### Node Endpoints
```typescript
const config = {
  nodeRpcUrl: 'https://rpc.mainnet.midnight.network',
  nodeWsUrl: 'wss://ws.mainnet.midnight.network',
  indexerUri: 'https://indexer.mainnet.midnight.network',
  indexerWsUri: 'wss://indexer-ws.mainnet.midnight.network',
  proverServerUri: 'https://prover.mainnet.midnight.network'
};
```

## DApp Configuration Pattern

### Respect User's Configuration

**CRITICAL**: DApps MUST use the user's configured services for privacy.

```typescript
// Get user's configured services from wallet
const connectedAPI = await window.midnight.wallet.connect(networkId);
const config = await connectedAPI.getConfiguration();

// Use user's services (REQUIRED for privacy)
const indexer = new IndexerClient(config.indexerUri);
const prover = new ProverClient(config.proverServerUri);
const node = new NodeClient(config.substrateNodeUri);

// Verify network matches
console.assert(config.networkId === networkId);
```

### Why This Matters

Users configure their own:
- Indexer (for query privacy)
- Prover server (for proof generation privacy)
- Node (for transaction submission privacy)

**Using hardcoded endpoints violates user privacy.**

## Common Errors

### Network ID Not Set
```
Error: Network ID not configured
```
**Cause**: `setNetworkId()` not called  
**Solution**: Call `setNetworkId()` before any API operations

```typescript
// ❌ WRONG - will fail
const hash = transientHash(data);

// ✅ CORRECT
setNetworkId(NetworkId('preprod'));
const hash = transientHash(data);
```

### Network Mismatch
```
Error: Network ID mismatch
```
**Cause**: Different network IDs used across APIs  
**Solution**: Use same network ID consistently

```typescript
// ❌ WRONG - inconsistent
setNetworkId(NetworkId('preprod')); // Runtime
await wallet.connect(NetworkId('preprod')); // Wallet

// ✅ CORRECT - consistent
const networkId = NetworkId('preprod');
setNetworkId(networkId); // Runtime
await wallet.connect(networkId); // Wallet
```

### Wrong Network
```
Error: Transaction rejected - wrong network
```
**Cause**: Transaction created for different network  
**Solution**: Verify network ID matches target network

## Environment-Based Configuration

### Development Setup
```typescript
// .env.development
VITE_NETWORK_ID=preprod
VITE_NODE_RPC=https://rpc.preprod.midnight.network
VITE_INDEXER_URI=https://indexer.preprod.midnight.network

// config.ts
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

export const config = {
  networkId: NetworkId(import.meta.env.VITE_NETWORK_ID),
  nodeRpcUrl: import.meta.env.VITE_NODE_RPC,
  indexerUri: import.meta.env.VITE_INDEXER_URI
};
```

### Production Setup
```typescript
// .env.production
VITE_NETWORK_ID=mainnet
VITE_NODE_RPC=https://rpc.mainnet.midnight.network
VITE_INDEXER_URI=https://indexer.mainnet.midnight.network
```

## Node Configuration

### Docker Environment Variables
```bash
docker run \
  -e CFG_PRESET="preprod" \
  -e POSTGRES_HOST="postgres" \
  midnightnetwork/midnight-node:latest \
  --chain=/res/preprod/preprodRaw.json
```

### Full Node Configuration
```yaml
# node-config.yaml
network:
  id: preprod
  chain_spec: /res/preprod/preprodRaw.json

database:
  host: localhost
  port: 5432
  name: midnight_node
```

## Testing Across Networks

### Multi-Network Testing
```typescript
describe('Cross-network tests', () => {
  const networks = ['preprod', 'preprod'] as const;
  
  networks.forEach(network => {
    it(`should work on ${network}`, async () => {
      setNetworkId(NetworkId(network));
      
      // Test logic here
      const result = await someOperation();
      expect(result).toBeDefined();
    });
  });
});
```

## Best Practices

### 1. Set Network ID Early
```typescript
// ✅ Set at app initialization
function initializeApp() {
  const networkId = NetworkId('preprod');
  setNetworkId(networkId);
  
  // Now safe to use APIs
  startApp();
}
```

### 2. Use Environment Variables
```typescript
// ✅ Configure via environment
const networkId = NetworkId(process.env.NETWORK_ID || 'preprod');
setNetworkId(networkId);
```

### 3. Validate Configuration
```typescript
// ✅ Verify configuration
async function validateConfig() {
  const connectedAPI = await wallet.connect(networkId);
  const config = await connectedAPI.getConfiguration();
  
  if (config.networkId !== networkId) {
    throw new Error('Network ID mismatch');
  }
}
```

### 4. Respect User Settings
```typescript
// ✅ Always use user's configured services
const config = await connectedAPI.getConfiguration();
const indexer = new IndexerClient(config.indexerUri);
// NOT: const indexer = new IndexerClient('https://my-indexer.com');
```

## Resources

- Network Status: https://status.midnight.network
- Preprod Faucet: https://faucet.preprod.midnight.network
- Node Endpoints: https://docs.midnight.network/nodes/node-endpoints
- DApp Connector: https://docs.midnight.network/api-reference/dapp-connector

---

## SDK Compatibility & Silent Failures

> Source: "Surviving Midnight SDK: a 700-line cure for the silent failure problem" — Fred Santana, Midnight Aliit

Midnight SDK moves fast. Version mismatches produce **silent failures** — no error, no timeout, just a hung process.

### Known compatibility matrix (as of April 2026)

| Track | `wallet-sdk-facade` | `midnight-node` | `indexer-standalone` | `proof-server` |
|---|---|---|---|---|
| Current | 4.0.0 | 0.21.0 | 4.0.0-rc.4 | 7.0.0 |
| Preprod-3x (legacy) | 2.0.0 | 0.21.0 | 4.0.0-rc.4 | 7.0.0 |

### Critical known issue: `WalletFacade.init()` hangs on standalone node (facade 2.x)

`WalletFacade.init({...})` in SDK 2.x wires sync to `subscribeRuntimeVersion`. The standalone dev node closes that subscription early. Result: wallet sits in `syncing` state forever with **zero error output**.

```typescript
// This will hang silently with facade 2.x + standalone node
await wallet.waitForSyncedState();
console.log('synced!');  // never prints
```

**Fix:** Either develop against preprod, or upgrade to `wallet-sdk-facade@4.0.0` which reverted to `new WalletFacade(...) + .start()` pattern.

### API change: facade 2.x → 4.x migration

```typescript
// facade 2.x (removed in 4.x)
const wallet = await WalletFacade.init({ configuration, shielded, unshielded, dust });

// facade 4.x
const wallet = new WalletFacade(shielded, unshielded, dust);
await wallet.start();
```

### Other common silent failures

| Symptom | Root cause | Fix |
|---|---|---|
| `waitForSyncedState()` hangs | facade 2.x + standalone node | Upgrade to facade 4.x or use preprod |
| `npm install` ENOTFOUND | `.npmrc` pointing at `npm.midnight.network` (doesn't exist) | Remove custom registry from `.npmrc` |
| Transactions silently fail | Duplicate `@midnight-ntwrk/ledger-v7` in `node_modules` | Run `npm dedupe` |
| Indexer crash-loops | `indexer.yml` missing `subscription:` block | Add `subscription:` block to config |

### Pre-flight check tool

Run `npx midnight-doctor` before debugging. It cross-references your `package.json`, running Docker containers, and config files against the compatibility matrix and surfaces mismatches in seconds.

```bash
npx midnight-doctor
```

Repo: https://github.com/fredericosanntana/midnight-doctor

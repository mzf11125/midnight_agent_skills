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

#### Testnet-02 (Development)
```typescript
NetworkId('testnet-02')
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
setNetworkId(NetworkId('testnet-02'));

// Now safe to use runtime functions
const hash = transientHash(data);
```

### ZSwap API
```typescript
import { setNetworkId, NetworkId } from '@midnight/zswap';

// MUST be called before creating transactions
setNetworkId(NetworkId('testnet-02'));

// Now safe to create offers
const offer = new Offer(...);
```

### Ledger API
```typescript
import { setNetworkId, NetworkId } from '@midnight-ntwrk/ledger';

// MUST be called before transaction assembly
setNetworkId(NetworkId('testnet-02'));

// Now safe to create transactions
const tx = new UnprovenTransaction(...);
```

### DApp Connector API
```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

// Network ID passed to connect()
const connectedAPI = await window.midnight.wallet.connect(
  NetworkId('testnet-02')
);
```

## Network-Specific Configuration

### Testnet-02

#### Node Endpoints
```typescript
const config = {
  nodeRpcUrl: 'https://rpc.testnet.midnight.network',
  nodeWsUrl: 'wss://ws.testnet.midnight.network',
  indexerUri: 'https://indexer.testnet.midnight.network',
  indexerWsUri: 'wss://indexer-ws.testnet.midnight.network',
  proverServerUri: 'https://prover.testnet.midnight.network'
};
```

#### Chain Specification
```bash
--chain=/res/testnet-02/testnetRaw.json
```

#### Configuration Preset
```bash
CFG_PRESET="testnet-02"
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
setNetworkId(NetworkId('testnet-02'));
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
setNetworkId(NetworkId('testnet-02')); // Runtime
await wallet.connect(NetworkId('preprod')); // Wallet

// ✅ CORRECT - consistent
const networkId = NetworkId('testnet-02');
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
VITE_NETWORK_ID=testnet-02
VITE_NODE_RPC=https://rpc.testnet.midnight.network
VITE_INDEXER_URI=https://indexer.testnet.midnight.network

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
  -e CFG_PRESET="testnet-02" \
  -e POSTGRES_HOST="postgres" \
  midnightnetwork/midnight-node:latest \
  --chain=/res/testnet-02/testnetRaw.json
```

### Full Node Configuration
```yaml
# node-config.yaml
network:
  id: testnet-02
  chain_spec: /res/testnet-02/testnetRaw.json

database:
  host: localhost
  port: 5432
  name: midnight_node
```

## Testing Across Networks

### Multi-Network Testing
```typescript
describe('Cross-network tests', () => {
  const networks = ['testnet-02', 'preprod'] as const;
  
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
  const networkId = NetworkId('testnet-02');
  setNetworkId(networkId);
  
  // Now safe to use APIs
  startApp();
}
```

### 2. Use Environment Variables
```typescript
// ✅ Configure via environment
const networkId = NetworkId(process.env.NETWORK_ID || 'testnet-02');
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
- Testnet Faucet: https://faucet.testnet.midnight.network
- Node Endpoints: https://docs.midnight.network/nodes/node-endpoints
- DApp Connector: https://docs.midnight.network/api-reference/dapp-connector

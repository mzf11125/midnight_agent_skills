# DApp Connector API Reference

**Package**: `@midnight-ntwrk/dapp-connector-api v4.0.0`

## Overview

The DApp Connector API enables decentralized applications to connect to Midnight wallets, request wallet information, create transactions, and interact with the Midnight Network.

## Installation

```bash
yarn add @midnight-ntwrk/dapp-connector-api
```

## Initial API Structure

### Window Injection Pattern

Wallets inject their API at:
```typescript
window.midnight.{walletId}
```

Multiple wallets can coexist without conflicts.

### InitialAPI Properties

```typescript
interface InitialAPI {
  name: string;           // Wallet display name
  icon: string;           // Icon URL (base64 or hosted)
  apiVersion: string;     // Semver version (e.g., "4.0.0")
  connect(networkId: NetworkId): Promise<ConnectedAPI>;
}
```

### Example: Get Wallet Info
```typescript
// Before connection
const walletName = window.midnight.lace.name;
const walletIcon = window.midnight.lace.icon;
const version = window.midnight.lace.apiVersion;

console.log(`${walletName} v${version}`);
```

## Connecting to Wallet

### Basic Connection
```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

const connectedAPI = await window.midnight.lace.connect(
  NetworkId('testnet-02')
);
```

### Connection with Version Check
```typescript
import semver from 'semver';

// Filter compatible wallets
const compatibleWallets = Object.values(window.midnight ?? {})
  .filter(wallet => semver.satisfies(wallet.apiVersion, '^4.0.0'));

if (compatibleWallets.length === 0) {
  throw new Error('No compatible wallets found');
}

// Let user select
const selectedWallet = await askUserToSelect(compatibleWallets);
const connectedAPI = await selectedWallet.connect(NetworkId('testnet-02'));
```

### Verify Connection
```typescript
const status = await connectedAPI.getConnectionStatus();
console.assert(status.networkId === NetworkId('testnet-02'));
```

## ConnectedAPI Methods

### Configuration

#### getConfiguration()
```typescript
const config = await connectedAPI.getConfiguration();

// Returns:
{
  indexerUri: string;        // HTTP endpoint
  indexerWsUri: string;      // WebSocket endpoint
  proverServerUri: string;   // Proof generation service
  substrateNodeUri: string;  // Node RPC endpoint
  networkId: NetworkId;      // Connected network
}
```

**CRITICAL**: Always use user's configured services for privacy.

```typescript
// ✅ CORRECT - respect user's privacy
const indexer = new IndexerClient(config.indexerUri);

// ❌ WRONG - violates user privacy
const indexer = new IndexerClient('https://my-indexer.com');
```

### State Queries

#### getShieldedBalances()
```typescript
const balances = await connectedAPI.getShieldedBalances();
// Returns: Record<TokenType, bigint>

// Example:
{
  "night_token": 1000000000n,  // 1000 NIGHT
  "custom_token": 500000n
}
```

#### getUnshieldedBalances()
```typescript
const balances = await connectedAPI.getUnshieldedBalances();
// Returns: Record<TokenType, bigint>
```

#### getDustBalance()
```typescript
const dust = await connectedAPI.getDustBalance();
// Returns: bigint
```

#### getShieldedAddresses()
```typescript
const addresses = await connectedAPI.getShieldedAddresses();
// Returns: { shieldedAddress: string }  // Bech32m format

// Example:
{
  shieldedAddress: "mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3"
}
```

#### getUnshieldedAddress()
```typescript
const address = await connectedAPI.getUnshieldedAddress();
// Returns: string (Bech32m format)
```

#### getDustAddress()
```typescript
const address = await connectedAPI.getDustAddress();
// Returns: string (Bech32m format)
```

#### getConnectionStatus()
```typescript
const status = await connectedAPI.getConnectionStatus();
// Returns: { networkId: NetworkId, connected: boolean }
```

### Transaction Operations

#### makeTransfer(outputs: InitActions[])

Create a payment transaction.

```typescript
import { nativeToken } from '@midnight-ntwrk/ledger';

const tx = await connectedAPI.makeTransfer([
  {
    kind: 'unshielded',
    tokenType: nativeToken().raw,
    value: 10_000_000n,  // 10 NIGHT
    recipient: 'mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3'
  }
]);
```

**InitActions Type**:
```typescript
type InitActions = {
  kind: 'shielded' | 'unshielded';
  tokenType: TokenType;
  value: bigint;
  recipient: Address;  // Bech32m format
};
```

**Multiple outputs**:
```typescript
const tx = await connectedAPI.makeTransfer([
  { kind: 'unshielded', tokenType: NIGHT, value: 10n, recipient: addr1 },
  { kind: 'shielded', tokenType: NIGHT, value: 5n, recipient: addr2 }
]);
```

#### makeIntent(inputs: InitActions[], outputs: InitActions[])

Create unbalanced transaction for swaps.

```typescript
// Party 1: Offer 10 NIGHT for 50,000 FOO tokens
const tx = await connectedAPI.makeIntent(
  [{ kind: 'unshielded', tokenType: NIGHT, value: 10_000_000n }],  // Surplus
  [{ kind: 'shielded', tokenType: FOO, value: 50_000n, recipient: myAddress }]  // Shortage
);

// Transaction has:
// - Surplus of 10 NIGHT (inputs > outputs)
// - Shortage of 50,000 FOO (outputs > inputs)
```

#### balanceSealedTransaction(tx: Transaction)

Balance a sealed transaction (e.g., from swap).

```typescript
const balancedTx = await connectedAPI.balanceSealedTransaction(tx);
// Returns: { tx: Transaction }
```

**Use for**:
- Completing swaps initiated by `makeIntent`
- Transactions from other parties

#### balanceUnsealedTransaction(tx: Transaction)

Balance an unsealed transaction (e.g., from contract call).

```typescript
const balancedTx = await connectedAPI.balanceUnsealedTransaction(tx);
// Returns: { tx: Transaction }
```

**Use for**:
- Contract call transactions
- Adding fees to user-created transactions

#### submitTransaction(tx: Transaction)

Submit transaction to network.

```typescript
const result = await connectedAPI.submitTransaction(tx);
// Returns: { txHash: string }
```

#### getProvingProvider(keyMaterialProvider: ZkConfigProvider)

Get proving provider for delegated proof generation.

```typescript
import { FetchZkConfigProvider } from '@midnight-ntwrk/midnight-js-fetch-zk-config-provider';

const keyMaterialProvider = new FetchZkConfigProvider('https://example.com');
const provingProvider = connectedAPI.getProvingProvider(keyMaterialProvider);

// Use for proof generation
const provenTx = await unprovenTx.prove(provingProvider, costModel);
```

## Complete Examples

### Example 1: Connect to Wallet

```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

async function connectWallet(): Promise<ConnectedAPI> {
  const networkId = NetworkId('testnet-02');
  
  // Filter compatible wallets
  const compatibleWallets = Object.values(window.midnight ?? {})
    .filter(wallet => {
      const version = wallet.apiVersion;
      return semver.satisfies(version, '^4.0.0');
    });
  
  if (compatibleWallets.length === 0) {
    throw new Error('No compatible Midnight wallets found');
  }
  
  // User selects wallet
  const selectedWallet = await askUserToSelect(compatibleWallets);
  
  // Connect
  const connectedAPI = await selectedWallet.connect(networkId);
  
  // Verify
  const status = await connectedAPI.getConnectionStatus();
  console.assert(status.networkId === networkId);
  
  return connectedAPI;
}
```

### Example 2: Send NIGHT Payment

```typescript
import { nativeToken } from '@midnight-ntwrk/ledger';

async function sendPayment(
  connectedAPI: ConnectedAPI,
  recipient: string,
  amount: bigint
): Promise<string> {
  // Create transfer
  const tx = await connectedAPI.makeTransfer([{
    kind: 'unshielded',
    tokenType: nativeToken().raw,
    value: amount,
    recipient: recipient
  }]);
  
  // Submit
  const result = await connectedAPI.submitTransaction(tx);
  
  console.log(`Transaction submitted: ${result.txHash}`);
  return result.txHash;
}

// Usage
const txHash = await sendPayment(
  connectedAPI,
  'mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3',
  10_000_000n  // 10 NIGHT
);
```

### Example 3: Atomic Swap

```typescript
// Party 1: Create swap offer
async function createSwapOffer(
  connectedAPI: ConnectedAPI
): Promise<Transaction> {
  const myAddress = (await connectedAPI.getShieldedAddresses()).shieldedAddress;
  
  // Offer: 10 NIGHT for 50,000 FOO
  const tx = await connectedAPI.makeIntent(
    [{ kind: 'unshielded', tokenType: nativeToken().raw, value: 10_000_000n }],
    [{ kind: 'shielded', tokenType: getFooToken(), value: 50_000n, recipient: myAddress }]
  );
  
  return tx;
}

// Party 2: Complete swap
async function completeSwap(
  connectedAPI: ConnectedAPI,
  offerTx: Transaction
): Promise<string> {
  // Balance transaction (provides 50,000 FOO, receives 10 NIGHT)
  const balancedTx = await connectedAPI.balanceSealedTransaction(offerTx);
  
  // Submit
  const result = await connectedAPI.submitTransaction(balancedTx.tx);
  
  return result.txHash;
}
```

### Example 4: Delegate Proof Generation

```typescript
import { FetchZkConfigProvider } from '@midnight-ntwrk/midnight-js-fetch-zk-config-provider';

async function delegateProving(
  connectedAPI: ConnectedAPI,
  unprovenTx: UnprovenTransaction
): Promise<string> {
  // Get user's configured prover
  const config = await connectedAPI.getConfiguration();
  const keyMaterialProvider = new FetchZkConfigProvider(config.proverServerUri);
  const provingProvider = connectedAPI.getProvingProvider(keyMaterialProvider);
  
  // Get cost model
  const costModel = await fetchCostModel();
  
  // Generate proof
  const provenTx = await unprovenTx.prove(provingProvider, costModel);
  
  // Balance (add fees)
  const finalTx = await connectedAPI.balanceUnsealedTransaction(provenTx);
  
  // Submit
  const result = await connectedAPI.submitTransaction(finalTx.tx);
  
  return result.txHash;
}
```

## Error Handling

### APIError Class

```typescript
class APIError extends Error {
  code: ErrorCode;
  message: string;
  details?: any;
}
```

### ErrorCodes

```typescript
enum ErrorCode {
  USER_REJECTED = 'USER_REJECTED',
  NETWORK_ERROR = 'NETWORK_ERROR',
  INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS',
  INVALID_ADDRESS = 'INVALID_ADDRESS',
  TRANSACTION_FAILED = 'TRANSACTION_FAILED',
  NOT_CONNECTED = 'NOT_CONNECTED',
  UNSUPPORTED_NETWORK = 'UNSUPPORTED_NETWORK'
}
```

### Error Handling Pattern

```typescript
try {
  const tx = await connectedAPI.makeTransfer([...]);
  await connectedAPI.submitTransaction(tx);
} catch (error) {
  if (error instanceof APIError) {
    switch (error.code) {
      case 'USER_REJECTED':
        console.log('User cancelled transaction');
        break;
      case 'INSUFFICIENT_FUNDS':
        console.error('Not enough balance');
        break;
      case 'NETWORK_ERROR':
        console.error('Network issue:', error.message);
        break;
      default:
        console.error('Transaction failed:', error.message);
    }
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## Best Practices

### 1. Always Check API Version
```typescript
const version = wallet.apiVersion;
if (!semver.satisfies(version, '^4.0.0')) {
  throw new Error('Incompatible wallet version');
}
```

### 2. Respect User Configuration
```typescript
// ✅ Use user's services
const config = await connectedAPI.getConfiguration();
const indexer = new IndexerClient(config.indexerUri);

// ❌ Don't hardcode endpoints
const indexer = new IndexerClient('https://my-indexer.com');
```

### 3. Handle User Rejection
```typescript
try {
  await connectedAPI.submitTransaction(tx);
} catch (error) {
  if (error.code === 'USER_REJECTED') {
    // User cancelled - this is normal, don't show error
    return;
  }
  throw error;
}
```

### 4. Validate Addresses
```typescript
function isValidAddress(addr: string): boolean {
  return addr.startsWith('mn_addr1') && addr.length >= 50;
}

if (!isValidAddress(recipient)) {
  throw new Error('Invalid Midnight address');
}
```

### 5. Use Bech32m Format
```typescript
// ✅ All addresses in Bech32m (v4.0.0+)
const address = await connectedAPI.getUnshieldedAddress();
// Returns: "mn_addr1..."
```

## Resources

- **Specification**: https://github.com/midnightntwrk/midnight-dapp-connector-api/blob/main/docs/api/_media/SPECIFICATION.md
- **Network Configuration**: See network-configuration.md
- **Address Formats**: See address-formats.md
- **Integration Patterns**: See integration-patterns.md

  tokenType: nativeToken().raw,
  value: 10_000_000,  // 10 Night
  recipient: 'mn_addr1...'
}]);
```

### Balance Transaction
```typescript
const balanced = await api.balanceUnsealedTransaction(tx);
```

### Submit Transaction
```typescript
await api.submitTransaction(balanced);
```

## Complete Example

```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';
import { nativeToken } from '@midnight-ntwrk/ledger-v7';

async function sendPayment() {
  const networkId = NetworkId('preprod');
  const api = await window.midnight.someWallet.connect(networkId);
  
  const tx = await api.makeTransfer([{
    kind: "unshielded",
    type: nativeToken().raw,
    value: 10_000_000,
    recipient: "mn_addr1..."
  }]);
  
  await api.submitTransaction(tx);
}
```

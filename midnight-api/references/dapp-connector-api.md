# DApp Connector API Reference

**Package**: `@midnight-ntwrk/dapp-connector-api v4.0.0`

## Installation

```bash
yarn add @midnight-ntwrk/dapp-connector-api
```

## Wallet Connection

### Connect to Wallet
```typescript
const api = await window.midnight.{walletId}.connect('mainnet');
```

### Get Wallet Info
```typescript
const name = window.midnight.{walletId}.name;
const icon = window.midnight.{walletId}.icon;
const apiVersion = window.midnight.{walletId}.apiVersion;
```

## Configuration

```typescript
const config = await api.getConfiguration();
// Returns: indexerUri, indexerWsUri, proverServerUri, substrateNodeUri, networkId
```

## Read Wallet State

```typescript
const shieldedBalances = await api.getShieldedBalances();
const unshieldedBalances = await api.getUnshieldedBalances();
const dustBalance = await api.getDustBalance();
const shieldedAddresses = await api.getShieldedAddresses();
const unshieldedAddress = await api.getUnshieldedAddress();
const dustAddress = await api.getDustAddress();
```

## Transactions

### Make Transfer
```typescript
import { nativeToken } from '@midnight-ntwrk/ledger';

const tx = await api.makeTransfer([{
  kind: 'unshielded',
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

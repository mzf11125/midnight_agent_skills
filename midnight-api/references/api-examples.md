# API Examples

## Example 1: Connect to Wallet

```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

async function connect() {
  const networkId = NetworkId('preprod');
  const compatibleWallets = Object.values(window.midnight ?? {})
    .filter((wallet) => semverMatch(wallet.apiVersion, '^1.0'));
  
  const selectedWallet = await askUserToSelect(compatibleWallets);
  const connectedWallet = await selectedWallet.connect(networkId);
  const connectionStatus = await connectedWallet.getConnectionStatus();
  
  return connectedWallet;
}
```

## Example 2: Send Payment

```typescript
import { nativeToken } from '@midnight-ntwrk/ledger-v7';

async function sendPayment() {
  const connectedWallet = await connect();
  const tx = await connectedWallet.makeTransfer([{
    kind: "unshielded",
    type: nativeToken().raw,
    value: 10_000_000,  // 10 Night
    recipient: "mn_addr1..."
  }]);
  await connectedWallet.submitTransaction(tx);
}
```

## Example 3: Private Swap

```typescript
// Party #1: Create unbalanced transaction
const tx = await connectedWallet.makeIntent([{
  kind: "unshielded",
  type: nativeToken().raw,
  value: 10_000_000,  // Offering 10 Night
}], [{
  kind: "shielded",
  type: getFooTokenType(),
  value: 50_000,  // Requesting 50,000 Foo
  recipient: shieldedAddress
}]);

// Party #2: Complete the swap
const balancedTx = await connectedWallet.balanceSealedTransaction(tx);
await connectedWallet.submitTransaction(balancedTx);
```

## Example 4: Delegate Proving

```typescript
import { FetchZkConfigProvider } from '@midnight-ntwrk/midnight-js-fetch-zk-config-provider';

const keyMaterialProvider = new FetchZkConfigProvider('https://example.com');
const connectedAPI = await connect();
const provingProvider = connectedAPI.getProvingProvider(keyMaterialProvider);

// Prepare unproven transaction
const costModel = await fetchCostModel();
const unprovedTx = prepareUnprovenTransaction(costModel);

// Generate proof
const provenTx = await unprovedTx.prove(provingProvider, costModel);

// Balance and submit
const finalTx = await connectedAPI.balanceUnsealedTransaction(provenTx);
await connectedAPI.submitTransaction(finalTx);
```

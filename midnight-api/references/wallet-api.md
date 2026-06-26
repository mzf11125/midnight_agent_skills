# Wallet SDK API Reference

**Package**: `@midnight-ntwrk/wallet-sdk-facade v3.0.0`

## Overview

The Wallet SDK provides unified wallet operations, key management, and transfers for Midnight Network. It handles shielded and unshielded transactions, DUST management, and atomic swaps.

## Installation

```bash
npm install @midnight-ntwrk/wallet-sdk-facade
```

## Wallet Initialization

### Create Wallet Instance

```typescript
import { WalletFacade } from '@midnight-ntwrk/wallet-sdk-facade';

// Initialize wallet (entry point)
const wallet = await WalletFacade.init({
  indexerUri: 'https://indexer.preprod.midnight.network',
  proofServerUri: 'http://localhost:6300',
  networkId: 'preprod',
});
```

`WalletFacade.init()` is the entry point. There is no `create` method.

### Start Wallet

```typescript
import { HDWallet, Roles } from '@midnight-ntwrk/wallet-sdk-facade';

// HD key derivation from seed
const hdWallet = HDWallet.fromSeed(seed);

// Derive keys using roles
const shieldedKey = hdWallet.derive(Roles.Zswap);
const dustKey = hdWallet.derive(Roles.Dust);
const nightKey = hdWallet.derive(Roles.NightExternal);

// Start wallet with secret keys
await wallet.start(shieldedSecretKeys, dustSecretKey);
```

### Stop Wallet

```typescript
await wallet.stop();
```

## HD Key Derivation

### From Seed

```typescript
import { HDWallet, Roles } from '@midnight-ntwrk/wallet-sdk-facade';

const hdWallet = HDWallet.fromSeed(seed);

// Derive keys for different purposes
const zswapKey = hdWallet.derive(Roles.Zswap);
const dustKey = hdWallet.derive(Roles.Dust);
const nightExternalKey = hdWallet.derive(Roles.NightExternal);
```

### Roles

- `Roles.Zswap` - Shielded transaction keys
- `Roles.Dust` - DUST generation keys
- `Roles.NightExternal` - NIGHT token keys

## Address Encoding

### Encode Address

```typescript
import { MidnightBech32m } from '@midnight-ntwrk/wallet-sdk-facade';

// Encode address to Bech32m format
const encoded = MidnightBech32m.encode(networkId, address);
```

### Decode Address

```typescript
const [networkId, address] = MidnightBech32m.decode(encodedAddress);
```

## Balance Queries

### Get Synced Balances

```typescript
// Wait for wallet to sync, then access balances
const syncedState = await wallet.waitForSyncedState();

// Shielded balances
const shieldedBalances = syncedState.shielded.balances;

// Unshielded balances
const unshieldedBalances = syncedState.unshielded.balances;
```

Balance access goes through `wallet.waitForSyncedState()`. The result has `.shielded.balances` and `.unshielded.balances` properties.

## Transfers

### Transfer Transaction (Recipe Pattern)

```typescript
// Transfer uses a recipe pattern
const recipe = await wallet.transferTransaction({
  recipient: recipientAddress,
  amount: amount,
  tokenType: tokenType,
});

// Submit the transaction
const txHash = await recipe.submit();
```

Transfers use `wallet.transferTransaction()` with a recipe pattern.

## DUST Management

### Register UTXOs for DUST Generation

```typescript
// Register NIGHT UTXOs to generate DUST
await wallet.registerNightUtxosForDustGeneration();
```

### DUST Sponsorship

```typescript
// Create an unbound transaction for balance
const unboundTx = await wallet.balanceUnboundTransaction();

// Use sponsor wallet to finalize
const finalizedTx = await sponsorWallet.balanceFinalizedTransaction(unboundTx);

// Submit
const txHash = await finalizedTx.submit();
```

DUST sponsorship uses `balanceUnboundTransaction()` then `sponsorWallet.balanceFinalizedTransaction()`.

## Atomic Swaps

### Initialize Swap

```typescript
// Start an atomic swap
const swap = await wallet.initSwap({
  counterparty: counterpartyAddress,
  offerToken: offerTokenType,
  offerAmount: offerAmount,
  wantToken: wantTokenType,
  wantAmount: wantAmount,
});

// Accept or complete swap
await swap.complete();
```

Atomic swaps use `wallet.initSwap()`.

## Alternative Proving

### WASM Proving Service

```typescript
import { makeWasmProvingService } from '@midnight-ntwrk/wallet-sdk-facade';

// Use WASM for proof generation instead of proof server
const provingService = makeWasmProvingService();
```

## Complete Example: Send Payment

```typescript
import {
  WalletFacade,
  HDWallet,
  Roles,
  MidnightBech32m,
} from '@midnight-ntwrk/wallet-sdk-facade';

async function sendPayment(
  seed: Uint8Array,
  recipientAddress: string,
  amount: bigint
) {
  // 1. Derive keys
  const hdWallet = HDWallet.fromSeed(seed);
  const shieldedKey = hdWallet.derive(Roles.Zswap);
  const dustKey = hdWallet.derive(Roles.Dust);

  // 2. Initialize and start wallet
  const wallet = await WalletFacade.init({
    indexerUri: 'https://indexer.preprod.midnight.network',
    proofServerUri: 'http://localhost:6300',
    networkId: 'preprod',
  });
  await wallet.start([shieldedKey], dustKey);

  // 3. Wait for sync and check balance
  const syncedState = await wallet.waitForSyncedState();
  console.log('Shielded balances:', syncedState.shielded.balances);

  // 4. Transfer
  const recipe = await wallet.transferTransaction({
    recipient: recipientAddress,
    amount: amount,
  });
  const txHash = await recipe.submit();
  console.log('Transaction submitted:', txHash);

  // 5. Stop wallet
  await wallet.stop();
  return txHash;
}
```

## Security Best Practices

### Secure Key Storage

```typescript
// Encrypt seed before storing
const encrypted = await encrypt(seed, userPassword);
await secureStorage.save('wallet', encrypted);

// Never store plaintext seed
// localStorage.setItem('seed', seed); // INSECURE
```

### Clear Sensitive Data

```typescript
// Stop wallet and clear on logout
await wallet.stop();
```

### Validate Addresses

```typescript
// Validate before sending
try {
  const [networkId, address] = MidnightBech32m.decode(recipientAddress);
  if (networkId !== expectedNetworkId) {
    throw new Error('Wrong network');
  }
} catch (error) {
  throw new Error('Invalid recipient address');
}
```

## Resources

- **API Documentation**: https://docs.midnight.network/api-reference/wallet-api
- **Address Formats**: See address-formats.md
- **ZSwap Integration**: See zswap-api.md
- **Security Guide**: https://docs.midnight.network/security

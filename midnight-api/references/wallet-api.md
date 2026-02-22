# Wallet API Reference

**Package**: `@midnight-ntwrk/wallet v5.0.0`

## Overview

The Wallet API provides key management, transaction signing, and state synchronization for Midnight Network. It handles both shielded (private) and unshielded (public) operations.

## Installation

```bash
yarn add @midnight-ntwrk/wallet
```

## Wallet Creation

### Generate New Wallet

```typescript
import { Wallet } from '@midnight-ntwrk/wallet';

// Generate random wallet
const wallet = await Wallet.generate();

// Get seed phrase for backup
const seedPhrase = wallet.getSeedPhrase();
console.log('Backup seed phrase:', seedPhrase);
```

**Security**: Store seed phrase securely. Anyone with it can access funds.

### From Seed Phrase

```typescript
const seedPhrase = 'word1 word2 word3 ... word24';
const wallet = await Wallet.fromSeedPhrase(seedPhrase);
```

**Seed phrase**: 24-word BIP39 mnemonic.

### From Private Key

```typescript
import { PrivateKey } from '@midnight-ntwrk/wallet';

const privateKey = PrivateKey.fromHex('0x...');
const wallet = await Wallet.fromPrivateKey(privateKey);
```

## Address Management

### Get Addresses

```typescript
// Shielded address (private transactions)
const shieldedAddress = wallet.getShieldedAddress();
console.log('Shielded:', shieldedAddress);

// Unshielded address (public transactions)
const unshieldedAddress = wallet.getUnshieldedAddress();
console.log('Unshielded:', unshieldedAddress);
```

**Address formats**: Both use Bech32m encoding (v4.0.0+).

### Derive Multiple Addresses

```typescript
// Derive address at specific index
const address0 = wallet.deriveShieldedAddress(0);
const address1 = wallet.deriveShieldedAddress(1);

// For account separation
const savingsAddress = wallet.deriveShieldedAddress(1);
const spendingAddress = wallet.deriveShieldedAddress(2);
```

**Use when**: Managing multiple accounts from one seed.

## Key Management

### Get Keys

```typescript
// Spending key (private)
const spendingKey = wallet.getSpendingKey();

// Viewing key (can see transactions, not spend)
const viewingKey = wallet.getViewingKey();

// Public key
const publicKey = wallet.getPublicKey();
```

### Key Types

```typescript
interface PrivateKey {
  toHex(): string;
  toBytes(): Uint8Array;
}

interface PublicKey {
  toHex(): string;
  toBytes(): Uint8Array;
  toAddress(): string;  // Convert to address
}

interface ViewingKey {
  toHex(): string;
  // Can decrypt transactions but not spend
}
```

### Export Keys

```typescript
// Export for backup
const privateKeyHex = wallet.getSpendingKey().toHex();
const viewingKeyHex = wallet.getViewingKey().toHex();

// Store securely (encrypted)
await secureStorage.save('privateKey', privateKeyHex);
```

## State Synchronization

### Sync with Indexer

```typescript
import { IndexerConfig } from '@midnight-ntwrk/wallet';

const indexerUri = 'https://indexer.testnet.midnight.network';

// Sync wallet state
await wallet.sync(indexerUri);

// Sync with progress callback
await wallet.sync(indexerUri, {
  onProgress: (current, total) => {
    console.log(`Syncing: ${current}/${total} blocks`);
  }
});
```

**Purpose**: Scans blockchain for wallet's transactions.

### Auto-Sync

```typescript
// Start background sync
wallet.startAutoSync(indexerUri, {
  interval: 10000,  // 10 seconds
  onError: (error) => console.error('Sync error:', error)
});

// Stop auto-sync
wallet.stopAutoSync();
```

### Get Sync Status

```typescript
const status = wallet.getSyncStatus();
console.log('Last synced block:', status.lastBlock);
console.log('Is syncing:', status.isSyncing);
console.log('Sync progress:', status.progress);
```

## Balance Queries

### Get All Balances

```typescript
const balances = wallet.getBalances();

// Iterate balances
for (const [tokenType, amount] of balances) {
  console.log(`Token ${tokenType}: ${amount}`);
}
```

**Returns**: Map of TokenType → bigint amount.

### Get Specific Token Balance

```typescript
import { DUST_TOKEN_TYPE } from '@midnight-ntwrk/wallet';

const dustBalance = wallet.getBalance(DUST_TOKEN_TYPE);
console.log(`DUST balance: ${dustBalance}`);

// Check sufficient funds
if (dustBalance < 1000n) {
  throw new Error('Insufficient DUST');
}
```

### Shielded vs Unshielded Balances

```typescript
// Shielded balance (private)
const shieldedBalance = wallet.getShieldedBalance(DUST_TOKEN_TYPE);

// Unshielded balance (public)
const unshieldedBalance = wallet.getUnshieldedBalance(DUST_TOKEN_TYPE);

// Total
const total = shieldedBalance + unshieldedBalance;
```

## Transaction History

### Get Transactions

```typescript
// All transactions
const txs = wallet.getTransactions();

// Filter by token type
const dustTxs = wallet.getTransactions({ tokenType: DUST_TOKEN_TYPE });

// Paginated
const recentTxs = wallet.getTransactions({ 
  limit: 10, 
  offset: 0 
});
```

### Transaction Details

```typescript
interface Transaction {
  hash: string;
  blockNumber: bigint;
  timestamp: number;
  type: 'send' | 'receive' | 'shield' | 'unshield';
  tokenType: TokenType;
  amount: bigint;
  fee: bigint;
  status: 'pending' | 'confirmed' | 'failed';
}

// Get specific transaction
const tx = wallet.getTransaction(txHash);
console.log('Amount:', tx.amount);
console.log('Status:', tx.status);
```

## Transaction Signing

### Sign Transaction

```typescript
import { Transaction } from '@midnight-ntwrk/wallet';

// Build transaction
const unsignedTx = await buildTransaction({
  from: wallet.getShieldedAddress(),
  to: recipientAddress,
  amount: 1000n,
  tokenType: DUST_TOKEN_TYPE
});

// Sign
const signedTx = await wallet.signTransaction(unsignedTx);

// Submit
const txHash = await submitTransaction(signedTx, nodeUri);
```

### Sign Message

```typescript
// Sign arbitrary message
const message = 'Hello Midnight';
const signature = await wallet.signMessage(message);

// Verify signature
const isValid = await wallet.verifySignature(
  message,
  signature,
  wallet.getPublicKey()
);
```

### Batch Signing

```typescript
// Sign multiple transactions
const signedTxs = await wallet.signTransactions([tx1, tx2, tx3]);

// Submit all
const txHashes = await Promise.all(
  signedTxs.map(tx => submitTransaction(tx, nodeUri))
);
```

## Coin Management

### Get Coins

```typescript
// All unspent coins
const coins = wallet.getCoins();

// Filter by token type
const dustCoins = wallet.getCoins({ tokenType: DUST_TOKEN_TYPE });

// Filter by minimum value
const largeCoins = wallet.getCoins({ minValue: 1000n });
```

### Coin Selection

```typescript
// Select coins for payment
const selectedCoins = wallet.selectCoins({
  tokenType: DUST_TOKEN_TYPE,
  amount: 5000n,
  strategy: 'minimize-inputs'  // or 'maximize-privacy'
});

console.log('Selected coins:', selectedCoins.length);
console.log('Total value:', selectedCoins.reduce((sum, c) => sum + c.value, 0n));
```

**Strategies**:
- `minimize-inputs`: Fewer coins, lower fees
- `maximize-privacy`: More coins, better privacy

### Coin Details

```typescript
interface Coin {
  tokenType: TokenType;
  value: bigint;
  nonce: Field;
  index: bigint;  // Merkle tree position
  isSpent: boolean;
}
```

## Shielding & Unshielding

### Shield Coins (Public → Private)

```typescript
// Move coins to shielded pool
const shieldTx = await wallet.shield({
  tokenType: DUST_TOKEN_TYPE,
  amount: 1000n,
  from: wallet.getUnshieldedAddress()
});

const signedTx = await wallet.signTransaction(shieldTx);
await submitTransaction(signedTx, nodeUri);
```

### Unshield Coins (Private → Public)

```typescript
// Move coins from shielded pool
const unshieldTx = await wallet.unshield({
  tokenType: DUST_TOKEN_TYPE,
  amount: 500n,
  to: wallet.getUnshieldedAddress()
});

const signedTx = await wallet.signTransaction(unshieldTx);
await submitTransaction(signedTx, nodeUri);
```

## Wallet Configuration

### Set Network

```typescript
import { NetworkId } from '@midnight-ntwrk/wallet';

wallet.setNetwork(NetworkId.TestNet);
// or NetworkId.MainNet
```

### Configure Indexer

```typescript
wallet.setIndexer({
  uri: 'https://indexer.testnet.midnight.network',
  timeout: 30000,  // 30 seconds
  retries: 3
});
```

### Set Fee Strategy

```typescript
wallet.setFeeStrategy({
  type: 'fixed',
  amount: 10n
});

// Or dynamic fees
wallet.setFeeStrategy({
  type: 'dynamic',
  multiplier: 1.5  // 1.5x base fee
});
```

## Complete Example: Send Payment

```typescript
import {
  Wallet,
  DUST_TOKEN_TYPE,
  NetworkId
} from '@midnight-ntwrk/wallet';
import { submitTransaction } from '@midnight-ntwrk/ledger';

async function sendPayment(
  seedPhrase: string,
  recipientAddress: string,
  amount: bigint
) {
  // 1. Load wallet
  const wallet = await Wallet.fromSeedPhrase(seedPhrase);
  wallet.setNetwork(NetworkId.TestNet);
  
  // 2. Sync state
  const indexerUri = 'https://indexer.testnet.midnight.network';
  await wallet.sync(indexerUri);
  
  // 3. Check balance
  const balance = wallet.getBalance(DUST_TOKEN_TYPE);
  const fee = 10n;
  
  if (balance < amount + fee) {
    throw new Error(`Insufficient balance: ${balance}`);
  }
  
  // 4. Build transaction
  const tx = await wallet.buildTransaction({
    to: recipientAddress,
    amount,
    tokenType: DUST_TOKEN_TYPE,
    fee
  });
  
  // 5. Sign transaction
  const signedTx = await wallet.signTransaction(tx);
  
  // 6. Submit
  const nodeUri = 'https://rpc.testnet.midnight.network';
  const txHash = await submitTransaction(signedTx, nodeUri);
  
  console.log(`Transaction submitted: ${txHash}`);
  
  // 7. Wait for confirmation
  await wallet.waitForTransaction(txHash, { timeout: 60000 });
  
  console.log('Transaction confirmed!');
  
  return txHash;
}
```

## Security Best Practices

### 1. Secure Seed Phrase Storage

```typescript
// ✅ Encrypt before storing
const encrypted = await encrypt(seedPhrase, userPassword);
await secureStorage.save('wallet', encrypted);

// ❌ Never store plaintext
localStorage.setItem('seedPhrase', seedPhrase);  // INSECURE
```

### 2. Use Viewing Keys for Read-Only

```typescript
// ✅ Share viewing key for auditing
const viewingKey = wallet.getViewingKey();
const readOnlyWallet = Wallet.fromViewingKey(viewingKey);

// Can see transactions, cannot spend
const balance = readOnlyWallet.getBalance(DUST_TOKEN_TYPE);
```

### 3. Validate Addresses

```typescript
// ✅ Validate before sending
import { isValidAddress } from '@midnight-ntwrk/wallet';

if (!isValidAddress(recipientAddress)) {
  throw new Error('Invalid recipient address');
}

// ❌ Sending to invalid address
await wallet.send(invalidAddress, amount);  // Funds lost
```

### 4. Handle Sync Errors

```typescript
// ✅ Retry on failure
async function syncWithRetry(wallet: Wallet, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await wallet.sync(indexerUri);
      return;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * (i + 1));  // Exponential backoff
    }
  }
}
```

### 5. Clear Sensitive Data

```typescript
// ✅ Clear on logout
wallet.clear();
delete wallet;

// Clear from memory
if (global.gc) global.gc();
```

## Resources

- **API Documentation**: https://docs.midnight.network/api-reference/wallet-api
- **Address Formats**: See address-formats.md
- **ZSwap Integration**: See zswap-api.md
- **Security Guide**: https://docs.midnight.network/security

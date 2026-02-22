# Ledger API Reference

**Package**: `@midnight-ntwrk/ledger v3.0.2`

## Overview

The Ledger API provides blockchain interaction capabilities including transaction submission, block queries, state management, and token operations.

## Installation

```bash
yarn add @midnight-ntwrk/ledger
```

## Network Configuration

```typescript
import { setNetworkId, NetworkId } from '@midnight-ntwrk/ledger';

// Set network before operations
setNetworkId(NetworkId.TestNet);
```

## Token Types

### Native Token

```typescript
import { nativeToken, TokenType } from '@midnight-ntwrk/ledger';

// Get native token (NIGHT)
const night = nativeToken();
console.log('Native token:', night);
```

### Custom Tokens

```typescript
import { customTokenType } from '@midnight-ntwrk/ledger';

// Create custom token type
const myToken = customTokenType('my-token-id');

// Token type is Bytes<32>
type TokenType = Bytes<32>;
```

### Token Info

```typescript
interface TokenInfo {
  tokenType: TokenType;
  name: string;
  symbol: string;
  decimals: number;
  totalSupply: bigint;
}

// Get token info
const tokenInfo = await getTokenInfo(tokenType, indexerUri);
console.log(`${tokenInfo.symbol}: ${tokenInfo.totalSupply}`);
```

## Transaction Submission

### Submit Transaction

```typescript
import { submitTransaction } from '@midnight-ntwrk/ledger';

const nodeUri = 'https://rpc.testnet.midnight.network';

// Submit signed transaction
const txHash = await submitTransaction(signedTx, nodeUri);
console.log('Transaction hash:', txHash);
```

### Submit with Options

```typescript
const txHash = await submitTransaction(signedTx, nodeUri, {
  timeout: 30000,      // 30 seconds
  retries: 3,          // Retry on failure
  waitForConfirmation: true
});
```

### Batch Submission

```typescript
// Submit multiple transactions
const txHashes = await submitTransactions([tx1, tx2, tx3], nodeUri);

console.log('Submitted transactions:', txHashes);
```

## Transaction Queries

### Get Transaction

```typescript
import { getTransaction } from '@midnight-ntwrk/ledger';

const tx = await getTransaction(txHash, indexerUri);

console.log('Block:', tx.blockNumber);
console.log('Status:', tx.status);
console.log('Fee:', tx.fee);
```

### Transaction Details

```typescript
interface Transaction {
  hash: string;
  blockNumber: bigint;
  blockHash: string;
  timestamp: number;
  from: string;
  to: string;
  value: bigint;
  tokenType: TokenType;
  fee: bigint;
  status: 'pending' | 'confirmed' | 'failed';
  gasUsed: bigint;
  data: Uint8Array;
}
```

### Get Transaction Receipt

```typescript
import { getTransactionReceipt } from '@midnight-ntwrk/ledger';

const receipt = await getTransactionReceipt(txHash, indexerUri);

console.log('Confirmed:', receipt.confirmed);
console.log('Block:', receipt.blockNumber);
console.log('Gas used:', receipt.gasUsed);
```

### Wait for Confirmation

```typescript
import { waitForTransaction } from '@midnight-ntwrk/ledger';

// Wait for transaction to be confirmed
const receipt = await waitForTransaction(txHash, indexerUri, {
  timeout: 60000,      // 60 seconds
  confirmations: 1     // Number of confirmations
});

console.log('Transaction confirmed in block:', receipt.blockNumber);
```

## Block Queries

### Get Block

```typescript
import { getBlock } from '@midnight-ntwrk/ledger';

// Get block by number
const block = await getBlock(12345n, indexerUri);

console.log('Block hash:', block.hash);
console.log('Transactions:', block.transactions.length);
console.log('Timestamp:', block.timestamp);
```

### Get Latest Block

```typescript
import { getLatestBlock } from '@midnight-ntwrk/ledger';

const latestBlock = await getLatestBlock(indexerUri);

console.log('Latest block number:', latestBlock.number);
console.log('Block time:', new Date(latestBlock.timestamp * 1000));
```

### Block Details

```typescript
interface Block {
  number: bigint;
  hash: string;
  parentHash: string;
  timestamp: number;
  transactions: string[];  // Transaction hashes
  stateRoot: string;
  transactionsRoot: string;
  receiptsRoot: string;
  gasUsed: bigint;
  gasLimit: bigint;
  validator: string;
}
```

### Get Block Range

```typescript
import { getBlocks } from '@midnight-ntwrk/ledger';

// Get multiple blocks
const blocks = await getBlocks(
  1000n,  // Start block
  1100n,  // End block
  indexerUri
);

console.log(`Retrieved ${blocks.length} blocks`);
```

## State Queries

### Get Account State

```typescript
import { getAccountState } from '@midnight-ntwrk/ledger';

const state = await getAccountState(address, indexerUri);

console.log('Nonce:', state.nonce);
console.log('Balance:', state.balance);
console.log('Code hash:', state.codeHash);
```

### Account Details

```typescript
interface AccountState {
  address: string;
  nonce: bigint;
  balance: bigint;
  codeHash: string;
  storageRoot: string;
}
```

### Get Contract State

```typescript
import { getContractState } from '@midnight-ntwrk/ledger';

const contractState = await getContractState(contractAddress, indexerUri);

console.log('State:', contractState);
```

### Query Storage

```typescript
import { getStorageAt } from '@midnight-ntwrk/ledger';

// Get storage value at key
const value = await getStorageAt(
  contractAddress,
  storageKey,
  indexerUri
);

console.log('Storage value:', value);
```

## Balance Queries

### Get Balance

```typescript
import { getBalance } from '@midnight-ntwrk/ledger';

// Get native token balance
const balance = await getBalance(address, indexerUri);
console.log('Balance:', balance);

// Get specific token balance
const tokenBalance = await getBalance(address, indexerUri, tokenType);
console.log('Token balance:', tokenBalance);
```

### Get All Balances

```typescript
import { getAllBalances } from '@midnight-ntwrk/ledger';

const balances = await getAllBalances(address, indexerUri);

// Iterate all token balances
for (const [tokenType, amount] of balances) {
  console.log(`Token ${tokenType}: ${amount}`);
}
```

## Event Queries

### Get Events

```typescript
import { getEvents } from '@midnight-ntwrk/ledger';

// Get events from contract
const events = await getEvents({
  address: contractAddress,
  fromBlock: 1000n,
  toBlock: 2000n,
  topics: ['Transfer']
}, indexerUri);

console.log('Events:', events.length);
```

### Event Details

```typescript
interface Event {
  address: string;
  topics: string[];
  data: Uint8Array;
  blockNumber: bigint;
  transactionHash: string;
  logIndex: number;
}
```

### Filter Events

```typescript
// Filter by event signature
const transferEvents = await getEvents({
  address: tokenContract,
  topics: ['0x' + keccak256('Transfer(address,address,uint256)')]
}, indexerUri);

// Filter by indexed parameters
const myTransfers = await getEvents({
  address: tokenContract,
  topics: [
    '0x' + keccak256('Transfer(address,address,uint256)'),
    null,  // from (any)
    myAddress  // to (my address)
  ]
}, indexerUri);
```

## Gas Estimation

### Estimate Gas

```typescript
import { estimateGas } from '@midnight-ntwrk/ledger';

// Estimate gas for transaction
const gasEstimate = await estimateGas({
  from: senderAddress,
  to: recipientAddress,
  value: 1000n,
  data: txData
}, nodeUri);

console.log('Estimated gas:', gasEstimate);
```

### Get Gas Price

```typescript
import { getGasPrice } from '@midnight-ntwrk/ledger';

const gasPrice = await getGasPrice(nodeUri);
console.log('Current gas price:', gasPrice);

// Calculate total fee
const totalFee = gasEstimate * gasPrice;
console.log('Total fee:', totalFee);
```

## Network Info

### Get Chain ID

```typescript
import { getChainId } from '@midnight-ntwrk/ledger';

const chainId = await getChainId(nodeUri);
console.log('Chain ID:', chainId);
```

### Get Network Version

```typescript
import { getNetworkVersion } from '@midnight-ntwrk/ledger';

const version = await getNetworkVersion(nodeUri);
console.log('Network version:', version);
```

### Get Peer Count

```typescript
import { getPeerCount } from '@midnight-ntwrk/ledger';

const peers = await getPeerCount(nodeUri);
console.log('Connected peers:', peers);
```

### Is Syncing

```typescript
import { isSyncing } from '@midnight-ntwrk/ledger';

const syncStatus = await isSyncing(nodeUri);

if (syncStatus === false) {
  console.log('Node is synced');
} else {
  console.log('Syncing:', syncStatus);
  console.log('Current block:', syncStatus.currentBlock);
  console.log('Highest block:', syncStatus.highestBlock);
}
```

## Transaction Building

### Build Transaction

```typescript
import { buildTransaction } from '@midnight-ntwrk/ledger';

const tx = await buildTransaction({
  from: senderAddress,
  to: recipientAddress,
  value: 1000n,
  tokenType: nativeToken(),
  nonce: await getAccountState(senderAddress, indexerUri).then(s => s.nonce),
  gasLimit: 21000n,
  gasPrice: await getGasPrice(nodeUri)
}, nodeUri);
```

### Transaction Parameters

```typescript
interface TransactionParams {
  from: string;
  to: string;
  value: bigint;
  tokenType?: TokenType;
  data?: Uint8Array;
  nonce?: bigint;
  gasLimit?: bigint;
  gasPrice?: bigint;
}
```

## Complete Example: Query Block Data

```typescript
import {
  setNetworkId,
  NetworkId,
  getLatestBlock,
  getBlock,
  getTransaction,
  getBalance
} from '@midnight-ntwrk/ledger';

async function queryBlockData(indexerUri: string) {
  // 1. Set network
  setNetworkId(NetworkId.TestNet);
  
  // 2. Get latest block
  const latestBlock = await getLatestBlock(indexerUri);
  console.log(`Latest block: ${latestBlock.number}`);
  console.log(`Transactions: ${latestBlock.transactions.length}`);
  
  // 3. Get block details
  const block = await getBlock(latestBlock.number, indexerUri);
  console.log(`Block hash: ${block.hash}`);
  console.log(`Timestamp: ${new Date(block.timestamp * 1000)}`);
  
  // 4. Query transactions
  for (const txHash of block.transactions.slice(0, 5)) {
    const tx = await getTransaction(txHash, indexerUri);
    console.log(`\nTransaction: ${txHash}`);
    console.log(`  From: ${tx.from}`);
    console.log(`  To: ${tx.to}`);
    console.log(`  Value: ${tx.value}`);
    console.log(`  Fee: ${tx.fee}`);
    
    // 5. Get sender balance
    const balance = await getBalance(tx.from, indexerUri);
    console.log(`  Sender balance: ${balance}`);
  }
}
```

## Complete Example: Submit Transaction

```typescript
import {
  setNetworkId,
  NetworkId,
  buildTransaction,
  submitTransaction,
  waitForTransaction,
  getGasPrice,
  estimateGas,
  nativeToken
} from '@midnight-ntwrk/ledger';
import { Wallet } from '@midnight-ntwrk/wallet';

async function sendTransaction(
  wallet: Wallet,
  recipientAddress: string,
  amount: bigint,
  nodeUri: string,
  indexerUri: string
) {
  // 1. Set network
  setNetworkId(NetworkId.TestNet);
  
  // 2. Get gas price
  const gasPrice = await getGasPrice(nodeUri);
  console.log('Gas price:', gasPrice);
  
  // 3. Build transaction
  const tx = await buildTransaction({
    from: wallet.getUnshieldedAddress(),
    to: recipientAddress,
    value: amount,
    tokenType: nativeToken(),
    gasPrice
  }, nodeUri);
  
  // 4. Estimate gas
  const gasEstimate = await estimateGas(tx, nodeUri);
  tx.gasLimit = gasEstimate * 120n / 100n;  // Add 20% buffer
  
  console.log('Gas estimate:', gasEstimate);
  console.log('Total fee:', tx.gasLimit * gasPrice);
  
  // 5. Sign transaction
  const signedTx = await wallet.signTransaction(tx);
  
  // 6. Submit transaction
  console.log('Submitting transaction...');
  const txHash = await submitTransaction(signedTx, nodeUri);
  console.log('Transaction hash:', txHash);
  
  // 7. Wait for confirmation
  console.log('Waiting for confirmation...');
  const receipt = await waitForTransaction(txHash, indexerUri, {
    timeout: 60000,
    confirmations: 1
  });
  
  console.log('Transaction confirmed!');
  console.log('Block number:', receipt.blockNumber);
  console.log('Gas used:', receipt.gasUsed);
  
  return txHash;
}
```

## Best Practices

### 1. Handle Network Errors

```typescript
// ✅ Retry on network failure
async function submitWithRetry(tx: Transaction, nodeUri: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await submitTransaction(tx, nodeUri);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * Math.pow(2, i));  // Exponential backoff
    }
  }
}
```

### 2. Validate Addresses

```typescript
// ✅ Validate before querying
import { isValidAddress } from '@midnight-ntwrk/ledger';

if (!isValidAddress(address)) {
  throw new Error('Invalid address format');
}

const balance = await getBalance(address, indexerUri);
```

### 3. Use Appropriate Confirmations

```typescript
// ✅ Wait for confirmations based on value
const confirmations = amount > 10000n ? 6 : 1;

const receipt = await waitForTransaction(txHash, indexerUri, {
  confirmations
});
```

### 4. Cache Block Data

```typescript
// ✅ Cache frequently accessed blocks
const blockCache = new Map<bigint, Block>();

async function getCachedBlock(blockNumber: bigint, indexerUri: string) {
  if (blockCache.has(blockNumber)) {
    return blockCache.get(blockNumber)!;
  }
  
  const block = await getBlock(blockNumber, indexerUri);
  blockCache.set(blockNumber, block);
  return block;
}
```

### 5. Monitor Gas Prices

```typescript
// ✅ Track gas price trends
async function getOptimalGasPrice(nodeUri: string) {
  const prices = [];
  
  for (let i = 0; i < 5; i++) {
    prices.push(await getGasPrice(nodeUri));
    await sleep(1000);
  }
  
  // Use median price
  prices.sort((a, b) => Number(a - b));
  return prices[Math.floor(prices.length / 2)];
}
```

## Resources

- **API Documentation**: https://docs.midnight.network/api-reference/ledger
- **Network Configuration**: See network-configuration.md
- **Wallet Integration**: See wallet-api.md
- **Indexer Setup**: See indexer-setup.md (midnight-network)

# Integration Patterns

## Overview

Common patterns for integrating Midnight Network APIs into DApps. Covers error handling, retry logic, state management, and production-ready implementations.

## Error Handling

### Basic Error Handling

```typescript
try {
  const api = await window.midnight.wallet.connect('testnet');
  const tx = await api.makeTransfer([...]);
  await api.submitTransaction(tx);
} catch (error) {
  if (error.code === 'USER_REJECTED') {
    console.log('User rejected transaction');
  } else if (error.code === 'INSUFFICIENT_FUNDS') {
    console.log('Insufficient balance');
  } else if (error.code === 'NETWORK_ERROR') {
    console.error('Network error:', error.message);
  } else {
    console.error('Transaction failed:', error);
  }
}
```

### APIError Structure

```typescript
interface APIError extends Error {
  code: ErrorCode;
  message: string;
  details?: any;
}

enum ErrorCode {
  USER_REJECTED = 'USER_REJECTED',
  INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS',
  NETWORK_ERROR = 'NETWORK_ERROR',
  INVALID_ADDRESS = 'INVALID_ADDRESS',
  TRANSACTION_FAILED = 'TRANSACTION_FAILED',
  WALLET_NOT_CONNECTED = 'WALLET_NOT_CONNECTED',
  UNSUPPORTED_NETWORK = 'UNSUPPORTED_NETWORK',
  PROOF_GENERATION_FAILED = 'PROOF_GENERATION_FAILED'
}
```

### Comprehensive Error Handler

```typescript
function handleMidnightError(error: APIError): string {
  switch (error.code) {
    case 'USER_REJECTED':
      return 'Transaction was cancelled';
    
    case 'INSUFFICIENT_FUNDS':
      return `Insufficient balance. Need ${error.details?.required}, have ${error.details?.available}`;
    
    case 'NETWORK_ERROR':
      return 'Network connection failed. Please try again.';
    
    case 'INVALID_ADDRESS':
      return `Invalid address: ${error.details?.address}`;
    
    case 'TRANSACTION_FAILED':
      return `Transaction failed: ${error.message}`;
    
    case 'WALLET_NOT_CONNECTED':
      return 'Please connect your wallet first';
    
    case 'UNSUPPORTED_NETWORK':
      return `Network not supported. Please switch to ${error.details?.supportedNetworks.join(', ')}`;
    
    case 'PROOF_GENERATION_FAILED':
      return 'Failed to generate zero-knowledge proof. Please try again.';
    
    default:
      return `Unexpected error: ${error.message}`;
  }
}
```

## Retry Logic

### Basic Retry

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * Math.pow(2, i));  // Exponential backoff
    }
  }
  throw new Error('Max retries exceeded');
}

// Usage
const balance = await withRetry(() => 
  api.getShieldedBalances()
);
```

### Retry with Specific Errors

```typescript
async function withRetryOnNetwork<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      // Only retry on network errors
      if (error.code !== 'NETWORK_ERROR') throw error;
      
      if (i === maxRetries - 1) throw error;
      
      const delay = 1000 * Math.pow(2, i);
      console.log(`Retry ${i + 1}/${maxRetries} in ${delay}ms...`);
      await sleep(delay);
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Retry with Timeout

```typescript
async function withRetryAndTimeout<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  timeout = 30000
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('Operation timed out')), timeout)
  );
  
  return Promise.race([
    withRetry(fn, maxRetries),
    timeoutPromise
  ]);
}
```

## State Synchronization

### Poll for Transaction Confirmation

```typescript
async function waitForConfirmation(
  txHash: string,
  indexerUri: string,
  options: {
    timeout?: number;
    interval?: number;
    confirmations?: number;
  } = {}
): Promise<Transaction> {
  const {
    timeout = 60000,
    interval = 5000,
    confirmations = 1
  } = options;
  
  const startTime = Date.now();
  
  while (true) {
    // Check timeout
    if (Date.now() - startTime > timeout) {
      throw new Error('Transaction confirmation timeout');
    }
    
    // Query transaction
    const tx = await queryTransaction(txHash, indexerUri);
    
    if (tx.confirmed && tx.confirmations >= confirmations) {
      return tx;
    }
    
    await sleep(interval);
  }
}

// Usage
const tx = await waitForConfirmation(txHash, indexerUri, {
  timeout: 120000,  // 2 minutes
  confirmations: 3
});
```

### Wallet State Sync

```typescript
class WalletStateManager {
  private syncInterval: NodeJS.Timeout | null = null;
  
  constructor(
    private wallet: Wallet,
    private indexerUri: string
  ) {}
  
  async startSync(intervalMs = 10000) {
    // Initial sync
    await this.sync();
    
    // Periodic sync
    this.syncInterval = setInterval(async () => {
      try {
        await this.sync();
      } catch (error) {
        console.error('Sync error:', error);
      }
    }, intervalMs);
  }
  
  stopSync() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }
  
  private async sync() {
    await this.wallet.sync(this.indexerUri);
    console.log('Wallet synced at', new Date().toISOString());
  }
}

// Usage
const stateManager = new WalletStateManager(wallet, indexerUri);
await stateManager.startSync(15000);  // Sync every 15 seconds
```

### Event-Based State Updates

```typescript
class EventBasedSync {
  private eventSource: EventSource | null = null;
  
  constructor(
    private wallet: Wallet,
    private wsUri: string
  ) {}
  
  connect() {
    this.eventSource = new EventSource(this.wsUri);
    
    this.eventSource.addEventListener('new-block', async (event) => {
      const block = JSON.parse(event.data);
      console.log('New block:', block.number);
      
      // Check if block contains wallet transactions
      await this.checkBlockForTransactions(block);
    });
    
    this.eventSource.addEventListener('error', (error) => {
      console.error('WebSocket error:', error);
      this.reconnect();
    });
  }
  
  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
  
  private async checkBlockForTransactions(block: Block) {
    // Scan block for wallet's transactions
    for (const txHash of block.transactions) {
      const tx = await getTransaction(txHash);
      if (this.isWalletTransaction(tx)) {
        console.log('Found wallet transaction:', txHash);
        await this.wallet.sync();
        break;
      }
    }
  }
  
  private isWalletTransaction(tx: Transaction): boolean {
    const addresses = [
      this.wallet.getShieldedAddress(),
      this.wallet.getUnshieldedAddress()
    ];
    return addresses.includes(tx.from) || addresses.includes(tx.to);
  }
  
  private reconnect() {
    setTimeout(() => {
      console.log('Reconnecting...');
      this.connect();
    }, 5000);
  }
}
```

## Wallet Connection Patterns

### Multi-Wallet Support

```typescript
async function connectWallet(
  preferredWallet?: string
): Promise<ConnectedAPI> {
  // Get all available wallets
  const wallets = Object.entries(window.midnight || {})
    .filter(([_, wallet]) => wallet.apiVersion)
    .map(([id, wallet]) => ({ id, ...wallet }));
  
  if (wallets.length === 0) {
    throw new Error('No Midnight wallets found');
  }
  
  // Try preferred wallet first
  if (preferredWallet) {
    const wallet = wallets.find(w => w.id === preferredWallet);
    if (wallet) {
      try {
        return await wallet.connect('testnet');
      } catch (error) {
        console.warn(`Failed to connect to ${preferredWallet}:`, error);
      }
    }
  }
  
  // Show wallet selection UI
  const selectedWallet = await showWalletSelector(wallets);
  return await selectedWallet.connect('testnet');
}
```

### Connection State Management

```typescript
class WalletConnection {
  private api: ConnectedAPI | null = null;
  private listeners: Set<(connected: boolean) => void> = new Set();
  
  async connect(networkId: string): Promise<ConnectedAPI> {
    if (this.api) return this.api;
    
    this.api = await window.midnight.wallet.connect(networkId);
    this.notifyListeners(true);
    
    // Monitor connection
    this.monitorConnection();
    
    return this.api;
  }
  
  disconnect() {
    this.api = null;
    this.notifyListeners(false);
  }
  
  isConnected(): boolean {
    return this.api !== null;
  }
  
  getAPI(): ConnectedAPI {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }
    return this.api;
  }
  
  onConnectionChange(listener: (connected: boolean) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  private notifyListeners(connected: boolean) {
    this.listeners.forEach(listener => listener(connected));
  }
  
  private async monitorConnection() {
    setInterval(async () => {
      if (!this.api) return;
      
      try {
        await this.api.getConnectionStatus();
      } catch (error) {
        console.error('Connection lost');
        this.disconnect();
      }
    }, 30000);  // Check every 30 seconds
  }
}

// Usage
const connection = new WalletConnection();

connection.onConnectionChange((connected) => {
  console.log('Wallet', connected ? 'connected' : 'disconnected');
  updateUI(connected);
});

await connection.connect('testnet');
```

## Transaction Patterns

### Safe Transaction Submission

```typescript
async function submitTransactionSafely(
  api: ConnectedAPI,
  tx: Transaction,
  indexerUri: string
): Promise<string> {
  // 1. Validate transaction
  if (!isValidTransaction(tx)) {
    throw new Error('Invalid transaction');
  }
  
  // 2. Check balance
  const balances = await api.getShieldedBalances();
  if (!hasSufficientBalance(tx, balances)) {
    throw new Error('Insufficient balance');
  }
  
  // 3. Submit with retry
  const txHash = await withRetryOnNetwork(
    () => api.submitTransaction(tx),
    3
  );
  
  console.log('Transaction submitted:', txHash);
  
  // 4. Wait for confirmation
  const confirmedTx = await waitForConfirmation(txHash, indexerUri, {
    timeout: 120000,
    confirmations: 1
  });
  
  console.log('Transaction confirmed in block:', confirmedTx.blockNumber);
  
  return txHash;
}
```

### Batch Transaction Processing

```typescript
async function processBatchTransactions(
  api: ConnectedAPI,
  transactions: Transaction[]
): Promise<string[]> {
  const results: string[] = [];
  const errors: Error[] = [];
  
  // Process in parallel with concurrency limit
  const concurrency = 3;
  
  for (let i = 0; i < transactions.length; i += concurrency) {
    const batch = transactions.slice(i, i + concurrency);
    
    const batchResults = await Promise.allSettled(
      batch.map(tx => api.submitTransaction(tx))
    );
    
    batchResults.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        results.push(result.value);
        console.log(`Transaction ${i + index} submitted:`, result.value);
      } else {
        errors.push(result.reason);
        console.error(`Transaction ${i + index} failed:`, result.reason);
      }
    });
  }
  
  if (errors.length > 0) {
    console.warn(`${errors.length} transactions failed`);
  }
  
  return results;
}
```

## Caching Patterns

### Simple Cache

```typescript
class SimpleCache<K, V> {
  private cache = new Map<K, { value: V; expiry: number }>();
  
  constructor(private ttl: number = 60000) {}  // 1 minute default
  
  set(key: K, value: V) {
    this.cache.set(key, {
      value,
      expiry: Date.now() + this.ttl
    });
  }
  
  get(key: K): V | undefined {
    const entry = this.cache.get(key);
    
    if (!entry) return undefined;
    
    if (Date.now() > entry.expiry) {
      this.cache.delete(key);
      return undefined;
    }
    
    return entry.value;
  }
  
  clear() {
    this.cache.clear();
  }
}

// Usage
const blockCache = new SimpleCache<bigint, Block>(30000);  // 30 second TTL

async function getCachedBlock(blockNumber: bigint): Promise<Block> {
  const cached = blockCache.get(blockNumber);
  if (cached) return cached;
  
  const block = await getBlock(blockNumber, indexerUri);
  blockCache.set(blockNumber, block);
  return block;
}
```

### LRU Cache

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();
  
  constructor(private maxSize: number = 100) {}
  
  get(key: K): V | undefined {
    const value = this.cache.get(key);
    
    if (value !== undefined) {
      // Move to end (most recently used)
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    
    return value;
  }
  
  set(key: K, value: V) {
    // Remove if exists
    this.cache.delete(key);
    
    // Add to end
    this.cache.set(key, value);
    
    // Evict oldest if over size
    if (this.cache.size > this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
  }
}
```

## Best Practices

### 1. Always Validate Inputs

```typescript
// ✅ Validate before processing
function validateTransferParams(
  recipient: string,
  amount: bigint,
  tokenType: TokenType
) {
  if (!isValidAddress(recipient)) {
    throw new Error('Invalid recipient address');
  }
  
  if (amount <= 0n) {
    throw new Error('Amount must be positive');
  }
  
  if (!isValidTokenType(tokenType)) {
    throw new Error('Invalid token type');
  }
}

// Use validation
validateTransferParams(recipient, amount, tokenType);
const tx = await api.makeTransfer([...]);
```

### 2. Handle User Rejections Gracefully

```typescript
// ✅ User-friendly rejection handling
try {
  const tx = await api.makeTransfer([...]);
  await api.submitTransaction(tx);
} catch (error) {
  if (error.code === 'USER_REJECTED') {
    // Don't show error - user intentionally cancelled
    console.log('Transaction cancelled by user');
    return;
  }
  
  // Show error for other cases
  showErrorToUser(handleMidnightError(error));
}
```

### 3. Provide Clear Error Messages

```typescript
// ✅ User-friendly error messages
function getUserFriendlyError(error: APIError): string {
  const messages = {
    'INSUFFICIENT_FUNDS': 'You don\'t have enough funds for this transaction.',
    'NETWORK_ERROR': 'Connection failed. Please check your internet.',
    'INVALID_ADDRESS': 'The recipient address is invalid.',
    'TRANSACTION_FAILED': 'Transaction failed. Please try again.'
  };
  
  return messages[error.code] || 'An unexpected error occurred.';
}
```

### 4. Use Proof Servers for Better UX

```typescript
// ✅ Delegate proving to wallet's proof server
const config = await api.getConfiguration();
const provingProvider = await api.getProvingProvider(keyMaterialProvider);

// Proof generation happens in background
const tx = await buildTransactionWithProving(provingProvider);
```

### 5. Cache Blockchain Data

```typescript
// ✅ Cache frequently accessed data
const balanceCache = new SimpleCache<string, bigint>(10000);

async function getBalanceWithCache(address: string): Promise<bigint> {
  const cached = balanceCache.get(address);
  if (cached !== undefined) return cached;
  
  const balance = await getBalance(address, indexerUri);
  balanceCache.set(address, balance);
  return balance;
}
```

### 6. Implement Retry Logic

```typescript
// ✅ Retry on transient failures
const balance = await withRetryOnNetwork(
  () => api.getShieldedBalances(),
  3
);
```

### 7. Monitor Transaction Status

```typescript
// ✅ Track transaction lifecycle
async function submitAndMonitor(tx: Transaction): Promise<void> {
  console.log('Submitting transaction...');
  const txHash = await api.submitTransaction(tx);
  
  console.log('Transaction submitted:', txHash);
  showNotification('Transaction submitted', 'info');
  
  try {
    const confirmedTx = await waitForConfirmation(txHash, indexerUri);
    console.log('Transaction confirmed:', confirmedTx.blockNumber);
    showNotification('Transaction confirmed!', 'success');
  } catch (error) {
    console.error('Transaction failed:', error);
    showNotification('Transaction failed', 'error');
  }
}
```

## Complete Example: Production DApp

```typescript
import {
  ConnectedAPI,
  DUST_TOKEN_TYPE
} from '@midnight-ntwrk/dapp-connector-api';

class MidnightDApp {
  private connection: WalletConnection;
  private stateManager: WalletStateManager | null = null;
  
  constructor(
    private indexerUri: string,
    private networkId: string
  ) {
    this.connection = new WalletConnection();
  }
  
  async initialize() {
    // Connect wallet
    const api = await this.connection.connect(this.networkId);
    
    // Start state sync
    const wallet = await Wallet.fromAPI(api);
    this.stateManager = new WalletStateManager(wallet, this.indexerUri);
    await this.stateManager.startSync();
    
    // Monitor connection
    this.connection.onConnectionChange((connected) => {
      if (!connected) {
        this.stateManager?.stopSync();
      }
    });
  }
  
  async sendPayment(recipient: string, amount: bigint) {
    // Validate
    validateTransferParams(recipient, amount, DUST_TOKEN_TYPE);
    
    // Get API
    const api = this.connection.getAPI();
    
    // Check balance
    const balances = await withRetry(() => api.getShieldedBalances());
    if ((balances[DUST_TOKEN_TYPE] || 0n) < amount) {
      throw new Error('Insufficient balance');
    }
    
    // Build transaction
    const tx = await api.makeTransfer([{
      kind: 'shielded',
      tokenType: DUST_TOKEN_TYPE,
      value: amount,
      recipient
    }]);
    
    // Submit safely
    return await submitTransactionSafely(api, tx, this.indexerUri);
  }
  
  async getBalance(): Promise<bigint> {
    const api = this.connection.getAPI();
    const balances = await withRetry(() => api.getShieldedBalances());
    return balances[DUST_TOKEN_TYPE] || 0n;
  }
  
  async disconnect() {
    this.stateManager?.stopSync();
    this.connection.disconnect();
  }
}

// Usage
const dapp = new MidnightDApp(
  'https://indexer.testnet.midnight.network',
  'testnet'
);

await dapp.initialize();
const txHash = await dapp.sendPayment(recipientAddress, 1000n);
console.log('Payment sent:', txHash);
```

## Resources

- **DApp Connector API**: See dapp-connector-api.md
- **Wallet API**: See wallet-api.md
- **Error Handling**: See error-codes.md
- **Network Configuration**: See network-configuration.md

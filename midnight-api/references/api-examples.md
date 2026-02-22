# API Examples

## Complete Working Examples

### Example 1: Connect to Wallet

```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';
import semver from 'semver';

async function connectWallet() {
  // 1. Check if Midnight wallets are available
  if (!window.midnight) {
    throw new Error('No Midnight wallets found. Please install a wallet extension.');
  }
  
  // 2. Get all available wallets
  const wallets = Object.entries(window.midnight)
    .filter(([_, wallet]) => wallet.apiVersion)
    .map(([id, wallet]) => ({ id, ...wallet }));
  
  if (wallets.length === 0) {
    throw new Error('No compatible Midnight wallets found');
  }
  
  // 3. Filter by API version compatibility
  const compatibleWallets = wallets.filter(wallet =>
    semver.satisfies(wallet.apiVersion, '^4.0.0')
  );
  
  if (compatibleWallets.length === 0) {
    throw new Error('No wallets with compatible API version (^4.0.0)');
  }
  
  // 4. Let user select wallet (or auto-select if only one)
  const selectedWallet = compatibleWallets.length === 1
    ? compatibleWallets[0]
    : await showWalletSelector(compatibleWallets);
  
  // 5. Connect to selected wallet
  const networkId = NetworkId('testnet');
  const connectedAPI = await selectedWallet.connect(networkId);
  
  // 6. Verify connection
  const status = await connectedAPI.getConnectionStatus();
  console.log('Connected:', status);
  
  return connectedAPI;
}

// Helper: Show wallet selection UI
async function showWalletSelector(wallets) {
  return new Promise((resolve) => {
    // Show UI with wallet options
    const modal = document.createElement('div');
    modal.innerHTML = `
      <div class="wallet-selector">
        <h3>Select Wallet</h3>
        ${wallets.map(w => `
          <button data-wallet="${w.id}">
            <img src="${w.icon}" alt="${w.name}">
            ${w.name}
          </button>
        `).join('')}
      </div>
    `;
    
    modal.addEventListener('click', (e) => {
      const button = e.target.closest('button');
      if (button) {
        const walletId = button.dataset.wallet;
        const wallet = wallets.find(w => w.id === walletId);
        modal.remove();
        resolve(wallet);
      }
    });
    
    document.body.appendChild(modal);
  });
}
```

### Example 2: Send Payment

```typescript
import { DUST_TOKEN_TYPE } from '@midnight-ntwrk/midnight-js-types';

async function sendPayment(
  recipientAddress: string,
  amount: bigint
) {
  // 1. Connect wallet
  const api = await connectWallet();
  
  // 2. Get current balance
  const balances = await api.getShieldedBalances();
  const balance = balances[DUST_TOKEN_TYPE] || 0n;
  
  console.log(`Current balance: ${balance}`);
  
  // 3. Check sufficient funds
  if (balance < amount) {
    throw new Error(`Insufficient balance. Have ${balance}, need ${amount}`);
  }
  
  // 4. Create transfer transaction
  const tx = await api.makeTransfer([{
    kind: 'shielded',
    tokenType: DUST_TOKEN_TYPE,
    value: amount,
    recipient: recipientAddress
  }]);
  
  console.log('Transaction created');
  
  // 5. Submit transaction
  const txHash = await api.submitTransaction(tx);
  console.log('Transaction submitted:', txHash);
  
  // 6. Wait for confirmation (optional)
  await waitForConfirmation(txHash);
  console.log('Transaction confirmed!');
  
  return txHash;
}

// Helper: Wait for transaction confirmation
async function waitForConfirmation(
  txHash: string,
  timeout = 60000
): Promise<void> {
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeout) {
    try {
      const tx = await queryTransaction(txHash);
      if (tx.confirmed) {
        return;
      }
    } catch (error) {
      // Transaction not found yet
    }
    
    await sleep(5000);
  }
  
  throw new Error('Transaction confirmation timeout');
}
```

### Example 3: Private Token Swap

```typescript
import { DUST_TOKEN_TYPE } from '@midnight-ntwrk/midnight-js-types';

// Party A: Create swap offer
async function createSwapOffer(
  offerAmount: bigint,
  requestTokenType: TokenType,
  requestAmount: bigint
) {
  const api = await connectWallet();
  
  // Get recipient address for requested tokens
  const myAddress = (await api.getShieldedAddresses())[0];
  
  // Create unbalanced transaction (offer without receiving)
  const unbalancedTx = await api.makeIntent(
    // Inputs: What we're offering
    [{
      kind: 'shielded',
      tokenType: DUST_TOKEN_TYPE,
      value: offerAmount,
      recipient: '' // Will be filled by counterparty
    }],
    // Outputs: What we want to receive
    [{
      kind: 'shielded',
      tokenType: requestTokenType,
      value: requestAmount,
      recipient: myAddress
    }]
  );
  
  console.log('Swap offer created');
  
  // Serialize and share with counterparty
  const serialized = serializeTransaction(unbalancedTx);
  return serialized;
}

// Party B: Complete swap
async function completeSwap(
  serializedOffer: string
) {
  const api = await connectWallet();
  
  // Deserialize offer
  const offerTx = deserializeTransaction(serializedOffer);
  
  // Balance the transaction (add our side)
  const balancedTx = await api.balanceSealedTransaction(offerTx);
  
  console.log('Swap balanced');
  
  // Submit completed swap
  const txHash = await api.submitTransaction(balancedTx);
  console.log('Swap submitted:', txHash);
  
  return txHash;
}
```

### Example 4: Delegate Proof Generation

```typescript
import { FetchZkConfigProvider } from '@midnight-ntwrk/midnight-js-fetch-zk-config-provider';

async function delegateProving() {
  // 1. Connect wallet
  const api = await connectWallet();
  
  // 2. Get wallet's configuration (includes proof server)
  const config = await api.getConfiguration();
  console.log('Proof server:', config.proverServerUri);
  
  // 3. Create key material provider
  const keyMaterialProvider = new FetchZkConfigProvider(
    config.proverServerUri
  );
  
  // 4. Get proving provider from wallet
  const provingProvider = await api.getProvingProvider(keyMaterialProvider);
  
  // 5. Prepare transaction
  const tx = await api.makeTransfer([{
    kind: 'shielded',
    tokenType: DUST_TOKEN_TYPE,
    value: 1000n,
    recipient: recipientAddress
  }]);
  
  // 6. Proof is generated automatically by wallet's proof server
  console.log('Proof generated by wallet');
  
  // 7. Submit transaction
  const txHash = await api.submitTransaction(tx);
  console.log('Transaction submitted:', txHash);
  
  return txHash;
}
```

### Example 5: Query Blockchain Data

```typescript
import { getBlock, getTransaction, getBalance } from '@midnight-ntwrk/ledger';

async function queryBlockchainData() {
  const indexerUri = 'https://indexer.testnet.midnight.network';
  
  // 1. Get latest block
  const latestBlock = await getLatestBlock(indexerUri);
  console.log('Latest block:', latestBlock.number);
  console.log('Transactions:', latestBlock.transactions.length);
  
  // 2. Get specific block
  const block = await getBlock(12345n, indexerUri);
  console.log('Block 12345 hash:', block.hash);
  
  // 3. Query transactions in block
  for (const txHash of block.transactions.slice(0, 5)) {
    const tx = await getTransaction(txHash, indexerUri);
    console.log(`Transaction ${txHash}:`);
    console.log(`  From: ${tx.from}`);
    console.log(`  To: ${tx.to}`);
    console.log(`  Value: ${tx.value}`);
  }
  
  // 4. Get account balance
  const balance = await getBalance(myAddress, indexerUri);
  console.log('Balance:', balance);
  
  return {
    latestBlock,
    block,
    balance
  };
}
```

### Example 6: Contract Interaction

```typescript
import { Contract } from '@midnight-ntwrk/midnight-js-contracts';

async function interactWithContract(contractAddress: string) {
  // 1. Connect wallet
  const api = await connectWallet();
  
  // 2. Create contract instance
  const contract = new Contract({
    address: contractAddress,
    network: 'testnet',
    wallet: api
  });
  
  // 3. Query contract state (read-only)
  const counter = await contract.query('getCounter');
  console.log('Current counter:', counter);
  
  // 4. Call contract method (state-changing)
  const tx = await contract.call('increment', []);
  console.log('Increment transaction:', tx);
  
  // 5. Wait for confirmation
  await waitForConfirmation(tx);
  
  // 6. Verify state changed
  const newCounter = await contract.query('getCounter');
  console.log('New counter:', newCounter);
  
  return newCounter;
}
```

### Example 7: Multi-Token Transfer

```typescript
async function multiTokenTransfer(
  recipients: Array<{
    address: string;
    tokenType: TokenType;
    amount: bigint;
  }>
) {
  const api = await connectWallet();
  
  // 1. Check balances for all token types
  const balances = await api.getShieldedBalances();
  
  for (const recipient of recipients) {
    const balance = balances[recipient.tokenType] || 0n;
    if (balance < recipient.amount) {
      throw new Error(
        `Insufficient ${recipient.tokenType}: have ${balance}, need ${recipient.amount}`
      );
    }
  }
  
  // 2. Create multi-output transaction
  const outputs = recipients.map(r => ({
    kind: 'shielded' as const,
    tokenType: r.tokenType,
    value: r.amount,
    recipient: r.address
  }));
  
  const tx = await api.makeTransfer(outputs);
  
  // 3. Submit transaction
  const txHash = await api.submitTransaction(tx);
  console.log('Multi-token transfer submitted:', txHash);
  
  return txHash;
}
```

### Example 8: Event Listening

```typescript
import { getEvents } from '@midnight-ntwrk/ledger';

async function listenToContractEvents(contractAddress: string) {
  const indexerUri = 'https://indexer.testnet.midnight.network';
  let lastBlock = await getLatestBlock(indexerUri);
  
  console.log('Listening for events...');
  
  // Poll for new events
  setInterval(async () => {
    const currentBlock = await getLatestBlock(indexerUri);
    
    if (currentBlock.number > lastBlock.number) {
      // Get events from new blocks
      const events = await getEvents({
        address: contractAddress,
        fromBlock: lastBlock.number + 1n,
        toBlock: currentBlock.number
      }, indexerUri);
      
      // Process events
      for (const event of events) {
        console.log('New event:', event);
        handleEvent(event);
      }
      
      lastBlock = currentBlock;
    }
  }, 5000); // Check every 5 seconds
}

function handleEvent(event: Event) {
  // Decode and process event
  switch (event.topics[0]) {
    case 'Transfer':
      console.log('Transfer event:', event.data);
      break;
    case 'Approval':
      console.log('Approval event:', event.data);
      break;
    default:
      console.log('Unknown event:', event);
  }
}
```

### Example 9: Batch Operations

```typescript
async function batchOperations() {
  const api = await connectWallet();
  
  // 1. Prepare multiple transactions
  const transactions = [
    api.makeTransfer([{
      kind: 'shielded',
      tokenType: DUST_TOKEN_TYPE,
      value: 100n,
      recipient: address1
    }]),
    api.makeTransfer([{
      kind: 'shielded',
      tokenType: DUST_TOKEN_TYPE,
      value: 200n,
      recipient: address2
    }]),
    api.makeTransfer([{
      kind: 'shielded',
      tokenType: DUST_TOKEN_TYPE,
      value: 300n,
      recipient: address3
    }])
  ];
  
  // 2. Create all transactions in parallel
  const txs = await Promise.all(transactions);
  
  // 3. Submit all transactions
  const txHashes = await Promise.all(
    txs.map(tx => api.submitTransaction(tx))
  );
  
  console.log('Submitted transactions:', txHashes);
  
  // 4. Wait for all confirmations
  await Promise.all(
    txHashes.map(hash => waitForConfirmation(hash))
  );
  
  console.log('All transactions confirmed!');
  
  return txHashes;
}
```

### Example 10: Error Handling

```typescript
async function robustPayment(
  recipientAddress: string,
  amount: bigint
) {
  try {
    // 1. Connect wallet with retry
    const api = await withRetry(() => connectWallet(), 3);
    
    // 2. Check balance
    const balances = await withRetry(
      () => api.getShieldedBalances(),
      3
    );
    
    const balance = balances[DUST_TOKEN_TYPE] || 0n;
    
    if (balance < amount) {
      throw new Error('INSUFFICIENT_FUNDS');
    }
    
    // 3. Create transaction
    const tx = await api.makeTransfer([{
      kind: 'shielded',
      tokenType: DUST_TOKEN_TYPE,
      value: amount,
      recipient: recipientAddress
    }]);
    
    // 4. Submit with retry
    const txHash = await withRetry(
      () => api.submitTransaction(tx),
      3
    );
    
    console.log('Transaction submitted:', txHash);
    
    // 5. Wait for confirmation with timeout
    await waitForConfirmation(txHash, 120000);
    
    return { success: true, txHash };
    
  } catch (error) {
    // Handle specific errors
    if (error.code === 'USER_REJECTED') {
      return { success: false, reason: 'User cancelled transaction' };
    }
    
    if (error.code === 'INSUFFICIENT_FUNDS') {
      return { success: false, reason: 'Insufficient balance' };
    }
    
    if (error.code === 'NETWORK_ERROR') {
      return { success: false, reason: 'Network connection failed' };
    }
    
    // Unknown error
    console.error('Payment failed:', error);
    return { success: false, reason: 'Transaction failed' };
  }
}

// Helper: Retry with exponential backoff
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * Math.pow(2, i));
    }
  }
  throw new Error('Max retries exceeded');
}

// Helper: Sleep utility
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

## Resources

- **DApp Connector API**: See dapp-connector-api.md
- **Wallet API**: See wallet-api.md
- **Ledger API**: See ledger-api.md
- **Integration Patterns**: See integration-patterns.md
- **Error Codes**: See error-codes.md

---
name: midnight-api
description: Comprehensive guide to Midnight Network APIs (v8.0+) for building decentralized applications. Use when users need to integrate Midnight APIs including Compact Runtime, DApp Connector, ZSwap, Wallet, and Ledger APIs, connect DApps to Midnight wallets, generate and verify zero-knowledge proofs programmatically, manage transactions and blockchain state, deploy and interact with Compact smart contracts, query blockchain data via indexer, implement wallet functionality, handle Zswap private transactions, and build complete web3 applications on Midnight.
---

# Midnight API Integration (v8.0+)

Complete guide to integrating Midnight Network APIs for building privacy-preserving decentralized applications.

## API Ecosystem Overview

Midnight provides multiple specialized APIs:

| API | Package | Version | Purpose |
|-----|---------|---------|---------|
| **Midnight.js** | `@midnight-ntwrk/midnight-js` | 4.0.4 | Complete TypeScript SDK |
| **Compact Runtime** | `@midnight-ntwrk/compact-runtime` | 0.16.0 | Execute contracts, generate ZK proofs |
| **DApp Connector** | `@midnight-ntwrk/dapp-connector-api` | 4.0.1 | Connect to wallets |
| **Ledger** | `@midnight/ledger` | 8.0.3 | Blockchain transactions |
| **Wallet SDK** | `@midnight-ntwrk/wallet-sdk-facade` | 3.0.0 | Unified wallet operations, key management, transfers |
| **Wallet API** | Various | Latest | Wallet operations |

## Quick Start

### Install Dependencies
```bash
npm install @midnight-ntwrk/midnight-js
npm install @midnight-ntwrk/dapp-connector-api
npm install @midnight-ntwrk/compact-runtime
npm install @midnight/ledger
npm install @midnight-ntwrk/wallet-sdk-facade
```

### Basic DApp Setup
```typescript
import { MidnightProvider } from '@midnight-ntwrk/midnight-js';
import { DAppConnector } from '@midnight-ntwrk/dapp-connector-api';

// Connect to Midnight
const connect = async () => {
  // Check for injected wallet
  if (typeof window !== 'undefined' && window.midnight) {
    const provider = new MidnightProvider(window.midnight);
    await provider.ready;
    return provider;
  }
  throw new Error('Midnight wallet not found');
};
```

## Core APIs

### 1. Midnight.js SDK (v4.0.4)

Complete JavaScript/TypeScript SDK for building DApps.

```typescript
import { 
  MidnightProvider,    // Main provider
  Wallet,             // Wallet connection
  Contract,           // Contract instance
  Transaction,        // Transaction builder
  findById,           // Indexer queries
} from '@midnight-ntwrk/midnight-js';

// Network configuration (REQUIRED)
const network = 'preprod'; // or 'testnet-02', 'mainnet'

// Initialize provider
const provider = await MidnightProvider.fetch({ network });

// Connect wallet
const wallet = await provider.wallet();
// Or use DApp connector
const connector = new DAppConnector();
await connector.ready;
```

### 2. DApp Connector API (v4.0.1)

Wallet connection interface.

```typescript
import { 
  InitialAPI,
  ConnectedAPI,
  Configuration,
  WalletConnectedAPI,
} from '@midnight-ntwrk/dapp-connector-api';

// Check for injected wallet
const getInitialAPI = (): InitialAPI | undefined => {
  return (window as any).midnight;
};

// Connect
const connect = async (): Promise<ConnectedAPI> => {
  const initial = getInitialAPI();
  if (!initial) throw new Error('Wallet not found');
  
  return await initial.connect();
};

// Get configuration (respects user privacy)
const config = await connected.getConfiguration();

// Get all addresses
const addresses = await connected.getAddresses();

// Get balance
const balance = await connected.getBalance();

// Make transfer
const tx = await connected.makeTransfer({
  to: recipientAddress,
  amount: 1000000n,
  token: 'midnight', // or custom token
});
```

### 3. Compact Runtime API (v0.16.0)

Execute Compact contracts and generate proofs.

```typescript
import {
  runProgram,
  createCircuitContext,
  createWitnessContext,
  ContractState,
  QueryContext,
} from '@midnight-ntwrk/compact-runtime';

// Run a circuit
const results = await runProgram(
  contract,           // Compiled contract
  'circuitName',     // Circuit to run
  { arg1: value1 }   // Arguments
);

// Create circuit context for proof generation
const ctx = await createCircuitContext(
  contract,
  arguments,
  provingKey
);

// Query ledger state
const state = await queryLedgerState(
  contractAddress,
  fieldName
);
```

### 4. Ledger API (v8.0.3)

Low-level blockchain operations.

```typescript
import {
  LedgerState,
  Transaction,
  runProgram,
  findById,
} from '@midnight/ledger';

// Submit transaction
const tx = await Transaction.create({
  contract,
  circuit: 'transfer',
  inputs: { to, amount },
  provingKey,
});
await tx.submit();

// Wait for confirmation
const receipt = await tx.wait();

// Query state
const state = await LedgerState.fetch(contractAddress);
const value = await state.get('fieldName');

// Query via indexer
const txs = await findById(txHash);
```

### 5. Indexer API

Query blockchain data.

```typescript
import { findById, findAll, findByKey } from '@midnight-ntwrk/midnight-js';

// Find transaction
const tx = await findById(txHash);

// Find by address
const txs = await findByAddress(address, {
  limit: 100,
  from: startBlock,
});

// Find by contract
const contractTxs = await findByContract(contractAddress);

// Query with filters
const results = await findAll({
  contract: contractAddress,
  circuit: 'transfer',
  fromBlock: 1000,
  toBlock: 2000,
});
```

## Wallet Integration Patterns

### React + Wallet Connection
```typescript
import { useMidnight } from '@midnight-ntwrk/midnight-react';

function WalletButton() {
  const { connect, disconnect, address, balance } = useMidnight();
  
  return address ? (
    <button onClick={disconnect}>
      Disconnect ({balance} TNS)
    </button>
  ) : (
    <button onClick={connect}>Connect Wallet</button>
  );
}
```

### Next.js + Wallet Connect
```typescript
// pages/api/auth.ts
import { MidnightAuth } from '@midnight-ntwrk/midnight-auth';

export default async function handler(req, res) {
  const { address, signature } = req.body;
  
  // Verify signature
  const isValid = await MidnightAuth.verify(address, message, signature);
  
  if (isValid) {
    // Create session
    const token = await MintToken.create({ address });
    res.json({ token });
  } else {
    res.status(401).json({ error: 'Invalid signature' });
  }
}
```

### Vanilla TypeScript
```typescript
// Simple wallet connection
class WalletConnection {
  private connector: DAppConnector;
  
  async connect(): Promise<string> {
    await this.connector.ready;
    const api = await this.connector.connect();
    const addresses = await api.getAddresses();
    return addresses[0];
  }
  
  async getBalance(): Promise<bigint> {
    const api = await this.connector.connect();
    return api.getBalance();
  }
}
```

## ZSwap Private Transactions

### Creating Shielded Transfers

```typescript
import {
  createZswapInput,
  createZswapOutput,
  ZswapLocalState,
  receiveShielded,
  sendShielded,
} from '@midnight-ntwrk/compact-runtime';

// Create input from received coin
const input = await createZswapInput(coinInfo);

// Create output for recipient
const output = await createZswapOutput({
  recipient: recipientAddress,
  amount: amount,
  token: tokenType,
});

// Receive to update local state
const newState = await receiveShielded(input);

// Send shielded tokens
const { tx, newState: finalState } = await sendShielded({
  inputs: [input],
  outputs: [output],
  change: changeOutput,
});
```

### Full Transfer Example
```typescript
import { 
  MidnightProvider, 
  findById,
} from '@midnight-ntwrk/midnight-js';

async function sendShielded(
  recipient: string,
  amount: bigint
): Promise<string> {
  const provider = await MidnightProvider.fetch({ 
    network: 'preprod' 
  });
  
  // Get unspent coins
  const coins = await provider.getCoins();
  
  // Select coins (UTXO model)
  const selected = selectCoins(coins, amount);
  
  // Create shielded transaction
  const tx = await provider.createTransaction({
    inputs: selected,
    outputs: [{
      recipient,
      amount,
    }],
    changeAddress: await provider.getChangeAddress(),
  });
  
  // Wait for confirmation
  return tx.submit();
}
```

## Smart Contract Deployment

### Compile and Deploy

```bash
# 1. Install tools
npm install @midnight-ntwrk/compact-tools

# 2. Compile contract
npx compact build my-contract.compact

# 3. Deploy
npx midnight-deploy --network preprod --contract my-contract.json
```

### Programmatic Deployment

```typescript
import { 
  MidnightProvider,
  Contract,
} from '@midnight-ntwrk/midnight-js';

async function deploy(
  contractPath: string,
  network: string = 'preprod'
): Promise<string> {
  const provider = await MidnightProvider.fetch({ network });
  
  // Read compiled contract
  const artifact = require(contractPath);
  
  // Deploy
  const tx = await Contract.deploy(artifact);
  await tx.submit();
  
  // Wait for confirmation
  const receipt = await tx.wait();
  
  return receipt.contractAddress;
}
```

## Real-World DApp Examples

### From midnight-awesome-dapps

#### Wallet Connection - midnight-wallet-cli
```typescript
// Using CLI for local development
// npm install midnight-wallet-cli
import { WalletCLI } from 'midnight-wallet-cli';

const wallet = new WalletCLI();
// Starts local DApp connector server
await wallet.serve();
// Then connect via http://localhost:9848
```

#### TypeScript SDK - Midday SDK
```typescript
// npm install @no-witness-labs/midday-sdk
import { MiddaySDK } from '@no-witness-labs/midday-sdk';

const sdk = new MiddaySDK({ network: 'preprod' });
const wallet = await sdk.wallet.connect();
```

#### React Integration
```typescript
// Using midnight-react
import { MidnightProvider } from '@midnight-ntwrk/midnight-react';

function App() {
  return (
    <MidnightProvider network="preprod">
      <YourDApp />
    </MidnightProvider>
  );
}
```

## Complete Code Examples

### 1. Connect Wallet
```typescript
import { DAppConnector } from '@midnight-ntwrk/dapp-connector-api';

async function connectWallet(): Promise<string | null> {
  const connector = new DAppConnector();
  await connector.ready;
  
  const api = await connector.connect();
  const addresses = await api.getAddresses();
  
  return addresses[0] ?? null;
}
```

### 2. Make Payment
```typescript
async function makePayment(
  toAddress: string,
  amount: bigint
): Promise<string> {
  const connector = new DAppConnector();
  await connector.ready;
  
  const api = await connector.connect();
  const result = await api.makeTransfer({
    to: toAddress,
    amount: amount,
  });
  
  return result.txId;
}
```

### 3. Query Balance
```typescript
async function getBalance(address: string): Promise<bigint> {
  const connector = new DAppConnector();
  await connector.ready;
  
  const api = await connector.connect();
  const balance = await api.getBalance();
  
  return balance;
}
```

### 4. Deploy Contract
```typescript
import { MidnightProvider } from '@midnight-ntwrk/midnight-js';

async function deployContract(
  artifact: any,
  network: string = 'preprod'
): Promise<string> {
  const provider = await MidnightProvider.fetch({ network });
  const tx = await provider.deploy(artifact);
  await tx.wait();
  
  return tx.contractAddress;
}
```

### 5. Call Contract Circuit
```typescript
async function callCircuit(
  contract: string,
  circuit: string,
  args: any
): Promise<any> {
  const provider = await MidnightProvider.fetch({ network: 'preprod' });
  
  const result = await provider.call({
    contract,
    circuit,
    args,
  });
  
  return result;
}
```

## Awesome DApp References for Learning

### Official Examples
- [Example Counter](https://github.com/midnightntwrk/example-counter)
- [Example Bboard](https://github.com/midnightntwrk/example-bboard)
- [Example ZK Loan](https://github.com/midnightntwrk/example-zkloan)

### SDKs and Tools
- [midnight-wallet-cli](https://github.com/nel349/midnight-wallet-cli-hub) - Terminal wallet
- [Midday SDK](https://github.com/no-witness-labs/midday-sdk) - TypeScript SDK
- [Create Midnight App](https://github.com/midnightntwrk/create-mn-app) - CLI scaffold

### DeFi Integration
- [LunarSwap](https://github.com/OpenZeppelin/midnight-apps) - DEX
- [Hydra Stake](https://github.com/statera-protocol/hydra-stake-protocol) - Staking
- [Statera Protocol](https://github.com/statera-protocol/statera-protocol-midnight) - Stablecoin

### Identity
- [Midnight Identity](https://github.com/bricktowers/midnight-identity) - ZK identity
- [Midnight Cloak](https://github.com/subc0der/midnight-cloak) - ZK verification

## Additional Resources

- [Midnight.js Docs](https://docs.midnight.network/api-reference)
- [DApp Connector Spec](https://docs.midnight.network/api-reference/dapp-connector)
- [Ledger API](https://docs.midnight.network/api-reference/ledger)
- [Compact Runtime](https://docs.midnight.network/api-reference/compact-runtime)

### Network Endpoints (Official)

| Network | RPC URL | Indexer | Faucet | Explorer | Status |
|---------|-------|--------|-------|----------|--------|
| Mainnet | https://rpc.mainnet.midnight.network | https://indexer.mainnet.midnight.network/api/v4/graphql | - | - | Production |
| Preprod | https://rpc.preprod.midnight.network | https://indexer.preprod.midnight.network/api/v4/graphql | https://faucet.preprod.midnight.network | https://explorer.preprod.midnight.network | Active |
| Preview | https://rpc.preview.midnight.network | https://indexer.preview.midnight.network/api/v4/graphql | https://faucet.preview.midnight.network | https://explorer.preview.midnight.network | Discontinued |

**⚠️ Important**: Both Testnet-02 and Preview are **discontinued**. Use **Preprod** for all testing.

**Preprod** is the active test network where:
- DUST must be generated programmatically (see midnight-dust-generator)
- tNIGHT available from [Preprod faucet](https://faucet.preprod.midnight.network)

### Troubleshooting

- **Wallet not found**: Install Lace wallet or use midnight-wallet-cli
- **Network mismatch**: Always call `setNetworkId()` before operations
- **Insufficient balance**: Use faucet for testnet tokens
- **Proof generation failing**: Check proof server is running
- **Transaction rejected**: Check fees and account state

### Lace Wallet Configuration

When using local networks (like `undeployed`), ensure Lace is configured correctly:

1. Open Lace Wallet → Settings → Midnight
2. Select **Undeployed** network (not Preprod or Mainnet)
3. Click Save configuration

## Cross Reference Skills

This skill covers API integration and DApp plumbing. For related areas see these skills.

- **midnight-concepts** — Architecture, privacy, ZK proofs, tokenomics
- **midnight-compact** — Smart contract syntax, types, ledger operations, ZK patterns
- **midnight-network** — Node operations, indexer setup, proof server deployment
- **midnight-wallet** — Wallet SDK, shielded/unshielded transactions, key management
- **midnight-dapp-dev** — Frontend scaffolds, wallet connect UI, provider setup
- **midnight-expert** — Health diagnostics, fact checking, version compatibility

### Inline References

- Verification methods: `references/verification-methods.md`
- Code quality pipeline: `references/quality-pipeline.md`
- Error catalog: `references/error-catalog.md`
- Plugin infrastructure: `references/infrastructure.md`

**Error: "Expected undeployed address, got Preprod address"**
- This means you're trying to use a Preprod address in the Undeployed network
- Switch Lace to use Undeployed network to get correct addresses
- Use the unshielded (mn1q...) address for the local network
# ZSwap API Reference

**Package**: `@midnight/zswap v3.0.2`

## Overview

ZSwap is Midnight's privacy-preserving transaction protocol. It enables:
- **Private transfers**: Shielded coin movements
- **Token management**: Multiple token types
- **Contract integration**: Private contract calls
- **Balance privacy**: Hidden amounts and owners

## Installation

```bash
yarn add @midnight/zswap
```

## Network Configuration

```typescript
import { setNetworkId, NetworkId } from '@midnight/zswap';

// Set network before any operations
setNetworkId(NetworkId.TestNet);
```

## Core Concepts

### Transaction Structure

Transactions execute in two phases:

1. **Guaranteed Phase**
   - Always executes
   - Fee payments
   - Fast operations
   - Cannot fail

2. **Fallible Phase**
   - May fail atomically
   - Contract calls
   - Complex operations
   - Rolls back on failure

```typescript
interface Transaction {
  guaranteedPhase: Offer;
  falliblePhase: Offer;
}
```

### Offer

An offer represents a set of coin movements.

```typescript
interface Offer {
  inputs: Input[];        // Coins being spent
  outputs: Output[];      // New coins created
  transients: Transient[]; // Temporary coins
  balance: Balance;       // Net token balance
}
```

**Balance**: Mapping from `TokenType` to net amount.

```typescript
type Balance = Map<TokenType, bigint>;
```

### Proof Stages

Transactions progress through proof stages:

```typescript
// 1. Initial (unproven)
type UnprovenTransaction = Transaction;

// 2. After proving
type ProvenTransaction = Transaction;

// 3. For testing (proof erased)
type ProofErasedTransaction = Transaction;
```

**Proving**: Convert unproven → proven via proof server.

## Coin Management

### CoinInfo

Basic coin information.

```typescript
interface CoinInfo {
  tokenType: TokenType;  // Token identifier
  value: bigint;         // Amount
  nonce: Field;          // Unique identifier
}
```

**Example:**
```typescript
const coin: CoinInfo = {
  tokenType: DUST_TOKEN_TYPE,
  value: 1000n,
  nonce: generateNonce()
};
```

### QualifiedCoinInfo

CoinInfo with Merkle tree position for spending.

```typescript
interface QualifiedCoinInfo extends CoinInfo {
  index: bigint;  // Position in Merkle tree
}
```

**Purpose**: Proves coin exists in ledger state.

### TokenType

Identifies token types.

```typescript
type TokenType = Bytes<32>;

// Built-in token
const DUST_TOKEN_TYPE: TokenType;
```

**Custom tokens:**
```typescript
import { customTokenType } from '@midnight/zswap';

const myToken = customTokenType('my-token-id');
```

## Creating Inputs

### User-Owned Input

Spend coins from user wallet.

```typescript
import { Input } from '@midnight/zswap';

const input = Input.fromQualifiedCoinInfo(
  qualifiedCoinInfo,
  zswapLocalState  // User's local state
);
```

**Requirements:**
- Coin must exist in wallet
- Must have spending key
- Coin must be unspent

### Contract-Owned Input

Spend coins from contract.

```typescript
const input = Input.fromQualifiedCoinInfo(
  qualifiedCoinInfo,
  contractAddress  // Contract's address
);
```

**Requirements:**
- Contract must authorize spend
- Coin must be owned by contract

## Creating Outputs

### User-Owned Output

Send coins to user.

```typescript
import { Output } from '@midnight/zswap';

const output = Output.fromCoinInfo(
  coinInfo,
  userPublicKey  // Recipient's public key
);
```

**Privacy**: Recipient and amount are hidden.

### Contract-Owned Output

Send coins to contract.

```typescript
const output = Output.fromCoinInfo(
  coinInfo,
  contractAddress  // Contract's address
);
```

**Use when**: Contract needs to hold coins.

## State Management

### ZswapChainState

On-chain state of ZSwap protocol.

```typescript
interface ZswapChainState {
  // Merkle tree of all coins
  coinTree: MerkleTree;
  
  // Current block height
  blockHeight: bigint;
  
  // Get coin by index
  getCoin(index: bigint): CoinInfo | null;
}
```

**Access:**
```typescript
import { getZswapChainState } from '@midnight/zswap';

const chainState = await getZswapChainState(provider);
```

### ZswapLocalState

Local wallet state (private).

```typescript
interface ZswapLocalState {
  // User's spending key
  spendingKey: PrivateKey;
  
  // User's public key
  publicKey: PublicKey;
  
  // Owned coins
  coins: QualifiedCoinInfo[];
  
  // Get balance
  getBalance(tokenType: TokenType): bigint;
}
```

**Initialization:**
```typescript
import { ZswapLocalState } from '@midnight/zswap';

const localState = new ZswapLocalState(spendingKey);
await localState.sync(chainState);
```

## Building Transactions

### Simple Transfer

```typescript
import { 
  TransactionBuilder, 
  DUST_TOKEN_TYPE 
} from '@midnight/zswap';

// 1. Create builder
const builder = new TransactionBuilder();

// 2. Add input (sender's coin)
const senderCoin = localState.coins.find(c => 
  c.tokenType === DUST_TOKEN_TYPE && c.value >= 1000n
);
builder.addInput(Input.fromQualifiedCoinInfo(senderCoin, localState));

// 3. Add output (recipient)
builder.addOutput(Output.fromCoinInfo(
  { tokenType: DUST_TOKEN_TYPE, value: 1000n, nonce: generateNonce() },
  recipientPublicKey
));

// 4. Add change output (back to sender)
const change = senderCoin.value - 1000n - FEE;
builder.addOutput(Output.fromCoinInfo(
  { tokenType: DUST_TOKEN_TYPE, value: change, nonce: generateNonce() },
  localState.publicKey
));

// 5. Build unproven transaction
const unprovenTx = builder.build();

// 6. Prove transaction
const provenTx = await proveTransaction(unprovenTx, proofServer);

// 7. Submit
await submitTransaction(provenTx, provider);
```

### Multi-Token Transfer

```typescript
const builder = new TransactionBuilder();

// Transfer DUST
builder.addInput(Input.fromQualifiedCoinInfo(dustCoin, localState));
builder.addOutput(Output.fromCoinInfo(
  { tokenType: DUST_TOKEN_TYPE, value: 500n, nonce: generateNonce() },
  recipientPublicKey
));

// Transfer custom token
builder.addInput(Input.fromQualifiedCoinInfo(customCoin, localState));
builder.addOutput(Output.fromCoinInfo(
  { tokenType: MY_TOKEN_TYPE, value: 100n, nonce: generateNonce() },
  recipientPublicKey
));

const unprovenTx = builder.build();
```

### Contract Call with Payment

```typescript
const builder = new TransactionBuilder();

// Guaranteed phase: Pay fee
builder.guaranteedPhase.addInput(Input.fromQualifiedCoinInfo(feeCoin, localState));

// Fallible phase: Contract call + payment
builder.falliblePhase.addInput(Input.fromQualifiedCoinInfo(paymentCoin, localState));
builder.falliblePhase.addOutput(Output.fromCoinInfo(
  { tokenType: DUST_TOKEN_TYPE, value: 1000n, nonce: generateNonce() },
  contractAddress
));

// Add contract call
builder.falliblePhase.addContractCall(contractAddress, 'myMethod', args);

const unprovenTx = builder.build();
```

## Transient Coins

Coins created and spent in same transaction.

```typescript
import { Transient } from '@midnight/zswap';

const builder = new TransactionBuilder();

// Create transient coin
const transientCoin: CoinInfo = {
  tokenType: DUST_TOKEN_TYPE,
  value: 500n,
  nonce: generateNonce()
};

// Add as transient (created then spent)
builder.addTransient(Transient.fromCoinInfo(transientCoin));

// Use in contract call
builder.addContractCall(contractAddress, 'process', [transientCoin]);
```

**Use when**: Temporary coins for contract logic.

## Balance Checking

### Check Offer Balance

```typescript
const offer: Offer = builder.guaranteedPhase;

// Get balance for token type
const dustBalance = offer.balance.get(DUST_TOKEN_TYPE) ?? 0n;

// Check if balanced
const isBalanced = Array.from(offer.balance.values()).every(v => v === 0n);
```

**Balanced offer**: All inputs = all outputs (per token type).

### Check Wallet Balance

```typescript
const balance = localState.getBalance(DUST_TOKEN_TYPE);
console.log(`DUST balance: ${balance}`);

// Check sufficient funds
if (balance < 1000n) {
  throw new Error('Insufficient funds');
}
```

## Proving Transactions

### Using Proof Server

```typescript
import { proveTransaction } from '@midnight/zswap';

const provenTx = await proveTransaction(
  unprovenTx,
  proofServerUrl
);
```

**Proof server**: Generates zero-knowledge proofs.

### Local Proving (Testing)

```typescript
import { eraseProof } from '@midnight/zswap';

// For testing only - no real proof
const testTx = eraseProof(unprovenTx);
```

**Warning**: Only use in test environments.

## Submitting Transactions

```typescript
import { submitTransaction } from '@midnight/zswap';

const txHash = await submitTransaction(
  provenTx,
  provider
);

console.log(`Transaction submitted: ${txHash}`);

// Wait for confirmation
const receipt = await provider.waitForTransaction(txHash);
console.log(`Confirmed in block: ${receipt.blockNumber}`);
```

## Privacy Features

### Hidden Amounts

All coin values are hidden on-chain.

```typescript
// Only sender and recipient know the amount
const output = Output.fromCoinInfo(
  { tokenType: DUST_TOKEN_TYPE, value: 1000n, nonce: generateNonce() },
  recipientPublicKey
);
```

### Hidden Owners

Coin ownership is private.

```typescript
// Only owner can identify their coins
const myCoins = await localState.scanForCoins(chainState);
```

### Unlinkability

Inputs and outputs cannot be linked.

```typescript
// Observer cannot tell which input funded which output
builder.addInput(input1);
builder.addInput(input2);
builder.addOutput(output1);
builder.addOutput(output2);
```

## Complete Example: Private Payment

```typescript
import {
  setNetworkId,
  NetworkId,
  ZswapLocalState,
  TransactionBuilder,
  Input,
  Output,
  DUST_TOKEN_TYPE,
  proveTransaction,
  submitTransaction,
  generateNonce
} from '@midnight/zswap';

async function sendPrivatePayment(
  localState: ZswapLocalState,
  recipientPublicKey: PublicKey,
  amount: bigint,
  provider: Provider,
  proofServer: string
) {
  // 1. Set network
  setNetworkId(NetworkId.TestNet);
  
  // 2. Check balance
  const balance = localState.getBalance(DUST_TOKEN_TYPE);
  const fee = 10n;
  const total = amount + fee;
  
  if (balance < total) {
    throw new Error(`Insufficient balance: ${balance} < ${total}`);
  }
  
  // 3. Select coin to spend
  const coin = localState.coins.find(c =>
    c.tokenType === DUST_TOKEN_TYPE && c.value >= total
  );
  
  if (!coin) {
    throw new Error('No suitable coin found');
  }
  
  // 4. Build transaction
  const builder = new TransactionBuilder();
  
  // Input: Spend coin
  builder.addInput(Input.fromQualifiedCoinInfo(coin, localState));
  
  // Output: Payment to recipient
  builder.addOutput(Output.fromCoinInfo(
    { tokenType: DUST_TOKEN_TYPE, value: amount, nonce: generateNonce() },
    recipientPublicKey
  ));
  
  // Output: Change back to sender
  const change = coin.value - total;
  if (change > 0n) {
    builder.addOutput(Output.fromCoinInfo(
      { tokenType: DUST_TOKEN_TYPE, value: change, nonce: generateNonce() },
      localState.publicKey
    ));
  }
  
  // 5. Build unproven transaction
  const unprovenTx = builder.build();
  
  // 6. Prove transaction
  console.log('Generating proof...');
  const provenTx = await proveTransaction(unprovenTx, proofServer);
  
  // 7. Submit transaction
  console.log('Submitting transaction...');
  const txHash = await submitTransaction(provenTx, provider);
  
  // 8. Wait for confirmation
  console.log(`Transaction submitted: ${txHash}`);
  const receipt = await provider.waitForTransaction(txHash);
  console.log(`Confirmed in block: ${receipt.blockNumber}`);
  
  // 9. Update local state
  await localState.sync(await getZswapChainState(provider));
  
  return txHash;
}
```

## Best Practices

### 1. Always Balance Offers

```typescript
// ✅ Balanced: inputs = outputs
builder.addInput(Input.fromQualifiedCoinInfo(coin1000, localState));
builder.addOutput(Output.fromCoinInfo(coin1000, recipient));

// ❌ Unbalanced: will fail
builder.addInput(Input.fromQualifiedCoinInfo(coin1000, localState));
builder.addOutput(Output.fromCoinInfo(coin500, recipient));
// Missing 500 output!
```

### 2. Use Unique Nonces

```typescript
// ✅ Generate fresh nonce
const nonce1 = generateNonce();
const nonce2 = generateNonce();

// ❌ Reusing nonce
const nonce = generateNonce();
const coin1 = { tokenType, value: 100n, nonce };
const coin2 = { tokenType, value: 200n, nonce };  // WRONG
```

### 3. Sync Local State

```typescript
// ✅ Sync before building transaction
await localState.sync(chainState);
const balance = localState.getBalance(DUST_TOKEN_TYPE);

// ❌ Stale state
const balance = localState.getBalance(DUST_TOKEN_TYPE);  // May be outdated
```

### 4. Handle Fees

```typescript
// ✅ Account for fees
const total = amount + FEE;
if (balance < total) {
  throw new Error('Insufficient funds for amount + fee');
}

// ❌ Forgetting fees
if (balance < amount) {  // Will fail when fee is added
  throw new Error('Insufficient funds');
}
```

### 5. Use Guaranteed Phase for Fees

```typescript
// ✅ Fee in guaranteed phase
builder.guaranteedPhase.addInput(feeCoin);

// ❌ Fee in fallible phase
builder.falliblePhase.addInput(feeCoin);  // May fail, losing fee
```

## Resources

- **API Documentation**: https://docs.midnight.network/api-reference/zswap
- **Privacy Mechanisms**: See privacy-mechanisms.md (midnight-concepts)
- **Compact Integration**: See compact-runtime-api.md
- **Network Configuration**: See network-configuration.md

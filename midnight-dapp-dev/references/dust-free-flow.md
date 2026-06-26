# Dust-Free Transaction Flow with 1AM Wallet

## Overview

The 1AM wallet abstracts DUST management away from users, providing a seamless transaction experience on the Midnight Network. Users never need to acquire, hold, or spend DUST tokens to pay for contract interactions. This reference explains how the dust-free flow works and how it compares to the standard flow.

## How the 1AM Wallet Eliminates DUST Management

### The DUST Problem

On Midnight, every transaction requires DUST tokens to pay for computational resources, including proof generation and ledger updates. Without the 1AM wallet, the user experience involves:

- Acquiring DUST tokens through a separate initial transaction
- Monitoring DUST balance to ensure sufficient funds for each operation
- Handling DUST exhaustion errors when balance runs low
- Managing multiple wallet types (shielded wallet for balances, dust wallet for fees)

### The 1AM Solution

The 1AM wallet consolidates these concerns into a single provider layer. When a user initiates a contract call, the wallet:

1. Checks whether the user has sufficient DUST to cover the transaction
2. If not, automatically triggers a DUST generation request
3. Waits for the DUST generation to complete
4. Proceeds with the requested contract call
5. Returns only the result of the contract call to the application

From the developer perspective, the application code is identical regardless of whether DUST needs to be generated. From the user perspective, there is no concept of DUST at all.

## DUST Generation Behind the Scenes

### Standard DUST Generation Flow

In a standard Midnight setup without 1AM, DUST generation follows this explicit flow:

```
User --> DustWallet.generateDust() --> Wait for transaction confirmation --> Check DUST balance --> Proceed with contract call
```

This requires the user (or the application) to:

1. Create a dedicated dust wallet
2. Call the `generateDust` method
3. Monitor transaction status
4. Verify the resulting DUST balance
5. Only then proceed with the intended contract interaction

### 1AM DUST Generation Flow

With the 1AM wallet, this flow is entirely transparent:

```
User --> contract.call.method() --> [1AM internally checks DUST, generates if needed] --> Returns result
```

The steps inside the brackets are handled by the 1AM provider without any application code changes.

## Transaction Fee Abstraction

### Fee Calculation

The 1AM wallet calculates the required DUST for each transaction based on:

- The circuit complexity (number of constraints in the ZK proof)
- The ledger operations (reads, writes, appends)
- The token operations (zswap deposits and withdrawals)
- Network congestion parameters

### Fee Sponsorship

The 1AM wallet uses a sponsorship model where DUST costs are covered at the wallet infrastructure level rather than charged to individual users. This enables applications to offer a frictionless onboarding experience without requiring users to first acquire tokens.

## Provider Chain for Dust-Free Operations

The 1AM wallet integrates with the Midnight provider chain as follows:

```
Application Code
    |
    v
Wallet Provider (1AM)
    |
    v
Proof Provider
    |
    +-----> DUST balance check
    |
    +-----> DUST generation (if needed)
    |
    +-----> Proof generation
    |
    v
Public Data Provider
    |
    v
Midnight Network
```

The application only needs to configure the wallet and proof providers. The public data provider handles transaction submission.

## Comparison: With DUST vs Without DUST

### User Experience Without 1AM

```
1. Install wallet extension
2. Create account
3. Acquire initial tNIGHT tokens
4. Generate DUST tokens (separate transaction, wait for confirmation)
5. Check DUST balance
6. Deposit tNIGHT into vault (first real action)
7. If DUST runs out, repeat steps 4-5
8. Withdraw tNIGHT from vault
```

Total user-perceived steps before first value-generating action: 5

### User Experience With 1AM

```
1. Install 1AM wallet extension
2. Create account
3. Acquire tNIGHT tokens
4. Deposit tNIGHT into vault (first real action)
5. Withdraw tNIGHT from vault
```

Total user-perceived steps before first value-generating action: 3

### Code Comparison

**Without 1AM wallet:**

```typescript
import { DustWalletBuilder, ShieldedWalletBuilder } from '@midnight-ntwrk/wallet-sdk';
import { providers } from '@midnight-ntwrk/midnight-js';

async function depositWithout1AM(amount: bigint) {
  const seed = getSeedFromEnv();

  const dustWallet = await DustWalletBuilder.build(providers);
  const dustTx = await dustWallet.generateDust();
  await dustTx.wait();

  const balance = await dustWallet.getBalance();
  if (balance === 0n) {
    throw new Error('Failed to generate DUST');
  }

  const shieldedWallet = await ShieldedWalletBuilder.build(providers, seed);
  const contract = await loadContract(providers, shieldedWallet);

  const tx = await contract.call.deposit(amount, shieldedWallet.publicKey);
  await tx.wait();

  console.log('Deposit complete. Transaction:', tx.hash);
}
```

**With 1AM wallet:**

```typescript
import { providers } from '@midnight-ntwrk/midnight-js';

async function depositWith1AM(amount: bigint) {
  const wallet = await window.midnight['1am'].connect();
  const contract = await loadContract(providers, wallet);

  const tx = await contract.call.deposit(amount, wallet.publicKey);
  await tx.wait();

  console.log('Deposit complete. Transaction:', tx.hash);
}
```

The 1AM version eliminates approximately 15 lines of explicit wallet and DUST management code. More importantly, it removes the DUST generation wait time from the user experience.

## Error Handling in Dust-Free Mode

Even with dust-free operation, certain errors can occur:

### Network Congestion

If the network is congested, DUST generation may take longer than expected. The 1AM wallet retries automatically and surfaces a timeout error if generation exceeds a threshold:

```typescript
try {
  await contract.call.deposit(amount, wallet.publicKey);
} catch (err) {
  if (err.message.includes('DUST generation timeout')) {
    console.log('Network is busy. Please try again in a moment.');
  }
}
```

### Wallet Disconnection

If the user disconnects their wallet during DUST generation, the operation fails:

```typescript
try {
  await contract.call.deposit(amount, wallet.publicKey);
} catch (err) {
  if (err.message.includes('wallet disconnected')) {
    console.log('Please reconnect your 1AM wallet and try again.');
  }
}
```

## Provider Configuration for 1AM

To enable dust-free operation, configure the providers to use the 1AM wallet:

```typescript
const providers = {
  proofProvider: createProofProvider(network),
  publicDataProvider: createPublicDataProvider(network),
  privateStateProvider: createPrivateStateProvider(network),
  walletProvider: window.midnight['1am'],
};
```

The `walletProvider` field is where the 1AM wallet is wired into the provider chain. If a different wallet is used, DUST management becomes the application's responsibility.

## Limitations and Considerations

- **Offline transactions**: Dust-free operation requires a network connection to generate DUST on demand. Offline flows need pre-generated DUST
- **High-volume operations**: Applications with extremely high transaction volumes may want to implement DUST pre-generation for predictable performance
- **Network dependency**: DUST generation depends on the network's ability to process transactions. During degraded network conditions, generation may be delayed
- **Fallback path**: Applications should provide a fallback error message if the 1AM wallet is not available, guiding users to install the extension

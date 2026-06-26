# DUST Operations

**Package**: `@midnight-ntwrk/wallet-sdk-facade`

## Overview

DUST is the fee token for the Midnight Network. Every transaction deploying a contract calling a circuit or transferring tokens consumes DUST. Without a sufficient DUST balance transactions will fail during submission. DUST is generated from existing unshielded NIGHT UTXOs through a registration and commitment process.

## DUST Tokenomics

- DUST is generated from unshielded NIGHT UTXOs at a fixed conversion rate
- Each DUST unit can only be spent once enforced via nullifiers
- DUST commitments are registered onchain before they can be consumed
- Generated DUST is associated with a specific dust address
- DUST balances are private and only visible to the dust wallet holder

The DUST supply grows organically as users register their NIGHT UTXOs. There is no separate DUST faucet or purchase mechanism.

## DUST Generation Process

### Step 1: Check NIGHT Balance

Before generating DUST you need unshielded NIGHT tokens:

```typescript
const state = await wallet.waitForSyncedState();
const nightBalance = state.unshielded.balances[NIGHT_TOKEN_TYPE];
```

### Step 2: Register UTXOs

Register unshielded NIGHT UTXOs for DUST generation. This creates onchain commitments that lock the UTXOs:

```typescript
await wallet.registerNightUtxosForDustGeneration();
```

### Step 3: Monitor Generation

DUST generation is asynchronous. Poll `DustGenerationState` until completion:

```typescript
const dustActions = wallet.dustActions();
let state = await dustActions.getLocalState();

while (state.generationState.status === 'pending') {
  await new Promise(resolve => setTimeout(resolve, 5000));
  state = await dustActions.getLocalState();
}
```

### Step 4: Verify Balance

```typescript
console.log('Available DUST:', state.dust.balance);
```

## DustActions Class

Access through the wallet facade:

```typescript
const dustActions = wallet.dustActions();
```

Available methods:
- `registerDust(params)` registers NIGHT UTXOs for DUST generation
- `getLocalState()` returns current `DustLocalState`
- `getState()` queries onchain DUST state
- `getGenerationState()` returns generation progress

## DustLocalState and DustState

```typescript
interface DustLocalState {
  balance: bigint;
  totalGenerated: bigint;
  totalSpent: bigint;
  generationState: DustGenerationState;
  pendingRegistrations: number;
}

interface DustState {
  balance: bigint;
  commitments: DustCommitment[];
  nullifiers: string[];
}
```

Local state may temporarily diverge from onchain state during pending registrations.

## DustParameters

```typescript
interface DustParameters {
  generationThreshold: bigint;   // minimum NIGHT to generate from
  maxRegistrations: number;      // max concurrent registrations
  retryDelayMs: number;          // delay between generation checks
  networkId: string;             // target network
}
```

## DustGenerationState

```typescript
type DustGenerationState =
  | { status: 'idle' }
  | { status: 'pending'; startedAt: number }
  | { status: 'processing'; blockHeight: number }
  | { status: 'complete'; txHash: string }
  | { status: 'failed'; error: string };
```

The pending state typically lasts a few seconds on Preprod. The processing state indicates the network is finalizing the commitment.

## DUST Nonce and Nullifier Management

```typescript
interface DustCommitment {
  nonce: bigint;
  value: bigint;
  dustAddress: string;
}

interface DustNullifier {
  nullifier: string;
  commitmentNonce: bigint;
}
```

Every commitment includes a nonce to prevent replay attacks. When DUST is spent the nullifier is published onchain to prevent double spending. The wallet SDK manages nonces and nullifiers automatically in normal usage.

## Generating DUST on Preprod

On Preprod you can generate DUST programmatically:
1. Request NIGHT from the Preprod faucet
2. Wait for the NIGHT to appear in your unshielded balance
3. Register the received UTXOs for DUST generation
4. Wait for DUST generation to complete

## FaucetClient

```typescript
import { FaucetClient } from '@midnight-ntwrk/wallet-sdk-facade';

const faucet = new FaucetClient('https://faucet.preprod.midnight.network');
await faucet.requestFunds(unshieldedAddress);
```

## waitForFunds Utility

```typescript
import { waitForFunds } from '@midnight-ntwrk/wallet-sdk-facade';

await waitForFunds({
  wallet: wallet,
  tokenType: NIGHT_TOKEN_TYPE,
  minimumBalance: 10_000_000n,
  timeoutMs: 120_000,
  pollIntervalMs: 5000,
});
```

Essential for test automation where you need deterministic fund availability.

## Error Recovery

- **Insufficient DUST**: Register more NIGHT UTXOs or wait for pending generation to complete
- **Registration failed**: Verify UTXOs are unshielded NIGHT and not already registered
- **Generation timeout**: Check network connectivity and indexer health then retry
- **Double spend detected**: Recreate the wallet with fresh keys

## Resources

- **Wallet SDK Overview**: See wallet-sdk.md
- **Key Management**: See key-management.md
- **Wallet Integration**: See ../midnight-dapp-dev/references/wallet-integration.md

# Transaction Flow

## Overview

Every Midnight transaction follows a lifecycle of creation proving submission and finalization. Understanding each phase is essential for debugging failures and building reliable DApps.

```
[Create Unproven] -> [Prove] -> [Submit] -> [Monitor] -> [Finalize]
```

## Create Unproven Transaction

### createUnprovenDeployTx

```typescript
import { createUnprovenDeployTx } from '@midnight-ntwrk/midnight-js';

const unprovenTx = await createUnprovenDeployTx(providers, {
  contractCode: compiledContract,
  constructorArgs: [arg1, arg2],
  deployerAddress: await wallet.getShieldedAddresses(),
});
```

### createUnprovenCallTx

```typescript
import { createUnprovenCallTx } from '@midnight-ntwrk/midnight-js';

const unprovenTx = await createUnprovenCallTx(providers, {
  contractAddress: deployedAddress,
  methodName: 'increment',
  methodArgs: [5n],
  callerAddress: await wallet.getShieldedAddresses(),
});
```

## Prove Transaction

### Proof Server Proving

```typescript
const provenTx = await unprovenTx.prove(providers.proofProvider, costModel);
```

### Wallet Proving

```typescript
const keyMaterialProvider = new FetchZkConfigProvider(proverUri);
const provingProvider = connectedAPI.getProvingProvider(keyMaterialProvider);
const provenTx = await unprovenTx.prove(provingProvider, costModel);
```

Preferred for browser DApps. Keeps proof generation close to user keys.

### Cost Model

```typescript
const costModel = {
  maxBudget: 1_000_000n,  // max prover fee in DUST
  priorityFee: 100n,      // tip for faster proving
};
```

### Submit Transaction

```typescript
const result = await providers.walletProvider.submitDeployTx(provenTx);
const result = await providers.walletProvider.submitCallTx(provenTx);
const { txHash } = await connectedAPI.submitTransaction(provenTx);
```

Sends the proven transaction to a Midnight node.

## Monitor Transaction Status

```typescript
function waitForFinalization(txHash: string, providers: MidnightProviders): Promise<TxResult> {
  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      const status = await providers.publicDataProvider.queryTransaction(txHash);
      if (status.finalized) { clearInterval(interval); resolve(status.result); }
      if (status.failed) { clearInterval(interval); reject(new Error(status.error)); }
    }, 3000);
  });
}
```

Poll the indexer at regular intervals. Three seconds is a reasonable default for Preprod.

## Transaction Result Interpretation

```typescript
type TxResult =
  | { type: 'success'; effects: TxEffects }
  | { type: 'partialSuccess'; segments: SegmentResult[] }
  | { type: 'failure'; error: string };
```

**Success**: All effects applied. **Partial Success**: Some segments failed. **Failure**: No effects applied.

## SegmentSuccess and SegmentFail

```typescript
interface SegmentSuccess {
  status: 'success';
  effects: TxEffects;
  segmentIndex: number;
}

interface SegmentFail {
  status: 'fail';
  error: string;
  segmentIndex: number;
  reason: FailReason;
}

type SegmentResult = SegmentSuccess | SegmentFail;
```

`FailReason` values: `InsufficientBalance` `InvalidWitness` `ContractError` `DustExhausted`.

## Error Handling Patterns

### Retry Logic

```typescript
async function submitWithRetry(
  providers: MidnightProviders,
  provenTx: ProvenTransaction,
  maxRetries: number = 3
): Promise<string> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const { txHash } = await providers.walletProvider.submitCallTx(provenTx);
      return txHash;
    } catch (error) {
      if (attempt === maxRetries) throw error;
      await new Promise(r => setTimeout(r, 2000 * attempt));
    }
  }
  throw new Error('Unreachable');
}
```

### Balance Validation

```typescript
async function validateBeforeCall(providers: MidnightProviders, requiredDust: bigint) {
  const balance = await wallet.getDustBalance();
  if (balance < requiredDust) {
    throw new APIError(ErrorCode.DUST_INSUFFICIENT,
      `Need ${requiredDust} DUST but only have ${balance}`);
  }
}
```

### Timeout Handling

```typescript
const proofTimeout = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Proof generation timed out')), 120_000)
);

const provenTx = await Promise.race([
  unprovenTx.prove(providers.proofProvider, costModel),
  proofTimeout,
]);
```

## Complete Flow Example

```typescript
async function deployAndCall() {
  const providers = await initializeMidnightProviders(config);
  await providers.start();
  try {
    const unprovenDeploy = await createUnprovenDeployTx(providers, deployArgs);
    const provenDeploy = await unprovenDeploy.prove(providers.proofProvider, costModel);
    const { txHash } = await providers.walletProvider.submitDeployTx(provenDeploy);
    const deployResult = await waitForFinalization(txHash, providers);
    const contractAddress = deployResult.effects.contractAddress;

    const unprovenCall = await createUnprovenCallTx(providers, {
      contractAddress, methodName: 'initialize', methodArgs: [],
    });
    const provenCall = await unprovenCall.prove(providers.proofProvider, costModel);
    const { txHash: callHash } = await providers.walletProvider.submitCallTx(provenCall);
    const callResult = await waitForFinalization(callHash, providers);
    return { contractAddress, callResult };
  } finally {
    await providers.stop();
  }
}
```

## Resources

- **Provider Architecture**: See provider-architecture.md
- **Wallet Integration**: See wallet-integration.md
- **DUST Operations**: See ../midnight-wallet/references/dust-operations.md

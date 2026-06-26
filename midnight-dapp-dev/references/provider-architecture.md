# Provider Architecture

**Package**: `@midnight-ntwrk/midnight-js-types`

## Overview

Midnight DApps interact with the network through a provider layer. Each provider handles a specific concern such as proof generation state queries or wallet operations. `MidnightProviders` composes these individual providers into a unified API.

## MidnightProviders Interface

```typescript
interface MidnightProviders {
  proofProvider: ProofProvider;
  publicDataProvider: PublicDataProvider;
  privateStateProvider: PrivateStateProvider;
  walletProvider: WalletProvider;
  zkConfigProvider: ZKConfigProvider;
}
```

Any DApp component needing network access should accept a `MidnightProviders` instance rather than individual providers to ensure consistent configuration.

## Individual Providers

### ProofProvider

Generates zero knowledge proofs via a proof server:

```typescript
interface ProofProvider {
  prove(tx: UnprovenTransaction, costModel: CostModel): Promise<ProvenTransaction>;
}
```

In browser contexts proofs delegate to the wallet's proving service. In server contexts proofs use a local or remote proof server.

### PublicDataProvider

Reads onchain state via the indexer GraphQL API:

```typescript
interface PublicDataProvider {
  queryContractState(contractAddress: string, query: ContractStateQuery): Promise<ContractState>;
  queryBlock(blockHeight: number): Promise<Block>;
  queryTransaction(txHash: string): Promise<Transaction>;
}
```

Public data includes deployed contract code ledger state and transaction history. No authentication required.

### PrivateStateProvider

Manages encrypted state visible only to the wallet holder:

```typescript
interface PrivateStateProvider {
  getPrivateState(contractAddress: string, encryptionKey: EncryptionSecretKey): Promise<DecryptedState>;
  watchPrivateState(contractAddress: string, key: EncryptionSecretKey, cb: (s: DecryptedState) => void): () => void;
}
```

Private state is encrypted onchain. Only wallets with the correct encryption key can decrypt it. `watchPrivateState` sets up real time subscriptions.

### WalletProvider

Bridges the DApp to the user's wallet for signing without exposing raw keys:

```typescript
interface WalletProvider {
  getAddresses(): Promise<WalletAddresses>;
  signTransaction(tx: Transaction): Promise<SignedTransaction>;
  getSigningKey(): Promise<SigningKey>;
}
```

### ZKConfigProvider

Supplies circuit artifacts and parameters for proof generation:

```typescript
interface ZKConfigProvider {
  getZkConfig(contractAddress: string): Promise<ZkConfig>;
}
```

ZK config includes proving key verification key and circuit metadata. Typically fetched from a remote server but can be bundled locally.

## initializeMidnightProviders Function

```typescript
import { initializeMidnightProviders } from '@midnight-ntwrk/midnight-js';

const providers = await initializeMidnightProviders({
  privateStateProvider: localStoragePrivateStateProvider,
  zkConfigProvider: new FetchZkConfigProvider(proverUri),
  walletProvider: connectedAPI,
});
```

Accepts partial provider configuration. Unspecified providers receive default implementations.

## Provider Initialization Flow

```typescript
async function setupProviders(): Promise<MidnightProviders> {
  const connectedAPI = await window.midnight.lace.connect(networkId);
  const config = await connectedAPI.getConfiguration();

  return initializeMidnightProviders({
    privateStateProvider: new IndexedDBPrivateStateProvider(),
    zkConfigProvider: new FetchZkConfigProvider(config.proverServerUri),
    walletProvider: connectedAPI,
  });
}
```

The flow validates provider dependencies initializes each provider asynchronously and returns the composed instance.

## Provider Configuration

```typescript
const proofProvider = new RemoteProofProvider({
  serverUri: 'http://localhost:6300',
  timeoutMs: 120_000,
  retries: 3,
});

const publicDataProvider = new IndexerPublicDataProvider({
  indexerUri: 'https://indexer.preprod.midnight.network',
  indexerWsUri: 'wss://indexer.preprod.midnight.network',
  networkId: 'preprod',
});
```

Always source provider URIs from the wallet's configuration rather than hardcoding them.

## Provider Lifecycle

```typescript
interface ProviderLifecycle {
  start(): Promise<void>;
  stop(): Promise<void>;
  isReady(): boolean;
}
```

`MidnightProviders` coordinates lifecycle across all child providers:

```typescript
await providers.start();
// ... use providers ...
await providers.stop();
```

## Provider Composition Patterns

### Read Only Client

Only needs to query public data. No wallet connection required:

```typescript
const readOnlyProviders = await initializeMidnightProviders({
  publicDataProvider: new IndexerPublicDataProvider(indexerConfig),
});
```

### Full Transaction Client

Deploys contracts and submits transactions. Needs all providers:

```typescript
const fullProviders = await initializeMidnightProviders({
  privateStateProvider: customPrivateStateProvider,
  zkConfigProvider: new FetchZkConfigProvider(proverUri),
  walletProvider: connectedAPI,
  publicDataProvider: new IndexerPublicDataProvider(indexerConfig),
});
```

### Local Development

Connects to local devnet Docker containers:

```typescript
const localProviders = await initializeMidnightProviders({
  zkConfigProvider: new FetchZkConfigProvider('http://localhost:6300'),
  publicDataProvider: new IndexerPublicDataProvider({
    indexerUri: 'http://localhost:32888/api/graphql',
    indexerWsUri: 'ws://localhost:32888/api/graphql/ws',
  }),
});
```

## Resources

- **Wallet Integration**: See wallet-integration.md
- **Transaction Flow**: See transaction-flow.md
- **Local Devnet**: See ../midnight-tooling/references/local-devnet.md

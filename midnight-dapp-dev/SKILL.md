---
name: midnight-dapp-dev
description: Comprehensive guide for Midnight Network DApp frontend development covering project scaffolding with Vite and React 19 plus shadcn/ui templates, Next.js wallet connector patterns via the DApp Connector API with App Router, React wallet connector with Vite setup, provider architecture including MidnightProviders, proof provider, public data provider, private state provider, wallet provider, and ZK config provider, wallet integration using DApp Connector API v4.0.1 with window.midnight, connect, disconnect, and request authorization flows, DApp Connector types covering Configuration, ConnectionStatus, ConnectedAPI, InitialAPI, WalletConnectedAPI, KeyMaterialProvider, and ProvingProvider, transaction flow from creating unproven transactions through proving, submitting, waiting for finalization, and handling transaction results, state management with public state queries via indexer and private state with level-private-state-provider, indexer public data provider for querying blockchain data, contract state, transactions, and blocks, level private state provider for encrypted local storage with password rotation and crypto backends, HTTP client proof provider for remote proving and proof server integration, DApp Connector proof provider for browser wallet proving including 1AM wallet and Lace wallet, fetch ZK config provider for fetching ZK configuration from the network, network ID management with getNetworkId, setNetworkId, and environment switching, logger provider for structured logging with LogLevel enum, contract integration with createCircuitCallTxInterface, createUnprovenCallTx, submitCallTx, and submitCallTxAsync, Vercel deployment with environment variables and production configuration, error handling covering CallTxFailedError, DeployTxFailedError, ContractTypeError, TxFailedError, and transaction result statuses, and DApp testing with Playwright E2E, testkit-js DAppConnectorWalletAdapter, and DAppConnectorInitialAPI.
---

# Midnight DApp Development

## Overview

Midnight DApp frontend development involves building web applications that interact with the Midnight Network blockchain using TypeScript and React. This guide covers the complete workflow from project scaffolding to production deployment. The Midnight ecosystem provides several TypeScript packages that enable wallet connections, contract interactions, state management, and ZK proof generation all from within a browser or Node.js application.

The core development pattern follows a provider based architecture where each concern such as wallet connectivity, proof generation, or state management is handled by a dedicated provider. These providers are composed together using the MidnightProviders abstraction which serves as the backbone of any Midnight DApp.

Developers typically use either Vite with React 19 for single page applications or Next.js with the App Router for server rendered applications. Both approaches support the full Midnight DApp Connector API for wallet integration.


## Project Scaffolding Patterns

### Vite Plus React 19 Plus shadcn/ui

The recommended Vite scaffolding pattern combines React 19 with TypeScript and shadcn/ui for building Midnight DApps. Start by creating a Vite project with React and TypeScript support.

```bash
npm create vite@latest my-midnight-dapp -- --template react-ts
cd my-midnight-dapp
npm install
```

Add the Midnight dependencies needed for a standard DApp frontend. The core packages include the DApp Connector for wallet integration and the various providers for state management and contract interaction.

```bash
npm install @midnight-ntwrk/dapp-connector-api
npm install @midnight-ntwrk/onchain-rpc-provider
npm install @midnight-ntwrk/midnight-js-types
npm install @midnight-ntwrk/midnight-js-contracts
npm install @midnight-ntwrk/midnight-js-level-private-state-provider
npm install @midnight-ntwrk/midnight-js-network-id
npm install @midnight-ntwrk/midnight-js-fetch-zk-config-provider
npm install @midnight-ntwrk/midnight-js-http-client-proof-provider
```

Install shadcn/ui following the standard CLI initialization. This requires tailwindcss and its associated configuration.

```bash
npx shadcn@latest init
npx shadcn@latest add button card input toast dialog
```

The project structure for a Midnight DApp should organize concerns clearly. Create directories for components, hooks, providers, contracts, and utilities.

```
src/
  components/
    wallet/
      ConnectButton.tsx
      WalletStatus.tsx
      BalanceDisplay.tsx
    contract/
      ContractForm.tsx
      TransactionResult.tsx
    layout/
      AppLayout.tsx
      Header.tsx
  hooks/
    useWallet.ts
    useContract.ts
    useMidnightProviders.ts
  providers/
    MidnightProviders.tsx
    wallet.ts
    proof.ts
    state.ts
  contracts/
    types.ts
    interaction.ts
  lib/
    midnight.ts
    utils.ts
  App.tsx
  main.tsx
```

### Next.js Wallet Connector

Next.js projects use the App Router pattern for Midnight DApp development. Create a Next.js application with TypeScript and the App Router enabled.

```bash
npx create-next-app@latest my-midnight-dapp --typescript --tailwind --app
cd my-midnight-dapp
```

Install the Midnight dependencies alongside the standard Next.js packages.

```bash
npm install @midnight-ntwrk/dapp-connector-api
npm install @midnight-ntwrk/midnight-js-types
npm install @midnight-ntwrk/midnight-js-contracts
npm install @midnight-ntwrk/midnight-js-level-private-state-provider
npm install @midnight-ntwrk/midnight-js-network-id
npm install @midnight-ntwrk/midnight-js-fetch-zk-config-provider
npm install @midnight-ntwrk/midnight-js-http-client-proof-provider
```

The App Router pattern for Midnight DApps requires careful handling of client side only components. The wallet connector and all blockchain interactions must run in the browser since they depend on the `window.midnight` API. Use the `'use client'` directive at the top of any file that interacts with the Midnight provider stack.

For the layout pattern create a root layout with metadata and a client side provider wrapper. The providers must be initialized in a client component and wrap the application at the layout level.

```
src/
  app/
    layout.tsx
    page.tsx
    providers.tsx
  components/
    wallet/
      ConnectButton.tsx
      WalletStatus.tsx
    contract/
      ContractForm.tsx
      TransactionResult.tsx
    ui/
      Button.tsx
      Card.tsx
      Input.tsx
  hooks/
    useWallet.ts
    useContract.ts
  lib/
    midnight.ts
    providers.ts
```

### React Wallet Connector With Vite

For projects that do not need Next.js features a simpler Vite plus React setup provides a lightweight alternative. This is suitable for single page DApps that do not require server side rendering.

```bash
npm create vite@latest my-midnight-dapp -- --template react-ts
cd my-midnight-dapp
npm install
npm install @midnight-ntwrk/dapp-connector-api @midnight-ntwrk/midnight-js-types
```

Wallet connection in a Vite React app follows the same DApp Connector API patterns. The initialization code checks for the `window.midnight` object and uses the connector API to establish a connection.

```typescript
import { useEffect, useState } from 'react';
import {
  type ConnectedAPI,
  type ConnectionStatus,
  DAppConnectorAPI
} from '@midnight-ntwrk/dapp-connector-api';

function useMidnightWallet() {
  const [api, setApi] = useState<ConnectedAPI | null>(null);
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');

  useEffect(() => {
    const midnight = window.midnight;
    if (!midnight) {
      setStatus('unavailable');
      return;
    }

    const connector = new DAppConnectorAPI(midnight);
    connector.connect().then((connectedApi) => {
      setApi(connectedApi);
      setStatus('connected');
    });

    return () => {
      connector.disconnect();
    };
  }, []);

  return { api, status };
}
```


## Provider Architecture

### MidnightProviders

The MidnightProviders abstraction is the central composition point for all provider services in a Midnight DApp. It combines the wallet provider, proof provider, public data provider, private state provider, and ZK config provider into a single interface that contracts consume.

The MidnightProviders type is generic over three parameters. The first parameter is the public state type which varies per contract. The second parameter is the wallet provider type. The third parameter is the private state type which can be void if the contract has no private state.

```typescript
type MidnightProviders<P, W extends WalletProvider, S> = {
  readonly publicDataProvider: PublicDataProvider<P>;
  readonly privateStateProvider: PrivateStateProvider<S>;
  readonly walletProvider: W;
  readonly zkConfigProvider: ZKConfigProvider<S>;
};
```

Building a MidnightProviders instance involves initializing each provider component and composing them together. The wallet provider comes from the DApp Connector connection. The public data provider wraps the indexer GraphQL endpoint. The private state provider manages encrypted local storage. The ZK config provider fetches circuit configuration from the network.

```typescript
async function buildProviders(walletAPI: ConnectedAPI): Promise<MidnightProviders<P, W, S>> {
  const walletProvider = new WalletProviderAdapter(walletAPI);
  const publicDataProvider = new IndexerPublicDataProvider(indexerUri);
  const privateStateProvider = await LevelPrivateStateProvider.create<P, S>({
    privateStateStoreName: 'my-dapp-state'
  });
  const zkConfigProvider = new FetchZkConfigProvider<S>(
    walletAPI.zkConfigUri,
    fetch
  );

  return {
    publicDataProvider,
    privateStateProvider,
    walletProvider,
    zkConfigProvider
  };
}
```

### Proof Provider

The proof provider handles zero knowledge proof generation for contract calls. There are two primary proof provider implementations available to DApp developers.

The DApp Connector Proof Provider relies on the browser wallet extension to generate proofs client side. This is the standard approach for end user applications where the wallet handles proving transparently.

```typescript
const proofProvider = new DAppConnectorProofProvider(connectedAPI);
```

The HTTP Client Proof Provider sends proving requests to a remote proof server. This is useful for server side proving or when the wallet does not support a particular proving scheme.

```typescript
const proofProvider = new HttpClientProofProvider(
  'https://proof-server.example.com',
  fetch
);
```

### Public Data Provider

The public data provider serves as the read interface to the Midnight blockchain. It wraps the GraphQL indexer API and provides typed access to contract state, transactions, and block data. All public state queries flow through this provider.

```typescript
const publicDataProvider = new IndexerPublicDataProvider<P>(
  'https://indexer.preview.midnight.network/api/v1/graphql',
  { contractAddress }
);
```

### Private State Provider

The private state provider uses level based encrypted local storage to persist sensitive contract state that must remain hidden from the public ledger. It supports password rotation for key updates and multiple crypto backends for flexibility.

```typescript
const privateStateProvider = await LevelPrivateStateProvider.create<P, S>({
  privateStateStoreName: 'my-app-private-state'
});
```

### Wallet Provider

The wallet provider wraps the DApp Connector connection and exposes wallet operations such as token transfers, balance queries, and key material access. It serves as the bridge between the DApp and the user's wallet.

### ZK Config Provider

The ZK config provider fetches zero knowledge circuit configuration from the network. This configuration includes circuit parameters, proof types, and verification keys needed for proof generation and verification.

```typescript
const zkConfigProvider = new FetchZkConfigProvider<S>(
  zkConfigUri,
  fetch
);
```


## Wallet Integration

### DApp Connector API v4.0.1

The DApp Connector API is the standard interface for DApps to interact with Midnight wallets. It is accessed through the `window.midnight` global object which is injected by wallet browser extensions such as 1AM and Lace.

The DApp Connector API provides methods for connecting to a wallet, disconnecting, requesting authorization, and accessing the connected wallet interface. The connected wallet interface exposes methods for contract deployment, contract calls, token operations, and key material access.

```typescript
const midnight = window.midnight;
if (!midnight) {
  throw new Error('No Midnight wallet extension detected');
}

const initialApi = await midnight.connect();
const connectedApi = await initialApi.requestAuthorization({
  networkId: NetworkId.Preprod
});
```

The connection status can be one of several states including `'disconnected'`, `'connecting'`, `'connected'`, or `'unavailable'`. DApps should monitor the connection status and update their UI accordingly.

### Connect and Disconnect

Connecting to a wallet is an asynchronous operation that may require user approval. The connect method returns an initial API object that has not yet been authorized for network access.

```typescript
async function connectWallet(): Promise<ConnectedAPI> {
  const midnight = window.midnight;
  const initialApi = await midnight.connect();
  const connectedApi = await initialApi.requestAuthorization();
  return connectedApi;
}
```

Disconnecting releases the wallet connection and clears any stored state on the DApp side. The wallet remains available for reconnection.

```typescript
async function disconnectWallet(api: ConnectedAPI): Promise<void> {
  await api.disconnect();
}
```

### Request Authorization

The request authorization step is where the DApp asks the user to approve network access. This step may present a wallet dialog to the user showing the requested network and permissions.

```typescript
const connectedApi = await initialApi.requestAuthorization({
  networkId: NetworkId.Preprod
});
```


## DApp Connector Types

### Configuration

The Configuration type defines the settings for a DApp Connector instance. It includes the network identifier and optional proving server configuration.

```typescript
type Configuration = {
  readonly networkId: NetworkId;
};
```

### ConnectionStatus

The ConnectionStatus type tracks the current state of the wallet connection. It is a union of string literal types representing each possible connection state.

```typescript
type ConnectionStatus =
  | 'disconnected'
  | 'connecting'
  | 'connected'
  | 'disconnecting'
  | 'unavailable';
```

### ConnectedAPI

The ConnectedAPI interface represents a fully authorized wallet connection. It exposes all methods needed for contract deployment, contract calls, token operations, and provider access.

```typescript
interface ConnectedAPI {
  readonly deployContract: (args: DeployArgs) => Promise<DeployResult>;
  readonly submitCallTx: (args: CallTxArgs) => Promise<CallTxResult>;
  readonly getBalances: () => Promise<Balance[]>;
  readonly getUtxos: () => Promise<Utxo[]>;
  readonly disconnect: () => Promise<void>;
  readonly networkId: NetworkId;
  readonly walletAddress: string;
  readonly proveTransaction: (tx: UnprovenTransaction) => Promise<ProvenTransaction>;
  readonly waitForTxFinalization: (txHash: string) => Promise<TxFinalization>;
}
```

### InitialAPI

The InitialAPI is returned from the connect call before authorization. It provides a limited interface for requesting authorization and checking connection state.

```typescript
interface InitialAPI {
  readonly requestAuthorization: (config?: Configuration) => Promise<ConnectedAPI>;
  readonly connectionStatus: ConnectionStatus;
}
```

### WalletConnectedAPI

The WalletConnectedAPI extends ConnectedAPI with wallet specific operations such as key material access and signing.

```typescript
interface WalletConnectedAPI extends ConnectedAPI {
  readonly keyMaterialProvider: KeyMaterialProvider;
  readonly provingProvider: ProvingProvider;
}
```

### KeyMaterialProvider

The KeyMaterialProvider gives DApps access to the wallet key material without exposing raw private keys. It provides derived keys for specific purposes such as encryption or signing.

```typescript
interface KeyMaterialProvider {
  readonly getEncryptionPublicKey: () => Promise<EncryptionPublicKey>;
  readonly getSigningPublicKey: () => Promise<SigningPublicKey>;
  readonly signData: (data: Uint8Array) => Promise<Signature>;
}
```

### ProvingProvider

The ProvingProvider handles zero knowledge proof generation using the wallet key material. It takes an unproven transaction and returns a proven transaction ready for submission.

```typescript
interface ProvingProvider {
  readonly proveTransaction: (
    tx: UnprovenTransaction,
    zkConfig: ZkConfig
  ) => Promise<ProvenTransaction>;
}
```


## Transaction Flow

### Creating an Unproven Transaction

An unproven transaction contains all the public inputs and circuit context needed for a contract call but lacks the zero knowledge proof. It is created using the contract type definitions and the provider stack.

```typescript
const unprovenTx = await contractInterface.createUnprovenCallTx(
  providers,
  'increment'
);
```

### Proving the Transaction

Proving generates the zero knowledge proof that attests to the validity of the transaction without revealing private inputs. The proof provider handles this step using either the browser wallet or a remote proof server.

```typescript
const provenTx = await contractInterface.proveCallTx(
  providers,
  unprovenTx
);
```

### Submitting the Transaction

Submission sends the proven transaction to the Midnight network. The transaction is broadcast to the mempool and included in a forthcoming block.

```typescript
const txHash = await contractInterface.submitCallTx(
  providers,
  provenTx
);
```

### Waiting for Finalization

After submission the DApp should wait for the transaction to be finalized. Finalization means the transaction has been included in a block and is considered irreversible.

```typescript
const result = await contractInterface.waitForCallTxFinalization(
  providers,
  txHash
);
```

### Handling Transaction Results

Transaction results indicate whether the call succeeded or failed in the guaranteed or fallible phase. DApps should inspect the result status and present appropriate feedback to the user.

```typescript
if (result.status === 'succeeded') {
  console.log('Transaction succeeded');
} else if (result.status === 'partially-succeeded') {
  console.warn('Transaction partially succeeded');
} else {
  console.error('Transaction failed:', result.error);
}
```


## State Management

### Public State Queries via Indexer

Public contract state is stored on chain and can be queried through the indexer public data provider. The indexer exposes a GraphQL API that supports queries for contract state, transactions, and block information.

```typescript
const state = await providers.publicDataProvider.queryContractState(
  contractAddress
);
```

### Private State with Level Private State Provider

Private state is stored locally using encrypted storage. The level private state provider manages this storage with support for password rotation and multiple crypto backends.

```typescript
const privateStateProvider = await LevelPrivateStateProvider.create<P, S>({
  privateStateStoreName: 'my-dapp-state'
});

await privateStateProvider.set('someKey', encryptedData);
const data = await privateStateProvider.get('someKey');
```

### State Synchronization

After a transaction is finalized the DApp should synchronize its local view of state. Public state updates are reflected automatically through indexer queries. Private state must be updated explicitly by replaying the transaction effects on the local state.


## Indexer Public Data Provider

The indexer public data provider wraps the Midnight indexer GraphQL API and provides typed access to on chain data. It supports queries for contract state, transaction history, block information, and event subscriptions.

Query patterns include fetching the latest contract state, retrieving transaction details by hash, listing blocks within a range, and subscribing to contract action events for real time updates.

```typescript
const indexerProvider = new IndexerPublicDataProvider<MyContractState>(
  indexerUri,
  { contractAddress }
);

const state = await indexerProvider.getContractState(contractAddress);
const txs = await indexerProvider.getContractTransactions(contractAddress, { limit: 10 });
const block = await indexerProvider.getBlockByHeight(blockHeight);
```


## Level Private State Provider

The level private state provider uses LevelDB for encrypted local storage of private contract state. It supports multiple crypto backends for encryption and allows password rotation to update encryption keys without losing data.

```typescript
const provider = await LevelPrivateStateProvider.create<P, S>({
  privateStateStoreName: 'my-dapp-private-state'
});
```

The provider supports standard CRUD operations on private state entries. Each entry is encrypted at rest using the configured crypto backend and password.

Password rotation is supported through a migration mechanism that re-encrypts all stored data with a new password. This is important for long lived DApps where encryption keys may need periodic rotation.

```typescript
await provider.rotatePassword('old-password', 'new-password');
```

Crypto backends include the default Midnight encryption scheme and can be extended with custom implementations. Migration between backends is supported for forward compatibility.

The provider also handles state migration when contract private state schemas change. Migration functions can be supplied to transform state from one version to the next during upgrades.


## HTTP Client Proof Provider

The HTTP client proof provider sends proving requests to a remote proof server over HTTP. This provider is useful when the browser wallet does not support proving or when server side proving is preferred for performance reasons.

```typescript
const proofProvider = new HttpClientProofProvider(
  'https://proof-server.preview.midnight.network',
  fetch
);
```

The provider uses the DEFAULT_CONFIG constants for connection timeouts and retry policies. The proof server must implement the Midnight proving protocol and have access to the corresponding ZK circuit artifacts.

Integration with a proof server involves deploying the proof server binary or Docker container and configuring the DApp to point to its endpoint. The proof server requires the compiled circuit artifacts and access to the network config for the target network.


## DApp Connector Proof Provider

The DApp Connector proof provider delegates proving to the browser wallet extension. This is the standard approach for end user DApps where the wallet handles proving transparently using the user's local hardware.

```typescript
const proofProvider = new DAppConnectorProofProvider(connectedAPI);
```

The 1AM wallet supports proving through its built in proof server integration. The Lace wallet also provides proving capabilities through its Midnight integration. Both wallets expose the proving interface through the DApp Connector API.

When using the DApp Connector proof provider the DApp does not need to manage proof server infrastructure. The wallet handles proof generation and returns the proven transaction to the DApp for submission.

```typescript
const provenTx = await proofProvider.proveTransaction(
  unprovenTransaction,
  zkConfig
);
```


## Fetch ZK Config Provider

The fetch ZK config provider retrieves zero knowledge circuit configuration from the network. This configuration includes the circuit parameters, proof types, and verification keys needed for proof generation and verification.

```typescript
const zkConfigProvider = new FetchZkConfigProvider<MyPrivateState>(
  zkConfigUri,
  fetch
);

const zkConfig = await zkConfigProvider.getZkConfig();
```

The provider fetches configuration from the network on demand and caches results locally. The configuration is specific to the contract type and version and must match the compiled contract artifacts used by the DApp.

The zkConfigUri is typically derived from the network ID and contract address. Each network has its own ZK configuration endpoint that serves the appropriate circuit parameters for that network.


## Network ID Management

Network ID management controls which Midnight network the DApp connects to. The network ID determines the RPC endpoint, indexer endpoint, proof server endpoint, and ZK configuration endpoint.

```typescript
import { NetworkId, getNetworkId, setNetworkId } from '@midnight-ntwrk/midnight-js-network-id';
```

The available networks include `Undeployed` for local development, `Preview` for the preview testnet, `Preprod` for the pre production testnet, and `Mainnet` for the production network.

```typescript
const currentNetwork = getNetworkId();
setNetworkId(NetworkId.Preprod);
```

Environment switching requires reinitializing all providers since each network has its own endpoints and configuration. DApps should support environment switching to allow testing on different networks before deploying to mainnet.

```typescript
function switchNetwork(networkId: NetworkId): void {
  setNetworkId(networkId);
  // Reinitialize all providers with new endpoints
  initializeProviders();
}
```


## Logger Provider

The logger provider enables structured logging for Midnight DApps. It supports multiple log levels and can be configured to filter by severity.

```typescript
enum LogLevel {
  Trace = 'trace',
  Debug = 'debug',
  Info = 'info',
  Warn = 'warn',
  Error = 'error'
}
```

Logging is helpful for debugging contract interactions, monitoring transaction flow, and tracking provider initialization. DApps can configure the log level at startup and redirect logs to different outputs.

```typescript
logger.info('Wallet connected', { address: walletAddress });
logger.error('Transaction failed', { error, txHash });
```


## Contract Integration

### Creating the Circuit Call Transaction Interface

The circuit call transaction interface provides typed methods for interacting with a deployed contract. It is created from the compiled contract type definitions.

```typescript
const contractInterface = createCircuitCallTxInterface(
  compiledContract,
  contractAddress
);
```

### Creating Unproven Call Transactions

An unproven call transaction is prepared with the contract method name and arguments. This does not yet include the zero knowledge proof.

```typescript
const unprovenTx = await contractInterface.createUnprovenCallTx(
  providers,
  'transfer',
  { recipient: recipientAddress, amount: BigInt(100) }
);
```

### Submitting Call Transactions

The asynchronous submission method submits the transaction and returns immediately without waiting for finalization. This is useful for fire and forget operations.

```typescript
const txHash = await contractInterface.submitCallTxAsync(
  providers,
  provenTx
);
```

The synchronous submission method waits for finalization before returning the result.

```typescript
const result = await contractInterface.submitCallTx(
  providers,
  provenTx
);
```


## Deployment

### Vercel Deployment

Midnight DApps built with Next.js or Vite can be deployed to Vercel using the standard Vercel deployment workflow. Connect the GitHub repository to Vercel and configure the build settings.

For Vite projects set the build command to `npm run build` and the output directory to `dist`. For Next.js projects Vercel detects the framework automatically.

Environment variables must be configured in the Vercel dashboard for each target network. These include the indexer URI, network ID, and proof server URI.

```
INDEXER_URI=https://indexer.preview.midnight.network/api/v1/graphql
NETWORK_ID=preview
PROOF_SERVER_URI=https://proof-server.preview.midnight.network
```

### Production Configuration

Production DApps should use environment specific configuration for all service endpoints. Never hardcode network endpoints in source code. Use environment variables that are injected at build time.

```typescript
const config = {
  indexerUri: import.meta.env.VITE_INDEXER_URI,
  networkId: import.meta.env.VITE_NETWORK_ID as NetworkId,
  proofServerUri: import.meta.env.VITE_PROOF_SERVER_URI
};
```

Production DApps should also implement proper error boundaries, loading states, and fallback UI for when the wallet is unavailable or the network is unreachable.


## Error Handling

### Error Types

The Midnight SDK defines several error types for common failure scenarios in DApp development.

CallTxFailedError is thrown when a contract call transaction fails. This includes failures in the guaranteed phase or the fallible phase of the transaction.

```typescript
class CallTxFailedError extends Error {
  readonly txHash: string;
  readonly phase: 'guaranteed' | 'fallible';
  readonly reason: string;
}
```

DeployTxFailedError is thrown when contract deployment fails. This can occur due to network issues, insufficient funds, or contract validation errors.

```typescript
class DeployTxFailedError extends Error {
  readonly contractCode: string;
  readonly reason: string;
}
```

ContractTypeError is thrown when there is a type mismatch between the DApp contract types and the deployed contract. This indicates that the DApp is using incompatible contract definitions.

```typescript
class ContractTypeError extends Error {
  readonly expected: string;
  readonly actual: string;
}
```

TxFailedError is the base error type for all transaction failures. It includes the transaction hash and a descriptive failure reason.

```typescript
class TxFailedError extends Error {
  readonly txHash: string;
  readonly reason: string;
}
```

### Transaction Result Statuses

Every transaction returns a result object with a status field indicating the outcome. The possible statuses are `'succeeded'`, `'partially-succeeded'`, and `'failed'`.

A succeeded status means the entire transaction completed successfully in both the guaranteed and fallible phases.

A partially succeeded status means the guaranteed phase completed but the fallible phase did not. The guaranteed effects are still applied to the chain.

A failed status means the guaranteed phase failed and no effects were applied.

```typescript
type TransactionResult = {
  readonly status: 'succeeded' | 'partially-succeeded' | 'failed';
  readonly txHash: string;
  readonly blockHeight?: number;
  readonly error?: string;
};
```


## Testing DApps

### Playwright E2E Testing

Playwright provides end to end testing capabilities for Midnight DApps. Tests can simulate wallet connections by mocking the `window.midnight` API and exercising the full DApp flow.

```typescript
import { test, expect } from '@playwright/test';

test('wallet connection flow', async ({ page }) => {
  await page.goto('http://localhost:5173');
  const connectButton = page.locator('[data-testid="connect-wallet"]');
  await connectButton.click();
  await expect(page.locator('[data-testid="wallet-address"]')).toBeVisible();
});
```

### Testkit JS DAppConnectorWalletAdapter

The testkit js package provides wallet adapters for testing Midnight DApps without a real browser wallet. The DAppConnectorWalletAdapter simulates the wallet API with configurable test accounts.

```typescript
import { DAppConnectorWalletAdapter } from '@midnight-ntwrk/testkit-js';

const walletAdapter = new DAppConnectorWalletAdapter({
  networkId: NetworkId.Undeployed,
  mnemonic: testMnemonic
});

// Inject the adapter into window.midnight for testing
window.midnight = walletAdapter;
```

### DAppConnectorInitialAPI

The DAppConnectorInitialAPI provides the initial connection interface for testing. It can be configured to simulate connection failures, authorization rejections, and network errors.

```typescript
import { DAppConnectorInitialAPI } from '@midnight-ntwrk/testkit-js';

const initialApi = new DAppConnectorInitialAPI({
  connectionStatus: 'connecting',
  networkId: NetworkId.Undeployed
});
```

Testing patterns include unit tests for provider initialization, integration tests for contract interactions, and E2E tests for complete user flows. Each test should clean up state between runs to ensure isolation.


## Best Practices

Always handle the case where `window.midnight` is undefined. Users may not have a Midnight wallet extension installed. Provide clear guidance on installing a compatible wallet.

Use React context or a state management library to share the midnight connection state across components. Avoid connecting to the wallet in individual components since this leads to multiple connection attempts.

Cache public state queries to avoid excessive indexer requests. The indexer has rate limits and repeated queries for the same data waste resources and degrade performance.

Implement proper loading states for all asynchronous operations. Transaction submission, proof generation, and state queries can take several seconds and users need visual feedback during these operations.

Validate transaction inputs before creating unproven transactions. Invalid inputs result in failed transactions that still consume DUST tokens.

Test on multiple networks before deploying to mainnet. Behavior differences between networks can cause unexpected failures in production.

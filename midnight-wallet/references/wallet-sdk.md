# Wallet SDK Overview

**Package**: `@midnight-ntwrk/wallet-sdk-facade`

## Overview

The Wallet SDK provides the core abstraction layer for managing Midnight wallets across their entire lifecycle. It supports four wallet types each serving a distinct role in the Midnight privacy model. The SDK exposes a builder pattern for low level control via `FluentWalletBuilder` and a factory facade via `WalletFacade` for common workflows.

## WalletFacade

`WalletFacade` is the primary entry point for most applications. It wraps the lower level builder API into a simplified interface.

```typescript
import { WalletFacade } from '@midnight-ntwrk/wallet-sdk-facade';

const wallet = await WalletFacade.init({
  indexerUri: 'https://indexer.preprod.midnight.network',
  proofServerUri: 'http://localhost:6300',
  networkId: 'preprod',
});

await wallet.start(shieldedSecretKeys, dustSecretKey);
const syncedState = await wallet.waitForSyncedState();
await wallet.stop();
```

`WalletFacade.init()` accepts a configuration object with network endpoints. `start()` activates the wallet with secret keys. `waitForSyncedState()` blocks until the wallet synchronizes with the indexer. `stop()` gracefully shuts down all wallet subsystems.

## Wallet Types

### ShieldedWallet

The shielded wallet handles private transactions using zero knowledge proofs. It manages shielded addresses derived from Zswap secret keys. Shielded balances are not visible onchain in plaintext. Only the wallet holder can decrypt and view them.

```typescript
const shieldedWallet = await builder.shieldedWallet(shieldedSecretKeys);
const address = await shieldedWallet.shieldedAddress();
const balances = await shieldedWallet.balances();
```

Shielded balances are accessed through the wallet facade via `syncedState.shielded.balances`. The shielded wallet is responsible for creating and consuming shielded UTXOs and generating ZK proofs for private transfers.

### UnshieldedWallet

The unshielded wallet manages public transactions visible onchain. It handles unshielded addresses derived from NIGHT coin secret keys. Unshielded balances are public and can be queried by anyone.

```typescript
const unshieldedWallet = await builder.unshieldedWallet(unshieldedSecretKeys);
const address = await unshieldedWallet.unshieldedAddress();
const balances = await unshieldedWallet.balances();
```

Unshielded transactions do not require ZK proofs and have lower fees. Unshielded addresses use the Bech32m encoding format with the `mn_addr1` prefix.

### DustWallet

The dust wallet manages DUST tokens used for paying transaction fees. Every transaction on Midnight consumes a small amount of DUST. Without DUST you cannot submit transactions.

```typescript
const dustWallet = await builder.dustWallet(dustSecretKey);
const dustBalance = await dustWallet.balance();
const dustAddress = await dustWallet.dustAddress();
```

DUST is generated from unshielded NIGHT UTXOs through a registration process. The dust wallet tracks available DUST and manages nonces for DUST commitments. Insufficient DUST is a common error when deploying or calling contracts.

### HDWallet

The HD wallet provides hierarchical deterministic key derivation following the BIP340 standard. It derives child keys from a single master seed for all wallet types.

```typescript
import { HDWallet, Roles } from '@midnight-ntwrk/wallet-sdk-facade';

const hdWallet = HDWallet.fromSeed(seed);
const zswapKey = hdWallet.derive(Roles.Zswap);
const dustKey = hdWallet.derive(Roles.Dust);
const nightKey = hdWallet.derive(Roles.NightExternal);
```

**Roles**:
- `Roles.Zswap` derives keys for shielded transactions
- `Roles.Dust` derives keys for DUST management
- `Roles.NightExternal` derives keys for unshielded NIGHT token handling

Each role produces a distinct key pair ensuring cryptographic separation between wallet types from a single seed.

## Wallet Creation

### From Seed

```typescript
const hdWallet = HDWallet.fromSeed(seedBytes);
const signingKey = hdWallet.derive(Roles.Zswap);
```

### Random Generation

```typescript
import { sampleSigningKey } from '@midnight-ntwrk/wallet-sdk-facade';

const randomKey = sampleSigningKey();
```

### From Existing Keys

```typescript
const wallet = await builder.shieldedWallet([existingSigningKey]);
```

## FluentWalletBuilder

`FluentWalletBuilder` provides fine grained control over wallet construction. It allows composing multiple wallet types into a single facade and customizing each component independently.

```typescript
import { FluentWalletBuilder } from '@midnight-ntwrk/wallet-sdk-facade';

const builder = new FluentWalletBuilder({
  indexerUri: 'https://indexer.preprod.midnight.network',
  proofServerUri: 'http://localhost:6300',
});

const facade = await builder
  .shieldedWallet(zswapKeys)
  .unshieldedWallet(nightKeys)
  .dustWallet(dustKey)
  .build();
```

Each wallet method on the builder is additive. You can build a wallet with only the types you need. For a read only client that only queries balances you might only include the unshielded wallet. For a full DApp you typically need all three.

## WalletFactory

`WalletFactory` provides an alternative creation path that takes a configuration object and produces wallet instances directly without the builder pattern.

```typescript
import { WalletFactory } from '@midnight-ntwrk/wallet-sdk-facade';

const factory = new WalletFactory(config);
const wallet = await factory.create({
  shielded: shieldedSecretKeys,
  unshielded: unshieldedSecretKeys,
  dust: dustSecretKey,
});
```

## State Management

### WalletSaveStateProvider

The `WalletSaveStateProvider` interface defines how wallets persist their state across sessions. The default implementation stores state in memory. Custom implementations can persist to local storage IndexedDB or other backends.

```typescript
interface WalletSaveStateProvider {
  save(key: string, data: Uint8Array): Promise<void>;
  load(key: string): Promise<Uint8Array | null>;
  delete(key: string): Promise<void>;
}

const customProvider: WalletSaveStateProvider = {
  save: async (key, data) => localStorage.setItem(key, JSON.stringify(data)),
  load: async (key) => { /* ... */ },
  delete: async (key) => localStorage.removeItem(key),
};
```

State includes wallet addresses synced block heights and transaction history. The provider is injected during wallet construction.

## Test Wallets

For testing you can use `FluentWalletBuilder` with the local devnet configuration. Test wallets do not require real funds for unit tests when using the testkit.

```typescript
import { FluentWalletBuilder } from '@midnight-ntwrk/wallet-sdk-facade';

const testBuilder = new FluentWalletBuilder({
  indexerUri: 'http://localhost:32888/api/graphql',
  proofServerUri: 'http://localhost:6300',
});

const testWallet = await testBuilder
  .shieldedWallet(testKeys.zswap)
  .unshieldedWallet(testKeys.night)
  .dustWallet(testKeys.dust)
  .build();
```

Always use the local devnet for testing rather than Preprod to avoid consuming real DUST and NIGHT tokens during development.

## Resources

- **DUST Operations**: See dust-operations.md
- **Key Management**: See key-management.md
- **1AM Wallet**: See 1am-wallet SKILL.md

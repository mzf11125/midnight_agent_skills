# Key Management

**Package**: `@midnight-ntwrk/wallet-sdk-facade`

## Overview

Midnight uses three distinct key types for its privacy model. Each key type serves a specific cryptographic purpose. Lost keys mean permanently inaccessible funds so proper management is critical.

## Key Types

### SigningKey

Authorizes transactions via Schnorr signatures:

```typescript
import { SigningKey } from '@midnight-ntwrk/wallet-sdk-facade';

const signingKey: SigningKey = {
  secretKey: secretKeyBytes,
  publicKey: publicKeyBytes,
};
```

Used by all wallet types for transaction authentication.

### CoinSecretKey

Controls unshielded token ownership and derives unshielded addresses. Used by `UnshieldedWallet` corresponding to `Roles.NightExternal`.

### EncryptionSecretKey

Enables viewing shielded balances and decrypting private state. Used by `ShieldedWallet` corresponding to `Roles.Zswap`. Sometimes called the view key.

## Key Derivation

### BIP340 (signingKeyFromBip340)

```typescript
import { signingKeyFromBip340 } from '@midnight-ntwrk/wallet-sdk-facade';

const signingKey = signingKeyFromBip340({
  seed: masterSeed,
  derivationPath: "m/44'/617'/0'/0/0",
});
```

BIP340 is the Schnorr based key derivation standard used by Midnight.

### HDWallet Derivation

```typescript
import { HDWallet, Roles } from '@midnight-ntwrk/wallet-sdk-facade';

const hdWallet = HDWallet.fromSeed(seed);
const zswapKey = hdWallet.derive(Roles.Zswap);
const dustKey = hdWallet.derive(Roles.Dust);
const nightKey = hdWallet.derive(Roles.NightExternal);
```

**Derivation paths**:
- `Roles.Zswap` -> `m/44'/617'/0'` (shielded transactions)
- `Roles.Dust` -> `m/44'/617'/1'` (DUST management)
- `Roles.NightExternal` -> `m/44'/617'/2'/0` (unshielded receive)

## Key Sampling

Generate random keys using cryptographically secure randomness:

```typescript
import { sampleSigningKey, sampleCoinPublicKey, sampleEncryptionPublicKey }
  from '@midnight-ntwrk/wallet-sdk-facade';

const randomSigningKey = sampleSigningKey();
const randomCoinKey = sampleCoinPublicKey();
const randomEncryptionKey = sampleEncryptionPublicKey();
```

## Key Storage

### WalletSaveStateProvider

```typescript
interface WalletSaveStateProvider {
  save(key: string, data: Uint8Array): Promise<void>;
  load(key: string): Promise<Uint8Array | null>;
  delete(key: string): Promise<void>;
}
```

Implement for localStorage IndexedDB secure enclave HSM or encrypted filesystem. Never store raw keys in plaintext.

### StorageEncryption

```typescript
import { StorageEncryption } from '@midnight-ntwrk/wallet-sdk-facade';

const encryption = new StorageEncryption({
  password: userPassword,
  iterations: 600_000,
});

const encrypted = await encryption.encrypt(rawState);
const decrypted = await encryption.decrypt(encrypted);
```

Higher iteration counts increase brute force resistance at the cost of slower encryption.

### Password Rotation

```typescript
const oldEnc = new StorageEncryption({ password: oldPw });
const newEnc = new StorageEncryption({ password: newPw });
const decrypted = await oldEnc.decrypt(storedState);
await stateProvider.save('wallet', await newEnc.encrypt(decrypted));
```

Verify the new password works before deleting old encrypted state.

## Key Export and Import

### ExportPrivateStatesOptions / ImportPrivateStatesOptions

```typescript
interface ExportPrivateStatesOptions {
  signingKeys: boolean;
  coinKeys: boolean;
  encryptionKeys: boolean;
  includeState: boolean;
  password?: string;
}

interface ImportPrivateStatesOptions {
  password?: string;
  mergeStrategy: 'replace' | 'merge';
}
```

`replace` overwrites all state. `merge` combines imported with existing state.

### ExportSigningKeysOptions / ImportSigningKeysOptions

```typescript
interface ExportSigningKeysOptions {
  includeDerivationPath: boolean;
  format: 'raw' | 'hex' | 'base64';
}

interface ImportSigningKeysOptions {
  format: 'raw' | 'hex' | 'base64';
  overwriteExisting: boolean;
}
```

## Crypto Backends

Pluggable cryptographic backends. The default uses platform native WebCrypto in browsers and Node.js crypto on servers:

```typescript
import { setCryptoBackend, NativeCryptoBackend } from '@midnight-ntwrk/wallet-sdk-facade';

setCryptoBackend(new NativeCryptoBackend());
```

Custom backends support hardware security modules secure enclaves or compliance requirements.

## Security Considerations

- Never log secret keys or include them in error messages
- Use `StorageEncryption` with a strong password for persisted key material
- Rotate keys if you suspect compromise
- Clear key material from memory when wallet is stopped
- Validate exported keys can be re-imported before deleting originals
- Use the testkit for development to avoid risking real keys

## Resources

- **Wallet SDK Overview**: See wallet-sdk.md
- **DUST Operations**: See dust-operations.md

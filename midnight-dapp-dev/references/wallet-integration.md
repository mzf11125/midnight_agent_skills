# Wallet Integration

**Package**: `@midnight-ntwrk/dapp-connector-api v4.0.1`

## Overview

The DApp Connector API enables DApps to connect to Midnight wallets via `window.midnight.{walletId}` injection. It handles connection lifecycle transaction creation and delegated proving without exposing raw keys.

## window.midnight Global

Wallets coexist at:
```typescript
window.midnight['1am']    // 1AM wallet
window.midnight['lace']   // Lace wallet
```

## Connect and Disconnect

```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

const wallet = window.midnight['1am'];
if (!wallet) throw new Error('Wallet not installed');
const connectedAPI = await wallet.connect(NetworkId('preprod'));
```

`connect` may trigger a wallet UI prompt. Call `disconnect` on logout or unmount.

## Request Authorization

```typescript
import semver from 'semver';

const wallets = Object.values(window.midnight ?? {});
const compatible = wallets.filter(w =>
  semver.satisfies(w.apiVersion, '^4.0.0')
);
```

## ConnectionStatus and ConnectedAPI

### ConnectionStatus

```typescript
interface ConnectionStatus {
  networkId: NetworkId;
  connected: boolean;
  address?: string;
}
```

### ConnectedAPI

```typescript
interface ConnectedAPI {
  getConfiguration(): Promise<WalletConfiguration>;
  getConnectionStatus(): Promise<ConnectionStatus>;
  getShieldedBalances(): Promise<Record<string, bigint>>;
  getUnshieldedBalances(): Promise<Record<string, bigint>>;
  getDustBalance(): Promise<bigint>;
  getShieldedAddresses(): Promise<{ shieldedAddress: string }>;
  getUnshieldedAddress(): Promise<string>;
  getDustAddress(): Promise<string>;
  makeTransfer(outputs: InitActions[]): Promise<Transaction>;
  submitTransaction(tx: Transaction): Promise<{ txHash: string }>;
  getProvingProvider(kmProvider: ZkConfigProvider): ProvingProvider;
  disconnect(): Promise<void>;
}
```

## KeyMaterialProvider and ProvingProvider

```typescript
interface KeyMaterialProvider {
  getProverKey(contractAddress: string): Promise<Uint8Array>;
  getVerifierKey(contractAddress: string): Promise<Uint8Array>;
  getCircuitMetadata(contractAddress: string): Promise<CircuitMetadata>;
}

interface ProvingProvider {
  prove(tx: UnprovenTransaction, keyMaterial: KeyMaterialProvider): Promise<ProvenTransaction>;
}
```

## WalletConnectedAPI

Extends `ConnectedAPI` with contract interaction and data signing:

```typescript
interface WalletConnectedAPI extends ConnectedAPI {
  deployContract(deployment: ContractDeployment): Promise<DeployResult>;
  callContract(call: ContractCall): Promise<CallResult>;
  signData(data: SignDataOptions): Promise<Signature>;
  getTransactionHistory(): Promise<HistoryEntry[]>;
}
```

## Error Codes

```typescript
class APIError extends Error {
  code: ErrorCode;
  message: string;
  details?: unknown;
}

enum ErrorCode {
  USER_REJECTED = 'USER_REJECTED',
  NETWORK_ERROR = 'NETWORK_ERROR',
  INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS',
  INVALID_ADDRESS = 'INVALID_ADDRESS',
  TRANSACTION_FAILED = 'TRANSACTION_FAILED',
  NOT_CONNECTED = 'NOT_CONNECTED',
  UNSUPPORTED_NETWORK = 'UNSUPPORTED_NETWORK',
  PROOF_GENERATION_FAILED = 'PROOF_GENERATION_FAILED',
  DUST_INSUFFICIENT = 'DUST_INSUFFICIENT',
}
```

### Error Handling Pattern

```typescript
try {
  const tx = await connectedAPI.makeTransfer([{
    kind: 'unshielded',
    tokenType: nativeToken().raw,
    value: amount,
    recipient: address,
  }]);
  await connectedAPI.submitTransaction(tx);
} catch (error) {
  if (error instanceof APIError) {
    switch (error.code) {
      case 'USER_REJECTED':
        return;  // User cancelled, not an error
      case 'INSUFFICIENT_FUNDS':
        showError('Not enough balance');
        break;
      case 'DUST_INSUFFICIENT':
        showError('Insufficient DUST. Generate more DUST first.');
        break;
      default:
        showError(`Transaction failed: ${error.message}`);
    }
  }
}
```

## React Hook Patterns

### useWalletConnection

```typescript
function useWalletConnection(walletId: string, networkId: string) {
  const [api, setApi] = useState<ConnectedAPI | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const wallet = window.midnight?.[walletId];
    if (!wallet) { setError('Wallet not found'); return; }
    wallet.connect(NetworkId(networkId)).then(setApi).catch(setError);
  }, [walletId, networkId]);

  return { api, error };
}
```

### useBalances

```typescript
function useBalances(api: ConnectedAPI | null) {
  const [shielded, setShielded] = useState<Record<string, bigint>>({});
  const [unshielded, setUnshielded] = useState<Record<string, bigint>>({});
  const [dust, setDust] = useState<bigint>(0n);

  useEffect(() => {
    if (!api) return;
    Promise.all([
      api.getShieldedBalances(),
      api.getUnshieldedBalances(),
      api.getDustBalance(),
    ]).then(([s, u, d]) => { setShielded(s); setUnshielded(u); setDust(d); });
  }, [api]);

  return { shielded, unshielded, dust };
}
```

## Best Practices

- Check for `window.midnight` undefined before accessing wallet properties
- Validate `apiVersion` before connecting using `semver.satisfies`
- Use wallet configured endpoints from `getConfiguration()` instead of hardcoding
- Handle `USER_REJECTED` gracefully without showing error UI
- Disconnect on logout or component unmount

## Resources

- **Provider Architecture**: See provider-architecture.md
- **Transaction Flow**: See transaction-flow.md
- **DApp Connector Specification**: https://github.com/midnightntwrk/midnight-dapp-connector-api

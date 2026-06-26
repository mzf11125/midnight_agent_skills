# Midnight DApp Connector API v4.0.1 Reference

This document covers the DApp Connector API for Midnight Network wallets in detail.

## API Surface

The DApp Connector API is available on the global `window.midnight` object. Each wallet provider exposes its own entry point.

```typescript
window.midnight.lace          // Lace wallet
window.midnight['1am']        // 1AM wallet
window.midnight.kuira         // Kuira wallet
```

All three providers implement the same `DAppConnectorAPI` interface.

## Core Methods

### checkConnection

Returns the current connection status and provides the wallet name.

```typescript
checkConnection(): Promise<{
  status: ConnectionStatus;
  walletName: string;
}>
```

Call this on app mount to restore a previously authorized session.

### connect

Initiates a connection to the wallet. Opens the wallet extension popup for user approval.

```typescript
connect(params?: ConnectParams): Promise<{
  status: ConnectionStatus;
  address: string;
  network: string;
}>
```

**ConnectParams fields:**

| Parameter | Type   | Description                                  |
|-----------|--------|----------------------------------------------|
| network   | string | Target Midnight network (preview, preprod, mainnet) |
| appName   | string | Display name of your DApp                    |

If the user rejects the connection request a `UserRejectedError` is thrown.

### disconnect

Terminates the current session. Clears any stored authorization on the wallet side.

```typescript
disconnect(): Promise<void>
```

After calling disconnect the DApp must request authorization again on the next connect.

### requestAuthorization

Requests permission to perform specific actions on behalf of the wallet holder.

```typescript
requestAuthorization(params?: AuthParams): Promise<{
  token: string;
  permissions: string[];
}>
```

**AuthParams fields:**

| Parameter   | Type     | Description                       |
|-------------|----------|-----------------------------------|
| methods     | string[] | Requested capability methods      |
| permissions | string[] | Granular permissions to request   |

## Type Definitions

### ConnectionStatus

```typescript
type ConnectionStatus =
  | 'connected'
  | 'disconnected'
  | 'pending'
  | 'error';
```

| Value          | Meaning                                      |
|----------------|----------------------------------------------|
| `connected`    | Wallet is connected and authorized           |
| `disconnected` | No active connection                         |
| `pending`      | Connection request is awaiting user approval |
| `error`        | Connection attempt failed                   |

### ErrorCode

```typescript
type ErrorCode =
  | 'WALLET_NOT_FOUND'
  | 'USER_REJECTED'
  | 'NETWORK_MISMATCH'
  | 'AUTHORIZATION_FAILED'
  | 'PROOF_GENERATION_FAILED'
  | 'INVALID_PARAMS'
  | 'INTERNAL_ERROR';
```

| ErrorCode                  | Cause                                              |
|----------------------------|----------------------------------------------------|
| `WALLET_NOT_FOUND`         | No compatible wallet extension is installed        |
| `USER_REJECTED`            | The user declined the connection or signing prompt |
| `NETWORK_MISMATCH`         | The DApp and wallet are targeting different networks |
| `AUTHORIZATION_FAILED`     | The wallet refused to authorize the DApp           |
| `PROOF_GENERATION_FAILED`  | ZK proving step failed                             |
| `INVALID_PARAMS`           | The provided parameters are malformed              |
| `INTERNAL_ERROR`           | An unexpected error occurred in the wallet         |

### APIError

```typescript
interface APIError {
  code: ErrorCode;
  message: string;
  details?: Record<string, unknown>;
}
```

## Event Listeners

The DApp Connector API emits events for connection state changes. Register listeners to keep the UI synchronized.

```typescript
// Connection state changed
api.on('connectionChange', (status: ConnectionStatus) => {
  console.log('Connection status changed to:', status);
});

// Wallet address changed
api.on('addressChange', (address: string) => {
  console.log('Current address is now:', address);
});

// Network changed
api.on('networkChange', (network: string) => {
  console.log('Wallet switched to network:', network);
});

// Remove a specific listener
api.off('connectionChange', handler);
```

## Signing Methods

### signData

Requests the wallet to sign arbitrary data. The wallet prompts for user confirmation.

```typescript
signData(data: Uint8Array | string): Promise<{
  signature: Uint8Array;
  publicKey: string;
}>
```

### verifySignature

Performs local verification of a signature without contacting the wallet.

```typescript
verifySignature(data: Uint8Array | string, signature: Uint8Array, publicKey: string): Promise<boolean>
```

## Usage Example

```typescript
import { DAppConnectorAPI } from '@midnight-ntwrk/dapp-connector-api';

async function connectWallet(): Promise<void> {
  const lace = window.midnight?.lace;
  if (!lace) {
    throw new Error('Lace wallet not installed');
  }

  const { status } = await lace.checkConnection();
  if (status === 'connected') {
    return;
  }

  const result = await lace.connect({
    network: 'preview',
    appName: 'My Midnight DApp',
  });

  console.log('Connected to', result.network, 'with address', result.address);
}
```

## Cross References

- `midnight-dapp-dev` skill for full DApp development workflows
- `midnight-wallet` skill for wallet SDK integration patterns
- `1am-wallet` skill for dust-free deployment using the 1AM extension

# Error Codes Reference

## Overview

Complete reference of error codes across Midnight Network APIs. All errors follow the `APIError` structure with standardized codes.

## APIError Structure

```typescript
interface APIError extends Error {
  code: ErrorCode;
  message: string;
  details?: any;
  stack?: string;
}
```

## Error Codes

### Wallet Connection Errors

#### WALLET_NOT_FOUND
**Description**: No Midnight wallet detected in browser.

**Cause**: User doesn't have a Midnight wallet extension installed.

**Solution**:
```typescript
if (error.code === 'WALLET_NOT_FOUND') {
  showMessage('Please install a Midnight wallet extension');
  redirectToWalletDownload();
}
```

#### WALLET_NOT_CONNECTED
**Description**: Wallet is not connected.

**Cause**: Attempting operations before connecting wallet.

**Solution**:
```typescript
if (error.code === 'WALLET_NOT_CONNECTED') {
  await connectWallet();
}
```

#### UNSUPPORTED_API_VERSION
**Description**: Wallet API version incompatible with DApp.

**Cause**: Version mismatch between DApp requirements and wallet.

**Details**:
```typescript
{
  required: '^4.0.0',
  actual: '3.2.1'
}
```

**Solution**:
```typescript
if (error.code === 'UNSUPPORTED_API_VERSION') {
  showMessage(`Please update your wallet. Required: ${error.details.required}`);
}
```

#### CONNECTION_FAILED
**Description**: Failed to establish wallet connection.

**Cause**: Network issues, wallet locked, or user rejection.

**Solution**:
```typescript
if (error.code === 'CONNECTION_FAILED') {
  // Retry with exponential backoff
  await retryConnection();
}
```

### User Action Errors

#### USER_REJECTED
**Description**: User rejected the operation.

**Cause**: User cancelled transaction, connection, or signature request.

**Solution**:
```typescript
if (error.code === 'USER_REJECTED') {
  // Don't show error - user intentionally cancelled
  console.log('Operation cancelled by user');
  return;
}
```

**Best Practice**: Don't treat as error - respect user's decision.

#### USER_TIMEOUT
**Description**: User didn't respond within timeout period.

**Cause**: User left prompt open too long.

**Solution**:
```typescript
if (error.code === 'USER_TIMEOUT') {
  showMessage('Request timed out. Please try again.');
}
```

### Transaction Errors

#### INSUFFICIENT_FUNDS
**Description**: Insufficient balance for transaction.

**Cause**: Balance less than amount + fees.

**Details**:
```typescript
{
  required: 1000n,
  available: 500n,
  tokenType: '0x...'
}
```

**Solution**:
```typescript
if (error.code === 'INSUFFICIENT_FUNDS') {
  const { required, available } = error.details;
  showMessage(`Need ${required}, have ${available}`);
}
```

#### INVALID_AMOUNT
**Description**: Transaction amount is invalid.

**Cause**: Amount is zero, negative, or exceeds maximum.

**Solution**:
```typescript
if (error.code === 'INVALID_AMOUNT') {
  showMessage('Please enter a valid amount');
}
```

#### INVALID_ADDRESS
**Description**: Recipient address is invalid.

**Cause**: Malformed address, wrong network, or invalid checksum.

**Details**:
```typescript
{
  address: 'invalid_address',
  reason: 'Invalid Bech32m checksum'
}
```

**Solution**:
```typescript
if (error.code === 'INVALID_ADDRESS') {
  showMessage('Invalid recipient address');
}
```

#### TRANSACTION_FAILED
**Description**: Transaction execution failed.

**Cause**: Contract revert, gas limit, or validation failure.

**Details**:
```typescript
{
  txHash: '0x...',
  reason: 'Contract execution reverted',
  gasUsed: 21000n
}
```

**Solution**:
```typescript
if (error.code === 'TRANSACTION_FAILED') {
  console.error('Transaction failed:', error.details.reason);
  showMessage('Transaction failed. Please try again.');
}
```

#### TRANSACTION_TIMEOUT
**Description**: Transaction not confirmed within timeout.

**Cause**: Network congestion or low gas price.

**Solution**:
```typescript
if (error.code === 'TRANSACTION_TIMEOUT') {
  // Transaction may still confirm later
  showMessage('Transaction pending. Check status later.');
}
```

#### NONCE_TOO_LOW
**Description**: Transaction nonce already used.

**Cause**: Duplicate transaction or stale nonce.

**Solution**:
```typescript
if (error.code === 'NONCE_TOO_LOW') {
  // Refresh nonce and retry
  const newNonce = await getAccountNonce(address);
  tx.nonce = newNonce;
  await submitTransaction(tx);
}
```

#### NONCE_TOO_HIGH
**Description**: Transaction nonce too far in future.

**Cause**: Nonce gap in transaction sequence.

**Solution**:
```typescript
if (error.code === 'NONCE_TOO_HIGH') {
  // Wait for previous transactions to confirm
  await waitForNonceSync(address);
}
```

### Network Errors

#### NETWORK_ERROR
**Description**: Network communication failed.

**Cause**: Connection timeout, DNS failure, or server unavailable.

**Solution**:
```typescript
if (error.code === 'NETWORK_ERROR') {
  // Retry with exponential backoff
  await retryWithBackoff(operation);
}
```

#### UNSUPPORTED_NETWORK
**Description**: Network not supported by wallet or DApp.

**Cause**: Wrong network selected in wallet.

**Details**:
```typescript
{
  current: 'mainnet',
  supported: ['testnet', 'preprod']
}
```

**Solution**:
```typescript
if (error.code === 'UNSUPPORTED_NETWORK') {
  showMessage(`Please switch to ${error.details.supported.join(' or ')}`);
}
```

#### NETWORK_MISMATCH
**Description**: Network ID mismatch between wallet and DApp.

**Cause**: Wallet on different network than DApp expects.

**Solution**:
```typescript
if (error.code === 'NETWORK_MISMATCH') {
  await wallet.switchNetwork(expectedNetworkId);
}
```

#### RPC_ERROR
**Description**: RPC node returned error.

**Cause**: Node error, invalid request, or rate limiting.

**Details**:
```typescript
{
  code: -32603,
  message: 'Internal error'
}
```

**Solution**:
```typescript
if (error.code === 'RPC_ERROR') {
  // Try different RPC endpoint
  await switchRPCEndpoint();
}
```

### Proof Generation Errors

#### PROOF_GENERATION_FAILED
**Description**: Failed to generate zero-knowledge proof.

**Cause**: Invalid witness, circuit error, or prover timeout.

**Details**:
```typescript
{
  circuit: 'transfer',
  reason: 'Witness computation failed'
}
```

**Solution**:
```typescript
if (error.code === 'PROOF_GENERATION_FAILED') {
  // Retry or use different prover
  await retryWithDifferentProver();
}
```

#### PROOF_VERIFICATION_FAILED
**Description**: Proof verification failed.

**Cause**: Invalid proof, wrong public inputs, or corrupted data.

**Solution**:
```typescript
if (error.code === 'PROOF_VERIFICATION_FAILED') {
  // Regenerate proof
  const newProof = await generateProof(witness);
}
```

#### PROVER_UNAVAILABLE
**Description**: Proof server unavailable.

**Cause**: Server down, network issues, or rate limiting.

**Solution**:
```typescript
if (error.code === 'PROVER_UNAVAILABLE') {
  // Use local proving or retry
  await useLocalProving();
}
```

### Contract Errors

#### CONTRACT_NOT_FOUND
**Description**: Contract not found at address.

**Cause**: Wrong address, contract not deployed, or wrong network.

**Solution**:
```typescript
if (error.code === 'CONTRACT_NOT_FOUND') {
  showMessage('Contract not found. Please check address.');
}
```

#### CONTRACT_EXECUTION_FAILED
**Description**: Contract execution reverted.

**Cause**: Contract logic error, assertion failure, or invalid state.

**Details**:
```typescript
{
  contract: '0x...',
  method: 'transfer',
  revertReason: 'Insufficient balance'
}
```

**Solution**:
```typescript
if (error.code === 'CONTRACT_EXECUTION_FAILED') {
  console.error('Contract error:', error.details.revertReason);
}
```

#### INVALID_CONTRACT_CALL
**Description**: Invalid contract call parameters.

**Cause**: Wrong method signature, invalid arguments, or type mismatch.

**Solution**:
```typescript
if (error.code === 'INVALID_CONTRACT_CALL') {
  // Validate parameters
  validateContractParams(method, args);
}
```

### State Errors

#### STATE_SYNC_FAILED
**Description**: Failed to sync wallet state.

**Cause**: Indexer unavailable, network error, or corrupted state.

**Solution**:
```typescript
if (error.code === 'STATE_SYNC_FAILED') {
  // Retry sync
  await wallet.sync(indexerUri);
}
```

#### STALE_STATE
**Description**: Operation using outdated state.

**Cause**: State not synced before operation.

**Solution**:
```typescript
if (error.code === 'STALE_STATE') {
  // Sync and retry
  await wallet.sync(indexerUri);
  await retryOperation();
}
```

#### COIN_NOT_FOUND
**Description**: Coin not found in wallet.

**Cause**: Coin already spent or not synced.

**Solution**:
```typescript
if (error.code === 'COIN_NOT_FOUND') {
  await wallet.sync(indexerUri);
}
```

#### COIN_ALREADY_SPENT
**Description**: Attempting to spend already spent coin.

**Cause**: Double-spend attempt or stale state.

**Solution**:
```typescript
if (error.code === 'COIN_ALREADY_SPENT') {
  await wallet.sync(indexerUri);
  // Select different coins
}
```

### Validation Errors

#### INVALID_PARAMETER
**Description**: Invalid parameter value.

**Cause**: Type mismatch, out of range, or null value.

**Details**:
```typescript
{
  parameter: 'amount',
  value: -100,
  expected: 'positive bigint'
}
```

**Solution**:
```typescript
if (error.code === 'INVALID_PARAMETER') {
  const { parameter, expected } = error.details;
  showMessage(`Invalid ${parameter}. Expected: ${expected}`);
}
```

#### MISSING_PARAMETER
**Description**: Required parameter missing.

**Details**:
```typescript
{
  parameter: 'recipient'
}
```

**Solution**:
```typescript
if (error.code === 'MISSING_PARAMETER') {
  showMessage(`Missing required field: ${error.details.parameter}`);
}
```

#### INVALID_SIGNATURE
**Description**: Signature verification failed.

**Cause**: Wrong private key, corrupted signature, or tampered data.

**Solution**:
```typescript
if (error.code === 'INVALID_SIGNATURE') {
  // Re-sign transaction
  const newSignature = await wallet.signTransaction(tx);
}
```

### Rate Limiting Errors

#### RATE_LIMIT_EXCEEDED
**Description**: Too many requests.

**Cause**: Exceeded API rate limits.

**Details**:
```typescript
{
  limit: 100,
  window: 60000,  // 1 minute
  retryAfter: 30000  // 30 seconds
}
```

**Solution**:
```typescript
if (error.code === 'RATE_LIMIT_EXCEEDED') {
  const { retryAfter } = error.details;
  await sleep(retryAfter);
  await retryOperation();
}
```

## Error Handling Patterns

### Basic Pattern

```typescript
try {
  await operation();
} catch (error) {
  if (error.code) {
    handleKnownError(error);
  } else {
    handleUnknownError(error);
  }
}
```

### Comprehensive Handler

```typescript
function handleMidnightError(error: APIError): void {
  // User actions - don't show as errors
  if (error.code === 'USER_REJECTED' || error.code === 'USER_TIMEOUT') {
    console.log('User cancelled operation');
    return;
  }
  
  // Retryable errors
  const retryable = [
    'NETWORK_ERROR',
    'RPC_ERROR',
    'STATE_SYNC_FAILED',
    'PROVER_UNAVAILABLE'
  ];
  
  if (retryable.includes(error.code)) {
    showRetryPrompt(error);
    return;
  }
  
  // User-fixable errors
  const userFixable = [
    'INSUFFICIENT_FUNDS',
    'INVALID_ADDRESS',
    'INVALID_AMOUNT',
    'UNSUPPORTED_NETWORK'
  ];
  
  if (userFixable.includes(error.code)) {
    showUserError(error);
    return;
  }
  
  // System errors
  console.error('System error:', error);
  showSystemError(error);
}
```

### Retry Pattern

```typescript
async function withErrorHandling<T>(
  operation: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  const retryableCodes = [
    'NETWORK_ERROR',
    'RPC_ERROR',
    'PROVER_UNAVAILABLE',
    'STATE_SYNC_FAILED'
  ];
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      // Don't retry non-retryable errors
      if (!retryableCodes.includes(error.code)) {
        throw error;
      }
      
      // Last attempt - throw error
      if (i === maxRetries - 1) {
        throw error;
      }
      
      // Wait before retry
      const delay = 1000 * Math.pow(2, i);
      console.log(`Retry ${i + 1}/${maxRetries} in ${delay}ms...`);
      await sleep(delay);
    }
  }
  
  throw new Error('Max retries exceeded');
}
```

## Error Categories

### Critical Errors (Stop Execution)
- `WALLET_NOT_FOUND`
- `UNSUPPORTED_API_VERSION`
- `CONTRACT_NOT_FOUND`
- `INVALID_SIGNATURE`

### Retryable Errors (Auto-Retry)
- `NETWORK_ERROR`
- `RPC_ERROR`
- `STATE_SYNC_FAILED`
- `PROVER_UNAVAILABLE`
- `TRANSACTION_TIMEOUT`

### User-Fixable Errors (Show Message)
- `INSUFFICIENT_FUNDS`
- `INVALID_ADDRESS`
- `INVALID_AMOUNT`
- `UNSUPPORTED_NETWORK`
- `NETWORK_MISMATCH`

### User Actions (Not Errors)
- `USER_REJECTED`
- `USER_TIMEOUT`

## Best Practices

### 1. Check Error Codes

```typescript
// ✅ Check specific error codes
if (error.code === 'INSUFFICIENT_FUNDS') {
  // Handle specifically
}

// ❌ Generic error handling
catch (error) {
  console.error(error);  // Too generic
}
```

### 2. Use Error Details

```typescript
// ✅ Use error details
if (error.code === 'INSUFFICIENT_FUNDS') {
  const { required, available } = error.details;
  showMessage(`Need ${required}, have ${available}`);
}
```

### 3. Don't Retry User Actions

```typescript
// ✅ Don't retry user rejections
if (error.code === 'USER_REJECTED') {
  return;  // User intentionally cancelled
}

// ❌ Retrying user rejection
await retryOperation();  // Will fail again
```

### 4. Log System Errors

```typescript
// ✅ Log unexpected errors
if (!knownErrorCodes.includes(error.code)) {
  console.error('Unexpected error:', error);
  reportToMonitoring(error);
}
```

### 5. Provide User-Friendly Messages

```typescript
// ✅ User-friendly messages
const messages = {
  'INSUFFICIENT_FUNDS': 'You don\'t have enough funds',
  'NETWORK_ERROR': 'Connection failed. Please try again.',
  'INVALID_ADDRESS': 'Invalid recipient address'
};

showMessage(messages[error.code] || 'An error occurred');
```

## Resources

- **Integration Patterns**: See integration-patterns.md
- **DApp Connector API**: See dapp-connector-api.md
- **Error Handling Examples**: See api-examples.md

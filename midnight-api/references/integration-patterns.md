# Integration Patterns

## Error Handling

```typescript
try {
  const api = await window.midnight.wallet.connect('mainnet');
  const tx = await api.makeTransfer([...]);
  await api.submitTransaction(tx);
} catch (error) {
  if (error.code === 'USER_REJECTED') {
    console.log('User rejected transaction');
  } else if (error.code === 'INSUFFICIENT_FUNDS') {
    console.log('Insufficient balance');
  } else {
    console.error('Transaction failed:', error);
  }
}
```

## Retry Logic

```typescript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * Math.pow(2, i));
    }
  }
}
```

## State Synchronization

```typescript
// Poll for transaction confirmation
async function waitForConfirmation(txHash, indexerUri) {
  while (true) {
    const tx = await queryTransaction(txHash, indexerUri);
    if (tx.confirmed) return tx;
    await sleep(5000);
  }
}
```

## Best Practices

1. **Always validate inputs** before submitting transactions
2. **Handle user rejections** gracefully
3. **Provide clear error messages** to users
4. **Use proof servers** for better UX (delegate proving)
5. **Cache blockchain data** to reduce API calls
6. **Implement retry logic** for network failures
7. **Monitor transaction status** after submission

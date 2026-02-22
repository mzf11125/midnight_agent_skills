# Wallet API Reference

## Key Management

```typescript
// Generate new wallet
const wallet = await Wallet.generate();

// From seed phrase
const wallet = await Wallet.fromSeedPhrase(seedPhrase);

// Get addresses
const shieldedAddress = wallet.getShieldedAddress();
const unshieldedAddress = wallet.getUnshieldedAddress();
```

## Transaction Signing

```typescript
const signedTx = await wallet.signTransaction(transaction);
```

## State Management

```typescript
// Sync wallet state
await wallet.sync(indexerUri);

// Get balances
const balances = wallet.getBalances();
```

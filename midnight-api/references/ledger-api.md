# Ledger API Reference

## Token Types

```typescript
import { nativeToken, TokenType } from '@midnight-ntwrk/ledger';

const night = nativeToken();  // Native token
```

## Transaction Submission

```typescript
import { submitTransaction } from '@midnight-ntwrk/ledger';

await submitTransaction(signedTx, nodeUri);
```

## Block Queries

```typescript
const block = await getBlock(blockNumber, indexerUri);
const latestBlock = await getLatestBlock(indexerUri);
```

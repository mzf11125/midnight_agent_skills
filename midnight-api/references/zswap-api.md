# ZSwap API Reference

**Package**: `@midnight/zswap v3.0.2`

## Setup

```typescript
import { setNetworkId, NetworkId } from '@midnight/zswap';
setNetworkId(NetworkId.TestNet);
```

## Transaction Structure

### Transaction
Runs in two phases:
- **Guaranteed Phase**: Fee payments, fast operations (always executes)
- **Fallible Phase**: Contract calls, may fail atomically

### Offer
Consists of:
- **Inputs**: Coins being spent (burned)
- **Outputs**: New coins being created
- **Transients**: Coins created and spent in same transaction
- **Balance**: Mapping from TokenType to offer balance

## Proof Stages

Transactions progress through stages:
1. **UnprovenX**: Initial stage
2. **X**: After proving via proof server
3. **ProofErasedX**: For testing (via `eraseProof[s]`)

## Coin Management

### CoinInfo
```typescript
interface CoinInfo {
  tokenType: TokenType;
  value: bigint;
  nonce: Field;
}
```

### QualifiedCoinInfo
CoinInfo with Merkle tree index for spending.

## Creating Inputs/Outputs

### User-Owned Input
```typescript
const input = Input.fromQualifiedCoinInfo(qualifiedCoinInfo, zswapLocalState);
```

### Contract-Owned Input
```typescript
const input = Input.fromQualifiedCoinInfo(qualifiedCoinInfo, contractAddress);
```

### User-Owned Output
```typescript
const output = Output.fromCoinInfo(coinInfo, userPublicKey);
```

### Contract-Owned Output
```typescript
const output = Output.fromCoinInfo(coinInfo, contractAddress);
```

## State

### ZswapChainState
On-chain state of Zswap.

### ZswapLocalState
Local wallet state.

# Ledger Models: UTXO vs Account

## Overview

Midnight's **unique hybrid architecture** supports BOTH the UTXO model (Bitcoin-style) and Account model (Ethereum-style). This isn't just flexibility—it's a strategic design that lets you choose the right tool for each use case.

## The Fundamental Difference

### Account Model (Ethereum-Style)

**Think: Bank Account**

```
Alice's Account: 100 NIGHT
Bob's Account: 50 NIGHT

Transfer 40 NIGHT:
Alice: 100 - 40 = 60 NIGHT
Bob: 50 + 40 = 90 NIGHT
```

- **Global state**: One big database of all accounts
- **Mutable balances**: Numbers that change
- **Sequential**: Transactions touching same account must be ordered

### UTXO Model (Bitcoin-Style)

**Think: Physical Cash**

```
Alice has: [100 NIGHT coin]
Bob has: [50 NIGHT coin]

Transfer 40 NIGHT:
Consume: Alice's 100 NIGHT coin
Create: Bob's 40 NIGHT coin + Alice's 60 NIGHT coin (change)
```

- **Discrete coins**: Individual unspent outputs
- **Immutable**: Coins consumed entirely, new ones created
- **Parallel**: Independent coins can be spent simultaneously

## Midnight's Hybrid Approach

### Two Token Types

#### 1. Ledger Tokens (UTXO-Based)

**Native to Midnight's blockchain ledger**

```compact
// NIGHT tokens are ledger tokens
const nightCoin: UTXO = {
  value: 100_000_000n, // 100 NIGHT
  owner: myAddress,
  tokenType: nativeToken()
};
```

**Characteristics**:
- Individual UTXOs on the ledger
- Can be shielded or unshielded
- Parallel processing
- Privacy-friendly
- NIGHT token is the prime example

**Use Cases**:
- High-volume payments
- Private transactions
- Cross-chain bridges
- Atomic swaps

#### 2. Contract Tokens (Account-Based)

**Live inside Compact smart contracts**

```compact
// ERC-20 style token in Compact
ledger balances: Map<Address, Uint<64>>;

export circuit transfer(to: Address, amount: Uint<64>): [] {
  const from = ownAddress();
  balances.lookup(from).decrement(amount);
  balances.lookup(to).increment(amount);
}
```

**Characteristics**:
- Mapping of addresses to balances
- Managed by contract code
- Rich state interactions
- Familiar to Ethereum devs

**Use Cases**:
- Complex DeFi protocols
- Gaming tokens
- Governance tokens
- Social tokens

## Deep Comparison

### Account Model Details

#### How It Works
```typescript
// Global state (simplified)
const accounts = {
  "0xAlice": { balance: 100, nonce: 5 },
  "0xBob": { balance: 50, nonce: 3 }
};

// Transaction
function transfer(from, to, amount) {
  accounts[from].balance -= amount;
  accounts[to].balance += amount;
  accounts[from].nonce += 1;
}
```

#### Nonces: The Sequential Enforcer
```typescript
// Alice's transactions MUST be sequential
tx1: { nonce: 5, ... }  // ✅ Processes
tx2: { nonce: 7, ... }  // ❌ Waits for nonce 6
tx3: { nonce: 6, ... }  // ✅ Unblocks tx2
```

**Problem**: One stuck transaction blocks all subsequent ones.

#### MEV (Maximal Extractable Value)
```typescript
// User submits trade (visible in mempool)
userTrade = { swap: "1000 USDC → ETH" };

// Bot front-runs
botTrade = { swap: "500 USDC → ETH", gasPrice: 500 }; // Higher gas

// Block order: [botTrade, userTrade]
// Bot profits from user's price impact
```

**Problem**: Transparent mempool enables exploitation.

#### Privacy: Nearly Impossible
```
Your Address: 0x742d35Cc...
├── Balance: 50.23 ETH (PUBLIC)
├── All Transactions: (PUBLIC)
│   ├── From Coinbase (links identity)
│   ├── To DEX (reveals trading)
│   └── ... complete history
└── All Token Balances: (PUBLIC)
```

**Problem**: Everything is permanently public.

### UTXO Model Details

#### How It Works
```typescript
// UTXOs (discrete coins)
const utxos = [
  { id: "abc", value: 100, owner: "Alice" },
  { id: "def", value: 50, owner: "Bob" }
];

// Transaction
function transfer(inputUTXO, recipient, amount) {
  // Consume input entirely
  markSpent(inputUTXO);
  
  // Create new outputs
  createUTXO({ value: amount, owner: recipient });
  createUTXO({ value: inputUTXO.value - amount, owner: inputUTXO.owner }); // Change
}
```

#### Nullifier Set (Midnight's Innovation)
```typescript
// When UTXO is spent
const nullifier = hash(utxo, ownerSecret);
nullifierSet.add(nullifier);

// Prevents double-spending
if (nullifierSet.has(nullifier)) {
  reject("Already spent!");
}
```

**Advantage**: Works even with hidden values (privacy).

#### Natural Parallelism
```typescript
// These can process simultaneously
tx1: Spend UTXO_A → Send to Bob
tx2: Spend UTXO_B → Send to Carol
// Different UTXOs = no conflict
```

**Advantage**: 10-100x better throughput potential.

#### Privacy Built-In
```typescript
// Alice's UTXOs (can use different addresses)
UTXO_1: { value: 100, owner: Address_A }  // Salary
UTXO_2: { value: 50, owner: Address_B }   // Shopping
UTXO_3: { value: 25, owner: Address_C }   // Donations

// Shielded UTXOs hide even more
ShieldedUTXO: { commitment: hash(value, nonce, owner) }
// Value and owner hidden, only commitment visible
```

**Advantage**: Natural isolation + shielding option.

## When to Use Each Model

### Use Ledger Tokens (UTXO) When:

✅ **High-volume payments**
```compact
// Payment processor handling thousands of transactions
// Each payment is independent UTXO
```

✅ **Privacy is critical**
```compact
// Shielded tokens for confidential transfers
const shieldedCoin = mintShieldedToken(amount, recipient);
```

✅ **Parallel processing needed**
```compact
// Multiple users spending different UTXOs simultaneously
// No bottlenecks
```

✅ **Atomic operations**
```compact
// Swap: Consume UTXO_A, Create UTXO_B
// All-or-nothing, no partial states
```

✅ **Cross-chain bridges**
```compact
// Lock UTXO on Chain A, mint on Chain B
// Clear ownership transfer
```

### Use Contract Tokens (Account) When:

✅ **Complex DeFi logic**
```compact
// AMM with liquidity pools
ledger reserves: Map<TokenType, Uint<64>>;
ledger liquidityShares: Map<Address, Uint<64>>;

export circuit swap(tokenIn: TokenType, amountIn: Uint<64>): Uint<64> {
  // Complex state interactions
  const reserveIn = reserves.lookup(tokenIn).read();
  const reserveOut = reserves.lookup(tokenOut).read();
  // ... AMM math
}
```

✅ **Gaming mechanics**
```compact
// In-game currency with complex rules
ledger playerBalances: Map<PlayerId, Uint<64>>;
ledger playerLevel: Map<PlayerId, Uint<8>>;

export circuit earnReward(player: PlayerId): [] {
  const level = playerLevel.lookup(player).read();
  const reward = calculateReward(level);
  playerBalances.lookup(player).increment(reward);
}
```

✅ **Governance systems**
```compact
// Voting with delegation
ledger votingPower: Map<Address, Uint<64>>;
ledger delegations: Map<Address, Address>;

export circuit delegate(to: Address): [] {
  const from = ownAddress();
  delegations.insert(from, to);
  // Transfer voting power
}
```

✅ **Rich state interactions**
```compact
// Multiple related state variables
ledger userProfiles: Map<Address, Profile>;
ledger relationships: Map<Address, Set<Address>>;
ledger reputation: Map<Address, Uint<32>>;
```

## Hybrid Patterns

### Pattern 1: UTXO for Value, Account for Logic

```compact
// Use NIGHT (UTXO) for payments
import { sendShielded, receiveShielded } from CompactStandardLibrary;

// Use contract tokens for game logic
ledger gameTokens: Map<PlayerId, Uint<64>>;

export circuit buyGameTokens(amount: Uint<64>): [] {
  // Receive NIGHT (UTXO)
  receiveShielded(nativeToken(), amount);
  
  // Mint game tokens (Account)
  const player = ownAddress();
  gameTokens.lookup(player).increment(amount);
}
```

### Pattern 2: Public Account, Private UTXO

```compact
// Public leaderboard (Account)
ledger publicScores: Map<PlayerId, Uint<32>>;

// Private rewards (UTXO)
witness myRewardCoins(): Vector<10, ShieldedCoinInfo>;

export circuit claimReward(): [] {
  const score = publicScores.lookup(ownAddress()).read();
  const reward = calculateReward(score);
  
  // Send shielded UTXO
  sendShielded(nativeToken(), reward, ownAddress());
}
```

### Pattern 3: Atomic Swap Between Models

```compact
export circuit swapAccountForUTXO(
  accountAmount: Uint<64>,
  utxoRecipient: Address
): [] {
  // Burn account tokens
  accountBalances.lookup(ownAddress()).decrement(accountAmount);
  
  // Mint UTXO
  sendUnshielded(nativeToken(), accountAmount, utxoRecipient);
}
```

## Performance Implications

### Account Model Performance

**Bottlenecks**:
- Sequential nonce requirement
- Global state contention
- All nodes re-execute code

**Throughput**: ~15-30 TPS (Ethereum)

### UTXO Model Performance

**Advantages**:
- Parallel UTXO processing
- No nonce bottlenecks
- Proof verification (not re-execution)

**Throughput**: 100-1000+ TPS potential

### Midnight's Hybrid

**Best of Both**:
- UTXO for high-throughput payments
- Account for complex logic
- Choose per use case

## Privacy Implications

### Account Model Privacy

❌ **All balances public**
❌ **All transactions linked**
❌ **Complete history visible**
❌ **Mixers only break links at specific points**

### UTXO Model Privacy

✅ **Individual UTXOs can be shielded**
✅ **Different addresses per UTXO**
✅ **No global balance to query**
✅ **Shielded UTXOs hide value and owner**

### Midnight's Approach

**Rational Privacy**:
- Shielded UTXOs when privacy needed
- Unshielded when transparency needed
- Viewing keys for compliance
- User controls disclosure

## Migration Guide

### From Ethereum (Account) to Midnight

**Familiar**: Contract tokens work like ERC-20
```solidity
// Ethereum
mapping(address => uint256) balances;

function transfer(address to, uint256 amount) {
    balances[msg.sender] -= amount;
    balances[to] += amount;
}
```

```compact
// Midnight (same pattern)
ledger balances: Map<Address, Uint<64>>;

export circuit transfer(to: Address, amount: Uint<64>): [] {
    balances.lookup(ownAddress()).decrement(amount);
    balances.lookup(to).increment(amount);
}
```

**New**: Ledger tokens (UTXO) for better performance
```compact
// Use NIGHT tokens for high-volume transfers
import { sendShielded } from CompactStandardLibrary;

export circuit fastTransfer(to: Address, amount: Uint<64>): [] {
    sendShielded(nativeToken(), amount, to);
}
```

### From Bitcoin (UTXO) to Midnight

**Familiar**: Ledger tokens work like Bitcoin
```
// Bitcoin
Input: UTXO(100 BTC)
Outputs: [UTXO(40 BTC, Bob), UTXO(60 BTC, Alice)]
```

```compact
// Midnight (same pattern)
const input = myUTXO; // 100 NIGHT
sendShielded(nativeToken(), 40, bob);
// Change automatically created: 60 NIGHT back to me
```

**New**: Contract tokens for complex logic
```compact
// Use contract tokens for DeFi
ledger liquidityPool: Map<TokenType, Uint<64>>;

export circuit addLiquidity(amount: Uint<64>): [] {
    liquidityPool.lookup(nativeToken()).increment(amount);
}
```

## Decision Matrix

| Requirement | Ledger Tokens (UTXO) | Contract Tokens (Account) |
|-------------|---------------------|--------------------------|
| High throughput | ✅ Excellent | ⚠️ Limited |
| Privacy | ✅ Shielding available | ❌ Difficult |
| Complex logic | ⚠️ Limited | ✅ Excellent |
| Parallel processing | ✅ Natural | ❌ Sequential |
| Familiar to Ethereum devs | ❌ New model | ✅ Familiar |
| Atomic operations | ✅ Built-in | ⚠️ Requires care |
| State management | ⚠️ Stateless | ✅ Rich state |
| Cross-chain | ✅ Clear ownership | ⚠️ Complex |

## Summary

Midnight's hybrid architecture is a **strategic advantage**:

- **UTXO (Ledger Tokens)**: Privacy, parallelism, performance
- **Account (Contract Tokens)**: Complex logic, familiar patterns
- **Choose per use case**: Not forced into one model
- **Combine both**: Hybrid patterns for best results

Understanding both models and when to use each is key to building optimal Midnight applications.

## Resources

- **Account Model Deep Dive**: https://docs.midnight.network/concepts/account
- **UTXO Model Deep Dive**: https://docs.midnight.network/concepts/utxo
- **Ledgers Comparison**: https://docs.midnight.network/concepts/ledgers
- **Compact Language**: See midnight-compact skill

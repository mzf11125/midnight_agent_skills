# Ledger Operations

## Overview

Ledger operations manage **on-chain state** in Compact contracts. The ledger is the public, replicated state visible to all network participants.

## Ledger Declarations

### Syntax
```compact
ledger fieldName: LedgerType;
export ledger publicField: Type;
sealed ledger immutableField: Type;
```

- **`ledger`**: Declares on-chain state
- **`export`**: Makes field visible outside contract
- **`sealed`**: Immutable after constructor (can only be set during initialization)

### Example
```compact
ledger counter: Counter;
export ledger totalSupply: Uint<64>;
sealed ledger owner: Bytes<32>;
```

## Ledger State Types

### 1. Cell<T> (Implicit)

**Any Compact type becomes a Cell automatically.**

```compact
ledger value: Field;           // Actually Cell<Field>
ledger flag: Boolean;          // Actually Cell<Boolean>
ledger data: Bytes<32>;        // Actually Cell<Bytes<32>>
```

#### Operations
```compact
// Read
const v = value.read();
const v = value;  // Shorthand

// Write
value.write(42);
value = 42;  // Shorthand

// Reset to default
value.reset_to_default();
```

### 2. Counter

**Monotonic counter that can only increment/decrement.**

```compact
ledger count: Counter;
```

#### Operations
```compact
// Read
const c = count.read();
const c = count;  // Shorthand

// Increment
count.increment(5);
count += 5;  // Shorthand

// Decrement
count.decrement(3);
count -= 3;  // Shorthand
```

#### Use Cases
- Vote counts
- Token supply tracking
- Round numbers (for unlinkability)
- Sequence numbers

### 3. Set<T>

**Unordered collection of unique values.**

```compact
ledger participants: Set<Address>;
ledger usedNonces: Set<Bytes<32>>;
```

#### Operations
```compact
// Insert
participants.insert(address);

// Remove
participants.remove(address);

// Contains
const exists = participants.contains(address);

// Size
const size = participants.size();

// Clear
participants.clear();
```

#### Use Cases
- Whitelist/blacklist addresses
- Track used nonces
- Membership lists
- Unique identifiers

### 4. Map<K, V>

**Key-value mapping.**

```compact
ledger balances: Map<Address, Uint<64>>;
ledger metadata: Map<Bytes<32>, Bytes<256>>;
```

#### Operations
```compact
// Insert
balances.insert(address, 1000);

// Lookup (returns V or nested state type)
const balance = balances.lookup(address).read();

// Remove
balances.remove(address);

// Contains
const exists = balances.contains(address);

// Size
const size = balances.size();
```

#### Nested State Types
```compact
ledger nested: Map<Address, Counter>;

// Initialize nested counter
nested.insert(address, default<Counter>);

// Use nested counter
nested.lookup(address).increment(1);
```

#### Use Cases
- Token balances
- User profiles
- Configuration settings
- Nested data structures

### 5. List<T>

**Ordered collection with index access.**

```compact
ledger items: List<Bytes<32>>;
ledger history: List<Uint<64>>;
```

#### Operations
```compact
// Push (append)
items.push("item1");

// Get by index
const item = items.get(0);

// Set by index
items.set(0, "updated");

// Length
const len = items.length();

// Pop (remove last)
const last = items.pop();
```

#### Use Cases
- Event logs
- Transaction history
- Ordered queues
- Time-series data

### 6. MerkleTree<n, T>

**Merkle tree for efficient membership proofs.**

```compact
ledger coinTree: MerkleTree<32, Bytes<32>>;  // 2^32 capacity
```

#### Operations
```compact
// Insert at index
coinTree.insert(index, commitment);

// Get by index
const value = coinTree.get(index);

// Root hash
const root = coinTree.root();

// Verify proof
const valid = coinTree.verify(index, value, proof);
```

#### Parameters
- **`n`**: Tree depth (1 < n ≤ 32)
- **Capacity**: 2^n leaves
- **`T`**: Leaf value type

#### Use Cases
- Coin commitments (Zswap)
- Nullifier sets
- Efficient membership proofs
- Privacy-preserving state

### 7. HistoricMerkleTree<n, T>

**Merkle tree that maintains historical roots.**

```compact
ledger stateTree: HistoricMerkleTree<32, Bytes<32>>;
```

#### Operations
Same as MerkleTree, plus:
```compact
// Get historical root
const oldRoot = stateTree.rootAt(blockNumber);

// Verify against historical root
const valid = stateTree.verifyHistoric(index, value, proof, blockNumber);
```

#### Use Cases
- State snapshots
- Historical proofs
- Rollback verification
- Audit trails

## Syntactic Sugar

### Cell Operations
```compact
// Long form
value.write(42);
const x = value.read();

// Short form (preferred)
value = 42;
const x = value;
```

### Counter Operations
```compact
// Long form
counter.increment(5);
counter.decrement(3);
const c = counter.read();

// Short form (preferred)
counter += 5;
counter -= 3;
const c = counter;
```

### Ledger Assignment
```compact
// These are equivalent
ledgerField.write(value);
ledgerField = value;
```

## Kernel Operations

**Special operations that don't depend on specific ledger state.**

```compact
import CompactStandardLibrary;

// Get contract's own address
const addr = kernel.self();

// Other kernel operations available
```

## Disclosure

**Making private data public on the ledger.**

```compact
witness secretValue(): Field;

export circuit publishValue(): [] {
  const secret = secretValue();
  
  // Disclose makes it public
  publicValue = disclose(secret);
}
```

- **`disclose()`**: Marks data for public ledger storage
- **Without disclose**: Data stays private in proof
- **Use carefully**: Once disclosed, permanently public

## Constructor Initialization

```compact
constructor(initialOwner: Bytes<32>, initialSupply: Uint<64>) {
  owner = disclose(initialOwner);
  totalSupply = disclose(initialSupply);
  balances.insert(initialOwner, initialSupply);
}
```

- **Sealed fields**: Can only be set in constructor
- **Regular fields**: Can be set in constructor or circuits
- **Must disclose**: Values from parameters

## Sealed Fields

```compact
sealed ledger owner: Bytes<32>;
sealed ledger maxSupply: Uint<64>;

constructor(ownerAddr: Bytes<32>) {
  owner = disclose(ownerAddr);  // ✅ OK in constructor
  maxSupply = disclose(1000000);
}

export circuit changeOwner(newOwner: Bytes<32>): [] {
  owner = disclose(newOwner);  // ❌ ERROR: sealed field
}
```

**Use sealed for**:
- Contract configuration
- Immutable parameters
- Owner addresses (if unchangeable)
- Maximum limits

## Complete Example: Token Contract

```compact
pragma language_version 0.16;
import CompactStandardLibrary;

// Ledger state
export ledger totalSupply: Uint<64>;
ledger balances: Map<Address, Uint<64>>;
sealed ledger owner: Bytes<32>;

// Constructor
constructor(ownerAddr: Bytes<32>, initialSupply: Uint<64>) {
  owner = disclose(ownerAddr);
  totalSupply = disclose(initialSupply);
  balances.insert(ownerAddr, initialSupply);
}

// Transfer tokens
export circuit transfer(to: Address, amount: Uint<64>): [] {
  const from = ownAddress();
  
  // Check balance
  const balance = balances.lookup(from).read();
  assert(balance >= amount, "Insufficient balance");
  
  // Update balances
  balances.lookup(from).decrement(amount);
  
  // Initialize recipient if needed
  if (!balances.contains(to)) {
    balances.insert(to, 0);
  }
  balances.lookup(to).increment(amount);
}

// Get balance
export circuit balanceOf(addr: Address): Uint<64> {
  if (balances.contains(addr)) {
    return balances.lookup(addr).read();
  }
  return 0;
}

// Mint (owner only)
export circuit mint(amount: Uint<64>): [] {
  witness ownerSecret(): Bytes<32>;
  
  const secret = ownerSecret();
  const pk = hash(secret);
  assert(pk == owner, "Not owner");
  
  totalSupply += amount;
  balances.lookup(owner).increment(amount);
}
```

## Nested State Example

```compact
// Nested counters in map
ledger userScores: Map<Address, Counter>;

export circuit initUser(user: Address): [] {
  // Must initialize nested state
  userScores.insert(user, default<Counter>);
}

export circuit incrementScore(user: Address, points: Uint<32>): [] {
  // Use nested counter
  userScores.lookup(user).increment(points);
}

export circuit getScore(user: Address): Uint<64> {
  // Read nested counter (shorthand)
  return userScores.lookup(user);
}
```

## Nested Maps Example

```compact
// Map of maps
ledger permissions: Map<Address, Map<Resource, Boolean>>;

export circuit grantPermission(user: Address, resource: Resource): [] {
  // Initialize inner map if needed
  if (!permissions.contains(user)) {
    permissions.insert(user, default<Map<Resource, Boolean>>);
  }
  
  // Set permission
  permissions.lookup(user).insert(resource, true);
}

export circuit checkPermission(user: Address, resource: Resource): Boolean {
  if (!permissions.contains(user)) {
    return false;
  }
  
  const userPerms = permissions.lookup(user);
  if (!userPerms.contains(resource)) {
    return false;
  }
  
  return userPerms.lookup(resource).read();
}
```

## Best Practices

### 1. Initialize Nested State
```compact
// ❌ WRONG - will fail
ledger counters: Map<Address, Counter>;
counters.lookup(addr).increment(1);  // ERROR: not initialized

// ✅ CORRECT
counters.insert(addr, default<Counter>);
counters.lookup(addr).increment(1);
```

### 2. Check Existence
```compact
// ✅ Safe
if (balances.contains(addr)) {
  const balance = balances.lookup(addr).read();
}

// ⚠️ Unsafe - may fail if not exists
const balance = balances.lookup(addr).read();
```

### 3. Use Appropriate Types
```compact
// ❌ Overkill
ledger simpleFlag: Map<Address, Boolean>;

// ✅ Better
ledger allowedUsers: Set<Address>;

// ❌ Inefficient for counters
ledger voteCount: Map<VoteId, Uint<64>>;

// ✅ Better
ledger voteCount: Map<VoteId, Counter>;
```

### 4. Minimize Ledger Operations
```compact
// ❌ Multiple reads
const a = field.read();
const b = field.read();
const c = field.read();

// ✅ Single read
const value = field.read();
const a = value;
const b = value;
const c = value;
```

### 5. Use Sealed for Immutability
```compact
// ✅ Configuration that shouldn't change
sealed ledger maxUsers: Uint<32>;
sealed ledger contractVersion: Uint<8>;
```

## Common Patterns

### Pattern 1: Token Balance
```compact
ledger balances: Map<Address, Uint<64>>;

circuit transfer(to: Address, amount: Uint<64>): [] {
  const from = ownAddress();
  balances.lookup(from).decrement(amount);
  if (!balances.contains(to)) {
    balances.insert(to, 0);
  }
  balances.lookup(to).increment(amount);
}
```

### Pattern 2: Access Control
```compact
sealed ledger owner: Bytes<32>;
ledger admins: Set<Address>;

circuit requireOwner(): [] {
  witness ownerSecret(): Bytes<32>;
  assert(hash(ownerSecret()) == owner, "Not owner");
}

circuit requireAdmin(): [] {
  assert(admins.contains(ownAddress()), "Not admin");
}
```

### Pattern 3: Nonce Tracking
```compact
ledger usedNonces: Set<Bytes<32>>;

circuit useNonce(nonce: Bytes<32>): [] {
  assert(!usedNonces.contains(nonce), "Nonce already used");
  usedNonces.insert(nonce);
}
```

### Pattern 4: Event Log
```compact
ledger events: List<Bytes<64>>;

circuit logEvent(eventData: Bytes<64>): [] {
  events.push(eventData);
}

circuit getEvent(index: Uint<32>): Bytes<64> {
  return events.get(index);
}
```

## Performance Considerations

### Storage Costs
- **Cell**: Minimal (single value)
- **Counter**: Minimal (single value)
- **Set**: Grows with elements
- **Map**: Grows with entries
- **List**: Grows with length
- **MerkleTree**: Fixed size (2^n capacity)

### Operation Costs
- **Read**: Fast
- **Write**: Moderate
- **Insert/Remove**: Moderate
- **Merkle operations**: Expensive (cryptographic)

### Optimization Tips
1. **Batch operations** when possible
2. **Use Counters** instead of Uint in Maps
3. **Prune old data** from Lists/Sets
4. **Use MerkleTrees** for large datasets
5. **Minimize nested lookups**

## Resources

- **Ledger ADT Reference**: https://docs.midnight.network/compact/reference/ledger-adt
- **Type System**: See type-system.md
- **Circuit Semantics**: See circuit-semantics.md
- **Standard Library**: See standard-library.md

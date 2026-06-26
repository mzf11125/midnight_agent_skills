---
name: compact-core
description: Comprehensive guide to the Compact programming language for writing privacy-preserving smart contracts on Midnight Network. Use when users need to write Compact contracts, understand the full development lifecycle from compilation to deployment, work with data types and ledger operations, implement security patterns, handle token operations, debug and test contracts, manage contract versions, understand TypeScript interop, and follow best practices for zero-knowledge contract development.
---

# Compact Language: Complete Development Lifecycle

Comprehensive guide to writing testing deploying and maintaining privacy-preserving smart contracts with Compact.

## What is Compact

Compact is a purpose-built programming language for zero-knowledge smart contracts on Midnight. Unlike adapting existing languages Compact was designed from scratch to make privacy-preserving programming natural and secure.

**Key Design Goals**:
- Compile directly to efficient ZK circuits
- Type-safe cryptographic operations
- Familiar syntax for developers (TypeScript-like)
- Automatic proof generation
- Bounded for finite proving circuits

**Key Features**:
- Strong static typing with no unsafe type bypass
- Generic type and numeric parameters
- Explicit disclosure via `disclose()` wrappers
- Module-based namespace management
- Direct compilation to zkSNARK circuits

## Mental Model: Circuits vs Functions

The single most important shift when learning Compact: circuits declare constraints. They do not execute instructions.

```
Function: Input leads to Execute steps leads to Output
Circuit:  Input leads to Declare constraints leads to Generate proof leads to Verify proof
```

### What assert() Actually Is

In a function `assert` is a runtime guard that throws on failure.
In a circuit `assert` is a **constraint declaration**. It defines what valid inputs look like.

```compact
assert(balance >= amount, "Insufficient balance");
```

This does not say "check if balance is high enough then continue". It says "a proof for this circuit cannot exist if balance < amount". If the condition is false the proof cannot be generated. There is nothing to submit. The transaction never happens.

### What Return Values Mean in Circuits

In a function: compute the sum and hand it back.
In a circuit: **the output is constrained to equal a + b**. The proof proves this relationship held for actual inputs without revealing them.

### Why No Recursion or Unbounded Loops

ZK proofs require **finite circuits**. A fixed structure of gates and wires determined entirely at compile time. Unbounded computation cannot become a circuit. The bounds are not restrictions. They are what makes proof generation possible at all.

Use `map` and `fold` instead of loops with early returns.

## Contract Structure

### The Three-Part Architecture

Every Compact contract has three distinct components forming a unified whole.

**1. Replicated Component**:
- Declares public ledger state
- Contains `export ledger` declarations
- Visible to all network participants
- Compiled to Impact VM bytecode

**2. Zero-Knowledge Circuit**:
- Defines constraint-based computation
- Contains `export circuit` functions
- Generates ZK proofs of valid transitions
- Private inputs stay inside the circuit

**3. Local Component**:
- Runs on user's device
- Contains `witness` functions
- Handles arbitrary computation
- Manages private state off-chain

### Minimal Contract Example

```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger counter: Counter;
export ledger owner: Bytes<32>;

witness local_secret_key(): Bytes<32>;

export circuit increment(): [] {
  counter.increment(1);
}
```

### Export Circuit Functions

Circuit functions define what the contract can do and what must be proven.

```compact
export circuit transfer(
  private amount: Uint<64>,
  private sender: Bytes<32>,
  public recipient: Bytes<32>
): [] {
  assert(amount > 0, "Amount must be positive");
  assert(sender == owner, "Only owner can transfer");
  balances.decrement(sender, amount);
  balances.increment(recipient, amount);
}
```

**Parameter Visibility**:
- `private`: Hidden in ZK proof. Only known to prover.
- `public`: Visible on-chain. Everyone can see.
- Default is private. Explicit disclosure required for public state writes.

### Witness Functions

Witness functions provide private inputs to the circuit. They have no body.

```compact
witness get_user_secret(): Bytes<32>;
witness get_balance_proof(): Field;
witness get_encrypted_data(): Bytes<128>;
```

**What Witness Functions Do**:
- Declare the type of private data available
- Act as interface between local component and circuit
- No execution. They are declarations of available private inputs.
- Types must match exactly what the circuit expects
- Implemented by the TypeScript layer at runtime

### Constructor

```compact
export constructor(initial_owner: Bytes<32>): [] {
  owner = initial_owner;
  counter.increment(0);
}
```

The constructor runs once at contract creation. It initializes sealed ledger fields. All parameters are public by default in constructors.

## Data Types

### Boolean

```compact
const flag: Boolean = true;
const check: Boolean = false;
```
Values are `true` or `false`. Default is `false`. Corresponds to `boolean` in TypeScript.

### Unsigned Integers

**Bounded Integers**:
```compact
const age: Uint<0..150> = 25;
const pct: Uint<0..100> = 75;
```
Lower bound is currently always 0. Upper bound is inclusive.

**Sized Integers**:
```compact
const value: Uint<32> = 12345;
const small: Uint<8> = 255;
```
Equivalent to `Uint<0..2^n-1>`. Common sizes are 8 16 32 64 128 256.

### Field

```compact
const element: Field = 12345;
```
Scalar field elements for ZK circuits. Range is 0 to prime modulus minus 1. Arithmetic wraps modulo field size. Default is 0. Corresponds to `bigint` in TypeScript.

### CurvePoint

```compact
const point: CurvePoint = ecMulGenerator(scalar);
```
Points on the elliptic curve used for ZK proofs. Operations include `ecAdd` `ecMul` `ecMulGenerator`. Used in cryptographic protocols.

### Bytes

```compact
const hash: Bytes<32>;
const data: Bytes<64>;
```
Fixed-length byte arrays. String literals are UTF-8 encoded and padded. Default is all zeros. Corresponds to `Uint8Array` in TypeScript.

### Tuples

```compact
const pair: [Field, Boolean] = [42, true];
const triple: [Uint<8>, Uint<16>, Uint<32>] = [1, 2, 3];
const empty: [] = [];
```
Heterogeneous elements. Fixed length at compile time. Default is tuple of defaults for each element type.

### Vectors

```compact
const vec: Vector<5, Field> = [1, 2, 3, 4, 5];
```
Homogeneous elements. Shorthand for repeated tuple type. Default is vector of default values. Corresponds to `T[]` in TypeScript with length checks.

### Map

```compact
export ledger registry: Map<Bytes<32>, Bytes<64>>;
```
Key-value associations. Supports `lookup` and `insert` operations. Keys must be disclosed when writing to public ledger maps.

**Operations**:
```compact
const value = registry.lookup(key);
registry.insert(key, value);
```

### Set

```compact
export ledger whitelist: Set<Bytes<32>>;
```
Collection of unique elements. Supports `contains` and `insert`. Used for membership checks.

**Operations**:
```compact
const isMember = whitelist.contains(element);
whitelist.insert(element);
```

### Cell

The Cell type is deprecated. Use direct type declarations instead.

```compact
// Deprecated
export ledger value: Cell<Field>;

// Correct
export ledger value: Field;
```

### Custom Structs

```compact
struct Player {
  score: Uint<32>;
  level: Uint<8>;
  name: Bytes<32>;
}

export ledger players: Map<Bytes<32>, Player>;
```

**Struct Properties**:
- Named collections of fields
- Strongly typed
- Can be used in ledger state
- Read and written as whole units
- Each field access is O(1) in circuit size

### Custom Enums

```compact
enum GameState {
  waiting,
  playing,
  finished
}

export ledger state: GameState;
```

**Enum Properties**:
- Named variants
- Accessed with dot notation: `GameState.playing`
- Not Rust-style colon notation
- Default is first variant
- Comparisons use `==`

## Ledger Data Types

Ledger types define how on-chain state is stored and accessed. There are seven Abstract Data Type (ADT) variants.

### Counter

**Monotonic counter that can only increment or decrement**:
```compact
export ledger count: Counter;
```

Operations:
- `count.read()` or `count` to read
- `count.increment(n)` or `count += n` to increase
- `count.decrement(n)` or `count -= n` to decrease

Use cases include vote counts round numbers for unlinkability and sequence numbers.

### StateValue

**Single value with persistent and transient modes**:
```compact
export ledger data: StateValue<Field>;
```

Operations:
- `data.read()` to read value
- `data.write(value)` to commit value
- `data.transient(value)` for temporary value
- `data.persistent(value)` for permanent value

StateValue tracks whether data is committed persistently or transiently allowing different access patterns for different use cases.

### StateMap

**Key-value map with composite state tracking**:
```compact
export ledger balances: StateMap<Bytes<32>, Uint<64>>;
```

Operations:
- `balances.lookup(key)` to read value
- `balances.insert(key, value)` to write
- `balances.remove(key)` to delete

StateMap is the most common ledger type for contract storage. It supports efficient lookups and insertions.

### StateBoundedMerkleTree

**Merkle tree with bounded capacity for efficient membership proofs**:
```compact
export ledger tree: StateBoundedMerkleTree<32, Field>;
```

Operations:
- `tree.insert(leaf)` to add a leaf
- `tree.contains(leaf)` to check membership
- `tree.root()` to get Merkle root

Used for private membership proofs. The tree can hold up to the bounded number of leaves enabling efficient ZK proofs of inclusion.

### Seven ADT Types Reference

**Simple Types**:
1. Direct types: Field Boolean Uint Bytes (auto-wrapped as Cell-like)
2. Counter: monotonic counters
3. StateValue: single value with persistence modes
4. StateMap: key-value storage

**Composite Types**:
5. StateBoundedMerkleTree: bounded Merkle tree
6. StateUnboundedMerkleTree: unbounded Merkle tree for variable-size sets
7. StateQueue: ordered queue for sequential processing

## Ledger Operations

### Read Operations

```compact
const value = ledger_field.read();
const value = ledger_field;  // Shorthand
const mapValue = map.lookup(key);
const treeRoot = tree.root();
const isMember = tree.contains(element);
```

Reading state is always permitted. No proof is required to read public state though privacy boundaries still apply.

### Write Operations

```compact
ledger_field.write(newValue);
ledger_field = newValue;  // Shorthand
map.insert(key, value);
map.remove(key);
tree.insert(leaf);
counter.increment(amount);
counter.decrement(amount);
```

Writing state must happen through circuit functions. Direct writes from witnesses are not allowed.

### Hash Commitments

**Persistent Hash**:
```compact
const hash = data.persistentHash();
```
Creates a commitment to data stored permanently on-chain. The hash is public but data stays private until disclosed.

**Transient Hash**:
```compact
const hash = data.transientHash();
```
Creates a temporary commitment. Useful when data needs temporary privacy.

### Persistent Commit

```compact
ledger_field.persistentCommit(value);
```
Commits a value permanently to public state. This is a public operation visible to all.

### Transient Commit

```compact
ledger_field.transientCommit(value);
```
Commits a value temporarily. The commitment is public but the value may be revealed later or discarded.

### Degrade and Upgrade

```compact
ledger_field.degradeToTransient();
ledger_field.upgradeFromTransient();
```

**DegradeToTransient**: Converts persistent state to transient mode. Data becomes temporarily private.

**UpgradeFromTransient**: Converts transient state to persistent mode. Data becomes permanently public.

## Opaque Types

### Purpose of Opaque Types

Opaque types hide the underlying data structure. The compiler enforces separation between public and private representations.

**What Opaque Types Enable**:
- Hide complex data structures from public view
- Selective transparency for specific fields
- Different public and private representations
- Compiler-enforced privacy boundaries

### Defining Opaque Types

```compact
opaque UserProfile {
  name: Bytes<64>,
  age: Uint<8>,
  score: Uint<32>
}
```

The opaque wrapper hides the internal structure. Only explicitly disclosed fields are visible publicly.

### Accessing Opaque Types

```compact
const score = profile.score;
const name = disclose(profile.name);
```

Access within the circuit is direct. But to make it public you must use `disclose()`.

## Witness Functions

### What Witness Functions Are

Witness functions are the interface between the user's private local state and the ZK circuit. They declare what private data is available without implementing how it is obtained.

### Witness Patterns

**Simple Secret Witness**:
```compact
witness get_secret_key(): Bytes<32>;
```

**Structured Data Witness**:
```compact
witness get_user_data(): UserProfile;
```

**Computed Witness**:
```compact
witness get_merkle_path(): Vector<32, Field>;
```

### Witness Trust Model

**What Witnesses Mean for Security**:
- The circuit does not know where witnesses come from
- Witness values must be validated in the circuit
- Never trust witness values without verification
- Witnesses are user-supplied and potentially malicious

**Validation Patterns**:
```compact
export circuit submit_score(witness score: Uint<32>, public proof: Field): [] {
  assert(score <= 10000, "Score out of range");
  assert(verifyProof(proof, score), "Invalid proof");
  leaderboard.insert(disclose(msg.sender), disclose(score));
}
```

### Witness at the TypeScript Level

Witness functions are implemented in TypeScript at runtime.

```typescript
const witnessContext = {
  get_secret_key: (): Uint8Array => wallet.getPrivateKey(),
  get_user_data: (): UserProfile => loadFromStorage("profile"),
  get_merkle_path: (): bigint[] => computeMerklePath(),
};
```

## Circuit Functions

### What Circuit Functions Are

Circuit functions define the constraint system that must be satisfied for a valid proof. They are the core of a Compact contract.

### Circuit Function Signature

```compact
export circuit function_name(
  private param1: Type1,
  public param2: Type2
): ReturnType {
  // Constraint declarations
  assert(condition);
  // State transitions
  ledger_field.write(value);
  // Return value
  return result;
}
```

### Return Types

```compact
export circuit no_return(): [] {
  // Must return empty tuple []
}

export circuit with_return(): Field {
  return computed_value;
}
```

Void-like circuits return `[]`. Circuits returning values use the return type directly.

### Proof Generation Flow

1. User provides private witness data
2. Circuit constraints are checked against inputs
3. If all constraints hold a ZK proof is generated
4. Proof includes public outputs and the validity assertion
5. Proof is submitted on-chain
6. Network verifies the proof and updates public state

### Disclosure in Circuits

```compact
export circuit register(
  private user_data: Bytes<64>,
  public user_id: Bytes<32>
): [] {
  // Correct: explicit disclosure before public state write
  registry.insert(user_id, disclose(user_data));
}
```

Private data flowing into public state requires explicit `disclose()`. The compiler enforces this. Disclosing as late as possible minimizes privacy leaks.

## Standard Library

### Cryptographic Functions

**Hashing**:
```compact
import std::crypto;

const digest = crypto.hash(data);
const poseidon_hash = crypto.poseidon(data);
```

Poseidon is the ZK-friendly hash used in most circuits. It is optimized for circuit efficiency.

**Commitments**:
```compact
const committed = crypto.commit(value, randomness);
const transient = crypto.transientCommit(value);
const persistent = crypto.persistentCommit(value);
```

Commit and open pattern for hiding values with ability to reveal later.

**Elliptic Curve Operations**:
```compact
const gen_mul = crypto.ecMulGenerator(scalar);
const point_mul = crypto.ecMul(point, scalar);
const sum = crypto.ecAdd(point1, point2);
```

### Field Arithmetic

```compact
import std::field;

const sum = field.add(a, b);
const product = field.mul(a, b);
const difference = field.sub(a, b);
const quotient = field.div(a, b);
const inverse = field.inv(a);
const negation = field.neg(a);
```

All field operations modulo the field prime. Used for advanced ZK circuit arithmetic.

### Encoding and Decoding

```compact
import std::convert;

const bytes = convert.toBytes(value, 32);
const field_val = convert.fromBytes(bytes);
const encoded = convert.encode(value);
const decoded = convert.decode(encoded);
```

Conversion between Compact types for interoperability and storage.

### Blockchain Context

```compact
const blockNum = block.number;
const blockTime = block.timestamp;
const sender = msg.sender;
const txValue = msg.value;
const contract_addr = self.address;
```

Read-only context about the current transaction and block. Available inside circuit functions.

### Utility Functions

```compact
const min_val = min(a, b);
const max_val = max(a, b);
const is_eq = eq(a, b);
const padded = pad(32, "hello");
const choice = conditional ? value1 : value2;
```

Standard utility functions for common operations in circuits.

## Token Operations

### NIGHT Token

**Available in Both Forms**:
- Unshielded NIGHT: visible transaction amounts and parties
- Shielded NIGHT: private via Zswap protocol

**Unshielded NIGHT Operations**:
```compact
// Send unshielded NIGHT
const recipient: Bytes<32>;
native_transfer(recipient, amount);
```

**Shielded NIGHT Operations**:
Handled through Zswap protocol with coin commitments and nullifiers. See the Zswap section of core concepts.

### DUST Token

**Transaction Fee Token**:
- Generated automatically from NIGHT holdings
- Consumed by transaction fees
- Not directly transferable
- Managed by the protocol automatically

**DUST in Contracts**:
- Contract deployment costs DUST
- State storage costs DUST
- Circuit execution costs DUST
- No explicit DUST management in contract code

### FungibleToken

The OpenZeppelin-style token standard for Compact.

```compact
import contracts::FungibleToken;

contract MyToken: FungibleToken {
  // Inherits: transfer, balanceOf, totalSupply, mint, burn
}
```

### Token Transfers Between Contracts

**Receiver Pattern**:
```compact
const recipient: Either<ZswapCoinPublicKey, ContractAddress>;
transfer(recipient, amount, token_id);
```

The `Either` type allows transfers to both user addresses (ZswapCoinPublicKey) and contract addresses (ContractAddress).

## Security Patterns

### Replay Protection

**The Problem**:
Without replay protection a valid transaction proof could be resubmitted multiple times. This could drain funds or corrupt state.

**The Solution: Nullifier Pattern**:
```compact
export ledger spent_nonces: Set<Field>;

export circuit transfer(private nonce: Field): [] {
  const nullifier = hash(nonce, msg.sender);
  assert(!spent_nonces.contains(nullifier));
  spent_nonces.insert(disclose(nullifier));
  // Transfer logic
}
```

Each transaction includes a unique nonce. The nullifier derived from it prevents reuse.

### Domain Separation

**Why Domain Separation Matters**:
Without domain separation a proof valid for one contract might be valid for another. This creates cross-contract attack vectors.

**Implementation**:
```compact
const domain = hash(
  self.address,
  block.chain_id,
  "transfer_v1"
);
const signed_message = hash(domain, user_data);
```

Include contract address chain ID and function identifier in every signature. This binds proofs to specific contracts and functions.

### Nullifier Design

**Nullifier Requirements**:
- Unique per coin or action
- Deterministic from private data
- Cannot be linked back to the original coin or action
- Prevents double-spending without revealing which coin was spent

**Nullifier Derivation**:
```compact
const nullifier = hash(coin_secret, coin_serial_number);
```

The nullifier must derive from data the spender knows uniquely. Combined with a unique serial number per coin.

### Commitment Patterns

**Commit-Reveal**:
```compact
// Phase 1: Commit
export circuit commit_bid(
  private bid: Uint<64>,
  private randomness: Field,
  public commitment: Field
): [] {
  const computed = hash(bid, randomness);
  assert(commitment == computed);
  commitments.insert(disclose(msg.sender), disclose(commitment));
}

// Phase 2: Reveal
export circuit reveal_bid(
  private bid: Uint<64>,
  private randomness: Field
): [] {
  const stored = commitments.lookup(disclose(msg.sender));
  assert(stored == hash(bid, randomness));
  // Process the bid
}
```

Two-phase protocol. First commit to a value without revealing it. Later reveal and prove it matches the commitment.

### Front-Running Resistance

**The Problem**:
In public blockchains transaction ordering can be exploited. Observing pending transactions enables front-running.

**Midnight's Protections**:
- Private transactions cannot be observed in mempool
- ZK proofs hide transaction details until execution
- Nullifier system prevents double execution
- Commit-reveal patterns hide intent until reveal phase
- Ordering is determined by consensus not visibility

### Witness Trust

**The Golden Rule**:
Never trust witness values without cryptographic verification. Witnesses come from the user and can be anything.

**Verification Strategy**:
```compact
export circuit claim_reward(
  witness score: Uint<32>,
  public merkle_proof: Vector<32, Field>
): [] {
  const root = scores_tree.root();
  assert(verifyMerkleProof(root, merkle_proof, score));
  // Safe to use score now
}
```

Always verify witness data against on-chain cryptographic commitments before using it.

## Contract Updatability

### Maintenance Authority

```compact
export sealed ledger maintainer: Bytes<32>;

export circuit update_contract(new_code: Bytes<1024>): [] {
  assert(msg.sender == maintainer);
  // Contract update logic
}
```

The maintenance authority can update the contract. This is a powerful capability. Use with care and governance.

### Verifier Key Management

**What Verifier Keys Are**:
- Cryptographic keys used to verify ZK proofs
- Each contract has a verifier key
- New contract versions have new verifier keys
- Updating verifier keys changes proof verification

**Verifier Key Insertion**:
```typescript
await contractDeployment.insertVerifierKey(
  contractAddress,
  newVerifierKey,
  { from: maintainerAddress }
);
```

### Replace Authority

```compact
export circuit replace_authority(new_maintainer: Bytes<32>): [] {
  assert(msg.sender == maintainer);
  maintainer = new_maintainer;
}
```

Transfer contract maintenance to a new authority. Critical for governance transitions.

### Migration Patterns

**State Migration**:
```compact
export circuit migrate_state(new_contract: ContractAddress): [] {
  assert(msg.sender == maintainer);
  // Export state to new contract
  // Lock old contract
  migrated = true;
}
```

When upgrading contracts state can be migrated to the new contract. Old contract should be locked to prevent further interactions.

## Compilation Flow

### The compactc Compiler

**Compilation Steps**:
1. Parse Compact source files
2. Type-check and resolve imports
3. Lower to ZK Intermediate Representation (ZKIR)
4. Generate verifier key
5. Generate prover key
6. Output compiled contract artifacts

**Compiler Invocation**:
```bash
compactc compile contract.compact --output-dir ./build
compactc compile contract.compact --optimize --output-dir ./build
compactc compile contract.compact --debug --output-dir ./build
```

### ZKIR Output

**What ZKIR Is**:
- Zero-Knowledge Intermediate Representation
- Low-level representation of the ZK circuit
- Not meant for human consumption
- Feeds into the proof system backend

### Verifier Keys

**Purpose**:
- Public key for proof verification
- Deployed with the contract
- Used by all nodes to verify proofs
- Deterministic from the circuit definition

**Prover Keys**:
- Private key for proof generation
- Much larger than verifier keys
- Used by proof servers or client wallets
- Deterministic from the circuit definition

### Build Output

A compiled contract typically produces:
- `contract.compact.zki`: ZKIR output
- `contract.verifier.key`: Verifier key for deployment
- `contract.prover.key`: Prover key for proof generation
- `contract.metadata.json`: Contract metadata including type information
- TypeScript type definitions for interop

## TypeScript Interop

### Witness Context

```typescript
interface WitnessContext {
  get_secret_key(): Uint8Array;
  get_user_data(): UserProfile;
  get_proof_data(): bigint[];
  [key: string]: (...args: any[]) => any;
}
```

The TypeScript layer implements what witness functions declare in Compact.

### Circuit Context

```typescript
interface CircuitContext {
  contractAddress: string;
  networkId: string;
  wallet: WalletFacade;
  provider: Provider;
  call<Args extends any[], Return>(
    circuitName: string,
    args: Args
  ): Promise<TransactionResult>;
}
```

The circuit context provides the runtime environment for contract interaction.

### Type Mappings

| Compact Type | TypeScript Type |
|---|---|
| Boolean | boolean |
| Uint<N> | bigint |
| Field | bigint |
| Bytes<N> | Uint8Array |
| CurvePoint | { x: bigint, y: bigint } |
| Vector<N, T> | T[] |
| Map<K, V> | Map<K, V> |
| Set<T> | Set<T> |
| Struct | Interface with same shape |
| Enum | Union of string literals |

### Runtime Functions

```typescript
// Deploy
const deployed = await wallet.deployContract(
  compiledContract,
  constructorArgs
);

// Call circuit
const result = await deployed.call("circuitName", {
  private: { amount: 100n },
  public: { recipient: address }
});

// Read state
const state = await deployed.readState();
```

## Debugging

### Common Compilation Errors

**Type Mismatch**:
```
Error: Expected type Field, found Uint<32>
```
Fix: Use explicit type conversion or check your type annotations.

**Missing disclose()**:
```
Error: Private value cannot flow into public state
```
Fix: Add `disclose()` wrapper around the value before writing to public state.

**Unbounded Loop**:
```
Error: Loop bound must be known at compile time
```
Fix: Use `map` `fold` or replace with bounded loop using compile-time constants.

### Trace Analysis

**V Stack Traces**:
When a proof verification fails the network returns a VmStack trace. This shows which constraints failed during execution.

**VmResults**:
```
VmResult {
  success: false
  error: "Assertion failed: Insufficient balance"
  trace: [
    { contract: "0x...", circuit: "transfer", line: 42 }
  ]
}
```

### compact-runtime Debugging

**Debug Mode**:
```bash
compactc compile contract.compact --debug
```

Debug mode includes additional assertions and more verbose error messages. Use during development not production.

**Local Devnet Debugging**:
- Run a local devnet for fast iteration
- Inspect transactions in the local block explorer
- Use the testkit for controlled debugging
- Enable verbose logging in the Docker compose setup

### Common Gotchas

**Circuits constrain they do not execute**: This is the most common mental model mistake. You are declaring what valid states look like not writing executable code.

**`export ledger` wrong patterns**: Use individual declarations not block syntax. `Cell<T>` is deprecated.

**`disclose()` is not optional**: Private data must be explicitly disclosed before writing to public state. The compiler enforces this.

**`return` inside `for` loops not allowed**: Use `fold` for accumulation and `map` for transformation.

**Enum access uses `.` not `::`**: `GameState.playing` not `GameState::playing`.

**Witness functions have no body**: They declare the type of available private data. Implementation happens in TypeScript.

## Testing

### Unit Tests with Vitest

```typescript
import { describe, it, expect } from 'vitest';
import { createTestEnvironment } from '@midnight-ntwrk/testkit-js';

describe('Counter Contract', () => {
  it('should increment counter', async () => {
    const env = await createTestEnvironment();
    const wallet = await env.createWallet();
    const contract = await wallet.deployContract(counterContract);
    await contract.call('increment');
    const state = await contract.readState();
    expect(state.counter).toBe(1n);
  });
});
```

### Integration Tests

```typescript
describe('Token Transfer Integration', () => {
  it('should transfer tokens between two users', async () => {
    const env = await createTestEnvironment();
    const alice = await env.createWallet();
    const bob = await env.createWallet();
    const token = await alice.deployContract(tokenContract, {
      initialSupply: 1000n
    });
    await token.call('transfer', {
      private: { amount: 100n },
      public: { recipient: bob.address }
    });
    const aliceBalance = await token.call('balanceOf', {
      public: { owner: alice.address }
    });
    const bobBalance = await token.call('balanceOf', {
      public: { owner: bob.address }
    });
    expect(aliceBalance).toBe(900n);
    expect(bobBalance).toBe(100n);
  });
});
```

### Testkit-JS Patterns

**FluentWalletBuilder**:
```typescript
const wallet = await FluentWalletBuilder
  .create(provider)
  .withSeed("test seed phrase")
  .withBalance(1000n) // DUST
  .build();
```

**Test Environment**:
```typescript
const env = await createTestEnvironment({
  network: 'local',
  contracts: [counterContract, tokenContract],
  accounts: 3  // Pre-fund 3 test wallets
});
```

### Testing Private State

Testing private state requires special handling since private state is never directly observable.

**Testing Strategies**:
- Test public state transitions
- Test that proofs verify correctly
- Test that invalid proofs are rejected
- Test edge cases through public state changes
- Use snapshots for verifier key compatibility

## Contract Deployment

### Network Environments

**Local Devnet**:
```typescript
const provider = await createLocalDevnetProvider();
```

**Preprod Testnet**:
```typescript
const provider = await createPreprodProvider();
```

**Mainnet**:
```typescript
const provider = await createMainnetProvider();
```

### deployContract

```typescript
const deployed = await wallet.deployContract(
  compiledContract,
  constructorArgs,
  { network: 'preprod' }
);
```

Returns a deployed contract instance with `call` and `readState` methods.

### findDeployedContract

```typescript
const contract = await wallet.findDeployedContract(
  contractAddress,
  contractAbi
);
```

Reconnect to an already deployed contract using its address and ABI.

### Verifier Key Insertion

```typescript
await wallet.insertVerifierKey(
  contractAddress,
  verifierKey,
  { fee: 1000n }
);
```

After deployment the verifier key must be inserted for proof verification. This is a separate transaction from deployment.

### Deployment Checklist

1. Compile contract with `compactc compile`
2. Verify the compilation output artifacts
3. Generate DUST for deployment fees
4. Deploy contract using `deployContract`
5. Insert verifier key using `insertVerifierKey`
6. Verify contract state is accessible via indexer
7. Test with sample transactions
8. Monitor for any issues

## Version Compatibility

### Compiler Versions

**Version Pragma**:
```compact
pragma language_version >= 0.20;
pragma language_version = 0.22;
```

Always specify version requirements. This prevents unexpected compilation changes.

### Runtime Versions

Contracts compiled for one runtime version may not work on another. Always verify compatibility before deploying to a new network version.

### Network Compatibility Matrix

| Component | Local Devnet | Preprod | Mainnet |
|---|---|---|---|
| compactc 0.20.x | Yes | Yes | Limited |
| compactc 0.22.x | Yes | Yes | Yes |
| compactc 0.23.x | Yes | Testing | No |

Check the latest network status documentation for current compatibility.

## Best Practices

### Gas Optimization

**Minimize Circuit Size**:
- Smaller circuits mean faster proofs
- Avoid unnecessary state reads
- Batch operations where possible
- Use Poseidon hash for ZK-friendly hashing
- Prefer `Counter` over `Uint` for monotonic operations

**State Access Patterns**:
- Read state once and reuse
- Avoid reading entire structs when only one field is needed
- Use Merkle trees for membership proofs instead of linear scans

### Privacy Hygiene

**Disclose at the Last Moment**:
```compact
const result = compute(privateData, publicContext);
registry.insert(key, disclose(result));
```

Not:
```compact
const disclosed = disclose(privateData);
const result = compute(disclosed, publicContext);
registry.insert(key, result);
```

**Minimize Public Data**:
- Only disclose what is absolutely necessary
- Use Merkle roots instead of full data
- Aggregate data before disclosure
- Consider whether an indexer can serve the data instead

### State Management

**Designing Efficient State**:
- Use the right ledger type for each data structure
- Counter for monotonic values
- StateMap for mutable key-value data
- StateBoundedMerkleTree for membership proofs
- Keep state minimal. Indexers handle metadata.

**Don't store metadata on-chain**: Names descriptions image URLs and categories belong in an indexer. Not ledger state.

**Don't compute rewards on-chain**: Off-chain computation plus Merkle root is the correct pattern for reward distribution.

### Error Handling

**Assert Early and Often**:
```compact
export circuit transfer(private amount: Uint<64>): [] {
  assert(amount > 0, "Amount must be positive");
  assert(amount <= balance, "Insufficient balance");
  assert(isActive, "Contract is paused");
  // Now safe to proceed
}
```

Catch invalid states before they reach the main logic. This prevents proof generation failures and reduces debugging time.

### Code Organization

**Module Structure**:
```
contracts/
  types.compact       // Shared type definitions
  utils.compact       // Utility functions
  token.compact       // Token contract
  governance.compact  // Governance contract
```

**Naming Conventions**:
- Circuit functions: verb_noun (transfer create_bid)
- Witness functions: get_descriptive_name
- Ledger fields: snake_case
- Struct types: PascalCase
- Enum types: PascalCase
- Enum variants: snake_case

### Documentation

**Contract Documentation**:
```compact
/// @title Private Token
/// @notice Implements a privacy-preserving token with shielded transfers
/// @dev Uses Zswap protocol for private transactions
contract PrivateToken {
  /// Total supply of the token
  export ledger totalSupply: Uint<64>;

  /// User balances (private by default)
  export ledger balances: StateMap<Bytes<32>, Uint<64>>;
}
```

Document what each circuit does. Document what is public versus private. Document the privacy guarantees.

## Community Gotchas

Distilled from the Midnight Aliit Fellowship community and developer ecosystem.

### Mental Model Mistakes

**Circuits are not functions**: The number one mistake. You are declaring constraints not writing executable code. Debug by asking "which constraint is unsatisfied" not "which line failed".

### Syntax Mistakes

**`export ledger` use individual declarations not block syntax**: Block syntax was removed. Use `export ledger field: Type;` for each field.

**`Cell<T>` is deprecated**: Use direct type declarations instead. `export ledger value: Field;` not `export ledger value: Cell<Field>;`.

**Enum access uses `.` not `::`**: `GameState.playing` is correct. `GameState::playing` is a compile error.

**Witness functions have no body**: They are declarations only. Implementation is in TypeScript.

### State Management Mistakes

**Reading entire structs when only one field needed**: `bets.lookup(userPk)` pulls every field into the circuit. Structure your data to minimize reads.

**Storing metadata on-chain**: Names descriptions URLs belong in an indexer. Ledger state is for cryptographic commitments and essential state.

**Computing rewards on-chain**: Use off-chain computation with Merkle root verification instead.

### Privacy Mistakes

**Forgetting `disclose()`**: The compiler catches this but understanding why it is needed prevents design mistakes. Private data cannot accidentally flow into public state.

**Disclosing too early**: Disclose at the last possible moment before the public state write. Early disclosure expands the attack surface.

**Not using domain separation**: Without domain separation proofs may be valid across contracts. Always include contract address and chain ID in signatures.

### Deployment Mistakes

**Forgetting verifier key insertion**: Deploying the contract is not enough. The verifier key must be inserted for proof verification to work. This is a separate step.

**Not testing on preprod before mainnet**: Preprod is the staging environment. Test there before deploying to mainnet to catch environment-specific issues.

**Assuming DUST is always available**: DUST generation takes time. Pre-fund test wallets with DUST. In production ensure users have sufficient NIGHT to generate DUST.

---
name: midnight-compact
description: Comprehensive guide to the Compact programming language (v0.22+) for writing privacy-preserving smart contracts on Midnight Network. Use when users need to write Compact smart contracts with zero-knowledge proofs, understand Compact syntax and language features, implement ZK circuit patterns and optimizations, generate contract boilerplate and project scaffolding, learn best practices for secure contract development, access Compact standard library functions, and compile and test Compact contracts.
---

# Midnight Compact Language (v0.22+)

Complete guide to writing privacy-preserving smart contracts with Compact.

## What is Compact?

Compact is a purpose-built programming language for zero-knowledge smart contracts. Unlike adapting existing languages, Compact was designed from scratch to make privacy-preserving programming natural and secure.

**Key Design Goals**:
- Compile directly to efficient ZK circuits
- Type-safe cryptographic operations
- Familiar syntax for developers (TypeScript-like)
- Automatic proof generation
- Bounded for finite proving circuits

**Key Features**:
- Strong static typing (no bypass via unsafe casts)
- Generic type and numeric parameters
- Explicit disclosure via `disclose()` wrappers
- Module-based namespace management

## Quick Start

### Minimal Working Contract (v0.22+)
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

// Ledger state (individual declarations)
export ledger counter: Counter;
export ledger owner: Bytes<32>;

// Witness for private data
witness local_secret_key(): Bytes<32>;

// Circuit (returns [] not Void)
export circuit increment(): [] {
  counter.increment(1);
}
```

### Full Counter with Read/Write
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger count: Counter;

export circuit increment(): [] {
  count.increment(1);
}

export circuit decrement(): [] {
  count.decrement(1);
}

export circuit getCount(): Uint<64> {
  return count.read();
}

export circuit setCount(newValue: Uint<64>): [] {
  count.write(newValue);
}
```

## Core Concepts

### Three-Part Contract Structure

Each Compact contract has three components:
1. **Replicated component** on a public ledger
2. **Zero-knowledge circuit** that confidentially proves correct execution
3. **Local, off-chain component** for arbitrary code

### Program Elements

A Compact program can contain:
- `module` / `import` for namespace management
- `struct` / `enum` / `type` for program-defined types
- `export ledger` for public state storage
- `witness` for callback functions (private state)
- `circuit` for the operational core
- `constructor` for initialization

## Comprehensive Syntax Reference

### ✅ CORRECT vs ❌ WRONG Examples

**Pragma**:
```compact
✅ pragma language_version >= 0.20;
❌ pragma language_version >= 0.16.0;  // Outdated version
❌ pragma version "0.20";  // Wrong format
```

**Ledger Declarations**:
```compact
✅ export ledger counter: Counter;
✅ export ledger owner: Bytes<32>;
✅ export ledger balances: Map<Address, Uint<64>>;
❌ ledger { counter: Counter; }  // Block syntax deprecated
❌ ledger counter = Counter;  // Missing colon
```

**Circuit Return Types**:
```compact
✅ export circuit increment(): [] { }
✅ export circuit getBalance(): Uint<64> { return 0; }
✅ export circuit getData(): [Uint<32>, Boolean] { return [0, true]; }
❌ export circuit increment(): Void { }  // Void doesn't exist
❌ export circuit noReturn() { }  // Missing return type
```

**Enum Access**:
```compact
✅ if (choice == Choice.rock) { }
❌ if (choice == Choice::rock) { }  // Rust-style doesn't work
❌ if (choice == "rock") { }  // String not enum variant
```

**Witness Declarations**:
```compact
✅ witness local_secret_key(): Bytes<32>;
✅ witness verify_signature(msg: Bytes<32>, sig: Bytes<64>): Boolean;
❌ witness get_key(): Bytes<32> { return ...; }  // No body allowed
❌ witness calculate(): Uint<64> = 42;  // No body or default
```

**Counter Operations**:
```compact
✅ const val = counter.read();
✅ counter.increment(1);
✅ counter.decrement(1);
✅ counter.write(100);
❌ const val = counter.value();  // Method doesn't exist
❌ counter.add(1);  // Wrong method name
```

**Pure Functions**:
```compact
✅ pure circuit helper(x: Field): Field { return x + 1; }
✅ circuit helper(x: Field): Field { return x + 1; }
❌ pure function helper(x: Field): Field { ... }  // 'function' keyword doesn't exist
❌ pure fn helper(x: Field): Field { ... }  // 'fn' keyword doesn't exist
```

**Disclosure in Conditionals**:
```compact
✅ if (disclose(witness_val == x)) { ... }
❌ if (witness_val == x) { ... }  // Implicit disclosure error
❌ disclose(witness_val == x);  // Statement form without if
```

**Vector/Tuple Operations**:
```compact
✅ const first = vec[0];
✅ const len = vec.len();
✅ const [a, b] = tuple;
✅ for (i: Uint<64>, item: vec) { ... }
❌ const last = vec[-1];  // No negative indexing
❌ vec.push(item);  // No push - vectors are immutable
```

### Common Mistakes to Avoid

| ❌ Wrong | ✅ Correct | Explanation |
|---------|-----------|-------------|
| `ledger { field: Type; }` | `export ledger field: Type;` | Individual declarations |
| `circuit fn(): Void` | `circuit fn(): []` | Empty return uses [] |
| `enum State { ... }` | `export enum State { ... }` | Enums need export |
| `counter.value()` | `counter.read()` | Use read() method |
| `Choice::rock` | `Choice.rock` | Dot, not :: |
| `Cell<T>` | `Field` | Cell type deprecated |
| `Vector.push(x)` | Create new vector | Vectors immutable |
| `disclose(a == b)` alone | `if (disclose(a == b))` | Needs conditional |
| `Uint` without size | `Uint<64>` | Size required |
| `Fn` or `function` | `circuit` | Use circuit keyword |

## Type System

### Primitive Types

| Type | Description | Example Values |
|------|-------------|---------------|
| `Boolean` | Boolean values | `true`, `false` |
| `Field` | Prime field integers | `0` to field max |
| `Uint<N>` | N-bit unsigned | `Uint<8>`, `Uint<32>`, `Uint<64>` |
| `Uint<M..N>` | Bounded unsigned | `Uint<0..100>` |
| `Bytes<N>` | N-byte vector | `Bytes<32>` for hashes |
| `Vector<N, T>` | N-element homogeneous | `Vector<10, Uint<32>>` |
| `[T1, T2, ...]` | Heterogeneous tuple | `[Uint<32>, Boolean]` |
| `Opaque<"string">` | Opaque string | Debug strings |
| `Opaque<"Uint8Array">` | Opaque bytes | Binary data |

### User-Defined Types

**Struct**:
```compact
struct Point {
  x: Field,
  y: Field,
}

struct Token<T> {
  amount: Uint<64>,
  data: T,
}
```

**Enum**:
```compact
export enum Direction { up, down, left, right }
export enum Status { pending, active, completed }
```

**Type Alias**:
```compact
type Address = Bytes<32>;
new type UserId = Uint<64>;  // Nominal (distinct)
type Vec3<T> = Vector<3, T>;  // Generic
```

### Subtyping Rules

- `Uint<0..N>` subtype of `Uint<0..M>` if N ≤ M
- `Uint<0..N>` subtype of `Field` if N ≤ field max
- Tuple subtypes when elements are subtypes

### Generic Parameters

```compact
module M<T, #N> {
  export circuit foo<A>(x: T, v: Vector<N, A>): Vector<N, [A, T]> {
    return map((y) => [y, x], v);
  }
}
import M<Boolean, 3>;

export circuit bar(): Vector<3, [Uint<8>, Boolean]> {
  return foo<Uint<8>>(true, [101, 103, 107]);
}
```

## Ledger State Types

Seven ledger state types for public data storage:

### 1. Counter
```compact
export ledger myCounter: Counter;
counter.increment(n);
counter.decrement(n);
counter.read();
counter.write(value);
```

### 2. Cell (Deprecated - use Field)
```compact
// Old way (avoid)
export ledger data: Cell<Uint<32>>;
// New way
export ledger data: Field;
```

### 3. Set
```compact
export ledger members: Set<Address>;
members.insert(addr);
members.contains(addr);
members.remove(addr);
```

### 4. Map
```compact
export ledger balances: Map<Address, Uint<64>>;
balances.get(addr);
balances.set(addr, value);
balances.contains(addr);
balances.remove(addr);
```

### 5. List
```compact
export ledger items: List<Uint<32>>;
items.push(value);
items.get(index);
items.len();
```

### 6. MerkleTree
```compact
export ledger tree: MerkleTree<Depth>;
tree.insert(value);
tree.getRoot();
tree.getPath(index);
tree.verifyPath(path, root);
```

### 7. HistoricMerkleTree
```compact
export ledger history: HistoricMerkleTree<Depth>;
history.insert(value);
history.getRoot();
history.getHistoricRoot(blockHeight);
history.getPath(index);
```

## Standard Library

### Data Types
```compact
Maybe<T>           // Optional values (some/none)
Either<L, R>       // Result types (left/right)
NativePoint        // BLS12-381 points
MerkleTreeDigest  // Tree hash digest
MerkleTreePath    // Proof path
ContractAddress   // Contract addressing
ZswapCoinPublicKey  // Shielded keys
UserAddress       // User addressing
```

### Coin Management (Zswap)
```compact
tokenType() -> TokenType
nativeToken() -> TokenType
ownPublicKey() -> CoinPublicKey

createZswapInput(coin: ShieldedCoinInfo) -> ZswapInput
createZswapOutput(recipient: Recipient, amount: Uint<64>) -> ZswapOutput

mintShieldedToken(amount: Uint<64>, recipient: Recipient): [] { }
sendShielded(amount: Uint<64>, recipient: Recipient): [] { }
receiveShielded(input: ZswapInput): [] { }

mintUnshieldedToken(amount: Uint<64>): [] { }
sendUnshielded(amount: Uint<64>, recipient: Address): [] { }
unshieldedBalance(): Uint<64>
```

### Hashing Functions
```compact
transientHash(data: Field): Field
transientCommit(data: Field, randomness: Field): Field
persistentHash(key: Field, value: Field): Field
persistentCommit(key: Field, value: Field): Field
degradeToTransient(value: Field): Field
```

### Elliptic Curve
```compact
ecAdd(p1: Point, p2: Point): Point
ecMul(point: Point, scalar: Field): Point
ecMulGenerator(scalar: Field): Point
hashToCurve(data: Field): Point
upgradeFromTransient(value: Field): Field
```

### Merkle Trees
```compact
merkleTreePathRoot(path: MerkleTreePath): Field
merkleTreePathRootNoLeafHash(path: MerkleTreePath): Field
```

### Block Time
```compact
blockTimeLt(time: Uint<64>): Boolean
blockTimeGte(time: Uint<64>): Boolean
blockTimeGt(time: Uint<64>): Boolean
blockTimeLte(time: Uint<64>): Boolean
```

## Control Flow

### If/Else
```compact
if (condition) {
  // then branch
} else {
  // else branch
}
```

### For Loop
```compact
// For each element
for (i: Uint<64>, item: vector) {
  process(item);
}

// With index
for (i: Uint<64>, item: vector) {
  log(i);
  log(item);
}
```

### Match (for enums)
```compact
match direction {
  Direction.up => 1,
  Direction.down => 2,
  Direction.left => 3,
  Direction.right => 4,
}
```

### Pure Circuit Functions
```compact
pure circuit addOne(x: Uint<32>): Uint<32> {
  return x + 1;
}
```

## Explicit Disclosure

Private data must be explicitly disclosed:

```compact
witness secret(): Uint<32>;

export circuit checkEqual(x: Uint<32>): Boolean {
  // Must disclose private comparison
  return disclose(secret() == x);
}

// Valid patterns:
if (disclose(secret() > 100)) { ... }
const revealed = disclose(secret() + publicValue);
```

## Development Workflow

### 1. Initialize Project
```bash
# Using official CLI
npx create-midnight-app my-project
cd my-project

# Or manual setup
mkdir my-contract && cd my-contract
npm init -y
npm install @midnight-ntwrk/compact-tools
```

### 2. Write Contract
Create `contract.compact`:
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger counter: Counter;

export circuit increment(): [] {
  counter.increment(1);
}

export circuit getCount(): Uint<64> {
  return counter.read();
}
```

### 3. Compile
```bash
npx compact build contract.compact
```

### 4. Generate TypeScript
```bash
# Output in src/ directory
```

### 5. Deploy
```bash
# Using deployment script
npx midnight-deploy --network testnet
```

## Real-World Contract Examples

### Private Token (Zswap)
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger totalSupply: Uint<64>;
export ledger balances: Map<Address, Uint<64>>;

export circuit mint(to: Address, amount: Uint<64>): [] {
  const current = balances.getOrDefault(to, 0);
  balances.set(to, current + amount);
  totalSupply.set(totalSupply.read() + amount);
}

export circuit burn(from: Address, amount: Uint<64>): [] {
  const current = balances.getOrDefault(from, 0);
  assert(current >= amount, "Insufficient balance");
  balances.set(from, current - amount);
  totalSupply.set(totalSupply.read() - amount);
}

export circuit transfer(from: Address, to: Address, amount: Uint<64>): [] {
  const fromBal = balances.getOrDefault(from, 0);
  assert(fromBal >= amount, "Insufficient balance");
  const toBal = balances.getOrDefault(to, 0);
  balances.set(from, fromBal - amount);
  balances.set(to, toBal + amount);
}

export circuit balanceOf(owner: Address): Uint<64> {
  return balances.getOrDefault(owner, 0);
}
```

### Private Voting
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger votes: Map<Bytes<32>, Uint<64>>;
export ledger voted: Set<Address>;

export circuit castVote(voter: Address, candidate: Bytes<32>): [] {
  assert(!voted.contains(voter), "Already voted");
  voted.insert(voter);
  const current = votes.getOrDefault(candidate, 0);
  votes.set(candidate, current + 1);
}

export circuit getVoteCount(candidate: Bytes<32>): Uint<64> {
  return votes.getOrDefault(candidate, 0);
}
```

### Access Control
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger owner: Address;
export ledger admins: Set<Address>;

export circuit onlyOwner(): [] {
  assert(msgSender() == owner, "Not owner");
}

export circuit onlyOwnerOrAdmin(): [] {
  const sender = msgSender();
  assert(sender == owner || admins.contains(sender), "Not authorized");
}

witness msgSender(): Address;
// Note: msgSender is typically provided by runtime
```

## OpenZeppelin Contracts

Standard implementations from [@OpenZeppelin/compact-contracts](https://github.com/OpenZeppelin/compact-contracts):

- **FungibleToken**: ERC-20 equivalent
- **MultiToken**: ERC-1155 equivalent (fungible + NFT)
- **NonFungibleToken**: NFT implementation

```compact
// Using OpenZeppelin
import OpenZeppelin.FungibleToken;

export ledger token: FungibleToken;

export circuit mint(to: Address, amount: Uint<64>): [] {
  token.mint(to, amount);
}

export circuit transfer(to: Address, amount: Uint<64>): [] {
  token.transfer(to, amount);
}
```

## Awesome Midnight DApps Reference

Real-world implementations for learning:

### Getting Started (Official)
- [Example Counter](https://github.com/midnightntwrk/example-counter)
- [Example Bboard](https://github.com/midnightntwrk/example-bboard)
- [Example ZK Loan](https://github.com/midnightntwrk/example-zkloan)
- [Midnight Kitties NFT](https://github.com/midnightntwrk/example-kitties)

### Finance & DeFi
- [LunarSwap](https://github.com/OpenZeppelin/midnight-apps) - UTXO-based DEX
- [Hydra Stake](https://github.com/statera-protocol/hydra-stake-protocol) - Liquid staking
- [Statera Protocol](https://github.com/statera-protocol/statera-protocol-midnight) - Stablecoin

### Identity & Privacy
- [Midnames](https://github.com/midnames/core) - ZK DID
- [Midnight Cloak](https://github.com/subc0der/midnight-cloak) - ZK verification SDK
- [KYC Midnight](https://github.com/joacolinares/kyc-midnight) - KYC attestations

### Gaming
- [Midnight Starship](https://github.com/nel349/midnight-starship) - Space shooter
- [Midnight Seabattle](https://github.com/bricktowers/midnight-seabattle) - Sea battle

### Developer Tools
- [midnight-wallet-cli](https://github.com/nel349/midnight-wallet-cli-hub)
- [Create Midnight App](https://github.com/midnightntwrk/create-mn-app)
- [Midnight Local Dev](https://github.com/midnightntwrk/midnight-local-dev)
- [Compact Playground](https://github.com/Olanetsoft/compact-playground)
- [VS Code Extension](https://github.com/foxytanuki/compact-vscode)

## Midnight MCP: AI-Assisted Development

Midnight MCP is an **MCP server** (Model Context Protocol) purpose-built for Midnight development. It gives AI assistants real compiler validation and semantic search across 102 Midnight repositories.

### Why Use MCP?

AI assistants hallucinate Compact syntax. Without MCP:
- They invent `Int` instead of `Uint<32>`
- They use `Void` instead of `[]` for empty returns
- They use `state` instead of `ledger`

With MCP, AI generates **verified working code**.

### Installation

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "midnight": {
      "command": "npx",
      "args": ["-y", "midnight-mcp@latest"]
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "midnight": {
      "command": "npx",
      "args": ["-y", "midnight-mcp@latest"]
    }
  }
}
```

### 29 Available Tools

| Category | Tools |
|----------|-------|
| **Search** | `midnight-search-compact`, `midnight-search-docs`, `midnight-search-typescript`, `midnight-fetch-docs` |
| **Validation** | `midnight-compile-contract`, `midnight-analyze-contract` |
| **Analysis** | `midnight-review-contract`, `midnight-extract-contract-structure` |
| **Generation** | `midnight-generate-contract`, `midnight-document-contract` |
| **Repository** | `midnight-get-file`, `midnight-get-latest-syntax`, `midnight-list-examples` |
| **Version** | `midnight-check-breaking-changes`, `midnight-get-migration-guide` |

### Version Management

Use exact versions (e.g., `0.30.0`) for reproducibility. Latest versions available on GitHub releases.

## CI/CD Integration

### setup-compact-action

Official GitHub Action for installing and caching the Compact compiler: [midnightntwrk/setup-compact-action](https://github.com/midnightntwrk/setup-compact-action)

**Features**:
- Intelligent caching for fast subsequent runs (~2-5 seconds cached vs ~30-60 seconds fresh)
- Version pinning support (e.g., `0.30.0`) or use `latest`

```yaml
- name: Setup Compact Compiler
  uses: midnightntwrk/setup-compact-action@v1
  with:
    compact-version: '0.30.0'

- name: Compile Compact code
  run: compact compile src/*.compact
```

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `compact-version` | Version of Compact compiler | No | `latest` |
| `cache-enabled` | Enable caching | No | `true` |

Outputs: `compact-version`, `cache-hit`

## Additional Resources

### Official Documentation
- [Compact Language Docs](https://docs.midnight.network/compact)
- [Standard Library API](https://docs.midnight.network/compact/standard-library)
- [Language Grammar](https://docs.midnight.network/compact/reference/compact-grammar)
- [Writing Contracts](https://docs.midnight.network/compact/reference/writing)

### Learning Resources
- [Learn Compact](https://github.com/Olanetsoft/learn-compact) - Interactive book
- [Compact By Example](https://github.com/Olanetsoft/compact-by-example)
- [Midnight MCP](https://github.com/Olanetsoft/midnight-mcp) - AI assistant integration

### Troubleshooting
- Compilation errors: Check language version pragma
- Type errors: Verify type annotations
- Disclosure errors: Use `disclose()` in conditionals
- Ledger errors: Import CompactStandardLibrary
# TypeScript Interop Guide

## Overview

How Compact types map to TypeScript and how to work with generated code.

## Type Mappings

### Primitive Types

| Compact Type | TypeScript Type | Example |
|--------------|-----------------|---------|
| `Boolean` | `boolean` | `true`, `false` |
| `Field` | `bigint` | `42n` |
| `Uint<8>` | `number` | `255` |
| `Uint<16>` | `number` | `65535` |
| `Uint<32>` | `number` | `4294967295` |
| `Uint<64>` | `bigint` | `18446744073709551615n` |
| `Uint<128>` | `bigint` | Large numbers |
| `Uint<256>` | `bigint` | Very large numbers |
| `Bytes<N>` | `Uint8Array` | `new Uint8Array(32)` |
| `Opaque<"string">` | `string` | `"hello"` |

### Collection Types

| Compact Type | TypeScript Type |
|--------------|-----------------|
| `Vector<N, T>` | `T[]` (fixed length N) |
| `List<T>` | `T[]` (dynamic) |
| `Maybe<T>` | `T \| null` |
| `Either<L, R>` | `{ left: L } \| { right: R }` |

### User-Defined Types

**Compact enum**:
```compact
export enum GameState {
  waiting,
  playing,
  finished
}
```

**TypeScript**:
```typescript
enum GameState {
  waiting = 'waiting',
  playing = 'playing',
  finished = 'finished'
}

// Usage
const state: GameState = GameState.playing;
```

**Compact struct**:
```compact
export struct Player {
  name: Opaque<"string">,
  score: Uint<32>,
  isActive: Boolean
}
```

**TypeScript**:
```typescript
interface Player {
  name: string;
  score: number;
  isActive: boolean;
}

// Usage
const player: Player = {
  name: "Alice",
  score: 100,
  isActive: true
};
```

## Generated Contract Interface

### Contract Class

**Compact**:
```compact
export ledger counter: Counter;
export circuit increment(amount: Uint<16>): []
export circuit getCount(): Uint<64>
```

**Generated TypeScript**:
```typescript
export class Contract {
  constructor(witnesses: Witnesses);
  
  initialState(params: {}): [PrivateState, PublicState];
  
  circuits: {
    increment(
      context: CircuitContext<PrivateState>,
      amount: number
    ): Promise<CircuitResults<PrivateState, void>>;
    
    getCount(
      context: CircuitContext<PrivateState>
    ): Promise<CircuitResults<PrivateState, bigint>>;
  };
}
```

### State Types

**Public State** (ledger):
```typescript
interface PublicState {
  counter: bigint;  // Counter type → bigint
}
```

**Private State** (local):
```typescript
interface PrivateState {
  // Your private fields
}
```

### Circuit Context

```typescript
interface CircuitContext<T> {
  privateState: T;
  ledgerState: PublicState;
}
```

### Circuit Results

```typescript
interface CircuitResults<T, R> {
  privateState: T;      // Updated private state
  publicState: PublicState;  // Updated public state
  result: R;            // Return value
}
```

## Working with Generated Code

### Import Generated Types

```typescript
import {
  Contract,
  Witnesses,
  PublicState,
  PrivateState,
  GameState,  // Your enums
  Player      // Your structs
} from './build/contract';
```

### Implement Witnesses

**Compact**:
```compact
witness local_secret_key(): Bytes<32>;
witness get_player_data(id: Uint<32>): Player;
```

**TypeScript**:
```typescript
const witnesses: Witnesses<PrivateState> = {
  local_secret_key: (): Uint8Array => {
    return secretKeyBytes;
  },
  
  get_player_data: (id: number): Player => {
    return {
      name: "Alice",
      score: 100,
      isActive: true
    };
  }
};
```

### Call Circuits

```typescript
const contract = new Contract(witnesses);

// Initialize
const [privateState, publicState] = contract.initialState({});

// Call circuit
const result = await contract.circuits.increment(
  { privateState, ledgerState: publicState },
  5  // amount: Uint<16> → number
);

// Access results
console.log('New counter:', result.publicState.counter);  // bigint
console.log('Private state:', result.privateState);
```

### Handle Return Values

**Void return** (`[]`):
```typescript
// Compact: circuit increment(): []
const result = await contract.circuits.increment(context, 5);
// result.result is void
```

**Value return**:
```typescript
// Compact: circuit getCount(): Uint<64>
const result = await contract.circuits.getCount(context);
console.log(result.result);  // bigint
```

**Struct return**:
```typescript
// Compact: circuit getPlayer(): Player
const result = await contract.circuits.getPlayer(context);
const player: Player = result.result;
console.log(player.name);  // string
```

## Type Conversions

### Compact → TypeScript

```typescript
// Field → bigint
const fieldValue: bigint = 42n;

// Uint<32> → number
const uint32Value: number = 100;

// Uint<64> → bigint
const uint64Value: bigint = 1000n;

// Bytes<32> → Uint8Array
const bytes32: Uint8Array = new Uint8Array(32);

// Opaque<"string"> → string
const opaqueString: string = "hello";
```

### TypeScript → Compact

When calling circuits, TypeScript values are automatically converted:

```typescript
// number → Uint<32>
await contract.circuits.setScore(context, 100);

// bigint → Uint<64>
await contract.circuits.setBalance(context, 1000n);

// string → Opaque<"string">
await contract.circuits.setName(context, "Alice");

// Uint8Array → Bytes<32>
await contract.circuits.setHash(context, hashBytes);
```

## Working with Enums

**Compact**:
```compact
export enum GameState { waiting, playing, finished }

export circuit setState(state: GameState): [] {
  gameState = state;
}
```

**TypeScript**:
```typescript
import { GameState } from './build/contract';

// Set state
await contract.circuits.setState(
  context,
  GameState.playing  // Use enum value
);

// Check state
if (publicState.gameState === GameState.playing) {
  console.log('Game is active');
}
```

## Working with Structs

**Compact**:
```compact
export struct Player {
  name: Opaque<"string">,
  score: Uint<32>
}

export circuit updatePlayer(player: Player): [] {
  currentPlayer = player;
}
```

**TypeScript**:
```typescript
import { Player } from './build/contract';

const player: Player = {
  name: "Alice",
  score: 100
};

await contract.circuits.updatePlayer(context, player);
```

## Working with Collections

### Vector (Fixed Size)

**Compact**: `Vector<3, Uint<32>>`  
**TypeScript**: `number[]` (length 3)

```typescript
const scores: number[] = [10, 20, 30];
await contract.circuits.setScores(context, scores);
```

### List (Dynamic)

**Compact**: `List<Uint<32>>`  
**TypeScript**: `number[]`

```typescript
const items: number[] = [1, 2, 3, 4, 5];
await contract.circuits.addItems(context, items);
```

### Maybe (Optional)

**Compact**: `Maybe<Uint<32>>`  
**TypeScript**: `number | null`

```typescript
// Some value
await contract.circuits.setValue(context, 42);

// No value
await contract.circuits.setValue(context, null);
```

### Either (Union)

**Compact**: `Either<String, Uint<32>>`  
**TypeScript**: `{ left: string } | { right: number }`

```typescript
// Left variant
await contract.circuits.setResult(context, { left: "error" });

// Right variant
await contract.circuits.setResult(context, { right: 42 });
```

## Complete Example

**Compact contract**:
```compact
pragma language_version >= 0.19;
import CompactStandardLibrary;

export enum Status { pending, active, completed }

export struct Task {
  title: Opaque<"string">,
  priority: Uint<8>,
  status: Status
}

export ledger tasks: List<Task>;

export circuit addTask(task: Task): [] {
  tasks.push(task);
}

export circuit getTasks(): List<Task> {
  return tasks;
}
```

**TypeScript usage**:
```typescript
import { Contract, Task, Status } from './build/contract';

const contract = new Contract({});
const [privateState, publicState] = contract.initialState({});

// Create task
const task: Task = {
  title: "Build DApp",
  priority: 1,
  status: Status.pending
};

// Add task
const result = await contract.circuits.addTask(
  { privateState, ledgerState: publicState },
  task
);

// Get tasks
const tasksResult = await contract.circuits.getTasks(
  { privateState: result.privateState, ledgerState: result.publicState }
);

const tasks: Task[] = tasksResult.result;
console.log('Tasks:', tasks);
// [{ title: "Build DApp", priority: 1, status: "pending" }]
```

## Best Practices

### 1. Use Generated Types

```typescript
// ✅ CORRECT - use generated types
import { Player } from './build/contract';
const player: Player = { name: "Alice", score: 100 };

// ❌ WRONG - manual types
const player = { name: "Alice", score: 100 };
```

### 2. Handle BigInt Correctly

```typescript
// ✅ CORRECT - use bigint for large numbers
const balance: bigint = 1000n;

// ❌ WRONG - number overflow
const balance: number = 18446744073709551615;  // Loses precision
```

### 3. Validate Enum Values

```typescript
// ✅ CORRECT - use enum
if (state === GameState.playing) { ... }

// ❌ WRONG - string comparison
if (state === "playing") { ... }
```

### 4. Type Circuit Parameters

```typescript
// ✅ CORRECT - typed parameters
async function increment(amount: number) {
  await contract.circuits.increment(context, amount);
}

// ❌ WRONG - untyped
async function increment(amount) {
  await contract.circuits.increment(context, amount);
}
```

## Resources

- **Type System**: See type-system.md
- **Contract Examples**: See contract-examples.md
- **API Integration**: See compact-runtime-api.md (midnight-api)

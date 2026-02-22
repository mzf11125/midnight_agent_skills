# Compact Runtime API Reference

**Package**: `@midnight-ntwrk/compact-runtime v0.14.0`

## Overview

The Compact Runtime API provides runtime primitives used by Compact's TypeScript output. It includes built-in functions for hashing, cryptography, state management, and circuit execution.

## Installation

```bash
yarn add @midnight-ntwrk/compact-runtime
```

## Network Configuration

**CRITICAL**: Must be called before any operations.

```typescript
import { setNetworkId, NetworkId } from '@midnight-ntwrk/compact-runtime';

// Set network ID first
setNetworkId(NetworkId.TestNet);

// Now safe to use runtime functions
```

## Core Interfaces

### CircuitContext<T>

Context passed to impure circuits.

```typescript
interface CircuitContext<T> {
  privateState: T;           // Private state type
  ledgerState: LedgerState;  // Access to public ledger
  // Additional context for circuit execution
}
```

**Usage in generated code:**
```typescript
// Generated circuit signature
function myCircuit(
  context: CircuitContext<MyPrivateState>,
  param1: bigint,
  param2: boolean
): CircuitResults<MyPrivateState, ReturnType>
```

### CircuitResults<T, R>

Wrapped circuit return values.

```typescript
interface CircuitResults<T, R> {
  privateState: T;  // Updated private state
  result: R;        // Circuit return value
  // Additional execution results
}
```

**Purpose**: Ensures functional purity - circuits don't have hidden side effects.

### WitnessContext<Ledger, T>

Context passed to witnesses.

```typescript
interface WitnessContext<Ledger, T> {
  ledger: Ledger;      // Read-only ledger view
  privateState: T;     // Current private state
}
```

**Witness signature:**
```typescript
function myWitness(
  context: WitnessContext<MyLedger, MyPrivateState>,
  param: bigint
): [MyPrivateState, ReturnType]  // Returns [newState, result]
```

## Built-in Functions

### Hashing Functions

#### transientHash<T>(value: T): Field

Hash for non-persistent data.

```typescript
import { transientHash } from '@midnight-ntwrk/compact-runtime';

const hash = transientHash({ x: 42, y: true });
// Returns: Field element
```

**Use when**: Data is not kept in contract state.

#### transientCommit<T>(value: T, randomness: Field): Field

Commitment for non-persistent data.

```typescript
import { transientCommit } from '@midnight-ntwrk/compact-runtime';

const commitment = transientCommit(secretValue, randomNonce);
// Returns: Field element
```

**Use when**: Committing to temporary values.

#### persistentHash<T>(value: T): Bytes<32>

Hash for persistent data.

```typescript
import { persistentHash } from '@midnight-ntwrk/compact-runtime';

const hash = persistentHash(userData);
// Returns: Bytes<32>
```

**Use when**: Data is stored in ledger state.

#### persistentCommit<T>(value: T, randomness: Bytes<32>): Bytes<32>

Commitment for persistent data.

```typescript
import { persistentCommit } from '@midnight-ntwrk/compact-runtime';

const commitment = persistentCommit(secretData, randomBytes);
// Returns: Bytes<32>
```

**Use when**: Committing to ledger-stored values.

#### degradeToTransient(persistent: Bytes<32>): Field

Convert persistent hash to transient.

```typescript
import { degradeToTransient } from '@midnight-ntwrk/compact-runtime';

const persistentHash = persistentHash(data);
const transientHash = degradeToTransient(persistentHash);
```

### Elliptic Curve Functions

#### ecAdd(p1: NativePoint, p2: NativePoint): NativePoint

Add two elliptic curve points.

```typescript
import { ecAdd } from '@midnight-ntwrk/compact-runtime';

const sum = ecAdd(point1, point2);
```

#### ecMul(scalar: Field, point: NativePoint): NativePoint

Scalar multiplication of curve point.

```typescript
import { ecMul } from '@midnight-ntwrk/compact-runtime';

const result = ecMul(scalar, point);
```

#### ecMulGenerator(scalar: Field): NativePoint

Multiply generator point by scalar.

```typescript
import { ecMulGenerator } from '@midnight-ntwrk/compact-runtime';

const publicKey = ecMulGenerator(privateKey);
```

#### hashToCurve(data: Bytes<32>): NativePoint

Hash data to curve point.

```typescript
import { hashToCurve } from '@midnight-ntwrk/compact-runtime';

const point = hashToCurve(hashValue);
```

#### upgradeFromTransient(transient: Field): NativePoint

Convert transient hash to curve point.

```typescript
import { upgradeFromTransient } from '@midnight-ntwrk/compact-runtime';

const point = upgradeFromTransient(transientHash);
```

## State Management

### ContractState

Encapsulates on-chain contract state.

```typescript
class ContractState {
  constructor(stateValue: StateValue);
  
  // Get state value
  getValue(): StateValue;
  
  // Update state
  update(newValue: StateValue): ContractState;
}
```

**Usage:**
```typescript
const state = new ContractState(initialValue);
const newState = state.update(updatedValue);
```

### StateValue

Encoding of on-chain data.

```typescript
class StateValue {
  // Encode data for storage
  static encode(data: any): StateValue;
  
  // Decode stored data
  decode(): any;
}
```

### QueryContext

Annotated view for VM program execution.

```typescript
class QueryContext {
  constructor(state: ContractState);
  
  // Execute query against state
  query(program: VMProgram): any;
}
```

## Runtime Type System

### CompactType<T>

Runtime representation of Compact types.

```typescript
interface CompactType<T> {
  // Validate value matches type
  validate(value: unknown): value is T;
  
  // Get default value
  default(): T;
  
  // Serialize/deserialize
  encode(value: T): Uint8Array;
  decode(data: Uint8Array): T;
}
```

### Type Constructors

#### Boolean
```typescript
import { CompactTypeBoolean } from '@midnight-ntwrk/compact-runtime';

const boolType = new CompactTypeBoolean();
const defaultValue = boolType.default();  // false
```

#### Field
```typescript
import { CompactTypeField } from '@midnight-ntwrk/compact-runtime';

const fieldType = new CompactTypeField();
const defaultValue = fieldType.default();  // 0n
```

#### Unsigned Integer
```typescript
import { CompactTypeUnsignedInteger } from '@midnight-ntwrk/compact-runtime';

const uint32Type = new CompactTypeUnsignedInteger(
  4294967295,  // max value (2^32-1)
  4            // byte length
);
```

#### Bytes
```typescript
import { CompactTypeBytes } from '@midnight-ntwrk/compact-runtime';

const bytes32Type = new CompactTypeBytes(32);
const defaultValue = bytes32Type.default();  // 32 zero bytes
```

#### Vector
```typescript
import { CompactTypeVector } from '@midnight-ntwrk/compact-runtime';

const vectorType = new CompactTypeVector(
  5,         // length
  fieldType  // element type
);
```

#### String
```typescript
import { CompactTypeString } from '@midnight-ntwrk/compact-runtime';

const stringType = new CompactTypeString();
```

#### Uint8Array
```typescript
import { CompactTypeUint8Array } from '@midnight-ntwrk/compact-runtime';

const uint8ArrayType = new CompactTypeUint8Array();
```

## Complete Example: Using Runtime Functions

```typescript
import {
  setNetworkId,
  NetworkId,
  persistentHash,
  persistentCommit,
  ecMulGenerator,
  CompactTypeField,
  CompactTypeBytes
} from '@midnight-ntwrk/compact-runtime';

// 1. Set network
setNetworkId(NetworkId.TestNet);

// 2. Create types
const fieldType = new CompactTypeField();
const bytes32Type = new CompactTypeBytes(32);

// 3. Hash data
const userData = { id: 123, active: true };
const userHash = persistentHash(userData);
console.log('User hash:', userHash);

// 4. Create commitment
const secretValue = 42n;
const randomness = bytes32Type.default();  // In real use, generate random
const commitment = persistentCommit(secretValue, randomness);
console.log('Commitment:', commitment);

// 5. Generate public key
const privateKey = 12345n;
const publicKey = ecMulGenerator(privateKey);
console.log('Public key:', publicKey);

// 6. Validate values
const isValid = fieldType.validate(secretValue);
console.log('Valid field:', isValid);
```

## Integration with Generated Code

### Circuit Execution

```typescript
// Generated by Compact compiler
import { Contract, Witnesses } from './contract';

// Implement witnesses
const witnesses: Witnesses<MyPrivateState> = {
  async getSecret(context) {
    // Access ledger (read-only)
    const publicData = context.ledger.someField;
    
    // Access private state
    const privateData = context.privateState.secret;
    
    // Return [newState, result]
    return [context.privateState, secretValue];
  }
};

// Create contract instance
const contract = new Contract(witnesses);

// Execute circuit
const [newPrivateState, publicState] = contract.initialState(initialPrivateState);
const results = await contract.circuits.myCircuit(
  { privateState: newPrivateState, ledgerState: publicState },
  param1,
  param2
);

console.log('Result:', results.result);
console.log('New state:', results.privateState);
```

### Pure Circuits

```typescript
import { pureCircuits } from './contract';

// Pure circuits don't need context
const result = pureCircuits.calculateHash(data);
```

## Best Practices

### 1. Always Set Network ID
```typescript
// ✅ At app initialization
setNetworkId(NetworkId.TestNet);

// ❌ Forgetting this causes errors
const hash = persistentHash(data);  // ERROR if network not set
```

### 2. Use Correct Hash Type
```typescript
// ✅ Persistent for ledger data
ledgerField = persistentHash(data);

// ✅ Transient for temporary data
const tempHash = transientHash(data);

// ❌ Wrong type
ledgerField = transientHash(data);  // Type mismatch
```

### 3. Never Reuse Nonces
```typescript
// ✅ Generate fresh randomness
const nonce1 = generateRandomBytes(32);
const commitment1 = persistentCommit(value1, nonce1);

const nonce2 = generateRandomBytes(32);  // Different!
const commitment2 = persistentCommit(value2, nonce2);

// ❌ Reusing nonce breaks security
const commitment3 = persistentCommit(value3, nonce1);  // INSECURE
```

### 4. Validate Runtime Types
```typescript
// ✅ Validate before use
if (!fieldType.validate(userInput)) {
  throw new Error('Invalid field value');
}

// ❌ Assuming validity
const result = processField(userInput);  // May fail
```

## Resources

- **API Documentation**: https://docs.midnight.network/api-reference/compact-runtime
- **Network Configuration**: See network-configuration.md
- **Type System**: See type-system.md (midnight-compact)
- **Generated Code**: See typescript-interop.md (midnight-compact)


```typescript
interface CircuitResults {
  outputs: any[];
  proof: Proof;
}
```

## Hashing Functions

### transientHash
```typescript
function transientHash(data: Uint8Array): Field
```
Hash data with transient commitment scheme.

### persistentHash
```typescript
function persistentHash(data: Uint8Array): Field
```
Hash data with persistent commitment scheme.

## Commitment Functions

### transientCommit
```typescript
function transientCommit(value: Field): Field
```
Create transient commitment (temporary).

### persistentCommit
```typescript
function persistentCommit(value: Field, randomness: Field): Field
```
Create persistent commitment (long-term).

### degradeToTransient
```typescript
function degradeToTransient(commitment: Field): Field
```
Convert persistent commitment to transient.

## Elliptic Curve Operations

### ecAdd
```typescript
function ecAdd(point1: ECPoint, point2: ECPoint): ECPoint
```
Add two elliptic curve points.

### ecMul
```typescript
function ecMul(point: ECPoint, scalar: Field): ECPoint
```
Multiply point by scalar.

### ecMulGenerator
```typescript
function ecMulGenerator(scalar: Field): ECPoint
```
Multiply generator point by scalar.

### hashToCurve
```typescript
function hashToCurve(data: Uint8Array): ECPoint
```
Hash data to curve point.

## Contract State

### ContractState
Encapsulates smart contract's on-chain state.

```typescript
class ContractState {
  constructor(stateData: StateData);
  getValue(key: string): StateValue;
  setValue(key: string, value: StateValue): void;
}
```

### StateValue
Encoding for on-chain data.

```typescript
class StateValue {
  static fromField(field: Field): StateValue;
  static fromBytes(bytes: Uint8Array): StateValue;
  toField(): Field;
  toBytes(): Uint8Array;
}
```

### QueryContext
Annotated view into contract state for VM programs.

```typescript
class QueryContext {
  constructor(state: ContractState);
  query(program: VMProgram): QueryResult;
}
```

## Compact Types

### CompactType
Runtime representation of Compact datatypes.

```typescript
interface CompactType {
  name: string;
  fields: Field[];
  encode(value: any): Uint8Array;
  decode(data: Uint8Array): any;
}
```

## Field Operations

### addField
```typescript
function addField(a: Field, b: Field): Field
```

### mulField
```typescript
function mulField(a: Field, b: Field): Field
```

### subField
```typescript
function subField(a: Field, b: Field): Field
```

### divField
```typescript
function divField(a: Field, b: Field): Field
```

## Example Usage

```typescript
import {
  setNetworkId,
  NetworkId,
  transientHash,
  persistentCommit,
  ecMulGenerator
} from '@midnight-ntwrk/compact-runtime';

// Initialize
setNetworkId(NetworkId.TestNet);

// Hash data
const data = new Uint8Array([1, 2, 3, 4]);
const hash = transientHash(data);

// Create commitment
const value = BigInt(42);
const randomness = BigInt(12345);
const commitment = persistentCommit(value, randomness);

// Elliptic curve operation
const scalar = BigInt(7);
const point = ecMulGenerator(scalar);
```

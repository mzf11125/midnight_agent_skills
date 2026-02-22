# Compact Runtime API Reference

**Package**: `@midnight-ntwrk/compact-runtime v0.14.0`

## Overview

Runtime primitives for Compact's TypeScript output, used by compiler and for reproducing its behavior.

## Setup

```typescript
import { setNetworkId, NetworkId } from '@midnight-ntwrk/compact-runtime';

// Set network before any operations
setNetworkId(NetworkId.TestNet);
```

## Core Types

### CircuitContext
Input/output definition for all circuits.

```typescript
interface CircuitContext {
  publicInputs: any[];
  publicOutputs: any[];
}
```

### WitnessContext
Private input definition for circuits.

```typescript
interface WitnessContext {
  privateInputs: any[];
}
```

### CircuitResults
Output from circuit execution.

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

# Compact Standard Library

## Cryptographic Functions

### Hashing
```compact
use std::crypto::hash;

let digest = hash(data);  // Generic hash function
```

### Commitments
```compact
use std::crypto::{commit, transientCommit, persistentCommit};

let commitment = commit(value, randomness);
let transient = transientCommit(value);  // Temporary commitment
let persistent = persistentCommit(value);  // Long-term commitment
```

### Elliptic Curve Operations
```compact
use std::crypto::{ecAdd, ecMul, ecMulGenerator};

let point1 = ecMulGenerator(scalar);  // Multiply generator by scalar
let point2 = ecMul(point, scalar);     // Multiply point by scalar
let sum = ecAdd(point1, point2);       // Add points
```

## Field Operations
```compact
use std::field::{addField, mulField, subField, divField};

let sum = addField(a, b);
let product = mulField(a, b);
```

## Blockchain Primitives
```compact
// Current block information
let blockNumber = block.number;
let blockTime = block.timestamp;

// Transaction information
let sender = msg.sender;
let value = msg.value;
```

## Data Structures
```compact
use std::collections::{Map, Set, Vec};

let map: Map<Field, U32> = Map::new();
let set: Set<Field> = Set::new();
let vec: Vec<U32> = Vec::new();
```

## Utility Functions
```compact
use std::convert::{toBytes, fromBytes};
use std::math::{min, max, abs};

let bytes = toBytes(value);
let value = fromBytes(bytes);
let minimum = min(a, b);
```

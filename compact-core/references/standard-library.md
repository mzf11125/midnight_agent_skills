# Compact Standard Library

## Overview

The Compact standard library provides built-in functions for cryptographic operations, field arithmetic, curve operations, and other common tasks. These functions are implemented directly by the compiler and translate to efficient circuit constraints. They are available in every Compact module without explicit imports.

## Cryptographic Hash Functions

### persistentHash

Computes a cryptographic hash of the input and stores the result persistently in the ledger. The hash is available for verification by future transactions.

```
let hash: Bytes<32> = persistentHash(data);
```

The function takes arbitrary data as input (Bytes values, struct values, or concatenations) and returns a 32-byte hash. The hash function used is a ZK-friendly hash function optimized for circuit efficiency rather than a general-purpose hash like SHA-256.

### leafHash

Computes a hash specifically for use as a leaf node in a Merkle tree. The hashing includes domain separation to prevent conflicts with non-leaf hashes.

```
let leaf: Bytes<32> = leafHash(key, value);
```

LeafHash is designed for use with StateBoundedMerkleTree. It ensures that leaf nodes cannot be interpreted as internal nodes, which would break the security of the Merkle tree.

### entryPointHash

Computes a hash that identifies the entry point of a contract call. This is used for domain separation in contract interactions.

```
let entryHash: Bytes<32> = entryPointHash(contractAddress, functionSelector);
```

EntryPointHash ensures that proofs generated for one contract function cannot be reused as proofs for a different function, even if the circuits are structurally similar.

### hashToCurve

Maps arbitrary data to a point on the elliptic curve. The mapping is deterministic and uniformly distributed, making it suitable for cryptographic protocols that require curve points as inputs.

```
let curvePoint: CurvePoint = hashToCurve(data);
```

HashToCurve is used in signature schemes and other protocols that need to convert arbitrary messages into curve points for further processing.

## Field Arithmetic

### bigIntModFr

Converts a large integer (represented as Bytes) to a field element modulo the field order.

```
let fieldElement: Field = bigIntModFr(largeInteger);
```

This function is used when importing values from outside the circuit that may not fit within a single field element. The result is the input modulo the field modulus.

### mulField

Multiplies two field elements. This is the fundamental multiplication operation in the circuit.

```
let product: Field = mulField(a, b);
```

Every multiplication in the circuit adds one multiplication gate. Minimizing the number of mulField calls is the primary way to reduce circuit size.

### subField

Subtracts one field element from another.

```
let difference: Field = subField(a, b);
```

Field subtraction is guaranteed to produce a result within the field range. Underflow wraps around according to modular arithmetic.

## Curve Operations

### ecAdd

Adds two points on the elliptic curve.

```
let sum: CurvePoint = ecAdd(pointA, pointB);
```

Curve point addition adds one complete addition gate to the circuit. The result is a point on the curve guaranteed by the circuit constraints.

### ecMul

Multiplies a curve point by a scalar (a field element). This is the fundamental scalar multiplication operation.

```
let product: CurvePoint = ecMul(point, scalar);
```

Scalar multiplication is the most expensive curve operation in terms of circuit constraints. It is used in signature verification and key derivation.

### ecMulGenerator

Multiplies the fixed generator point of the curve by a scalar. This is more efficient than general ecMul because the generator is known at compile time, allowing optimizations.

```
let pubkey: CurvePoint = ecMulGenerator(privateKey);
```

EcMulGenerator is the primary operation for deriving public keys from private keys. Because the base point is fixed, the compiler can use precomputed tables to reduce the circuit cost.

## Signature Verification

### verifySignature

Verifies a digital signature against a public key and message. Returns a Boolean indicating whether the signature is valid.

```
let valid: Boolean = verifySignature(publicKey, message, signature);
```

The signature scheme used is a Schnorr-style signature over the proving curve. This enables efficient verification within the circuit while maintaining the security level expected for blockchain applications.

Signature verification uses ecMul and ecAdd operations internally. The cost is roughly equivalent to two scalar multiplications. Contract authors should be mindful of this cost when designing contracts that verify many signatures in a single transaction.

## Encoding Functions

### pack

Converts values of various types into Bytes for hashing or storage. The function is overloaded to accept different input types.

```
let packed: Bytes<N> = pack(uint_value);
let packed: Bytes<N> = pack(struct_value);
```

Pack produces a canonical byte representation suitable for hashing. The encoding is deterministic: the same input always produces the same output bytes. This determinism is essential for consistent state commitments across different executions.

### unpack

Converts Bytes back into a typed value. The target type must be specified through the return type context.

```
let value: Uint<64> = unpack(bytes_data);
```

Unpack is the inverse of pack for types that support it. Not all types can be unpacked from arbitrary bytes. The compiler enforces type compatibility at compile time.

## Coin Functions

### createCoin

Creates a new coin commitment from a value, owner public key, and random salt. The commitment is a persistentHash of these inputs with domain separation.

```
let coin: Bytes<32> = createCoin(value, ownerPublicKey, salt);
```

CreateCoin is the foundation of shielded transfers. The resulting commitment is stored in the coin tree, and the owner can later prove ownership by demonstrating knowledge of the value, public key, and salt.

### createNullifier

Derives a nullifier from a coin's serial number and the owner's secret key. The nullifier is a persistentHash with domain separation.

```
let nf: Bytes<32> = createNullifier(coinSerialNumber, ownerSecretKey);
```

CreateNullifier ensures that the same coin always produces the same nullifier for the same owner, and different owners of the same coin produce different nullifiers. This is the mechanism that prevents double spending while preserving privacy.

### coinValue

Extracts the value from a coin commitment given the commitment, value, and salt. The function adds constraints that verify the commitment was formed correctly.

```
let value: Uint<64> = coinValue(commitment, claimedValue, salt);
```

The function returns the value only if the claimed value and salt match the stored commitment. If they do not match, the constraint fails and the proof cannot be generated. This is how the circuit enforces that only the coin's owner (who knows the value and salt) can spend it.

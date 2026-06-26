# Midnight Proof Server API Reference

## Overview

The Proof Server generates zero knowledge proofs required for private contract execution on the Midnight network. It exposes APIs for proof generation, proof checking, status monitoring, and configuration management. This document covers all API operations, proving payload types, key material, proof types, and proof provider interfaces.

## Proof Generation API

### Generate Proof

The `/proof` endpoint accepts a proving request containing the circuit identifier, input witness data, and optional configuration overrides. The server queues the request and returns a proof job identifier for status tracking. Inputs are validated before queuing to fail fast on malformed requests.

### Proof Job Status

The `/proof/status` endpoint accepts a proof job identifier and returns the current status. Status values include `queued`, `processing`, `completed`, and `failed`. Completed jobs include the generated proof data. Failed jobs include an error code and diagnostic message.

### Result Retrieval

The `/proof/result` endpoint retrieves the completed proof for a given job identifier. Results include the proof bytes, public outputs, and verification metadata. Results are cached for a configurable duration after which they require regeneration.

## Check API

### Validate Proof

The `/check` endpoint verifies a submitted proof against its public inputs. The server loads the verifier key for the specified circuit and executes the verification algorithm. Successful verification returns a confirmation with performance metrics.

### Batch Check

The `/check/batch` endpoint accepts multiple proofs and verifies them in sequence. This reduces overhead for clients with many proofs to validate. Results are returned as an array matching the input order with individual pass or fail statuses.

## Status API

### Server Health

The `/status` endpoint returns server health information including uptime, active worker count, queue depth, and memory usage. This endpoint does not require authentication and can be used for load balancer health checks and monitoring.

### Queue Statistics

The `/status/queue` endpoint provides detailed queue metrics. It reports the number of jobs in each status category, average processing time, and throughput rate. These metrics help in capacity planning and detecting processing bottlenecks.

### Worker Status

The `/status/workers` endpoint lists each worker process with its current state, the job it is processing, and runtime statistics. Worker details help diagnose uneven load distribution or stuck workers.

## Configuration API

### Get Configuration

The `/config` endpoint returns the current server configuration. This includes timeout values, concurrency limits, resource allocations, and network specific parameters. The response includes both applied values and default values for comparison.

### Update Configuration

The `/config` endpoint accepts a partial configuration object and merges it with the current settings. Only explicitly provided fields are updated. Configuration changes take effect immediately for new jobs while active jobs continue with their original settings.

### Reload Keys

The `/config/reload-keys` endpoint triggers a reload of proving keys and verifier keys from the configured key store. Use this endpoint after deploying new circuit versions to avoid server restarts.

## Proving Payloads

### createProvingPayload

The `createProvingPayload` function constructs the data structure sent to the proof generation endpoint. It accepts a circuit name, input witness data, and optional metadata. The payload is serialized to a format compatible with the proving backend.

### createProvingTransactionPayload

The `createProvingTransactionPayload` function extends the proving payload with transaction context. It includes the block height, transaction hash, and chain state references needed for transaction aware proof generation. This payload type is used when proofs must reference specific blockchain state.

### createCheckPayload

The `createCheckPayload` function constructs the data structure sent to the proof verification endpoint. It accepts the proof bytes, public inputs, and the circuit identifier. The payload includes all data needed for the verifier to execute the verification algorithm.

## Key Material

### Proving Keys

Proving keys are the cryptographic material required to generate a zero knowledge proof for a specific circuit. Each circuit version has a unique proving key. Keys are stored in the key store and loaded into memory on server startup or through the reload keys endpoint.

### Verifier Keys

Verifier keys are the cryptographic material required to verify a zero knowledge proof. They are derived from the proving key and are significantly smaller. Verifier keys are published onchain so any party can verify proofs without running a proof server.

### ZKIR

Zero Knowledge Intermediate Representation files contain the compiled circuit description. Each ZKIR file encodes the arithmetic circuit representing a Compact contract. The proof server uses ZKIR files to determine the proving and verification algorithms for each circuit.

### Key Management

Keys are versioned and associated with specific contract deployments. The proof server maintains a key registry mapping contract identifiers to the appropriate key versions. Key rotation occurs when contracts are upgraded with new circuit versions.

## Proof Types

### Proof

The Proof type represents a successfully generated zero knowledge proof. It contains the proof bytes, public outputs, and metadata including the circuit identifier, proving time, and proof size. The proof is serializable for transmission to the blockchain.

### PreProof

The PreProof type represents an intermediate stage in proof generation. Some circuits require multiple proving steps where intermediate results must be exchanged between parties. The PreProof encapsulates the partial computation state between steps.

### NoProof

The NoProof type indicates that no proof was generated for a computation. This occurs when the computation produces only public outputs with no private inputs requiring zero knowledge protection. The NoProof still carries the public outputs for onchain submission.

### ProofData

The ProofData type wraps Proof and NoProof variants with additional metadata. It includes the circuit identifier, a hash of the public inputs, and a timestamp. ProofData is the standard format for associating proofs with transactions.

## Proof Providers

### httpClientProofProvider

The `httpClientProofProvider` communicates with a proof server over HTTP. It implements the proof provider interface for applications running outside the browser. Configuration includes the proof server URL, authentication token, and retry policy.

### dappConnectorProofProvider

The `dappConnectorProofProvider` integrates with the Midnight DApp Connector browser extension. It routes proof requests through the extension which manages key material and communicates with the configured proof server. This provider is used by browser based decentralized applications.

### Provider Interface

Both providers implement a common interface with `prove`, `check`, and `getStatus` methods. Applications code against the interface rather than concrete implementations enabling provider swapping based on deployment context.

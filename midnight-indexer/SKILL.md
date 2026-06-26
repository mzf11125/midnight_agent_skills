---
name: midnight-indexer
description: Query and subscribe to Midnight blockchain data via the Indexer GraphQL API v4. Covers contract state reads, transaction lookups, block queries, real-time subscriptions, state deserialization, the offset/null bug workaround, and TypeScript helper patterns. Use when a user needs to read on-chain state after a transaction, watch contract events in real time, look up blocks or transactions, query unshielded balances, monitor DUST generation status, or debug indexer connectivity issues.
---

# Midnight Indexer

## Indexer Overview

The Midnight Indexer is a blockchain data indexing pipeline that ingests raw ledger data from a Midnight node, processes it into a structured relational format, stores it in a PostgreSQL database, and exposes it through a GraphQL API. This pipeline enables efficient historical queries and real-time subscriptions over all on-chain activity. The indexer is a critical piece of infrastructure that sits between a Midnight node and any dApp or service that needs to query blockchain state.

The indexer performs three core functions. First it continuously reads blocks and transactions from a connected Midnight node as they are produced. Second it transforms raw ledger data into normalized database tables that are optimized for query performance. Third it exposes a GraphQL API v4 endpoint that clients use to request data and subscribe to real-time updates.

Real-time subscriptions allow dApps to react to blockchain events as they occur. When a new block is produced or a contract action is confirmed, the indexer pushes that event to all subscribed clients over a WebSocket connection. This eliminates the need for polling and enables responsive user interfaces that update immediately when on-chain state changes.

Historical queries allow dApps to retrieve past data. You can look up any block by hash or height, retrieve any transaction by its ID, list all contract actions for a given address, or query aggregate statistics across multiple epochs. The indexer maintains a complete history of the chain from genesis to the current tip.

The indexer is designed to be deployed alongside a Midnight node. In a typical local development setup, the Docker Compose stack defined by midnight-local-dev runs a node, an indexer, and a proof server together. For test networks and mainnet, the indexer runs as a separate service that connects to the network's nodes.

Key capabilities of the indexer include querying block headers and metadata, listing transactions with their status and fees, retrieving contract state and deployed contract information, looking up committee membership and epoch details, tracking DUST generation and consumption, subscribing to real-time block production, subscribing to real-time contract actions, monitoring shielded transaction events, monitoring unshielded transaction events, and subscribing to zswap ledger events.

## Architecture

The indexer architecture consists of four main layers. The data retrieval layer connects to a Midnight node and pulls blocks and transactions as they are finalized. The processing pipeline layer transforms raw ledger data into structured records by decoding binary formats, resolving internal references, and normalizing data into database rows. The indexed storage layer persists the processed data in a PostgreSQL database with appropriate indexes for fast queries. The GraphQL layer exposes the data through a GraphQL API v4 endpoint that handles queries, mutations, and subscriptions.

The data retrieval layer uses the node's JSON-RPC API or the Cardano DB Sync integration to fetch new blocks. It tracks the last processed block height and only fetches new data since that point. When starting from scratch, it begins at genesis and processes every block sequentially. When resuming after a restart, it picks up from the last persisted block.

The processing pipeline layer decodes each block into its constituent parts. It extracts the block header metadata, the list of transactions, each transaction's inputs and outputs, contract calls and deployments, and system-level events. It also processes the ledger state to compute contract balances, track DUST generation, and maintain the collapsed Merkle tree state. All decoded data is inserted into normalized database tables with foreign key relationships.

The indexed storage layer uses PostgreSQL as its backing store. Tables are designed around the GraphQL schema so that queries map directly to efficient SQL queries. Indexes are created on frequently queried columns such as block height, transaction hash, contract address, and epoch number. The database schema is versioned alongside the indexer software so that upgrades can include migrations.

The GraphQL layer implements the GraphQL API v4 specification. It supports a comprehensive set of query operations that cover all indexed data. It supports mutations for wallet session management such as connecting and disconnecting viewing keys. It supports subscriptions over WebSocket connections for real-time event delivery. The GraphQL layer also handles authentication via viewing keys for accessing private state data.

## GraphQL API v4

The GraphQL API v4 is the primary interface for interacting with the indexer. It provides a single endpoint that handles all queries, mutations, and subscriptions. The endpoint URL varies by environment. For local development it is typically `http://localhost:8085/graphql`. For test networks and mainnet, the endpoint is provided by the network operator.

Authentication is handled through viewing keys. To access private state data such as shielded transaction details or contract state that requires authorization, the client must authenticate with a valid viewing key. This is done through the `connectWallet` mutation which establishes a session. The session remains active until the client disconnects via the `disconnectWallet` mutation or the session expires.

Session management operates as follows. The `connectWallet` mutation takes a viewing key and returns a session token. The session token is included in subsequent requests either as an HTTP header or as a connection parameter for WebSocket subscriptions. The indexer uses the session to determine which private data the client is authorized to view. Multiple sessions can exist simultaneously for different viewing keys.

Viewing keys are derived from wallet keys using a specific derivation path. They grant read-only access to private state associated with a specific set of keys. Viewing keys do not grant the ability to create transactions or modify state. They are designed specifically for the indexer's read operations.

The GraphQL API supports both HTTP POST requests for queries and mutations, and WebSocket connections for subscriptions. The WebSocket protocol uses the `graphql-ws` sub-protocol for managing subscription lifecycle including subscribe, next, error, and complete message types.

## Queries

### Block Lookup

Blocks can be queried by hash or by height. The `block` query takes an offset parameter that specifies which block to retrieve.

```graphql
query {
  block(offset: { height: 12345 }) {
    hash
    height
    timestamp
    epoch
    slotNo
    txCount
    previousBlock { hash }
  }
}
```

The block object includes the block hash as a hex-encoded string, the block height as an integer, the timestamp of block production, the epoch number, the slot number within the epoch, the count of transactions in the block, and a reference to the previous block.

Multiple blocks can be queried using the `blocks` query which accepts a range offset or a list of specific offsets. Pagination is supported through limit and cursor parameters.

### Transaction Lookup

Transactions can be queried by hash or by transaction ID. The `transaction` query takes an offset parameter.

```graphql
query {
  transaction(offset: { hash: "abcdef..." }) {
    hash
    block { height }
    status
    fees { total }
    index
    data
  }
}
```

The `transactions` query allows listing transactions with optional filtering by block height range or by contract address. Results are paginated.

### Contract Actions

Contract actions represent all interactions with a Compact contract. The `contractActions` query retrieves actions for a specific contract address.

```graphql
query {
  contractActions(offset: { contractAddress: "contract_abc..." }) {
    contractAddress
    block { height }
    transaction { hash }
    action {
      ... on ContractCall {
        methodName
        callData
      }
      ... on ContractDeploy {
        contractCode
      }
    }
  }
}
```

The `ContractAction` union type distinguishes between `ContractCall` actions which represent method invocations on an existing contract and `ContractDeploy` actions which represent the initial deployment of a new contract. Each action includes the block and transaction context.

### Contract Balances

The `contractBalance` query retrieves the current balance for a specific contract address. The balance includes both shielded and unshielded token amounts.

```graphql
query {
  contractBalance(contractAddress: "contract_abc...") {
    address
    amount
    tokenId
  }
}
```

### Committee Membership

The `committeeMembers` query retrieves the current or historical committee membership. The committee is responsible for block production and consensus.

```graphql
query {
  committeeMembers(epoch: 42) {
    members {
      address
      votingPower
    }
    totalMembers
  }
}
```

### Epoch Information

The `epochInfo` query retrieves details about a specific epoch or the current epoch.

```graphql
query {
  epochInfo(epoch: 42) {
    epochNumber
    firstBlock { height }
    lastBlock { height }
    slotCount
    committeeSize
  }
}
```

### D Parameter History

The D parameter controls the decentralization of the network. The `dParameters` query retrieves the history of D parameter values.

```graphql
query {
  dParameters {
    epoch
    value
    timestamp
  }
}
```

### DUST Generation Status

The DUST ledger tracks DUST token generation and consumption. The `dustLedger` query retrieves DUST related information.

```graphql
query {
  dustLedger {
    outputs {
      address
      amount
      status
    }
    totalGenerated
    totalConsumed
  }
}
```

### SPO Queries

Stake pool operator data can be queried through the `spoIdentities` and `spoComposites` queries. These provide information about registered stake pools.

```graphql
query {
  spoIdentities {
    poolId
    metadata { name ticker description }
  }
}
```

### Stake Distribution

The `stakeDistribution` query retrieves the distribution of stake across the network. This includes per validator stake amounts and delegator information.

```graphql
query {
  stakeDistribution(epoch: 42) {
    shares {
      poolId
      amount
      percentage
    }
  }
}
```

## Subscriptions

### Blocks Subscription

The `blocks` subscription delivers a new block event each time a block is produced and indexed. This is useful for applications that need to react to every new block.

```graphql
subscription {
  blocks {
    hash
    height
    timestamp
    epoch
    slotNo
    txCount
    previousBlock { hash }
  }
}
```

The subscription starts delivering events from the current tip forward. It does not replay historical blocks. Each event contains the full block object. The subscription remains active until the client disconnects.

### Contract Actions Subscription

The `contractActions` subscription delivers events whenever a contract is called or deployed. This is the primary mechanism for dApps to react to on-chain contract activity.

```graphql
subscription {
  contractActions(contractAddress: "contract_abc...") {
    contractAddress
    block { height }
    transaction { hash }
    action {
      ... on ContractCall {
        methodName
        callData
      }
      ... on ContractDeploy {
        contractCode
      }
    }
  }
}
```

The subscription can be filtered by contract address to only receive events for a specific contract. Without a filter, it delivers events for all contracts. Each event includes enough context to identify the block, transaction, and action details.

### DUST Ledger Events

The `dustLedger` subscription delivers events related to DUST token generation and consumption. DUST tokens are used to pay for transaction fees in the Midnight network.

```graphql
subscription {
  dustLedger {
    output { address amount }
    event
    timestamp
  }
}
```

Events include new DUST generation outputs, DUST consumption for fees, and DUST output status changes.

### Shielded Transactions Events

The `shieldedTransactions` subscription delivers events for shielded transactions. Shielded transactions are private and require a viewing key to access. The subscription must be used in conjunction with the `connectWallet` mutation.

```graphql
subscription {
  shieldedTransactions {
    event {
      ... on ShieldedTxEvent {
        txHash
        status
      }
    }
  }
}
```

The `ShieldedTransactionsEvent` union type includes different event variants for different stages of shielded transaction processing. Events include transaction submission, inclusion in a block, and finalization.

### Unshielded Transactions Events

The `unshieldedTransactions` subscription delivers events for unshielded transactions. Unshielded transactions are public and do not require a viewing key.

```graphql
subscription {
  unshieldedTransactions(address: "addr_abc...") {
    event {
      ... on UnshieldedTxEvent {
        txHash
        utxos { address amount }
        status
      }
    }
  }
}
```

The subscription can be filtered by address to only receive events related to a specific unshielded address. Events include UTXO creation, consumption, and transaction status changes.

### ZSwap Ledger Events

The `zswapLedger` subscription delivers events from the ZSwap ledger. ZSwap is Midnight's shielded token swap mechanism.

```graphql
subscription {
  zswapLedger {
    event {
      ... on ZswapEvent {
        offerId
        status
        details
      }
    }
  }
}
```

Events include offer creation, acceptance, cancellation, and settlement.

## Mutations

### Connect Wallet

The `connectWallet` mutation establishes a session for accessing private state. It takes a viewing key and returns a session token.

```graphql
mutation {
  connectWallet(viewingKey: "vk_abc...") {
    sessionToken
    expiresAt
  }
}
```

The session token must be included in subsequent requests. For HTTP requests, it is sent as a header. For WebSocket subscriptions, it is sent as a connection initialization parameter.

### Disconnect Wallet

The `disconnectWallet` mutation terminates an active session. It takes the session token returned by `connectWallet`.

```graphql
mutation {
  disconnectWallet(sessionToken: "session_abc...")
}
```

After disconnecting, the session token is invalidated and can no longer be used to access private data. It is good practice to disconnect when the dApp no longer needs private state access.

## Data Types and Objects

### Block

The `Block` type represents a block on the Midnight blockchain. Fields include `hash` of type `HexEncoded`, `height` of type `Int`, `timestamp` of type `String`, `epoch` of type `Int`, `slotNo` of type `Int`, `txCount` of type `Int`, `previousBlock` of type `Block`, `transactions` of type `[Transaction]`, and `committeeMembers` of type `[CommitteeMember]`.

### Transaction

The `Transaction` type represents a single transaction within a block. Fields include `hash` of type `HexEncoded`, `block` of type `Block`, `status` of type `TransactionResultStatus`, `fees` of type `TransactionFees`, `index` of type `Int`, `data` of type `String`, `contractActions` of type `[ContractAction]`, and `result` of type `TransactionResult`.

### ContractAction

The `ContractAction` union type represents either a `ContractCall` or a `ContractDeploy`. It includes the `contractAddress` field of type `String`, the `block` field of type `Block`, and the `transaction` field of type `Transaction`.

### ContractCall

The `ContractCall` type represents a method invocation on an existing contract. Fields include `methodName` of type `String` and `callData` of type `String`.

### ContractDeploy

The `ContractDeploy` type represents the initial deployment of a contract. Fields include `contractCode` of type `String`.

### ContractBalance

The `ContractBalance` type represents the balance of a contract. Fields include `address` of type `String`, `amount` of type `Int`, and `tokenId` of type `String`.

### CollapsedMerkleTree

The `CollapsedMerkleTree` type represents the collapsed Merkle tree state used for efficient ZK proofs. Fields include `root` of type `HexEncoded` and `size` of type `Int`.

### CommitteeMember

The `CommitteeMember` type represents a member of the consensus committee. Fields include `address` of type `String` and `votingPower` of type `Float`.

### DustOutput

The `DustOutput` type represents a DUST token output. Fields include `address` of type `DustAddress`, `amount` of type `Int`, and `status` of type `String`.

### EpochInfo

The `EpochInfo` type represents information about an epoch. Fields include `epochNumber` of type `Int`, `firstBlock` of type `Block`, `lastBlock` of type `Block`, `slotCount` of type `Int`, and `committeeSize` of type `Int`.

### DParameter

The `DParameter` type represents a D parameter value at a point in time. Fields include `epoch` of type `Int`, `value` of type `Float`, and `timestamp` of type `String`.

### PoolMetadata

The `PoolMetadata` type represents stake pool metadata. Fields include `name` of type `String`, `ticker` of type `String`, `description` of type `String`, and `homepage` of type `String`.

### SpoIdentity

The `SpoIdentity` type represents a registered stake pool operator identity. Fields include `poolId` of type `String` and `metadata` of type `PoolMetadata`.

### SpoComposite

The `SpoComposite` type represents a composite view of a stake pool. Fields include `identity` of type `SpoIdentity` and `stake` of type `StakeShare`.

### StakeShare

The `StakeShare` type represents a share of the total stake. Fields include `poolId` of type `String`, `amount` of type `Int`, and `percentage` of type `Float`.

### TransactionResult

The `TransactionResult` type represents the result of a transaction execution. Fields include `status` of type `TransactionResultStatus` and `errorMessage` of type `String` when the status is failure.

### TransactionFees

The `TransactionFees` type represents the fees paid for a transaction. Fields include `total` of type `Int`, `computation` of type `Int`, and `storage` of type `Int`.

### UnshieldedUtxo

The `UnshieldedUtxo` type represents an unspent transaction output. Fields include `address` of type `UnshieldedAddress`, `amount` of type `Int`, `tokenId` of type `String`, and `txHash` of type `HexEncoded`.

### SystemTransaction

The `SystemTransaction` type represents a system-level transaction such as epoch transitions or parameter updates.

## Enums

### TransactionResultStatus

The `TransactionResultStatus` enum has three values. `success` means the transaction was fully executed and all its effects applied. `partialSuccess` means some but not all effects of the transaction were applied, typically due to some sub-operations failing while others succeeded. `failure` means the transaction was rejected entirely and no effects were applied.

## Scalars

`CardanoRewardAddress` is a string scalar representing a Cardano reward address used for stake delegation. `DustAddress` is a string scalar representing a DUST token address. `HexEncoded` is a string scalar for hex-encoded binary data. `UnshieldedAddress` is a string scalar representing an unshielded Midnight address. `ViewingKey` is a string scalar representing a viewing key for private state access. `Boolean` is the standard GraphQL boolean. `Float` is the standard GraphQL float. `Int` is the standard GraphQL 32-bit integer. `String` is the standard GraphQL string. `Unit` is a scalar representing no value, used for mutation results.

## Unions

### ShieldedTransactionsEvent

The `ShieldedTransactionsEvent` union type includes event variants for shielded transaction lifecycle events. Variants include transaction submission events, block inclusion events, and finalization events. Each variant contains the relevant data for that stage of processing.

### UnshieldedTransactionsEvent

The `UnshieldedTransactionsEvent` union type includes event variants for unshielded transaction lifecycle events. Variants include UTXO creation events, UTXO consumption events, and transaction status change events.

## Directives

The GraphQL API v4 uses standard GraphQL directives. `include` conditionally includes a field or fragment when the argument is true. `skip` conditionally excludes a field or fragment when the argument is true. `deprecated` marks a field as deprecated with an optional reason string. `oneOf` indicates that exactly one of a set of input fields must be provided. `specifiedBy` provides a URL to the specification for a custom scalar type.

## Offsets

### BlockOffset

The `BlockOffset` input type specifies how to locate a block. It supports lookup by hash using the `hash` field of type `HexEncoded` or by height using the `height` field of type `Int`. Exactly one of these fields must be provided.

### ContractActionOffset

The `ContractActionOffset` input type specifies how to locate contract actions. It supports filtering by block using the `block` field which references a `BlockOffset` or by transaction using the `transaction` field which references a `TransactionOffset`.

### TransactionOffset

The `TransactionOffset` input type specifies how to locate a transaction. It supports lookup by hash using the `hash` field of type `HexEncoded` or by transaction ID using the `transactionId` field of type `String`.

## Shielded Transactions

Shielded transactions are private transactions where the details of the transfer are hidden from public view. Accessing shielded transaction data requires authenticating with a viewing key that has been granted access to the relevant private state.

The connect and disconnect pattern works as follows. First the dApp calls `connectWallet` with a viewing key to establish a session. The session token is stored and included in subsequent requests. Shielded transaction queries and subscriptions then return data scoped to the authorized viewing key. When the dApp no longer needs access, it calls `disconnectWallet` to terminate the session.

Session management is handled by the indexer. Sessions have a configurable timeout period. If no requests are made within the timeout period, the session is automatically terminated. The dApp is responsible for reconnecting if the session expires.

The viewing key derivation path is specific to the wallet implementation. The 1AM browser extension wallet uses a specific derivation path for generating viewing keys from the wallet's master key. The viewing key is then passed to the indexer through the `connectWallet` mutation.

Progress tracking for shielded transactions is done through the subscription mechanism. Each event includes a transaction hash and status. The dApp can track the lifecycle of a shielded transaction from submission through inclusion to finalization by monitoring these events.

The `RelevantTransaction` type is returned as part of shielded transaction subscriptions. It includes the transaction hash, status, and any relevant data that the viewing key authorizes access to. Transactions that are not relevant to the connected viewing key are not delivered.

## Unshielded Transactions

Unshielded transactions are public transactions where all details are visible on-chain. They do not require a viewing key to access. Unshielded transaction subscriptions are filtered by address rather than by viewing key.

Address-based subscriptions deliver events for all transactions that involve a specific unshielded address. The dApp subscribes with the address as a filter and receives events whenever that address sends or receives tokens. This is the primary mechanism for tracking unshielded balances and activity.

UTXO tracking through subscriptions allows the dApp to maintain an up-to-date view of all unspent transaction outputs for a given address. Each event includes the UTXOs created or consumed by a transaction. The dApp aggregates these events to compute the current UTXO set.

Progress tracking works similarly to shielded transactions. Each event includes a transaction hash and status. The dApp can track the lifecycle of an unshielded transaction through the event stream.

## State Deserialization

Contract state on Midnight is stored in a compact binary format. To read contract state through the indexer, the raw state data must be deserialized into the types defined in the Compact contract. The indexer does not automatically deserialize contract state because it does not have the contract's type definitions. Deserialization must be done client-side using the compact runtime.

The deserialization process uses the compact type definitions from the compiled contract. The `midnight-js` library provides helper functions for deserializing state. The `SparseCompact` type represents contract state that may have missing or optional fields. The deserialization code must handle these sparse types correctly.

Compact type handling involves mapping between the Compact language types and their JavaScript or TypeScript equivalents. Integer types map to BigInt or number. Bytes types map to Uint8Array. Record types map to objects. Variant types map to discriminated unions. Each type requires specific deserialization logic.

SparseCompact types occur when contract state has fields that are optional or that have been modified from their default values. The serialized form only includes fields with non-default values. When deserializing, missing fields must be filled in with their default values from the contract definition.

## Helper Patterns

The midnight-js indexer module provides several helper functions for working with indexer data.

### isRegularTransaction

The `isRegularTransaction` function determines whether a transaction is a regular user transaction or a system transaction. Regular transactions are those submitted by users or dApps. System transactions are internal transactions such as epoch transitions. This distinction is important for filtering and display purposes.

### toTxStatus

The `toTxStatus` function converts the raw `TransactionResultStatus` enum value into a human-readable status string. It handles the `success`, `partialSuccess`, and `failure` variants and returns appropriate display strings. This is useful for user interfaces that need to show transaction status.

### toSegmentStatus

The `toSegmentStatus` function converts a segment status code into a human-readable string. Segments are parts of a transaction and each segment has its own status. This function provides a consistent way to display segment-level status information.

### toSegmentStatusMap

The `toSegmentStatusMap` function creates a mapping from segment IDs to their status strings. This is useful when a transaction has multiple segments and you need to display the status of each one. The map allows efficient lookup by segment ID.

### toUnshieldedBalances

The `toUnshieldedBalances` function aggregates UTXO data into a balance map. It takes a list of unshielded UTXOs and sums the amounts by token ID. The result is a map from token ID to total amount. This is the standard way to compute unshielded balances from UTXO data.

### toUnshieldedUtxos

The `toUnshieldedUtxos` function converts raw indexer response data into a typed UTXO array. It handles the deserialization and normalization of UTXO data from the GraphQL response format into the application's internal representation.

## Indexer Public Data Provider

The Indexer Public Data Provider is a component in the midnight-js library that integrates with the indexer. It wraps GraphQL queries behind a provider interface that other components in midnight-js can use without knowing about GraphQL.

The provider implementation handles connection management to the indexer endpoint, query execution and result deserialization, subscription setup and teardown, error handling and retry logic, and caching of frequently accessed data.

Integration with midnight-js is through the provider interface. The provider is passed to wallet and contract components during initialization. These components use the provider to query block data, transaction data, and contract state without directly calling the GraphQL API. This abstraction allows the same application code to work with different indexer implementations.

Wrapping GraphQL queries behind the provider interface means that application code does not need to know about GraphQL syntax. The provider exposes typed methods that return typed results. This improves type safety and makes the code easier to maintain.

## Operational Guidance

### Indexer Setup

Setting up an indexer requires a running Midnight node, a PostgreSQL database, and the indexer software. In development, midnight-local-dev automates this setup using Docker Compose. For production deployments, each component must be configured manually.

The indexer connects to the node using its JSON-RPC endpoint. This endpoint must be reachable from the indexer's network. The indexer also requires a PostgreSQL connection string for its database. The database must be initialized with the correct schema before the indexer starts.

Configuration is typically done through environment variables or a configuration file. Key settings include the node endpoint URL, the PostgreSQL connection string, the GraphQL API port, the session timeout duration, and the batch size for block processing.

### Configuration

The indexer can be configured through environment variables. Common variables include `NODE_ENDPOINT` for the Midnight node JSON-RPC URL, `DATABASE_URL` for the PostgreSQL connection string, `GRAPHQL_PORT` for the API port, `SESSION_TIMEOUT` for how long viewing key sessions last, `BATCH_SIZE` for how many blocks to process at once, and `LOG_LEVEL` for logging verbosity.

In Docker deployments, these variables are set in the Docker Compose file or passed as container environment variables. In standalone deployments, they are set in the shell environment or in a dotenv file.

### Scaling

The indexer is designed to run as a single instance because it must process blocks sequentially. Horizontal scaling is not supported in the current architecture. Instead, scaling is achieved by increasing the resources allocated to the indexer instance.

For high throughput environments, the indexer benefits from fast storage for the PostgreSQL database, sufficient memory for caching indexed data, and a low latency connection to the Midnight node. The GraphQL endpoint can be scaled independently by deploying a read replica of the database.

### Troubleshooting

Common issues include the indexer falling behind the node due to slow database performance, connection failures to the node requiring automatic reconnection, memory pressure from large query result sets, and session management issues with expired or invalid viewing keys.

The indexer exposes health check endpoints that can be used for monitoring. A `/health` endpoint returns a 200 status when the indexer is healthy. A `/metrics` endpoint exposes Prometheus-compatible metrics including processed block count, query latency, subscription count, and error rates.

### Version Compatibility

The indexer version must be compatible with the Midnight node version it connects to. Breaking changes in the node API may require an indexer upgrade. The indexer's GraphQL API version is independent of the node version, but the underlying data schema changes with node protocol upgrades.

Always check the compatibility matrix before deploying. The midnight-js version must also be compatible with the indexer's GraphQL API version. Mismatches can cause query errors or data deserialization failures.

## Error Codes

### IndexerError

The `IndexerError` type represents errors returned by the indexer. It includes an `errorCode` field of type `String`, a `message` field of type `String`, and optional `details` of type `String`. Error codes follow a consistent naming pattern based on the category of error.

### IndexerFormattedError

The `IndexerFormattedError` type wraps a raw error with additional context for display purposes. It includes the original error, a formatted message suitable for user display, and a suggested resolution action.

### Common Error Patterns

The error code `AUTHENTICATION_REQUIRED` means that a viewing key session is required for the requested operation. The resolution is to call `connectWallet` before making the request.

The error code `INVALID_VIEWING_KEY` means the provided viewing key is malformed or invalid. The resolution is to verify the viewing key derivation and try again.

The error code `SESSION_EXPIRED` means the viewing key session has timed out. The resolution is to call `connectWallet` again to establish a new session.

The error code `BLOCK_NOT_FOUND` means the requested block hash or height does not exist. This may occur if the block has not yet been indexed or if the hash is invalid. Wait for the indexer to catch up or verify the hash.

The error code `TRANSACTION_NOT_FOUND` means the requested transaction hash or ID does not exist. Similar to block not found, this may be a timing issue.

The error code `SUBSCRIPTION_LIMIT_REACHED` means the client has too many active subscriptions. Close unused subscriptions before opening new ones.

The error code `QUERY_TIMEOUT` means the query took too long to execute. Simplify the query or add appropriate filters.

The error code `RATE_LIMITED` means the client has exceeded the rate limit for requests. Implement exponential backoff and reduce request frequency.

## Best Practices

### Efficient Querying

Request only the fields you need. GraphQL allows you to specify exactly which fields to return and requesting unnecessary fields increases query latency and database load. Use filters to limit result sets. Queries that return large result sets should use pagination with reasonable page sizes.

Use the block and transaction offsets to target specific data rather than scanning large ranges. When querying contract actions, always filter by contract address. When querying transactions, use time ranges or block ranges to limit the scope.

### Pagination

Always paginate queries that return lists. The default page size is typically 50 items. Larger page sizes increase latency and memory usage. Use cursor-based pagination for forward-only traversal and offset-based pagination for random access.

Cursor-based pagination uses the `after` parameter to specify the last item from the previous page. This is the most efficient pagination method because it uses index lookups. The `PageInfo` type returned with paginated results includes `hasNextPage` and `endCursor` fields for determining whether more pages exist.

### Subscription Lifecycle

Open subscriptions only when needed and close them when no longer needed. Each active subscription consumes server resources and network bandwidth. Implement reconnection logic with exponential backoff in case the WebSocket connection drops.

Use subscription filters to limit the events you receive. Filtering by contract address or address reduces network traffic and client-side processing. Subscribe at the most specific level that meets your needs.

### Error Handling

Implement comprehensive error handling for all indexer interactions. Handle authentication errors by reconnecting the viewing key. Handle timeout errors by retrying with backoff. Handle subscription errors by reconnecting with appropriate delay.

Log errors for debugging but avoid exposing sensitive information such as viewing keys in logs. Use the `IndexerFormattedError` type to provide user-friendly error messages while preserving technical details for debugging.

### Reconnection Logic

WebSocket connections can drop due to network issues or server restarts. Implement reconnection logic that first attempts an immediate reconnect, then retries with exponential backoff starting at 1 second, capping at 30 seconds maximum delay, adding jitter to avoid thundering herd problems, and resetting the backoff on successful reconnection.

When reconnecting, re-establish any viewing key sessions by calling `connectWallet` again. Re-subscribe to all required subscriptions. Handle any events that may have been missed during the disconnection period by querying for recent data.

For HTTP queries, implement retry logic with exponential backoff for transient errors. Do not retry for authentication errors or validation errors. Retry up to 3 times before reporting a failure.

### Viewing Key Management

Store viewing keys securely. Never expose viewing keys in client-side code or network requests beyond the `connectWallet` mutation. Use short-lived sessions and reconnect when needed rather than maintaining long-lived sessions. Implement session expiration handling so the dApp can recover gracefully when a session expires.

Rotate viewing keys periodically as a security best practice. Different viewing keys can be used for different purposes to implement the principle of least privilege. A viewing key that only needs to see contract state for one contract should not have broader access.

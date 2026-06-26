# Midnight Indexer API Reference

## Overview

The Midnight Indexer exposes a GraphQL API at version 4 for querying and subscribing to blockchain data. The API provides access to blocks, transactions, contract actions, committee information, epoch data, D parameter history, staking information, and various ledger events. This document covers all query operations, subscription streams, mutations, type definitions, enums, scalars, unions, directives, and offset pagination mechanisms.

## Endpoint

The GraphQL endpoint is available at the configured indexer URL under the `/graphql` path. All operations use HTTP POST with a JSON body containing a `query`, optional `variables`, and optional `operationName` field. The endpoint also supports WebSocket connections for subscription operations using the same path. Authentication is managed through API keys passed in the `Authorization` header when required by the network tier.

## Query Operations

### Block Queries

The `block` query retrieves a single block by its hash or height. It returns block metadata including the timestamp, parent hash, and block producer identity. The `blocks` query supports list retrieval with filtering by height range, timestamp range, or producer identity.

### Transaction Queries

The `transaction` query looks up a single transaction by its identifier. It returns the transaction type, status, block reference, and associated contract calls. The `transactions` query supports filtering by status, sender, contract address, and time range.

### Contract Actions

The `contractAction` query retrieves a specific contract interaction by its action identifier. It returns the contract address, method called, input data reference, and output state changes. The `contractActions` query enables filtering by contract address, action type, and time range.

### Committee Information

The `committee` query returns the current epoch committee including all active members and their stake weights. The `currentEpochInfo` query provides the current epoch number, start height, remaining slots, and protocol parameters active for the current epoch.

### D Parameter Queries

The `dParameterHistory` query retrieves the historical values of the D parameter. Each entry includes the epoch number, the D value that was active, and the block height at which the value changed. This query supports filtering by epoch range.

### DUST Generation Status

The `dustGenerationStatus` query returns the current DUST generation state. It indicates whether DUST generation is active, the current generation rate, the accumulated DUST balance, and the remaining capacity for new generation requests.

### SPO Queries

The `spo` query retrieves a specific Stake Pool Operator by their identifier. It returns the pool metadata, total stake, delegation count, and performance statistics. The `spos` query supports filtering by active status and stake range.

The `stakeDistribution` query returns the distribution of stake across all active SPOs. Each entry includes the SPO identifier, total delegated stake, and percentage of total network stake controlled by the pool.

## Subscription Operations

### Block Subscriptions

The `blocks` subscription pushes new blocks as they are finalized. Each event includes the full block header and a summary of included transactions. Clients can filter by producer identity to receive only blocks from specific validators.

### Contract Action Subscriptions

The `contractActions` subscription streams contract interactions in real time. Events include the contract address, action type, timestamp, and transaction reference. Filtering is available by contract address and action type.

### Dust Ledger Events

The `dustLedgerEvents` subscription streams DUST generation and consumption events. Each event includes the event type, amount, associated account, and timestamp. This stream enables real time tracking of DUST token movements.

### Shielded Transactions

The `shieldedTransactions` subscription pushes transactions involving shielded token transfers. Events include encrypted payload references and zero knowledge proof identifiers. Actual shielded amounts are not visible in these events.

### Unshielded Transactions

The `unshieldedTransactions` subscription streams public token transfers. Events include sender, recipient, amount, fee, and timestamp. This provides full transparency for unshielded token operations.

### Zswap Ledger Events

The `zswapLedgerEvents` subscription streams zswap protocol state changes. Events include swap initiations, participant additions, proof submissions, and swap completions. Each event references the swap identifier and participating parties.

## Mutation Operations

### Connect

The `connect` mutation establishes a persistent authenticated session. It accepts an API key and returns a session token with an expiration time. Subsequent operations can use the session token for authentication.

### Disconnect

The `disconnect` mutation terminates an active session. It invalidates the session token and prevents further operations with that token. Disconnect should be called when clients complete their work with the indexer.

## Types

### Block

The Block type contains fields for `hash`, `height`, `parentHash`, `timestamp`, `producer`, `transactionCount`, and `stateRoot`. The `transactions` field resolves to a paginated list of transactions included in the block.

### Transaction

The Transaction type contains `id`, `status`, `type`, `block`, `sender`, `fee`, `contractCalls`, and `timestamp`. The status field uses the TransactionStatus enum to indicate pending, finalized, or failed states.

### ContractAction

The ContractAction type contains `id`, `contractAddress`, `actionType`, `blockHeight`, `transactionId`, and `timestamp`. The `inputReference` and `outputReference` fields provide pointers to the offchain stored input and output data.

### Committee

The Committee type contains `epoch`, `members`, and `totalStake`. Each member entry includes the SPO identifier, stake amount, and assigned slot ranges within the epoch.

### SPO

The SPO type contains `id`, `name`, `ticker`, `description`, `homepage`, `pledge`, `margin`, `fixedCost`, `totalStake`, `delegatorCount`, `activeStatus`, and `blockProductionStats`.

### StakeDistribution

The StakeDistribution type contains `spoId`, `stakeAmount`, and `percentageShare`. The percentage represents the share of total network stake held by the SPO including both self stake and delegated stake.

## Enums

### TransactionStatus

Values include `PENDING`, `FINALIZED`, and `FAILED`. Pending transactions are in the mempool or being processed. Finalized transactions have confirmed inclusion. Failed transactions were invalid or reverted.

### ContractActionType

Values include `DEPLOY`, `CALL`, and `ZK_VERIFY`. Deploy actions register new contracts on chain. Call actions execute contract methods. ZK verify actions submit zero knowledge proofs for private computation validation.

### EventType

Values include `CREATED`, `UPDATED`, and `DELETED`. These describe the nature of state changes emitted by contracts and runtime pallets.

## Scalars

The API defines custom scalars for blockchain specific types. The `Address` scalar represents a 32 byte account or contract address. The `Hash` scalar represents a 32 byte Blake2b hash. The `BigInt` scalar represents arbitrarily large integer values for token amounts and stake quantities. The `Timestamp` scalar represents Unix timestamps with millisecond precision.

## Unions

The `EventPayload` union combines `DustEvent`, `TokenEvent`, `ContractEvent`, and `ZswapEvent` types. Subscription handlers receive this union and discriminate by the `__typename` field to process specific event types.

## Directives

The `@skip` and `@include` directives control field inclusion based on boolean variables. These follow the standard GraphQL specification. The `@deprecated` directive marks fields scheduled for removal with a reason string.

## Offset Pagination

### BlockOffset

The BlockOffset type contains `height` and `hash` fields. Used as a cursor for block list queries. Subsequent queries use this offset to fetch the next page of results starting after the specified block.

### ContractActionOffset

The ContractActionOffset type contains `id` and `timestamp` fields. Used as a cursor for contract action list queries. Results are returned in chronological order after the specified offset.

### TransactionOffset

The TransactionOffset type contains `id` and `blockHeight` fields. Used as a cursor for transaction list queries. This offset based pagination avoids the performance issues of offset based pagination on large result sets.

### Offset Usage

Each list query returns a `pageInfo` object containing `hasNextPage` and an `endCursor`. Pass the `endCursor` as the `after` argument in subsequent queries to fetch subsequent pages. The page size is controlled by the `first` argument with a server enforced maximum.

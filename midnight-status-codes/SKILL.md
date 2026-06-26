---
name: midnight-status-codes
description: Error code catalog for Midnight Network. Use when looking up error codes, troubleshooting transaction failures, decoding LEDGER errors, identifying DApp Connector API errors, understanding Compact compiler errors, diagnosing proof server issues, interpreting Midnight.js errors, handling Indexer errors, decoding Substrate 1010 transaction rejection errors, implementing error handling patterns, managing retry strategies, classifying errors by severity, or escalating unresolved issues. Provides a comprehensive error reference across all Midnight components with structured lookup and resolution guidance.
---

# Midnight Status Codes

A comprehensive error code catalog for the Midnight Network. This skill covers error codes from all Midnight components with structured lookup patterns, severity classification, and resolution guidance.

## Error Code Overview

The Midnight Network produces errors across multiple independent components. Each component defines its own error types with unique characteristics. Understanding the error landscape is essential for effective debugging and robust application development.

The error catalog unifies error information from six primary sources: the Ledger, the Node runtime, the Wallet SDK, the DApp Connector API, the Compact Compiler and Runtime, and the Proof Server. Each source has its own error taxonomy and code ranges. Cross-referencing errors between components is often necessary because errors in one component frequently manifest as different errors in another.

When an error occurs the first step is always to identify which component produced the error. The error message, error code format, and the context in which the error occurred all provide clues. Once the component is identified the structured lookup tables in this catalog provide detailed information about the error meaning, severity, and resolution steps.

### Lookup Patterns

Errors follow predictable patterns that enable quick identification. Ledger errors contain Rust enum variant names. Node errors contain Substrate module indices. Wallet SDK errors contain JavaScript class names. DApp Connector errors contain integer codes from the ErrorCodes enum. Compact compiler errors contain file paths and line numbers. Proof server errors contain HTTP status codes. Recognizing these patterns speeds up diagnosis significantly.

### Troubleshooting Flow

The troubleshooting flow follows a systematic path from error observation to resolution. First capture the complete error message and any stack trace. Second identify the error source component using the pattern recognition rules. Third look up the error in the catalog tables. Fourth apply the recommended resolution steps for that error. Fifth if the error persists escalate to the next level of support with a full error report.

## Ledger Errors

The Midnight Ledger is implemented in Rust and uses Rust error types to communicate failures. Ledger errors cover transaction validation, execution, and state management.

### Transaction Validation Errors

Transaction validation errors occur before a transaction is executed. The ledger validates transaction structure, signatures, fee payment, and state access permissions. Validation errors prevent the transaction from being executed at all.

Common validation errors include `InvalidSignature` when the transaction signature does not match the signer, `InsufficientFunds` when the sender does not have enough balance to pay fees, `InvalidNonce` when the transaction nonce does not match the expected nonce, `BadProof` when the zero-knowledge proof attached to the transaction is invalid, `InvalidContractAddress` when the contract address in the transaction does not correspond to a deployed contract, and `ExpiredTransaction` when the transaction time to live has expired.

### Execution Errors

Execution errors occur during transaction execution. The transaction has been validated but fails while running. Execution errors may leave partial state changes depending on whether the circuit is guaranteed or fallible.

Common execution errors include `AssertionFailed` when a circuit assertion fails, `OutOfGas` when the transaction consumes more gas than allocated, and `StateConflict` when multiple transactions attempt to modify the same state simultaneously.

### State Management Failures

State management failures occur when the ledger cannot read or write contract state. These errors indicate problems with the underlying storage layer.

Common state errors include `StateNotFound` when the requested state does not exist for the contract, `StateReadError` when the ledger cannot read state from storage, and `StateWriteError` when the ledger cannot write updated state to storage.

### Ledger Error Codes

The ledger exposes error codes through transaction results. Each error code is an integer that maps to a specific error variant. The codes are defined in the ledger Rust source and are stable across ledger versions.

Error code 1000 indicates an invalid signature. Error code 1001 indicates insufficient funds. Error code 1002 indicates an invalid nonce. Error code 1003 indicates a bad proof. Error code 1004 indicates an invalid contract address. Error code 2000 indicates an assertion failure. Error code 2001 indicates out of gas. Error code 3000 indicates state not found.

## Node Errors

The Midnight Node is built on Substrate and inherits Substrate error handling patterns. Node errors cover P2P networking, consensus, storage, and RPC interfaces.

### Substrate Error Codes

Substrate modules each have an index and each index has error variants. The error is reported as a combination of the module index and the error variant index. The module index identifies which pallet produced the error. The error variant index identifies the specific error within that pallet.

### P2P Errors

P2P errors occur in the peer-to-peer networking layer. These errors typically indicate network connectivity problems. Common P2P errors include `ConnectionRefused`, `ConnectionTimeout`, `PeerNotFound`, and `BandwidthLimitExceeded`. Network errors often resolve themselves when connectivity is restored.

### Consensus Errors

Consensus errors occur during block production and finalization. These errors may indicate problems with validator configuration or network synchronization. Common consensus errors include `SlotMissed`, `DoubleVotingDetected`, and `FinalizationStalled`.

### Storage Errors

Storage errors occur when the node cannot read or write to its database. These errors may indicate disk problems, corruption, or insufficient space. Common storage errors include `DatabaseCorruption`, `DiskFull`, and `ReadOnlyDatabase`.

### RPC Errors

RPC errors occur when clients communicate with the node via the RPC interface. These errors follow the JSON-RPC error format with numeric codes. Common RPC errors include `MethodNotFound`, `InvalidParams`, `ParseError`, and `InternalError`.

### Network Errors

Network errors include DNS resolution failures, TLS certificate errors, and proxy configuration issues. These errors prevent the application from connecting to the Midnight Network at all. Network errors should be addressed before attempting to debug application-level errors.

## Wallet SDK Errors

The Wallet SDK is a TypeScript library that manages wallet connections, key management, and transaction signing. Wallet errors typically originate from user interaction or configuration issues.

### Connection Errors

Connection errors occur when the SDK cannot connect to a wallet provider. Common causes include the wallet extension not being installed, the wallet being locked, or the user rejecting the connection request. The error message indicates which specific failure occurred and often includes user-actionable instructions.

### Signing Errors

Signing errors occur when the SDK cannot sign a transaction. Common causes include the user rejecting the signing request, the wallet being disconnected, or the transaction being malformed. The SDK provides detailed error messages that help identify the root cause.

### State Errors

State errors occur when the wallet cannot retrieve contract state. Common causes include the contract not being deployed, the state being private and inaccessible to the wallet, or network connectivity issues preventing state retrieval.

### Key Management Errors

Key management errors occur when generating, storing, or retrieving cryptographic keys. These errors are critical because they affect the ability to sign transactions. Key management errors should be investigated immediately because they may indicate a security issue.

### DUST Errors

DUST errors occur when the wallet cannot generate or manage DUST tokens. DUST is required for transaction fees on Midnight. If the wallet cannot produce DUST transactions will fail with insufficient fee errors.

## DApp Connector API Errors

The DApp Connector API is the primary interface between dApps and Midnight wallets. It defines a standardized set of error codes for common failure scenarios.

### Connection Errors

The DApp Connector returns connection errors when the dApp cannot establish communication with the wallet. The `ConnectionError` type indicates that the wallet provider is not available. The `AuthorizationError` type indicates that the user denied the connection request. These errors include user-friendly messages suitable for display.

### Authorization Errors

Authorization errors occur when the user has not granted necessary permissions or when the authorization has expired. Common scenarios include the user denying a transaction or the connection timeout expiring. Authorization errors can be resolved by requesting authorization again or by the user changing their permission settings.

### Transaction Errors

Transaction errors occur during transaction construction and submission. The DApp Connector wraps lower-level errors from the wallet and ledger into standardized transaction error types. Transaction errors include the original error for debugging along with simplified messages for display.

### Proving Errors

Proving errors occur when the proof server cannot generate or verify a proof. These errors may indicate problems with the proof server configuration, the verifier key, or the contract itself. Proving errors are typically transient and can be resolved by retrying or by updating the proof server configuration.

### ErrorCodes Enum

The `ErrorCodes` enum defines the complete set of DApp Connector error codes. Each variant has a numeric code and a description. The enum is stable and new codes are added at the end to maintain backward compatibility.

### ErrorCode Type

The `ErrorCode` type is the numeric representation of an error from the ErrorCodes enum. Applications should compare against the enum variants rather than raw numbers for clarity and future compatibility.

### APIError Type

The `APIError` type is the structure returned by the DApp Connector when an error occurs. It contains the error code, a human-readable message, and optional detail fields with additional context. The APIError structure is designed to be both machine-parsable and human-readable.

## Compact Compiler Errors

The Compact compiler produces errors during contract compilation. Compiler errors are categorized by the compilation phase in which they occur.

### Lexer Errors

Lexer errors occur during the first phase of compilation when source text is tokenized. These errors are caused by invalid characters, unterminated strings, or other lexical-level issues. The error message includes the file path and the line and column where the invalid token was found.

### Parser Errors

Parser errors occur during syntax analysis when tokens are assembled into an abstract syntax tree. These errors are caused by syntax mistakes such as missing semicolons, unmatched brackets, or invalid expressions. The error message describes what the parser expected and what it found instead.

### Witness Errors

Witness errors occur during witness analysis when the compiler checks that witness data is used correctly. These errors may indicate missing witness validations, unused witness parameters, or circuit access to witness data without proper declaration.

### Disclosure Errors

Disclosure errors occur during disclosure analysis when the compiler checks that data is disclosed correctly. These errors may indicate disclosures of private data without proper wrapping, missing disclosures for required public outputs, or attempts to disclose data that does not exist.

### ZKIR Errors

ZKIR errors occur during intermediate representation generation. These errors may indicate that the contract logic cannot be expressed as a valid ZK circuit. Common ZKIR errors include unbounded loops, recursion, and unsupported operations.

### Runtime Errors

Runtime errors occur when the compiled contract is loaded and executed. These errors are not compilation errors but are closely related because they indicate that the compiler produced code that fails at runtime. Runtime errors should be reported to the compiler team for investigation.

### Type Errors

Type errors occur when the contract contains type mismatches. The Compact type system is strict and many errors are caught at compile time. Type errors include mismatched argument counts, incompatible type assignments, and invalid type constructions.

## Compact Runtime Errors

The Compact Runtime executes compiled contracts and produces runtime errors when execution fails.

### CompactError Class

The `CompactError` class is the base error type for all Compact Runtime errors. It contains a message describing the error and a code identifying the error type. Applications can catch CompactError to handle all runtime errors uniformly.

### type_error

The `type_error` variant indicates that a type check failed at runtime. This may occur when a contract receives input with an unexpected type. Type errors at runtime typically indicate a mismatch between the contract interface and the calling code.

### typeError

The `typeError` variant is a JavaScript-level type error that occurs when the runtime receives a value of an incorrect JavaScript type. These errors are distinct from Compact type errors and indicate integration issues between TypeScript code and the runtime.

### Runtime Assertion Errors

Runtime assertion errors occur when a circuit assertion fails during execution. Assertions are used to validate preconditions and invariants. An assertion failure indicates that a condition the contract assumed to be true was actually false.

## Proof Server Errors

The Proof Server generates and verifies zero-knowledge proofs. Proof server errors affect transaction submission because proofs are required for all transactions.

### Proving Errors

Proving errors occur when the proof server cannot generate a proof for a transaction. Common causes include incorrect circuit inputs, missing prover keys, or timeout during proof generation. The error response includes details about which circuit failed and why.

### Key Errors

Key errors occur when the proof server cannot find or use the verifier key for a contract. This may indicate that the verifier key has not been inserted or that the key is corrupted. Key errors prevent proof generation and verification for the affected contract.

### Timeout Errors

Timeout errors occur when proof generation exceeds the configured time limit. Large circuits may require more time than the default timeout allows. The timeout can be increased in the proof server configuration if needed.

### Configuration Errors

Configuration errors occur when the proof server is misconfigured. Common issues include incorrect network settings, missing environment variables, or incompatible versions of supporting software. Configuration errors are typically resolved by updating the proof server configuration.

### Server Errors

Server errors are internal errors in the proof server that cannot be attributed to a specific request. These errors should be reported to the proof server operators. The server may need to be restarted or upgraded to resolve the issue.

## Midnight.js Errors

Midnight.js is the TypeScript SDK for building Midnight dApps. It provides typed error classes for common failure scenarios.

### CallTxFailedError

The `CallTxFailedError` is thrown when a call transaction fails. This error wraps the underlying transaction failure and provides access to the transaction data. Applications should catch this error specifically when they need to handle call transaction failures differently from other errors.

### DeployTxFailedError

The `DeployTxFailedError` is thrown when a contract deployment transaction fails. This error includes information about the contract that could not be deployed and the reason for the failure. Developers should check for this error during contract deployment workflows.

### ContractTypeError

The `ContractTypeError` is thrown when there is a type mismatch between the TypeScript type definition for a contract and the actual contract interface. This error indicates that the contract descriptor is out of sync with the deployed contract.

### TxFailedError

The `TxFailedError` is a general transaction failure error that is thrown for any transaction type that fails. It is the parent class of more specific transaction error types. Applications can catch TxFailedError to handle all transaction failures generically.

### InsertVerifierKeyTxFailedError

The `InsertVerifierKeyTxFailedError` is thrown when a verifier key insertion transaction fails. This error includes the verifier key that was being inserted and the reason for the failure.

### RemoveVerifierKeyTxFailedError

The `RemoveVerifierKeyTxFailedError` is thrown when a verifier key removal transaction fails. This error includes the verifier key that was being removed and the reason for the failure.

### ReplaceMaintenanceAuthorityTxFailedError

The `ReplaceMaintenanceAuthorityTxFailedError` is thrown when a maintenance authority replacement transaction fails. This error includes the contract and the proposed new authority.

## Indexer Errors

The Midnight Indexer provides a GraphQL API for querying blockchain data. Indexer errors affect applications that read contract state or transaction history.

### Indexer Error Codes

The indexer returns GraphQL errors with standardized extensions that include the error code. These codes identify specific failure modes such as `INDEXER_UNAVAILABLE`, `QUERY_TIMEOUT`, `RATE_LIMIT_EXCEEDED`, and `INVALID_QUERY`. Each code maps to a specific resolution strategy.

### GraphQL Errors

GraphQL errors follow the GraphQL error specification with a message and optional extensions. The indexer extends this format with Midnight-specific error codes in the extensions field. Applications should inspect the extensions.code field to determine the specific error type.

### Connection Errors

Connection errors occur when the indexer endpoint cannot be reached. These errors have the same causes as general network errors and should be addressed with network diagnostics. Retry with backoff is the recommended recovery strategy.

### Subscription Errors

Subscription errors occur when a GraphQL subscription fails. Subscriptions can fail due to network interruptions, authorization changes, or server-side issues. Applications should implement reconnection logic for subscriptions that must remain active.

### IndexerFormattedError

The `IndexerFormattedError` type provides a structured representation of indexer errors that includes the error code, message, and any relevant metadata. This type is used internally by the indexer client to parse and categorize error responses.

## Transaction Result Status

Midnight transactions can have complex result statuses that go beyond simple success or failure. Understanding these statuses is essential for correct error handling.

### Success

A success status means the transaction completed successfully and all circuits executed without errors. State changes from the transaction are final and irreversible.

### Partial Success

A partial success status means some parts of the transaction succeeded while others failed. In a transaction with multiple circuits some may have executed successfully while others failed. State changes from successful circuits are applied and state changes from failed circuits are rolled back.

### Failure

A failure status means the transaction could not be executed. No state changes are applied. The transaction fee may still be consumed depending on when the failure occurred.

### SegmentSuccess

A `SegmentSuccess` variant indicates that a single circuit within a multi-circuit transaction succeeded. This is an internal status used for composite transactions.

### SegmentFail

A `SegmentFail` variant indicates that a single circuit within a multi-circuit transaction failed. The transaction processor uses this status to determine which state changes to apply and which to reverse.

### SucceedEntirely

A `SucceedEntirely` variant indicates that the entire transaction including all circuits completed successfully. This is the most desirable outcome.

### FailEntirely

A `FailEntirely` variant indicates that the entire transaction could not be executed. No circuits ran and no state was changed.

### FailFallible

A `FailFallible` variant indicates that a transaction with fallible circuits failed. Fallible circuits are designed to allow partial success so this status indicates that even the fallible aspects of the transaction could not be completed.

## Decoding 1010 Transaction Rejection Errors

Substrate uses error code 1010 to indicate that a transaction was rejected as invalid. This error code carries additional information that can be decoded to identify the underlying issue.

### Substrate Code 1010

Error code 1010 is the Substrate error code for "Invalid Transaction". When this error is returned the transaction was rejected before execution. The error includes a message from the transaction validation logic that explains why the transaction was rejected.

### Decode Inner u8

The inner u8 value of a 1010 error identifies the specific reason the transaction was rejected. Common values include 1 for "Cannot Pay Fees", 2 for "Bad Proof", and 3 for "Invalid Contract Address". Decoding this value provides immediate insight into the rejection reason.

### Identify Underlying LEDGER Error

The u8 value from the 1010 error maps to a specific Ledger error variant. By cross-referencing the u8 value with the Ledger error catalog the developer can identify exactly which validation rule was violated. This mapping is documented in the error reference tables below.

## Error Handling Patterns

Robust Midnight applications implement consistent error handling patterns that provide good user experience while preserving diagnostic information.

### Expected Errors vs Unexpected Errors

Errors are classified as expected or unexpected. Expected errors are those that the application anticipates and can handle gracefully such as insufficient funds or user rejection. Unexpected errors are those that should not occur in normal operation such as internal server errors or data corruption. Expected errors should produce user-friendly messages. Unexpected errors should be logged in detail and may trigger alerts.

### Retry Strategies

Many errors are transient and resolve themselves on retry. Network errors, timeout errors, and rate limit errors are all candidates for retry. The recommended retry strategy is exponential backoff with jitter. Start with a one second delay and double it on each subsequent retry up to a maximum of 30 seconds. Add random jitter to prevent thundering herd problems.

### Exponential Backoff

Exponential backoff is a retry strategy where the delay between retries increases exponentially. This gives the underlying issue time to resolve while preventing the application from overwhelming the network with retries. The delay formula is `min(base * 2^attempt, max_delay)` where base is 1000 milliseconds and max delay is 30000 milliseconds.

### Circuit Breakers

Circuit breakers prevent the application from repeatedly calling a failing service. When error rates exceed a threshold the circuit breaker opens and subsequent calls fail immediately without attempting the operation. After a timeout the circuit breaker half-opens and allows a test call. If the test succeeds the circuit closes and normal operation resumes. If the test fails the circuit opens again.

### Graceful Degradation

When a component fails the application should degrade gracefully rather than failing completely. For example if the indexer is unavailable the application can show a cached view of data rather than a blank screen. Graceful degradation maintains user experience while the underlying issue is being resolved.

## Error Code Lookup

The error code lookup system provides structured access to error information across all Midnight components.

### Structured Lookup by Component

Errors are organized by component with tables that map error codes to descriptions. To look up an error first identify the component from which it originated using the pattern recognition rules. Then find the code in that component's error table. The table entry provides the error description, severity classification, and resolution steps.

### Error Code to Description Mapping

Each error code maps to a concise description that explains what the error means. The descriptions are written for developers and include enough context to understand the error without consulting external documentation.

### Severity Classification

Errors are classified by severity into four levels. `Critical` errors require immediate attention because they indicate system failure or security issues. `High` severity errors prevent the current operation from completing but do not affect other operations. `Medium` severity errors indicate configuration issues or non-critical failures. `Low` severity errors are informational or indicate deprecated usage.

### Resolution Steps

Each error entry includes resolution steps that guide the developer from diagnosis to resolution. Steps are ordered starting with the most common fix. If the first step does not resolve the issue proceed to subsequent steps.

## Troubleshooting Guide

The troubleshooting guide provides structured diagnostic paths for common error scenarios.

### Common Error Scenarios

Frequently encountered error scenarios include "transaction rejected with code 1010", "proof server returning timeouts", "wallet connection always failing", "indexer returning empty results", and "contract deployment failing on preprod". Each scenario has a dedicated diagnostic flow.

### Diagnostic Steps

The diagnostic flow for each scenario follows a consistent pattern. First gather all available information about the error. Second verify that dependent services are running. Third check that configuration values are correct. Fourth test with a simpler operation to isolate variables. Fifth consult the specific error documentation.

### Resolution Paths

Each diagnostic flow ends with resolution paths that provide concrete actions to resolve the issue. Resolution paths include code changes, configuration updates, service restarts, or escalation to the appropriate team. Where possible resolution paths include example commands or code snippets.

### Escalation Criteria

Errors should be escalated when they cannot be resolved using the documented resolution paths. Escalation criteria include errors that persist after all resolution steps have been attempted, errors that affect multiple users, errors that involve security or fund safety, and errors that indicate possible bugs in Midnight software.

## Error Code Reference Tables

The reference tables provide a complete listing of error codes organized for efficient lookup.

### Grouped by Component

Error codes are grouped by the component that produces them. The Ledger section lists all Ledger error codes in order. The Node section lists Node error codes by pallet. The Wallet section lists Wallet error codes by category. The DApp Connector section lists all ErrorCodes enum values. The Compiler section lists compiler error types. The Proof Server section lists proof server error types. The Indexer section lists indexer error codes.

### Sorted by Severity

Error codes are also available sorted by severity so that the most critical errors can be addressed first. The severity sort places Critical errors first followed by High, Medium, and Low. Within each severity level errors are sorted alphabetically.

### Cross-Referenced with Documentation

Each error code entry includes references to relevant documentation sections where more detailed information can be found. Cross-references link error codes to the features or modules that produce them and to the resolution guides that explain how to fix them.

## Error Code Reference Tables by Component

The following tables provide detailed error code mappings for each Midnight component. Use these tables for precise error identification and resolution.

### Ledger Error Reference

The Ledger is the core state machine of Midnight. Its errors indicate fundamental problems with transaction validity or execution.

| Code | Name | Description | Severity | Resolution |
|------|------|-------------|----------|------------|
| 1000 | InvalidSignature | The transaction signature verification failed. The signer key does not match the signature data. | High | Verify the wallet is using the correct signing key. |
| 1001 | InsufficientFunds | The sender account does not have enough balance to cover the transaction fee. | High | Add funds to the sender account before retrying. |
| 1002 | InvalidNonce | The transaction nonce value is incorrect. This may indicate a replay attack or that another transaction from this account is pending. | High | Wait for pending transactions to clear or recalculate the correct nonce. |
| 1003 | BadProof | The zero-knowledge proof attached to the transaction is invalid. | Critical | Rebuild the proof with correct circuit inputs and verifier key. |
| 1004 | InvalidContractAddress | The contract address does not correspond to a deployed contract. | High | Verify the contract address and the target network. |
| 1005 | StaleTransaction | The transaction time-to-live expired before inclusion in a block. | Medium | Resubmit the transaction with a longer time-to-live. |
| 1006 | TransactionTooLarge | The transaction exceeds the maximum allowed size. | Medium | Reduce the size of data attached to the transaction. |
| 2000 | AssertionFailed | A circuit assertion evaluated to false during execution. | Critical | Review the circuit logic and the input values provided. |
| 2001 | OutOfGas | The transaction consumed more gas than its allocation. | High | Increase the gas limit or optimize the circuit for lower gas usage. |
| 2002 | StateAccessDenied | The circuit attempted to access state that it does not have permission to access. | Critical | Review the circuit state access declarations. |
| 3000 | StateNotFound | The requested contract state does not exist. | High | Verify the contract has been deployed and initialized. |
| 3001 | StateReadError | The ledger encountered an internal error while reading state. | Critical | Report to network operators for investigation. |
| 3002 | StateWriteError | The ledger encountered an internal error while writing state. | Critical | Report to network operators for investigation. |
| 4000 | MaintenanceUnauthorized | The transaction attempted a maintenance operation without proper authorization. | High | Verify that the maintenance authority signature is correct. |

### DApp Connector Error Code Reference

The DApp Connector defines a comprehensive set of error codes covering wallet interactions. Each code maps to a specific failure scenario.

| Code | Name | Description |
|------|------|-------------|
| 1 | CONNECTION_REFUSED | The wallet provider refused to establish a connection. The user may have dismissed the connection dialog. |
| 2 | CONNECTION_TIMEOUT | The connection request timed out before receiving a response from the wallet. |
| 3 | WALLET_NOT_INSTALLED | No Midnight wallet extension was detected in the browser. |
| 4 | WALLET_LOCKED | The wallet is locked and requires user authentication before use. |
| 5 | SIGNING_REFUSED | The user refused to sign the transaction in the wallet dialog. |
| 6 | SIGNING_TIMEOUT | The signing request timed out waiting for user approval. |
| 7 | INVALID_TRANSACTION | The transaction was rejected as invalid by the ledger. Check the nested error for details. |
| 8 | PROOF_GENERATION_FAILED | The proof server could not generate a proof for the transaction. |
| 9 | NETWORK_MISMATCH | The wallet is connected to a different network than the dApp expects. |
| 10 | UNSUPPORTED_OPERATION | The wallet does not support the requested operation. |
| 11 | INTERNAL_ERROR | An unexpected internal error occurred in the wallet or connector. |
| 12 | INSUFFICIENT_DUST | The account does not have enough DUST tokens to pay for the transaction. |

### Compact Compiler Error Reference

Compiler errors prevent contract compilation and must be fixed before deployment. Each error type corresponds to a specific compilation phase.

| Phase | Error Type | Description |
|-------|-----------|-------------|
| Lexer | UnterminatedString | A string literal was opened but never closed with a matching quote. |
| Lexer | InvalidCharacter | The source contains a character that is not valid in Compact syntax. |
| Lexer | NumericOverflow | A numeric literal exceeds the maximum value for its type. |
| Parser | UnexpectedToken | The parser encountered a token it did not expect at this position. |
| Parser | MissingSemicolon | A statement is missing its terminating semicolon. |
| Parser | UnmatchedBracket | Opening and closing brackets do not match. |
| Witness | MissingWitnessValidation | A circuit uses witness data without validating it. |
| Witness | UnusedWitnessParameter | A witness parameter is declared but never used in the circuit. |
| Disclosure | MissingDisclosure | A value must be disclosed but no disclose call exists for it. |
| Disclosure | InvalidDisclosure | A disclose call references data that does not exist or cannot be disclosed. |
| ZKIR | UnboundedLoop | The circuit contains a loop that cannot be bounded at compile time. |
| ZKIR | RecursiveCall | The circuit contains a recursive function call which is not supported. |
| Type | TypeMismatch | A value of one type is used where a different type is expected. |
| Type | MissingReturn | A circuit is declared to return a value but does not have a return statement. |

## Maintaining Error Code Documentation

### Updating Error Catalogs

Error catalogs should be updated whenever a new Midnight component release introduces new error codes or changes existing ones. The update process involves reviewing release notes and changelogs, identifying new or changed error codes, updating the catalog tables, and publishing the updated catalog with the next skills release.

### Version-Tagging Error Definitions

Each error code entry should indicate which version of the component introduced or last modified the error. Version tags help developers determine whether an error they are seeing is expected for their installed version. Errors introduced in newer versions may not appear in older installations.

### Community Contributions

Error catalog improvements are welcome from the Midnight developer community. Developers who encounter errors not yet documented can contribute descriptions, severity assessments, and resolution steps. Contributions should include the full error context including component, version, and reproduction steps.

### Testing Against Live Errors

Error catalogs should be periodically validated against live Midnight environments. Test transactions designed to trigger specific errors verify that error codes and messages have not changed. Automated testing can catch drift between the documented errors and actual runtime behavior.

## Best Practices

### Error Handling in DApps

DApps should handle errors at multiple levels. At the API level catch specific error types and convert them to user-friendly messages. At the UI level display error messages with appropriate severity styling. At the infrastructure level log errors with full context for debugging. Implement retry logic for transient errors and circuit breakers for persistent failures.

### Logging Strategies

Error logs should include the error type, error message, timestamp, user context, and any relevant transaction or contract identifiers. Logs should be structured in a machine-readable format for aggregation and analysis. Sensitive data such as private keys or user secrets should never be logged.

### User-Facing Error Messages

User-facing error messages should explain what happened and what the user can do about it. Messages should be concise, use plain language, and avoid technical jargon. For example instead of "ECDSA signature verification failed" show "The transaction could not be verified. Please try again or contact support if the problem continues."

### Monitoring and Alerting

Error rates should be monitored in production and alerted on when they exceed thresholds. Critical errors should trigger immediate alerts. High severity errors should be reviewed daily. Monitoring should track error rates by type, by user, and by component to identify patterns and emerging issues.

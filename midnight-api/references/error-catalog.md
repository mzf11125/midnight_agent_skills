# Unified Error Code Catalog

Complete error reference across all Midnight components with severity classification and resolution guidance.

## Ledger Errors

### Transaction Validation Errors

`LEDGER_001` Invalid transaction format. The submitted transaction bytes do not conform to the expected encoding. Severity: error. Resolution: verify the transaction is constructed using the SDK transaction builder rather than manually assembled.

`LEDGER_002` Insufficient funds. The sender account balance is below the required amount for the transaction fee plus transfer value. Severity: error. Resolution: ensure the wallet has sufficient NIGHT tokens and DUST for the operation.

`LEDGER_003` Nonce mismatch. The transaction nonce does not match the expected account nonce. Severity: error. Resolution: fetch the current account nonce from the indexer and rebuild the transaction.

`LEDGER_004` Signature verification failed. The transaction signature does not validate against the declared public key. Severity: error. Resolution: confirm the signing key matches the wallet address and that the transaction payload has not been modified after signing.

### Execution Errors

`LEDGER_010` Proof verification failed. The ZK proof attached to the transaction does not satisfy the verifier key constraints. Severity: error. Resolution: regenerate the proof using the correct prover key and verify the circuit inputs match the transaction data.

`LEDGER_011` State transition rejected. The circuit execution produced an invalid state transition per the contract rules. Severity: error. Resolution: check circuit preconditions and ensure the input witnesses produce a valid state change.

`LEDGER_012` Gas limit exceeded. The transaction consumed more gas than the specified limit. Severity: error. Resolution: increase the gas limit or optimize the circuit to reduce constraint count.

### State Management Errors

`LEDGER_020` Ledger read out of bounds. A circuit attempted to read from a ledger key that has not been initialized. Severity: error. Resolution: ensure the ledger key is written before it is read or add a default value initialization step.

`LEDGER_021` Ledger write conflict. Two circuits in the same block attempted to write to the same ledger key. Severity: error. Resolution: restructure the contract to avoid concurrent writes to shared state or use an ordered execution pattern.

`LEDGER_022` Contract not found. The referenced contract address does not exist on chain. Severity: error. Resolution: verify the contract address is correct and the contract has been deployed to the target network.

## Wallet Errors

### Connection Errors

`WALLET_001` Wallet not connected. An operation requiring a wallet was called before connecting. Severity: error. Resolution: call the wallet connect method and wait for the user to approve the connection before proceeding.

`WALLET_002` Network mismatch. The wallet is connected to a different network than the DApp expects. Severity: warning. Resolution: prompt the user to switch networks or configure the DApp to support the current network.

`WALLET_003` Wallet locked. The wallet is in a locked state and requires user authentication. Severity: warning. Resolution: prompt the user to unlock the wallet via password or biometric authentication.

### Signing Errors

`WALLET_010` User rejected signature. The user declined the transaction signing request. Severity: info. Resolution: no action required but the DApp should handle this gracefully by resetting the transaction UI state.

`WALLET_011` Signing timeout. The signing request timed out waiting for user approval. Severity: warning. Resolution: retry the signing request and inform the user that the previous attempt expired.

### State Errors

`WALLET_020` Key not found. The requested key is not present in the wallet keystore. Severity: error. Resolution: verify the key path or address is correct and that the key was previously generated or imported.

`WALLET_021` Keystore corrupted. The wallet keystore file is unreadable or has invalid structure. Severity: error. Resolution: restore the wallet from the backup mnemonic phrase using the wallet recovery flow.

### DUST Errors

`WALLET_030` Insufficient DUST. The wallet does not have enough DUST tokens to pay for the transaction. Severity: error. Resolution: initiate a DUST generation request through the DUST wallet or faucet.

`WALLET_031` DUST generation failed. The automated DUST generation process did not complete successfully. Severity: warning. Resolution: retry DUST generation or request DUST manually from the network faucet.

## DApp Connector Errors

### ErrorCodes Enum

The DApp Connector defines error codes as a typed enumeration in the SDK.

`APIError.NetworkError` A network request to the wallet or node failed. Severity: error. Resolution: check network connectivity and endpoint URLs.

`APIError.ConnectionRejected` The user declined the wallet connection request. Severity: info. Resolution: respect the user choice and offer a manual connect button.

`APIError.UnsupportedMethod` The requested wallet method is not supported by the connected wallet. Severity: error. Resolution: check wallet compatibility and use only methods listed in the wallet capability advertisement.

`APIError.InvalidParams` The parameters passed to a wallet method are malformed or out of range. Severity: error. Resolution: validate parameters against the method documentation before calling.

`APIError.InternalError` An unexpected error occurred inside the wallet or connector. Severity: error. Resolution: log the error details and retry the operation. Report the error if it persists.

## Compact Compiler Errors

### Lexer Errors

`COMPILE_001` Unexpected character. The lexer encountered a character that is not valid in any Compact token. Severity: error. Resolution: remove or replace the unexpected character at the indicated position.

`COMPILE_002` Unterminated string literal. A string started with a quote but was not closed before the line end. Severity: error. Resolution: add the closing quote to the string.

`COMPILE_003` Invalid number format. A numeric literal uses unsupported syntax. Severity: error. Resolution: use standard decimal or hexadecimal integer notation.

### Parser Errors

`COMPILE_010` Unexpected token. The parser found a token that does not fit the expected grammar production. Severity: error. Resolution: check the surrounding syntax and ensure keywords and operators are used in valid positions.

`COMPILE_011` Missing semicolon. A statement is missing its terminating punctuation. Severity: error. Resolution: add the required token at the end of the statement.

### Witness Errors

`COMPILE_020` Undeclared witness. A circuit references a witness that is not declared in the witness block. Severity: error. Resolution: add the witness declaration or fix the witness name typo.

`COMPILE_021` Witness type mismatch. A witness is used with an incompatible type in its usage context. Severity: error. Resolution: align the witness declaration type with the usage site expectation.

### Disclosure Errors

`COMPILE_030` Cannot disclose private field. A field marked as private in the ledger declaration is being disclosed in a circuit. Severity: error. Resolution: either remove the disclosure or change the ledger field visibility to public.

`COMPILE_031` Disclosure type violation. The disclosed field type does not support disclosure due to privacy constraints. Severity: error. Resolution: restructure the data so that only permitted fields are disclosed.

### ZKIR Errors

`COMPILE_040` Constraint system overflow. The generated constraint system exceeds the maximum supported size. Severity: error. Resolution: reduce circuit complexity by splitting into multiple smaller circuits.

`COMPILE_041` Unsupported operation. The circuit uses an operation that cannot be expressed in the ZKIR target. Severity: error. Resolution: replace the operation with an equivalent supported operation or restructure the circuit logic.

## Compact Runtime Errors

### CompactError

`RUNTIME_001` Circuit panic. A circuit assertion failed during proof generation. Severity: error. Resolution: verify the circuit preconditions are satisfied by the input witnesses.

`RUNTIME_002` Type mismatch at runtime. The actual value type does not match the expected type in the circuit. Severity: error. Resolution: ensure witnesses and ledger readings produce values of the declared types.

### TypeError

`RUNTIME_010` Invalid cast. An attempted type conversion is not permitted between the source and target types. Severity: error. Resolution: use an explicit conversion function that handles the type transformation correctly.

`RUNTIME_011` Overflow. An arithmetic operation produced a result exceeding the type maximum value. Severity: error. Resolution: use a larger integer type or add overflow guards to the circuit.

## Proof Server Errors

`PROOF_001` Prover key not found. The prover key for the requested contract is not loaded on the proof server. Severity: error. Resolution: upload the prover key to the proof server or verify the contract address is correct.

`PROOF_002` Proof generation timeout. The proof generation exceeded the configured time limit. Severity: warning. Resolution: increase the proof server timeout setting or reduce circuit complexity.

`PROOF_003` Proof queue full. The proof generation queue has reached maximum capacity. Severity: warning. Resolution: scale the proof server horizontally or add rate limiting to the DApp to reduce proof generation demand.

## Indexer Errors

`INDEX_001` Block indexing lag. The indexer has fallen more than 10 blocks behind the chain tip. Severity: warning. Resolution: check indexer resource allocation (CPU, memory, disk I/O) and network connectivity to the node.

`INDEX_002` GraphQL query timeout. An indexer query exceeded the configured execution time limit. Severity: warning. Resolution: add query filters to reduce the result set size or paginate the query with smaller page sizes.

`INDEX_003` Schema mismatch. The indexer GraphQL schema does not match the expected contract schema. Severity: error. Resolution: restart the indexer with the updated contract ABI or check that the correct contract version is deployed.

## Transaction Result Statuses

`TX_SUCCESS` The transaction was accepted and executed successfully. No errors.

`TX_REJECTED_INVALID_FORMAT` The transaction bytes could not be deserialized. Equivalent to LEDGER_001.

`TX_REJECTED_INSUFFICIENT_FUNDS` The transaction sender lacks funds. Equivalent to LEDGER_002.

`TX_REJECTED_BAD_SIGNATURE` The transaction signature is invalid. Equivalent to LEDGER_004.

`TX_REJECTED_PROOF_VERIFICATION_FAILED` The attached ZK proof is invalid. Equivalent to LEDGER_010.

`TX_PENDING` The transaction has been submitted but not yet included in a block. This is not an error but a transitional status.

## Decoding 1010 Transaction Rejection

The 1010 error code indicates a generic transaction rejection. The specific reason is embedded in the error details field as a sub-code.

Decoding procedure: parse the error JSON from the node response, extract the `details.module` field to identify the rejecting component, extract the `details.index` field as the sub-code, and cross reference with the relevant component error table above.

Example: a 1010 rejection with module `ledger` and index `003` corresponds to LEDGER_003 (nonce mismatch).

## Error Lookup by Component

Each error code follows the pattern `COMPONENT_NNN` where the component prefix identifies the source. Ledger errors use the LEDGER prefix and codes 001 through 099. Wallet errors use WALLET and codes 001 through 099. Compiler errors use COMPILE and codes 001 through 099. Runtime errors use RUNTIME and codes 001 through 099. Proof server errors use PROOF and codes 001 through 099. Indexer errors use INDEX and codes 001 through 099.

For severity classification: error severity means the operation cannot proceed and requires a code or configuration change. Warning severity means the operation may proceed after a retry or user action. Info severity means the condition is expected and requires only UI handling.

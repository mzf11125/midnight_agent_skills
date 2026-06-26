# Verification Methods

Multi method verification framework for Compact contracts and Midnight DApp deployments.

## Overview

The verification framework applies five independent verification layers to each contract. Each layer catches different classes of issues. Running all five layers provides high confidence that a contract is correct and safe before mainnet deployment.

## Compile Verification

### compactc Success Check

The first and simplest verification confirms that `compactc` exits with code 0 for the contract source. A failing compilation indicates syntax errors, type mismatches, or unsupported language features. The verification captures the full compiler output including warnings.

### ZKIR Validation

After successful compilation the generated ZKIR artifact is validated for structural correctness. The ZKIR JSON is parsed and checked for required top level fields including circuits, variables, constraints, and disclosure. Each circuit entry is verified to have a valid constraint array and variable declarations. Missing or malformed sections indicate a compiler bug or output corruption.

### Constraint Bounds

The verification compares the constraint count per circuit against the declared budget. If a circuit exceeds the budget the verification flags it with a warning. Budget overruns are acceptable during development but must be resolved before production deployment to keep proof generation times predictable.

## Execute Verification

### runProgram Integration

The verification invokes `runProgram` from the midnight testkit to execute each circuit against a set of test inputs. The execution produces `VmResults` containing the circuit output, gas consumption, and any execution errors. Successful execution confirms the ZKIR is runnable by the proof server.

### VmResults Analysis

Each VmResult is inspected for three properties. The exit code must be zero. The return value must match the expected output for the test case. The gas consumed must fall within acceptable bounds. Deviations in any property indicate a circuit logic error or unexpected computational cost.

### VmStack Inspection

For circuits that produce errors the VmStack trace is analyzed to identify the failing instruction. Common failure modes include assertion violations from failed precondition checks, arithmetic overflow from unchecked operations, and out of bounds accesses from invalid ledger reads. The stack trace provides the instruction pointer and operand values at the failure point.

## Type Check Verification

### CompactType Checks

The verification extracts type information from the compiler output and validates type consistency across all circuits. Each witness declaration is checked to match its usage sites. Each ledger read is checked to match the declared ledger type. Type mismatches are reported with the expected type and the actual type found.

### Descriptor Validation

Ledger descriptor types are validated against their usage context. A descriptor used for reading in one circuit and writing in another must support both operations. Descriptors with incompatible access patterns are flagged for restructuring.

## Source Inspection

### Disclosure Audit

The verification scans the contract source for all `disclose` statements and produces a disclosure map. The map lists each disclosed field with its type, the circuit that discloses it, and the visibility constraint applied. Reviewers use this map to verify that no sensitive data is unintentionally disclosed to public observers.

### Privacy Leak Detection

An automated privacy leak detector analyzes the disclosure map against the ledger state declarations. It flags fields where a private ledger value is disclosed without a corresponding commitment transformation. It also flags circuits where the disclosure reveals more information than the stated privacy policy allows. Each flag includes the file location and a suggested fix.

## E2E Testing

### Full Deploy and Call Cycle

The E2E verification deploys the contract to a local devnet instance and executes a complete lifecycle. The cycle includes wallet initialization, DUST generation, contract deployment, proof server registration, circuit call submission, transaction confirmation polling, and ledger state verification via the indexer. A passing E2E cycle confirms the contract works in a realistic network environment.

### Devnet Environment

The local devnet is provisioned using Docker Compose with the Midnight local dev stack. The environment includes a block producing node, proof server, and indexer. The verification waits for all services to report healthy before beginning the test cycle.

## Contract Specification Mapping

The verification framework maps each contract function to one or more verification claims. The mapping is stored alongside the contract source in a claims file that the verification runner reads at startup. Claims are tagged by category: functional for behavior assertions, security for access control and privacy, performance for gas and constraint budgets, and integration for cross-contract interactions. Each claim references the specific circuit name and a human readable description of the expected behavior.

## Claim Extraction and Structured Verification Flow

### Claim Extraction

The verification begins by extracting claims from the contract specification or developer annotations. Each claim describes a property the contract must satisfy such as "only the owner may call the mint circuit" or "the total supply equals the sum of all balances". Claims are parsed into a structured format with a description, the circuit or circuits involved, and the expected behavior.

### Structured Flow

The verification flow proceeds in five ordered stages. Stage one runs compile verification and blocks further stages if compilation fails. Stage two runs type check verification and source inspection in parallel. Stage three runs execute verification on all circuits with test inputs. Stage four runs E2E testing on the contracts that passed earlier stages. Stage five produces a combined report with per-claim status, per-stage results, and an overall pass or fail verdict.

### Report Output

The verification report is produced in markdown format by default. Each claim appears as a row with its verification status. Each stage appears as a section with summary statistics. Failures include detailed diagnostics with file locations and remediation guidance. The report concludes with a confidence score from 0 to 100 reflecting the fraction of claims that passed all applicable verification stages.

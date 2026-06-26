# Tutorial Contract References

Documentation driven tutorial contracts demonstrating Midnight Compact patterns and privacy capabilities.

## Battleship

A two player naval combat game that mixes public and private state on the blockchain.

### Architecture

Each player places ships on a private grid represented as committed coordinates. The circuit verifies that a guessed coordinate hits or misses without revealing ship positions. A public turn counter and game phase enum track progress visible to both players.

### State Machine

The game transitions through Setup, Player1Turn, Player2Turn, and GameOver phases. Each transition validates that the calling player matches the current turn. The circuit consumes the previous state hash and emits a new state hash after the move processes.

### Key Learning Outcomes

Understand how public and private state coexist in a single contract. Learn when to use commitments for hidden data versus plain ledger storage for shared game state. Practice turn enforcement through phase guards.

## Bulletin Board

A privacy preserving message posting system with optional ZK identity verification.

### Posting Flow

Any user may post a message to the board. The message content is stored as a commitment on chain while the plaintext passes through the circuit witness. An optional signature field allows the poster to prove ownership of a specific identity without revealing it.

### ZK Identity Verification

The contract supports a verifyPoster circuit that proves a message was posted by a given identity. The circuit checks that the posted commitment opens to a message signed by the claimed key. Verifiers learn only the outcome of the check, not the underlying key material.

### Privacy Preserving Design

Messages never appear in plaintext on the ledger. Indexer queries return only commitments and timestamps. The disclosure policy determines which fields the poster chooses to make public at submission time.

### Key Learning Outcomes

Work with commitments and openings as the primary data hiding mechanism. Apply selective disclosure to let users control which fields are visible. Build verifiable proofs about private data without exposing the data itself.

## ZK Loan

A decentralized lending contract using Schnorr attestations for credit privacy.

### Credit Attestation Model

A trusted attestor issues Schnorr signatures over a borrower credit score. The borrower presents this attestation as a circuit witness without revealing the raw score. The contract verifies the attestor signature and checks that the score exceeds a threshold before approving the loan.

### Loan Lifecycle

The contract tracks loan principal, interest rate, collateral, and repayment deadline in public ledger state. The borrower deposits collateral, receives the loan amount, and must repay before the deadline or face liquidation. Each state change requires a valid borrower or liquidator witness.

### Privacy Preserving Credit

The borrower credit score never appears on chain. The attestor issues one signature per borrower and the circuit proves the score satisfies the threshold without revealing the exact number. This preserves borrower privacy while maintaining lender confidence in creditworthiness.

### Key Learning Outcomes

Integrate Schnorr signature verification inside a Compact circuit. Design privacy preserving credential systems where attestations prove properties about hidden values. Manage collateralized positions with automated state transitions.

## Leaderboard

A score tracking contract demonstrating privacy modes and ownership.

### Scoring Mechanism

Players submit scores as circuit transactions. The contract stores scores in a sorted data structure on chain. A player witness ensures each submission corresponds to the claimed identity.

### Privacy Modes

Three visibility modes control score exposure. Public mode stores scores directly on the ledger. Pseudonymous mode stores a commitment to the player identity with the score. Private mode stores only a nullifier proving the score was submitted without linking it to any identity. Users select their mode at submission time.

### Ownership Proof

The proveOwnership circuit verifies that a given nullifier corresponds to a specific player. This supports prize claims where winners must prove they submitted a particular score without revealing their other game activity.

### Key Learning Outcomes

Implement multiple privacy tiers in a single contract. Use nullifiers to enable anonymous submissions with optional identity linking later. Manage sorted on-chain data structures inside ZK circuits.

## Private Party

A privacy boundary demonstration showing how data stays within authorized groups.

### Party Membership

A party creator deploys the contract and manages a member list stored as a `Map<Bytes, Bool>`. Only members may read or write party state. A member witness gates all circuits.

### Shared State

Party members share a list of items each member plans to bring. The circuit allows adding, removing, and viewing items. Non-members cannot read the list because the circuit rejects their witness. The disclosure policy further restricts what external observers can see.

### Boundary Enforcement

The contract demonstrates the privacy boundary at two layers. The circuit layer rejects unauthorized witnesses. The disclosure layer prevents indexer visibility of party data for non-members. Together they create a confidentiality zone around the party group.

### Key Learning Outcomes

Define and enforce privacy boundaries through member lists. Combine circuit level access control with disclosure policy restrictions. Build collaborative applications where data is visible only to authorized participants.

## Calculator

A simple arithmetic contract demonstrating basic Compact math operations.

### Operations

The contract exposes add, subtract, multiply, and divide circuits. Each circuit takes two operands and returns the result. Division includes a zero check assertion. The contract stores the last computed result in a ledger cell.

### Circuit Structure

Each operation follows the same pattern. Receive operand witnesses, perform the arithmetic operation in the guaranteed phase, write the result to ledger state, and disclose the output. The straightforward design makes it easy to study circuit anatomy.

### Key Learning Outcomes

Write basic Compact arithmetic circuits. Understand the guaranteed versus fallible phase split. Learn how to declare witnesses, read and write ledger state, and control disclosure.

## Summary

Each tutorial contract isolates a specific concept or pattern. Battleship teaches state machines with mixed visibility. Bulletin Board demonstrates commitment based privacy. ZK Loan shows attestation integration. Leaderboard explores privacy modes. Private Party illustrates privacy boundaries. Calculator provides the minimal circuit template. Study them in this order for a progressive learning path from basic syntax to advanced privacy patterns.

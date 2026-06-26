# Zero-Knowledge Proofs on Midnight

## Overview

Zero-knowledge proofs (ZKPs) are the cryptographic foundation of privacy on Midnight. A ZKP allows one party (the prover) to convince another party (the verifier) that a statement is true without revealing any information beyond the truth of the statement itself. On Midnight, this means a user can prove they followed the rules of a contract without revealing their private inputs.

## Fundamentals of Zero-Knowledge Proofs

A zero-knowledge proof system must satisfy three properties.

### Completeness

If the statement is true and both parties follow the protocol honestly, the verifier will accept the proof. A correctly constructed proof of a valid computation will always pass verification.

### Soundness

If the statement is false, no prover (even a malicious one) can convince an honest verifier to accept the proof, except with a negligibly small probability. This property ensures that invalid computations cannot be passed off as valid.

### Zero-Knowledge

The verifier learns nothing beyond the truth of the statement. Even after seeing the proof and interacting with the prover, the verifier cannot extract any information about the prover's private inputs. This is the property that gives zero-knowledge proofs their name and enables privacy on Midnight.

## zkSNARKs on Midnight

Midnight uses zkSNARKs, a specific type of zero-knowledge proof with desirable properties for blockchain applications.

### What SNARK Stands For

SNARK is an acronym for Succinct Non-interactive Argument of Knowledge. Each word describes an important property.

Succinct means the proof is small (a few hundred bytes) and fast to verify (a few milliseconds). This is critical for blockchain use because proofs must be stored on chain and verified by every validator.

Non-interactive means the prover creates the proof without any back-and-forth communication with the verifier. The prover produces a single proof message, and anyone can verify it independently. This fits the blockchain model where provers and validators do not interact directly.

Argument means the proof provides computational soundness rather than unconditional soundness. The security relies on cryptographic assumptions about the hardness of certain mathematical problems (specifically, the hardness of computing discrete logarithms in certain elliptic curve groups).

Of Knowledge means the proof demonstrates that the prover actually knows the private inputs, not just that the statement happens to be true. This prevents certain types of attacks where a prover might construct a proof without knowing the underlying data.

### KZG-Based SNARKs

Midnight's zkSNARK construction uses the KZG polynomial commitment scheme (also known as the Kate commitment scheme). KZG commitments are homomorphic, meaning they support operations on committed values without opening the commitments. This enables efficient proof construction and compact proof sizes.

The specific proving system used on Midnight is a variant of PLONK or a similar universal setup scheme. The universal setup means the same trusted setup can be used for many different circuits, avoiding the need for a new setup ceremony for each application.

## Circuits and Witnesses

### What Is a Circuit

A circuit is a mathematical representation of a computation. It consists of gates connected by wires, where each gate performs a simple operation (addition or multiplication over a finite field). Complex computations are broken down into sequences of these simple operations.

In Midnight, the Compact compiler translates Compact source code into an arithmetic circuit. Each constraint in the Compact code becomes a set of gates and wires in the circuit. The resulting circuit defines exactly what the prover must prove.

### The Witness

The witness is a set of values that satisfy all the constraints of the circuit. It includes both public inputs (values visible to validators) and private inputs (values known only to the prover). The prover constructs the witness by assigning concrete values to every wire in the circuit such that all gate constraints are satisfied.

For a simple example, consider a circuit that checks whether the prover knows x such that x squared equals y (where y is public). The public input is y. The private witness is x. The circuit defines multiplication gates that compute x times x and constrain the result to equal y.

### Circuit Satisfaction

A circuit is satisfied when there exists an assignment of values to all wires such that the output of every gate matches its inputs according to the gate's operation. Proving circuit satisfaction is equivalent to proving that the private computation was performed correctly.

## Proof Generation Flow

Midnight's proof generation follows a three-step process.

### Step One: Create Unproven Transaction

The local component constructs an unproven transaction. This step gathers all the inputs needed for the proof: public inputs from the contract's replicated component, private witness data from private state providers and the user's wallet, and the circuit definition from the compiled contract.

The unproven transaction is a data structure that contains everything the prover needs. It includes the circuit identifier, the public inputs, the private witness values, and metadata about the transaction (such as fees and the target contract).

### Step Two: Prove

The proving engine takes the unproven transaction and produces a ZK proof. This is the computationally intensive step. The proving engine converts the circuit constraints into a polynomial identity, constructs a proof polynomial using the witness values, and generates the final proof using the KZG polynomial commitment scheme.

Proof generation happens entirely off chain on the user's machine. The time required depends on the circuit complexity and the user's hardware. Simple circuits might prove in under a second. Complex circuits with many constraints might take several seconds or longer.

The proving engine outputs a proof (a small set of group elements) and the public inputs. The private witness values are discarded after proving. They exist only in the proving engine's memory during generation and never leave the user's machine.

### Step Three: Verify

The user submits the proof and public inputs to the network as part of a transaction. Validators verify the proof using the public inputs and the circuit's verification key. Verification is fast and deterministic. Every validator seeing the same proof and public inputs will reach the same verification decision.

If verification succeeds, the transaction is valid, and the replicated component can proceed with any public state changes that depend on the proof. If verification fails, the transaction is rejected and has no effect on state.

## Privacy and Verifiability

The key insight of zero-knowledge proofs on Midnight is that privacy and verifiability are not opposing goals. They are simultaneously achievable through the ZK proof architecture.

### How Privacy Is Achieved

The witness (which contains private data) is never sent to validators. Only the proof is sent. The zero-knowledge property ensures that the proof reveals nothing about the witness beyond what is placed in the public disclosure. Validators can verify that the computation was correct without ever seeing the private inputs.

### How Verifiability Is Achieved

The soundness property ensures that if a transaction includes a valid proof, the underlying computation genuinely followed the circuit constraints. Validators do not need to trust the prover. They verify the proof against the circuit's verification key and the public inputs. A malicious prover cannot create a valid proof for an invalid computation.

### The Dual Guarantee

Together, these properties give Midnight its fundamental dual guarantee. For every private computation, validators learn only what the contract author chose to disclose through the disclosure mechanism. And validators can be certain that the private computation satisfied all the rules defined in the circuit. Privacy for the user, verifiability for the network.

## Performance Considerations

ZK proof generation is computationally expensive. The cost scales with circuit size, measured by the number of multiplication gates. Compact contract authors should be aware of circuit complexity and design their contracts to minimize unnecessary constraints.

Proof verification is fast and has a fixed cost regardless of circuit size. This asymmetry between proving cost and verification cost is intentional. It enables the blockchain model where many users generate proofs in parallel on their own machines while validators efficiently verify them.

The Compact compiler applies optimizations to reduce circuit size. These include constant folding (evaluating constant expressions at compile time), common subexpression elimination, and constraint reuse. Contract authors can also help by avoiding unnecessary branching, using efficient data structures, and minimizing the number of hash operations in their circuits.

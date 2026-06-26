# Privacy Mechanisms

## Overview

Midnight provides privacy at the protocol level through a combination of cryptographic commitments, zero-knowledge proofs, and a shielded transaction protocol called Zswap. These mechanisms ensure that transaction details remain confidential while preserving the ability of validators to verify correctness and prevent double spending.

## Zswap Shielded Transactions

Zswap is Midnight's protocol for confidential value transfers. It hides three critical pieces of information in every shielded transaction: the amount being transferred, the identity of the sender, and the identity of the recipient. Only the parties involved in the transaction can see these details.

### How Zswap Works

A shielded transaction consumes existing coin commitments and creates new ones. Each coin commitment is a cryptographic hash that binds a coin's value and owner without revealing either. When a coin is spent, the spender reveals a nullifier (a unique identifier derived from the coin) that proves the coin existed and has not been spent before. The nullifier does not reveal which coin it corresponds to, so an observer cannot link the spend to any particular coin commitment.

The transaction includes a zero-knowledge proof that attests to several facts: the spender knows the secret key corresponding to the nullifier, the sum of input coin values equals the sum of output coin values (enforcing conservation of value), and each output coin commitment is correctly formed. Validators verify this proof without learning any of the private values.

### Multi-Party Transactions

Zswap supports transactions involving multiple senders and multiple recipients within a single proof. This enables complex transfer patterns such as splitting a large coin into several smaller ones, combining multiple coins into one, or routing value through intermediate parties. The proof enforces conservation of value across all inputs and outputs simultaneously.

## Selective Disclosure Pattern

Selective disclosure is a design pattern that allows users to reveal specific facts about their private data while keeping everything else hidden. Rather than an all-or-nothing choice between full privacy and full transparency, selective disclosure gives users fine-grained control.

### How Selective Disclosure Works

In a Compact contract, the circuit defines what information will be disclosed as part of the proof. Any value placed in the disclosure section of the circuit becomes publicly visible when the proof is verified. Everything else remains hidden. The contract author decides at design time which pieces of data are disclosed and which remain private.

### Use Cases

A compliance application might disclose that a transaction's value falls within a regulatory threshold range without revealing the exact amount. An identity application might disclose that a user is over 18 without revealing their birth date. A voting application might disclose that a vote was cast without revealing which option was chosen.

### Design Considerations

Disclosure is irreversible. Once data appears in the disclosure section, it is permanently visible on chain. Contract authors must carefully consider what they disclose. The general principle is to disclose only what is strictly necessary for the application to function and for compliance requirements to be met.

## Communication Commitments

Communication commitments are the mechanism by which the local component sends private state updates to the replicated component. Rather than sending the actual data (which would compromise privacy), the local component sends a cryptographic commitment that binds to the data without revealing it.

The replicated component stores these commitments on chain. Later, when the local component needs to reference that private state, it can open the commitment by providing the original data and proving that it matches the stored commitment. This proof happens within the ZK circuit, so the data itself never appears on chain.

## Coin Commitments

Coin commitments are the building blocks of shielded value on Midnight. A coin commitment is a cryptographic hash computed from three inputs: the coin's value, the owner's public key, and a random salt. The salt prevents an observer from deriving the owner or value by brute-force hashing.

### Creating Coin Commitments

When value enters the shielded pool, the protocol creates a new coin commitment and adds it to the commitment tree. Coin commitments are stored in a Merkle tree structure that allows efficient membership proofs. A user who knows the value, public key, and salt can prove that their coin commitment exists in the tree without revealing which commitment it is.

### Spending Coins

To spend a shield coin, the owner must prove two things: they know the preimage of the coin commitment (value, public key, salt), and the coin has not been spent before. The first proof shows ownership. The second proof is accomplished through nullifiers.

## Nullifiers

A nullifier is a unique identifier derived from a coin commitment and the owner's secret key. When a coin is spent, its nullifier is revealed on chain. Validators check that the nullifier has not appeared before (preventing double spending). Because the nullifier is derived using a one-way function, it cannot be linked back to the original coin commitment, preserving the spender's privacy.

### Nullifier Derivation

The nullifier is computed as the hash of the coin commitment's serial number (a field element unique to each coin) and the owner's secret key. Two different owners spending coins from the same commitment tree entry would produce different nullifiers. The same owner spending the same coin twice would produce the same nullifier both times, which validators detect as a double-spend attempt.

### Nullifier Safety

Contract authors must ensure that nullifiers are derived correctly. A poorly designed nullifier scheme could allow an attacker to spend the same coin twice or could inadvertently link different spends to the same user. The Compact standard library provides safe nullifier derivation functions that implement the correct pattern.

## Viewing Keys

Viewing keys enable selective access to transaction details. The owner of a viewing key can decrypt the amounts and counterparties of transactions that involve a particular shielded address. This enables auditing, compliance reporting, and wallet functionality while maintaining privacy against the general public.

### Outgoing Viewing Keys

An outgoing viewing key allows the holder to see the details of transactions sent from a particular address. This is useful for wallet software that needs to display the user's sent transaction history.

### Incoming Viewing Keys

An incoming viewing key allows the holder to see the details of transactions received at a particular address. This is useful for wallet software that needs to detect and display incoming payments.

### Key Distribution

Users can share viewing keys selectively. An individual user might share their incoming viewing key with their accountant for tax purposes but not with anyone else. The protocol does not enforce how viewing keys are distributed. Users control this themselves.

## Encryption

Midnight uses encryption to protect the contents of transactions from network observers. When a user submits a shielded transaction, the recipient's portion of the transaction data is encrypted with the recipient's public key. Only the recipient can decrypt this data and learn that they received funds.

### Payload Encryption

The encrypted payload contains the coin value, the salt used to create the new coin commitment, and any memo data attached to the transaction. Without this information, the recipient cannot spend the received coin because they need the value and salt to construct the proof of ownership.

The sender encrypts the payload using the recipient's public key and includes the ciphertext in the transaction. Validators store the encrypted payload on chain but cannot decrypt it. The recipient's wallet software monitors the chain for transactions that contain decryptable payloads.

## Private State Providers

Private state providers are services that store private data off chain and supply it to the local component when needed. They act as a bridge between the user's private data and the on-chain verification system.

### How Private State Providers Work

When the local component needs private data to construct a witness (for example, the value of a coin the user owns), it queries a private state provider. The provider returns the requested data, which the local component uses to build the witness. The provider never submits data to the chain. It only responds to queries from authorized clients.

### Provider Trust Model

Private state providers must be trusted to store data correctly and respond honestly. If a provider loses data, the user may be unable to spend their coins. If a provider gives incorrect data, the proof generation will fail or produce an invalid proof. The trust is limited to availability and correctness of stored data. The provider cannot steal funds because it does not have access to the user's secret key.

## On-Chain Proofs with Off-Chain Data

The fundamental privacy architecture of Midnight can be summarized as follows: proofs live on chain, data lives off chain. Validators verify cryptographic proofs that attest to the correctness of private computations. The actual private data never appears in any block, never enters any validator's memory, and never gets stored in any on-chain data structure. Observers of the blockchain see only proofs, commitments, and nullifiers. They can verify that every transaction followed the rules, but they cannot see what those transactions actually did.

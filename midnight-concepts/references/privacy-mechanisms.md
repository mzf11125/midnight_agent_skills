# Privacy Mechanisms in Midnight

## Overview

Midnight provides multiple privacy mechanisms that work together to enable confidential blockchain applications while maintaining verifiability.

## Zswap Protocol

### What is Zswap?

Zswap is Midnight's privacy-preserving token system that hides:
- Transaction amounts
- Sender and receiver identities
- Token types being transferred

### How Zswap Works

**Traditional Blockchain Transaction**:
```
Alice sends 100 tokens to Bob
[Publicly visible: sender=Alice, receiver=Bob, amount=100]
```

**Zswap Transaction**:
```
Someone sent some amount of some token to someone
[Publicly visible: cryptographic commitments proving validity]
[Private: actual sender, receiver, amount, token type]
```

### Key Components

#### Coin Commitments
Zswap represents tokens as cryptographic commitments:
- Commitment hides the coin's value, type, and owner
- Commitment can be proven to be valid without revealing details
- Commitments are stored in a Merkle tree on-chain

#### Nullifiers
When spending a coin:
- Generate a unique nullifier for that coin
- Nullifier prevents double-spending
- Nullifier doesn't reveal which coin was spent

#### Zero-Knowledge Proofs
Each Zswap transaction includes proofs that:
- Inputs are valid unspent coins
- Outputs are properly formed
- Transaction balances (inputs = outputs)
- Sender has authority to spend inputs

### Transaction Structure

A Zswap transaction consists of:

**Guaranteed Phase** (always executes):
- Fee payments
- Fast-to-verify operations
- Always succeeds or transaction is invalid

**Fallible Phase** (may fail atomically):
- Contract calls
- Operations that might fail
- Fails separately from guaranteed phase

### Shielded vs Unshielded

#### Shielded Tokens
- Fully private (amounts, owners hidden)
- Use ZK proofs for all operations
- Maximum privacy

#### Unshielded Tokens
- Amounts and owners visible
- Faster operations (no ZK proofs needed)
- Useful for public operations

#### Conversion
- Shield: Convert unshielded → shielded (gain privacy)
- Unshield: Convert shielded → unshielded (lose privacy for transparency)

### Dust Tokens
Special token type for paying transaction fees:
- Unshielded by default
- Used to pay network fees
- Can be converted to/from other tokens

## Selective Disclosure

### Concept
Applications choose exactly what information to reveal and what to keep private.

### Granular Control
- **Fully Private**: No information revealed (e.g., secret ballot voting)
- **Partially Private**: Some properties revealed (e.g., "transaction > $10,000" without exact amount)
- **Conditionally Private**: Reveal to specific parties (e.g., auditor access)

### Implementation Patterns

#### Pattern 1: Public Verification, Private Data
```
Public: "A valid vote was cast"
Private: Who voted, what they voted for
```

#### Pattern 2: Threshold Disclosure
```
Public: "Balance exceeds $10,000" (for compliance)
Private: Exact balance amount
```

#### Pattern 3: Time-Based Disclosure
```
Private during: Auction bidding period
Public after: Auction ends, winning bid revealed
```

### Use Cases

**Financial Compliance**:
- Prove transaction is under reporting threshold
- Don't reveal exact amount

**Age Verification**:
- Prove age > 18
- Don't reveal birthdate

**Credential Verification**:
- Prove university degree
- Don't reveal GPA or graduation date

## State Channels (Hydra Integration)

### What are State Channels?

State channels allow groups of users to conduct many transactions off-chain, then settle the final result on-chain.

### Benefits

**Privacy**:
- Off-chain transactions aren't visible to the network
- Only opening and closing states are on-chain
- Intermediate states remain private

**Performance**:
- Near-instant transactions
- No waiting for block confirmation
- Thousands of transactions per second

**Cost**:
- Pay fees only for opening/closing channel
- Unlimited off-chain transactions
- Dramatically lower costs

### How It Works

1. **Open Channel**: Parties lock funds on-chain
2. **Transact Off-Chain**: Exchange signed state updates
3. **Close Channel**: Submit final state on-chain

### Privacy Implications

**On-Chain Visibility**:
- Channel opening (parties, initial amounts)
- Channel closing (final amounts)

**Off-Chain Privacy**:
- All intermediate transactions
- Transaction patterns
- Exact timing of transfers

### Use Cases

**Gaming**:
- Fast in-game transactions
- Private game state
- Settle final scores on-chain

**Micropayments**:
- Streaming payments
- Pay-per-use services
- Low-cost frequent transactions

**Private Exchanges**:
- Negotiate trades privately
- Settle final swap on-chain
- Hide trading strategies

## Combining Privacy Mechanisms

### Zswap + Selective Disclosure
- Use Zswap for private token transfers
- Selectively reveal properties for compliance
- Example: Private DeFi with regulatory reporting

### Zswap + State Channels
- Open state channel with Zswap (private amounts)
- Conduct private off-chain transactions
- Close channel with Zswap (private final state)
- Example: Private gaming with token rewards

### All Three Together
- State channels for performance
- Zswap for token privacy
- Selective disclosure for compliance
- Example: High-frequency private trading with audit trails

## Privacy vs Performance Trade-offs

### Maximum Privacy
- Fully shielded Zswap transactions
- All data private
- Slower (ZK proof generation)
- Higher computational cost

### Balanced Approach
- Mix shielded and unshielded as needed
- Selective disclosure for necessary transparency
- State channels for frequent operations
- Optimal for most applications

### Performance Priority
- Unshielded transactions where privacy not needed
- State channels for high-frequency operations
- Selective disclosure only when required
- Faster, lower cost

## Security Considerations

### Cryptographic Assumptions
- Elliptic curve discrete logarithm hardness
- Collision-resistant hash functions
- Secure random number generation

### Privacy Leaks to Avoid
- **Timing Analysis**: Transaction timing can reveal information
- **Amount Correlation**: Unique amounts can be tracked
- **Network Analysis**: IP addresses can reveal identities

### Best Practices
- Use standard denominations to avoid amount correlation
- Batch transactions to obscure timing
- Use privacy-preserving network layers (Tor, VPN)
- Regularly mix shielded and unshielded operations

## Development Guidelines

### Choosing Privacy Level
1. Identify what data must be private
2. Determine what must be public (compliance, UX)
3. Use appropriate mechanism for each data type
4. Test privacy properties thoroughly

### Testing Privacy
- Verify no unintended information leakage
- Test with realistic transaction patterns
- Consider adversarial analysis
- Use privacy analysis tools

### User Experience
- Explain privacy trade-offs to users
- Provide clear privacy indicators
- Allow user control over disclosure
- Balance privacy with usability

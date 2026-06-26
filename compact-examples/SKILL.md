---
name: compact-examples
description: Collection of reference Compact contracts demonstrating privacy patterns, token standards, access control, commit-reveal protocols, Merkle tree membership, state machines, and multi-party interactions. Use when users need working examples of shielded tokens, NFT contracts, voting systems, private auctions, guest lists, bulletin boards, leaderboards, ZK loan patterns, or any privacy-preserving smart contract pattern on Midnight. Each example includes its purpose, key patterns, and privacy techniques used.
---

# Compact Reference Contracts and Patterns

A collection of production-ready Compact contract examples demonstrating privacy-preserving patterns and best practices.

## OpenZeppelin-Style Contracts

### FungibleToken

**Purpose**: Implements a standard fungible token similar to ERC-20 with privacy-preserving capabilities.

**Key Patterns Demonstrated**:
- Token minting and burning with supply tracking
- Balance transfers between accounts
- Allowance and approval mechanism
- Events for indexer consumption

**Contract Structure**:
```compact
pragma language_version >= 0.20;
import CompactStandardLibrary;

export ledger totalSupply: Uint<64>;
export ledger balances: StateMap<Bytes<32>, Uint<64>>;
export ledger allowances: StateMap<[Bytes<32>, Bytes<32>], Uint<64>>;
export sealed ledger owner: Bytes<32>;

export constructor(initialOwner: Bytes<32>, supply: Uint<64>): [] {
  owner = initialOwner;
  totalSupply = disclose(supply);
  balances.insert(initialOwner, disclose(supply));
}

export circuit transfer(
  private amount: Uint<64>,
  public recipient: Bytes<32>
): [] {
  const sender = msg.sender;
  const senderBalance = balances.lookup(sender);
  assert(amount <= senderBalance, "Insufficient balance");
  assert(amount > 0, "Amount must be positive");
  balances.insert(sender, senderBalance - amount);
  const recipientBalance = balances.lookup(recipient);
  balances.insert(recipient, recipientBalance + amount);
}
```

**Privacy Techniques**:
Balances are stored in public StateMap. Amount values are visible as public parameters. For fully private transfers use the shielded token pattern with Zswap instead.

### MultiToken

**Purpose**: Implements a multi-token standard similar to ERC-1155 supporting both fungible and non-fungible tokens in a single contract.

**Key Patterns Demonstrated**:
- Token ID-based management
- Batch transfers for gas efficiency
- Mixed fungible and non-fungible support
- Operator approval system

**Contract Structure**:
```compact
export ledger tokenBalances: StateMap<[Bytes<32>, Uint<32>], Uint<64>>;
export ledger operators: StateMap<[Bytes<32>, Bytes<32>], Boolean>;
export sealed ledger uri: Bytes<256>;
```

### NonFungibleToken

**Purpose**: Implements a non-fungible token standard similar to ERC-721 with privacy-aware ownership tracking.

**Key Patterns Demonstrated**:
- Unique token ownership
- Mint and transfer
- Approval mechanism
- Token metadata via URI

**Contract Structure**:
```compact
export ledger tokenOwner: StateMap<Uint<32>, Bytes<32>>;
export ledger tokenApprovals: StateMap<Uint<32>, Bytes<32>>;
export ledger ownedTokens: StateMap<Bytes<32>, Uint<32>>;
export sealed ledger owner: Bytes<32>;
export sealed ledger name: Bytes<32>;
export sealed ledger symbol: Bytes<16>;
```

**Privacy Techniques**:
Ownership is public. Token IDs are sequential. For private ownership tracking use a shielded NFT pattern with Merkle tree commitments.

## Access Control Patterns

### Ownable

**Purpose**: Provides basic authorization control with a single owner.

**Key Patterns Demonstrated**:
- Owner-only function modifier
- Ownership transfer with two-step confirmation
- Pending owner pattern for safety

**Contract Structure**:
```compact
export sealed ledger owner: Bytes<32>;
export ledger pendingOwner: Bytes<32>;

export constructor(initialOwner: Bytes<32>): [] {
  owner = initialOwner;
}

export circuit transferOwnership(public newOwner: Bytes<32>): [] {
  assert(msg.sender == owner, "Only owner");
  pendingOwner = newOwner;
}

export circuit acceptOwnership(): [] {
  assert(msg.sender == pendingOwner, "Only pending owner");
  owner = msg.sender;
}
```

**Privacy Techniques**:
Ownership is public. The two-step transfer prevents accidental loss of ownership. For private ownership use a commitment-based approach.

### AccessControl

**Purpose**: Role-based permission system with granular access control.

**Key Patterns Demonstrated**:
- Role definition and assignment
- Role-based function guards
- Role admin hierarchy
- Grant and revoke operations

**Contract Structure**:
```compact
export ledger roles: StateMap<[Bytes<32>, Bytes<32>], Boolean>;
export sealed ledger adminRole: Bytes<32>;

export circuit grantRole(
  public role: Bytes<32>,
  public account: Bytes<32>
): [] {
  assert(hasRole(adminRole, msg.sender), "Only admin");
  const key: [Bytes<32>, Bytes<32>] = [role, account];
  roles.insert(disclose(key), true);
}

fn hasRole(role: Bytes<32>, account: Bytes<32>): Boolean {
  const key: [Bytes<32>, Bytes<32>] = [role, account];
  return roles.lookup(key);
}
```

### Pausable

**Purpose**: Emergency stop mechanism that allows pausing and unpausing contract operations.

**Key Patterns Demonstrated**:
- Pause state management
- WhenNotPaused guard
- Pause guardian authorization
- Circuit breaker pattern

**Contract Structure**:
```compact
export ledger paused: Boolean;
export sealed ledger guardian: Bytes<32>;

export circuit pause(): [] {
  assert(msg.sender == guardian, "Only guardian");
  paused = true;
}

export circuit unpause(): [] {
  assert(msg.sender == guardian, "Only guardian");
  paused = false;
}

modifier whenNotPaused {
  assert(!paused, "Contract is paused");
}
```

## Token Patterns

### Shielded Token (ERC-20-like with Privacy)

**Purpose**: A fungible token where transfers are private via commitment and nullifier patterns.

**Key Patterns Demonstrated**:
- Coin commitments for private balances
- Nullifier-based double-spend prevention
- Merkle tree for commitment storage
- Shield and unshield operations

**Contract Structure**:
```compact
export ledger commitmentTree: StateBoundedMerkleTree<256, Field>;
export ledger spentNullifiers: Set<Field>;
export ledger unshieldedBalances: StateMap<Bytes<32>, Uint<64>>;

export circuit shield(
  private amount: Uint<64>,
  private randomness: Field,
  public commitment: Field
): [] {
  const sender = msg.sender;
  const balance = unshieldedBalances.lookup(sender);
  assert(amount <= balance, "Insufficient unshielded balance");
  assert(commitment == hash(amount, sender, randomness));
  unshieldedBalances.insert(sender, balance - amount);
  commitmentTree.insert(disclose(commitment));
}

export circuit transfer(
  private inputAmount: Uint<64>,
  private inputRandomness: Field,
  private inputNullifier: Field,
  private outputAmount: Uint<64>,
  private recipient: Bytes<32>,
  private outputRandomness: Field,
  public outputCommitment: Field
): [] {
  assert(!spentNullifiers.contains(inputNullifier));
  assert(outputCommitment == hash(outputAmount, recipient, outputRandomness));
  assert(inputAmount == outputAmount, "Amount mismatch");
  spentNullifiers.insert(disclose(inputNullifier));
  commitmentTree.insert(disclose(outputCommitment));
}
```

**Privacy Techniques**:
Transfer amounts and parties are hidden behind ZK proofs. The commitment tree stores encrypted balances. Nullifiers prevent double-spending without linking to specific coins. The Merkle tree enables efficient membership proofs.

### NFT with Shielded Ownership

**Purpose**: An NFT contract where ownership is private via Merkle tree commitments.

**Key Patterns Demonstrated**:
- Private ownership tracking
- Ownership proof via Merkle path
- Transfer without revealing token or owner
- Public metadata with private ownership

## Shielded Token Transfers

### Zswap Input and Output Model

**Purpose**: Demonstrate the complete flow of private token transfers using Zswap protocol.

**Key Patterns Demonstrated**:
- Input coin selection and verification
- Output coin creation
- Proof of valid input sum equals output sum
- Nullifier management

**Contract Structure**:
```compact
export circuit shieldedTransfer(
  private input1_amount: Uint<64>,
  private input1_secret: Field,
  private input1_nullifier: Field,
  private input2_amount: Uint<64>,
  private input2_secret: Field,
  private input2_nullifier: Field,
  private output1_amount: Uint<64>,
  private output1_recipient: Bytes<32>,
  private output1_randomness: Field,
  public output1_commitment: Field,
  private output2_amount: Uint<64>,
  private output2_recipient: Bytes<32>,
  private output2_randomness: Field,
  public output2_commitment: Field
): [] {
  // Verify inputs are unspent
  assert(!spentNullifiers.contains(input1_nullifier));
  assert(!spentNullifiers.contains(input2_nullifier));

  // Verify amounts balance
  const inputSum = input1_amount + input2_amount;
  const outputSum = output1_amount + output2_amount;
  assert(inputSum == outputSum, "Amount mismatch");

  // Verify output commitments
  assert(output1_commitment == hash(output1_amount, output1_recipient, output1_randomness));
  assert(output2_commitment == hash(output2_amount, output2_recipient, output2_randomness));

  // Spend inputs and create outputs
  spentNullifiers.insert(disclose(input1_nullifier));
  spentNullifiers.insert(disclose(input2_nullifier));
  commitmentTree.insert(disclose(output1_commitment));
  commitmentTree.insert(disclose(output2_commitment));
}
```

**Privacy Techniques**:
Multiple inputs and outputs in a single ZK proof. Observer sees only that some coins were spent and new coins created. Amounts source destination and change are all hidden.

### Coin Creation and Spending

**Purpose**: Separate the creation and spending of private coins into distinct operations.

## Unshielded Token Transfers

### UTXO Model Transfers

**Purpose**: Demonstrate public transparent token transfers using the UTXO model.

**Key Patterns Demonstrated**:
- Native NIGHT transfers
- Address encoding and validation
- Fee handling in DUST

```compact
export circuit unshieldedTransfer(
  public recipient: Bytes<32>,
  private amount: Uint<64>
): [] {
  const senderBalance = unshieldedBalances.lookup(msg.sender);
  assert(amount <= senderBalance, "Insufficient balance");
  unshieldedBalances.insert(msg.sender, senderBalance - amount);
  const recipientBalance = unshieldedBalances.lookup(recipient);
  unshieldedBalances.insert(recipient, recipientBalance + amount);
}
```

### Address-Based Transfers

**Purpose**: Transfer between Midnight addresses with public visibility.

## Application Patterns

### Calculator Contract

**Purpose**: Simple arithmetic operations demonstrating basic public state manipulation.

**Key Patterns Demonstrated**:
- Public state read and write
- Circuit function constraints
- Result computation and return

```compact
export ledger lastResult: Field;
export ledger operationCount: Counter;

export circuit add(public a: Field, public b: Field): Field {
  const result = field.add(a, b);
  lastResult = result;
  operationCount.increment(1);
  return result;
}
```

### Election Contract

**Purpose**: Private voting with public tally verification.

**Key Patterns Demonstrated**:
- Private votes hidden via ZK proofs
- Public vote counts for each candidate
- One-vote-per-voter enforcement via nullifiers
- Double-voting prevention

**Contract Structure**:
```compact
export ledger voteCounts: StateMap<Uint<8>, Counter>;
export ledger spentVotes: Set<Field>;
export ledger electionActive: Boolean;
export sealed ledger admin: Bytes<32>;

export circuit castVote(
  private voterSecret: Field,
  private candidateChoice: Uint<8>,
  public nullifier: Field
): [] {
  assert(electionActive, "Election is closed");
  assert(!spentVotes.contains(nullifier), "Already voted");
  assert(candidateChoice < 10, "Invalid candidate");

  spentVotes.insert(disclose(nullifier));
  voteCounts.lookup(candidateChoice).increment(1);
}
```

**Privacy Techniques**:
Individual votes are private. Each voter has a secret that produces a unique nullifier. The nullifier prevents double voting without revealing the voter. Vote counts are public. Candidate choice is hidden. The ZK proof verifies the vote is for a valid candidate without revealing which one.

### Private Guest List

**Purpose**: Membership verification without revealing identity using Merkle tree proofs.

**Key Patterns Demonstrated**:
- Merkle tree for membership set
- ZK proof of membership
- Guest addition by admin
- Membership verification without identity reveal

**Contract Structure**:
```compact
export ledger guestTree: StateBoundedMerkleTree<1024, Field>;
export sealed ledger admin: Bytes<32>;

export circuit addGuest(public guestHash: Field): [] {
  assert(msg.sender == admin, "Only admin");
  guestTree.insert(guestHash);
}

export circuit verifyMembership(
  private memberSecret: Field,
  private merklePath: Vector<10, Field>
): [] {
  const leaf = hash(memberSecret);
  const root = guestTree.root();
  assert(verifyMerkleProof(root, merklePath, leaf), "Not on guest list");
}
```

**Privacy Techniques**:
Guests prove membership without revealing their identity. The Merkle path proves inclusion. The guest secret never leaves the local component. The admin adds hashed identities not raw identities. Even the admin cannot determine who is attending.

### Private Reserve Auction

**Purpose**: Sealed-bid auction with commit-reveal pattern and private bids.

**Key Patterns Demonstrated**:
- Commit phase for bid submission
- Reveal phase for bid opening
- Highest bid determination
- Bid privacy during commit phase

**Contract Structure**:
```compact
export ledger committedBids: StateMap<Bytes<32>, Field>;
export ledger revealedBids: StateMap<Bytes<32>, Uint<64>>;
export ledger highestBid: Uint<64>;
export ledger highestBidder: Bytes<32>;
export ledger phase: Uint<8>; // 0=commit 1=reveal 2=closed

export circuit commitBid(
  private bidAmount: Uint<64>,
  private randomness: Field,
  public commitment: Field
): [] {
  assert(phase == 0, "Commit phase closed");
  assert(commitment == hash(bidAmount, msg.sender, randomness));
  committedBids.insert(msg.sender, disclose(commitment));
}

export circuit revealBid(
  private bidAmount: Uint<64>,
  private randomness: Field
): [] {
  assert(phase == 1, "Reveal phase closed");
  const storedCommitment = committedBids.lookup(msg.sender);
  assert(storedCommitment == hash(bidAmount, msg.sender, randomness));
  revealedBids.insert(msg.sender, disclose(bidAmount));
  if bidAmount > highestBid {
    highestBid = bidAmount;
    highestBidder = msg.sender;
  }
}
```

**Privacy Techniques**:
Bids are hidden during the commit phase via cryptographic commitments. The reveal phase proves the bid matches the commitment. Only the highest bid and bidder become public. Other bids remain known only to their bidders.

### Battleship Contract

**Purpose**: Two-player game demonstrating state machine pattern with public and private state.

**Key Patterns Demonstrated**:
- State machine for game phases
- Private board state
- Public move verification
- Turn-based interaction with privacy

**Contract Structure**:
```compact
enum GamePhase {
  setup,
  player1Turn,
  player2Turn,
  finished
}

export ledger gamePhase: GamePhase;
export ledger player1: Bytes<32>;
export ledger player2: Bytes<32>;
export ledger board1Hash: Field;
export ledger board2Hash: Field;

export circuit attack(
  private targetX: Uint<4>,
  private targetY: Uint<4>,
  private myBoard: Vector<100, Boolean>,
  public hit: Boolean
): [] {
  assert(gamePhase == player1Turn && msg.sender == player1 ||
         gamePhase == player2Turn && msg.sender == player2);
  // Verify board integrity
  assert(board1Hash == hashBoard(myBoard));
  // Verify hit claim
  const idx = targetY * 10 + targetX;
  assert(hit == myBoard[idx]);
  // Advance turn
  gamePhase = msg.sender == player1 ?
    GamePhase.player2Turn : GamePhase.player1Turn;
}
```

**Privacy Techniques**:
Board positions are private. The opponent only learns whether their shot was a hit or miss. The board commitment ensures players cannot change their board after setup. Game state machine is public.

### Bulletin Board

**Purpose**: Privacy-preserving message posting with optional identity verification.

**Key Patterns Demonstrated**:
- Anonymous posting with proof of membership
- Message storage with privacy options
- Public and private message modes
- Registration with identity verification

**Contract Structure**:
```compact
export ledger registeredUsers: StateBoundedMerkleTree<1024, Field>;
export ledger messages: StateMap<Uint<32>, Bytes<256>>;
export ledger messageCount: Counter;
export ledger messageAuthors: StateMap<Uint<32>, Field>;

export circuit postMessage(
  private userSecret: Field,
  private merklePath: Vector<10, Field>,
  public message: Bytes<256>,
  public revealIdentity: Boolean
): Field {
  const leaf = hash(userSecret);
  const root = registeredUsers.root();
  assert(verifyMerkleProof(root, merklePath, leaf), "Not registered");

  const msgId = messageCount.read();
  messages.insert(disclose(msgId), message);
  if revealIdentity {
    messageAuthors.insert(disclose(msgId), disclose(hash(userSecret)));
  }
  messageCount.increment(1);
  return msgId;
}
```

**Privacy Techniques**:
Posters prove they are registered without revealing identity. Messages can be posted anonymously or with optional identity disclosure. The Merkle tree enables efficient membership proofs. Identity verification happens at registration time.

### ZK Loan

**Purpose**: Credit evaluation without revealing financial details using Schnorr attestations.

**Key Patterns Demonstrated**:
- Schnorr signature verification in ZK
- Credit score attestation from trusted issuer
- Loan terms based on verified score
- Privacy-preserving credit evaluation

**Contract Structure**:
```compact
export ledger issuerPublicKey: CurvePoint;
export ledger activeLoans: StateMap<Bytes<32>, Uint<64>>;
export ledger totalBorrowed: Counter;

export circuit applyForLoan(
  private creditScore: Uint<16>,
  private attestationSignature: Field,
  private attestationRandomness: Field,
  public loanAmount: Uint<64>
): [] {
  // Verify attestation from trusted issuer
  const message = hash(creditScore, msg.sender);
  assert(
    verifySchnorr(issuerPublicKey, message, attestationSignature),
    "Invalid attestation"
  );

  // Determine loan terms based on score
  const maxLoan = creditScore * 100;
  assert(loanAmount <= maxLoan, "Loan exceeds credit limit");

  activeLoans.insert(msg.sender, disclose(loanAmount));
  totalBorrowed.increment(loanAmount);
}
```

**Privacy Techniques**:
The credit score is private. The lender learns only that the score meets the threshold. The Schnorr signature proves the trusted issuer attested to the score without revealing the score itself. Loan amounts become public but credit history remains private.

### Leaderboard

**Purpose**: Scoring system with configurable privacy modes for gaming and competition.

**Key Patterns Demonstrated**:
- Score submission with proof of ownership
- Public and private score modes
- Ranking without revealing exact scores
- Verification that scores are legitimate

**Contract Structure**:
```compact
export ledger scores: StateMap<Bytes<32>, Uint<32>>;
export ledger privacyMode: StateMap<Bytes<32>, Boolean>;
export ledger topScores: Vector<10, [Bytes<32>, Uint<32>]>;

export circuit submitScore(
  private newScore: Uint<32>,
  private gameProof: Field,
  public privacy: Boolean
): [] {
  const currentScore = scores.lookup(msg.sender);
  assert(newScore > currentScore, "Not a new high score");
  assert(verifyGameProof(gameProof, newScore, msg.sender));

  scores.insert(msg.sender, disclose(newScore));
  privacyMode.insert(msg.sender, disclose(privacy));
  updateLeaderboard(msg.sender, newScore, privacy);
}
```

**Privacy Techniques**:
Players can choose public or private score display. Private scores are hidden behind commitments. The leaderboard shows rankings but optionally hides exact scores. Game proof verification ensures scores are legitimate.

### Private Party

**Purpose**: Demonstration of privacy boundaries and access control for private events.

**Key Patterns Demonstrated**:
- Privacy boundary between public and private data
- Invitation proofs via Merkle tree
- RSVP tracking with privacy
- Event capacity management

**Contract Structure**:
```compact
export ledger inviteTree: StateBoundedMerkleTree<256, Field>;
export ledger rsvpCount: Counter;
export sealed ledger maxCapacity: Uint<16>;
export sealed ledger eventName: Bytes<64>;

export circuit rsvp(
  private inviteCode: Field,
  private merklePath: Vector<8, Field>
): [] {
  const leaf = hash(inviteCode);
  const root = inviteTree.root();
  assert(verifyMerkleProof(root, merklePath, leaf), "Not invited");
  assert(rsvpCount.read() < maxCapacity, "Event full");
  rsvpCount.increment(1);
}
```

**Privacy Techniques**:
Attendees prove they are invited without revealing their identity. The invite list is a Merkle tree of hashed invite codes. RSVP count is public but individual RSVPs are not identifiable. Capacity enforcement is public.

## Pattern Reference Matrix

| Pattern | Contract Example | Privacy Level | Use When |
|---|---|---|---|
| Public State | Calculator | None | Basic dApp state |
| Token Standard | FungibleToken | Low | Public token operations |
| Access Control | Ownable AccessControl | None | Authorization |
| Emergency Stop | Pausable | None | Circuit breaker |
| Shielded Token | ShieldedToken ERC-20 | High | Private transfers |
| Membership Proof | Private Guest List | High | Access control with privacy |
| Commit-Reveal | Private Reserve Auction | High | Sealed bids time-locked |
| State Machine | Battleship | Medium | Game phases workflows |
| Anonymous Posting | Bulletin Board | Medium-High | Identity-optional content |
| Credit Privacy | ZK Loan | High | Financial privacy |
| Scoring Privacy | Leaderboard | Configurable | Gaming competitions |
| Invite Privacy | Private Party | High | Events with access control |
| Voting Privacy | Election | High | Secret ballot voting |
| NFT Privacy | Shielded NFT | High | Private collectibles |
| Merkle Membership | Guest List Auction | High | Large membership sets |

## Privacy Technique Summary

### Commitment Patterns

**When to Use Commitments**:
- Store a value temporarily without revealing it
- Enable later reveal of the committed value
- Prove knowledge of a value before disclosure

**Implementation**:
```compact
const commitment = hash(value, randomness);
// Later: reveal value and randomness to prove commitment matches
assert(commitment == hash(value, randomness));
```

### Nullifier Patterns

**When to Use Nullifiers**:
- Prevent double-spending of private coins
- Prevent double-voting in private elections
- Prevent reuse of any one-time private action

**Implementation**:
```compact
const nullifier = hash(userSecret, actionIdentifier);
assert(!spentNullifiers.contains(nullifier));
spentNullifiers.insert(disclose(nullifier));
```

### Merkle Tree Patterns

**When to Use Merkle Trees**:
- Large membership sets with inclusion proofs
- Private state with public roots
- Efficient verification without revealing full set

**Implementation**:
```compact
export ledger tree: StateBoundedMerkleTree<1024, Field>;
const root = tree.root();
assert(verifyMerkleProof(root, path, leaf));
```

### Commit-Reveal Patterns

**When to Use Commit-Reveal**:
- Auctions with sealed bids
- Voting with delayed reveal
- Any two-phase protocol where first phase hides intent

**Implementation**:
Two separate circuits for commit and reveal phases. Commit circuit stores commitment. Reveal circuit verifies match then processes result.

### Domain Separation

**When to Use Domain Separation**:
- Any contract using signatures
- Contracts that might share key material
- Preventing cross-contract replay attacks

**Implementation**:
```compact
const domain = hash(self.address, "function_name_v1");
const signedData = hash(domain, userData, nonce);
```

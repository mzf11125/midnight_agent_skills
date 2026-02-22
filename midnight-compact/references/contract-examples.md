# Compact Contract Examples

## Private Token Contract

```compact
contract PrivateToken {
  state {
    commitments: Map<Field, Bool>,  // Coin commitments
    nullifiers: Map<Field, Bool>     // Spent coins
  }
  
  circuit mint(private amount: Field, private owner: Field, public commitment: Field) {
    require(!commitments[commitment]);
    require(commitment == commit(amount, owner));
    commitments[commitment] = true;
  }
  
  circuit transfer(
    private inputAmount: Field,
    private inputOwner: Field,
    private inputNullifier: Field,
    private outputAmount: Field,
    private outputOwner: Field,
    public outputCommitment: Field
  ) {
    // Verify input
    require(!nullifiers[inputNullifier]);
    require(inputAmount == outputAmount);
    
    // Spend input
    nullifiers[inputNullifier] = true;
    
    // Create output
    commitments[outputCommitment] = true;
  }
}
```

## Private Voting Contract

```compact
contract PrivateVoting {
  state {
    voteCount: Map<U32, U32>,  // candidate -> count
    hasVoted: Map<Field, Bool>  // nullifier -> voted
  }
  
  circuit vote(
    private voterId: Field,
    private candidate: U32,
    public nullifier: Field
  ) {
    require(!hasVoted[nullifier]);
    require(nullifier == hash(voterId));
    require(candidate < 10);  // Valid candidate
    
    hasVoted[nullifier] = true;
    voteCount[candidate] += 1;
  }
  
  pub fn getResults() -> Map<U32, U32> {
    voteCount
  }
}
```

## Confidential DeFi Contract

```compact
contract PrivateDEX {
  circuit privateSwap(
    private inputToken: Field,
    private inputAmount: Field,
    private outputToken: Field,
    private outputAmount: Field,
    public rate: Field
  ) {
    require(outputAmount == inputAmount * rate);
    // Swap logic with hidden amounts
  }
}
```

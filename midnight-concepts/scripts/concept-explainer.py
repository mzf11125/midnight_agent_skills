#!/usr/bin/env python3
"""
Interactive Midnight Concepts Explainer

This script provides interactive explanations of Midnight Network concepts
with examples and visualizations.
"""

import sys

CONCEPTS = {
    "zk-proofs": {
        "title": "Zero-Knowledge Proofs",
        "explanation": """
Zero-knowledge proofs allow proving a statement is true without revealing why it's true.

Example: Proving you're over 18 without revealing your birthdate
- Traditional: Show ID with birthdate (reveals too much)
- Zero-Knowledge: Prove "birthdate < today - 18 years" (reveals only the fact)

In Midnight:
- Smart contracts can operate on private data
- Proofs verify correctness without seeing the data
- Users maintain privacy while enabling verification
        """,
        "use_case": "Private voting: Prove you're eligible to vote without revealing identity"
    },
    "zswap": {
        "title": "Zswap Protocol",
        "explanation": """
Zswap is Midnight's privacy-preserving token system.

Traditional Transaction:
  Alice → 100 tokens → Bob
  [Everyone sees: sender, receiver, amount]

Zswap Transaction:
  ??? → ??? tokens → ???
  [Everyone sees: cryptographic proof it's valid]
  [Private: sender, receiver, amount, token type]

How it works:
1. Coins represented as cryptographic commitments
2. Spending generates nullifiers (prevents double-spend)
3. Zero-knowledge proofs verify validity
4. No information leaked about parties or amounts
        """,
        "use_case": "Private DeFi: Trade without revealing your strategy or positions"
    },
    "selective-disclosure": {
        "title": "Selective Disclosure",
        "explanation": """
Choose exactly what information to reveal and what to keep private.

Examples:
1. Age Verification
   - Reveal: "Age > 18" ✓
   - Keep Private: Exact birthdate

2. Financial Compliance
   - Reveal: "Transaction < $10,000" ✓
   - Keep Private: Exact amount

3. Credential Verification
   - Reveal: "Has university degree" ✓
   - Keep Private: GPA, graduation date

In Midnight:
- Applications control disclosure granularity
- Users can prove properties without revealing data
- Compliance without sacrificing privacy
        """,
        "use_case": "KYC: Prove you're verified without revealing personal information"
    },
    "partner-chain": {
        "title": "Partner Chain Architecture",
        "explanation": """
Midnight is a "partner chain" to Cardano, not a completely separate blockchain.

Benefits:
1. Security Inheritance
   - Leverages Cardano's proven consensus
   - Benefits from Cardano's validator network
   - Shared economic security

2. Specialized Capabilities
   - Optimized for privacy (ZK proofs, Zswap)
   - Custom VM for Compact contracts
   - Features not possible on main chain

3. Interoperability
   - Bridge assets between chains
   - Leverage Cardano ecosystem
   - Unified security model

Think of it as:
- Cardano = Secure foundation
- Midnight = Privacy-specialized extension
- Bridge = Seamless connection
        """,
        "use_case": "Build privacy apps while leveraging Cardano's security and ecosystem"
    },
    "compact": {
        "title": "Compact Programming Language",
        "explanation": """
Compact is purpose-built for writing privacy-preserving smart contracts.

Why a new language?
- Traditional languages weren't designed for zero-knowledge proofs
- Compact compiles directly to efficient ZK circuits
- Makes privacy programming natural and secure

Key Features:
1. Automatic circuit generation
2. Type safety for cryptographic operations
3. Built-in privacy primitives
4. Familiar syntax for developers

Example concept:
  circuit myPrivateFunction(private x, public y) {
    // x is private (hidden in proof)
    // y is public (visible to all)
    // Proof shows execution was correct without revealing x
  }
        """,
        "use_case": "Write smart contracts that operate on private data with public verification"
    },
    "state-channels": {
        "title": "State Channels (Hydra)",
        "explanation": """
State channels enable high-speed private transactions off-chain.

How it works:
1. Open Channel: Lock funds on-chain
2. Transact Off-Chain: Exchange signed state updates (instant, private)
3. Close Channel: Submit final state on-chain

Benefits:
- Privacy: Intermediate transactions not visible to network
- Speed: Near-instant transactions (no block confirmation)
- Cost: Pay fees only for open/close (unlimited off-chain txs)

Example:
Gaming:
- Open channel with game tokens
- Play game with instant moves (all private)
- Close channel with final scores on-chain
- Thousands of moves, two on-chain transactions
        """,
        "use_case": "High-frequency private transactions (gaming, micropayments, trading)"
    }
}

def print_concept(concept_key):
    """Print detailed explanation of a concept"""
    if concept_key not in CONCEPTS:
        print(f"❌ Unknown concept: {concept_key}")
        print(f"Available: {', '.join(CONCEPTS.keys())}")
        return
    
    concept = CONCEPTS[concept_key]
    print(f"\n{'='*70}")
    print(f"  {concept['title']}")
    print(f"{'='*70}")
    print(concept['explanation'])
    print(f"\n💡 Use Case: {concept['use_case']}")
    print(f"{'='*70}\n")

def list_concepts():
    """List all available concepts"""
    print("\n📚 Available Midnight Concepts:\n")
    for key, concept in CONCEPTS.items():
        print(f"  • {key:20} - {concept['title']}")
    print("\nUsage: python concept-explainer.py <concept-key>")
    print("       python concept-explainer.py all\n")

def main():
    if len(sys.argv) < 2:
        list_concepts()
        return
    
    concept_key = sys.argv[1].lower()
    
    if concept_key == "all":
        for key in CONCEPTS.keys():
            print_concept(key)
    elif concept_key in ["list", "help", "-h", "--help"]:
        list_concepts()
    else:
        print_concept(concept_key)

if __name__ == "__main__":
    main()

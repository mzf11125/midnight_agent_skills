#!/usr/bin/env python3
"""Generate Compact contract from templates"""
import sys
from pathlib import Path

TEMPLATES = {
    "token": """contract PrivateToken {
  state {
    commitments: Map<Field, Bool>,
    nullifiers: Map<Field, Bool>
  }
  
  circuit transfer(private amount: Field, private from: Field, private to: Field) {
    // Private token transfer logic
  }
}""",
    "voting": """contract PrivateVoting {
  state {
    voteCount: Map<U32, U32>,
    hasVoted: Map<Field, Bool>
  }
  
  circuit vote(private voterId: Field, private candidate: U32) {
    // Private voting logic
  }
}""",
    "basic": """contract MyContract {
  state {
    // State variables
  }
  
  init() {
    // Constructor
  }
  
  pub fn publicFunction() {
    // Public function
  }
}"""
}

def generate_contract(template_name, output_file):
    if template_name not in TEMPLATES:
        print(f"❌ Unknown template: {template_name}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        return False
    
    Path(output_file).write_text(TEMPLATES[template_name])
    print(f"✅ Generated {template_name} contract: {output_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate-contract.py <template> <output-file>")
        print(f"Templates: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    
    generate_contract(sys.argv[1], sys.argv[2])

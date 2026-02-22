---
name: midnight-compact
description: Comprehensive guide to the Compact programming language for writing privacy-preserving smart contracts on Midnight Network. Use when users need to write Compact smart contracts with zero-knowledge proofs, understand Compact syntax and language features, implement ZK circuit patterns and optimizations, generate contract boilerplate and project scaffolding, learn best practices for secure contract development, access Compact standard library functions, and compile and test Compact contracts.
---

# Midnight Compact Language

Complete guide to writing privacy-preserving smart contracts with Compact.

## What is Compact?

Compact is a purpose-built programming language for zero-knowledge smart contracts. Unlike adapting existing languages, Compact was designed from scratch to make privacy-preserving programming natural and secure.

**Key Design Goals**:
- Compile directly to efficient ZK circuits
- Type-safe cryptographic operations
- Familiar syntax for developers
- Automatic proof generation

## Quick Start

### Basic Contract Structure
```compact
circuit myContract(private secretInput, public publicInput) {
  // Private data hidden in proof
  // Public data visible to all
  // Proof shows execution was correct
}
```

### Project Scaffolding
Use `scripts/init-compact-project.py` to create new projects with proper structure.

### Contract Generation
Use `scripts/generate-contract.py` to generate boilerplate from templates.

### Compilation
Use `scripts/compile-compact.py` for compilation with error handling.

## Language Reference

### Basics
See [language-basics.md](references/language-basics.md) for:
- Syntax and structure
- Types and variables
- Functions and control flow
- Modules and imports

### ZK Patterns
See [zk-patterns.md](references/zk-patterns.md) for:
- Common zero-knowledge proof patterns
- Circuit optimization techniques
- Performance best practices
- Privacy-preserving algorithms

### Standard Library
See [standard-library.md](references/standard-library.md) for:
- Built-in cryptographic functions
- Hashing and commitments
- Elliptic curve operations
- Blockchain interaction primitives

## Contract Examples

See [contract-examples.md](references/contract-examples.md) for annotated examples:
- Private token contracts (Zswap integration)
- Voting contracts (secret ballot)
- DeFi contracts (confidential trading)
- Identity contracts (credential verification)

## Best Practices

See [best-practices.md](references/best-practices.md) for:
- Security guidelines
- Performance optimization
- Testing strategies
- Formal verification approaches

## Contract Templates

Ready-to-use templates in `assets/templates/`:
- **basic-contract/**: Minimal working contract
- **private-token/**: Zswap token implementation
- **voting-contract/**: Private voting system
- **defi-contract/**: Confidential DeFi protocol

## Development Workflow

1. **Initialize**: `python scripts/init-compact-project.py <project-name>`
2. **Generate**: `python scripts/generate-contract.py <template-name>`
3. **Develop**: Write contract logic in Compact
4. **Compile**: `python scripts/compile-compact.py <contract-file>`
5. **Test**: Run tests with Compact test framework
6. **Deploy**: Deploy to Midnight network

## Resources

- Official Docs: https://docs.midnight.network/develop/reference/compact/
- Language Reference: https://docs.midnight.network/develop/reference/compact/lang-ref
- Standard Library: https://docs.midnight.network/develop/reference/compact/compact-std-library/
- Grammar Spec: https://docs.midnight.network/develop/reference/compact/compact-grammar

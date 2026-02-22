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

### Minimal Working Contract (v0.19+)
```compact
pragma language_version >= 0.19;
import CompactStandardLibrary;

// Ledger state (individual declarations)
export ledger counter: Counter;
export ledger owner: Bytes<32>;

// Witness for private data
witness local_secret_key(): Bytes<32>;

// Circuit (returns [] not Void)
export circuit increment(): [] {
  counter.increment(1);
}
```

## Quick Syntax Reference

### ✅ CORRECT vs ❌ WRONG

**Pragma**:
```compact
✅ pragma language_version >= 0.19;
❌ pragma language_version >= 0.16.0;  // Outdated
```

**Ledger Declarations**:
```compact
✅ export ledger counter: Counter;
✅ export ledger owner: Bytes<32>;
❌ ledger { counter: Counter; }  // Block syntax deprecated
```

**Circuit Return Types**:
```compact
✅ export circuit increment(): [] { ... }
✅ export circuit getBalance(): Uint<64> { ... }
❌ export circuit increment(): Void { ... }  // Void doesn't exist
```

**Enum Access**:
```compact
✅ if (choice == Choice.rock) { ... }
❌ if (choice == Choice::rock) { ... }  // Rust-style doesn't work
```

**Witness Declarations**:
```compact
✅ witness local_secret_key(): Bytes<32>;
❌ witness get_key(): Bytes<32> { return ...; }  // No body allowed
```

**Counter Operations**:
```compact
✅ const val = counter.read();
❌ const val = counter.value();  // Method doesn't exist
```

**Pure Functions**:
```compact
✅ pure circuit helper(x: Field): Field { ... }
❌ pure function helper(x: Field): Field { ... }  // 'function' keyword doesn't exist
```

**Disclosure in Conditionals**:
```compact
✅ if (disclose(witness_val == x)) { ... }
❌ if (witness_val == x) { ... }  // Implicit disclosure error
```

### Common Mistakes to Avoid

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `ledger { field: Type; }` | `export ledger field: Type;` |
| `circuit fn(): Void` | `circuit fn(): []` |
| `enum State { ... }` | `export enum State { ... }` |
| `counter.value()` | `counter.read()` |
| `Choice::rock` | `Choice.rock` |
| `Cell<T>` | `Field` (Cell deprecated) |

### Project Scaffolding
Use `scripts/init-compact-project.py` to create new projects with proper structure.

### Contract Generation
Use `scripts/generate-contract.py` to generate boilerplate from templates.

### Compilation
Use `scripts/compile-compact.py` for compilation with error handling.

## Language Reference

### Quick Start
See [quick-start.md](references/quick-start.md) for:
- **Your first contract in 10 minutes**: Complete walkthrough
- **Step-by-step guide**: From installation to deployment
- **Working example**: Counter contract with tests
- **Common issues**: Troubleshooting compilation and deployment
- **Next steps**: Adding features and learning more

### TypeScript Interop
See [typescript-interop.md](references/typescript-interop.md) for:
- **Type mappings**: Compact types → TypeScript types
- **Generated code**: Working with Contract class
- **Witnesses**: Implementing witness functions
- **Circuit calls**: Calling circuits from TypeScript
- **Enums and structs**: Using user-defined types
- **Collections**: Vector, List, Maybe, Either
- **Best practices**: Type safety, BigInt handling

### Type System
See [type-system.md](references/type-system.md) for:
- **Primitive types**: Boolean, Uint, Field, tuples, vectors, Bytes, Opaque
- **User-defined types**: struct, enum, generic types
- **Subtyping rules**: Implicit conversions, least upper bounds
- **Type annotations**: Required vs optional
- **Default values**: Every type has a default
- **Type conversions**: Complete conversion table
- **TypeScript mappings**: Runtime representations
- **Generic types**: Type and size parameters
- **Best practices**: Type safety patterns

### Ledger Operations
See [ledger-operations.md](references/ledger-operations.md) for:
- **7 ledger state types**: Cell, Counter, Set, Map, List, MerkleTree, HistoricMerkleTree
- **Operations for each type**: Read, write, insert, lookup, increment, etc.
- **Syntactic sugar**: Shorthand for common operations
- **Nested state types**: Map<K, Counter>, Map<K, Map<K2, V>>
- **Sealed fields**: Immutable after constructor
- **Disclosure**: Making private data public
- **Complete examples**: Token contract, access control
- **Best practices**: Initialization, existence checks, optimization

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
- Common mistakes (10 detailed patterns)
- Formal verification approaches

## Contract Deployment

See [contract-deployment.md](references/contract-deployment.md) for:
- **Local deployment**: Compile and deploy to local testnet
- **Testnet deployment**: Deploy to Midnight testnet
- **Mainnet deployment**: Production deployment checklist
- **Deployment scripts**: Automated bash and TypeScript scripts
- **Troubleshooting**: Common compilation and deployment issues

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

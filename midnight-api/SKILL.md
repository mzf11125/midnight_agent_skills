---
name: midnight-api
description: Comprehensive guide to Midnight Network APIs for building decentralized applications. Use when users need to integrate Midnight APIs including Compact Runtime, DApp Connector, ZSwap, Wallet, and Ledger APIs, connect DApps to Midnight wallets, generate and verify zero-knowledge proofs programmatically, manage transactions and blockchain state, deploy and interact with Compact smart contracts, query blockchain data via indexer, implement wallet functionality, handle Zswap private transactions, and build complete web3 applications on Midnight.
---

# Midnight API Integration

Complete guide to integrating Midnight Network APIs for building privacy-preserving decentralized applications.

## API Ecosystem Overview

Midnight provides multiple specialized APIs:

- **Compact Runtime API**: Execute Compact contracts, generate ZK proofs
- **DApp Connector API**: Connect applications to wallets
- **ZSwap API**: Private token transactions
- **Wallet API**: Wallet operations and key management
- **Ledger API**: Blockchain transactions and state
- **Midnight.js**: Complete TypeScript SDK

## Quick Start

### Install Dependencies
```bash
npm install @midnight-ntwrk/midnight-js
npm install @midnight-ntwrk/dapp-connector-api
npm install @midnight-ntwrk/compact-runtime
```

### Initialize DApp Project
```bash
python scripts/init-dapp-project.py my-dapp
```

### Generate API Client
```bash
python scripts/generate-api-client.py wallet-connector
```

## API References

### Compact Runtime API
See [compact-runtime-api.md](references/compact-runtime-api.md) for:
- CircuitContext and WitnessContext
- Hashing and commitment functions
- Elliptic curve operations
- ContractState and QueryContext
- Proof generation and verification

### DApp Connector API
See [dapp-connector-api.md](references/dapp-connector-api.md) for:
- Wallet connection and authentication
- Reading balances and addresses
- Creating transactions
- Transaction balancing
- Proof delegation
- Complete code examples

### ZSwap API
See [zswap-api.md](references/zswap-api.md) for:
- Transaction structure (offers, inputs, outputs)
- Coin management
- Proof stages
- Shielded/unshielded operations

### Wallet API
See [wallet-api.md](references/wallet-api.md) for:
- Key management
- Transaction signing
- State synchronization
- Wallet operations

### Ledger API
See [ledger-api.md](references/ledger-api.md) for:
- Token types and operations
- Transaction submission
- Block queries
- Network interaction

## Integration Patterns

See [integration-patterns.md](references/integration-patterns.md) for:
- Common integration patterns
- Error handling strategies
- Best practices
- Performance optimization

## Complete Examples

See [api-examples.md](references/api-examples.md) for:
- Wallet connection
- Token transfers
- Private swaps
- Proof generation and delegation
- Contract deployment
- Blockchain queries

## Development Scripts

### Initialize DApp Project
`python scripts/init-dapp-project.py <project-name>`

Creates a new DApp project with:
- Midnight.js dependencies
- Wallet connector setup
- Example components
- Build configuration

### Generate API Client
`python scripts/generate-api-client.py <client-type>`

Generates boilerplate for:
- Wallet connection
- Transaction handling
- Proof generation
- State management

### Deploy Contract
`python scripts/deploy-contract.py <contract-file> <network>`

Deploys Compact contracts to Midnight network.

### Query Blockchain
`python scripts/query-blockchain.py <query-type> [params]`

Queries blockchain data via indexer.

### Test Wallet Connection
`python scripts/test-wallet-connection.py`

Tests wallet connectivity and configuration.

## Application Templates

Ready-to-use templates in `assets/templates/`:

- **web-dapp/**: Complete web application with wallet integration
- **api-examples/**: Standalone API usage examples
- **wallet-integration/**: Wallet connection patterns

## Resources

- Midnight.js SDK: https://docs.midnight.network/sdks/official/midnight-js
- API Reference: https://docs.midnight.network/api-reference
- DApp Connector Spec: https://github.com/midnightntwrk/midnight-dapp-connector-api
- GitHub: https://github.com/midnightntwrk/midnight-js

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

### Authentication Patterns
See [authentication-patterns.md](references/authentication-patterns.md) for:
- **Wallet-based auth**: Sign in with Midnight wallet
- **Challenge-response**: Prove wallet ownership
- **Session management**: Store and restore auth state
- **Protected routes**: Secure pages and API calls
- **Multi-wallet support**: Handle multiple wallets
- **Account switching**: Detect and handle account changes
- **Role-based access**: On-chain roles and permissions
- **Complete flow**: Production-ready authentication

### Network Configuration
See [network-configuration.md](references/network-configuration.md) for:
- **setNetworkId() requirement** (CRITICAL)
- Available networks (mainnet, preprod, testnet-02)
- Network-specific endpoints
- User configuration respect (privacy requirement)
- Common errors and solutions
- Environment-based configuration

### Address Formats
See [address-formats.md](references/address-formats.md) for:
- **Bech32m encoding** (v4.0.0+ standard)
- Address structure and validation
- Shielded, unshielded, and DUST addresses
- TypeScript validation examples
- Migration from pre-v4.0.0 formats
- Security considerations

### Compact Runtime API
See [compact-runtime-api.md](references/compact-runtime-api.md) for:
- **Network configuration**: setNetworkId() requirement
- **Core interfaces**: CircuitContext, CircuitResults, WitnessContext
- **Built-in functions**: Hashing (transient/persistent), commitments
- **Elliptic curve operations**: ecAdd, ecMul, hashToCurve
- **State management**: ContractState, StateValue, QueryContext
- **Runtime type system**: CompactType constructors for all types
- **Integration patterns**: Using with generated code
- **Best practices**: Network setup, hash types, nonce management

### DApp Connector API
See [dapp-connector-api.md](references/dapp-connector-api.md) for:
- **Complete ConnectedAPI specification**: All methods with signatures
- **InitialAPI structure**: Window injection, version checking
- **Configuration methods**: getConfiguration() for user privacy
- **State queries**: Balances, addresses (all Bech32m format)
- **Transaction operations**: makeTransfer, makeIntent, balance, submit
- **Proof delegation**: getProvingProvider() for ZK proofs
- **4 complete examples**: Connect, payment, swap, proof delegation
- **Error handling**: APIError class, ErrorCodes enum
- **Best practices**: Version checks, privacy respect, validation

### ZSwap API
See [zswap-api.md](references/zswap-api.md) for:
- **Transaction structure**: Guaranteed/fallible phases, offers
- **Coin management**: CoinInfo, QualifiedCoinInfo, TokenType
- **Input/output creation**: User-owned and contract-owned
- **State management**: ZswapChainState, ZswapLocalState
- **Transaction building**: Simple transfer, multi-token, contract calls
- **Transient coins**: Temporary coins for contract logic
- **Proving and submission**: Proof generation, transaction submission
- **Privacy features**: Hidden amounts, owners, unlinkability
- **Best practices**: Balancing offers, unique nonces, fee handling

### Wallet API
See [wallet-api.md](references/wallet-api.md) for:
- **Wallet creation**: Generate, from seed phrase, from private key
- **Address management**: Shielded/unshielded, derivation
- **Key management**: Spending, viewing, public keys
- **State synchronization**: Manual sync, auto-sync, status
- **Balance queries**: All tokens, specific tokens, shielded/unshielded
- **Transaction history**: Get transactions, details, filtering
- **Transaction signing**: Single, batch, message signing
- **Coin management**: Get coins, selection strategies
- **Shielding/unshielding**: Public ↔ private operations
- **Security best practices**: Seed storage, validation, error handling

### Ledger API
See [ledger-api.md](references/ledger-api.md) for:
- **Token types**: Native token, custom tokens, token info
- **Transaction submission**: Single, batch, with options
- **Transaction queries**: Get transaction, receipt, wait for confirmation
- **Block queries**: Get block, latest block, block range
- **State queries**: Account state, contract state, storage
- **Balance queries**: Single token, all tokens
- **Event queries**: Get events, filtering by topics
- **Gas estimation**: Estimate gas, get gas price
- **Network info**: Chain ID, version, peers, sync status
- **Best practices**: Error handling, caching, gas monitoring

### Integration Patterns
See [integration-patterns.md](references/integration-patterns.md) for:
- **Error handling**: APIError structure, comprehensive handlers
- **Retry logic**: Basic retry, network-specific, with timeout
- **State synchronization**: Polling, wallet sync, event-based
- **Wallet connection**: Multi-wallet support, connection state
- **Transaction patterns**: Safe submission, batch processing
- **Caching patterns**: Simple cache, LRU cache
- **Best practices**: Validation, user rejections, error messages
- **Production example**: Complete DApp implementation

### Error Codes
See [error-codes.md](references/error-codes.md) for:
- **Complete error catalog**: All API error codes
- **Error categories**: Wallet, transaction, network, proof, contract
- **Error details**: Cause, solution, code examples
- **Handling patterns**: Basic, comprehensive, retry patterns
- **Error classification**: Critical, retryable, user-fixable
- **Best practices**: Error checking, logging, user messages

### Contract Deployment
See [contract-deployment.md](references/contract-deployment.md) for:
- **Local deployment**: Start infrastructure, compile, deploy
- **Testnet deployment**: Configure environment, get test tokens, deploy
- **Mainnet deployment**: Pre-deployment checklist, production deployment
- **Deployment scripts**: Automated bash and TypeScript scripts
- **Network configuration**: Local, testnet, mainnet endpoints
- **Frontend integration**: Update environment, connect to contract
- **Troubleshooting**: Common deployment issues and solutions
- **Best practices**: Environment variables, testing, verification

### Testing Guide
See [testing-guide.md](references/testing-guide.md) for:
- **Contract testing**: Unit tests, property-based tests, ZK circuit tests
- **DApp testing**: Frontend component tests, E2E tests, API mocking
- **Infrastructure testing**: Node health checks, validator tests, indexer tests
- **Performance testing**: Load testing, benchmarks
- **Security testing**: Vulnerability scanning, penetration testing
- **Test coverage**: Measurement, thresholds, CI/CD integration
- **Best practices**: Test pyramid, isolation, descriptive names

## Complete Examples

See [api-examples.md](references/api-examples.md) for:
- Wallet connection
- Token transfers
- Private swaps
- Proof generation and delegation
- Contract deployment
- Blockchain queries
- Multi-token transfers
- Event listening
- Batch operations
- Error handling

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

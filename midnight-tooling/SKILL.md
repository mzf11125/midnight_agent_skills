---
name: midnight-tooling
description: Comprehensive guide to the Midnight development environment, tooling, and build system. Covers CLI installation, local devnet setup, Docker configuration, test environments, diagnostics, wallets, CI/CD, version management, and troubleshooting. Use when setting up a new Midnight project, debugging build issues, configuring CI pipelines, or resolving dependency conflicts.
---

# Midnight Tooling

## Development Environment Overview

The Midnight development environment consists of several components that work together to enable building, testing, and deploying Compact contracts and dApps. The required tools include the Compact compiler for compiling .compact files into ZKIR artifacts, Node.js for running TypeScript and JavaScript tooling, Docker for running the local devnet, and a package manager such as yarn or bun for managing dependencies. Optional tools include the Lace or 1AM browser extension wallet for browser-based dApps, the Midnight CLI for command-line wallet management, and the format-compact and fixup-compact tools for code formatting.

The setup flow for a new developer follows this sequence. Install Node.js version 18 or later. Install Docker and ensure the Docker daemon is running. Install either yarn or bun as the package manager. Install the Compact compiler. Set up the local devnet using midnight-local-dev. Verify the setup by running the example counter or hello-world project.

Each tool has its own installation instructions and version requirements. The compatibility matrix in the Midnight documentation lists which versions of each tool work together. Following the compatibility matrix is essential to avoid version mismatch errors.

## CLI Installation

### compactc Compiler

The `compactc` compiler transforms Compact language source files into ZKIR artifacts that the proof server uses to generate proofs and the network uses to verify them. The compiler must be available in your PATH for other Midnight tools to work correctly.

Install the compiler using the following command. The exact download URL depends on your operating system and the version you need. For Linux, download the binary and place it in a directory in your PATH such as `/usr/local/bin/compactc`. For macOS, the process is similar. For Windows via WSL, use the Linux installation process within the WSL environment.

```bash
curl -L https://github.com/midnight-ntwrk/compactc/releases/download/v0.X.Y/compactc-linux-x64 -o compactc
chmod +x compactc
sudo mv compactc /usr/local/bin/compactc
```

Verify the installation by running `compactc --version`. This should print the compiler version number. If the command is not found, ensure the installation directory is in your PATH.

### Compact Command Line Tool

The `compact` command-line tool provides utilities for working with Compact contracts. It supports compilation, testing, and code generation. The tool is installed as part of the compact-sdk package.

```bash
yarn add @midnight-ntwrk/compact-sdk
```

The tool can be invoked through `yarn compact` or `npx compact` after installation. It works with the contract's project configuration to compile contracts, run tests, and generate TypeScript bindings.

### format-compact

The `format-compact` tool formats Compact source code according to the official style guidelines. It enforces consistent indentation, line breaks, and spacing. Run it before committing Compact source files to ensure code style consistency.

```bash
npx format-compact src/*.compact
```

The formatter can be integrated into CI pipelines and pre-commit hooks. It supports formatting a single file, a directory of files, or all files matching a pattern.

### fixup-compact

The `fixup-compact` tool automatically fixes common issues in Compact source code. It can correct import paths, update syntax to the latest Compact language version, and fix common mistakes. Unlike the formatter, it makes semantic changes not just formatting changes.

```bash
npx fixup-compact src/*.compact
```

### Wallet CLI

The wallet CLI provides command-line access to Midnight wallet operations. It supports generating new wallets, checking balances, sending transactions, and managing viewing keys. This is primarily used for development and testing.

```bash
npx midnight-wallet --help
```

The wallet CLI works with both local devnet and remote networks. Configure the network endpoint before using wallet operations on a remote network.

## Local Devnet Setup

### midnight-local-dev

The `midnight-local-dev` tool is the recommended way to set up a local Midnight development network. It uses Docker Compose to run a complete Midnight node, indexer, and proof server on your local machine. This provides a fully functional Midnight environment for development and testing.

```bash
npx midnight-local-dev start
```

The tool downloads the necessary Docker images, starts the containers, and waits for all services to be healthy. Once started, the local devnet is available for dApp development. The default endpoints are the node JSON-RPC at `http://localhost:9944`, the indexer GraphQL at `http://localhost:8085/graphql`, and the proof server at `http://localhost:6300`.

The `midnight-local-dev stop` command stops all containers and preserves the blockchain state. The `midnight-local-dev reset` command stops the containers and deletes all state, starting from genesis on the next start. The `midnight-local-dev status` command shows the current state of all services.

### Docker Compose Stack

The local devnet consists of three main containers. The midnight-node container runs the Midnight blockchain node. The midnight-indexer container runs the indexer connected to the node, indexing blocks and transactions into PostgreSQL. The midnight-proof-server container runs the proof server for generating ZK proofs.

The Docker Compose file defines the dependencies between these containers. The indexer waits for the node to be healthy before starting. The proof server waits for both the node and the compiled ZKIR artifacts to be available. Health checks on each container ensure the stack is fully operational.

Additional containers may include PostgreSQL for the indexer's database, and a faucet service for providing test tokens. The complete stack provides everything needed for development.

### Node

The Midnight node container runs the full Midnight blockchain protocol. It produces blocks on a single validator schedule in the local devnet configuration. The node exposes a JSON-RPC endpoint for submitting transactions and querying state, a WebSocket endpoint for subscribing to events, and a Cardano DB Sync compatible endpoint for the indexer.

### Indexer

The indexer container processes blocks from the node and indexes them into PostgreSQL. It provides the GraphQL API for querying indexed data. The indexer exposes port 8085 for the GraphQL endpoint. Health checks ensure the indexer is caught up with the node before dependent services start.

### Proof Server

The proof server container generates ZK proofs for contract calls. It loads ZKIR artifacts from the compiled contracts and generates proving keys. The proof server exposes port 6300 for proof generation requests.

## Docker Configuration

### Container Images

The Docker images for the Midnight stack are published on the GitHub Container Registry. The images are tagged with version numbers that correspond to the Midnight protocol version. Always use pinned version tags rather than `latest` to ensure reproducibility.

The main images are `ghcr.io/midnight-ntwrk/node` for the node, `ghcr.io/midnight-ntwrk/indexer` for the indexer, `ghcr.io/midnight-ntwrk/proof-server` for the proof server, and `postgres` for the indexer's database.

### Environment Variables

Each container accepts environment variables for configuration. The node container variables include `NETWORK` for which network configuration to use, `VALIDATOR_KEY` for the validator signing key, and `RPC_PORT` for the JSON-RPC port. The indexer container variables include `NODE_ENDPOINT` for the node's URL, `DATABASE_URL` for the PostgreSQL connection, and `GRAPHQL_PORT` for the API port. The proof server container variables include `PROOF_SERVER_PORT` for the HTTP port, `KEY_STORE_PATH` for key storage, and `MAX_CONCURRENT_PROOFS` for concurrency limits.

### Volume Mounts

Volume mounts persist data across container restarts and provide access to host files. The node container mounts a volume for the blockchain state. The indexer container mounts a volume for the PostgreSQL data directory. The proof server container mounts a volume for the key store and a bind mount for the ZKIR artifacts directory containing compiled contracts.

### Network Configuration

The Docker Compose file defines a custom network for the Midnight stack. All containers communicate over this network. The node exposes its ports to the host for dApp connections. The indexer and proof server also expose their ports to the host. Internal container communication uses the Docker network DNS.

### Resource Limits

Set resource limits on containers to prevent the local devnet from consuming all system resources. The node container typically needs 1 to 2 CPU cores and 2 GB to 4 GB of memory. The indexer container needs 1 CPU core and 1 GB to 2 GB of memory. The proof server container needs 2 to 4 CPU cores and 4 GB to 8 GB of memory.

## Local Test Configuration

### LocalTestConfiguration

The `LocalTestConfiguration` type defines the configuration for a local test environment. It includes the container endpoint URLs, authentication tokens for internal services, and network configuration for the local devnet. This configuration is used by the test framework to connect to the local development environment.

```typescript
const config: LocalTestConfiguration = {
  nodeEndpoint: "http://localhost:9944",
  indexerEndpoint: "http://localhost:8085/graphql",
  proofServerEndpoint: "http://localhost:6300",
  networkId: "local-devnet"
}
```

### LocalTestEnvironment

The `LocalTestEnvironment` type wraps a `LocalTestConfiguration` with additional utilities for managing the test environment. It provides methods for starting and stopping the Docker containers, resetting the blockchain state, and generating test wallets.

### Container Endpoints

Container endpoints are the URLs for accessing each service in the local devnet. The node endpoint is typically `http://localhost:9944`. The indexer endpoint is typically `http://localhost:8085/graphql`. The proof server endpoint is typically `http://localhost:6300`. These endpoints are used by midnight-js providers to connect to the local services.

### Ports

The default port assignments avoid conflicts with common development tools. Port 9944 is the node JSON-RPC port. Port 8085 is the indexer GraphQL port. Port 6300 is the proof server port. Port 5432 is the PostgreSQL port. These ports can be overridden through environment variables or the Docker Compose configuration.

### Auth Tokens

Some services require authentication tokens for internal communication. The indexer uses a token to authenticate with the node. The proof server uses a token for internal API calls. In local development, these tokens are preconfigured. For remote environments, tokens must be obtained from the network operator.

## Remote Test Environments

### PreprodTestEnvironment

The `PreprodTestEnvironment` type defines configuration for connecting to the preprod test network. Preprod is a persistent test network that closely mirrors mainnet. It is used for integration testing before deploying to mainnet.

```typescript
const env: PreprodTestEnvironment = {
  networkId: "preprod",
  nodeEndpoint: "https://node.preprod.midnight.network",
  indexerEndpoint: "https://indexer.preprod.midnight.network/graphql",
  proofServerEndpoint: "https://proof-server.preprod.midnight.network"
}
```

### PreviewTestEnvironment

The `PreviewTestEnvironment` type defines configuration for the preview test network. Preview is used for early testing of new features before they are deployed to preprod.

### QanetTestEnvironment

The `QanetTestEnvironment` type defines configuration for the QA test network. Qanet is used for automated quality assurance testing.

### EnvVarRemoteTestEnvironment

The `EnvVarRemoteTestEnvironment` type reads test environment configuration from environment variables. This is useful for CI pipelines where the environment configuration is injected at runtime rather than hardcoded.

```typescript
const env: EnvVarRemoteTestEnvironment = {
  networkId: process.env.MIDNIGHT_NETWORK_ID,
  nodeEndpoint: process.env.MIDNIGHT_NODE_ENDPOINT,
  indexerEndpoint: process.env.MIDNIGHT_INDEXER_ENDPOINT,
  proofServerEndpoint: process.env.MIDNIGHT_PROOF_SERVER_ENDPOINT
}
```

### RemoteTestEnvironment

The `RemoteTestEnvironment` type is a union of all remote environment types. It is used when the specific environment type is not known at compile time.

### getTestEnvironment

The `getTestEnvironment` function auto-detects the appropriate test environment. It checks environment variables for a configured environment. If no environment is configured, it falls back to the local test environment. This function is used by test suites to automatically configure the correct environment.

```typescript
const env = getTestEnvironment()
```

The auto-detection logic checks the `MIDNIGHT_NETWORK_ID` environment variable. If it is set to `preprod`, `preview`, or `qanet`, the corresponding remote environment is used. If it is not set, the local test environment is used. This allows the same test code to run in different environments without code changes.

## Diagnostics

### Version Checking

Version checking verifies that all installed tools are at compatible versions. The diagnostic tools check the version of the Compact compiler, the midnight-js library, the indexer, the proof server, and Docker. Mismatches are reported with suggested fixes.

Run diagnostics with `npx midnight-diag` to check your environment. The output lists each tool's version, the expected version range, and whether the tool is compatible.

### Dependency Validation

Dependency validation checks that all required npm packages are installed at compatible versions. It inspects the `package.json` and `node_modules` to verify that midnight-js, compact-sdk, and other Midnight packages are present and consistent.

### Network Connectivity Tests

Network connectivity tests verify that the dApp can reach all required services. They check the node endpoint, the indexer GraphQL endpoint, and the proof server endpoint. If any endpoint is unreachable, the test reports the error and suggests fixes such as starting the local devnet or checking the network configuration.

### Proof Server Health

Proof server health checks verify that the proof server is running and has the required key material. The check sends a status request to the proof server and verifies that it responds with a healthy status. If the proof server is unhealthy, the check reports any error details.

### Indexer Health

Indexer health checks verify that the indexer is running and caught up with the node. The check queries the indexer's health endpoint and compares the indexed block height with the node's current block height. If the indexer is behind, the check reports the lag.

## Status Bar

The status bar provides real-time display of the development environment's status. It shows component health including whether the node, indexer, and proof server are healthy. It shows sync progress including the current block height and whether the indexer is caught up. It shows active connections to each service.

The status bar is typically displayed in the terminal when running midnight-local-dev. It updates every few seconds to reflect the current state. When a service becomes unhealthy, the status bar highlights the issue with a red indicator. When all services are healthy, the status bar shows green indicators.

## Faucet Client

### Acquiring Test Tokens

The faucet client provides test tokens for development on test networks. Test tokens have no real value and are used only for testing and development. The client connects to the faucet endpoint and requests tokens for a specified address.

```typescript
import { faucetClient } from "midnight-js"

await faucetClient.requestTokens({
  address: "addr_test_abc...",
  amount: 1000
})
```

### Faucet Endpoints

Each test network has its own faucet endpoint. The local devnet faucet is at `http://localhost:8086`. The preprod faucet is at `https://faucet.preprod.midnight.network`. The preview faucet is at `https://faucet.preview.midnight.network`.

### Rate Limits

Faucet endpoints have rate limits to prevent abuse. The typical rate limit is one request per address per hour. Exceeding the rate limit results in a 429 Too Many Requests response. Implement backoff and retry logic when rate limited.

### Token Amounts

The default token amount from the faucet is sufficient for development and testing. Larger amounts can be requested by specifying the amount parameter. The faucet will provide up to a maximum amount that varies by network.

### waitForFunds

The `waitForFunds` function polls the network until the requested tokens are available at the target address. It is used after requesting tokens from the faucet to ensure the tokens have been confirmed before proceeding with tests.

```typescript
await waitForFunds({
  address: "addr_test_abc...",
  expectedAmount: 1000,
  timeoutMs: 60000
})
```

## Browser Wallet Setup

### Lace Wallet

The Lace wallet is a browser extension for Cardano and Midnight networks. It supports Midnight test networks and mainnet. Install the extension from the Chrome Web Store or the Firefox Add-ons store. After installation, configure the network to the desired Midnight network and create or import a wallet.

### 1AM Wallet

The 1AM wallet is the reference browser extension wallet for Midnight. It supports all Midnight networks and provides features specific to Midnight such as viewing key management, proof generation coordination, and contract interaction. Install it from the browser extension store appropriate for your browser.

After installation, open the 1AM wallet and create a new wallet or import an existing one using a seed phrase. Configure the network to your development environment. For local development, set the network to the local devnet endpoint. For test networks, select the appropriate network from the list.

### Kuira Wallet

The Kuira wallet is another browser extension option for Midnight. It provides similar functionality to 1AM with a different user interface. The choice between 1AM and Kuira is a matter of personal preference. Both support the standard Midnight DApp Connector API.

### Browser Extension Installation

Browser extension wallets for Midnight are installed like any other browser extension. Search for the wallet name in your browser's extension store. Click install. After installation, the wallet icon appears in the browser toolbar. Click the icon to open the wallet interface.

### Network Configuration

Browser wallet network configuration determines which Midnight network the wallet connects to. For local development, add a custom network with the local devnet endpoint. For test networks, select from the preconfigured options. The network configuration affects which tokens are displayed and which nodes the wallet communicates with.

## Community Tools

### Midnight Explorer

The Midnight Explorer is a web-based block explorer for viewing blockchain data. It displays blocks, transactions, contract information, and network statistics. The explorer is available for test networks at their respective URLs. It is not available for the local devnet.

### Midnight Live View

The Midnight Live View is a real-time visualization of Midnight network activity. It shows blocks being produced, transactions being confirmed, and contract activity in a live dashboard. This is useful for understanding network activity patterns and for debugging transaction flow.

### Nightforge CLI

The Nightforge CLI is a community-developed tool for Midnight development. It provides project scaffolding, contract management, and deployment utilities. Use it to quickly create new Midnight projects with preconfigured settings.

### Midnames Playground

The Midnames playground is an interactive environment for experimenting with Midnight naming services. It allows you to register names on test networks and experiment with naming conventions. This is useful for developers building dApps that use human-readable names.

### Edda Starter Template

The Edda starter template is a preconfigured project template for Midnight dApps. It includes a Compact contract, a TypeScript CLI for interaction, configuration for multiple networks, and tests. Use it as a starting point for new Midnight projects.

## Platform Setup

### Linux Setup

Linux is the recommended development platform for Midnight. Install Docker using the official Docker repository. Install Node.js version 18 or later using nvm or the NodeSource repository. Install yarn or bun as the package manager. Install the Compact compiler as a binary in your PATH. Start the local devnet with midnight-local-dev.

```bash
curl -fsSL https://get.docker.com | sudo sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
npm install -g yarn
```

### macOS Setup

macOS setup follows a similar process. Install Docker Desktop for Mac. Install Node.js via Homebrew with `brew install node@18` or via nvm. Install the Compact compiler for macOS. Start Docker Desktop and then start the local devnet.

### Windows via WSL

Windows users should use Windows Subsystem for Linux (WSL) for Midnight development. Install WSL 2 and a Linux distribution such as Ubuntu. Follow the Linux setup instructions within the WSL environment. Docker Desktop for Windows can be configured to work with WSL 2.

### Docker Requirements

Docker Engine version 20.10 or later is required. Docker Compose version 2.0 or later is required. The Docker daemon must be running and accessible from the command line. Verify with `docker --version` and `docker compose version`.

### Node.js Version Requirements

Node.js version 18 or later is required. Version 20 is recommended. Check your version with `node --version`. Use nvm to manage multiple Node.js versions if needed.

## Fix Package Repository Access

### 403 Forbidden Errors

When installing Midnight packages, you may encounter 403 Forbidden errors. This occurs because Midnight packages are hosted on the GitHub Packages registry which requires authentication even for public packages.

### npm Registry Configuration

Configure npm to authenticate with the GitHub Packages registry. Create a GitHub personal access token with the `read:packages` scope. Add the token to your npm configuration.

```bash
npm config set @midnight-ntwrk:registry https://npm.pkg.github.com
npm config set //npm.pkg.github.com/:_authToken YOUR_GITHUB_TOKEN
```

### GitHub Packages Auth

For yarn, add the GitHub token to your `.yarnrc.yml` file. For bun, use the `bunfig.toml` configuration file. The authentication token must have the `read:packages` scope. Tokens should be stored securely and not committed to version control.

## Fix Version Mismatches

### Compatibility Matrix

The Midnight compatibility matrix lists which versions of each component work together. Before upgrading any component, check the matrix to ensure compatibility. The matrix is maintained in the Midnight documentation and updated with each release.

### Dependency Alignment

Dependency alignment ensures that all Midnight packages in your project use the same version. Inconsistent versions can cause runtime errors. Use the `resolutions` field in `package.json` to force consistent versions across transitive dependencies.

```json
{
  "resolutions": {
    "@midnight-ntwrk/midnight-js": "0.X.Y",
    "@midnight-ntwrk/compact-sdk": "0.X.Y"
  }
}
```

### Version Pinning

Always pin dependency versions to exact versions rather than using version ranges. This ensures that builds are reproducible and that you do not accidentally pick up breaking changes. Use exact version numbers in `package.json` and lock the lockfile.

### Upgrade Strategies

When upgrading Midnight dependencies, first check the compatibility matrix to identify which versions can be upgraded together. Upgrade all Midnight packages to their compatible versions simultaneously rather than upgrading one at a time. Run the full test suite after upgrading to verify compatibility. Check for migration guides for breaking changes between versions.

## Bun Runtime Setup

### Bun Package Manager

Bun is a fast JavaScript runtime and package manager that is well-suited for Midnight development. It provides faster installation times and faster script execution compared to npm or yarn. Install Bun following the instructions at `bun.sh`.

```bash
curl -fsSL https://bun.sh/install | bash
```

### Compact Compiler with Bun

The Compact compiler invoked through `bun compact` works similarly to `yarn compact`. Ensure the compact-sdk package is installed and the compiler binary is in your PATH. The compiler does not depend on Bun but uses it for script execution if available.

## CI/CD Integration

### GitHub Actions Setup

Midnight projects can be tested in CI using GitHub Actions. The workflow file installs Node.js, installs dependencies, starts the local devnet using Docker, runs tests, and collects test results. The workflow should run on every push and pull request.

```yaml
name: Midnight CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: yarn install
      - run: yarn midnight-local-dev start
      - run: yarn test
      - run: yarn midnight-local-dev stop
```

### Docker in CI

GitHub Actions runners support Docker out of the box. The Midnight local devnet containers can be started directly in the CI environment. Ensure the workflow has enough resources to run the containers. The default GitHub Actions runner with 2 CPU cores and 7 GB of memory is sufficient for most Midnight projects.

### Testing in CI

Tests in CI run against the local devnet started by midnight-local-dev. Tests should wait for the devnet to be fully healthy before starting. The test suite should include unit tests, integration tests, and end-to-end tests. Test results should be reported in JUnit format for integration with GitHub's test reporting.

### Deployment Pipelines

Deployment pipelines automate the process of deploying contracts to test networks. The pipeline compiles the Compact contracts, runs tests, generates deployment artifacts, and deploys to the target network. Deployment to mainnet should include a manual approval step.

## Best Practices

### Version Pinning

Pin all dependency versions to exact versions. Pin Docker image versions to specific tags. Pin the Compact compiler version. Pin Node.js version in `.nvmrc` or `.node-version`. Version pinning ensures that all team members and CI systems use the same tool versions.

### Lockfile Management

Commit lockfiles to version control. This ensures that all developers and CI systems get the exact same dependency versions. Update lockfiles when dependencies change by running `yarn install` or `bun install` and committing the updated lockfile. Review lockfile changes in pull requests to understand what dependency versions changed.

### Environment Isolation

Use separate environments for development, testing, and production. The local devnet is for development and unit testing. Test networks are for integration testing. Mainnet is for production. Never use real funds on test networks. Never use test wallets on mainnet.

### Reproducible Builds

Ensure that builds are reproducible across different machines. Use Docker for consistent build environments. Use exact version pins for all dependencies. Use lockfiles for reproducible dependency resolution. Document the build process in the project README. Test the build in CI to catch reproducibility issues early.

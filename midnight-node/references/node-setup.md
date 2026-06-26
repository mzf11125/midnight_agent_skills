# Midnight Node Setup Guide

## Hardware Requirements

### Minimum Requirements

A full node requires at least 4 CPU cores, 8 GB RAM, and 250 GB SSD storage. Network connectivity should provide 10 Mbps symmetrical bandwidth with low latency. Disk I/O performance is critical and NVMe storage is strongly recommended.

### Recommended Requirements

For production deployments allocate 8 CPU cores, 16 GB RAM, and 500 GB NVMe SSD storage. Validator nodes benefit from 32 GB RAM to handle concurrent proving workloads. Archive nodes require 2 TB or more of SSD storage plus additional capacity for database indexes.

### Network Ports

Open TCP port 30333 for the P2P protocol. Open TCP port 9944 for the WebSocket RPC interface. Open TCP port 9615 for Prometheus metrics. Restrict RPC ports to trusted networks only.

## Installation

### Using Prebuilt Binaries

Download the latest release binary from the official repository. Verify the checksum against the published signature. Place the binary in a directory on your system PATH. Create a dedicated system user to run the node service.

### Building From Source

Install the Rust toolchain using rustup. Clone the node repository and checkout the desired release tag. Build the release binary with `cargo build --release`. The output binary is located at `target/release/midnight-node`.

### Verifying Installation

Run `midnight-node --version` to confirm the binary is installed correctly. Run `midnight-node --help` to review all available command line options.

## Full Node Setup

### Directory Structure

Create a data directory for blockchain data and a config directory for configuration files. The recommended layout places data in `/var/lib/midnight` and configuration in `/etc/midnight`.

### Service Configuration

Create a systemd unit file to manage the node process. Configure the service to restart on failure and set appropriate resource limits. Enable the service to start automatically on system boot.

### Running the Node

Start the node with `midnight-node --base-path /var/lib/midnight --chain midnight`. The node will begin syncing from the network. Initial sync may take several hours depending on hardware and network speed.

### Syncing Options

Warp sync downloads the state at a recent finalized block and verifies only the finality proofs rather than executing every block. This is the fastest sync method for new nodes. Full sync replays every block from genesis and is required only for archive nodes or when you need complete verification history.

## Boot Node Configuration

A boot node requires minimal configuration. Specify the listen address and disable unnecessary subsystems. Boot nodes do not participate in consensus or maintain state. The key configuration directive is `--bootnode` which other nodes use to discover the network.

Boot nodes should run on stable infrastructure with a static public IP address. Multiple boot nodes across different geographic regions improve network resilience.

## RPC Node Configuration

### Rate Limiting

Configure rate limiting to prevent abuse. Set maximum concurrent connections and requests per second per client. Use the `--rpc-max-connections` and `--rpc-max-request-size` flags to define limits. Consider proxying RPC traffic through nginx or a similar reverse proxy for additional control.

### Authentication

Enable RPC authentication for administrative methods. Use the `--rpc-auth` flag to require bearer tokens. Generate tokens with appropriate scopes and rotation policies. Store tokens securely and never expose them in configuration files or logs.

### CORS Settings

Configure CORS origins to restrict which web applications can connect to the RPC endpoint. Set `--rpc-cors` to a comma separated list of allowed origins. Use specific origins rather than wildcards in production.

## Docker Deployment

### Official Image

Pull the official Docker image from the container registry. Tag the image with the specific version rather than using the latest tag. Pin the digest for reproducible deployments.

### Docker Compose

Create a `docker-compose.yml` file defining the node service, volume mounts for persistent data, and port mappings. Include a health check that queries the RPC endpoint. Configure resource limits appropriate for your node type.

### Volume Management

Mount host directories or named volumes for blockchain data and configuration. Do not store blockchain data inside the container filesystem. Use separate volumes for different node types to prevent data corruption.

## Configuration File Structure

### Main Configuration

The configuration file uses TOML format. Top level sections include `chain`, `node`, `rpc`, `network`, and `consensus`. Each section contains key value pairs that override default settings.

### Chain Settings

Specify the chain specification file, sync mode, pruning configuration, and database settings. The `pruning` field accepts values of `archive` or a block count for pruned mode.

### Network Settings

Configure the P2P port, boot nodes, reserved nodes, and maximum peer count. The `boot_nodes` array lists node addresses used for initial peer discovery.

### RPC Settings

Define RPC interfaces, ports, CORS origins, and authentication requirements. The `methods` field can be set to `safe` or `unsafe` depending on whether administrative functions should be exposed.

## Cardano Integration

Midnight nodes interact with the Cardano blockchain as a partner chain. A Cardano node provides the settlement layer context. Run a Cardano node with DB Sync to index Cardano blocks and transactions that serve as inputs for Midnight state transitions.

### DB Sync Setup

Install PostgreSQL and create a database for Cardano DB Sync. Configure the DB Sync service to connect to the Cardano node socket. The sync process populates relational tables with decoded block and transaction data. Midnight nodes reference this data through the DB Sync API.

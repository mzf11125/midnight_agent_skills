---
name: midnight-node
description: Complete guide to Midnight Network node infrastructure covering node architecture based on Substrate with runtime pallets, consensus engine, P2P networking, and storage layer, node types including full node, archive node, RPC node, boot node, and validator node, runtime pallets for onchain logic, state management, contract execution, token handling, and governance, RPC interface with JSON-RPC endpoints, WebSocket connections, chain queries, transaction submission, and system operations, consensus mechanism using proof-of-stake with SPO participation, committee selection, epoch management, and D-parameter, setting up a full node with hardware requirements, installation, configuration, syncing, and pruning options, setting up a boot node for network bootstrapping and peer discovery, setting up an RPC node with endpoint configuration, rate limiting, authentication, and access control, Cardano integration with Cardano node setup, DB Sync, cross-chain communication, and reward addresses, node endpoints for Preprod, Preview, and Mainnet RPC with network identification and endpoint discovery, node configuration via command line flags, configuration file, environment variables, and runtime parameters, operations covering monitoring, logging, health checks, backup procedures, upgrade procedures, and emergency procedures, governance with on-chain governance, parameter changes, protocol upgrades, D-parameter history, and terms and conditions, error codes reference and troubleshooting for common operational issues, performance tuning for hardware optimization, database tuning, network optimization, and memory management, security considerations for firewall configuration, key management, TLS setup, access control, and node hardening, Docker deployment with container configuration, docker-compose, volume management, and health checks, version history with release notes, compatibility matrix, upgrade paths, and breaking changes, and monitoring setup with Prometheus metrics, Grafana dashboards, alerting rules, and log aggregation.
---

# Midnight Node Infrastructure

## Node Architecture Overview

Midnight nodes are built on the Substrate blockchain framework which provides a modular architecture for constructing blockchain networks. Each node consists of several layers that together implement the full Midnight protocol stack. The architecture follows a layered design where each layer provides specific services to the layer above it.

The foundation is the Substrate client which handles peer to peer networking, block import and export, transaction pool management, and the runtime execution environment. On top of the client sits the runtime which contains the Midnight specific business logic implemented as a collection of WebAssembly pallets.

The P2P networking layer uses the libp2p library to manage peer connections and message propagation. Nodes discover each other through boot nodes and maintain a mesh of connections that propagate blocks and transactions across the network.

The storage layer uses a key-value database with Merkle tree indexing to persist blockchain state. Support for multiple database backends allows operators to choose between performance and storage efficiency.

The consensus layer implements a proof of stake mechanism where stake pool operators produce blocks and a committee validates them. This layer coordinates block production scheduling, fork choice, and finality.

The runtime pallet layer contains the Midnight specific logic for token operations, contract execution, governance, and cross chain communication. These pallets run as WebAssembly in a sandboxed environment isolated from the host system.


## Node Types

### Full Node

A full node maintains a complete copy of the blockchain state and verifies every block and transaction. Full nodes do not produce blocks but they fully validate the chain and participate in consensus by observing and verifying block production.

Full nodes are the backbone of network decentralization. They provide state to light clients through the RPC interface and serve as the data source for indexers and explorers.

Hardware requirements for a full node include a multi core CPU, at least 16 GB of RAM, and fast SSD storage with at least 500 GB capacity. Network connectivity should be stable with reasonable bandwidth since the node must stay in sync with the chain.

### Archive Node

An archive node extends a full node by preserving the complete historical state at every block. While a full node can prune old state trie data that is no longer needed for current validation, an archive node retains everything.

Archive nodes require significantly more storage than full nodes. The storage requirements grow linearly with chain history and can reach several terabytes over time. Archive nodes are typically operated by infrastructure providers and explorers that need historical state access.

### RPC Node

An RPC node exposes the JSON-RPC and WebSocket interfaces for external clients to query chain state and submit transactions. RPC nodes may be full nodes or may delegate to full nodes behind them depending on the deployment architecture.

RPC nodes require additional resources for handling client requests and should be configured with rate limiting and authentication to prevent abuse. Public RPC endpoints should have strict rate limits while private RPC endpoints can be more permissive.

### Boot Node

A boot node serves as the initial entry point for new nodes joining the network. It provides the peer discovery service that new nodes use to find other peers and establish their initial connections.

Boot nodes do not need to maintain full blockchain state. They run a lightweight configuration that focuses on the P2P networking layer. Boot nodes should have high availability and stable well known addresses that are hardcoded in node configurations.

### Validator Node

A validator node participates in block production and consensus. It holds the keys for a stake pool and signs blocks that are validated by the committee. Validator nodes have strict security requirements since compromise of validator keys can lead to slashing penalties.

Validator nodes should run on dedicated hardware with redundant power and network connectivity. Key management should use hardware security modules or secure enclaves to protect signing keys from extraction. Validator nodes should also run with limited RPC exposure to reduce attack surface.


## Runtime Pallets

### Onchain Logic

The Midnight runtime comprises multiple pallets that each implement a specific domain of onchain logic. Pallets are compiled to WebAssembly and executed by the Substrate runtime environment. This modular design allows upgrading individual pallets without affecting others.

Key pallets include the contracts pallet for Compact contract execution, the balances pallet for token management, the zswap pallet for shielded transactions, and the governance pallet for onchain decision making.

### State Management

The state management pallets handle the creation, reading, updating, and deletion of onchain state. Public state is stored in the blockchain state trie and is readable by any observer. Private state is not stored on chain but is managed through the Zswap protocol.

State queries are served through the RPC interface using the state pallet. The pallet supports both direct key lookups and prefix based iteration for efficient state enumeration.

### Contract Execution

The contracts pallet handles the deployment and execution of Compact smart contracts. It manages contract accounts, executes contract methods, and enforces the gas metering and fee schedule.

Contract execution occurs in the guaranteed phase for public operations and in the fallible phase for private operations that involve ZK proofs. The pallet coordinates between phases and manages the rollback behavior when operations fail.

### Token Handling

The token pallet manages the native NIGHT token including transfers, balance queries, and fee payment. It also manages DUST tokens which are a separate asset used for transaction fee payment.

Token operations are integrated with the shielded transaction system so that token transfers can be either public or private. The pallet tracks token supply and enforces the monetary policy parameters.

### Governance

The governance pallet enables onchain parameter changes and protocol upgrades. Stakeholders can propose changes, vote on proposals, and execute approved changes. The governance system uses a council and referendum model with configurable voting periods and thresholds.

Governance parameters include the D parameter which controls transaction fees, the epoch length for block production scheduling, and the committee size for consensus validation.


## RPC Interface

### JSON-RPC Endpoints

Midnight nodes expose JSON-RPC endpoints for programmatic access to chain data and transaction submission. The endpoints follow a standard method naming convention of `namespace_method`. Common namespaces include `chain`, `state`, `system`, `author`, and `contract`.

```bash
curl -X POST http://localhost:9933 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"chain_getBlock","params":[],"id":1}'
```

The `chain` namespace provides methods for querying block headers and bodies and subscribing to new block events.

The `state` namespace provides methods for querying storage keys and values. State queries can target specific pallets and storage items.

The `system` namespace provides methods for node health, peer information, and network status.

The `author` namespace provides methods for transaction submission and validation.

The `contract` namespace provides methods for contract deployment and call encoding.

### WebSocket Connections

WebSocket connections enable subscription based access to chain events and state changes. Clients subscribe to event types and receive push notifications when matching events occur.

```javascript
const ws = new WebSocket('ws://localhost:9944');
ws.send(JSON.stringify({
  jsonrpc: '2.0',
  method: 'chain_subscribeNewHeads',
  params: [],
  id: 1
}));
```

### Chain Queries

Chain queries retrieve information about blocks, transactions, and accounts. The `chain_getBlock` method retrieves a block by hash or number. The `chain_getBlockHash` method resolves a block number to its hash. The `chain_getFinalizedHead` method returns the hash of the latest finalized block.

### Transaction Submission

Transaction submission sends signed transactions to the node for inclusion in a block. The `author_submitExtrinsic` method accepts a raw signed transaction and broadcasts it to the network.

Transactions must be properly constructed with the correct nonce, signature, and metadata. The SDK libraries handle transaction construction automatically but the RPC interface allows direct submission for custom integrations.

### System Operations

System operations include node health checks, peer management, and network state queries. The `system_health` method returns whether the node is syncing and has peers. The `system_peers` method lists connected peers. The `system_name` and `system_version` methods return node identification information.


## Consensus Mechanism

### Proof of Stake

Midnight uses a proof of stake consensus mechanism where stake pool operators produce and validate blocks. SPOs stake tokens to participate in consensus and receive rewards proportional to their stake.

The consensus protocol separates block production from finality. Block production follows a slot based schedule where each slot is assigned to a specific SPO. Finality is achieved through a committee based mechanism where a rotating committee votes on blocks.

### SPO Participation

Stake pool operators register their pools through an onchain process. Registration requires a minimum stake amount and provides a pledge of the operator's own tokens. Delegators can assign their tokens to pools to earn rewards while contributing to network security.

SPOs must run validator nodes with high availability to fulfill their block production duties. Missing block production slots results in reduced rewards but not slashing. Malicious behavior such as double signing results in slashing of the operator's stake.

### Committee Selection

The consensus committee is a rotating set of validators that votes on block finality. Committee members are selected randomly weighted by stake at the beginning of each epoch. The committee size is a governance parameter that balances finality speed against security.

Committee members must be online to vote and earn rewards. Members who miss votes receive reduced rewards. The committee operates on a schedule within each epoch with specific slots for proposal, voting, and confirmation.

### Epoch Management

An epoch is a fixed number of slots that defines the block production and committee rotation schedule. At the beginning of each epoch the SPO slot assignments and committee membership are recalculated based on current stake distribution.

Epoch transitions trigger several housekeeping operations including reward distribution, parameter updates from governance, and stale data cleanup. The epoch length is a governance parameter typically set to balance operational overhead against stake churn.

### D Parameter

The D parameter controls the DUST cost of transactions on the Midnight Network. It functions as an adaptive fee mechanism that adjusts based on network conditions. When the network is congested the D parameter increases to raise transaction costs and reduce demand. When the network has spare capacity the D parameter decreases.

The D parameter is adjusted by governance and through an automatic mechanism that monitors network utilization. Understanding the D parameter is important for node operators since it affects the economic viability of operations.


## Setting Up a Full Node

### Hardware Requirements

A Midnight full node requires a modern multi core CPU with at least 4 physical cores. Recommended CPUs include Intel Xeon or AMD EPYC series processors. The node can utilize multiple cores for parallel block verification and execution.

Memory requirements start at 16 GB RAM for a full node with some pruning. For archive nodes 32 GB or more is recommended since the full state must be kept in memory or quickly accessible from disk.

Storage requirements depend on the pruning configuration. A pruned full node needs approximately 500 GB of fast SSD storage. An archive node may need several terabytes. NVMe SSDs provide the best performance for database operations.

Network connectivity should provide at least 100 Mbps with low latency. Monthly bandwidth usage can reach several terabytes on a busy node. A stable public IP address is recommended for better peer connectivity.

### Installation Steps

Install the Midnight node binary by downloading from the official release page or building from source. Binary downloads are available for Linux x86_64 and ARM64 platforms.

```bash
wget https://releases.midnight.network/node/latest/midnight-node-linux-x86_64.tar.gz
tar xzf midnight-node-linux-x86_64.tar.gz
sudo mv midnight-node /usr/local/bin/
```

Building from source requires Rust and the Substrate development toolchain. Clone the repository and use cargo to build the binary.

```bash
git clone https://github.com/midnight-ntwrk/midnight-node.git
cd midnight-node
cargo build --release
```

### Configuration

Create a configuration directory and initialize the default configuration file. The configuration file controls all node parameters including network, RPC, database, and consensus settings.

```bash
midnight-node init --base-path /var/lib/midnight --chain preprod
```

### Syncing

Start the node and allow it to sync with the network. Full sync downloads and verifies all blocks from genesis. Fast sync downloads the latest state snapshot and verifies a smaller set of recent blocks.

```bash
midnight-node \
  --base-path /var/lib/midnight \
  --chain preprod \
  --sync full \
  --name "my-full-node"
```

### Pruning Options

Pruning controls how much historical state the node retains. Archive mode retains all state. Pruned mode retains state for a configurable number of recent blocks. Light mode retains only the current state.

```bash
midnight-node --pruning 1000
```


## Setting Up a Boot Node

### Network Bootstrapping

Boot nodes are the initial contact points for new nodes joining the network. Configure the boot node by specifying its own address and providing the addresses of other boot nodes for redundancy.

```bash
midnight-node \
  --bootnodes /ip4/1.2.3.4/tcp/30333/p2p/12D3KooWNodeId1 \
  --node-key-file /etc/midnight/node-key
```

### Peer Discovery

Boot nodes participate in the Kademlia distributed hash table for peer discovery. They maintain a routing table of known peers and respond to discovery queries from new nodes.

The boot node configuration should specify a reasonable maximum number of peers to maintain. Too many peers consumes excessive resources while too few reduces the effectiveness of peer discovery.

```bash
midnight-node --out-peers 50 --in-peers 100
```

### Configuration

Boot nodes do not need to maintain full blockchain state. Configure them as light client peers that store only the minimum state needed for peer discovery and network health monitoring.

```bash
midnight-node \
  --light \
  --no-telemetry \
  --bootnodes /ip4/other-boot-node/tcp/30333/p2p/PeerId
```

### Security Considerations

Boot nodes are public facing infrastructure that must be protected against DDoS attacks and unauthorized access. Use firewall rules to restrict access to the P2P port only. Run boot nodes on dedicated hosts with no other services.

Monitor boot node health continuously. A compromised or unavailable boot node degrades the network's ability to onboard new nodes. Maintain multiple boot nodes with geographic diversity for resilience.


## Setting Up an RPC Node

### Endpoint Configuration

Configure RPC endpoints with appropriate CORS settings and connection limits. Public RPC endpoints require strict limits while private endpoints can be more permissive.

```bash
midnight-node \
  --rpc-cors all \
  --rpc-external \
  --rpc-max-connections 100 \
  --ws-external \
  --ws-max-connections 100
```

### Rate Limiting

Implement rate limiting to prevent abuse of public RPC endpoints. The node provides built in rate limiting that can be configured with maximum request rates per IP address.

```bash
midnight-node \
  --rpc-rate-limit 100 \
  --rpc-rate-limit-window 60
```

### Authentication

Secure sensitive RPC methods behind authentication. The node supports API key authentication where clients provide a key in the HTTP headers.

### Public vs Private Access

Public RPC endpoints should expose only safe methods that do not consume excessive resources. Private RPC endpoints can expose administrative methods. Separate endpoints or separate nodes should be used for public and private access.

Public endpoint safe methods include `chain_getBlock`, `state_getStorage`, and `system_health`. Administrative methods like node control and key management should only be available on private endpoints.


## Cardano Integration

### Cardano Node Setup

Midnight integrates with Cardano as a partner chain. A Cardano node provides the cross chain communication bridge between the Midnight and Cardano networks. The Cardano node must be synced to the same network stage as the Midnight node.

```bash
cardano-node run \
  --config /etc/cardano/preprod/config.json \
  --topology /etc/cardano/preprod/topology.json \
  --database-path /var/lib/cardano/db \
  --socket-path /var/lib/cardano/node.socket
```

### Cardano DB Sync

Cardano DB Sync indexes Cardano blockchain data into a PostgreSQL database for efficient querying. This is required for certain Midnight operations that reference Cardano state.

Setup involves running a Cardano node in parallel with the DB Sync service. The DB Sync service connects to the node through the UNIX socket and populates the database.

### Cross-Chain Communication

Cross chain communication between Midnight and Cardano uses bridge transactions that are validated on both chains. The Midnight node monitors Cardano for relevant transactions and encodes Cardano state references in Midnight blocks.

### Reward Addresses

SPO reward addresses link Midnight validator keys to Cardano payment addresses. Rewards earned through Midnight consensus are distributed to the associated Cardano address. The address mapping is registered on chain and can be updated by the SPO.


## Node Endpoints

### Preprod RPC

The preprod test network provides the most realistic testing environment before mainnet deployment. Preprod endpoints are stable and long lived with regular maintenance.

```
RPC: wss://rpc.preprod.midnight.network
Indexer: https://indexer.preprod.midnight.network/api/v1/graphql
Proof Server: https://proof-server.preprod.midnight.network
```

### Preview RPC

The preview test network runs newer node versions that have not yet reached preprod. Preview is useful for testing upcoming features and upgrades.

```
RPC: wss://rpc.preview.midnight.network
Indexer: https://indexer.preview.midnight.network/api/v1/graphql
```

### Mainnet RPC

Mainnet is the production network with real economic value. Mainnet endpoints should be used for production applications only after thorough testing on preprod.

```
RPC: wss://rpc.mainnet.midnight.network
Indexer: https://indexer.mainnet.midnight.network/api/v1/graphql
```

### Network Identification

Each network has a unique chain identifier and genesis hash that distinguishes it from other networks. Nodes verify the genesis hash on startup to ensure they are connected to the correct network.

### Endpoint Discovery

Nodes discover RPC and indexer endpoints through the network configuration. The configuration is distributed through the node source code and updated with each release. DApps should use environment variables rather than hardcoded endpoints to enable network switching.


## Node Configuration

### Command Line Flags

Node behavior is configured through command line flags passed at startup. The most important flags control the base path, network chain, RPC settings, and sync strategy.

```bash
midnight-node \
  --base-path /var/lib/midnight \
  --chain mainnet \
  --name "production-node" \
  --validator \
  --rpc-cors all \
  --rpc-external \
  --ws-external \
  --prometheus-external
```

### Configuration File

Configuration can be specified through a TOML configuration file instead of command line flags. This is preferred for production deployments where configuration is managed through infrastructure as code.

```toml
[network]
name = "production-node"
port = 30333

[rpc]
port = 9933
cors = ["all"]
external = true

[state]
base-path = "/var/lib/midnight"
chain = "mainnet"
pruning = 1000
```

### Environment Variables

Some configuration options can be set through environment variables. This is useful for containerized deployments where configuration is injected through the container orchestration system.

### Runtime Parameters

Runtime parameters that control consensus behavior are configured through governance rather than node startup flags. These include the D parameter, epoch length, committee size, and fee schedule. Node operators observe these parameters but do not directly set them.


## Operations

### Monitoring

Node monitoring tracks key metrics including block height, sync status, peer count, memory usage, CPU utilization, and disk I/O. Metric collection is essential for detecting issues before they affect service.

Prometheus metrics are exposed on a dedicated metrics port. Configure the Prometheus endpoint and set up alerting rules for critical conditions such as falling out of sync or running out of disk space.

### Logging

Structured logging using JSON format enables log aggregation and analysis. Configure the log level to balance visibility against noise. Production nodes typically run at info level while debugging sessions may use debug or trace levels.

```bash
midnight-node --log info,midnight=debug,runtime=info
```

### Health Checks

Health check endpoints report node status to load balancers and monitoring systems. A healthy node is synced with the network and has a minimum number of connected peers.

The `system_health` RPC method returns a simple health status. More detailed health checks should verify specific conditions relevant to the node's role.

### Backup Procedures

Regular backups protect against data loss from hardware failure or corruption. Backup procedures should cover the database files and the node configuration.

For validator nodes also back up the session keys and any other cryptographic material needed for recovery. Store backups in multiple geographically separated locations.

### Upgrade Procedures

Node upgrades follow a planned maintenance window approach. Before an upgrade verify compatibility of the new version with the current chain state. Run the new version on a test node before upgrading production nodes.

Upgrade steps include stopping the node gracefully, backing up current state, installing the new binary, and restarting with the existing data directory. Monitor the node after upgrade for any issues.

### Emergency Procedures

Emergency procedures cover scenarios such as chain forks, database corruption, and security incidents. Each scenario should have a documented response plan with specific steps and responsible personnel.

For chain forks follow the network governance guidance on which fork to follow. For database corruption restore from the most recent backup. For security incidents follow the incident response plan that protects keys and prevents further compromise.


## Governance

### On-Chain Governance

Midnight uses on chain governance for parameter changes and protocol upgrades. Governance participants include token holders who can vote on proposals and the technical committee who can fast track urgent changes.

Proposals go through a lifecycle of submission, voting, and enactment. Successful proposals are automatically enacted by the runtime without requiring a node restart.

### Parameter Changes

Governance can modify most runtime parameters through on chain proposals. Common parameter changes include adjusting the D parameter, modifying fee schedules, and updating consensus parameters.

Parameter changes take effect at the next epoch boundary after enactment. This gives operators time to adjust their configurations in response to changes.

### Protocol Upgrades

Protocol upgrades involve deploying new runtime code through governance. The new runtime is uploaded as a WASM blob and enacted after approval. Nodes automatically execute the new runtime without requiring manual intervention.

Upgrades can be coordinated across the network through the governance system. The upgrade process includes a pre upgrade notification period, an enactment block, and a post upgrade monitoring period.

### D-Parameter History

The D parameter evolves over time through governance decisions. Each change is recorded on chain with the new value, the proposal that enacted it, and the block height at which it took effect.

Historical D parameter values are useful for analyzing network economics and predicting future adjustments. The governance dashboard tracks D parameter changes alongside network utilization metrics.

### Terms and Conditions

Node operators are bound by the Midnight network terms and conditions which are published with each protocol upgrade. Operators should review terms updates as part of the upgrade preparation process.


## Error Codes

### Node Error Reference

The node emits error codes for common failure scenarios. Understanding these codes helps operators diagnose and resolve issues quickly.

Block import errors indicate problems with incoming blocks that may suggest a fork or corrupted data. Transaction validation errors indicate that submitted transactions are malformed or invalid. Network errors indicate connectivity issues with peers.

### Troubleshooting

Common operational issues and their resolutions are documented in the troubleshooting guide. Issues covered include sync stuck, high memory usage, slow block import, and peer connectivity problems.

For sync stuck issues check network connectivity and peer count. For high memory usage consider increasing pruning aggressiveness or adding RAM. For slow block import verify that the database is on SSD storage. For peer connectivity check firewall rules and network configuration.

### Recovery Steps

Recovery steps vary by failure mode. For database corruption stop the node, restore from backup, and restart. For chain fork issues follow network guidance and possibly resync. For key compromise rotates keys through governance and restore from secure backup.


## Performance Tuning

### Hardware Optimization

Optimize hardware selection based on the node's role. Validator nodes prioritize CPU performance for fast block production. Archive nodes prioritize storage I/O for handling large state databases. RPC nodes prioritize network throughput for handling client requests.

Consider NUMA aware CPU pinning to improve cache locality. Use memory interleaving across memory channels for maximum bandwidth. Select NVMe storage with high IOPS ratings for database workloads.

### Database Tuning

The node database can be tuned for different workloads. Increase the database cache size to reduce disk reads for frequently accessed data. Adjust the compression level to balance storage efficiency against CPU usage.

Consider running the database on a dedicated storage volume to isolate I/O from system operations. Use a file system with direct I/O support to bypass the operating system page cache for database operations.

### Network Optimization

Network performance depends on peer selection and connection management. Configure outbound connection limits based on available bandwidth. Use static peers for critical connections to ensure stable connectivity.

Consider network interface bonding for increased throughput and redundancy. Use QoS rules to prioritize node traffic over other services on shared network interfaces.

### Memory Management

Memory usage is dominated by the database cache and the runtime state cache. Configure memory limits to prevent the node from consuming all system memory under heavy load. Use memory monitoring to detect memory leaks in long running nodes.

Consider using huge pages for the database memory allocation to improve TLB efficiency. Set appropriate memory limits in containerized deployments to allow graceful degradation under memory pressure.


## Security

### Firewall Configuration

Configure firewall rules to restrict access to node ports. The P2P port must be accessible from the public internet for peer connectivity. The RPC port should be restricted to trusted networks or localhost only.

```bash
ufw allow 30333/tcp
ufw allow from 10.0.0.0/8 to any port 9933
ufw enable
```

### Key Management

Protect node keys using hardware security modules or secure key management services. Session keys should be generated on the node and stored with restricted permissions. Validator keys should ideally be stored in HSMs that perform signing operations without exposing the key material.

Never store keys in version control or configuration management systems. Use secrets management tools to inject keys at deployment time.

### TLS Setup

Enable TLS for RPC endpoints to encrypt client communication. Use certificates from a trusted certificate authority for public endpoints. Configure mutual TLS for backend service communication where both client and server authenticate.

```bash
midnight-node \
  --rpc-cert /etc/ssl/certs/node.crt \
  --rpc-key /etc/ssl/private/node.key
```

### Access Control

Implement access control at multiple layers. File system permissions should restrict access to node data directories. RPC access should be controlled through authentication and authorization. Administrative access should require multi factor authentication.

### Node Hardening

Follow security hardening best practices for the host operating system. Run the node as a dedicated user with minimal privileges. Disable unnecessary services and remove unused packages. Apply security updates promptly.

Use SELinux or AppArmor to confine the node process. Configure audit logging to detect unauthorized access attempts. Regularly scan for vulnerabilities in the node binary and its dependencies.


## Docker Deployment

### Container Configuration

Run Midnight nodes in Docker containers for consistent and reproducible deployments. Use the official Docker image from the Midnight container registry.

```dockerfile
FROM midnightntwrk/midnight-node:latest
COPY config.toml /etc/midnight/config.toml
ENTRYPOINT ["midnight-node", "--config", "/etc/midnight/config.toml"]
```

### Docker Compose

Docker Compose manages multi container deployments including the node, monitoring stack, and supporting services.

```yaml
version: '3.8'
services:
  node:
    image: midnightntwrk/midnight-node:latest
    volumes:
      - node-data:/var/lib/midnight
      - ./config.toml:/etc/midnight/config.toml
    ports:
      - "30333:30333"
      - "9933:9933"
      - "9944:9944"
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"

volumes:
  node-data:
```

### Volume Management

Persist node data in Docker volumes to survive container restarts and updates. Use named volumes for production deployments and bind mounts for development.

Backup Docker volumes by stopping the container and copying the volume data. Consider using volume plugins that support snapshot backups.

### Health Checks

Configure Docker health checks to monitor node status within the container. The health check can call the RPC health endpoint to verify the node is running and synced.

```yaml
healthcheck:
  test: ["CMD", "curl", "-s", "http://localhost:9933/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```


## Version History

### Release Notes

Each node release includes detailed release notes documenting new features, bug fixes, performance improvements, and breaking changes. Review release notes before upgrading to understand the impact on your deployment.

Release notes are published on the Midnight GitHub releases page and include upgrade instructions when manual intervention is needed.

### Compatibility Matrix

The compatibility matrix documents which node versions are compatible with which network stages. Some networks require specific node versions while others support multiple versions.

Check the compatibility matrix before upgrading to ensure the new version supports your target network. Running an incompatible version may cause the node to fail to sync or produce invalid blocks.

### Upgrade Paths

Direct upgrades are supported between consecutive versions. Upgrades skipping multiple versions may require intermediate steps. The release notes specify the supported upgrade paths.

Test upgrades on a non critical node before upgrading production validators. Keep backups of the current state before performing any upgrade.

### Breaking Changes

Breaking changes are documented in release notes with migration guides. Common breaking changes include database format changes requiring a resync, API changes affecting client compatibility, and configuration changes requiring updates.

Plan upgrades during maintenance windows when breaking changes are involved. Notify downstream consumers such as indexers and explorers when API breaking changes are introduced.


## Monitoring Setup

### Prometheus Metrics

Midnight nodes expose Prometheus metrics on a configurable port. Key metrics include block height, sync status, peer count, transaction count, memory usage, and database size.

Configure Prometheus to scrape the metrics endpoint at regular intervals. Set up recording rules for derived metrics such as sync drift and transaction throughput.

### Grafana Dashboards

Pre built Grafana dashboards visualize key node metrics. Import the dashboards from the Midnight monitoring repository and customize for your deployment.

Dashboards cover node health, sync performance, peer connectivity, resource utilization, and transaction metrics. Set up dashboard alerts for critical conditions.

### Alerting Rules

Configure Prometheus alerting rules for conditions that require operator attention. Critical alerts include node out of sync, disk space low, peer count below minimum, and excessive memory usage.

Route alerts to appropriate notification channels such as email, Slack, or pager systems. Set up on call rotations for production node incidents.

### Log Aggregation

Aggregate node logs to a central logging system such as Elasticsearch or Loki for search and analysis. Configure log shipping from all nodes to the aggregation system.

Set up log based alerts for error patterns and security events. Use log analysis to identify trends such as increasing error rates or performance degradation.

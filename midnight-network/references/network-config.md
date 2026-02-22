# Network Configuration

## Network IDs

### Mainnet
- Network ID: `mainnet`
- Chain ID: `1`
- Status: Coming soon

### Testnet
- Network ID: `testnet`
- Chain ID: `2`
- Status: Active

### Preprod
- Network ID: `preprod`
- Chain ID: `3`
- Status: Active (pre-production testing)

## Endpoints

### Testnet
```
Node RPC: https://rpc.testnet.midnight.network
Node WS: wss://ws.testnet.midnight.network
Indexer: https://indexer.testnet.midnight.network/graphql
Proof Server: https://prover.testnet.midnight.network
```

### Preprod
```
Node RPC: https://rpc.preprod.midnight.network
Node WS: wss://ws.preprod.midnight.network
Indexer: https://indexer.preprod.midnight.network/graphql
Proof Server: https://prover.preprod.midnight.network
```

## Node Configuration

### Basic Config
```yaml
network:
  id: testnet
  listen: 0.0.0.0:30333
  external: your-ip:30333
  bootnodes:
    - /dns4/bootnode1.testnet.midnight.network/tcp/30333/p2p/...
    - /dns4/bootnode2.testnet.midnight.network/tcp/30333/p2p/...

rpc:
  enabled: true
  port: 9933
  cors: ["*"]

ws:
  enabled: true
  port: 9944
  cors: ["*"]
```

### Validator Config
```yaml
validator:
  enabled: true
  keys: /path/to/validator-keys.json
  stake: 1000000

telemetry:
  enabled: true
  url: wss://telemetry.midnight.network/submit
```

## Substrate Configuration

### Substrate URI
Format: `wss://node.network.midnight.network`

Used for:
- Wallet connections
- DApp integrations
- Block explorers

## Firewall Rules

### Inbound
- 30333: P2P networking
- 9933: RPC (if public)
- 9944: WebSocket (if public)

### Outbound
- Allow all (for peer discovery)

## Network Parameters

### Block Time
- Target: 6 seconds
- Actual: ~6-8 seconds

### Block Size
- Max: 5MB
- Typical: 1-2MB

### Transaction Fees
- Base fee: Dynamic
- Priority fee: User-set
- Fee token: Night (NIGHT)

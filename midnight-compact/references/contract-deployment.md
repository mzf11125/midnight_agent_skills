# Contract Deployment Guide

## Overview

Complete guide to deploying Compact smart contracts to Midnight Network. Covers local development, testnet deployment, and production mainnet deployment.

## Prerequisites

### Required Tools

```bash
# Compact compiler (v0.19+)
compact --version

# Node.js (v18+)
node --version

# Docker (for local infrastructure)
docker --version

# Midnight CLI
npm install -g @midnight-ntwrk/cli
```

### Install Compact Compiler

```bash
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh

compact update +0.19.0
```

## Local Development

### 1. Start Local Infrastructure

```bash
# Using Docker Compose
docker-compose up -d

# Or using Midnight CLI
midnight-cli start-local
```

**Services started**:
- Midnight Node: `ws://127.0.0.1:9944`
- Indexer: `http://127.0.0.1:8088`
- Proof Server: `http://127.0.0.1:6300`

### 2. Compile Contract

```bash
cd my-contract
compact build
```

**Output**:
- `build/contract.wasm` - WebAssembly module
- `build/circuit.zkey` - ZK circuit proving key
- `build/contract.json` - Contract metadata

### 3. Deploy Locally

```bash
# Using Midnight CLI
midnight-cli deploy \
  --contract build/contract.wasm \
  --network local \
  --wallet dev

# Or using TypeScript
npm run deploy:local
```

**TypeScript deployment**:
```typescript
import { deployContract } from '@midnight-ntwrk/midnight-js-contracts';

const contractAddress = await deployContract({
  wasmPath: './build/contract.wasm',
  circuitPath: './build/circuit.zkey',
  network: 'local',
  wallet: devWallet
});

console.log('Contract deployed:', contractAddress);
```

## Testnet Deployment

### 1. Configure Environment

Create `.env`:
```env
MIDNIGHT_NETWORK=testnet
MIDNIGHT_MNEMONIC="your twelve word mnemonic phrase here"
MIDNIGHT_WALLET_ADDRESS="your_wallet_address"

# Network endpoints
MIDNIGHT_NODE_URL=wss://rpc.testnet.midnight.network
MIDNIGHT_INDEXER_URL=https://indexer.testnet.midnight.network
MIDNIGHT_PROOF_SERVER_URL=https://proof.testnet.midnight.network
```

### 2. Get Test Tokens

Visit [Midnight Faucet](https://faucet.testnet.midnight.network/):
1. Enter your wallet address
2. Request tDUST tokens
3. Wait for confirmation (~30 seconds)

**Check balance**:
```bash
midnight-cli balance --network testnet
```

### 3. Deploy to Testnet

```bash
# Compile contract
compact build

# Deploy
midnight-cli deploy \
  --contract build/contract.wasm \
  --network testnet \
  --wallet-mnemonic "$MIDNIGHT_MNEMONIC"
```

**With initialization parameters**:
```bash
midnight-cli deploy \
  --contract build/contract.wasm \
  --network testnet \
  --wallet-mnemonic "$MIDNIGHT_MNEMONIC" \
  --init-params '{"owner": "0x1234...", "initialValue": 100}'
```

### 4. Verify Deployment

```bash
# Check contract exists
midnight-cli contract-info \
  --address <contract-address> \
  --network testnet

# Query contract state
midnight-cli query \
  --contract <contract-address> \
  --method getState \
  --network testnet
```

## Mainnet Deployment

### 1. Pre-Deployment Checklist

- [ ] Contract audited by security firm
- [ ] All tests passing (unit, integration, e2e)
- [ ] Testnet deployment successful
- [ ] Gas costs estimated
- [ ] Wallet funded with sufficient DUST
- [ ] Backup of deployment keys
- [ ] Monitoring setup ready
- [ ] Rollback plan documented

### 2. Configure Mainnet

```env
MIDNIGHT_NETWORK=mainnet
MIDNIGHT_MNEMONIC="your mainnet mnemonic - KEEP SECURE"
MIDNIGHT_WALLET_ADDRESS="your_mainnet_address"

MIDNIGHT_NODE_URL=wss://rpc.mainnet.midnight.network
MIDNIGHT_INDEXER_URL=https://indexer.mainnet.midnight.network
MIDNIGHT_PROOF_SERVER_URL=https://proof.mainnet.midnight.network
```

### 3. Deploy to Mainnet

```bash
# Final compilation
compact build --release

# Deploy with confirmation
midnight-cli deploy \
  --contract build/contract.wasm \
  --network mainnet \
  --wallet-mnemonic "$MIDNIGHT_MNEMONIC" \
  --confirm
```

### 4. Post-Deployment

```bash
# Save contract address
echo "CONTRACT_ADDRESS=<address>" >> .env.production

# Verify on explorer
open "https://explorer.midnight.network/contract/<address>"

# Monitor initial transactions
midnight-cli logs \
  --contract <address> \
  --network mainnet \
  --follow
```

## Deployment Scripts

### Automated Deployment Script

**deploy.sh**:
```bash
#!/bin/bash
set -e

NETWORK=${1:-local}
CONTRACT_DIR=${2:-.}

echo "Deploying to $NETWORK..."

# Compile
cd "$CONTRACT_DIR"
compact build

# Deploy based on network
case $NETWORK in
  local)
    midnight-cli deploy \
      --contract build/contract.wasm \
      --network local \
      --wallet dev
    ;;
  testnet)
    midnight-cli deploy \
      --contract build/contract.wasm \
      --network testnet \
      --wallet-mnemonic "$MIDNIGHT_MNEMONIC"
    ;;
  mainnet)
    echo "⚠️  Deploying to MAINNET. Are you sure? (yes/no)"
    read -r confirm
    if [ "$confirm" = "yes" ]; then
      midnight-cli deploy \
        --contract build/contract.wasm \
        --network mainnet \
        --wallet-mnemonic "$MIDNIGHT_MNEMONIC" \
        --confirm
    else
      echo "Deployment cancelled"
      exit 1
    fi
    ;;
  *)
    echo "Unknown network: $NETWORK"
    exit 1
    ;;
esac

echo "✅ Deployment complete!"
```

**Usage**:
```bash
# Deploy to local
./deploy.sh local

# Deploy to testnet
./deploy.sh testnet ./my-contract

# Deploy to mainnet
./deploy.sh mainnet ./my-contract
```

### TypeScript Deployment

**deploy.ts**:
```typescript
import { deployContract, NetworkId } from '@midnight-ntwrk/midnight-js-contracts';
import { Wallet } from '@midnight-ntwrk/wallet';
import * as fs from 'fs';

async function deploy(network: NetworkId) {
  // Load wallet
  const wallet = await Wallet.fromMnemonic(
    process.env.MIDNIGHT_MNEMONIC!
  );
  
  // Load contract artifacts
  const wasm = fs.readFileSync('./build/contract.wasm');
  const circuit = fs.readFileSync('./build/circuit.zkey');
  
  console.log(`Deploying to ${network}...`);
  
  // Deploy
  const { contractAddress, txHash } = await deployContract({
    wasm,
    circuit,
    network,
    wallet,
    initParams: {
      owner: wallet.getAddress(),
      initialValue: 0
    }
  });
  
  console.log('✅ Deployment successful!');
  console.log('Contract Address:', contractAddress);
  console.log('Transaction Hash:', txHash);
  
  // Save to file
  fs.writeFileSync(
    `.env.${network}`,
    `CONTRACT_ADDRESS=${contractAddress}\n`,
    { flag: 'a' }
  );
  
  return contractAddress;
}

// Run
const network = process.argv[2] as NetworkId || 'local';
deploy(network).catch(console.error);
```

**Usage**:
```bash
# Deploy to local
npx ts-node deploy.ts local

# Deploy to testnet
npx ts-node deploy.ts testnet

# Deploy to mainnet
npx ts-node deploy.ts mainnet
```

## Network Configuration

### Local (Development)

```typescript
const config = {
  networkId: 'local',
  node: 'ws://127.0.0.1:9944',
  indexer: 'http://127.0.0.1:8088',
  proofServer: 'http://127.0.0.1:6300'
};
```

### Testnet

```typescript
const config = {
  networkId: 'testnet',
  node: 'wss://rpc.testnet.midnight.network',
  indexer: 'https://indexer.testnet.midnight.network',
  proofServer: 'https://proof.testnet.midnight.network'
};
```

### Mainnet

```typescript
const config = {
  networkId: 'mainnet',
  node: 'wss://rpc.mainnet.midnight.network',
  indexer: 'https://indexer.mainnet.midnight.network',
  proofServer: 'https://proof.mainnet.midnight.network'
};
```

## Frontend Integration

### Update Environment

After deployment, update frontend `.env`:
```env
VITE_CONTRACT_ADDRESS=0x1234567890abcdef...
VITE_NETWORK=testnet
```

### Connect to Contract

```typescript
import { Contract } from '@midnight-ntwrk/midnight-js-contracts';

const contract = new Contract({
  address: process.env.VITE_CONTRACT_ADDRESS,
  network: process.env.VITE_NETWORK,
  wallet: connectedWallet
});

// Call contract method
const result = await contract.call('increment', []);
```

## Troubleshooting

### Compilation Errors

```bash
Error: Failed to compile contract
```

**Solution**:
```bash
# Check Compact version
compact --version

# Update compiler
compact update +0.19.0

# Clean build
rm -rf build/
compact build
```

### Insufficient Funds

```bash
Error: Insufficient balance for deployment
```

**Solution**:
```bash
# Check balance
midnight-cli balance --network testnet

# Get test tokens
open https://faucet.testnet.midnight.network

# Wait for confirmation
midnight-cli balance --network testnet --watch
```

### Proof Server Timeout

```bash
Error: Proof generation timeout after 60s
```

**Solution**:
```typescript
// Increase timeout
const contract = await deployContract({
  // ...
  proofTimeout: 120000  // 2 minutes
});
```

### Contract Already Exists

```bash
Error: Contract at address already deployed
```

**Solution**:
- Use existing contract address
- Or deploy with different parameters
- Or use contract upgrade mechanism

### Network Connection Failed

```bash
Error: Failed to connect to node
```

**Solution**:
```bash
# Check network status
curl https://status.midnight.network

# Try different endpoint
MIDNIGHT_NODE_URL=wss://rpc2.testnet.midnight.network

# Check firewall/proxy settings
```

## Deployment Checklist

### Pre-Deployment
- [ ] Contract compiled successfully
- [ ] All tests passing
- [ ] Security audit completed (mainnet)
- [ ] Gas costs estimated
- [ ] Wallet funded
- [ ] Environment variables configured
- [ ] Backup of deployment keys

### During Deployment
- [ ] Correct network selected
- [ ] Contract address saved
- [ ] Transaction hash recorded
- [ ] Deployment verified on explorer

### Post-Deployment
- [ ] Contract state verified
- [ ] Frontend updated with address
- [ ] Monitoring enabled
- [ ] Documentation updated
- [ ] Team notified

## Best Practices

### 1. Use Environment Variables

```bash
# ✅ CORRECT
midnight-cli deploy --wallet-mnemonic "$MIDNIGHT_MNEMONIC"

# ❌ WRONG - hardcoded secrets
midnight-cli deploy --wallet-mnemonic "word1 word2 ..."
```

### 2. Test on Testnet First

```bash
# Always deploy to testnet before mainnet
./deploy.sh testnet
# Test thoroughly
./deploy.sh mainnet
```

### 3. Save Deployment Info

```bash
# Save contract address and tx hash
echo "CONTRACT_ADDRESS=$ADDRESS" >> .env.production
echo "DEPLOYMENT_TX=$TX_HASH" >> .env.production
echo "DEPLOYED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> .env.production
```

### 4. Verify Deployment

```bash
# Always verify after deployment
midnight-cli contract-info --address $ADDRESS --network mainnet
```

### 5. Monitor After Deployment

```bash
# Watch for errors
midnight-cli logs --contract $ADDRESS --follow
```

## Resources

- **Deployment Guide**: https://docs.midnight.network/guides/deployment
- **Network Configuration**: See network-configuration.md
- **Contract Examples**: See contract-examples.md (midnight-compact)
- **Testnet Faucet**: https://faucet.testnet.midnight.network
- **Mainnet Explorer**: https://explorer.midnight.network

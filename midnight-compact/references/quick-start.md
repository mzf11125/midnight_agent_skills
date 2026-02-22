# Quick Start Guide

## Your First Compact Contract in 10 Minutes

### Prerequisites

```bash
# Install Compact compiler
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh

# Verify installation
compact --version  # Should show v0.19+
```

### Step 1: Create Project

```bash
mkdir my-first-contract
cd my-first-contract
```

### Step 2: Write Contract

Create `counter.compact`:

```compact
pragma language_version >= 0.19;
import CompactStandardLibrary;

// Public ledger state
export ledger counter: Counter;

// Initialize counter to 0
constructor() {
  counter = 0;
}

// Increment counter by amount
export circuit increment(amount: Uint<16>): [] {
  counter.increment(amount);
}

// Get current counter value
export circuit getCount(): Uint<64> {
  return counter.read();
}
```

**What this does**:
- `counter: Counter` - Stores a number on-chain
- `increment()` - Increases the counter
- `getCount()` - Reads current value

### Step 3: Compile

```bash
compact build counter.compact
```

**Output**:
```
✓ Compiled successfully
  - counter.wasm (WebAssembly)
  - counter.zkey (ZK circuit)
  - counter.json (metadata)
```

### Step 4: Test Locally

Create `test.ts`:

```typescript
import { Contract } from './build/counter';

// Create contract instance
const contract = new Contract({});

// Initialize
const [privateState, publicState] = contract.initialState({});

// Test increment
const result = await contract.circuits.increment(
  { privateState, ledgerState: publicState },
  5
);

console.log('Counter:', result.publicState.counter);  // 5

// Test getCount
const count = await contract.circuits.getCount(
  { privateState: result.privateState, ledgerState: result.publicState }
);

console.log('Count:', count.result);  // 5
```

Run test:
```bash
npx ts-node test.ts
```

### Step 5: Deploy to Testnet

```bash
# Set environment
export MIDNIGHT_NETWORK=testnet
export MIDNIGHT_MNEMONIC="your twelve word mnemonic here"

# Deploy
midnight-cli deploy \
  --contract build/counter.wasm \
  --network testnet
```

**Output**:
```
✓ Contract deployed!
  Address: 0x1234567890abcdef...
  Transaction: 0xabcdef1234567890...
```

### Step 6: Interact with Contract

```typescript
import { Contract } from '@midnight-ntwrk/midnight-js-contracts';

const contract = new Contract({
  address: '0x1234567890abcdef...',
  network: 'testnet',
  wallet: connectedWallet
});

// Call increment
await contract.call('increment', [5]);

// Query count
const count = await contract.query('getCount');
console.log('Count:', count);  // 5
```

## Next Steps

### Add More Features

**Add decrement**:
```compact
export circuit decrement(amount: Uint<16>): [] {
  counter.decrement(amount);
}
```

**Add reset**:
```compact
export circuit reset(): [] {
  counter.resetToDefault();
}
```

**Add owner check**:
```compact
export sealed ledger owner: Bytes<32>;
witness local_secret_key(): Bytes<32>;

constructor() {
  counter = 0;
  owner = disclose(public_key(local_secret_key()));
}

export circuit increment(amount: Uint<16>): [] {
  const caller = public_key(local_secret_key());
  assert(disclose(caller == owner), "Not authorized");
  counter.increment(amount);
}
```

### Learn More

- **Language basics**: See language-basics.md
- **Type system**: See type-system.md
- **Best practices**: See best-practices.md
- **More examples**: See contract-examples.md

## Common Issues

### Compilation Error: "pragma not found"
```bash
# Update compiler
compact update +0.19.0
```

### Error: "counter.value() not found"
```compact
❌ counter.value()
✅ counter.read()
```

### Error: "Void is not defined"
```compact
❌ export circuit fn(): Void
✅ export circuit fn(): []
```

### Deployment Error: "Insufficient funds"
```bash
# Get test tokens
open https://faucet.testnet.midnight.network
```

## Complete Example Repository

See working example:
```bash
git clone https://github.com/midnight-examples/counter-contract
cd counter-contract
npm install
npm test
```

## What You Built

✅ A working Compact smart contract  
✅ Compiled to WebAssembly + ZK circuits  
✅ Tested locally  
✅ Deployed to testnet  
✅ Interacted with from TypeScript  

**Time**: ~10 minutes  
**Lines of code**: ~20 lines of Compact  

You're now ready to build more complex contracts!

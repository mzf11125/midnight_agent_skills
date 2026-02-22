# Testing Guide

## Overview

Complete guide to testing Midnight Network applications including Compact contracts, DApps, and infrastructure.

## Testing Compact Contracts

### Unit Testing

**Test framework**: Use Compact's built-in test framework

**test/counter.test.ts**:
```typescript
import { describe, it, expect } from '@midnight-ntwrk/compact-test';
import { Contract, Witnesses } from '../build/contract';

describe('Counter Contract', () => {
  let contract: Contract;
  let witnesses: Witnesses;
  
  beforeEach(() => {
    // Initialize contract with test witnesses
    witnesses = {
      local_secret_key: () => testSecretKey
    };
    
    contract = new Contract(witnesses);
  });
  
  it('should initialize with zero', async () => {
    const [privateState, publicState] = contract.initialState({});
    expect(publicState.counter).toBe(0n);
  });
  
  it('should increment counter', async () => {
    const [privateState, publicState] = contract.initialState({});
    
    const result = await contract.circuits.increment(
      { privateState, ledgerState: publicState },
      1n
    );
    
    expect(result.publicState.counter).toBe(1n);
  });
  
  it('should reject negative increment', async () => {
    const [privateState, publicState] = contract.initialState({});
    
    await expect(
      contract.circuits.increment(
        { privateState, ledgerState: publicState },
        -1n
      )
    ).rejects.toThrow('Amount must be positive');
  });
});
```

**Run tests**:
```bash
npm test
```

### Property-Based Testing

Test invariants hold across all inputs:

```typescript
import { fc, test } from '@fast-check/jest';

describe('Counter Properties', () => {
  test.prop([fc.nat()])('counter never negative', async (n) => {
    const [privateState, publicState] = contract.initialState({});
    
    const result = await contract.circuits.increment(
      { privateState, ledgerState: publicState },
      BigInt(n)
    );
    
    expect(result.publicState.counter).toBeGreaterThanOrEqual(0n);
  });
  
  test.prop([fc.nat(), fc.nat()])('increment is additive', async (a, b) => {
    const [privateState, publicState] = contract.initialState({});
    
    // Increment by a
    const result1 = await contract.circuits.increment(
      { privateState, ledgerState: publicState },
      BigInt(a)
    );
    
    // Then increment by b
    const result2 = await contract.circuits.increment(
      { privateState: result1.privateState, ledgerState: result1.publicState },
      BigInt(b)
    );
    
    // Should equal a + b
    expect(result2.publicState.counter).toBe(BigInt(a + b));
  });
});
```

### ZK Circuit Testing

Test zero-knowledge properties:

```typescript
describe('Privacy Properties', () => {
  it('should hide secret value', async () => {
    const secretValue = 42n;
    const [privateState, publicState] = contract.initialState({
      secretValue
    });
    
    // Public state should not reveal secret
    expect(publicState).not.toContain(secretValue);
    expect(JSON.stringify(publicState)).not.toContain('42');
  });
  
  it('should verify proof without revealing witness', async () => {
    const witness = generateWitness();
    
    const result = await contract.circuits.verifySecret(
      { privateState, ledgerState: publicState },
      witness
    );
    
    // Proof verifies but witness not in public output
    expect(result.result).toBe(true);
    expect(result.publicState).not.toContain(witness);
  });
  
  it('should produce valid proofs', async () => {
    const result = await contract.circuits.increment(
      { privateState, ledgerState: publicState },
      1n
    );
    
    // Verify proof is valid
    const isValid = await verifyProof(result.proof);
    expect(isValid).toBe(true);
  });
});
```

### Integration Testing

Test contract deployment and interaction:

```typescript
import { deployContract, Contract } from '@midnight-ntwrk/midnight-js-contracts';
import { Wallet } from '@midnight-ntwrk/wallet';

describe('Contract Integration', () => {
  let contractAddress: string;
  let wallet: Wallet;
  
  beforeAll(async () => {
    // Deploy contract to local testnet
    wallet = await Wallet.fromMnemonic(testMnemonic);
    
    contractAddress = await deployContract({
      wasmPath: './build/contract.wasm',
      circuitPath: './build/circuit.zkey',
      network: 'local',
      wallet
    });
  });
  
  it('should deploy successfully', () => {
    expect(contractAddress).toMatch(/^0x[a-fA-F0-9]{40}$/);
  });
  
  it('should call contract method', async () => {
    const contract = new Contract({
      address: contractAddress,
      network: 'local',
      wallet
    });
    
    const tx = await contract.call('increment', [1n]);
    expect(tx).toBeDefined();
    
    await waitForConfirmation(tx);
    
    const counter = await contract.query('getCounter');
    expect(counter).toBe(1n);
  });
});
```

## Testing DApps

### Frontend Testing

**Component tests** (React Testing Library):

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { WalletConnect } from './WalletConnect';

describe('WalletConnect', () => {
  it('should render connect button', () => {
    render(<WalletConnect />);
    expect(screen.getByText('Connect Wallet')).toBeInTheDocument();
  });
  
  it('should connect to wallet on click', async () => {
    const mockConnect = jest.fn();
    window.midnight = {
      wallet: {
        connect: mockConnect
      }
    };
    
    render(<WalletConnect />);
    fireEvent.click(screen.getByText('Connect Wallet'));
    
    await waitFor(() => {
      expect(mockConnect).toHaveBeenCalledWith('testnet');
    });
  });
  
  it('should display balance after connection', async () => {
    const mockAPI = {
      getShieldedBalances: jest.fn().mockResolvedValue({
        [DUST_TOKEN_TYPE]: 1000n
      })
    };
    
    render(<WalletConnect api={mockAPI} />);
    
    await waitFor(() => {
      expect(screen.getByText('Balance: 1000')).toBeInTheDocument();
    });
  });
});
```

### E2E Testing

**Playwright tests**:

```typescript
import { test, expect } from '@playwright/test';

test.describe('DApp E2E', () => {
  test('should connect wallet and send payment', async ({ page }) => {
    // Navigate to DApp
    await page.goto('http://localhost:3000');
    
    // Connect wallet
    await page.click('button:has-text("Connect Wallet")');
    await page.click('button:has-text("Midnight Wallet")');
    
    // Wait for connection
    await expect(page.locator('.wallet-connected')).toBeVisible();
    
    // Enter payment details
    await page.fill('input[name="recipient"]', testAddress);
    await page.fill('input[name="amount"]', '100');
    
    // Submit payment
    await page.click('button:has-text("Send")');
    
    // Wait for confirmation
    await expect(page.locator('.tx-success')).toBeVisible({ timeout: 30000 });
    
    // Verify transaction hash displayed
    const txHash = await page.locator('.tx-hash').textContent();
    expect(txHash).toMatch(/^0x[a-fA-F0-9]{64}$/);
  });
  
  test('should handle insufficient funds', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('button:has-text("Connect Wallet")');
    
    // Try to send more than balance
    await page.fill('input[name="amount"]', '999999999');
    await page.click('button:has-text("Send")');
    
    // Should show error
    await expect(page.locator('.error-message')).toContainText('Insufficient balance');
  });
});
```

### API Mocking

**Mock Midnight APIs**:

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  // Mock indexer
  rest.get('http://localhost:8088/blocks/latest', (req, res, ctx) => {
    return res(ctx.json({
      number: 12345n,
      hash: '0xabc...',
      transactions: []
    }));
  }),
  
  // Mock balance query
  rest.get('http://localhost:8088/balance/:address', (req, res, ctx) => {
    return res(ctx.json({
      balance: 1000n
    }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('should fetch balance', async () => {
  const balance = await getBalance(testAddress);
  expect(balance).toBe(1000n);
});
```

## Testing Infrastructure

### Node Testing

**Health check tests**:

```bash
#!/bin/bash

# Test node health
response=$(curl -s http://localhost:9933 -H "Content-Type: application/json" \
  -d '{"id":1, "jsonrpc":"2.0", "method":"system_health"}')

peers=$(echo $response | jq -r '.result.peers')
syncing=$(echo $response | jq -r '.result.isSyncing')

if [ "$peers" -lt 5 ]; then
  echo "FAIL: Low peer count: $peers"
  exit 1
fi

if [ "$syncing" = "true" ]; then
  echo "FAIL: Node still syncing"
  exit 1
fi

echo "PASS: Node healthy"
```

### Validator Testing

**Block production test**:

```typescript
import { getLatestBlock } from '@midnight-ntwrk/ledger';

describe('Validator', () => {
  it('should produce blocks', async () => {
    const block1 = await getLatestBlock(indexerUri);
    
    // Wait 30 seconds
    await sleep(30000);
    
    const block2 = await getLatestBlock(indexerUri);
    
    // Should have produced at least one block
    expect(block2.number).toBeGreaterThan(block1.number);
  });
  
  it('should not miss blocks', async () => {
    const blocks = await getBlocks(
      currentBlock - 100n,
      currentBlock,
      indexerUri
    );
    
    const validatorBlocks = blocks.filter(
      b => b.validator === validatorAddress
    );
    
    // Should have produced expected number of blocks
    const expectedBlocks = 100 / validatorCount;
    const missedBlocks = expectedBlocks - validatorBlocks.length;
    
    expect(missedBlocks).toBeLessThan(5); // < 5% miss rate
  });
});
```

### Indexer Testing

**Sync test**:

```typescript
describe('Indexer', () => {
  it('should sync with chain', async () => {
    const chainBlock = await getLatestBlock(nodeUri);
    const indexerStatus = await getIndexerStatus(indexerUri);
    
    const lag = chainBlock.number - indexerStatus.syncedBlock;
    
    expect(lag).toBeLessThan(10n);
  });
  
  it('should index transactions', async () => {
    // Submit transaction
    const txHash = await submitTransaction(tx, nodeUri);
    
    // Wait for indexing
    await sleep(10000);
    
    // Query from indexer
    const indexedTx = await getTransaction(txHash, indexerUri);
    
    expect(indexedTx).toBeDefined();
    expect(indexedTx.hash).toBe(txHash);
  });
});
```

## Performance Testing

### Load Testing

**Artillery config** (`load-test.yml`):

```yaml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Spike"

scenarios:
  - name: "Query balance"
    flow:
      - get:
          url: "/api/balance/{{ $randomString() }}"
  
  - name: "Submit transaction"
    flow:
      - post:
          url: "/api/transaction"
          json:
            to: "{{ $randomString() }}"
            amount: "{{ $randomNumber(1, 1000) }}"
```

**Run load test**:
```bash
artillery run load-test.yml
```

### Benchmark Testing

```typescript
import { performance } from 'perf_hooks';

describe('Performance', () => {
  it('should generate proof in < 5s', async () => {
    const start = performance.now();
    
    await contract.circuits.increment(
      { privateState, ledgerState: publicState },
      1n
    );
    
    const duration = performance.now() - start;
    
    expect(duration).toBeLessThan(5000);
  });
  
  it('should handle 100 concurrent queries', async () => {
    const queries = Array(100).fill(null).map(() =>
      contract.query('getCounter')
    );
    
    const start = performance.now();
    await Promise.all(queries);
    const duration = performance.now() - start;
    
    expect(duration).toBeLessThan(10000); // < 10s for 100 queries
  });
});
```

## Security Testing

### Vulnerability Scanning

```bash
# Scan dependencies
npm audit

# Fix vulnerabilities
npm audit fix

# Scan Docker images
docker scan midnight-node:latest
```

### Penetration Testing

**Test common vulnerabilities**:

```typescript
describe('Security', () => {
  it('should reject invalid signatures', async () => {
    const invalidTx = {
      ...validTx,
      signature: 'invalid'
    };
    
    await expect(
      submitTransaction(invalidTx)
    ).rejects.toThrow('Invalid signature');
  });
  
  it('should prevent replay attacks', async () => {
    const tx = await createTransaction();
    await submitTransaction(tx);
    
    // Try to submit same transaction again
    await expect(
      submitTransaction(tx)
    ).rejects.toThrow('Nonce already used');
  });
  
  it('should validate input bounds', async () => {
    await expect(
      contract.circuits.increment(
        { privateState, ledgerState: publicState },
        -1n
      )
    ).rejects.toThrow();
  });
});
```

## Test Coverage

### Measure Coverage

```bash
# Run tests with coverage
npm test -- --coverage

# View coverage report
open coverage/index.html
```

**Target coverage**:
- Statements: > 80%
- Branches: > 75%
- Functions: > 80%
- Lines: > 80%

### Coverage Configuration

**jest.config.js**:
```javascript
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}'
  ],
  coverageThresholds: {
    global: {
      statements: 80,
      branches: 75,
      functions: 80,
      lines: 80
    }
  }
};
```

## CI/CD Testing

### GitHub Actions

**.github/workflows/test.yml**:
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
  
  e2e:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Start local network
        run: docker-compose up -d
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Stop network
        run: docker-compose down
```

## Best Practices

### 1. Test Pyramid

```
       /\
      /E2E\      <- Few, slow, expensive
     /------\
    /  API  \    <- More, medium speed
   /--------\
  /  Unit   \   <- Many, fast, cheap
 /----------\
```

### 2. Test Isolation

```typescript
// ✅ CORRECT - isolated tests
beforeEach(() => {
  contract = new Contract(witnesses);
});

// ❌ WRONG - shared state
const contract = new Contract(witnesses);
```

### 3. Descriptive Test Names

```typescript
// ✅ CORRECT
it('should reject negative increment amounts', async () => {

// ❌ WRONG
it('test increment', async () => {
```

### 4. Test Edge Cases

```typescript
describe('Edge Cases', () => {
  it('should handle zero amount', async () => {
  it('should handle maximum uint64', async () => {
  it('should handle empty input', async () => {
});
```

### 5. Mock External Dependencies

```typescript
// ✅ CORRECT - mock external APIs
jest.mock('@midnight-ntwrk/ledger', () => ({
  getBalance: jest.fn().mockResolvedValue(1000n)
}));

// ❌ WRONG - real API calls in tests
const balance = await getBalance(address, realIndexerUri);
```

## Resources

- **Compact Testing**: https://docs.midnight.network/develop/testing
- **Jest Documentation**: https://jestjs.io/docs
- **Playwright**: https://playwright.dev
- **Artillery**: https://artillery.io
- **Contract Examples**: See contract-examples.md (midnight-compact)

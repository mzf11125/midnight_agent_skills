---
name: compact-cli-dev
description: Complete guide to CLI tooling, project scaffolding, and development environment setup for Midnight Network dApp projects. Use when users need to scaffold new projects, manage contracts via CLI, deploy contracts, manage wallets, run local devnet, use the Compact compiler, format code, integrate with VS Code or Neovim, set up CI/CD pipelines, configure testing frameworks, or handle Windows WSL setup for Compact development.
---

# CLI and Development Tooling

Complete guide to command-line interfaces project scaffolding and development environment setup for Midnight Network development.

## Project Scaffolding

### create-mn-app

The recommended way to bootstrap a new Midnight dApp project.

**Usage**:
```bash
npx create-mn-app my-dapp
cd my-dapp
npm install
```

**What It Creates**:
- Project directory with standard folder structure
- Contracts directory for .compact files
- Tests directory with vitest configuration
- CLI scaffolding with Oclif framework
- TypeScript configuration
- Docker Compose for local devnet
- .env file template
- GitHub Actions CI configuration

**Options**:
```bash
npx create-mn-app my-dapp --template basic
npx create-mn-app my-dapp --template counter
npx create-mn-app my-dapp --template token
npx create-mn-app my-dapp --network preprod
```

**Available Templates**:
- `basic`: Minimal contract with counter example
- `counter`: Full counter dApp with CLI and tests
- `token`: Token contract with shielded transfers
- `hello-world`: Simple hello world contract with vitest tests

### Project Structure After Scaffolding

```
my-dapp/
  contracts/
    src/
      counter.compact
    test/
      counter.test.ts
  src/
    cli/
      commands/
        deploy.ts
        interact.ts
        devnet.ts
      index.ts
    lib/
      contract.ts
      wallet.ts
      providers.ts
  docker/
    docker-compose.yml
  .env
  .env.example
  package.json
  tsconfig.json
  vitest.config.ts
  compact.json
```

### Manual Project Setup

For projects not using create-mn-app:

```bash
mkdir -p contracts/src contracts/test src/cli/commands
npm init -y
npm install --save-dev typescript vitest @midnight-ntwrk/compact-cli
npx tsc --init
```

Create `compact.json` at project root:
```json
{
  "compiler": "compactc",
  "version": ">=0.20",
  "contracts": "contracts/src",
  "output": "contracts/build",
  "test": "contracts/test"
}
```

## Oclif-Based CLI Patterns

Midnight projects use Oclif for building robust command-line interfaces.

### CLI Entry Point

```typescript
// src/cli/index.ts
import { Command } from '@oclif/core';

export class MidnightCLI extends Command {
  static description = 'Midnight dApp CLI';

  async run(): Promise<void> {
    this.log('Midnight CLI ready');
  }
}
```

### Command Structure

```typescript
// src/cli/commands/deploy.ts
import { Command, Flags } from '@oclif/core';
import { deployContract } from '../../lib/contract';

export default class Deploy extends Command {
  static description = 'Deploy contract to network';

  static flags = {
    network: Flags.string({
      char: 'n',
      options: ['local', 'preprod', 'mainnet'],
      default: 'local',
      description: 'Target network'
    }),
    contract: Flags.string({
      char: 'c',
      required: true,
      description: 'Contract file path'
    }),
    'output-dir': Flags.string({
      char: 'o',
      default: './contracts/build',
      description: 'Compilation output directory'
    })
  };

  async run(): Promise<void> {
    const { flags } = await this.parse(Deploy);
    this.log(`Deploying ${flags.contract} to ${flags.network}...`);
    const result = await deployContract(flags);
    this.log(`Deployed at: ${result.address}`);
  }
}
```

### Progress Output

```typescript
import { CliUx } from '@oclif/core';

async function deployWithProgress(contract: string, network: string) {
  CliUx.ux.action.start('Compiling contract');
  await compileContract(contract);
  CliUx.ux.action.stop('done');

  CliUx.ux.action.start('Generating ZK keys');
  await generateKeys();
  CliUx.ux.action.stop('done');

  CliUx.ux.action.start('Deploying to network');
  const result = await submitDeployTx(network);
  CliUx.ux.action.stop(`deployed at ${result.address}`);
}
```

### Configuration Management

```typescript
import { Config } from '../../lib/config';

export default class ConfigCommand extends Command {
  static description = 'Set configuration';

  async run(): Promise<void> {
    const config = Config.load(this.config.configDir);

    config.set('network', 'preprod');
    config.set('defaultContract', './contracts/src/counter.compact');
    config.save();

    this.log('Configuration updated');
  }
}
```

## Contract Deployment CLI

### deployContract Command

```typescript
import { deployContract as deploy } from '@midnight-ntwrk/compact-cli';

async function deployContract(
  compiledPath: string,
  constructorArgs: any[],
  network: string
): Promise<string> {
  const provider = await getProvider(network);
  const wallet = await getWallet(provider);

  const contract = await deploy(
    wallet,
    compiledPath,
    constructorArgs,
    { network }
  );

  return contract.address;
}
```

### findDeployedContract

```typescript
import { findDeployedContract } from '@midnight-ntwrk/compact-cli';

async function connectToContract(
  address: string,
  network: string
): Promise<DeployedContract> {
  const provider = await getProvider(network);
  const wallet = await getWallet(provider);

  const contract = await findDeployedContract(
    wallet,
    address,
    { network }
  );

  return contract;
}
```

### submitDeployTx

```typescript
async function submitDeployTx(
  compiledContract: CompiledContract,
  constructorArgs: any[],
  wallet: WalletFacade
): Promise<string> {
  const tx = await wallet.prepareDeployTransaction(
    compiledContract,
    constructorArgs
  );

  const signed = await wallet.signTransaction(tx);
  const txHash = await wallet.submitTransaction(signed);
  const receipt = await wallet.waitForConfirmation(txHash);

  return receipt.contractAddress;
}
```

### Deployment Verification

```typescript
async function verifyDeployment(
  contractAddress: string,
  expectedCode: Uint8Array,
  network: string
): Promise<boolean> {
  const provider = await getProvider(network);
  const onChainCode = await provider.getContractCode(contractAddress);
  return arraysEqual(onChainCode, expectedCode);
}
```

## Wallet Management CLI

### Create Wallet

```typescript
static description = 'Create a new wallet';

static flags = {
  name: Flags.string({
    char: 'n',
    description: 'Wallet name'
  }),
  password: Flags.string({
    char: 'p',
    description: 'Wallet encryption password'
  }),
  seed: Flags.string({
    char: 's',
    description: 'Mnemonic seed phrase (optional)'
  })
};

async run(): Promise<void> {
  const { flags } = await this.parse(CreateWallet);
  const wallet = await createWallet({
    name: flags.name,
    password: flags.password,
    seed: flags.seed
  });

  this.log(`Wallet created: ${wallet.address}`);
  this.log(`Public key: ${wallet.publicKey}`);
  this.log(`Save your seed phrase securely: ${wallet.mnemonic}`);
}
```

### Fund Wallet

```typescript
export default class FundWallet extends Command {
  static description = 'Request funds from faucet';

  static flags = {
    network: Flags.string({
      char: 'n',
      default: 'preprod',
      description: 'Network for the faucet request'
    }),
    address: Flags.string({
      char: 'a',
      description: 'Address to fund'
    })
  };

  async run(): Promise<void> {
    const { flags } = await this.parse(FundWallet);
    const faucet = getFaucetClient(flags.network);
    const result = await faucet.requestTokens(flags.address);
    this.log(`Funded ${flags.address} with ${result.amount} tNIGHT`);
  }
}
```

### Check Balances

```typescript
export default class Balance extends Command {
  static description = 'Check wallet balances';

  async run(): Promise<void> {
    const wallet = await loadActiveWallet();

    const nightBalance = await wallet.getNightBalance();
    const dustBalance = await wallet.getDustBalance();
    const shieldedBalance = await wallet.getShieldedBalance();

    this.log('Balance Summary:');
    this.log(`  DUST:     ${dustBalance.toString()}`);
    this.log(`  Unshielded NIGHT: ${nightBalance.unshielded}`);
    this.log(`  Shielded NIGHT:   ${nightBalance.shielded}`);
  }
}
```

### DUST Generation

```typescript
export default class GenerateDust extends Command {
  static description = 'Check DUST generation status';

  async run(): Promise<void> {
    const wallet = await loadActiveWallet();

    const generationRate = await wallet.getDustGenerationRate();
    const currentDust = await wallet.getDustBalance();
    const timeToTarget = calculateDustGenerationTime(
      currentDust,
      targetAmount,
      generationRate
    );

    this.log(`Generation Rate: ${generationRate} DUST/block`);
    this.log(`Current DUST: ${currentDust}`);
    this.log(`Time to 1000 DUST: ~${timeToTarget} minutes`);
  }
}
```

## Devnet Control

### Docker-Based Local Devnet

The local devnet runs Midnight nodes in Docker containers for fast development.

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  midnight-node:
    image: midnightntwrk/node:latest
    ports:
      - "9944:9944"
      - "9933:9933"
      - "9615:9615"
    volumes:
      - midnight-data:/data
    command: --dev --rpc-external --ws-external

  midnight-indexer:
    image: midnightntwrk/indexer:latest
    ports:
      - "8080:8080"
    environment:
      NODE_URL: http://midnight-node:9944
    depends_on:
      - midnight-node

  proof-server:
    image: midnightntwrk/proof-server:latest
    ports:
      - "6300:6300"
    environment:
      NODE_URL: http://midnight-node:9944
    depends_on:
      - midnight-node

volumes:
  midnight-data:
```

### CLI Commands for Devnet

```typescript
export default class Devnet extends Command {
  static description = 'Manage local devnet';

  async start(): Promise<void> {
    const { exec } = require('child_process');
    exec('docker-compose up -d', { cwd: './docker' }, (error, stdout) => {
      if (error) {
        this.error(`Failed to start devnet: ${error.message}`);
        return;
      }
      this.log('Devnet started');
      this.log('RPC: http://localhost:9944');
      this.log('Indexer: http://localhost:8080');
      this.log('Proof Server: http://localhost:6300');
    });
  }

  async stop(): Promise<void> {
    const { exec } = require('child_process');
    exec('docker-compose down', { cwd: './docker' }, (error) => {
      if (error) {
        this.error(`Failed to stop devnet: ${error.message}`);
        return;
      }
      this.log('Devnet stopped');
    });
  }

  async status(): Promise<void> {
    const { exec } = require('child_process');
    exec('docker-compose ps', { cwd: './docker' }, (error, stdout) => {
      if (error) {
        this.log('Devnet is not running');
        return;
      }
      this.log(stdout);
    });
  }
}
```

## Compiler CLI

### compactc Usage

The Compact compiler `compactc` converts .compact files into deployable contracts.

**Basic Compilation**:
```bash
compactc compile contracts/src/counter.compact --output-dir contracts/build
```

**With Optimization**:
```bash
compactc compile contracts/src/counter.compact --optimize --output-dir contracts/build
```

**With Debug Information**:
```bash
compactc compile contracts/src/counter.compact --debug --output-dir contracts/build
```

### Compiler Flags

```bash
compactc compile <file> [flags]

Flags:
  --output-dir <dir>      Output directory for compiled artifacts
  --optimize              Enable circuit optimizations
  --debug                 Include debug information
  --no-verify             Skip post-compilation verification
  --target <target>       Compilation target (default: zkir)
  --pragma <version>      Override pragma version
  --include <dir>         Add include directory
  --json-abi              Export ABI as JSON
  --typescript-types      Generate TypeScript type definitions
  --max-circuit-size <n>  Maximum circuit size in gates
```

### Output Files

Running `compactc compile` produces:
- `contract.compact.zki`: Zero-Knowledge Intermediate Representation
- `contract.verifier.key`: Verifier key for on-chain deployment
- `contract.prover.key`: Prover key for proof generation
- `contract.abi.json`: Contract Application Binary Interface (with --json-abi)
- `contract.types.ts`: TypeScript type definitions (with --typescript-types)

### Batch Compilation

```bash
compactc compile contracts/src/*.compact --output-dir contracts/build
compactc compile --project ./compact.json
```

### Watcher Mode

```bash
compactc watch contracts/src --output-dir contracts/build
```

Recompiles contracts automatically when source files change. Uses file system watchers for instant feedback.

## Compact Project Tool

### compact CLI

The `compact` command provides project management for Compact development.

```bash
compact init          # Initialize a new Compact project
compact build         # Compile all contracts
compact test          # Run contract tests
compact deploy        # Deploy contracts to network
compact clean         # Clean build artifacts
compact update        # Update dependencies
compact doctor        # Check development environment
```

### compact init

Creates a `compact.json` with project configuration:
```bash
compact init --name my-dapp --version 0.1.0
```

### compact build

Compiles contracts according to compact.json configuration:
```bash
compact build
compact build --optimize
compact build --contract counter
```

### compact test

Runs the test suite with vitest:
```bash
compact test
compact test --watch
compact test --contract counter
compact test --coverage
```

### compact deploy

Deploys contracts using the configured network:
```bash
compact deploy --network local
compact deploy --network preprod
compact deploy --contract counter --network local
```

### compact clean

Removes build artifacts:
```bash
compact clean
compact clean --all   # Also remove node_modules
```

### compact doctor

Checks development environment:
```bash
compact doctor
```

Verifies:
- Node.js version compatibility
- compactc compiler installation
- Docker installation for devnet
- Network connectivity
- Required environment variables

## Formatter CLI

### format-compact

Code formatting for Compact files.

```bash
format-compact contracts/src/counter.compact
format-compact contracts/src/ --recursive
format-compact contracts/src/counter.compact --check   # Check only
format-compact contracts/src/counter.compact --diff    # Show diff
```

### Formatting Rules

- Consistent indentation (2 spaces)
- Line length maximum of 100 characters
- Trailing newline at end of file
- Consistent spacing around operators
- Import ordering and grouping
- Brace style enforcement

### Configuration

```json
{
  "format": {
    "indentSize": 2,
    "maxLineLength": 100,
    "trailingComma": true,
    "semicolons": true,
    "bracketSpacing": true
  }
}
```

## Fixup CLI

### fixup-compact

Automatic code migrations and fixes for Compact.

```bash
fixup-compact contracts/src/counter.compact
fixup-compact contracts/src/ --recursive
fixup-compact contracts/src/counter.compact --dry-run
fixup-compact contracts/src/counter.compact --rule remove-cell
```

### Available Fixups

- `remove-cell`: Replace deprecated Cell<T> with direct types
- `update-pragma`: Update language version pragma
- `ledger-block-to-flat`: Convert block ledger syntax to flat declarations
- `add-disclose`: Add missing disclose() calls where needed
- `fix-enum-access`: Fix incorrect enum access syntax
- `migrate-v020-to-v022`: Full migration from version 0.20 to 0.22

## Editor Integration

### VS Code Extension

**Installation**:
Install the Midnight Compact extension from the VS Code marketplace.

**Features**:
- Syntax highlighting for .compact files
- Real-time error reporting
- Compilation on save
- Go to definition
- Find all references
- Hover documentation
- Code completion
- Format on save

**Configuration**:
```json
{
  "midnight.compact.compilerPath": "/usr/local/bin/compactc",
  "midnight.compact.compileOnSave": true,
  "midnight.compact.formatOnSave": true,
  "midnight.compact.languageVersion": "0.22",
  "midnight.compact.includePaths": ["node_modules/@midnight-ntwrk"]
}
```

**Keybindings**:
- Ctrl+Shift+B: Compile current contract
- Ctrl+Shift+P > Midnight: Deploy Contract
- Ctrl+Shift+P > Midnight: Run Tests

### Neovim Setup

**compact.vim Plugin**:
```vim
Plug 'midnightntwrk/compact.vim'
```

**Configuration**:
```vim
let g:compact_compiler = 'compactc'
let g:compact_language_version = '0.22'
let g:compact_compile_on_save = 1

autocmd BufRead,BufNewFile *.compact set filetype=compact
```

**LSP Configuration** (via nvim-lspconfig):
```lua
require('lspconfig').compact_ls.setup({
  cmd = { 'compactc', 'lsp' },
  filetypes = { 'compact' },
  root_dir = require('lspconfig').util.root_pattern('compact.json', '.git'),
  settings = {
    compact = {
      languageVersion = "0.22",
      includePaths = { "node_modules/@midnight-ntwrk" }
    }
  }
})
```

**Tree-sitter Support**:
```lua
require('nvim-treesitter.configs').setup({
  ensure_installed = { 'compact' },
  highlight = { enable = true },
  indent = { enable = true }
})
```

**Key Mappings**:
```lua
vim.keymap.set('n', '<leader>cc', '<cmd>!compactc compile %<CR>')
vim.keymap.set('n', '<leader>cf', '<cmd>!format-compact %<CR>')
vim.keymap.set('n', '<leader>ct', '<cmd>!compact test<CR>')
```

## CI and CD Integration

### GitHub Actions for Compact

**setup-compact-action**:

```yaml
name: Compact CI
on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Compact
        uses: midnightntwrk/setup-compact-action@v1
        with:
          compactc-version: '0.22'
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Format check
        run: format-compact contracts/src/ --check

      - name: Compile contracts
        run: compactc compile contracts/src/*.compact --output-dir contracts/build

      - name: Start devnet
        run: docker-compose -f docker/docker-compose.yml up -d

      - name: Wait for devnet
        run: npx wait-on http://localhost:9944

      - name: Run tests
        run: npx vitest run
        env:
          MIDNIGHT_NETWORK: local
          MIDNIGHT_RPC_URL: http://localhost:9944

      - name: Stop devnet
        run: docker-compose -f docker/docker-compose.yml down
```

### Verification Steps in CI

```yaml
      - name: Verify verifier keys
        run: |
          for file in contracts/build/*.verifier.key; do
            echo "Verifying $file"
            compactc verify-key "$file"
          done

      - name: Type check TypeScript
        run: npx tsc --noEmit

      - name: Lint with ESLint
        run: npx eslint src/ contracts/test/

      - name: Check formatting
        run: npx prettier --check '**/*.ts'
```

### Pre-Commit Hooks

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.compact": [
      "format-compact --check",
      "compactc compile --check"
    ],
    "*.ts": [
      "prettier --check",
      "eslint --fix"
    ]
  }
}
```

## CLI Best Practices

### Error Handling

```typescript
export default class DeployContract extends Command {
  async run(): Promise<void> {
    try {
      const { flags } = await this.parse(DeployContract);
      const result = await deployContract(flags);

      if (!result.success) {
        this.error(`Deployment failed: ${result.error}`, { exit: 1 });
      }

      this.log(`Contract deployed at: ${result.address}`);
    } catch (error) {
      if (error instanceof NetworkError) {
        this.error(
          `Cannot connect to ${flags.network}. Is the devnet running?`,
          { exit: 2 }
        );
      } else if (error instanceof CompilationError) {
        this.error(
          `Compilation failed: ${error.message}\nCheck your contract for errors.`,
          { exit: 3 }
        );
      } else {
        this.error(`Unexpected error: ${error.message}`, { exit: 99 });
      }
    }
  }
}
```

### Progress Output

**Do**:
- Show spinner for long-running operations
- Display clear success messages with relevant details
- Show transaction hashes and contract addresses
- Provide estimated time for operations

**Do Not**:
- Log raw JSON responses without formatting
- Show stack traces to end users
- Print verbose debug output by default (use --verbose flag)
- Block without any indication of activity

### Environment Variables

**Required Variables**:
```bash
MIDNIGHT_NETWORK=local
MIDNIGHT_RPC_URL=http://localhost:9944
MIDNIGHT_INDEXER_URL=http://localhost:8080
MIDNIGHT_PROOF_SERVER_URL=http://localhost:6300
MIDNIGHT_WALLET_SEED="your twelve word seed phrase here"
```

**Optional Variables**:
```bash
MIDNIGHT_LOG_LEVEL=debug
MIDNIGHT_COMPILER_PATH=/usr/local/bin/compactc
MIDNIGHT_CONTRACTS_DIR=./contracts/src
MIDNIGHT_BUILD_DIR=./contracts/build
MIDNIGHT_DEPLOY_GAS_LIMIT=1000000
```

**.env.example for Projects**:
```bash
# Network configuration
MIDNIGHT_NETWORK=local
MIDNIGHT_RPC_URL=http://localhost:9944

# Wallet (DO NOT COMMIT REAL SEEDS)
MIDNIGHT_WALLET_SEED=bottom drive obey lake curtain smoke basket hold race lonely fit walk

# Compiler
MIDNIGHT_COMPILER_VERSION=0.22

# Docker
MIDNIGHT_DOCKER_COMPOSE_PATH=./docker/docker-compose.yml
```

### Configuration Management

```typescript
interface MidnightConfig {
  network: 'local' | 'preprod' | 'mainnet';
  rpcUrl: string;
  indexerUrl: string;
  proofServerUrl: string;
  compilerPath: string;
  contractsDir: string;
  buildDir: string;
  testDir: string;
}

function loadConfig(): MidnightConfig {
  return {
    network: process.env.MIDNIGHT_NETWORK as any || 'local',
    rpcUrl: process.env.MIDNIGHT_RPC_URL || 'http://localhost:9944',
    indexerUrl: process.env.MIDNIGHT_INDEXER_URL || 'http://localhost:8080',
    proofServerUrl: process.env.MIDNIGHT_PROOF_SERVER_URL || 'http://localhost:6300',
    compilerPath: process.env.MIDNIGHT_COMPILER_PATH || 'compactc',
    contractsDir: process.env.MIDNIGHT_CONTRACTS_DIR || './contracts/src',
    buildDir: process.env.MIDNIGHT_BUILD_DIR || './contracts/build',
    testDir: process.env.MIDNIGHT_TEST_DIR || './contracts/test'
  };
}
```

## Testing CLI Tools

### Automated CLI Testing

```typescript
import { test } from '@oclif/test';
import { expect } from 'chai';

describe('deploy command', () => {
  test
    .stdout()
    .command(['deploy', '--network', 'local', '--contract', 'counter.compact'])
    .it('deploys contract to local network', (ctx) => {
      expect(ctx.stdout).to.contain('Contract deployed at:');
    });

  test
    .stderr()
    .command(['deploy', '--network', 'invalid'])
    .catch((error) => {
      expect(error.message).to.contain('Invalid network');
    })
    .it('fails with invalid network');
});
```

### Snapshot Testing

```typescript
import { expect, test } from 'vitest';

test('deploy command output format', async () => {
  const output = await runDeployCommand(['deploy', '--network', 'local']);

  expect(output).toMatchInlineSnapshot(`
    "Compiling contract... done
    Generating ZK keys... done
    Deploying to local... done
    Contract deployed at: 0x1234567890abcdef"
  `);
});
```

### Integration Testing CLI

```typescript
describe('CLI integration tests', () => {
  beforeAll(async () => {
    await startDevnet();
    await waitForDevnet();
    await generateTestWallet();
  });

  afterAll(async () => {
    await stopDevnet();
  });

  it('full deploy and interact flow', async () => {
    const deployResult = await cli(['deploy', '--network', 'local']);
    expect(deployResult.address).toBeDefined();
    expect(deployResult.address).toMatch(/^[0-9a-f]{64}$/);

    const interactResult = await cli([
      'interact', '--contract', deployResult.address,
      '--circuit', 'increment'
    ]);
    expect(interactResult.success).toBe(true);

    const state = await cli([
      'read-state', '--contract', deployResult.address
    ]);
    expect(state.counter).toBe(1);
  });
});
```

## Package Management

### npm for Midnight Projects

**Typical package.json**:
```json
{
  "name": "my-midnight-dapp",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "build": "compact build",
    "test": "compact test",
    "deploy:local": "compact deploy --network local",
    "deploy:preprod": "compact deploy --network preprod",
    "devnet:start": "docker-compose -f docker/docker-compose.yml up -d",
    "devnet:stop": "docker-compose -f docker/docker-compose.yml down",
    "format": "format-compact contracts/src/ && prettier --write 'src/**/*.ts'",
    "lint": "eslint src/ contracts/test/",
    "typecheck": "tsc --noEmit",
    "ci": "npm run format && npm run lint && npm run typecheck && npm run test"
  },
  "dependencies": {
    "@midnight-ntwrk/compact-runtime": "^0.23.0",
    "@midnight-ntwrk/midnight-js": "^0.23.0",
    "@midnight-ntwrk/wallet-sdk": "^0.23.0"
  },
  "devDependencies": {
    "@midnight-ntwrk/compact-cli": "^0.23.0",
    "@midnight-ntwrk/testkit-js": "^0.23.0",
    "typescript": "^5.3.0",
    "vitest": "^1.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "@types/node": "^20.0.0"
  }
}
```

### yarn and bun Support

**yarn**:
```bash
yarn create @midnight-ntwrk/app my-dapp
yarn compact build
yarn compact test
```

**bun**:
```bash
bun create @midnight-ntwrk/app my-dapp
bun compact build
bun compact test
```

### Version Pinning

**Why Version Pinning Matters**:
- Contract compilation is deterministic
- Different compiler versions produce different ZK circuits
- Verifier keys must match the compiler version
- Production deployments should pin exact versions

**Dependency Strategy**:
```json
{
  "dependencies": {
    "@midnight-ntwrk/compact-runtime": "0.23.0"
  }
}
```

Use exact versions (without `^` or `~`) for production deployments. Use caret ranges for development dependencies.

### Package Update Flow

1. Check changelog for breaking changes
2. Update dependencies in package.json
3. Recompile all contracts
4. Verify verifier keys still match
5. Run full test suite
6. Update CI configuration if needed
7. Deploy to testnet first
8. Verify behavior before mainnet

## Windows Setup

### WSL Configuration

Midnight development on Windows requires WSL2 (Windows Subsystem for Linux).

**Install WSL2**:
```powershell
wsl --install -d Ubuntu-22.04
wsl --set-default-version 2
```

**Configure Ubuntu**:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl git

curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

sudo npm install -g @midnight-ntwrk/compact-cli
```

### VS Code with WSL

**Install Extensions**:
- Remote - WSL (ms-vscode-remote.remote-wsl)
- Midnight Compact Language Support

**Open Project in WSL**:
1. Open VS Code
2. Press F1
3. Select "Remote-WSL: Open Folder in WSL"
4. Navigate to your project in the Linux filesystem

**Important**: Store project files in the WSL filesystem (e.g. `/home/user/projects/`) not on the Windows filesystem (e.g. `/mnt/c/`). The Windows filesystem is significantly slower for development operations.

### Docker on WSL

**Install Docker Desktop for Windows**:
Enable WSL 2 integration in Docker Desktop settings. Docker commands work from WSL terminal automatically.

**Verify Setup**:
```bash
docker --version
docker-compose --version
docker run hello-world
```

### Common Windows Issues

**Line Endings**:
```bash
git config --global core.autocrlf input
```

Ensures LF line endings in WSL and prevents CRLF issues in Compact files.

**Path Separators**:
Always use forward slashes in configuration files even on Windows. WSL handles path translation automatically.

**File Permissions**:
WSL filesystem permissions are independent of Windows. Use `chmod` and `chown` as needed. Avoid editing WSL files from Windows applications.

**Performance**:
- Store projects in `/home/user/` on the WSL filesystem
- Allocate sufficient memory to WSL (at least 4GB)
- Use Docker with WSL2 backend for best performance
- Compile on the WSL side never cross-compile from Windows

### PowerShell Aliases for WSL

```powershell
function midnight {
  wsl bash -c "cd /home/user/projects/my-dapp && compact $args"
}

function midnight-devnet {
  wsl bash -c "cd /home/user/projects/my-dapp && docker-compose -f docker/docker-compose.yml $args"
}
```

## Environment Variables Reference

### Complete Variable Listing

| Variable | Required | Default | Description |
|---|---|---|---|
| MIDNIGHT_NETWORK | Yes | local | Target network |
| MIDNIGHT_RPC_URL | Yes | http://localhost:9944 | RPC endpoint |
| MIDNIGHT_INDEXER_URL | No | http://localhost:8080 | Indexer GraphQL endpoint |
| MIDNIGHT_PROOF_SERVER_URL | No | http://localhost:6300 | Proof generation server |
| MIDNIGHT_WALLET_SEED | No | (none) | Mnemonic seed phrase |
| MIDNIGHT_COMPILER_PATH | No | compactc | Path to compactc binary |
| MIDNIGHT_COMPILER_VERSION | No | latest | Target compiler version |
| MIDNIGHT_CONTRACTS_DIR | No | ./contracts/src | Contracts source directory |
| MIDNIGHT_BUILD_DIR | No | ./contracts/build | Build output directory |
| MIDNIGHT_TEST_DIR | No | ./contracts/test | Test files directory |
| MIDNIGHT_LOG_LEVEL | No | info | Logging verbosity |
| MIDNIGHT_DEPLOY_GAS_LIMIT | No | 1000000 | Max gas for deploy tx |
| MIDNIGHT_DOCKER_COMPOSE_PATH | No | ./docker/docker-compose.yml | Devnet compose file |

### Network-Specific Configurations

**Local Devnet**:
```bash
MIDNIGHT_NETWORK=local
MIDNIGHT_RPC_URL=http://localhost:9944
MIDNIGHT_INDEXER_URL=http://localhost:8080
MIDNIGHT_PROOF_SERVER_URL=http://localhost:6300
```

**Preprod Testnet**:
```bash
MIDNIGHT_NETWORK=preprod
MIDNIGHT_RPC_URL=https://rpc.preprod.midnight.network
MIDNIGHT_INDEXER_URL=https://indexer.preprod.midnight.network
MIDNIGHT_PROOF_SERVER_URL=https://proof.preprod.midnight.network
```

**Mainnet**:
```bash
MIDNIGHT_NETWORK=mainnet
MIDNIGHT_RPC_URL=https://rpc.midnight.network
MIDNIGHT_INDEXER_URL=https://indexer.midnight.network
MIDNIGHT_PROOF_SERVER_URL=https://proof.midnight.network
```

## Troubleshooting

### Common CLI Errors

**"Network connection failed"**:
- Verify the devnet is running with `docker-compose ps`
- Check the RPC URL is correct
- Ensure no firewall is blocking the connection
- Try `curl http://localhost:9944/health`

**"Compilation failed"**:
- Run `compactc compile --debug` for verbose output
- Check the language version pragma matches installed compiler
- Verify all imports resolve correctly
- Check for syntax errors in .compact files

**"Deployment failed"**:
- Ensure wallet has sufficient DUST for fees
- Verify constructor arguments match contract definition
- Check that the network is accepting transactions
- Verify the contract address format is correct

**"Proof generation failed"**:
- Verify witness values satisfy all circuit constraints
- Check that assert conditions are logically correct
- Ensure the proof server is running and accessible
- Try generating proof locally for debugging

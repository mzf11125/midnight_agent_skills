# Code Quality Pipeline

Continuous quality enforcement for Midnight DApp projects covering linting, testing, coverage, CI, pre-commit hooks, quality gates, and metric tracking.

## Biome Linting

### Configuration

Biome serves as the primary linting and formatting tool. The configuration lives in `biome.json` at the project root.

```
{
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": { "all": true },
      "suspicious": { "all": true },
      "style": {
        "useConst": "error",
        "useTemplate": "error"
      }
    }
  }
}
```

### Rules

The correctness category includes rules for unreachable code, invalid type comparisons, and undefined variable usage. The suspicious category catches noExplicitAny, noDoubleEquals, and noConsoleLog in production code. The style category enforces const over let, template literals over string concatenation, and consistent import ordering.

### Integration

Run Biome as a check in CI with `npx biome ci .`. For local development use `npx biome check --write .` to auto fix issues. The VS Code Biome extension provides inline diagnostics and format on save.

## Vitest Testing

### Unit Test Patterns

Unit tests verify individual circuit functions in isolation. Each test imports the contract module, constructs mock ledger state, calls the target circuit, and asserts the output matches expectations. Tests use `describe` blocks to group related circuits and `it` blocks for individual scenarios.

```ts
describe("FungibleToken.transfer", () => {
  it("transfers tokens between accounts", async () => {
    const result = await callCircuit("transfer", {
      sender: alice,
      recipient: bob,
      amount: 100n
    });
    expect(result.success).toBe(true);
    expect(result.balances.get(bob)).toBe(100n);
  });

  it("rejects transfers exceeding balance", async () => {
    const result = await callCircuit("transfer", {
      sender: alice,
      recipient: bob,
      amount: 999999n
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain("insufficient balance");
  });
});
```

### Integration Test Patterns

Integration tests exercise full transaction flows across multiple circuits and services. They deploy the contract to a test network, fund wallets with DUST, call a sequence of circuits, and verify ledger state changes through the indexer. Integration tests use longer timeouts and retry logic for network dependent operations.

### Test Configuration

The `vitest.config.ts` file sets the test environment, timeout, and coverage thresholds.

```
export default defineConfig({
  test: {
    environment: "node",
    testTimeout: 30000,
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov", "html"],
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 80,
        statements: 80
      }
    }
  }
});
```

## Playwright E2E Testing

### Browser Automation

Playwright tests automate browser based DApp interactions. Tests navigate to the DApp URL, connect a test wallet, click through the user interface, and verify on-screen state changes. The `page` fixture provides methods for clicking, typing, and waiting for selectors.

### Wallet Flow Testing

Wallet connection tests verify the DApp Connector integration from the browser perspective. The test clicks the connect wallet button, approves the connection in the simulated wallet popup, and verifies the connected address appears in the DApp header. Disconnection, account switching, and network switching flows are tested similarly.

### Test Configuration

Playwright configuration defines the browsers, base URL, and test directory.

```
export default defineConfig({
  testDir: "./e2e",
  use: {
    baseURL: "http://localhost:5173",
    browserName: "chromium"
  },
  webServer: {
    command: "npm run dev",
    port: 5173
  }
});
```

## Coverage Requirements

Coverage thresholds are enforced at 80 percent across lines, branches, functions, and statements. The coverage provider is v8 for accurate TypeScript source mapping. Coverage reports are generated in text for terminal output, lcov for CI tooling, and html for local review.

Files excluded from coverage include type declaration files, test files, configuration files, and generated contract artifacts. The exclude list is configured in `vitest.config.ts`.

## CI Pipeline with GitHub Actions

The CI workflow runs on every push and pull request.

```
name: Quality Pipeline
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: npm ci
      - run: npx biome ci .
      - run: npx vitest run --coverage
      - run: npx playwright test
```

The Biome step ensures code style consistency. The vitest step runs unit and integration tests with coverage checks. The Playwright step runs E2E browser tests. Each step must pass for the pipeline to succeed.

## Pre Commit Hooks with Husky

### Installation

Husky manages Git hooks from the project `package.json`.

```
npm install --save-dev husky
npx husky init
```

### Lint Staged

The `lint-staged` integration runs Biome only on staged files for speed.

```
// .husky/pre-commit
npx lint-staged
```

```
// package.json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx,json,css}": ["biome check --write --no-errors-on-unmatched"],
    "*.compact": ["compactc --max-constraints 1000000"]
  }
}
```

Compact files get validated through the compiler during pre-commit. The constraint limit catches circuits that exceed budget before they reach CI.

## Quality Gates

### Coverage Thresholds

Coverage thresholds are checked during the vitest run. Lines, branches, functions, and statements must each reach 80 percent. If any threshold is not met vitest exits with a non-zero code failing the CI pipeline.

### Complexity and File Size Limits

Circuit complexity is limited by the constraint budget. The `compactc --max-constraints` flag enforces this limit during both pre-commit hooks and CI compilation. For TypeScript code cyclomatic complexity is checked by Biome with a maximum of 20 per function. Files exceeding 500 lines trigger a warning in Biome and files exceeding 1000 lines are rejected.

## Quality Metrics and Trend Tracking

### Metrics and Trend Reporting

The quality dashboard displays coverage percentages by file, lint violations by severity, test pass rate, and E2E test duration from the most recent CI run. Coverage trends are stored as time series data. A coverage drop exceeding 2 percent between consecutive runs triggers a quality alert. A weekly report aggregates trend data into a summary posted automatically to the team communication channel.

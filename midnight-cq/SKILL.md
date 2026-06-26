---
name: midnight-cq
description: Code quality enforcement for Midnight projects. Use when running Biome linting, configuring Vitest testing, setting up Playwright E2E tests, integrating CI pipelines, enforcing coverage thresholds, configuring pre-commit hooks, automating code review, setting quality gates, checking TypeScript strictness, auditing contract quality, reviewing dependency quality, computing quality metrics, generating quality reports, or implementing shift-left quality practices. Provides a comprehensive code quality framework covering linting, testing, formatting, and automated enforcement.
---

# Midnight Code Quality

A comprehensive code quality enforcement framework for Midnight Network projects. This skill covers linting, testing, formatting, coverage, CI integration, and automated quality gates.

## Code Quality Overview

Code quality for Midnight projects encompasses four pillars: linting for code correctness and style, unit testing for functional verification, end-to-end testing for integration validation, and CI pipeline integration for automated enforcement. Together these pillars ensure that Midnight projects maintain high quality standards throughout the development lifecycle.

The Midnight ecosystem uses specific tools for each quality pillar. Biome provides linting and formatting with Midnight-specific rule configurations. Vitest provides unit and integration testing with fast execution and native TypeScript support. Playwright provides browser-based end-to-end testing for wallet interactions and transaction flows. GitHub Actions provides the CI orchestration layer.

The quality framework is designed to be incrementally adoptable. Projects can start with basic linting and gradually add testing, coverage requirements, and automated gates as they mature. The framework provides sensible defaults at each adoption level while allowing customization for project-specific needs.

## Biome Linting

Biome is the primary linting and formatting tool for Midnight projects. It replaces both ESLint and Prettier with a single tool that is significantly faster and requires minimal configuration.

### Rules Configuration

Biome rules are configured in a `biome.json` file at the project root. The configuration specifies which rules are active, their severity levels, and any rule-specific options. Rules can be set to "off", "warn", or "error".

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },
      "suspicious": {
        "noExplicitAny": "error",
        "noConsoleLog": "warn"
      }
    }
  }
}
```

### Midnight-Specific Rules

In addition to standard Biome rules, Midnight projects benefit from domain-specific linting rules. These rules enforce conventions that are important for Midnight development.

The `midnight/no-missing-witness-check` rule ensures that all circuits verify witness data before using it. The `midnight/no-unchecked-disclosure` rule requires explicit review comments on every disclose call. The `midnight/require-circuit-return` rule checks that circuits have explicit return type annotations. The `midnight/validate-state-access` rule verifies that circuit state access declarations match actual usage.

### Import Organization

Biome can automatically organize imports by sorting them and removing unused imports. Imports are grouped by type: external packages first, then internal modules, then relative imports. Within each group imports are sorted alphabetically.

```json
{
  "assist": {
    "enabled": true,
    "actions": {
      "source": {
        "organizeImports": true
      }
    }
  }
}
```

### Code Formatting

Biome provides opinionated code formatting that is consistent across all Midnight projects. The formatter handles indentation, line wrapping, quote style, and all other formatting concerns. The formatter is not configurable beyond a few high-level options ensuring that all Midnight project code looks consistent.

### Error Level Configuration

Rules can be configured at different severity levels. "error" level rules cause linting to fail and must be fixed before code can be committed. "warn" level rules produce warnings that should be addressed but do not block commits. "off" level rules are disabled entirely. Midnight projects default to "error" for correctness rules and "warn" for style rules.

## Format Rules

The Biome formatter enforces consistent code formatting across all Midnight project files. The rules are designed to maximize readability and minimize diff noise.

### Indentation

Indentation uses two spaces per level. Tabs are not allowed. This provides sufficient visual hierarchy while keeping line lengths manageable. All file types in the project use consistent indentation including TypeScript, JSON, and YAML files.

### Line Width

Maximum line width is set to 100 characters. Lines that exceed this limit are wrapped by the formatter. Comments are not automatically wrapped because manual line breaks in comments often carry semantic meaning. String literals are never broken across lines.

### Quotes Style

Single quotes are used for TypeScript strings. Double quotes are used for JSX attributes. Template literals are used when interpolation is needed. These conventions match the wider TypeScript ecosystem and help distinguish between different kinds of string usage.

### Trailing Commas

Trailing commas are always added in multiline constructs. This practice reduces diff noise when adding or removing items and eliminates syntax errors from forgotten commas. Single-line constructs do not receive trailing commas.

### Bracket Spacing

Spaces are added inside curly braces for object literals and import statements. This improves readability by visually separating the braces from their contents. Empty braces are not padded with spaces.

### Semicolons

Semicolons are always required at the end of statements. This is the safest convention and eliminates an entire class of bugs related to automatic semicolon insertion. The formatter adds missing semicolons automatically.

## Lint Rules

Biome lint rules are organized into rule groups that address different categories of code quality issues.

### Correctness Rules

Correctness rules detect code that is likely to be wrong. These rules are always enabled at the "error" level. They catch bugs such as unreachable code, duplicate declarations, invalid regular expressions, and type errors that TypeScript might miss. Correctness rules must never produce false positives so each rule is carefully designed to only flag genuinely problematic code.

### Suspicious Code Detection

Suspicious rules detect patterns that are often mistakes but might in rare cases be intentional. These rules flag things like no-op assignments, comparisons that are always true or false, and overly complex expressions. Suspicious rules default to "warn" but can be elevated to "error" for stricter enforcement.

### Complexity Limits

Biome can enforce complexity limits on functions and files. The `complexity/noExcessiveCognitiveComplexity` rule limits cognitive complexity which measures how difficult a function is to understand. The default limit is 15 but can be adjusted for project needs. The `complexity/noExcessiveNestedDepth` rule limits nesting to prevent deeply nested control structures.

### Naming Conventions

Naming convention rules enforce consistent naming patterns. Type names and interface names must use PascalCase. Variable names and function names must use camelCase. Constant values must use UPPER_CASE. Boolean variables should be prefixed with "is", "has", or "should" to indicate their boolean nature.

### Unused Imports

The `correctness/noUnusedVariables` rule detects variables that are declared but never used. This includes unused imports, unused function parameters, and unused local variables. Unused code adds noise and can mask bugs where a variable was intended to be used but was forgotten.

## Vitest Testing

Vitest is the primary testing framework for Midnight projects. It provides fast test execution, native TypeScript support, and a Jest-compatible API that makes migration easy.

### Test Structure

Tests are organized to mirror the source code structure. Each source file has a corresponding test file with the `.test.ts` extension. Tests are co-located with source files or placed in a parallel `__tests__` directory. Test files import the functions and types they test directly from the source files.

```typescript
import { describe, it, expect } from "vitest";
import { CounterContract } from "./Counter";

describe("CounterContract", () => {
  describe("increment", () => {
    it("adds the given amount to the counter", async () => {
      const counter = new CounterContract();
      await counter.increment(5);
      expect(await counter.getCount()).toBe(5);
    });

    it("rejects negative amounts", async () => {
      const counter = new CounterContract();
      await expect(counter.increment(-1)).rejects.toThrow();
    });
  });
});
```

### Test Organization

Tests follow the Arrange-Act-Assert pattern. The Arrange phase sets up the test environment and creates the objects under test. The Act phase performs the operation being tested. The Assert phase verifies that the operation produced the expected results. Each test should test exactly one behavior.

### Mocking Strategies

Vitest provides powerful mocking capabilities through `vi.fn()`, `vi.mock()`, and `vi.spyOn()`. For Midnight projects the most common mocking targets are wallet providers, proof servers, and indexer APIs. Mocks should be created at the boundary between the code under test and external dependencies. Mocks should verify that they are called with the expected arguments and return controlled responses.

```typescript
vi.mock("midnight-js", () => ({
  WalletFacade: vi.fn().mockImplementation(() => ({
    getBalance: vi.fn().mockResolvedValue(1000n),
    signTransaction: vi.fn().mockResolvedValue(signedTx)
  }))
}));
```

### Snapshot Testing

Vitest supports snapshot testing for validating complex output structures. Snapshots capture the output of a function and compare it against a stored reference. If the output changes the test fails and the developer must either accept the new output as correct or fix the regression. Snapshots are most useful for testing serialization, state representations, and API responses.

### Coverage Configuration

Vitest includes built-in code coverage via c8 or istanbul. Coverage is configured in the `vitest.config.ts` file. The configuration specifies which files to include and exclude from coverage, the coverage thresholds to enforce, and the report formats to generate.

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: "c8",
      include: ["src/**/*.ts"],
      exclude: ["src/**/*.test.ts", "src/**/generated/**"],
      thresholds: {
        lines: 80,
        branches: 70,
        functions: 80,
        statements: 80
      }
    }
  }
});
```

## Unit Testing Patterns

Unit tests for Midnight contracts follow specific patterns that cover the unique aspects of zero-knowledge contract development.

### Contract Function Testing

Each circuit in a contract should have dedicated tests that verify its behavior with valid inputs. The tests should exercise boundary values, typical values, and edge cases. For circuits that modify state the tests should verify both the state change and the return value. For circuits that only return values the tests should verify the return value across a range of inputs.

### Witness Testing

Circuits that depend on witness data need tests that verify the correct handling of both valid and invalid witnesses. Valid witness tests confirm that the circuit produces correct results when given the expected witness. Invalid witness tests confirm that the circuit fails with the appropriate error when given an incorrect witness.

### Circuit Testing

Low-level circuit tests validate the internal logic of circuits independently of the contract. These tests call circuits directly with specific inputs and verify the output state and return values. Circuit tests can be more granular than contract tests because they can test intermediate computation steps.

### State Transition Testing

State transition tests verify that state changes occur correctly across sequences of circuit calls. These tests simulate realistic usage patterns where multiple circuits are called in sequence and the cumulative state effects are verified. State transition tests catch bugs that only manifest across multiple transactions.

### Error Case Testing

Error case tests verify that contracts fail correctly when given invalid inputs. Every validation check in a circuit should have a corresponding error case test. Tests should verify both that the correct error is raised and that state is not corrupted when an error occurs.

## Integration Testing

Integration tests verify that multiple components work together correctly. For Midnight projects the most important integration boundaries are between the application code and external dependencies.

### Wallet Integration Tests

Wallet integration tests verify that the application correctly interacts with Midnight wallets. Tests cover wallet connection, transaction signing, balance queries, and error handling when the wallet is unavailable or rejects a request. These tests mock the wallet API to simulate different wallet states and behaviors.

### API Integration Tests

API integration tests verify that the application correctly calls external APIs including the indexer API and the proof server API. Tests cover successful responses, error responses, and timeout scenarios. API responses are mocked using recorded fixtures to ensure test reliability.

### Provider Integration Tests

Provider integration tests verify that the application correctly uses Midnight network providers. Tests cover provider configuration, connection management, and fallback behavior when primary providers are unavailable. These tests validate that the application can recover gracefully from network issues.

### Cross-Component Tests

Cross-component tests verify interactions between the application frontend and contract backend. These tests simulate complete user flows from wallet connection through transaction submission to state verification. They catch integration issues that unit tests in isolation would miss.

## Playwright E2E Testing

Playwright provides browser-based end-to-end testing for Midnight dApps. It automates real browsers to test the complete user experience.

### Browser Automation

Playwright launches real Chromium, Firefox, or WebKit browsers and controls them programmatically. Tests can navigate to pages, click buttons, fill forms, and verify page content. The browser runs in headless mode by default but can be switched to headed mode for debugging.

```typescript
import { test, expect } from "@playwright/test";

test("user can connect wallet and submit transaction", async ({ page }) => {
  await page.goto("http://localhost:3000");
  await page.click("text=Connect Wallet");
  await page.click("text=1AM Wallet");
  await page.waitForSelector("text=Connected");
  await page.click("text=Increment Counter");
  await page.waitForSelector("text=Transaction confirmed");
  expect(await page.textContent(".counter-value")).toBe("1");
});
```

### Wallet Connection Flows

Wallet connection is the most important user flow in a Midnight dApp. Playwright tests simulate the complete connection flow including selecting the wallet provider, approving the connection in the wallet popup, and verifying the connected state in the application UI. The tests verify that connection errors are displayed correctly and that reconnection works after page refresh.

### Transaction Submission Flows

Transaction submission tests simulate the complete flow from user action to confirmed transaction. Tests click a button to initiate a transaction, wait for the wallet popup to appear, approve the transaction, wait for confirmation, and verify the updated UI. Tests also verify error handling when transactions fail.

### UI Validation

UI validation tests check that the application displays correctly at various viewport sizes. Tests verify that elements are properly aligned, that text is readable, that buttons are clickable, and that interactive elements respond to user input. Visual regression testing compares screenshots against approved baselines to detect unintended UI changes.

### Screenshot Comparison

Playwright can capture screenshots of pages and compare them against reference images. If the screenshot differs from the reference the test fails and the developer must either approve the new appearance or fix the regression. Screenshot comparison is most useful for detecting CSS regressions and layout changes.

## Coverage Requirements

Code coverage measures how much of the codebase is exercised by tests. Midnight projects enforce minimum coverage thresholds to ensure adequate test coverage.

### Line Coverage

Line coverage measures the percentage of source lines that are executed during tests. The minimum threshold for Midnight projects is 80 percent. Lines that are not covered should be reviewed to determine if they need dedicated tests or if they can be excluded from coverage requirements.

### Branch Coverage

Branch coverage measures the percentage of conditional branches that are tested. Each if-else, switch case, and ternary operator creates branches. The minimum threshold is 70 percent. Low branch coverage indicates that not all code paths are tested.

### Function Coverage

Function coverage measures the percentage of functions that are called at least once during tests. The minimum threshold is 80 percent. Every exported function should have at least one test that calls it.

### Coverage Thresholds

Coverage thresholds are enforced in CI. If coverage falls below the threshold the pipeline fails. Thresholds should be set at levels that encourage good testing practices without being so high that they incentivize low-quality tests just to hit coverage numbers.

### Coverage Reporting

Coverage reports are generated in multiple formats. HTML reports provide an interactive view of coverage by file. LCOV reports integrate with CI annotation systems. JSON reports can be consumed by dashboards and trend analysis tools. The HTML report is generated by default and can be opened in a browser for detailed exploration.

## CI Pipeline Configuration

Continuous integration pipelines automate quality checks on every code change. Midnight projects use GitHub Actions for CI orchestration.

### GitHub Actions Workflows

The CI workflow is defined in `.github/workflows/ci.yml`. It runs on every push and pull request. The workflow includes separate jobs for linting, testing, and building. Jobs run in parallel where possible to minimize total pipeline time.

```yaml
name: CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx biome ci .
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx vitest --coverage
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
```

### Test Stages

The CI pipeline separates tests into stages based on their scope and speed. Unit tests run first because they are fastest and most likely to catch issues. Integration tests run next. End-to-end tests run last because they are slowest. If unit tests fail later stages are skipped to provide fast feedback.

### Lint Stages

Linting runs as a separate job that can be fast-tracked. Biome analysis completes in seconds for most projects. The lint job also runs type checking with `tsc --noEmit` to catch type errors that linting alone would miss.

### Build Stages

The build stage verifies that the project compiles successfully. For TypeScript projects this means running the TypeScript compiler. The build stage also verifies that generated outputs are correct and that the project can be packaged for distribution.

### Deployment Gates

CI can be extended with deployment gates that run additional verification before deploying to specific environments. Preprod deployment requires all tests to pass. Mainnet deployment requires all tests to pass plus additional checks such as security scanning and manual approval.

## Pre-Commit Hooks

Pre-commit hooks run quality checks before code is committed to the repository. They catch issues at the earliest possible point in the development workflow.

### Linting Before Commit

Biome runs on staged files before each commit. Only files that would be committed are linted. If linting fails the commit is blocked until the issues are fixed. This ensures that lint errors never enter the repository.

### Type Checking Before Commit

TypeScript type checking runs on staged files before each commit. Type errors block the commit. Type checking catches bugs that linting might miss and ensures that the codebase remains type-safe.

### Test Running Before Commit

Unit tests run on changed files before each commit. Only tests related to the changed code are executed to keep the pre-commit hook fast. If tests fail the commit is blocked. This ensures that commits never break existing functionality.

### Husky Configuration

Husky manages pre-commit hooks in Midnight projects. Hooks are defined in the `.husky/` directory and are automatically installed when `npm install` runs. Husky integrates with both Biome and Vitest to provide a seamless pre-commit experience.

## Code Review Automation

Automated code review checks complement human code review by catching mechanical issues that reviewers might miss.

### Automated Review Comments

When linting or testing fails in CI the failure is posted as a review comment on the pull request. Comments include a summary of the issues, links to the relevant code, and suggested fixes where applicable. This gives developers immediate feedback without needing to check CI logs.

### Security Scanning

Security scanning checks for known vulnerabilities in dependencies. The scanner checks the project against vulnerability databases and reports any dependencies with known security issues. Critical vulnerabilities block merges. Lower severity vulnerabilities produce warnings that should be addressed in a timely manner.

### Dependency Auditing

Dependency auditing checks that all dependencies are pinned to specific versions and that no deprecated packages are used. It also checks for license compliance and reports any dependencies with licenses that are incompatible with the project license.

### Breaking Change Detection

Breaking change detection analyzes pull request diffs to identify changes that could break dependent code. It checks for removed exports, changed function signatures, and modified type definitions. Breaking changes are flagged for careful review and may require a major version bump.

## Quality Gates

Quality gates are automated checks that must pass before code can be merged or deployed. They provide objective criteria for code quality decisions.

### Minimum Coverage Thresholds

Coverage gates require that code coverage does not decrease below minimum thresholds. The current coverage must be greater than or equal to the baseline coverage. Coverage gates prevent the gradual erosion of test coverage over time.

### Maximum Complexity Scores

Complexity gates limit how complex individual functions can be. The cognitive complexity score must not exceed the maximum threshold. If complexity increases the gate fails and the function must be simplified before it can be merged.

### Lint Error Budget

The lint error budget limits the total number of lint warnings allowed in the codebase. New code must not increase the warning count above the budget. If the budget is exceeded the team must reduce warnings before adding new code. This mechanism allows gradual cleanup of existing warnings while preventing new warnings from accumulating.

### Test Pass Requirements

All tests must pass before code can be merged. There is no allowance for flaky tests. Flaky tests must be fixed or removed. If a test fails intermittently it is treated as a test failure and blocks merges until it is stabilized.

## TypeScript Quality

TypeScript quality rules enforce strict typing practices that catch errors at compile time rather than runtime.

### Strict Mode

TypeScript strict mode enables all strict type checking options. `strict: true` in tsconfig.json enables eight separate checks including strict null checks, strict function types, and no implicit any. Strict mode is required for all Midnight projects.

### No Implicit Any

The `noImplicitAny` option forbids variables and parameters with an implied `any` type. All types must be explicitly declared or inferred from a typed expression. This prevents accidentally untyped code that could hide type errors.

### Strict Null Checks

The `strictNullChecks` option changes how `null` and `undefined` are handled. With strict null checks enabled `null` and `undefined` are not assignable to other types. Variables that can be null must be explicitly declared with a union type. Code must check for null before using potentially null values.

### Type Exports

All exported types must use explicit export syntax. Types are exported using `export type` for type-only exports and `export` for value exports. This distinction allows the TypeScript compiler to eliminate type-only imports at compile time.

### Unused Locals

The `noUnusedLocals` option catches local variables that are declared but never used. Unused variables indicate either missing code or unnecessary declarations. Both cases should be addressed before the code is committed.

## Contract Quality

Contract quality rules address the unique requirements of Midnight Compact contracts. These rules go beyond general code quality to cover contract-specific concerns.

### Witness Validation Completeness

Every circuit that accepts witness data must validate that data before using it. The witness validation check ensures that all witness fields are checked against expected values or constraints. Incomplete witness validation is a security risk because it could allow an attacker to provide arbitrary witness data.

### Circuit Disclosure Audit

Every value disclosed by a circuit must be explicitly annotated. The disclosure audit checks that all `disclose()` calls are intentional and necessary. Unnecessary disclosures leak data to the public ledger. Missing disclosures on required data prevent the contract from functioning correctly.

### State Access Patterns

Every circuit must declare which ledger states it reads and writes. The state access pattern check verifies that these declarations are accurate and complete. Incorrect state declarations can cause transaction failures or allow unauthorized state access.

### Gas Optimization Checks

Circuits should be optimized for gas efficiency. The gas optimization check measures the constraint count of each circuit and flags circuits that exceed recommended limits. High gas costs make contracts expensive to use and may indicate unnecessarily complex logic that could be simplified.

## Dependency Quality

Dependency quality affects the security, stability, and maintainability of Midnight projects. Regular dependency audits ensure that the project depends on well-maintained packages.

### Version Pinning Audit

All dependencies must be pinned to exact versions. Version ranges allow dependency changes without explicit approval which can introduce breaking changes unexpectedly. Pinned versions ensure that all builds use the same dependencies and that dependency updates are intentional.

### Dependency Freshness

Dependencies should be updated regularly to incorporate security fixes and improvements. The freshness check identifies dependencies that are significantly behind their latest versions. Outdated dependencies should be updated after testing confirms compatibility.

### Security Vulnerability Scanning

Every dependency is checked against known vulnerability databases. If a vulnerability is found the dependency must be updated to a version that fixes the vulnerability. If no fix is available the team must assess the risk and decide whether to accept it or find an alternative.

### License Compliance

All dependencies must have licenses that are compatible with the project license. The license check identifies dependencies with problematic licenses such as GPL or non-commercial licenses. Incompatible dependencies must be replaced with alternatives that have acceptable licenses.

## Quality Metrics

Quality metrics provide quantitative measures of code quality that can be tracked over time.

### Code Quality Score

The code quality score is a composite metric that combines lint results, test coverage, test pass rate, and complexity measurements into a single number. The score ranges from 0 to 100 with higher scores indicating better quality. The score is computed independently for each skill in the project.

### Trend Tracking

Quality metrics are tracked over time to identify trends. Improving trends indicate that the team is maintaining or improving quality. Declining trends indicate that quality is eroding and corrective action is needed. Trend data is visualized in dashboards that show metric values over weeks and months.

### Per-Skill Quality Breakdown

Quality metrics are broken down by skill to identify which parts of the project need attention. Each skill gets its own quality score and trend line. Teams can use this breakdown to prioritize quality improvement work.

### Team Quality Dashboards

Quality dashboards display current quality metrics and trends for the entire project team. Dashboards are visible to all team members to promote transparency and shared ownership of quality. Dashboards highlight both successes and areas needing improvement.

## Quality Reports

Quality reports communicate quality status to developers, managers, and stakeholders. Reports are generated in multiple formats for different audiences.

### Markdown Reports

Markdown reports provide a human-readable summary of quality status. They include the overall quality score, breakdowns by skill, trend indicators, and lists of specific issues that need attention. Markdown reports are generated after each CI run and can be included in pull request descriptions.

### JSON Output

JSON output provides machine-readable quality data for integration with other tools. The JSON format includes all raw metric values and detailed issue information. JSON output can be consumed by dashboards, monitoring systems, and notification tools.

### CI Annotations

CI annotations add quality information directly to pull request diffs. Annotations appear as comments on specific lines of code that have quality issues. They provide immediate context-specific feedback to developers during code review.

### GitHub Checks Integration

Quality results are integrated with GitHub Checks to provide a summary in the pull request UI. The Checks tab shows the quality status with pass or fail indicators for each quality gate. Developers can see at a glance whether their changes meet quality standards.

## Best Practices

### Shift-Left Quality

Quality checks should run as early as possible in the development workflow. Pre-commit hooks catch issues before they reach the repository. CI catches issues before they merge. Staging validation catches issues before they reach production. Each layer of checking provides an additional safety net.

### Incremental Adoption

Teams should adopt quality practices incrementally rather than attempting to achieve perfection immediately. Start with basic linting and add one quality gate at a time. This approach allows teams to build quality habits gradually without being overwhelmed by excessive failures.

### Team Quality Standards

Quality standards should be defined and agreed upon by the team. Standards should be documented in the project README or CONTRIBUTING guide. All team members should understand the standards and be able to apply them consistently. Quality is a team responsibility not an individual one.

### Automated Enforcement

Quality rules that can be automated should be automated. Manual enforcement is inconsistent and burdensome. Automation ensures that rules are applied consistently and frees humans to focus on quality aspects that require judgment such as design review and code architecture.

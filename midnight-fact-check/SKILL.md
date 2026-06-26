---
name: midnight-fact-check
description: Fact-checking pipeline for Midnight Network documentation covering claim extraction from documentation sources, domain classification for Compact language claims, API reference claims, network claims, concept claims, and SDK claims, verification methods including source cross-referencing, API testing, compile verification, and runtime behavior checks, multi-source validation comparing official docs, GitHub repos, npm packages, and community sources, verification report generation with structured reports, confidence levels, source attribution, and unresolved claims, automated checking via CLI-based verification and CI pipeline integration, common claim types covering version numbers, function signatures, type definitions, error codes, network endpoints, gas costs, and configuration defaults, source hierarchy with official docs as primary and GitHub source code as authoritative, fact-check rules for version freshness, dead link detection, deprecated API flagging, and breaking change detection, integration with midnight-expert for health checks and ecosystem compatibility verification, report formats in markdown, JSON, and CI-friendly exit codes, and documentation maintenance including flagging outdated docs, suggesting corrections, and tracking doc drift over time.
---

# Midnight Fact-Checking Pipeline

## Fact-Checking Overview

The Midnight fact-checking pipeline is a systematic methodology for validating the accuracy of Midnight Network documentation. As the Midnight ecosystem evolves rapidly across multiple packages and networks documentation can drift from actual behavior. This pipeline provides automated and manual verification processes to detect and correct inaccuracies.

The pipeline operates on a continuous basis ingesting documentation from official sources and community contributions then extracting verifiable claims and validating them against ground truth sources such as the GitHub source code, npm package metadata, and live network data.

The purpose of this fact-checking system is to maintain high quality documentation that developers can trust when building on Midnight. Inaccurate documentation leads to wasted developer time, broken DApps, and erosion of trust in the ecosystem. By systematically verifying claims the pipeline catches errors before they impact users.

The methodology follows a structured four phase process. First claims are extracted from documentation sources through parsing and pattern matching. Second claims are classified by domain and assigned verification strategies. Third claims are verified against authoritative sources using the assigned strategy. Fourth verification results are compiled into reports with confidence levels and recommended corrections.

### Claim Extraction Process

Claim extraction parses documentation Markdown files to identify factual assertions that can be verified. Claims include API signatures, version numbers, network endpoint URLs, configuration defaults, error codes, and behavioral descriptions.

The extraction uses pattern matching for common claim types and natural language analysis for free form claims. Each extracted claim is tagged with its source location including the file path and line number so that corrections can be applied precisely.

Extracted claims are stored in a structured format with the claim text, source information, domain classification, and verification status. This structured storage enables tracking claim verification over time and detecting new or changed claims between documentation versions.

The extraction process runs as part of the CI pipeline on every documentation change. It can also be triggered manually with the `midnight-fact-check extract` command for targeted verification of specific documentation files.


## Domain Classification

### Compact Language Claims

Claims about the Compact programming language fall into several subcategories. Syntax claims describe valid Compact syntax patterns and grammar rules. Type system claims describe the Compact type hierarchy including built-in types, user defined types, and type inference rules. Circuit claims describe ZK circuit semantics including confidentiality annotations and disclosure rules. Standard library claims describe the Compact standard library functions and their signatures.

Verification of Compact claims typically involves checking the Compact compiler source code or attempting to compile example code that exercises the claimed behavior. Some claims can be verified by consulting the Compact language specification if one exists.

### API Reference Claims

API claims involve the Midnight TypeScript SDK packages and their exported interfaces. These claims specify function names, parameter types, return types, thrown errors, and behavioral contracts.

API claims are verified by checking the actual TypeScript source code in the GitHub repository. Type definition files provide the canonical source for function signatures. Runtime behavior claims require examination of function implementations.

The npm package metadata provides additional verification through the published version numbers and dependency declarations. These must match the documentation claims about package versions and compatibility.

### Network Claims

Network claims describe the behavior and configuration of Midnight network nodes. These include RPC endpoint URLs, network identifiers, gas parameters, block time targets, consensus parameters, and network topology details.

Network claims are verified against the actual network configuration in the node source code and against live network queries. Some claims such as endpoint availability can be verified by attempting connections.

### Concept Claims

Concept claims describe higher level ideas and design patterns in the Midnight ecosystem. These include descriptions of the privacy model, ZK proof architecture, token economics, governance mechanisms, and cross chain integration details.

Concept claims are harder to verify automatically and often require expert review and cross referencing against multiple sources. The pipeline flags concept claims for manual review with lower initial confidence scores.

### SDK Claims

SDK claims describe the behavior of Midnight SDK packages including their APIs, initialization patterns, error handling, and integration requirements. These are similar to API claims but focus on the developer experience and integration patterns rather than individual function signatures.

SDK claims are verified by examining the SDK source code, running the SDK against test networks, and checking for consistency with published examples and tutorials.


## Verification Methods

### Source Cross-Referencing

Source cross-referencing compares documentation claims against the actual source code in the Midnight GitHub repositories. This is the most reliable verification method since the source code defines actual behavior.

The cross-referencing process clones relevant repositories and searches for the APIs, types, and constants described in the documentation. Discrepancies between documented and actual signatures are flagged as errors.

For TypeScript packages the published `.d.ts` type definition files provide a stable interface that can be compared against documentation claims. The fact-checker extracts type information from these files and matches it against claimed types.

```typescript
interface CrossReferenceResult {
  readonly claim: Claim;
  readonly sourceMatch: boolean;
  readonly actualSignature?: string;
  readonly sourceFilePath?: string;
  readonly sourceLineNumber?: number;
}
```

### API Testing

API testing verifies claims by actually executing the described API calls against a test network. This catches claims that are technically correct in source code but misleading in practice due to environment specific behavior.

```bash
npx midnight-fact-check test-api \
  --network preprod \
  --claim "WalletFacade.fromMnemonic accepts 12 word BIP39 phrases"
```

API tests run against configurable networks and can be parameterized with test mnemonics and wallets. Tests produce pass or fail results with detailed error information for failures.

### Compile Verification

Compile verification checks Compact language claims by attempting to compile example code. If the claimed syntax or type is valid the compiler should accept it. If the claimed behavior is accurate the compiled output should match expectations.

```bash
npx midnight-fact-check verify-compile \
  --contract examples/test-claim.compact \
  --expected-outcome success
```

### Runtime Behavior Checks

Runtime behavior checks deploy contracts and execute transactions to verify behavioral claims that cannot be checked through static analysis alone. These checks run against a local developer network to avoid consuming testnet resources.

Runtime checks are the most expensive verification method and are reserved for high value claims where static analysis is insufficient. They provide the highest confidence since they verify actual end to end behavior.


## Multi-Source Validation

### Official Docs

Official Midnight documentation hosted on docs.midnight.network serves as the primary reference for documentation claims. When verifying claims from other sources the official docs provide the baseline for comparison.

The fact-checker maintains a cache of official documentation pages and their last update timestamps. When a claim is extracted it is first checked against the current official documentation for consistency.

### GitHub Repos

The Midnight GitHub organization hosts the source code for all official packages. The repositories under `github.com/midnight-ntwrk` are the authoritative source for API definitions, type signatures, and implementation behavior.

The fact-checker clones or fetches from these repositories to access the latest source code. It tracks repository tags and release branches to verify version specific claims against the correct code snapshot.

### NPM Packages

Published npm packages under the `@midnight-ntwrk` scope provide the distributed versions of Midnight SDK packages. The package metadata including version numbers, dependencies, and published types is used to verify distribution related claims.

The fact-checker queries the npm registry for package information and compares it against claims in documentation. Package version claims that do not match the latest published version are flagged as outdated.

### Community Sources

Community sources including blog posts, tutorials, and forum discussions may contain additional claims. These sources are treated with lower confidence and flagged for verification against official sources before being accepted.

Community sources that consistently align with official sources can be promoted to secondary references. Sources that diverge are noted with warnings for readers.


## Verification Report Generation

### Structured Reports

Verification reports present findings in a structured format that highlights verified claims, unverified claims, and claims found to be incorrect. Each claim in the report includes its source location, verification status, confidence level, and supporting evidence.

Reports are generated in multiple formats for different consumers. Developers receive detailed reports with source code references. Technical writers receive summaries with correction suggestions. CI systems receive machine readable reports with exit codes.

### Confidence Levels

Each verified claim is assigned a confidence level that reflects the certainty of the verification result. The levels range from `high` for claims verified against source code to `low` for claims verified only against community sources.

Claims that could not be verified are assigned an `unverified` status with suggestions for how to verify them. Claims that were verified but with caveats are assigned an `uncertain` status with notes about the caveats.

### Source Attribution

Every verified claim includes attribution to the sources used for verification. This includes the specific file paths, line numbers, and commit hashes from the source code as well as the URLs and timestamps for web sources.

Source attribution enables readers to independently verify claims and provides an audit trail for the verification process. When sources change the attribution links may break which is itself a signal that claims need re-verification.

### Unresolved Claims

Claims that could not be resolved are listed separately with the reason for non-resolution. Common reasons include insufficient source access, conflicting information across sources, and claims about behavior that cannot yet be tested against any available network.

Unresolved claims are reviewed on a regular schedule and rechecked when new verification capabilities become available or when relevant source code is published.


## Automated Checking

### CLI-Based Verification

The fact-checking pipeline provides a command line interface for running verification tasks. The CLI supports claim extraction, verification, and report generation from the terminal.

```bash
npx midnight-fact-check extract --docs docs/ --output claims.json

npx midnight-fact-check verify \
  --claims claims.json \
  --network preprod \
  --output report.md

npx midnight-fact-check report \
  --claims claims.json \
  --format markdown \
  --output fact-check-report.md
```

### Integration with CI Pipelines

The fact-checker integrates with GitHub Actions to run verification on every pull request that modifies documentation. The CI job extracts claims from the changed files and verifies them against current source code.

```yaml
name: Fact Check Documentation
on:
  pull_request:
    paths:
      - 'docs/**'
      - 'packages/**/README.md'
jobs:
  fact-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Extract claims
        run: npx midnight-fact-check extract --docs docs/ --output claims.json
      - name: Verify claims
        run: npx midnight-fact-check verify --claims claims.json --network preprod
      - name: Check report
        run: npx midnight-fact-check report --claims claims.json --format ci-exit-code
```

### Scheduled Checks

Scheduled checks run on a regular cadence to detect documentation drift over time. Even without documentation changes the source code and network behavior may change making previously accurate claims incorrect.

Weekly scheduled checks extract claims from all documentation and re-verify them against the latest source code and network state. Any newly broken claims are reported as issues in the documentation repository.

```yaml
name: Weekly Fact Check
on:
  schedule:
    - cron: '0 6 * * 1'
jobs:
  weekly-fact-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run weekly fact check
        run: |
          npx midnight-fact-check extract --docs docs/ --output claims.json
          npx midnight-fact-check verify --claims claims.json --network mainnet
          npx midnight-fact-check verify --claims claims.json --network preprod
          npx midnight-fact-check report --claims claims.json --format markdown --output reports/weekly.md
      - name: Open issues for failures
        if: failure()
        run: |
          npx midnight-fact-check report --claims claims.json --format github-issues
```


## Common Claim Types

### Version Numbers

Version number claims specify the current version of a Midnight package, component, or network. These claims become stale quickly as new versions are released. The fact-checker verifies version numbers against npm registry metadata and GitHub release tags.

```markdown
Claim: "@midnight-ntwrk/dapp-connector-api version 4.0.1 supports the connect method"
Source: docs/dapp-connector.md:42
Verification: Check npm registry for @midnight-ntwrk/dapp-connector-api@4.0.1
```

### Function Signatures

Function signature claims specify the parameter types, return types, and thrown exceptions of SDK functions. These are verified against TypeScript type definition files and JSDoc annotations in the source code.

```markdown
Claim: "createUnprovenCallTx(providers, method, args) returns Promise<UnprovenTransaction>"
Source: docs/contract-interaction.md:78
Verification: Check contracts package source for createUnprovenCallTx signature
```

### Type Definitions

Type definition claims describe the structure of TypeScript types and interfaces in the SDK. These are verified by extracting the actual type definitions from `.d.ts` files and comparing the structure.

```markdown
Claim: "Configuration type has readonly networkId of type NetworkId"
Source: docs/dapp-connector.md:15
Verification: Check dapp-connector-api types for Configuration interface
```

### Error Codes

Error code claims document the error types and codes that can be thrown by SDK functions. These are verified by examining error class definitions and throw statements in the source code.

```markdown
Claim: "CallTxFailedError includes fields txHash, phase, and reason"
Source: docs/error-handling.md:23
Verification: Check contracts package for CallTxFailedError class definition
```

### Network Endpoints

Network endpoint claims specify the URLs for RPC nodes, indexers, proof servers, and faucets. These are verified by checking the actual network configuration and attempting connections.

```markdown
Claim: "Preprod indexer is at https://indexer.preprod.midnight.network/api/v1/graphql"
Source: docs/network-config.md:10
Verification: Check network configuration and attempt connection
```

### Gas Costs

Gas cost claims describe the DUST cost of various operations. These are verified by examining the network parameters and testing actual transaction costs on test networks.

### Configuration Defaults

Configuration default claims specify the default values for SDK configuration options. These are verified by examining the default parameter values in the source code constructors and factory functions.


## Source Hierarchy

### Official Docs as Primary

Official Midnight documentation at docs.midnight.network is treated as the primary reference for what developers should believe. When fact-checking reveals discrepancies the official docs are updated to match reality rather than the reverse.

The fact-checker includes a special mode that compares community documentation against official docs to identify areas where unofficial sources diverge from the canonical reference.

### GitHub Source Code as Authoritative

The source code in GitHub repositories is the authoritative source for API behavior. When documentation claims conflict with source code the source code is considered correct and documentation is flagged for correction.

Source code verification uses specific commit hashes or release tags to ensure reproducibility. The fact-checker records which version of the source code was used for each verification.

### NPM Package Metadata

Package metadata from the npm registry provides the authoritative version numbers and dependency declarations. The fact-checker trusts npm metadata over hardcoded version numbers in documentation.

### Community Consensus

Community sources provide supporting evidence but are not treated as authoritative. Claims supported only by community sources receive lower confidence scores and are flagged for verification against official sources.


## Fact-Check Rules

### Version Freshness Check

Claims that reference specific version numbers are checked for freshness against the latest published versions. If a documented version is more than two minor versions behind the latest the claim is flagged as potentially stale.

Version freshness checks run automatically as part of the scheduled verification pipeline. When new versions are published all documentation claims referencing the old version are flagged for review.

### Dead Link Detection

All URLs in documentation are checked for reachability. Links that return HTTP error codes or fail to resolve are flagged as dead. The fact-checker attempts multiple retries over time to distinguish transient failures from truly dead links.

Dead links in documentation are categorized by severity. Links to official resources are critical. Links to community resources are lower priority. Links that were available previously and recently became unavailable are flagged for investigation.

### Deprecated API Flagging

When APIs are deprecated in the source code the fact-checker flags documentation that still references the deprecated API without noting its deprecated status. Documentation should either remove deprecated API references or clearly mark them as deprecated with migration guidance.

The fact-checker monitors deprecation annotations in source code and cross references them against documentation references to the same APIs.

### Breaking Change Detection

When new SDK releases include breaking changes the fact-checker flags documentation that describes the old behavior without noting the change. Breaking changes include removed functions, changed parameter types, new required parameters, and changed error behavior.

Breaking change detection relies on the GitHub release notes and changelog entries. The fact-checker parses these for breaking change announcements and verifies that documentation has been updated accordingly.


## Integration with Midnight Expert

### Health Checks Feed into Fact-Check Pipeline

The midnight-expert health check system monitors the operational status of Midnight network services. When a health check detects a service degradation or configuration change the fact-check pipeline is triggered to verify documentation claims about the affected service.

For example if the health check detects that a proof server endpoint has changed the fact-checker re-verifies all documentation claims that reference the proof server URL and flags any that are now incorrect.

```typescript
interface HealthCheckEvent {
  readonly service: string;
  readonly endpoint: string;
  readonly previousState: 'healthy' | 'degraded';
  readonly currentState: 'healthy' | 'degraded' | 'unavailable';
  readonly timestamp: number;
}
```

### Ecosystem Compatibility Verification

The fact-checker verifies compatibility claims between Midnight packages by comparing their dependency declarations in npm metadata against the claimed compatible versions in documentation.

When a new version of a dependency is released the fact-checker verifies whether the documented compatibility range still covers the new version and flags any gaps.


## Report Formats

### Markdown Reports

Markdown reports present verification results in a human readable format suitable for inclusion in documentation repositories. Each finding includes the claim text, source location, verification result, and recommended action.

```markdown
## Fact Check Report

### Summary
- Total claims: 142
- Verified: 118 (83%)
- Unverified: 15 (11%)
- Incorrect: 9 (6%)

### Incorrect Claims

#### Claim: WalletFacade.fromMnemonic returns Promise<Wallet>
**Source:** docs/wallet.md:156
**Finding:** Return type in source is `Promise<WalletFacade>` not `Promise<Wallet>`
**Recommendation:** Update docs/wallet.md:156 to use `Promise<WalletFacade>`
```

### JSON Output

JSON output provides structured verification results for programmatic consumption. The JSON schema includes all claim metadata, verification results, and source attribution.

```json
{
  "report": {
    "generated": "2026-06-27T12:00:00Z",
    "claims": [
      {
        "id": "claim-001",
        "text": "Vite create command uses react-ts template",
        "source": { "file": "docs/quickstart.md", "line": 12 },
        "domain": "sdk",
        "status": "verified",
        "confidence": "high",
        "sources": ["github:midnight-ntwrk/example-counter"],
        "verifiedAt": "2026-06-27T12:00:01Z"
      }
    ]
  }
}
```

### CI-Friendly Exit Codes

When running in CI environments the fact-checker uses exit codes to signal verification results. Exit code 0 means all claims verified successfully. Exit code 1 means one or more claims were found incorrect. Exit code 2 means verification could not be completed.

### Human-Readable Summaries

Concise summaries present the key findings without overwhelming detail. These are suitable for inclusion in pull request comments and status updates.

```
Fact Check Summary for docs/contract-api.md
3 claims extracted | 2 verified | 1 incorrect
Incorrect: The submitCallTx return type in docs does not match source
Fix: Update line 234 to use `Promise<TransactionResult>` instead of `Promise<string>`
```


## Doc Maintenance

### Flagging Outdated Documentation

The fact-check pipeline automatically creates issues or comments on documentation files that contain outdated claims. Each flag includes the specific claim, the corrected value, and a suggested edit.

Documentation maintainers receive notifications for newly flagged claims and can accept or reject the suggested corrections. Accepted corrections can be applied automatically through a GitHub commit or pull request.

### Suggesting Corrections

When a claim is found to be incorrect the fact-checker generates a suggested correction in diff format. The suggestion shows the exact change needed to bring the documentation in line with the verified behavior.

```diff
- `createUnprovenCallTx` returns `Promise<UnprovenTransaction>`
+ `createUnprovenCallTx(providers, method, args?)` returns `Promise<UnprovenCallTx>`
```

### Tracking Doc Drift Over Time

The fact-checker maintains a history of verification results that tracks how documentation accuracy changes over time. This reveals trends such as increasing drift after rapid development periods or improvements after dedicated documentation sprints.

Historical tracking enables measurement of documentation quality metrics such as the percentage of verified claims and the average time to fix incorrect claims. These metrics inform resourcing decisions for documentation maintenance.

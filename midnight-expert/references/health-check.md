# Ecosystem Health Check System

Comprehensive health verification for the Midnight development ecosystem covering plugins, tools, networks, and version compatibility.

## Plugin Health Verification

### SKILL.md Presence

Each plugin directory must contain a SKILL.md file at its root. The check scans the skills base directory and lists any plugin directory missing this file. A valid SKILL.md must contain at minimum a level one heading matching the plugin name, a description section, and a references section.

### skill.json Validity

The skill.json file is validated against the skillsrc.json schema. Required fields include name, version, description, and author. The version field must follow semver format. Optional fields include dependencies, capabilities, and configuration. Validation errors are reported with the exact field and expected format.

### References Integrity

Each reference file listed in the SKILL.md references section must exist on disk. The check follows relative paths from the SKILL.md location. Missing references are reported with the expected path. The check also validates that reference files are not empty and contain at minimum 10 lines of content suggesting substantive documentation.

### Scripts Executability

If a plugin declares scripts in skill.json the check verifies each script file exists and has the execute permission bit set. Scripts must return exit code 0 when invoked with `--help` or `--version` flags. Scripts that fail basic invocation are flagged for review.

## Tool Availability Checks

### compactc

The compiler binary must be on the system PATH. The check runs `compactc --version` and captures the output. If the command fails with a not found error the check reports compactc as unavailable. Version information is parsed and compared against the minimum required version defined in the version compatibility matrix.

### Docker

Docker must be installed and the daemon must be running. The check runs `docker version --format json` and verifies both client and server components respond. If Docker is installed but the daemon is stopped the check reports Docker as partially available with instructions to start the daemon.

### Node.js

Node.js must be version 18 or later. The check runs `node --version` and parses the major version number. If the version is below 18 the check reports the current version and the minimum requirement. The npm version is also captured via `npm --version` and must be version 9 or later.

### npm

The npm client must be functional and able to install packages. The check runs `npm ping` to verify registry connectivity. It also validates that the global npm prefix is writable to avoid permission errors during package installation.

### Wallet CLI

The Midnight wallet CLI tool if present is checked with `midnight-wallet --version`. The check verifies the wallet can access its key storage directory and that the storage is not corrupted. A corrupted keystore is reported as a warning rather than an error since it may be intentional for development environments.

## Network Diagnostics

### Endpoint Reachability

Each network endpoint defined in the configuration is tested with an HTTP GET to the health check path. Expected endpoints include the RPC node, the proof server, and the indexer GraphQL endpoint. A timeout of 5 seconds is applied per endpoint. Unreachable endpoints are reported with the connection error details.

### Chain Synchronization

The RPC node is queried for its current block height and syncing status. The check compares the node block height against the expected chain height from a trusted source or secondary node. If the node is more than 10 blocks behind or reports `syncing: true` the check flags a synchronization issue.

### Proof Server

The proof server health endpoint is queried for status. The expected response includes the server version, loaded contract count, and queue depth. A healthy proof server responds within 2 seconds and reports a queue depth below 100. High queue depth indicates proving capacity problems.

### Indexer

The indexer GraphQL endpoint is tested with a basic introspection query. The check verifies the GraphQL schema is accessible and that the indexer has processed blocks up to within 5 blocks of the chain tip. A stale indexer is reported with the current lag in blocks.

## Version Compatibility Matrix

The compatibility matrix defines which versions of each component are supported together.

| Component | Minimum Version | Maximum Version |
|-----------|----------------|-----------------|
| compactc | 0.8.0 | latest |
| midnight-node | 0.12.0 | latest |
| midnight-proof-server | 0.6.0 | latest |
| midnight-indexer | 4.0.0 | latest |
| midnight-js-sdk | 1.0.0 | latest |
| wallet-sdk | 0.5.0 | latest |
| Node.js | 18.0.0 | 22.x |
| Docker | 24.0.0 | latest |
| npm | 9.0.0 | latest |

## Report Generation

### Markdown Report

The default output format is a markdown report saved to `health-report.md`. The report opens with a summary section showing the overall health score and pass or fail counts by category. Each section details individual checks with status icons, messages, and remediation steps.

### JSON Report

The `--format json` flag produces machine readable output written to `health-report.json`. The JSON structure includes a top level status field, a results array with per-check detail objects, and a metadata block with the timestamp and environment information. JSON output is suitable for CI pipeline consumption.

### HTML Report

The `--format html` flag produces a standalone HTML report with collapsible sections, color coded status indicators, and inline remediation instructions. The HTML file includes embedded CSS and requires no external resources. It is suitable for sharing with team members who prefer a browser view.

## CI Integration

Add a health check step to your GitHub Actions workflow.

```
- name: Ecosystem Health Check
  run: npx midnight-health-check --format json
- name: Validate Health
  run: npx midnight-health-check --ci --min-score 80
```

The `--ci` flag ensures the check exits with a non-zero code when the health score falls below the `--min-score` threshold. The `--format json` flag produces output that can be uploaded as a CI artifact for post-run review.

For scheduled checks add a cron workflow.

```
on:
  schedule:
    - cron: '0 6 * * 1'
```

This runs the health check every Monday morning at 6 AM UTC providing a weekly ecosystem health snapshot. Configure notifications for health score regressions using GitHub Actions notification settings.

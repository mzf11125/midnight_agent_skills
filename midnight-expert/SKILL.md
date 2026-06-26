---
name: midnight-expert
description: Meta skill for Midnight ecosystem diagnostics, health checks, version compatibility, and environment validation. Use when troubleshooting setup issues, verifying cross-plugin compatibility, running health checks, generating diagnostic reports, or integrating Midnight health checks into CI pipelines. Acts as the ecosystem diagnostician coordinating all Midnight skills.
---

# Midnight Expert

## Midnight Expert Overview

Midnight Expert is the meta plugin for ecosystem diagnostics across all Midnight development tooling. It coordinates health checks, version compatibility verification, dependency scanning, and environment validation across the entire Midnight stack. When a developer encounters issues that span multiple components, Midnight Expert provides a unified diagnostic view that identifies root causes and recommends resolutions.

The meta plugin design means that Midnight Expert does not directly implement diagnostic logic. Instead, it orchestrates the diagnostic capabilities of each specialized plugin. It queries the proof server plugin for proof generation health, the indexer plugin for data pipeline health, the tooling plugin for development environment health, and other plugins for their respective domains.

Midnight Expert is activated through the `doctor` command which runs a full diagnostic sweep. The `doctor` command produces a summary report, a detailed JSON report, and actionable recommendations. It can be run interactively in the terminal or integrated into CI pipelines for automated health checks.

Version matrix management is a core responsibility. Midnight Expert maintains a comprehensive mapping of which versions of each component are compatible with each other. This matrix is consulted during health checks to detect version mismatches that could cause subtle runtime errors.

Network diagnostics verify that all required network endpoints are reachable. This includes the node JSON-RPC endpoint, the indexer GraphQL endpoint, the proof server HTTP endpoint, and any faucet endpoints. Each endpoint is tested for connectivity, response time, and health status.

## Health Check System

The health check system runs a series of checks against each plugin and aggregates the results. Each check returns a status of healthy, degraded, or unhealthy, along with a human-readable message and diagnostic data. The system categorizes checks by severity so that critical issues that prevent development are highlighted while informational issues are noted but do not block the report.

Plugin health checks cover the core Midnight plugins. The indexer plugin is checked for database connectivity, sync progress versus the node's current height, and GraphQL endpoint responsiveness. The proof server plugin is checked for key material availability, proof generation capability, and endpoint responsiveness. The tooling plugin is checked for Docker availability, compiler presence, and network configuration. The compact plugin is checked for compiler version compatibility and contract compilation ability.

Tool availability checks verify that required executables are present. These checks look for Docker in the PATH with `docker --version`, the Compact compiler with `compactc --version`, Node.js with `node --version`, the package manager with `yarn --version` or `bun --version`, and the wallet CLI if installed.

Network connectivity checks verify reachability of the node endpoint by sending a JSON-RPC request, the indexer GraphQL endpoint by sending an introspection query, the proof server endpoint by sending a health check request, and external registries such as the GitHub Packages registry.

Configuration validation checks verify the Docker Compose configuration for syntax and semantics, the package.json for required Midnight dependencies, the TypeScript configuration for proper settings, and environment variables for correct values.

## Dependency Scanning

Dependency scanning analyzes the project's dependencies against the version compatibility matrix. It identifies version conflicts where multiple versions of the same package are present, missing dependencies where a required package is not installed, outdated packages where a newer compatible version is available, and incompatible upgrades where upgrading one package would break compatibility with others.

The scanner reads the project's `package.json` and lockfile to determine which versions are installed. It cross-references these versions against the compatibility matrix to check for known issues. It also checks for security vulnerabilities in installed packages using the npm audit or yarn audit tools.

Version compatibility checking is the most sophisticated part of dependency scanning. The compatibility matrix defines compatible version ranges for each pair of packages. For example, midnight-js version 0.8.x requires compact-runtime version 0.8.x and indexer version 4.x. The scanner checks that all pairs satisfy their constraints and reports any violations.

Dependency conflict detection looks for cases where two packages depend on conflicting versions of a shared dependency. This can happen with transitive dependencies. The scanner uses the lockfile to identify these conflicts and recommends resolution strategies such as adding a resolution override or upgrading one of the conflicting packages.

Missing dependency detection verifies that all packages listed as required by the project's configuration are actually installed. This includes checking for peer dependencies that may not be automatically installed. The scanner also checks for optional dependencies that may be needed for certain features.

Outdated package detection compares installed versions against the latest published versions. It distinguishes between compatible updates that can be applied safely and breaking updates that require migration work. The scanner provides upgrade recommendations with associated risk levels.

## Plugin Registry

The plugin registry maintains a list of all installed Midnight plugins and their capabilities. Each plugin registers its name, version, skill count claiming how many skills it provides, agent count claiming how many specialized agents it defines, reference count claiming how many reference documents it bundles, dependencies on other plugins, and capabilities that other plugins can query.

Plugins can be queried for their capabilities. The registry provides a discovery mechanism so that Midnight Expert can find which plugin handles a specific diagnostic or operation. When a health check fails, the registry identifies the responsible plugin and routes the diagnostic request to it.

Skill counts track how many skills each plugin provides. This helps Midnight Expert understand the scope of each plugin and identify gaps in coverage. Agent counts track specialized agent definitions. Reference counts track bundled documentation and reference materials.

Plugin capabilities include proof generation for the proof server plugin, data querying for the indexer plugin, contract compilation for the compact plugin, environment setup for the tooling plugin, network management for the multinetwork plugin, wallet operations for the specific wallet plugins, and token management for the token plugin.

## Version Compatibility Matrix

The version compatibility matrix is the authoritative reference for which versions of each Midnight component work together. The matrix is organized as a table where rows and columns represent components and cells indicate whether specific versions are compatible.

Compact compiler versions are versioned independently. Version 0.8.x of the compiler produces ZKIR artifacts compatible with compact-runtime 0.8.x. Version 0.9.x is a breaking change that produces ZKIR artifacts only compatible with compact-runtime 0.9.x. Always use the compiler version that matches your target runtime.

Compact runtime versions determine which ZKIR artifact format is supported. The runtime version must match the compiler version used to produce the artifacts. The ledger has a minimum supported runtime version. Contracts compiled with an older compiler may not deploy on a newer ledger.

Ledger versions refer to the Midnight protocol version deployed on each network. The ledger version determines which transaction formats are accepted, which proof formats are verified, and which contract features are supported. Test networks typically run the latest ledger version while mainnet runs a stable release.

midnight-js versions must be compatible with the ledger version, the indexer GraphQL API version, and the proof server API version. Version 0.8.x of midnight-js supports GraphQL API v4 and proof server API v2. Upgrading midnight-js may require upgrading the indexer and proof server.

DApp Connector versions must match between the dApp and the browser wallet extension. The dApp uses a specific version of the DApp Connector API in its code. The wallet extension implements a specific version of the API. Both must use compatible versions for communication to work.

ZSwap versions define the protocol for shielded token swaps. ZSwap is versioned independently of the main Midnight protocol. The dApp must use a ZSwap version that is supported by both the proof server and the network.

Proof server versions define the API for proof generation requests. Version changes may add new features or change the proof format. The dApp must use a proof server version that is compatible with the midnight-js version and the network version.

Indexer versions define the GraphQL API version. Version 4 introduced subscriptions and the current schema. Future versions may add new query types or deprecate old types. The dApp must use an indexer version that provides the GraphQL API version expected by midnight-js.

Node versions define the node software version. The node must be compatible with the network it connects to. Test networks may require specific node versions. The local devnet node version should match the version used on the target test network.

## Network Diagnostics

### Endpoint Reachability

Endpoint reachability checks verify that the dApp can establish a network connection to each required endpoint. The check sends a TCP connection request to each endpoint's host and port. If the connection is refused or times out, the endpoint is unreachable. Common causes include the service not running, a firewall blocking the connection, or an incorrect URL configuration.

Each endpoint is checked sequentially. The node endpoint is tested by connecting to its JSON-RPC port and sending a `system_health` request. The indexer endpoint is tested by connecting to its GraphQL port and sending an introspection query. The proof server endpoint is tested by connecting to its HTTP port and requesting the status page. The faucet endpoint is tested by connecting to its HTTP port.

### Chain Sync Status

Chain sync status checks whether the local node or the connected node is synchronized with the network. The check queries the node's `system_syncState` JSON-RPC method. If the node reports that it is syncing, the check reports the current block and the target block. If the node reports that it is synced, the check confirms that the node is at the network's tip.

For the indexer, sync status checks whether the indexed block height matches the node's block height. A small lag is expected under normal operation. A large lag indicates that the indexer is falling behind and may need more resources or a restart.

### Proof Server Health

Proof server health checks verify that the proof server is operational. The check sends a health request to the proof server and verifies the response. A healthy proof server responds with a 200 status code and includes information about loaded contracts and key material availability.

If the proof server is unhealthy, the check reports the specific issue. Possible issues include missing ZKIR artifacts for deployed contracts, proving key generation failures, resource exhaustion, or configuration errors.

### Indexer Availability

Indexer availability checks verify that the indexer is accessible and responding to queries. The check sends a simple GraphQL query such as `{ __typename }` to the indexer endpoint. If the query returns successfully, the indexer is available. If the query fails, the check reports the error for diagnosis.

### Faucet Status

Faucet status checks verify that the faucet service is available on test networks. The check sends a request to the faucet's health endpoint. If the faucet is available, the check confirms that test tokens can be requested. If the faucet is unavailable, alternative methods for acquiring test tokens are suggested.

## Tool Verification

### compactc in PATH

The `compactc` compiler must be available in the system PATH. The verification check runs `compactc --version` and confirms that the command executes successfully. If the command fails, the check provides installation instructions for the appropriate operating system.

### Docker Availability

Docker availability is verified by running `docker --version` and `docker compose version`. Both the Docker Engine and Docker Compose must be installed and the Docker daemon must be running. The check also verifies that the current user has permission to run Docker commands.

### Node.js Version

Node.js version is verified by running `node --version`. The version must be 18 or later. The check reports the installed version and whether it meets the minimum requirement. If the version is too old, upgrade instructions are provided.

### npm, yarn, or bun Availability

At least one of npm, yarn, or bun must be available as the package manager. The check runs each installed package manager's version command and reports which are available. Bun is recommended for Midnight development due to its performance advantages.

### Wallet CLI Presence

The wallet CLI verification checks whether the Midnight wallet CLI is installed. This is an optional tool but useful for development. The check runs `midnight-wallet --version` and reports whether the tool is available.

## Environment Validation

### Operating System Check

The operating system check identifies the host operating system and version. Midnight development is supported on Linux, macOS, and Windows via WSL. The check verifies that the operating system is supported and reports any known issues for that platform.

### Disk Space

Disk space verification checks that sufficient free disk space is available for the Midnight stack. The local devnet requires approximately 2 GB for Docker images, 1 GB for the blockchain state database, and additional space for node modules and build artifacts. At least 10 GB of free space is recommended.

### Memory

Memory verification checks that sufficient RAM is available. The local devnet requires approximately 4 GB for the node, 2 GB for the indexer including PostgreSQL, 4 GB for the proof server, and additional memory for the development tools. At least 16 GB of system memory is recommended for comfortable development.

### CPU

CPU verification checks that the processor meets the minimum requirements. A multi-core processor with at least 4 cores is recommended. The proof server benefits from higher clock speeds and more cores for concurrent proof generation. CPU feature checks verify that required instruction sets are available.

### Network Bandwidth

Network bandwidth checks are informational. The initial setup downloads several gigabytes of Docker images and dependencies. A fast internet connection reduces setup time. Bandwidth checks measure the download speed to estimate setup time.

## Doctor Command

### expert:doctor Implementation

The `expert:doctor` command runs a comprehensive diagnostic sweep of the Midnight ecosystem. It executes all health checks, dependency scans, and environment validations. Results are aggregated into a report with pass, warn, and fail indicators.

```bash
npx midnight-expert doctor
```

The command can be run with flags to control its behavior. The `--json` flag outputs the report in JSON format for programmatic consumption. The `--ci` flag runs in CI mode with stricter thresholds and machine-readable output. The `--fix` flag attempts to automatically fix detected issues.

### Summary Report

The summary report provides a high-level overview of the ecosystem health. It includes a pass count showing how many checks passed, a warn count showing how many checks have warnings that do not block development, a fail count showing how many checks failed and require attention, an overall health score from 0 to 100, and a list of critical issues that must be resolved.

The summary report is displayed at the top of the doctor output. It is designed to be scannable so that developers can quickly assess the state of their environment. Critical issues are highlighted for immediate attention.

### Detailed Report

The detailed report breaks down the results for each plugin and each check. For each failing check, it includes the error message, the root cause analysis, the recommended resolution steps, and links to relevant documentation. The detailed report is valuable for diagnosing complex issues that span multiple components.

### JSON Output

When the `--json` flag is used, the report is output as structured JSON. This format is suitable for integration with CI systems, monitoring dashboards, and automated remediation scripts. The JSON output includes all the same information as the human-readable report in a machine-parseable format.

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "overallHealth": 85,
  "plugins": {
    "indexer": { "health": "healthy", "checks": [] },
    "proofServer": { "health": "degraded", "checks": [] },
    "tooling": { "health": "healthy", "checks": [] }
  },
  "versionMatrix": {},
  "recommendations": []
}
```

## Quick Start Validation

The quick start validation checks whether a new developer can start building a Midnight dApp in under 5 minutes. This check runs through the entire setup flow and measures the time for each step. It verifies that Docker images can be pulled in under 2 minutes, that the local devnet becomes healthy in under 2 minutes, that the compiler is available and can compile a simple contract in under 30 seconds, that dependencies can be installed in under 1 minute, and that an example project can be built and tested in under 2 minutes.

If any step exceeds its time budget, the check reports the bottleneck. Common bottlenecks include slow Docker image downloads on the first run, insufficient CPU for proof generation, or network latency to the GitHub Packages registry. Recommendations are provided for each bottleneck.

The quick start validation is designed to catch setup issues early. It simulates the experience of a new developer following the getting started guide. If the validation fails, the developer knows that their environment needs attention before they start building.

## Cross Plugin Coordination

Midnight Expert coordinates across plugins to provide unified diagnostics. When a developer reports an error, Midnight Expert determines which plugins are involved and routes diagnostic questions to the appropriate plugin. This reduces the need for the developer to understand which plugin handles which domain.

Plugin dependency resolution ensures that diagnostics run in the correct order. For example, checking Docker availability must happen before checking the local devnet health. Checking the node endpoint must happen before checking the indexer sync status. Midnight Expert manages these dependencies automatically.

Avoiding duplicate work is another coordination responsibility. When two plugins need the same diagnostic information such as the node's block height, Midnight Expert queries it once and shares the result rather than making duplicate queries. This improves performance and reduces load on the services being checked.

## Report Generation

### Health Reports

Health reports provide a snapshot of the ecosystem's current state. They include pass/fail/warn indicators for each check, overall health score, trend data showing how health has changed over time, and recommendations for improving health. Health reports can be generated on demand or on a schedule.

### Compatibility Reports

Compatibility reports focus specifically on version compatibility. They list each component, its installed version, the latest available version, whether the versions are compatible according to the matrix, and upgrade recommendations with risk assessments. Compatibility reports are generated before upgrades to assess risk.

### Environment Reports

Environment reports document the development environment setup. They include the operating system, installed tools with versions, network configuration, Docker configuration, and project configuration. Environment reports are useful for sharing with team members or for troubleshooting issues that may be environment-specific.

### Output Formats

Reports support multiple output formats. Markdown is the default format for human-readable reports in the terminal. JSON is used for programmatic consumption and CI integration. HTML supports rich formatting and interactive elements for web-based viewing.

## CI Integration

### Health Checks in CI Pipelines

Midnight Expert can be integrated into CI pipelines to run health checks automatically. A CI step runs `midnight-expert doctor --ci` and fails the build if critical issues are found. This catches environmental problems before they affect development.

### PR Gates

Pull request gates use Midnight Expert to verify that dependency changes do not introduce compatibility issues. When a PR updates dependencies, the gate runs the dependency scanner and checks the compatibility matrix. If incompatible versions are introduced, the gate blocks the merge.

### Deployment Gates

Deployment gates use Midnight Expert to verify that the target environment is healthy before deploying. The gate runs health checks against the target network and verifies that all endpoints are reachable. If the environment is unhealthy, the deployment is blocked.

### Scheduled Checks

Scheduled checks run Midnight Expert on a regular schedule to monitor ecosystem health over time. Weekly checks track version drift and flag outdated dependencies. Daily checks verify network availability. Scheduled checks can alert the team via Slack or email when issues are detected.

## Troubleshooting Guide

### Common Setup Issues

Missing Docker permissions cause Docker commands to fail with permission denied. The resolution is to add the user to the docker group with `sudo usermod -aG docker $USER` and log out and back in.

Port conflicts occur when another service is using a port needed by the Midnight stack. The resolution is to identify the conflicting service and either stop it or change the Midnight port configuration.

Authentication failures when installing packages cause 403 Forbidden errors from the GitHub Packages registry. The resolution is to configure npm or yarn authentication with a GitHub personal access token that has the `read:packages` scope.

Disk space exhaustion causes Docker containers to fail to start or the node to fail to produce blocks. The resolution is to free up disk space by pruning unused Docker images and volumes and removing old build artifacts.

### Resolution Steps

For each diagnostic issue, Midnight Expert provides specific resolution steps. These steps are designed to be actionable even for developers new to the ecosystem. Steps include the exact commands to run, configuration changes to make, and links to documentation for more detailed guidance.

### Escalation Paths

When Midnight Expert cannot resolve an issue automatically, it provides escalation paths. For community support, it suggests posting in the Midnight Discord server with the diagnostic report attached. For official support, it provides the support contact for the relevant component. For documentation, it links to the relevant sections of the Midnight developer documentation.

## Plugin Development Guide

### Creating New Plugins

New plugins for Midnight Expert extend the ecosystem diagnostics to new domains. A plugin consists of a SKILL.md file following the standard plugin format, health check implementations, compatibility data, and diagnostic logic.

### Coding Standards

Plugin code should follow the existing Midnight plugin conventions. Use TypeScript for implementation. Write tests for health check logic. Document each check with a description, severity level, and resolution steps. Register the plugin with the plugin registry.

### Testing Requirements

Each health check must have corresponding tests. Tests should cover the healthy case where the check passes, warning cases where the check identifies a minor issue, error cases where the check identifies a critical issue, and edge cases such as timeouts or unexpected responses.

### Documentation Requirements

Each plugin must document its health checks, its compatibility requirements, its dependencies on other plugins, and its configuration options. Documentation should be written in the SKILL.md file following the standard format.

## Metadata Management

### Plugin Versions

Each plugin tracks its own version. The version follows semantic versioning. Version bumps occur when new health checks are added, existing checks are modified, or compatibility data is updated.

### Skill Counts

Skill counts track how many distinct skills a plugin provides. This metadata helps Midnight Expert understand plugin scope. Skill counts are reported in the plugin registry.

### Reference Counts

Reference counts track how many reference documents a plugin bundles. This metadata helps developers understand the documentation coverage. Reference counts are reported in the plugin registry.

### Update Tracking

Midnight Expert tracks when plugins were last updated. This helps identify stale plugins that may have outdated compatibility data or health checks. Update tracking warns developers when a plugin has not been updated in the recommended period.

## Best Practices

### Regular Health Checks

Run health checks regularly, not just when something breaks. Weekly health checks catch issues before they become critical. Pre-release health checks verify that the deployment environment is healthy. Post-upgrade health checks verify that the upgrade did not introduce new issues.

### Version Updates

Keep all Midnight components updated to compatible versions. Check the compatibility matrix before upgrading. Upgrade all components that share version constraints together. Test thoroughly after upgrading. Have a rollback plan in case the upgrade causes issues.

### Dependency Auditing

Audit dependencies regularly for security vulnerabilities. Use `npm audit` or `yarn audit` to identify vulnerable packages. Review transitive dependencies for unexpected additions. Lock dependency versions to prevent unexpected changes.

### Environment Consistency

Maintain consistent development environments across the team. Use Docker for the Midnight stack to ensure consistent service versions. Use version pinning for all development tools. Document the environment setup process. Use CI health checks to enforce consistency.

## Advanced Diagnostic Workflows

### Transaction Failure Diagnostics

When a transaction fails, Midnight Expert can trace the failure through the entire stack. The diagnostic workflow first checks the node for the transaction status using the transaction hash. It then checks the indexer for the transaction record and any associated contract actions. It checks the proof server logs for any proof generation errors. It checks the wallet for any signing or witness errors. The result is a complete trace of where the failure occurred and why.

The transaction diagnostic command accepts a transaction hash as input and produces a trace report. The report shows each component that the transaction passed through, the status at each component, timing information for performance analysis, and the root cause of any failure. This is especially valuable for debugging issues in production where the failure may be in a component that the developer does not directly control.

### Contract Deployment Diagnostics

Contract deployment diagnostics verify that a contract has been deployed correctly and is accessible. The diagnostic checks that the deployment transaction is confirmed on-chain, that the contract address is registered in the indexer, that the contract's ZKIR artifacts are available on the proof server, that the contract's proving keys have been generated, that the contract's initial state is queryable through the indexer, and that the contract can be called with a test invocation.

### Proof Generation Diagnostics

Proof generation diagnostics are triggered when a proof fails to generate. The diagnostic checks that the contract's ZKIR artifacts are loaded on the proof server, that the proving keys exist and are valid, that the witness data structure matches the circuit inputs, that the proof server has sufficient resources for proof generation, and that no transient errors such as timeouts caused the failure.

The diagnostic provides specific recommendations for each failure mode. For ZKIR missing errors, it recommends running the contract compilation step. For witness mismatch errors, it shows the expected input types versus the provided types. For resource errors, it recommends adjusting the proof server's resource allocation.

### Indexer Lag Diagnostics

Indexer lag diagnostics investigate why the indexer is falling behind the node. The diagnostic checks CPU and memory usage on the indexer container, PostgreSQL query performance using slow query analysis, disk I/O throughput, network latency between the indexer and the node, and the batch processing configuration. The diagnostic recommends resource allocation adjustments, PostgreSQL tuning, or configuration changes to resolve the lag.

### Multi-Network Diagnostics

Multi-network diagnostics verify that the dApp's configuration for different networks is correct. The diagnostic checks that the correct endpoints are configured for each network, that the correct contract addresses are used for each network, that the correct ZKIR artifacts are deployed for each network's contract versions, and that authentication credentials are correct for each network. This prevents the common mistake of using testnet configuration on mainnet or vice versa.

## Metrics Collection

### Diagnostic Metrics

Midnight Expert collects metrics during health checks and diagnostic runs. These metrics are useful for tracking ecosystem health over time and for identifying trends that may indicate emerging problems. Metrics are exported in Prometheus format for integration with monitoring systems.

Key diagnostic metrics include health check pass rate over time per component, diagnostic run duration to track performance, version drift to track how many versions behind each component is, dependency vulnerability count to track outstanding security issues, endpoint response times for network performance tracking, and proof generation time for performance monitoring.

### Trend Analysis

Trend analysis examines metrics over time to identify patterns. A gradual increase in indexer lag may indicate that the database needs optimization. A gradual increase in proof generation time may indicate that contract complexity is growing. A spike in dependency vulnerabilities may indicate that a major upgrade is needed. Trend analysis helps proactively address issues before they become critical.

### Alert Thresholds

Configurable alert thresholds determine when a diagnostic result triggers an alert. Critical thresholds include health score dropping below 60, proof server becoming unreachable, indexer falling more than 100 blocks behind the node, and dependency vulnerabilities with CVSS scores above 7. Warning thresholds include health score dropping below 80 but above 60, proof generation time exceeding the 95th percentile by 2x, indexer lag exceeding 10 blocks, and outdated dependencies more than one minor version behind.

## Log Aggregation

### Centralized Logging

For teams running their own Midnight infrastructure, centralized logging aggregates logs from all components. Each component should be configured to send logs to a centralized logging system such as Elasticsearch, Loki, or a cloud logging service. Aggregated logs enable cross-component debugging where an issue spanning the node, indexer, and proof server can be traced through a single query.

### Log Format Standards

Midnight Expert recommends standardized log formats for all components. Log entries should include a timestamp in ISO 8601 format, a severity level from debug, info, warn, to error, a component name to identify which service produced the log, a correlation ID that links related log entries across components during a single transaction, and a structured message with key information.

### Correlation Across Components

Correlation IDs are essential for tracing a single transaction through multiple components. When a dApp submits a transaction, it generates a correlation ID. This ID is passed to the node with the transaction, to the proof server with the proof request, and to the indexer through the transaction metadata. When debugging, all log entries for that transaction can be found by filtering on the correlation ID.

## Configuration Management

### Configuration File Structure

Midnight Expert recommends a structured approach to configuration management. Store configuration in environment-specific files such as `.env.local`, `.env.preprod`, and `.env.mainnet`. Use a configuration schema to validate that all required fields are present. Never commit secrets to version control. Use environment variables in CI for sensitive configuration values.

### Configuration Validation

Configuration validation checks that all required configuration values are present and that they have valid formats. Checks include verifying that endpoint URLs are well-formed, that addresses have the correct format for the target network, that timeouts are reasonable values, and that resource limits are within the machine's capacity.

### Environment Switching

Environment switching allows the same codebase to target different networks. Midnight Expert verifies that switching environments correctly updates all relevant configuration. The check ensures that contract addresses are updated to the target network's addresses, that endpoints are updated to the target network's endpoints, that authentication credentials are updated, and that the version compatibility matrix is checked for the target network's protocol version.

## Security Diagnostics

### Configuration Security Checks

Security diagnostic checks verify that the development and deployment configuration follows security best practices. Checks include verifying that no secrets are committed to version control, that authentication tokens have appropriate scopes and expiration, that HTTPS is used for all remote endpoints, that Docker containers run with least privilege, and that the CI pipeline does not expose secrets in logs.

### Key Material Security

Key material security checks verify that cryptographic keys are handled securely. Checks include verifying that proving keys are stored with appropriate permissions, that viewing keys are not logged or exposed, that wallet seed phrases are stored securely, and that CI environments use secure secret storage for any required keys.

### Network Security Verification

Network security verification checks that connections to Midnight services use appropriate security. Checks include verifying that TLS is enabled for remote connections, that certificate validation is not disabled, that WebSocket connections use secure protocols, and that API authentication is properly configured.

## Performance Benchmarking

### Proof Generation Benchmarks

Proof generation benchmarking measures the time and resources required to generate proofs for specific contracts. The benchmark runs proof generation multiple times and reports the mean, median, 95th percentile, and 99th percentile times. This helps identify contracts that may need circuit optimization and helps configure appropriate timeout values.

### Indexer Query Benchmarks

Indexer query benchmarking measures the response time for common query patterns. The benchmark runs each query pattern multiple times and reports performance statistics. Slow queries are flagged for optimization. The benchmark also measures how query performance degrades as the indexer's database grows.

### End-to-End Transaction Benchmarks

End-to-end transaction benchmarking measures the full lifecycle of a transaction from preparation through confirmation. The benchmark includes wallet preparation time, witness collection time, proof generation time, transaction submission time, and confirmation time. This provides a realistic picture of the user experience for dApp interactions.

## Recovery Procedures

### Container Recovery

When a Docker container fails, Midnight Expert provides recovery procedures. For the node container, restart with `docker compose restart node`. If the state is corrupted, reset with `midnight-local-dev reset` which deletes all state and starts from genesis. For the indexer container, restart with `docker compose restart indexer`. The indexer will resume indexing from where it left off. For the proof server container, restart with `docker compose restart proof-server`. The proof server will reload ZKIR artifacts and regenerate keys as needed.

### Database Recovery

PostgreSQL database recovery procedures cover corrupted indexes which can be rebuilt with `REINDEX DATABASE`, disk full errors which require freeing space and restarting the database, connection limit errors which require increasing the connection pool size, and slow query performance which requires analyzing the query plan and adding indexes.

### Network State Recovery

Network state recovery procedures cover cases where the blockchain state needs to be restored. The local devnet can be reset to genesis with `midnight-local-dev reset`. Remote test networks cannot be reset by individual developers. If a remote network is reset by the operator, developers must clear their local state and reconnect.

## Integration with External Monitoring

### Prometheus Integration

Midnight Expert exports health check results as Prometheus metrics. This allows Midnight ecosystem health to be monitored alongside other infrastructure in a unified dashboard. Metrics include a `midnight_health_check_status` gauge per check, a `midnight_version_info` gauge per component, and a `midnight_dependency_vulnerability` gauge per vulnerability.

### Grafana Dashboards

Pre-built Grafana dashboards are available for visualizing Midnight ecosystem health. The overview dashboard shows the health score for each component with color coding. The version dashboard shows installed versions versus available versions for each component. The performance dashboard shows proof generation times and indexer query times over time. The network dashboard shows endpoint response times and sync status.

### Alert Manager Integration

Alert Manager rules can be configured based on Midnight Expert metrics. Rules can trigger alerts when the health score drops, when any endpoint becomes unreachable, when version drift exceeds a threshold, or when security vulnerabilities are detected. Alerts can be routed to Slack, email, or PagerDuty based on severity.

## Offline Diagnostics

### Air-Gapped Diagnostics

For environments without internet access, Midnight Expert supports offline diagnostics. The offline mode skips checks that require network access and relies on cached data for version compatibility and dependency information. Cached data must be periodically updated by running Midnight Expert online and exporting the data.

### Export and Import

Diagnostic data can be exported to a file for sharing with support or for analysis on another machine. The export includes all health check results, the full version matrix, dependency scan results, and environment information. The import function loads a previously exported diagnostic report for review or comparison.

### Comparison Reports

Comparison reports highlight differences between environments. Run diagnostics on two environments and then compare the results. This helps identify why an issue occurs in one environment but not another. Common differences include different package versions, different Docker image tags, different network configurations, and different operating system versions.

## Continuous Improvement

### Diagnostic Coverage Tracking

Midnight Expert tracks which aspects of the ecosystem have diagnostic coverage and which do not. Coverage gaps are reported so that new diagnostics can be developed. The coverage tracking includes the number of potential failure modes and the number that have automated diagnostics, expressed as a coverage percentage.

### Diagnostic Accuracy Tracking

When a diagnostic produces a recommendation, Midnight Expert tracks whether that recommendation resolved the issue. This feedback loop improves diagnostic accuracy over time. Developers can report whether a diagnostic was helpful, partially helpful, or not helpful. This data feeds into future diagnostic improvements.

### Community Contributions

New diagnostics and improvements to existing diagnostics can be contributed by the community. Contribution guidelines ensure that new diagnostics follow the established patterns for implementation, testing, and documentation. Community contributed diagnostics are reviewed for accuracy and safety before being merged.


---
name: midnight-plugin-utils
description: Infrastructure utilities for Midnight plugins. Use when checking plugin dependencies, verifying required tools are installed, scanning for installed plugins, resolving plugin roots, validating plugin structures, managing cross-plugin compatibility, handling configuration, performing file system operations, managing child processes, checking network connectivity, setting up logging, formatting errors, building plugin tests, scaffolding new plugins, integrating build systems, or connecting with midnight-expert. Provides shared infrastructure components used across all Midnight agent skills and plugins.
---

# Midnight Plugin Utilities

Shared infrastructure utilities for all Midnight plugins and agent skills. This skill covers dependency management, plugin discovery, configuration handling, process management, and development tooling.

## Plugin Utilities Overview

The Midnight plugin ecosystem depends on a shared set of infrastructure utilities that handle common concerns across all plugins. Rather than each plugin implementing its own version of these utilities, the plugin utilities package provides a single implementation that all plugins can depend on. This ensures consistent behavior, reduces duplicate code, and simplifies maintenance.

The utilities cover eight functional areas: dependency checking ensures the development environment has required tools. Plugin scanning discovers what is installed and what capabilities are available. Root resolution finds plugin directories and configuration files. Structure validation ensures plugins follow the expected conventions. Configuration management handles per-plugin and centralized settings. Process management handles running external tools and Docker containers. Network utilities verify connectivity to Midnight services. Logging and error utilities provide consistent output formatting.

All utilities in this package are designed to be self-contained with minimal external dependencies. They should work on Linux, macOS, and Windows. Error messages are clear and actionable. When a utility fails it should provide enough information for the developer to diagnose and fix the issue without needing to consult external documentation.

## Dependency Checking

Before any plugin can perform its work the development environment must have the required tools installed. Dependency checking verifies that all prerequisites are met.

### Required Tools

The dependency checker verifies the presence of these tools: `compactc` the Compact language compiler, Docker for containerized local development, Node.js for TypeScript and JavaScript execution, npm or bun for package management, the wallet CLI for wallet operations, and the proof server binary for proof generation. Each tool is checked independently and a summary report lists which tools are available and which are missing.

```typescript
import { checkDependencies } from "midnight-plugin-utils";

const result = await checkDependencies();
if (!result.allSatisfied) {
  for (const missing of result.missing) {
    console.error(`Missing: ${missing.tool} (requires ${missing.requiredVersion})`);
  }
}
```

The checker looks for tools on the system PATH. It also checks common installation directories such as `/usr/local/bin`, `~/.cargo/bin`, and `~/.nvm/versions`. If a tool is installed but not on PATH the checker reports this and suggests configuration changes.

### Version Requirements

Each tool has minimum version requirements. Node.js version must be 18.0.0 or higher. Docker version must be 24.0.0 or higher. The compactc compiler must be the latest stable release. npm must be version 9.0.0 or higher. The checker compares installed versions against these requirements and reports any tools that need upgrading.

The version checker uses semantic version comparison. Pre-release versions are considered lower than release versions. Tools at exactly the minimum version satisfy the requirement. Tools above the minimum version satisfy the requirement.

### compactc

The `compactc` compiler is the most critical dependency for Midnight contract development. The checker verifies that `compactc` is installed, that it is executable, and that it produces expected output when run with the version flag. The version output is parsed to extract the compiler version number.

### Docker

Docker is required for running the local Midnight network stack. The checker verifies that the Docker daemon is running by calling `docker version`. It also checks that the Docker Compose plugin is available for orchestrating the multi-container network stack.

### Node.js

Node.js provides the JavaScript runtime for Midnight TypeScript packages. The checker verifies that `node` is installed and meets the minimum version. It also checks that the `npm` package manager is available and functional.

### npm

npm is the package manager used by most Midnight projects. The checker runs `npm --version` to verify npm availability and version. It also checks that the npm registry is reachable by attempting a basic metadata query.

### bun

bun is an alternative JavaScript runtime and package manager. Some Midnight projects use bun for faster installation and execution. The checker verifies bun availability if the project configuration indicates bun usage.

### Wallet CLI

The wallet CLI provides command-line wallet operations for testing. The checker verifies that the wallet CLI is installed and that it can be invoked. The wallet CLI is typically installed as part of the Midnight development tooling.

### Proof Server Binary

The proof server binary provides local proof generation for testing. The checker verifies that the binary exists and is executable. The binary may be in the system PATH or in a project-local directory.

## Version Requirements

The version requirements table defines the minimum versions for all tools used by Midnight plugins. These requirements are updated when new features or fixes require newer versions.

Node.js must be version 18.0.0 or higher. This requirement is driven by the use of modern JavaScript features such as native fetch, structured clone, and the built-in test runner. Version 18 is the oldest LTS release still receiving security updates.

Docker must be version 24.0.0 or higher. This requirement ensures compatibility with the Midnight Docker Compose configuration which uses features introduced in Docker 24.

compactc must be the latest stable release. Because the compiler is tightly coupled to the network protocol version it is important to use the same version that the target network uses. The checker reports the installed version and the latest available version.

npm must be version 9.0.0 or higher. This requirement is driven by the use of workspace features and lockfile improvements introduced in npm 9.

## Plugin Scanning

Plugin scanning discovers which Midnight plugins are installed and what capabilities they provide. This enables dependency resolution, capability detection, and health checking across the plugin ecosystem.

### Discover Installed Plugins

The scanner searches for plugins in standard locations. It checks the current project node_modules directory first, then the global node_modules directory, and finally a configurable list of additional search paths. Each directory is inspected for the presence of a skill.json file which identifies it as a Midnight plugin.

```typescript
import { scanPlugins } from "midnight-plugin-utils";

const plugins = await scanPlugins({ searchPaths: ["./node_modules", globalModules] });
for (const plugin of plugins) {
  console.log(`${plugin.name} v${plugin.version} (${plugin.path})`);
}
```

### Detect Plugin Versions

Each plugin reports its version in its skill.json manifest. The scanner reads this version and compares it against known version ranges. Version mismatches between plugins that depend on each other are reported as warnings. The scanner can also check for updates by comparing installed versions against a registry.

### Identify Plugin Capabilities

Plugins declare their capabilities in the skill.json manifest under the `capabilities` field. Capabilities describe what the plugin can do such as "contract-compilation", "network-deployment", or "state-verification". The scanner aggregates capabilities across all installed plugins and provides a query interface for finding plugins that support specific capabilities.

### Plugin Registry

The plugin registry maintains a catalog of known Midnight plugins with their names, versions, capabilities, and dependencies. The registry is used by other plugins to discover what is available. Plugins register themselves when they are installed and deregister when they are removed. The registry supports queries by name, by capability, and by dependency graph.

## Root Resolution

Root resolution finds the root directory of a Midnight plugin or project. The root directory contains configuration files and serves as the base for relative path resolution.

### Find Plugin Root Directory

The root directory of a plugin is the directory that contains the skill.json file. The resolver starts from a given path and walks up the directory tree until it finds a skill.json file. If no skill.json is found the resolver reports that the path is not within a Midnight plugin.

```typescript
import { resolvePluginRoot } from "midnight-plugin-utils";

const root = await resolvePluginRoot("/path/to/some/file.ts");
// root is "/path/to" if that directory contains skill.json
```

### Resolve Relative Paths

Once the root is found relative paths can be resolved against it. The resolver normalizes paths, resolves parent directory references, and validates that the resolved path exists and is within the project tree. Relative paths are always resolved relative to the plugin root unless the user specifies an absolute path or a path relative to the current working directory.

### Locate Configuration Files

Configuration files follow a priority order. The resolver checks for project-local configuration first, then user-global configuration, then system-wide defaults. At each level it checks for common configuration file names and formats. The first configuration file found wins. If no configuration file exists the resolver returns the default settings.

### Workspace Detection

In monorepo setups the resolver detects that the project is part of a workspace managed by npm, yarn, or pnpm. Workspace detection is important for resolving inter-package dependencies and for locating the correct configuration scope. The resolver inspects workspace configuration files and reports the workspace root and member packages.

## Plugin Structure Validation

Structure validation ensures that plugins follow the expected conventions and contain all required files. Validation catches issues early before they cause problems at runtime.

### Verify SKILL.md Presence

Every Midnight plugin must have a SKILL.md file at its root. This file describes the plugin purpose, usage instructions, and configuration options. The validator checks that the file exists and is not empty. It does not validate the content quality but ensures the file is present and readable.

### Validate skill.json Format

The skill.json file is the plugin manifest. The validator checks that the file is valid JSON, that it contains all required fields (name, version, description), that the version field is valid semantic versioning, that the name field follows the naming convention, and that optional fields have the correct types if present.

```json
{
  "name": "midnight-example",
  "version": "1.0.0",
  "description": "An example Midnight plugin",
  "main": "src/index.ts",
  "capabilities": ["contract-compilation"],
  "dependencies": {
    "midnight-plugin-utils": "^1.0.0"
  }
}
```

### Check References Directory

Plugins may include a references directory containing supplementary documentation, example code, or test data. The validator checks that the directory exists if the skill.json references it. Files in the references directory should follow the naming conventions for their types.

### Verify Required Scripts

If the skill.json declares scripts the validator checks that each script exists at the specified path and is executable. Scripts are used for tasks such as installation, setup, and testing. Missing scripts are reported as errors. Non-executable scripts are reported as warnings.

## Cross-Plugin Compatibility

As the Midnight plugin ecosystem grows compatibility between plugins becomes important. Cross-plugin compatibility checks prevent version conflicts and dependency issues.

### Version Alignment

Plugins that depend on each other must agree on compatible versions. The compatibility checker resolves the dependency graph and identifies any version conflicts. For each conflict it reports which plugins require which versions and whether the requirements can be satisfied simultaneously.

### Shared Dependency Resolution

When multiple plugins depend on the same package they must resolve to compatible versions. The resolver uses the same algorithm as npm to find a version that satisfies all requirements. If no compatible version exists the resolver reports the conflict and suggests manual resolution steps.

### Conflict Detection

Conflicts can arise from version requirements, capability overlaps, or configuration differences. The conflict detector identifies both direct conflicts where requirements explicitly contradict and indirect conflicts where satisfying all requirements would produce an invalid state. Each conflict is reported with severity and suggested resolution.

## Configuration Management

Configuration management provides a unified system for plugin settings with support for project-local, user-global, and environment variable sources.

### Centralized Plugin Configuration

A centralized configuration file at the workspace root provides settings shared by all plugins. Individual plugins can override these settings in their own configuration. The configuration system merges settings from all sources with explicit priority rules.

```typescript
import { loadConfig } from "midnight-plugin-utils";

const config = await loadConfig({
  scope: "plugin",
  pluginName: "midnight-verify",
  defaults: {
    timeout: 30000,
    retries: 3
  }
});
```

### Per-Plugin Settings

Each plugin can define its own configuration schema with typed settings and default values. The configuration loader validates that provided settings match the schema and applies defaults for missing values. Per-plugin settings are stored alongside the plugin or in the central configuration file.

### Environment Variable Handling

Configuration can be provided through environment variables following the naming convention `MIDNIGHT_PLUGIN_SETTING`. Environment variables override all file-based settings. This is useful for CI environments where configuration must be injected at runtime. The loader validates that environment variable values match the expected types.

### Config File Discovery

Configuration files are discovered using the same priority system as root resolution. The loader checks the current project directory, then parent directories, then the user home directory, and finally system configuration directories. The first matching configuration file provides the base values which are then overridden by more specific sources.

## File System Utilities

File system utilities provide safe operations for reading, writing, and managing files within the plugin workspace.

### Safe File Operations

All file operations go through safety checks that prevent accidental damage. Write operations verify that the target path is within the allowed workspace. Delete operations require explicit confirmation for files outside the temp directory. Overwrite operations create backups of the original file.

### Temp Directory Management

Temporary directories are created for intermediate artifacts such as compilation outputs and test data. Temp directories are created in the system temp location with a unique name. They are automatically cleaned up when the operation completes or when the plugin shuts down. Manual cleanup is available for long-running operations.

```typescript
import { createTempDir, cleanupTempDir } from "midnight-plugin-utils";

const tempDir = await createTempDir({ prefix: "midnight-verify-" });
try {
  // Use temp directory for intermediate files
} finally {
  await cleanupTempDir(tempDir);
}
```

### Cache Management

Plugins can cache data to improve performance on repeated runs. The cache is stored in a well-known location with versioned entries. Cache entries have expiration times after which they are automatically refreshed. Cache corruption is detected and corrupted entries are discarded.

### Workspace Cleanup

After operations complete the workspace should be cleaned to remove temporary files and reduce disk usage. The cleanup utility removes temp directories, expired cache entries, and orphaned lock files. Cleanup is idempotent and safe to run at any time.

## Process Management

Process management utilities handle spawning and managing child processes for external tools.

### Spawning Child Processes

Child processes are spawned for tools such as compactc, Docker, and the proof server. The process manager handles argument construction, environment setup, stdout and stderr capture, and exit code handling. Timeouts can be configured to prevent hung processes from blocking the workflow.

```typescript
import { spawnTool } from "midnight-plugin-utils";

const result = await spawnTool("compactc", ["compile", "contract/src"], {
  timeout: 30000,
  env: { ...process.env, COMPACT_LOG_LEVEL: "info" }
});
```

### Managing Docker Containers

Docker containers are managed for the local Midnight network stack. The Docker manager handles container lifecycle from pull through start, health check, and stop. It monitors container health and restarts unhealthy containers. Cleanup on shutdown removes containers and networks.

### Process Lifecycle

Process lifecycle management ensures that all child processes are properly started, monitored, and terminated. A process registry tracks all running processes. When the parent plugin exits all registered processes are terminated gracefully with escalating force for unresponsive processes.

### Signal Handling

The process manager handles operating system signals such as SIGINT and SIGTERM. When a signal is received it is forwarded to all managed child processes. Processes are given time to shut down gracefully before being forcefully terminated. Signal handling ensures clean shutdown in all circumstances.

## Network Utilities

Network utilities verify connectivity to Midnight services and handle network configuration.

### Port Checking

Port availability is checked before starting services. The port checker determines whether a port is in use by attempting to bind to it. If the port is available the checker returns the port number. If not it suggests alternative ports.

```typescript
import { checkPort } from "midnight-plugin-utils";

const available = await checkPort(3000);
if (available) {
  console.log("Port 3000 is available");
} else {
  console.log("Port 3000 is in use, try port 3001");
}
```

### Endpoint Verification

HTTP endpoints can be verified to confirm that services are running. The endpoint verifier sends a GET request to the health check endpoint and validates the response. Timeout and retry settings control how long the verifier waits and how many times it retries.

### Connectivity Testing

Network connectivity to Midnight nodes and services is tested with TCP connection attempts. The tester verifies that hosts are reachable, that TLS certificates are valid, and that response times are within acceptable limits. Results are reported with latency measurements.

### Proxy Support

Network operations can be routed through HTTP and SOCKS proxies. The proxy configuration is read from environment variables (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`) and applied to all network requests. Custom proxy configurations can also be provided programmatically.

## Logging Infrastructure

Logging infrastructure provides structured logging across all Midnight plugins with consistent formats and configurable verbosity.

### Structured Logging

Log messages are written in structured JSON format that can be parsed and analyzed by log aggregation tools. Each log entry includes a timestamp, severity level, plugin name, message, and optional context data. Structured logging enables searching and filtering logs across multiple plugins.

```typescript
import { createLogger } from "midnight-plugin-utils";

const logger = createLogger({ plugin: "midnight-verify", level: "info" });
logger.info("Starting verification", { contract: "Counter", method: "compile" });
```

### Log Levels

Four log levels are available. `debug` provides detailed information for troubleshooting and is typically disabled in production. `info` provides general operational information about plugin activity. `warn` indicates potential issues that should be investigated. `error` indicates failures that prevented an operation from completing.

### Log Rotation

Log files are rotated when they reach a configurable size limit. Old logs are compressed and archived. Rotation prevents log files from consuming excessive disk space while preserving historical logs for debugging.

### Log Aggregation

Logs from multiple plugins can be aggregated into a unified log stream. The aggregator collects logs from all active plugins and writes them to a shared output. Aggregation provides a complete picture of system activity across all plugin operations.

## Error Utilities

Error utilities provide consistent error formatting, classification, and reporting across all plugins.

### Error Formatting

Errors are formatted with consistent structure including the error type, message, and optional cause chain. Formatted errors are readable in both terminal output and log files. The formatter handles both built-in Error objects and custom error types.

```typescript
import { formatError } from "midnight-plugin-utils";

try {
  await riskyOperation();
} catch (err) {
  console.error(formatError(err));
}
```

### Error Chaining

When errors propagate through multiple layers each layer can add context to the error chain. The error chain preserves the complete causal history of the error. When displayed the chain shows the most recent error first with earlier causes indented below.

### Error Classification

Errors are classified into categories for consistent handling. Categories include `NETWORK` for connectivity errors, `CONFIGURATION` for setup errors, `USER_INPUT` for invalid user input, `COMPILATION` for build errors, `RUNTIME` for execution errors, and `INTERNAL` for unexpected internal errors. Classification determines the error severity and suggested response.

### Error Reporting

Errors can be reported with structured data suitable for filing bug reports. The report includes the error details, environment information, relevant configuration, and steps to reproduce. Error reports can be written to files for attachment to issues.

## Testing Utilities

Testing utilities provide helpers, mocks, and fixtures for writing tests for Midnight plugins.

### Plugin Test Helpers

Test helpers provide convenience functions for common test scenarios. Helpers include functions for creating temporary workspaces, setting up test contracts, deploying to test networks, and verifying test results.

```typescript
import { createTestWorkspace, deployTestContract } from "midnight-plugin-utils/test";

const workspace = await createTestWorkspace();
const contract = await deployTestContract(workspace, "Counter");
const result = await contract.callCircuit("increment", { amount: 1 });
expect(result.output).toBe(1);
```

### Mock Factories

Mock factories create mock objects for external dependencies. Mocks for the wallet SDK, proof server, indexer, and network provider simulate real behavior without requiring actual services. Mocks can be configured with specific responses and verification assertions.

### Test Fixtures

Test fixtures provide pre-built data for testing. Fixtures include contract sources, compiled contracts, transaction data, and state snapshots. Fixtures are versioned alongside the code that uses them.

### Assertion Helpers

Assertion helpers extend the standard test assertions with Midnight-specific checks. Helpers include assertions for verifying contract state, transaction results, proof validity, and error types.

## Plugin Development Kit

The Plugin Development Kit provides tools for creating new Midnight plugins.

### Scaffolding for New Plugins

A scaffolding tool generates the initial structure for a new plugin. It creates the directory layout, the skill.json manifest, the SKILL.md documentation template, and configuration files. The scaffolded plugin is ready for development with all required files in place.

```bash
npx midnight-plugin-utils scaffold my-new-plugin
```

### Boilerplate Generation

Boilerplate code is generated for common plugin patterns. Templates provide implementations for health check commands, dependency validation, configuration loading, and error handling. Boilerplate ensures that new plugins follow conventions from the start.

### Validation Scripts

Validation scripts check that a plugin meets all requirements before release. The scripts verify structure, validate configuration, run tests, and check documentation completeness. Validation must pass before a plugin can be published.

### Packaging Scripts

Packaging scripts prepare a plugin for distribution. They bundle the plugin code, include required assets, stamp the version, and create a distributable archive. The packaging process is automated and reproducible.

## Build System Integration

Build system integration connects plugin development into the broader project build pipeline.

### Plugin Bundling

Plugins are bundled into distributable packages that include all required code and assets. Bundling resolves dependencies, strips development-only code, and optimizes for production use. The bundled output is a single directory that can be installed as a package.

### Dependency Resolution

The build system resolves all plugin dependencies to specific versions and bundles them with the plugin or declares them as externally provided. Resolution ensures that the plugin will work correctly in any environment that satisfies the declared dependency constraints.

### Version Stamping

Build artifacts are stamped with the plugin version, build timestamp, and git commit hash. Version stamping enables traceability from production behavior back to the exact source that produced the plugin.

### Release Preparation

Release preparation runs the complete validation suite, generates changelog entries, updates version numbers, and creates release artifacts. The preparation process ensures that releases are consistent and complete.

## Best Practices

### Minimal Dependencies

Plugins should minimize their external dependencies. Each dependency adds maintenance burden and potential for conflicts. Utilities from this package should be preferred over external alternatives. Dependencies should be pinned to exact versions.

### Self-Contained Plugins

Each plugin should be self-contained with clear boundaries. Inter-plugin dependencies should be declared explicitly. Shared functionality should go in this plugin-utils package rather than creating coupling between plugins.

### Clear Error Messages

Error messages should clearly state what went wrong and what the user should do about it. Messages should avoid jargon and internal implementation details. Each error should provide context sufficient for the user to understand and resolve the issue.

### Comprehensive Validation

Plugins should validate their environment before performing any operation. Validation includes dependency checks, configuration validation, and connectivity testing. Early validation prevents cryptic failures later in the workflow.

## Integration with midnight-expert

The midnight-expert plugin is the primary consumer of plugin utilities. It integrates plugin utilities into a comprehensive development workflow.

### Health Check Integration

midnight-expert runs health checks that verify the entire development environment. These checks use dependency checking from plugin-utils to verify tool availability. Results are incorporated into the health report that guides the developer toward a working environment.

### Dependency Validation Integration

When midnight-expert diagnoses issues it uses dependency validation from plugin-utils to check that all prerequisites are met. Missing or outdated dependencies are reported with installation instructions. Version mismatches are flagged for resolution.

### Plugin Registry Integration

midnight-expert uses the plugin registry from plugin-utils to discover what capabilities are available. The registry informs the expert about which operations can be performed and which plugins need to be installed. The expert can suggest plugin installations to fill capability gaps.

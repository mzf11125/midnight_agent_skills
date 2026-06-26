# Midnight Plugin Utilities

Reference for shared infrastructure utilities used across all Midnight plugins.

## Overview

Plugin utilities provide shared infrastructure that all Midnight agent skills depend on. This includes dependency checking, plugin discovery, configuration management, file system operations, process management, and network utilities.

## Dependency Checking

Verify that all required development tools are installed and at compatible versions:

**Required Tools:**
- Node.js version 18.0.0 or higher
- Docker version 24.0.0 or higher (for local devnet)
- compactc (Compact compiler, latest stable)
- npm version 9.0.0 or higher

**Optional Tools:**
- Bun package manager (alternative to npm)
- wallet CLI (for wallet operations via MCP)
- Docker Compose (for managing multi container devnet)

**Check Patterns:**
```bash
node --version
docker --version
compactc --version
npm --version
```

## Plugin Scanning

Discover installed Midnight plugins by scanning the skills directory:

**Scanning patterns:**
- Look for directories containing both SKILL.md and skill.json
- Validate skill.json has required fields (name, description, tags)
- Check for references/ directory presence
- Verify scripts/ are executable where applicable
- Build plugin registry from discovered plugins

## Root Resolution

Resolve the plugin root directory for path operations:

- Detect workspace root from package.json presence
- Resolve relative paths to absolute paths
- Locate configuration files (skillsrc.json, .claude/settings.local.json)
- Support monorepo and nested workspace structures

## Configuration Management

Centralized configuration handling:

- Read per plugin configuration from skill.json
- Merge environment variables with defaults
- Discover configuration files across the workspace
- Provide consistent configuration access patterns

## File System Utilities

Safe file operations for plugin interactions:

- Atomic file writes to prevent corruption
- Temporary directory management with cleanup
- Cache directory management for performance
- Workspace cleanup operations

## Process Management

Spawning and managing child processes:

- Execute compactc compiler with proper flags
- Manage Docker container lifecycle (start, stop, health check)
- Process signal handling and graceful shutdown
- Timeout management for long running operations

## Network Utilities

Common network operations:

- Port availability checking for local devnet
- Endpoint verification (HTTP and WebSocket)
- Connectivity testing to Midnight network endpoints
- Proxy support for enterprise environments

## Plugin Development Kit

Tools for creating new Midnight plugins:

- Scaffolding templates for new skill directories
- Boilerplate generation for SKILL.md and skill.json
- Validation scripts to verify plugin structure
- Packaging scripts for distribution

## Integration with midnight-expert

These utilities integrate with the midnight-expert meta skill by providing:
- Dependency validation for the health check system
- Plugin scanning for the plugin registry
- Configuration validation for ecosystem diagnostics
- Root resolution for cross plugin path operations

## Resources

- midnight-expert skill for ecosystem diagnostics
- STRUCTURE.md for plugin organization rules
- package.json for dependency requirements

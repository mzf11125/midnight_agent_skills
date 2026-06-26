# Midnight Fact Check Pipeline

Reference for the fact checking pipeline that validates Midnight documentation accuracy.

## Overview

The fact check pipeline systematically verifies claims found in Midnight documentation, GitHub repositories, and community sources. It extracts verifiable assertions, classifies them by domain, validates against authoritative sources, and generates reports.

## Claim Extraction

Claims are extracted from documentation sources by identifying verifiable statements such as API signatures, version numbers, error codes, configuration defaults, network endpoints, and behavior descriptions.

**Extractable claim types:**
- Function signatures and parameter types
- Return type assertions and version specific behavior
- API endpoint URLs and network addresses
- Error code numbers and descriptions
- Version numbers for packages and tools
- Configuration default values
- Gas cost estimates and pricing models
- Behavior guarantees and invariants

## Domain Classification

Each claim is classified into one of these domains for targeted verification:

**Compact Language**: Claims about syntax, types, compiler behavior, standard library functions
**API Reference**: Claims about SDK methods, parameters, return types, error codes
**Network Infrastructure**: Claims about endpoints, nodes, consensus, network parameters
**Concepts**: Claims about architecture, protocols, tokenomics, privacy mechanisms
**SDK Behavior**: Claims about runtime behavior, transaction processing, state management

## Verification Methods

**Source Cross Referencing**: Compare claims against official source code on GitHub
**API Testing**: Execute API calls to verify behavior matches documentation
**Compile Verification**: Run compactc to verify compiler behavior claims
**Runtime Verification**: Execute contracts on devnet to verify runtime claims
**Version Checking**: Verify version numbers against npm registry and release tags
**Endpoint Probing**: Test network endpoint URLs for reachability

## Multi Source Validation

Claims are validated against multiple sources in a defined hierarchy:

1. Official source code (GitHub) is the most authoritative
2. npm package metadata and type definitions
3. Official documentation on docs.midnight.network
4. Community consensus from midnight awesome dapps

## Report Generation

Verification reports include:
- Claim text and source location
- Verification method used
- Confidence level (high, medium, low)
- Evidence and source attribution
- Resolution recommendation for unverified claims

## Integration with CI

The fact check pipeline can be integrated into CI workflows to:
- Flag claims about deprecated APIs
- Detect version number mismatches between docs and packages
- Identify broken documentation links
- Track documentation drift over time

## Resources

- midnight-expert skill for ecosystem health checks
- midnight-verify skill for runtime verification
- Official Midnight docs at docs.midnight.network
- Midnight GitHub organization at github.com/midnightntwrk

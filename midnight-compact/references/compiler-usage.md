# compactc Compiler CLI

The compactc compiler transforms Compact source files into ZKIR artifacts for the Midnight proof server.

## Command Syntax

```
compactc [options] <input.compact>
```

Basic compilation of a single source file.

```
compactc --out-dir <path> [options] <input1.compact> <input2.compact>
```

Compilation of multiple source files sharing a common output directory.

## Flags and Options

### Output Control

`--out-dir <path>` specifies the directory for generated artifacts. Defaults to the current working directory.

`--out-base <path>` sets the base path for resolving relative output paths. Useful for monorepo projects where source files live in varied subdirectories.

`--name <string>` overrides the contract name used in generated artifact filenames. Defaults to the source filename without extension.

### Compilation Targets

`--zkir` generates only the ZKIR intermediate representation. This is the default target and produces the file `contract_name.zkir`.

`--prover-key` generates the prover key required for constructing proofs. Produces `contract_name.pk`. Depends on the ZKIR being generated first.

`--verifier-key` generates the verifier key for proof validation. Produces `contract_name.vk`. Also depends on ZKIR generation.

`--all` generates ZKIR, prover key, and verifier key in a single invocation.

### Circuit Configuration

`--witness-count <n>` sets the expected number of witnesses per circuit. The compiler uses this for circuit size estimation and allocation.

`--max-constraints <n>` sets an upper bound on circuit constraints. Compilation fails if this bound is exceeded. Useful for CI pipelines that enforce circuit budget limits.

### Debugging and Diagnostics

`--verbose` enables detailed compilation progress output including per-circuit timing and memory statistics.

`--dump-ast` writes the parsed abstract syntax tree to stdout for debugging grammar and parsing issues.

`--dump-ir` writes the intermediate representation before ZKIR lowering for inspecting the compiler pipeline.

`--error-format <json|text>` controls how compilation errors are formatted. JSON output is machine readable and integrates with editor tooling.

### Optimization

`--opt-level <0|1|2|3>` controls the optimization aggressiveness. Level 0 disables optimizations for fast debug cycles. Level 1 enables basic peephole optimizations. Level 2 adds circuit level optimizations including constraint reduction. Level 3 enables aggressive optimizations that may increase compile time.

## Input Formats

The compiler accepts `.compact` source files as its primary input. Source files use UTF-8 encoding. The compiler resolves `import` statements relative to the source file location and against any paths specified via `--include-path <path>` which may be repeated.

Import resolution order is as follows. First check relative to the importing file. Then check each include path in the order specified. Finally check the standard library path.

## Output Formats

### ZKIR

The Zero Knowledge Intermediate Representation is a JSON formatted file describing the arithmetic circuit, constraint system, discrete variables, ledger operations, and disclosure configuration. This is the primary artifact consumed by the proof server.

### Prover Key

The prover key is a binary file encoding the proving parameters for each circuit in the contract. Prover keys may be large for complex circuits. Store them alongside the proof server configuration.

### Verifier Key

The verifier key is a compact binary file used by the blockchain validators to check submitted proofs. Verifier keys are published on chain during contract deployment.

## Circuit Size Estimation

The compiler reports estimated constraint counts per circuit after compilation. The `--max-constraints` flag provides a hard limit. For capacity planning multiply the constraint count by the witness count to estimate total circuit variables.

## Error Output Interpretation

Errors follow a familiar format of `file:line:column: severity: message`. The severity is one of `error`, `warning`, or `note`. Parse errors indicate syntax issues in the source. Type errors indicate witness or variable type mismatches. Disclosure errors indicate fields that cannot be disclosed due to privacy constraints. ZKIR errors indicate the compiled circuit cannot be expressed in the target constraint system.

Each error includes a primary message and may include additional context lines showing the relevant source range with carets pointing to the problematic tokens.

## Integration with Build Scripts

Use `compactc --error-format json` for machine parseable output in build scripts. Exit code 0 indicates success. Exit code 1 indicates a compilation error. Exit code 2 indicates an internal compiler error.

For npm based projects add a compile script to package.json.

```
"scripts": {
  "compile": "compactc --out-dir dist/zkir src/*.compact"
}
```

For Makefile based projects use a pattern rule.

```
dist/zkir/%.zkir: src/%.compact
\tcompactc --out-dir dist/zkir $<
```

For CI pipelines always use `--max-constraints` to enforce circuit budgets and `--error-format json` for structured log output.

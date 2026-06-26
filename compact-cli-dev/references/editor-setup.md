# Editor Setup for Compact Development

Configuration guides for VS Code and Neovim to support Compact language editing with syntax highlighting, error reporting, and compilation integration.

## VS Code Extension

### Installation

Search for the Compact extension in the VS Code marketplace. The extension ID is `midnight.compact-vscode`. Click Install and reload the editor window. Alternatively install from the command line.

```
code --install-extension midnight.compact-vscode
```

### Syntax Highlighting

The extension provides automatic syntax highlighting for `.compact` files. Keywords such as `circuit`, `witness`, `ledger`, `disclose`, `import`, `struct`, and `enum` are colorized distinctly. Type annotations appear in a separate color. Comments use a muted foreground.

The extension reads the TextMate grammar bundled in `syntaxes/compact.tmLanguage.json`. Custom themes may override the default scopes but the grammar recognizes the standard token types.

### Error Reporting

Compilation diagnostics appear inline in the editor. Errors are underlined in red. Warnings appear as yellow squiggles. The Problems panel lists all diagnostics across open files with clickable links to the source locations.

The extension invokes `compactc --error-format json` on save to produce diagnostics. It uses the current workspace root as the include path. Multi-root workspaces are supported with per-root compiler settings.

### Compilation on Save

Enable compilation on save in the extension settings by checking the `compact.compileOnSave` option. The extension runs `compactc` with the file path and configured output directory. Generated artifacts appear in the configured `compact.outputDir` directory. The default output directory is `out/zkir` relative to the workspace root.

### Keyboard Shortcuts

`Ctrl+Shift+B` (or `Cmd+Shift+B` on macOS) triggers the build task. The extension registers a default build task that runs `compactc --out-dir out/zkir` on all `.compact` files in the workspace.

`Ctrl+Shift+P` and type `Compact` to see available commands. `Compact: Compile Current File` compiles the active editor file. `Compact: Compile All` compiles all compact files in the workspace. `Compact: Show Circuit Stats` displays constraint counts and circuit size estimates for the current file.

### Settings

Key settings with their defaults:

```
"compact.compileOnSave": true
"compact.outputDir": "out/zkir"
"compact.includePaths": []
"compact.compilerPath": "compactc"
"compact.optLevel": 0
"compact.errorFormat": "json"
"compact.maxConstraints": 0
```

Set `compact.maxConstraints` to a positive integer to enforce circuit size limits during development. Set `compact.compilerPath` to a custom path if compactc is not on the system PATH.

## Neovim Setup

### Plugin Installation

The `compact.vim` plugin provides Compact language support for Neovim. Install using your preferred plugin manager.

Using lazy.nvim:

```lua
{
  "midnight/compact.vim",
  ft = { "compact" },
  config = function()
    -- configuration here
  end
}
```

Using packer.nvim:

```lua
use {
  "midnight/compact.vim",
  ft = { "compact" }
}
```

### LSP Configuration

The compact LSP server ships with the compiler. Configure it in your Neovim LSP setup.

```lua
local lspconfig = require("lspconfig")
lspconfig.compact_ls.setup({
  cmd = { "compactc", "lsp" },
  filetypes = { "compact" },
  root_dir = lspconfig.util.root_pattern(".git"),
  settings = {
    compact = {
      includePaths = {},
      optLevel = 0,
      maxConstraints = 0
    }
  }
})
```

The LSP provides hover type information, go to definition, find references, rename, and code actions for common fixes. Diagnostic messages appear as virtual text and in the diagnostic float window.

### Formatting on Save

Enable formatting on save with an autocommand.

```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.compact",
  callback = function()
    vim.lsp.buf.format({ async = false })
  end
})
```

The LSP format provider runs the compact formatter which normalizes indentation, spacing around operators, and import ordering to match the canonical Compact style.

### Syntax Highlighting

The plugin provides Treesitter based syntax highlighting. Install the Treesitter grammar.

```lua
require("nvim-treesitter.configs").setup({
  ensure_installed = { "compact" }
})
```

Tree-sitter based highlighting is more precise than regex based highlighting, correctly handling nested expressions, multi-line comments, and edge cases.

## Troubleshooting Common Issues

### VS Code Issues

If syntax highlighting is not working check that the file extension is `.compact` and that the extension is enabled. Open the Command Palette and run `Developer: Reload Window` to force a full reload.

If diagnostics are not appearing check that `compactc` is on the system PATH or set `compact.compilerPath` to the full compiler binary path. Verify the compiler works by running `compactc --version` in a terminal.

If compilation on save uses an old compiler version update the system PATH to point to the newer binary first or set `compact.compilerPath` explicitly.

### Neovim Issues

If the LSP fails to start verify the command `compactc lsp` runs successfully in a terminal. Check that the LSP configuration loads by running `:LspInfo` and confirming compact_ls appears in the configured servers list.

If Treesitter highlighting is not active run `:TSInstall compact` and restart Neovim. Verify the Treesitter parser installed correctly with `:TSModuleInfo compact`.

If formatting on save produces unexpected changes adjust the formatter settings. The compact formatter respects a `.compactfmt` configuration file in the project root for custom indentation width and line length preferences.

### General Issues

If compile errors reference missing imports add the include paths to the editor settings. For VS Code set `compact.includePaths`. For Neovim set `settings.compact.includePaths` in the LSP configuration.

If compilation is slow during development set `optLevel` to 0 in editor settings. Use higher optimization levels only for final builds or CI pipelines.

If the editor freezes during compilation of large contracts increase the compiler timeout setting. For VS Code set `compact.compilerTimeout` to a larger value in milliseconds. For Neovim the LSP timeout defaults to 60 seconds and can be adjusted with `vim.lsp.set_log_level("debug")` to diagnose slow operations.

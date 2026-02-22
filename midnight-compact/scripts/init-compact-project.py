#!/usr/bin/env python3
"""Initialize a new Compact project with proper structure"""
import os
import sys
from pathlib import Path

def create_project(project_name, output_dir="."):
    project_path = Path(output_dir) / project_name
    
    if project_path.exists():
        print(f"❌ Project '{project_name}' already exists")
        return False
    
    # Create directory structure
    dirs = [
        project_path,
        project_path / "src",
        project_path / "tests",
        project_path / "scripts"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create main contract file
    main_contract = project_path / "src" / "main.compact"
    main_contract.write_text("""// Main contract
contract MyContract {
  state {
    // Contract state
  }
  
  init() {
    // Constructor
  }
  
  pub fn publicFunction() {
    // Public function
  }
  
  circuit privateFunction(private data: Field) {
    // Private circuit
  }
}
""")
    
    # Create package config
    config = project_path / "compact.toml"
    config.write_text(f"""[package]
name = "{project_name}"
version = "0.1.0"

[dependencies]
std = "*"
""")
    
    # Create README
    readme = project_path / "README.md"
    readme.write_text(f"""# {project_name}

Midnight Compact smart contract project.

## Build
```bash
compact build
```

## Test
```bash
compact test
```

## Deploy
```bash
compact deploy --network testnet
```
""")
    
    print(f"✅ Created Compact project: {project_path}")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  # Edit src/main.compact")
    print(f"  compact build")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init-compact-project.py <project-name> [output-dir]")
        sys.exit(1)
    
    project_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    create_project(project_name, output_dir)

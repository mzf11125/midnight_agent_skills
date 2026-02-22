#!/usr/bin/env python3
"""Initialize a new Midnight DApp project"""
import os
import sys
from pathlib import Path

def create_dapp(project_name, output_dir="."):
    project_path = Path(output_dir) / project_name
    
    if project_path.exists():
        print(f"❌ Project '{project_name}' already exists")
        return False
    
    # Create structure
    (project_path / "src").mkdir(parents=True)
    (project_path / "public").mkdir(parents=True)
    
    # package.json
    (project_path / "package.json").write_text(f'''{{
  "name": "{project_name}",
  "version": "0.1.0",
  "dependencies": {{
    "@midnight-ntwrk/midnight-js": "latest",
    "@midnight-ntwrk/dapp-connector-api": "latest",
    "@midnight-ntwrk/compact-runtime": "latest"
  }}
}}
''')
    
    # index.html
    (project_path / "public" / "index.html").write_text('''<!DOCTYPE html>
<html>
<head>
  <title>Midnight DApp</title>
</head>
<body>
  <div id="app"></div>
  <script src="../src/index.js" type="module"></script>
</body>
</html>
''')
    
    # index.js
    (project_path / "src" / "index.js").write_text('''import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

async function connectWallet() {
  const networkId = NetworkId('preprod');
  const api = await window.midnight.someWallet.connect(networkId);
  console.log('Connected to wallet');
  return api;
}

connectWallet();
''')
    
    print(f"✅ Created DApp project: {project_path}")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  npm install")
    print(f"  npm start")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init-dapp-project.py <project-name> [output-dir]")
        sys.exit(1)
    
    create_dapp(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")

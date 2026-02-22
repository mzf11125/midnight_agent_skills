#!/usr/bin/env python3
"""Compile Compact contracts with error handling"""
import subprocess
import sys
from pathlib import Path

def compile_contract(contract_file):
    if not Path(contract_file).exists():
        print(f"❌ File not found: {contract_file}")
        return False
    
    print(f"🔨 Compiling {contract_file}...")
    
    try:
        result = subprocess.run(
            ["compact", "build", contract_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Compilation successful")
            print(result.stdout)
            return True
        else:
            print("❌ Compilation failed")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Compact compiler not found. Please install Midnight toolchain.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compile-compact.py <contract-file>")
        sys.exit(1)
    
    compile_contract(sys.argv[1])

#!/usr/bin/env python3
"""Deploy Compact contract to Midnight network"""
import subprocess
import sys
from pathlib import Path

def deploy_contract(contract_file, network="testnet"):
    if not Path(contract_file).exists():
        print(f"❌ Contract file not found: {contract_file}")
        return False
    
    print(f"🚀 Deploying {contract_file} to {network}...")
    
    try:
        result = subprocess.run(
            ["midnight-cli", "deploy", contract_file, "--network", network],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Deployment successful")
            print(result.stdout)
            return True
        else:
            print("❌ Deployment failed")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ midnight-cli not found. Please install Midnight toolchain.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy-contract.py <contract-file> [network]")
        sys.exit(1)
    
    contract = sys.argv[1]
    network = sys.argv[2] if len(sys.argv) > 2 else "testnet"
    deploy_contract(contract, network)

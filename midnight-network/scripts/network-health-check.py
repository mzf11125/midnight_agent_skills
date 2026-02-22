#!/usr/bin/env python3
"""Check Midnight network health"""
import requests
import sys

ENDPOINTS = {
    "testnet": {
        "rpc": "https://rpc.testnet.midnight.network",
        "indexer": "https://indexer.testnet.midnight.network/graphql"
    }
}

def check_health(network="testnet"):
    if network not in ENDPOINTS:
        print(f"❌ Unknown network: {network}")
        return False
    
    endpoints = ENDPOINTS[network]
    print(f"🔍 Checking {network} network health...\n")
    
    # Check RPC
    try:
        response = requests.post(
            f"{endpoints['rpc']}/health",
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Node RPC: Healthy")
        else:
            print(f"⚠️  Node RPC: Unhealthy ({response.status_code})")
    except Exception as e:
        print(f"❌ Node RPC: Unreachable ({e})")
    
    # Check Indexer
    try:
        response = requests.post(
            endpoints['indexer'],
            json={"query": "{ latestBlock { number } }"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            block = data.get('data', {}).get('latestBlock', {}).get('number', 'unknown')
            print(f"✅ Indexer: Healthy (block {block})")
        else:
            print(f"⚠️  Indexer: Unhealthy ({response.status_code})")
    except Exception as e:
        print(f"❌ Indexer: Unreachable ({e})")
    
    print("\n✅ Health check complete")
    return True

if __name__ == "__main__":
    network = sys.argv[1] if len(sys.argv) > 1 else "testnet"
    check_health(network)

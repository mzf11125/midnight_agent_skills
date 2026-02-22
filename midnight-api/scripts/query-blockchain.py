#!/usr/bin/env python3
"""Query blockchain data via indexer"""
import requests
import sys

INDEXER_URL = "https://indexer.testnet.midnight.network/graphql"

QUERIES = {
    "latest-block": '''
        query { latestBlock { number timestamp } }
    ''',
    "transaction": '''
        query($hash: String!) { transaction(hash: $hash) { hash status } }
    '''
}

def query_blockchain(query_type, params=None):
    if query_type not in QUERIES:
        print(f"❌ Unknown query: {query_type}")
        print(f"Available: {', '.join(QUERIES.keys())}")
        return
    
    query = QUERIES[query_type]
    variables = params or {}
    
    response = requests.post(INDEXER_URL, json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        print("✅ Query successful")
        print(response.json())
    else:
        print(f"❌ Query failed: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query-blockchain.py <query-type> [params]")
        print(f"Queries: {', '.join(QUERIES.keys())}")
        sys.exit(1)
    
    query_blockchain(sys.argv[1])

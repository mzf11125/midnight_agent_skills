#!/usr/bin/env python3
"""Generate API client boilerplate"""
import sys
from pathlib import Path

TEMPLATES = {
    "wallet-connector": '''import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

export async function connectWallet(networkId = 'preprod') {
  const api = await window.midnight.someWallet.connect(NetworkId(networkId));
  return api;
}

export async function getBalances(api) {
  return {
    shielded: await api.getShieldedBalances(),
    unshielded: await api.getUnshieldedBalances(),
    dust: await api.getDustBalance()
  };
}
''',
    "transaction-handler": '''import { nativeToken } from '@midnight-ntwrk/ledger';

export async function sendPayment(api, recipient, amount) {
  const tx = await api.makeTransfer([{
    kind: 'unshielded',
    tokenType: nativeToken().raw,
    value: amount,
    recipient
  }]);
  return await api.submitTransaction(tx);
}
'''
}

def generate_client(template_name, output_file):
    if template_name not in TEMPLATES:
        print(f"❌ Unknown template: {template_name}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        return False
    
    Path(output_file).write_text(TEMPLATES[template_name])
    print(f"✅ Generated {template_name}: {output_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate-api-client.py <template> <output-file>")
        print(f"Templates: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    
    generate_client(sys.argv[1], sys.argv[2])

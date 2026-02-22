#!/usr/bin/env python3
"""Test wallet connection"""
import sys

def test_connection():
    print("🔍 Testing wallet connection...")
    print("""
To test wallet connection:

1. Open browser console
2. Run: window.midnight
3. Check available wallets
4. Run: await window.midnight.someWallet.connect('preprod')
5. Verify connection successful

Expected output:
- Wallet API object with methods
- getConfiguration(), getBalances(), etc.
    """)

if __name__ == "__main__":
    test_connection()

#!/usr/bin/env python3
"""Monitor validator performance"""
import sys
import time

def monitor_validator():
    print("📊 Monitoring validator performance...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Simulate metrics
            print(f"[{time.strftime('%H:%M:%S')}] Blocks: 123456 | Peers: 25 | Stake: 1000000 | Status: Active")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")

if __name__ == "__main__":
    monitor_validator()

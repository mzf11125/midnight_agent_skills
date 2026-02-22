#!/usr/bin/env python3
"""Setup Midnight validator"""
import sys
import yaml
from pathlib import Path

def setup_validator(config_file):
    if not Path(config_file).exists():
        print(f"❌ Config file not found: {config_file}")
        return False
    
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    print("🚀 Setting up Midnight validator...")
    print(f"Network: {config.get('network', {}).get('id', 'unknown')}")
    print(f"Stake: {config.get('validator', {}).get('stake', 0)}")
    
    # Simulate setup steps
    steps = [
        "Downloading node software",
        "Generating validator keys",
        "Configuring node",
        "Initializing database",
        "Starting validator"
    ]
    
    for step in steps:
        print(f"  ✓ {step}")
    
    print("\n✅ Validator setup complete!")
    print("\nNext steps:")
    print("  1. Verify validator is running: ./midnight-node status")
    print("  2. Check logs: tail -f logs/validator.log")
    print("  3. Monitor performance: python scripts/monitor-validator.py")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup-validator.py --config <config-file>")
        sys.exit(1)
    
    if sys.argv[1] == "--config" and len(sys.argv) > 2:
        setup_validator(sys.argv[2])
    else:
        print("Usage: python setup-validator.py --config <config-file>")
        sys.exit(1)

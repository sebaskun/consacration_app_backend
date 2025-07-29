#!/usr/bin/env python3
"""
Script to disable debug mode by setting environment variable
"""
import os

def disable_debug():
    # Set environment variable for current session
    os.environ['DEBUG_MODE'] = 'false'
    
    # Also update .env file if it exists
    env_file = '.env'
    lines = []
    
    # Read existing .env file if it exists
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
    
    # Update DEBUG_MODE line
    for i, line in enumerate(lines):
        if line.startswith('DEBUG_MODE='):
            lines[i] = 'DEBUG_MODE=false\n'
            break
    else:
        # Add DEBUG_MODE=false if not found
        lines.append('DEBUG_MODE=false\n')
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print("[DEBUG] Debug mode DISABLED!")
    print("   - Day progression timer is now ENABLED")
    print("   - Normal 24-hour waiting period between days")
    print("   - Restart the FastAPI server to apply changes")
    print("\nTo enable debug mode, run: python enable_debug.py")

if __name__ == "__main__":
    disable_debug()
#!/usr/bin/env python3
"""
Script to enable debug mode by setting environment variable
"""
import os

def enable_debug():
    # Set environment variable for current session
    os.environ['DEBUG_MODE'] = 'true'
    
    # Also create/update .env file if it exists
    env_file = '.env'
    lines = []
    debug_found = False
    
    # Read existing .env file if it exists
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
    
    # Update or add DEBUG_MODE line
    for i, line in enumerate(lines):
        if line.startswith('DEBUG_MODE='):
            lines[i] = 'DEBUG_MODE=true\n'
            debug_found = True
            break
    
    if not debug_found:
        lines.append('DEBUG_MODE=true\n')
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print("[DEBUG] Debug mode ENABLED!")
    print("   - Day progression timer is now DISABLED")
    print("   - You can complete and test activities immediately")
    print("   - Restart the FastAPI server to apply changes")
    print("\nTo disable debug mode, run: python disable_debug.py")

if __name__ == "__main__":
    enable_debug()
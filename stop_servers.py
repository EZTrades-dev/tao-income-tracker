#!/usr/bin/env python3
"""
Stop script for Tao Income Tracking Application servers
"""

import subprocess
import sys

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        result = subprocess.run(['lsof', '-ti', str(port)], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(['kill', '-9', pid])
                    print(f"✅ Killed process {pid} on port {port}")
        else:
            print(f"ℹ️  No process found on port {port}")
    except Exception as e:
        print(f"⚠️  Warning: Could not kill process on port {port}: {e}")

def main():
    """Stop both servers"""
    print("🛑 Stopping Tao Income Tracking servers...")
    print("=" * 40)
    
    # Stop backend server (port 8000)
    print("📊 Stopping backend server (port 8000)...")
    kill_process_on_port(8000)
    
    # Stop frontend server (port 8080)
    print("🌐 Stopping frontend server (port 8080)...")
    kill_process_on_port(8080)
    
    print("=" * 40)
    print("✅ All servers stopped successfully!")
    print("💡 To restart, run: python3 start_servers.py")

if __name__ == "__main__":
    main()

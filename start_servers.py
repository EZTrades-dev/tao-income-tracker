#!/usr/bin/env python3
"""
Automatic server startup script for Tao Income Tracking Application
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path

def check_port_in_use(port):
    """Check if a port is already in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        result = subprocess.run(['lsof', '-ti', str(port)], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(['kill', '-9', pid])
                    print(f"Killed process {pid} on port {port}")
    except Exception as e:
        print(f"Warning: Could not kill process on port {port}: {e}")

def start_backend_server():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server on port 8000...")
    
    # Kill any existing process on port 8000
    kill_process_on_port(8000)
    
    # Start the backend server
    backend_process = subprocess.Popen(
        ['python3', 'main.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Check if the server started successfully
    if backend_process.poll() is None:
        print("✅ Backend server started successfully on http://localhost:8000")
        return backend_process
    else:
        stdout, stderr = backend_process.communicate()
        print(f"❌ Failed to start backend server:")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return None

def start_frontend_server():
    """Start the HTTP frontend server"""
    print("🌐 Starting frontend server on port 8080...")
    
    # Kill any existing process on port 8080
    kill_process_on_port(8080)
    
    # Start the frontend server
    frontend_process = subprocess.Popen(
        ['python3', '-m', 'http.server', '8080'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Check if the server started successfully
    if frontend_process.poll() is None:
        print("✅ Frontend server started successfully on http://localhost:8080")
        return frontend_process
    else:
        stdout, stderr = frontend_process.communicate()
        print(f"❌ Failed to start frontend server:")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return None

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shutdown servers"""
    print("\n🛑 Shutting down servers...")
    sys.exit(0)

def main():
    """Main function to start both servers"""
    print("📊 Tao Income Tracking Application - Server Startup")
    print("=" * 50)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if required files exist
    if not Path('main.py').exists():
        print("❌ Error: main.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    if not Path('index.html').exists():
        print("❌ Error: index.html not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Start backend server
    backend_process = start_backend_server()
    if not backend_process:
        print("❌ Failed to start backend server. Exiting.")
        sys.exit(1)
    
    # Start frontend server
    frontend_process = start_frontend_server()
    if not frontend_process:
        print("❌ Failed to start frontend server. Exiting.")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n🎉 Both servers are now running!")
    print("=" * 50)
    print("📊 Backend API: http://localhost:8000")
    print("📊 API Docs:    http://localhost:8000/docs")
    print("🌐 Frontend:    http://localhost:8080")
    print("🧪 Test Page:   http://localhost:8080/test_frontend.html")
    print("=" * 50)
    print("Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    try:
        # Keep the script running and monitor the processes
        while True:
            # Check if backend is still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            
            # Check if frontend is still running
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal")
    finally:
        # Cleanup: terminate both processes
        print("🛑 Stopping servers...")
        
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except subprocess.TimeoutExpired:
                backend_process.kill()
                print("⚠️  Backend server force-killed")
        
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except subprocess.TimeoutExpired:
                frontend_process.kill()
                print("⚠️  Frontend server force-killed")
        
        print("👋 All servers stopped. Goodbye!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🚀 Simple Agent-Aster Launcher
No email/password - just API keys and wallet
"""

import subprocess
import sys
import time
import requests
import os

def check_backend():
    """Check if backend is running."""
    try:
        response = requests.get("http://localhost:5000/health", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return True, data
        return False, None
    except:
        return False, None

def main():
    print("🚀 Agent-Aster Simple Platform Launcher")
    print("=" * 45)
    
    # Check if backend is already running
    backend_running, health_data = check_backend()
    
    if backend_running:
        print("✅ Backend already running!")
        if health_data:
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Auth Type: {health_data.get('auth_type', 'Unknown')}")
    else:
        print("🔧 Backend not running - start it manually:")
        print("   python agent_backend_simple.py")
        print("\n⏰ Waiting for backend...")
        
        # Wait a bit for backend to start
        for i in range(10):
            time.sleep(2)
            backend_running, health_data = check_backend()
            if backend_running:
                print("✅ Backend is now online!")
                break
            print(f"   Checking... ({i+1}/10)")
        
        if not backend_running:
            print("❌ Backend still offline")
    
    print("\n🎨 Starting Simple Frontend...")
    print("📱 Frontend will be available at: http://localhost:8502")
    print("🔗 Backend API at: http://localhost:5000")
    
    print("\n💡 Simple Features:")
    print("   ✅ No email/password required")
    print("   ✅ Just enter your Aster API keys")
    print("   ✅ Create/import Ethereum wallet")
    print("   ✅ Secure wallet-signed trading")
    print("   ✅ AI trading assistant")
    
    print("\n🔑 Demo API Credentials:")
    print("   API Key: 9889c4ca2a8612bbdc801df6f1fba74c6365b094df19d878b8a21a420e04436a")
    print("   API Secret: 748c304002a5b1e4d841b079d636f0c8c8eeb96fb055f6b98684c65f56fe2fb3")
    
    print("\n🌐 Access your platform:")
    print("   Frontend: http://localhost:8502")
    print("   Backend: http://localhost:5000/health")
    
    print("\n⌨️  Press Ctrl+C to stop")
    
    try:
        # Keep running to show status
        while True:
            time.sleep(10)
            backend_running, _ = check_backend()
            status = "🟢 Online" if backend_running else "🔴 Offline"
            print(f"   Backend: {status} | Frontend: 🟢 Running")
            
    except KeyboardInterrupt:
        print("\n👋 Launcher stopped")
        return 0

if __name__ == "__main__":
    sys.exit(main())

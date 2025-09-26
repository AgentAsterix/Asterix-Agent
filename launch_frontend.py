#!/usr/bin/env python3
"""Launch Agent-Aster Frontend"""

import subprocess
import sys
import time
import requests

def check_backend():
    """Check if backend is running."""
    try:
        response = requests.get("http://localhost:5000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("🎨 Agent-Aster Frontend Launcher")
    print("=" * 35)
    
    # Check if backend is running
    print("🔍 Checking backend status...")
    if check_backend():
        print("✅ Backend is online at http://localhost:5000")
    else:
        print("❌ Backend is offline!")
        print("💡 Start backend first: python agent_backend.py")
        print("⏰ Waiting 5 seconds for backend to start...")
        time.sleep(5)
        
        if check_backend():
            print("✅ Backend is now online!")
        else:
            print("⚠️  Backend still offline, but launching frontend anyway")
    
    print("\n🚀 Launching frontend...")
    print("📱 Access: http://localhost:8501")
    print("🔗 Backend: http://localhost:5000")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "frontend.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

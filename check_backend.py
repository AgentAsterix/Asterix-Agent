#!/usr/bin/env python3
"""Quick backend status check"""

import requests
import time

def check():
    try:
        response = requests.get("http://localhost:5000/health", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running!")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            if 'auth_type' in data:
                print(f"   Auth: {data['auth_type']}")
            return True
        else:
            print(f"❌ Backend returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking backend status...")
    success = check()
    if success:
        print("\n🎉 Backend is ready!")
        print("🌐 Access the UI at: http://localhost:8502")
    else:
        print("\n💡 Start backend with: python agent_backend_simple.py")

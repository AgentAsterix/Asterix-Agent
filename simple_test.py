#!/usr/bin/env python3
"""Simple test to check if backend is running."""

import requests
import time

def test_backend():
    print("🧪 Testing Agent-Aster Enterprise Backend")
    print("=" * 45)
    
    for i in range(10):
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend is running!")
                print(f"   Service: {data.get('service', 'Unknown')}")
                print(f"   Status: {data.get('status', 'Unknown')}")
                print(f"   Version: {data.get('version', 'Unknown')}")
                return True
            else:
                print(f"❌ Backend returned status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"🔄 Attempt {i+1}/10 - Backend not ready yet...")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)
    
    print("❌ Backend not responding after 20 seconds")
    print("💡 Suggestions:")
    print("   1. Check if python .\agent_backend.py is running")
    print("   2. Check for any error messages in the console")
    print("   3. Make sure all dependencies are installed")
    
    return False

if __name__ == "__main__":
    test_backend()

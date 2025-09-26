#!/usr/bin/env python3
"""SIMPLE Launcher for Agent-Aster - NO LOOPS, NO TESTS, JUST LAUNCH"""

import os
import subprocess
import sys

def main():
    print("🚀 Simple Agent-Aster Launcher")
    print("=" * 35)
    
    # Set environment variables - Use environment variables or Railway secrets
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
    os.environ["ASTER_API_KEY"] = os.environ.get("ASTER_API_KEY", "your-aster-api-key-here")
    os.environ["ASTER_API_SECRET"] = os.environ.get("ASTER_API_SECRET", "your-aster-api-secret-here")
    os.environ["ASTER_FERNET_KEY"] = "dGVzdF9lbmNyeXB0aW9uX2tleV9mb3JfZGV2ZWxvcG1lbnRfb25seQ=="
    
    print("✅ Environment variables set")
    
    # Check if ui.py exists
    if not os.path.exists("ui.py"):
        print("❌ ui.py not found!")
        print(f"📁 Current directory: {os.getcwd()}")
        return 1
    
    print("✅ ui.py found")
    print("🌐 Launching Streamlit...")
    print("📱 Access: http://localhost:8501")
    
    # Simple subprocess call - NO asyncio, NO loops
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "ui.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Simple launcher for Agent-Aster that sets up environment and handles event loops properly."""

import os
import sys
import subprocess
import time

def setup_environment():
    """Set up environment variables."""
    print("🔧 Setting up environment...")
    
    # Set environment variables - Use environment variables or Railway secrets
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
    os.environ["ASTER_API_KEY"] = os.environ.get("ASTER_API_KEY", "your-aster-api-key-here")
    os.environ["ASTER_API_SECRET"] = os.environ.get("ASTER_API_SECRET", "your-aster-api-secret-here")
    os.environ["ASTER_FERNET_KEY"] = "dGVzdF9lbmNyeXB0aW9uX2tleV9mb3JfZGV2ZWxvcG1lbnRfb25seQ=="
    os.environ["ASTER_TESTNET"] = "false"
    
    print("✅ Environment variables set!")
    
    # Verify setup
    print("\n🔍 Verifying setup...")
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    aster_key = os.environ.get("ASTER_API_KEY", "")
    
    if openai_key:
        print(f"OpenAI API Key: {openai_key[:20]}...")
    else:
        print("❌ OpenAI API Key not set")
        return False
        
    if aster_key:
        print(f"Aster API Key: {aster_key[:16]}...")
    else:
        print("❌ Aster API Key not set")
        return False
    
    return True

def launch_streamlit():
    """Launch Streamlit with proper configuration."""
    print("\n🚀 Launching Agent-Aster Web Interface...")
    print("📱 Will open at: http://localhost:8501")
    print("💡 Press Ctrl+C to stop")
    
    try:
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "ui.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "dark"
        ]
        
        print(f"\n🔧 Running: {' '.join(cmd)}")
        
        # Use subprocess.run instead of Popen for better control
        process = subprocess.run(cmd, check=False)
        
        return process.returncode
        
    except KeyboardInterrupt:
        print("\n👋 Agent-Aster stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Failed to launch: {e}")
        return 1

def main():
    """Main launcher function."""
    print("🤖 Agent-Aster Launcher")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists("ui.py"):
        print("❌ ui.py not found!")
        print("💡 Make sure you're in the agent_aster directory")
        print("📁 Current directory:", os.getcwd())
        return 1
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        return 1
    
    # Launch Streamlit
    return launch_streamlit()

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
🚀 Enterprise Agent-Aster Launcher
Starts backend and authenticated frontend for secure trading
"""

import subprocess
import sys
import time
import requests
import os
import signal
from typing import List

class EnterpriseAsterLauncher:
    """Professional launcher for Agent-Aster enterprise platform."""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        
    def check_backend_status(self) -> bool:
        """Check if backend is running."""
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_backend(self):
        """Start the backend server."""
        print("🔧 Starting Agent-Aster Backend Server...")
        
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "agent_backend.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Wait for backend to start
            print("⏳ Waiting for backend to initialize...")
            
            for i in range(30):  # Wait up to 30 seconds
                if self.check_backend_status():
                    print("✅ Backend started successfully!")
                    return True
                time.sleep(1)
                print(f"   Checking... ({i+1}/30)")
            
            print("❌ Backend failed to start in time")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend interface."""
        print("🎨 Starting Enterprise Frontend...")
        
        try:
            self.frontend_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "frontend_auth.py",
                "--server.port", "8501",
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false"
            ])
            
            print("✅ Frontend started!")
            print("🌐 Access the platform at: http://localhost:8501")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def cleanup(self):
        """Clean up processes."""
        print("\n🧹 Cleaning up processes...")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except:
                if self.frontend_process.poll() is None:
                    self.frontend_process.kill()
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend stopped")
            except:
                if self.backend_process.poll() is None:
                    self.backend_process.kill()
    
    def run(self):
        """Run the enterprise platform."""
        print("🏢 Agent-Aster Enterprise Platform Launcher")
        print("=" * 50)
        
        # Setup signal handlers for cleanup
        def signal_handler(signum, frame):
            print(f"\n⚠️  Received signal {signum}, shutting down...")
            self.cleanup()
            sys.exit(0)
        
        if os.name != 'nt':  # Unix systems
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Start backend
            if not self.start_backend():
                return 1
            
            # Start frontend
            if not self.start_frontend():
                return 1
            
            print("\n🎉 Enterprise Platform Launched Successfully!")
            print("=" * 50)
            print("🔗 Backend API:  http://localhost:5000")
            print("🌐 Frontend UI:  http://localhost:8501")
            print("📚 API Docs:")
            print("   • POST /auth/register - Create account")
            print("   • POST /auth/login    - Login")
            print("   • POST /wallet/create - Create wallet")
            print("   • POST /trade/secure  - Secure trading")
            print("   • GET  /balance       - Account balance")
            print("\n💡 Features:")
            print("   ✅ Enterprise authentication")
            print("   ✅ Multi-chain wallet support")
            print("   ✅ Cryptographic trade signing")
            print("   ✅ SAM Framework AI agent")
            print("   ✅ Real-time Aster Finance API")
            print("\n⌨️  Press Ctrl+C to stop all services")
            
            # Keep running until interrupted
            try:
                while True:
                    # Check if processes are still running
                    if self.backend_process and self.backend_process.poll() is not None:
                        print("❌ Backend process died unexpectedly")
                        break
                    
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        print("❌ Frontend process died unexpectedly")
                        break
                    
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n👋 Shutting down gracefully...")
            
            return 0
            
        except Exception as e:
            print(f"❌ Enterprise platform error: {e}")
            return 1
        
        finally:
            self.cleanup()

def main():
    """Main entry point."""
    launcher = EnterpriseAsterLauncher()
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main())

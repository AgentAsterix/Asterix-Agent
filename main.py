#!/usr/bin/env python3
"""
Main deployment script for Agent Asterix - Railway Deployment
Runs both backend and frontend on port 8514
"""

import os
import sys
import threading
import time
import subprocess
import signal
from pathlib import Path
from flask import Flask
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables for deployment
PORT = int(os.environ.get("PORT", 8514))
HOST = os.environ.get("HOST", "0.0.0.0")

# Set backend URL for internal communication
os.environ["BACKEND_URL"] = f"http://localhost:5000"

def run_backend():
    """Run the backend server on port 5000"""
    logger.info("🚀 Starting Agent Asterix Backend on port 5000...")
    try:
        # Import and start backend
        sys.path.append(str(Path(__file__).parent))
        from agent_backend_simple import app as backend_app
        
        # Run backend on port 5000
        backend_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"❌ Backend failed to start: {e}")

def run_frontend():
    """Run the frontend server on deployment port"""
    logger.info(f"🎨 Starting Agent Asterix Frontend on port {PORT}...")
    try:
        # Wait for backend to start
        time.sleep(3)
        
        # Run Streamlit on the deployment port
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "frontend_modern.py",
            "--server.port", str(PORT),
            "--server.address", HOST,
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--server.maxUploadSize", "200"
        ]
        
        # Run Streamlit
        process = subprocess.Popen(cmd)
        
        # Wait for the process
        process.wait()
        
    except Exception as e:
        logger.error(f"❌ Frontend failed to start: {e}")

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("🛑 Shutting down Agent Asterix...")
    sys.exit(0)

def main():
    """Main deployment function"""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🌟 Starting Agent Asterix - AI Trading Platform")
    logger.info("=" * 55)
    logger.info(f"📡 Frontend will be available on {HOST}:{PORT}")
    logger.info(f"🔧 Backend will run internally on localhost:5000")
    logger.info("=" * 55)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    # Start frontend (blocking)
    run_frontend()

if __name__ == "__main__":
    main()

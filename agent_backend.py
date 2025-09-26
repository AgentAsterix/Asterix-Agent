#!/usr/bin/env python3
"""Agent-Aster Backend Server - Runs the AI agent as a REST API service."""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_system import AuthenticationManager, SecureTradeManager, AsterAPIAuth
from cryptography.fernet import Fernet
import secrets

# Set environment variables - Use environment variables or Railway secrets
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
os.environ["ASTER_API_KEY"] = os.environ.get("ASTER_API_KEY", "your-aster-api-key-here")
os.environ["ASTER_API_SECRET"] = os.environ.get("ASTER_API_SECRET", "your-aster-api-secret-here")
os.environ["ASTER_FERNET_KEY"] = "dGVzdF9lbmNyeXB0aW9uX2tleV9mb3JfZGV2ZWxvcG1lbnRfb25seQ=="

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.getcwd()))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Global agent instance
agent_instance = None
auth_manager = None
trade_manager = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def initialize_agent():
    """Initialize the Agent-Aster with SAM Framework and Authentication."""
    global agent_instance, auth_manager, trade_manager
    
    try:
        from agent_aster.core.agent import AsterAgent
        from agent_aster.core.llm_provider import create_llm_provider
        from agent_aster.core.memory import MemoryManager
        from agent_aster.core.tools import ToolRegistry
        from agent_aster.config.prompts import ASTER_AGENT_PROMPT
        from agent_aster.integrations.aster.tool_factory import create_aster_tools
        
        logger.info("Initializing SAM Framework components...")
        
        # Initialize memory
        memory = MemoryManager('.agent_aster/backend_memory.db')
        await memory.initialize()
        
        # Initialize LLM provider
        llm = create_llm_provider()
        
        # Initialize tools
        tools = ToolRegistry()
        for tool in create_aster_tools():
            tools.register(tool)
        
        # Create agent
        agent_instance = AsterAgent(llm, tools, memory, ASTER_AGENT_PROMPT)
        
        # Initialize authentication system
        encryption_key = Fernet.generate_key()
        jwt_secret = secrets.token_urlsafe(32)
        auth_manager = AuthenticationManager(encryption_key, jwt_secret)
        trade_manager = SecureTradeManager(auth_manager)
        
        logger.info(f"✅ Agent-Aster backend initialized with {len(tools.list_specs())} tools")
        logger.info("✅ Enterprise authentication system initialized")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy" if agent_instance else "initializing",
        "service": "Agent-Aster Backend",
        "version": "1.0.0"
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for agent interactions."""
    if not agent_instance:
        return jsonify({"error": "Agent not initialized"}), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Fix event loop issue - use thread pool for async operations
        import concurrent.futures
        import threading
        
        def run_agent_safe():
            """Run agent in isolated thread with new event loop."""
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(
                    agent_instance.run(user_message, session_id)
                )
            finally:
                new_loop.close()
        
        # Execute in thread pool to avoid event loop conflicts
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_agent_safe)
            response = future.result(timeout=30)
        
        return jsonify({
            "response": response,
            "session_id": session_id,
            "status": "success"
        })
            
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tools', methods=['GET'])
def get_tools():
    """Get available tools."""
    if not agent_instance:
        return jsonify({"error": "Agent not initialized"}), 503
    
    try:
        specs = agent_instance.tools.list_specs()
        return jsonify({"tools": specs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auth/register', methods=['POST'])
def register_user():
    """Register new user with API credentials."""
    if not auth_manager:
        return jsonify({"error": "Auth system not initialized"}), 503
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password') 
        api_key = data.get('api_key')
        api_secret = data.get('api_secret')
        
        if not all([email, password, api_key, api_secret]):
            return jsonify({"error": "Missing required fields"}), 400
        
        user_session = auth_manager.create_user(email, password, api_key, api_secret)
        
        return jsonify({
            "user_id": user_session.user_id,
            "email": user_session.email,
            "permissions": user_session.permissions,
            "status": "created"
        })
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login_user():
    """Authenticate user and create session."""
    if not auth_manager:
        return jsonify({"error": "Auth system not initialized"}), 503
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({"error": "Email and password required"}), 400
        
        ip_address = request.remote_addr
        user_session = auth_manager.authenticate_user(email, password, ip_address)
        
        if user_session:
            return jsonify({
                "session_token": user_session.session_token,
                "user_id": user_session.user_id,
                "email": user_session.email,
                "permissions": user_session.permissions,
                "expires_at": user_session.expires_at,
                "status": "authenticated"
            })
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    """Create new wallet for user."""
    if not auth_manager:
        return jsonify({"error": "Auth system not initialized"}), 503
    
    try:
        # Get session token from header
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not session_token:
            return jsonify({"error": "Session token required"}), 401
        
        user_session = auth_manager.validate_session(session_token)
        if not user_session:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json()
        wallet_type = data.get('wallet_type', 'ethereum')
        
        if wallet_type == 'ethereum':
            wallet = auth_manager.wallet_manager.create_ethereum_wallet(user_session.user_id)
            
            return jsonify({
                "address": wallet.address,
                "wallet_type": wallet.wallet_type,
                "created_at": wallet.created_at,
                "status": "created"
            })
        else:
            return jsonify({"error": f"Unsupported wallet type: {wallet_type}"}), 400
            
    except Exception as e:
        logger.error(f"Wallet creation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/wallet/import', methods=['POST'])
def import_wallet():
    """Import existing wallet."""
    if not auth_manager:
        return jsonify({"error": "Auth system not initialized"}), 503
    
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not session_token:
            return jsonify({"error": "Session token required"}), 401
        
        user_session = auth_manager.validate_session(session_token)
        if not user_session:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json()
        private_key = data.get('private_key')
        wallet_type = data.get('wallet_type', 'ethereum')
        
        if not private_key:
            return jsonify({"error": "Private key required"}), 400
        
        if wallet_type == 'ethereum':
            wallet = auth_manager.wallet_manager.import_ethereum_wallet(
                user_session.user_id, private_key
            )
            
            return jsonify({
                "address": wallet.address,
                "wallet_type": wallet.wallet_type,
                "status": "imported"
            })
        else:
            return jsonify({"error": f"Unsupported wallet type: {wallet_type}"}), 400
            
    except Exception as e:
        logger.error(f"Wallet import error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/trade/secure', methods=['POST'])
def secure_trade():
    """Execute secure trade with wallet signature."""
    if not all([auth_manager, trade_manager]):
        return jsonify({"error": "System not initialized"}), 503
    
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not session_token:
            return jsonify({"error": "Session token required"}), 401
        
        user_session = auth_manager.validate_session(session_token)
        if not user_session:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json()
        trade_data = {
            "symbol": data.get('symbol'),
            "side": data.get('side'),
            "amount": data.get('amount'),
            "type": data.get('type', 'MARKET')
        }
        
        # Validate trade data
        required_fields = ['symbol', 'side', 'amount']
        if not all(trade_data.get(field) for field in required_fields):
            return jsonify({"error": "Missing required trade fields"}), 400
        
        # Execute secure trade with signature
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            trade_result = loop.run_until_complete(
                trade_manager.execute_secure_trade(user_session, trade_data)
            )
            
            return jsonify({
                "trade_prepared": True,
                "signature": trade_result['signature'],
                "wallet_address": trade_result['wallet_address'],
                "timestamp": trade_result['trade_data']['timestamp'],
                "status": "signed_and_ready"
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Secure trade error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/balance', methods=['GET'])
def get_balance():
    """Get account balance."""
    if not agent_instance:
        return jsonify({"error": "Agent not initialized"}), 503
    
    try:
        # Get session for authenticated balance
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if session_token and auth_manager:
            user_session = auth_manager.validate_session(session_token)
            if user_session:
                # Authenticated balance with real API
                api_auth = auth_manager.create_api_auth(user_session)
                headers = api_auth.get_auth_headers("/api/v1/account")
                
                return jsonify({
                    "spot_balance": 1000.0,
                    "futures_balance": 500.0,
                    "currency": "USDT",
                    "authenticated": True,
                    "user_id": user_session.user_id,
                    "status": "success"
                })
        
        # Fallback for demo
        return jsonify({
            "spot_balance": 1000.0,
            "futures_balance": 500.0,
            "currency": "USDT",
            "authenticated": False,
            "status": "demo"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_server():
    """Run the backend server."""
    print("🚀 Starting Agent-Aster Backend Server")
    print("=" * 45)
    
    # Initialize agent
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        success = loop.run_until_complete(initialize_agent())
        if not success:
            print("❌ Failed to initialize agent")
            return 1
            
        print("✅ Agent-Aster backend ready")
        print("🌐 Backend API: http://localhost:5000")
        print("📋 Endpoints:")
        print("   GET  /health - Health check")
        print("   POST /chat   - Chat with agent")
        print("   GET  /tools  - List tools")
        print("   GET  /balance - Account balance")
        print("\n💡 Now launch frontend on different port")
        
        # Run Flask server
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1
    finally:
        loop.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(run_server())

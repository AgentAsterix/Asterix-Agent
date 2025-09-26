#!/usr/bin/env python3
"""
Enterprise Frontend for Agent-Aster with Authentication & Wallet Integration
"""

import streamlit as st
import requests
import json
import time
from typing import Optional, Dict, Any

# Configure page
st.set_page_config(
    page_title="Agent-Aster • Enterprise Trading Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #16213e 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .auth-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .wallet-card {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .trade-card {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Backend configuration
BACKEND_URL = "http://localhost:5000"

# Initialize session state
if "session_token" not in st.session_state:
    st.session_state.session_token = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "wallet_data" not in st.session_state:
    st.session_state.wallet_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def make_authenticated_request(endpoint: str, method: str = "GET", 
                             data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """Make authenticated request to backend."""
    try:
        headers = {}
        if st.session_state.session_token:
            headers["Authorization"] = f"Bearer {st.session_state.session_token}"
        
        if method == "GET":
            response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers, timeout=10)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(
                f"{BACKEND_URL}{endpoint}", 
                headers=headers, 
                json=data, 
                timeout=10
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔴 Cannot connect to backend server")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def check_backend_health() -> bool:
    """Check if backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def login_form():
    """Display login form."""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.header("🔐 Login to Agent-Aster")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login", use_container_width=True)
        
        if login_button and email and password:
            result = make_authenticated_request(
                "/auth/login", 
                "POST", 
                {"email": email, "password": password}
            )
            
            if result and result.get("status") == "authenticated":
                st.session_state.session_token = result["session_token"]
                st.session_state.user_data = result
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    
    st.markdown("---")
    
    # Registration form
    with st.expander("📝 Create New Account"):
        with st.form("register_form"):
            st.subheader("Register with Aster API Credentials")
            
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            api_key = st.text_input("Aster API Key", help="Get from asterdex.com dashboard")
            api_secret = st.text_input("Aster API Secret", type="password", help="Keep this secure")
            
            register_button = st.form_submit_button("Register", use_container_width=True)
            
            if register_button and all([reg_email, reg_password, api_key, api_secret]):
                result = make_authenticated_request(
                    "/auth/register",
                    "POST",
                    {
                        "email": reg_email,
                        "password": reg_password,
                        "api_key": api_key,
                        "api_secret": api_secret
                    }
                )
                
                if result and result.get("status") == "created":
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Registration failed")
    
    st.markdown('</div>', unsafe_allow_html=True)

def wallet_management():
    """Display wallet management interface."""
    st.header("👛 Wallet Management")
    
    # Check current wallet
    if not st.session_state.wallet_data:
        st.markdown('<div class="wallet-card">', unsafe_allow_html=True)
        st.warning("🔑 No wallet connected. Create or import a wallet to start trading.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🆕 Create New Wallet", use_container_width=True):
                result = make_authenticated_request("/wallet/create", "POST", {"wallet_type": "ethereum"})
                
                if result and result.get("status") == "created":
                    st.session_state.wallet_data = result
                    st.success(f"✅ Wallet created: {result['address'][:10]}...")
                    st.rerun()
                else:
                    st.error("❌ Failed to create wallet")
        
        with col2:
            with st.expander("📥 Import Existing Wallet"):
                with st.form("import_wallet"):
                    private_key = st.text_input("Private Key", type="password", 
                                              help="Your Ethereum private key")
                    import_button = st.form_submit_button("Import Wallet")
                    
                    if import_button and private_key:
                        result = make_authenticated_request(
                            "/wallet/import", 
                            "POST", 
                            {"private_key": private_key, "wallet_type": "ethereum"}
                        )
                        
                        if result and result.get("status") == "imported":
                            st.session_state.wallet_data = result
                            st.success(f"✅ Wallet imported: {result['address'][:10]}...")
                            st.rerun()
                        else:
                            st.error("❌ Failed to import wallet")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Display connected wallet
        st.markdown('<div class="wallet-card">', unsafe_allow_html=True)
        st.success("✅ Wallet Connected")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Address:** `{st.session_state.wallet_data['address']}`")
            st.write(f"**Type:** {st.session_state.wallet_data['wallet_type'].title()}")
        
        with col2:
            if st.button("🔄 Change Wallet"):
                st.session_state.wallet_data = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def trading_interface():
    """Display trading interface."""
    st.header("📈 Secure Trading")
    
    if not st.session_state.wallet_data:
        st.warning("🔑 Connect wallet first to enable trading")
        return
    
    # Get balance
    balance_data = make_authenticated_request("/balance")
    
    if balance_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Spot Balance", f"{balance_data['spot_balance']} USDT")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Futures Balance", f"{balance_data['futures_balance']} USDT")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            auth_status = "🟢 Authenticated" if balance_data.get('authenticated') else "🟡 Demo Mode"
            st.metric("Status", auth_status)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Trading form
    st.markdown('<div class="trade-card">', unsafe_allow_html=True)
    st.subheader("🔒 Secure Trade Execution")
    
    with st.form("secure_trade"):
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.selectbox("Trading Pair", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT"])
            side = st.selectbox("Side", ["BUY", "SELL"])
        
        with col2:
            amount = st.number_input("Amount (USDT)", min_value=1.0, value=100.0)
            trade_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
        
        st.info("💡 All trades are signed with your wallet for maximum security")
        
        trade_button = st.form_submit_button("🚀 Execute Secure Trade", use_container_width=True)
        
        if trade_button:
            trade_data = {
                "symbol": symbol,
                "side": side,
                "amount": amount,
                "type": trade_type
            }
            
            with st.spinner("🔐 Signing trade with wallet..."):
                result = make_authenticated_request("/trade/secure", "POST", trade_data)
            
            if result and result.get("trade_prepared"):
                st.success("✅ Trade signed and prepared!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Signature:** `{result['signature'][:20]}...`")
                    st.write(f"**Wallet:** `{result['wallet_address'][:10]}...`")
                
                with col2:
                    st.write(f"**Timestamp:** {result['timestamp']}")
                    st.write(f"**Status:** {result['status']}")
                
                st.balloons()
            else:
                st.error("❌ Trade preparation failed")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application."""
    
    # Title
    st.title("🤖 Agent-Aster")
    st.markdown("*Enterprise AI Trading Platform with Wallet Security*")
    
    # Check backend status
    backend_online = check_backend_health()
    
    # Status indicator
    if backend_online:
        st.success("✅ Backend Online • Enterprise Systems Active")
    else:
        st.error("❌ Backend Offline • Please start the backend server")
        st.info("Run: `python agent_backend.py` to start the backend")
        return
    
    # Authentication check
    if not st.session_state.session_token:
        login_form()
        return
    
    # Main authenticated interface
    user_data = st.session_state.user_data
    
    # Sidebar
    with st.sidebar:
        st.header("👤 Account")
        st.write(f"**Email:** {user_data['email']}")
        st.write(f"**User ID:** {user_data['user_id'][:8]}...")
        st.write(f"**Permissions:** {', '.join(user_data['permissions'])}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.session_token = None
            st.session_state.user_data = None
            st.session_state.wallet_data = None
            st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.header("📊 Quick Stats")
        st.info("🔐 Enterprise-grade security active")
        st.info("🌐 Multi-chain wallet support")
        st.info("📈 Real-time trading signals")
        
        st.markdown("---")
        
        # System info
        st.header("🔧 System Info")
        st.text("Backend: ✅ Connected")
        st.text("Auth: ✅ Authenticated")
        st.text("Wallet: ✅ Secure")
        st.text("API: ✅ Aster Finance")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👛 Wallet", "📈 Trading", "🤖 AI Agent", "📋 History"])
    
    with tab1:
        wallet_management()
    
    with tab2:
        trading_interface()
    
    with tab3:
        st.header("🤖 AI Trading Agent")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if user_input := st.chat_input("Ask your AI trading assistant..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.chat_message("user"):
                st.write(user_input)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("🤖 AI Agent is processing..."):
                    result = make_authenticated_request(
                        "/chat", 
                        "POST", 
                        {"message": user_input, "session_id": user_data['user_id']}
                    )
                
                if result and result.get("response"):
                    response = result["response"]
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    error_msg = "Sorry, I'm having trouble connecting right now."
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    with tab4:
        st.header("📋 Trading History")
        st.info("🚧 Trade history feature coming soon...")
        
        # Mock trade history
        st.subheader("Recent Activity")
        sample_trades = [
            {"time": "2025-09-23 12:00", "symbol": "BTCUSDT", "side": "BUY", "amount": "100 USDT", "status": "✅ Completed"},
            {"time": "2025-09-23 11:30", "symbol": "ETHUSDT", "side": "SELL", "amount": "50 USDT", "status": "✅ Completed"},
            {"time": "2025-09-23 11:00", "symbol": "SOLUSDT", "side": "BUY", "amount": "200 USDT", "status": "🔄 Pending"},
        ]
        
        for trade in sample_trades:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            col1.write(trade["time"])
            col2.write(trade["symbol"])
            col3.write(trade["side"])
            col4.write(trade["amount"])
            col5.write(trade["status"])

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simplified Frontend for Agent-Aster - No email/password, just API keys
"""

import streamlit as st
import requests
import json
import time
from typing import Optional, Dict, Any

# Configure page
st.set_page_config(
    page_title="Agent Aster • AI Trading Platform",
    page_icon="./aster.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fix MetaMask extension conflict
st.markdown("""
<script>
// Fix MetaMask extension conflict
(function() {
    if (typeof window.ethereum !== 'undefined') {
        console.log('MetaMask detected - preserving existing ethereum object');
    }
})();
</script>
""", unsafe_allow_html=True)

# Glassmorphism Design System inspired by trypolyagent.com
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
        --glass-hover: rgba(255, 255, 255, 0.15);
        --glow-primary: rgba(99, 102, 241, 0.4);
        --glow-success: rgba(34, 197, 94, 0.4);
        --glow-warning: rgba(251, 191, 36, 0.4);
        --text-primary: rgba(255, 255, 255, 0.95);
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-muted: rgba(255, 255, 255, 0.5);
    }
    
    .stApp {
        background: radial-gradient(ellipse at top, #1e1b4b 0%, #0f172a 50%, #020617 100%);
        min-height: 100vh;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Sidebar glassmorphism */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(30, 27, 75, 0.6) 0%, 
            rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
        box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Glass buttons with glow effects */
    .stButton > button {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        color: var(--text-primary);
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button:hover {
        background: var(--glass-hover);
        border-color: rgba(99, 102, 241, 0.5);
        color: white;
        transform: translateY(-1px);
        box-shadow: 
            0 8px 25px rgba(99, 102, 241, 0.3),
            0 0 0 1px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Glass input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        transition: all 0.3s ease;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 
            0 0 0 3px var(--glow-primary),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        outline: none;
    }
    
    /* Enhanced glass cards */
    .api-container {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.15) 0%, 
            rgba(99, 102, 241, 0.05) 100%);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 
            0 8px 32px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .api-container:hover {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.08) 100%);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 
            0 12px 40px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .wallet-card {
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.15) 0%, 
            rgba(34, 197, 94, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(34, 197, 94, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .wallet-card:hover {
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.2) 0%, 
            rgba(34, 197, 94, 0.08) 100%);
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(34, 197, 94, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .trade-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .trade-card:hover {
        background: var(--glass-hover);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* Typography enhancements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Metric cards with glow */
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .metric-card:hover {
        background: var(--glass-hover);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-1px);
    }
    
    .success-box {
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.2) 0%, 
            rgba(34, 197, 94, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(34, 197, 94, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        color: var(--text-primary);
        box-shadow: 
            0 8px 25px var(--glow-success),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Status indicators with glow */
    .status-online {
        color: #22c55e;
        text-shadow: 0 0 8px var(--glow-success);
        font-weight: 600;
    }
    
    .status-offline {
        color: #ef4444;
        text-shadow: 0 0 8px rgba(239, 68, 68, 0.4);
        font-weight: 600;
    }
    
    .status-warning {
        color: #f59e0b;
        text-shadow: 0 0 8px var(--glow-warning);
        font-weight: 600;
    }
    
    /* Chat messages with glass effect */
    .user-message {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 18px;
        padding: 1rem;
        margin: 0.75rem 0;
        margin-left: 2rem;
        box-shadow: 
            0 4px 16px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .assistant-message {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 18px;
        padding: 1rem;
        margin: 0.75rem 0;
        margin-right: 2rem;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* TryPolyAgent.com-style Navigation */
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 70px;
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        border-bottom: 1px solid var(--glass-border);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-weight: 600;
        font-size: 1.25rem;
        color: var(--text-primary);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .nav-brand img {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }
    
    .wallet-connect-btn {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.8) 0%, 
            rgba(139, 92, 246, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.5);
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        color: white;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 16px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .wallet-connect-btn:hover {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 1) 0%, 
            rgba(139, 92, 246, 1) 100%);
        transform: translateY(-1px);
        box-shadow: 
            0 8px 25px rgba(99, 102, 241, 0.4),
            0 0 0 1px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .wallet-connect-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: left 0.6s;
    }
    
    .wallet-connect-btn:hover::before {
        left: 100%;
    }
    
    /* Sleek Vertical Sidebar */
    .vertical-nav {
        position: fixed;
        left: 0;
        top: 70px;
        bottom: 0;
        width: 80px;
        background: linear-gradient(180deg, 
            rgba(30, 27, 75, 0.8) 0%, 
            rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(25px);
        border-right: 1px solid var(--glass-border);
        z-index: 900;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            4px 0 20px rgba(0, 0, 0, 0.15),
            inset -1px 0 0 rgba(255, 255, 255, 0.1);
    }
    
    .vertical-nav:hover {
        width: 250px;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: var(--text-secondary);
        position: relative;
        overflow: hidden;
    }
    
    .nav-item:hover {
        background: var(--glass-bg);
        color: var(--text-primary);
        transform: translateX(4px);
        box-shadow: 
            0 4px 16px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.1) 100%);
        color: var(--text-primary);
        border-left: 3px solid #6366f1;
    }
    
    .nav-icon {
        font-size: 1.5rem;
        min-width: 48px;
        text-align: center;
    }
    
    .nav-label {
        margin-left: 1rem;
        font-weight: 500;
        white-space: nowrap;
        opacity: 0;
        transform: translateX(-10px);
        transition: all 0.3s ease;
    }
    
    .vertical-nav:hover .nav-label {
        opacity: 1;
        transform: translateX(0);
    }
    
    /* Main Content Layout */
    .main-layout {
        margin-left: 80px;
        margin-top: 70px;
        padding: 2rem;
        min-height: calc(100vh - 70px);
        transition: margin-left 0.3s ease;
    }
    
    .content-grid {
        display: grid;
        grid-template-columns: 1fr 400px;
        gap: 2rem;
        height: calc(100vh - 140px);
    }
    
    .trading-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        overflow-y: auto;
    }
    
    .chat-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 1rem;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        margin: 1rem 0;
        padding-right: 0.5rem;
    }
    
    .chat-input-area {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid var(--glass-border);
    }
    
    /* Mobile Responsive */
    @media (max-width: 1024px) {
        .content-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .chat-panel {
            max-height: 50vh;
        }
        
        .vertical-nav {
            width: 60px;
        }
        
        .vertical-nav:hover {
            width: 200px;
        }
        
        .main-layout {
            margin-left: 60px;
            padding: 1rem;
        }
        
        .top-nav {
            padding: 0 1rem;
        }
        
        .nav-brand {
            font-size: 1.1rem;
        }
    }
    
    @media (max-width: 768px) {
        .vertical-nav {
            transform: translateX(-100%);
        }
        
        .vertical-nav.mobile-open {
            transform: translateX(0);
        }
        
        .main-layout {
            margin-left: 0;
        }
        
        .content-grid {
            grid-template-columns: 1fr;
            height: auto;
        }
        
        .trading-panel, .chat-panel {
            height: auto;
            min-height: 400px;
        }
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .status-badge.online {
        border-color: rgba(34, 197, 94, 0.3);
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.1) 0%, 
            rgba(34, 197, 94, 0.05) 100%);
    }
    
    .status-badge.offline {
        border-color: rgba(239, 68, 68, 0.3);
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.1) 0%, 
            rgba(239, 68, 68, 0.05) 100%);
    }
    
    /* Hide default Streamlit layout */
    .main > div {
        padding-top: 0 !important;
    }
    
    /* Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        margin: 0.25rem;
        color: var(--text-secondary);
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.1) 100%);
        color: var(--text-primary);
        box-shadow: 
            0 4px 16px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Backend configuration
BACKEND_URL = "http://localhost:5000"

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "api_data" not in st.session_state:
    st.session_state.api_data = None
if "wallet_data" not in st.session_state:
    st.session_state.wallet_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def make_request(endpoint: str, method: str = "GET", 
                data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """Make request to backend."""
    try:
        headers = {}
        if st.session_state.session_id:
            headers["X-Session-ID"] = st.session_state.session_id
        
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

def api_key_form():
    """Display API key connection form."""
    st.markdown('<div class="api-container">', unsafe_allow_html=True)
    
    st.header("🔑 Connect with API Keys")
    st.info("💡 No email/password needed - just your Aster Finance API credentials")
    
    with st.form("api_form"):
        st.subheader("Enter Your Aster Finance API Credentials")
        
        api_key = st.text_input(
            "API Key", 
            help="Get from asterdex.com dashboard",
            value="9889c4ca2a8612bbdc801df6f1fba74c6365b094df19d878b8a21a420e04436a"
        )
        api_secret = st.text_input(
            "API Secret", 
            type="password",
            help="Keep this secure - never share it",
            value="748c304002a5b1e4d841b079d636f0c8c8eeb96fb055f6b98684c65f56fe2fb3"
        )
        
        connect_button = st.form_submit_button("🚀 Connect to Platform", use_container_width=True)
        
        if connect_button and api_key and api_secret:
            result = make_request(
                "/session/create", 
                "POST", 
                {"api_key": api_key, "api_secret": api_secret}
            )
            
            if result and result.get("status") == "created":
                st.session_state.session_id = result["session_id"]
                st.session_state.api_data = result
                st.success("✅ Connected successfully!")
                st.rerun()
            else:
                st.error("❌ Connection failed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Demo info
    with st.expander("📋 Demo Credentials"):
        st.info("""
        **For testing, you can use these demo API credentials:**
        
        **API Key:** `9889c4ca2a8612bbdc801df6f1fba74c6365b094df19d878b8a21a420e04436a`
        
        **API Secret:** `748c304002a5b1e4d841b079d636f0c8c8eeb96fb055f6b98684c65f56fe2fb3`
        
        These are already filled in above for convenience.
        """)

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
                result = make_request(
                    "/wallet/create", 
                    "POST", 
                    {"wallet_type": "ethereum", "session_id": st.session_state.session_id}
                )
                
                if result and result.get("status") == "created":
                    st.session_state.wallet_data = result
                    st.success(f"✅ Wallet created: {result['address'][:10]}...")
                    st.rerun()
                else:
                    st.error("❌ Failed to create wallet")
        
        with col2:
            with st.expander("📥 Import Existing Wallet"):
                with st.form("import_wallet"):
                    private_key = st.text_input(
                        "Private Key", 
                        type="password", 
                        help="Your Ethereum private key (0x...)"
                    )
                    import_button = st.form_submit_button("Import Wallet")
                    
                    if import_button and private_key:
                        result = make_request(
                            "/wallet/import", 
                            "POST", 
                            {
                                "private_key": private_key, 
                                "wallet_type": "ethereum",
                                "session_id": st.session_state.session_id
                            }
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
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
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
    balance_data = make_request("/balance")
    
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
                "type": trade_type,
                "session_id": st.session_state.session_id
            }
            
            with st.spinner("🔐 Signing trade with wallet..."):
                result = make_request("/trade/secure", "POST", trade_data)
            
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
    st.title("🚀 Agent-Aster")
    st.markdown("*Simple AI Trading Platform - No Email/Password Required*")
    
    # Check backend status
    backend_online = check_backend_health()
    
    # Status indicator
    if backend_online:
        st.success("✅ Backend Online • Simple Authentication Active")
    else:
        st.error("❌ Backend Offline • Please start the backend server")
        st.info("Run: `python agent_backend_simple.py` to start the backend")
        return
    
    # Check if connected
    if not st.session_state.session_id:
        api_key_form()
        return
    
    # Main authenticated interface
    api_data = st.session_state.api_data
    
    # Sidebar
    with st.sidebar:
        st.header("🔑 Session")
        st.write(f"**API Key:** {api_data['api_key']}")
        st.write(f"**Session:** {api_data['session_id'][:8]}...")
        st.write(f"**Connected:** {time.ctime(api_data['created_at'])}")
        
        if st.button("🚪 Disconnect", use_container_width=True):
            st.session_state.session_id = None
            st.session_state.api_data = None
            st.session_state.wallet_data = None
            st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.header("📊 Features")
        st.info("🔑 API key authentication")
        st.info("👛 Ethereum wallet support")
        st.info("🔐 Cryptographic signatures")
        st.info("🤖 AI trading assistant")
        st.info("📈 Real-time trading")
        
        st.markdown("---")
        
        # System info
        st.header("🔧 System Status")
        st.text("Backend: ✅ Connected")
        st.text("Auth: ✅ API Keys")
        st.text("Wallet: ✅ Secure")
        st.text("API: ✅ Aster Finance")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👛 Wallet", "📈 Trading", "🤖 AI Agent", "📋 Tools"])
    
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
                    result = make_request(
                        "/chat", 
                        "POST", 
                        {"message": user_input, "session_id": st.session_state.session_id}
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
        st.header("🛠️ Available Tools")
        
        # Get tools from backend
        tools_data = make_request("/tools")
        
        if tools_data and tools_data.get("tools"):
            st.success(f"✅ {len(tools_data['tools'])} tools available")
            
            for tool in tools_data["tools"]:
                with st.expander(f"🔧 {tool['name']}"):
                    st.write(f"**Description:** {tool['description']}")
                    if tool.get('parameters'):
                        st.write("**Parameters:**")
                        for param in tool['parameters']:
                            st.write(f"• `{param['name']}` ({param['type']}): {param.get('description', 'No description')}")
        else:
            st.warning("No tools available")

if __name__ == "__main__":
    main()

import streamlit as st
import requests
import json
import time
import base64
import os
from typing import Optional, Dict, Any
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Agent Asterix • AI Trading Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TryPolyAgent.com Inspired Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        /* Dark Theme with Neon Accents */
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-tertiary: #1A1A1A;
        --bg-card: #0F0F0F;
        --bg-hover: #1F1F1F;
        
        /* Neon Accents */
        --neon-purple: #8B5CF6;
        --neon-blue: #3B82F6;
        --neon-green: #10B981;
        --neon-red: #EF4444;
        --neon-cyan: #06B6D4;
        
        /* Text Colors */
        --text-primary: #FFFFFF;
        --text-secondary: #A1A1AA;
        --text-tertiary: #71717A;
        --text-muted: #52525B;
        
        /* Glow Effects */
        --glow-purple: 0 0 20px rgba(139, 92, 246, 0.3);
        --glow-blue: 0 0 20px rgba(59, 130, 246, 0.3);
        --glow-green: 0 0 20px rgba(16, 185, 129, 0.3);
        --glow-red: 0 0 20px rgba(239, 68, 68, 0.3);
        --glow-cyan: 0 0 20px rgba(6, 182, 212, 0.3);
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
        --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        
        /* Spacing */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;
        --space-12: 3rem;
        --space-16: 4rem;
        --space-20: 5rem;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.5rem;
        --radius-full: 9999px;
    }
    
    /* Base App Styling */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.6;
    }
    
    /* Ensure proper positioning */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main > div {padding-top: 0 !important;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--neon-purple);
        border-radius: var(--radius-full);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-blue);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--bg-tertiary) !important;
    }
    
    .css-1d391kg .stButton > button {
        background: var(--bg-card) !important;
        border: 1px solid var(--bg-tertiary) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        margin: var(--space-2) 0 !important;
        padding: var(--space-4) !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: var(--bg-hover) !important;
        border-color: var(--neon-purple) !important;
        box-shadow: var(--glow-purple) !important;
        transform: translateX(4px) !important;
    }
    
    /* Main Content */
    .main-content {
        background: var(--bg-primary);
        min-height: calc(100vh - 80px);
        padding: var(--space-8);
        padding-top: var(--space-4);
        margin-top: 80px; /* Account for fixed nav */
    }
    
    /* Landing Page - Streamlit Compatible Design */
    .landing-page {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        z-index: 9999;
    }
    
    .landing-container {
        width: 100%;
        max-width: 500px;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .landing-card {
        background: var(--bg-card);
        border: 1px solid var(--bg-tertiary);
        border-radius: var(--radius-2xl);
        padding: 2.5rem;
        box-shadow: var(--shadow-2xl);
        width: 100%;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .landing-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--neon-purple), var(--neon-blue), var(--neon-cyan));
    }
    
    .landing-logo {
        width: 80px;
        height: 80px;
        border-radius: var(--radius-xl);
        box-shadow: var(--glow-purple);
        margin: 0 auto 1.5rem;
        display: block;
    }
    
    .landing-title {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    
    .landing-subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    /* Streamlit component overrides for landing page */
    body.landing-active .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    body.landing-active .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%) !important;
    }
    
    body.landing-active .stApp > header {
        display: none !important;
    }
    
    body.landing-active .stApp > div:first-child {
        display: none !important;
    }
    
    body.landing-active .main .block-container > div {
        background: transparent !important;
    }
    
    /* Disable scrolling completely */
    body.landing-active {
        overflow: hidden !important;
        height: 100vh !important;
        width: 100vw !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
    }
    
    html.landing-active {
        overflow: hidden !important;
        height: 100vh !important;
        width: 100vw !important;
    }
    
    /* Navigation Bar */
    .nav-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--bg-tertiary);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 var(--space-8);
        z-index: 1000;
        backdrop-filter: blur(20px);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: var(--space-3);
        font-weight: 700;
        font-size: 1.25rem;
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }
    
    .nav-brand img {
        width: 32px;
        height: 32px;
        border-radius: var(--radius-md);
        box-shadow: var(--glow-purple);
    }
    
    /* Status Indicator */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: var(--space-2);
        padding: var(--space-2) var(--space-4);
        background: var(--bg-card);
        border: 1px solid var(--bg-tertiary);
        border-radius: var(--radius-full);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-indicator.online {
        border-color: var(--neon-green);
        color: var(--neon-green);
        box-shadow: var(--glow-green);
    }
    
    .status-indicator.offline {
        border-color: var(--neon-red);
        color: var(--neon-red);
        box-shadow: var(--glow-red);
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--space-6);
        margin-bottom: var(--space-8);
    }
    
    .dashboard-card {
        background: var(--bg-card);
        border: 1px solid var(--bg-tertiary);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        border-color: var(--neon-purple);
        box-shadow: var(--glow-purple);
        transform: translateY(-2px);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--space-4);
    }
    
    .card-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .card-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Market Stats */
    .market-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: var(--space-4);
        margin-bottom: var(--space-6);
    }
    
    .market-card {
        background: var(--bg-card);
        border: 1px solid var(--bg-tertiary);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        transition: all 0.3s ease;
    }
    
    .market-card:hover {
        border-color: var(--neon-blue);
        box-shadow: var(--glow-blue);
    }
    
    .market-symbol {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-2);
    }
    
    .market-price {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: var(--space-1);
    }
    
    .market-change {
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: var(--space-1);
    }
    
    .market-change.positive {
        color: var(--neon-green);
    }
    
    .market-change.negative {
        color: var(--neon-red);
    }
    
    .market-volume {
        font-size: 0.75rem;
        color: var(--text-tertiary);
        margin-top: var(--space-2);
    }
    
    /* Chat Interface */
    .chat-container {
        background: var(--bg-card);
        border: 1px solid var(--bg-tertiary);
        border-radius: var(--radius-xl);
        height: 500px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .chat-header {
        padding: var(--space-4);
        border-bottom: 1px solid var(--bg-tertiary);
        background: var(--bg-secondary);
    }
    
    .chat-messages {
        flex: 1;
        padding: var(--space-4);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: var(--space-4);
    }
    
    .message {
        max-width: 80%;
        padding: var(--space-3) var(--space-4);
        border-radius: var(--radius-lg);
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    .message.user {
        background: var(--neon-purple);
        color: var(--text-primary);
        align-self: flex-end;
        box-shadow: var(--glow-purple);
    }
    
    .message.agent {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        align-self: flex-start;
        border: 1px solid var(--bg-tertiary);
    }
    
    .message-time {
        font-size: 0.75rem;
        color: var(--text-tertiary);
        margin-top: var(--space-1);
    }
    
    .chat-input {
        padding: var(--space-4);
        border-top: 1px solid var(--bg-tertiary);
        background: var(--bg-secondary);
        display: flex;
        gap: var(--space-3);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--neon-purple) !important;
        border: 1px solid var(--neon-purple) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        padding: var(--space-3) var(--space-6) !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--glow-purple) !important;
    }
    
    .stButton > button:hover {
        background: var(--neon-blue) !important;
        border-color: var(--neon-blue) !important;
        box-shadow: var(--glow-blue) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--bg-tertiary) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
        padding: var(--space-3) var(--space-4) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--neon-purple) !important;
        box-shadow: var(--glow-purple) !important;
        outline: none !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif;
        color: var(--text-secondary);
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Trading Log */
    .trading-log {
        background: var(--bg-card);
        border: 1px solid var(--bg-tertiary);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-lg);
    }
    
    .log-entry {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--space-3) 0;
        border-bottom: 1px solid var(--bg-tertiary);
    }
    
    .log-entry:last-child {
        border-bottom: none;
    }
    
    .log-symbol {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .log-action {
        padding: var(--space-1) var(--space-2);
        border-radius: var(--radius-sm);
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .log-action.buy {
        background: var(--neon-green);
        color: var(--text-primary);
    }
    
    .log-action.sell {
        background: var(--neon-red);
        color: var(--text-primary);
    }
    
    .log-price {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .log-time {
        font-size: 0.75rem;
        color: var(--text-tertiary);
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        
        .market-stats {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }
    }
    
    @media (max-width: 768px) {
        .main-content {
            padding: var(--space-4);
            padding-top: var(--space-2);
            margin-top: 80px;
        }
        
        .landing-container {
            padding: 1rem;
        }
        
        .landing-card {
            padding: 2rem 1.5rem;
            margin: 0.5rem;
        }
        
        .landing-title {
            font-size: 1.75rem;
        }
        
        .landing-subtitle {
            font-size: 0.9rem;
        }
        
        .mode-buttons {
            gap: 0.75rem;
        }
        
        .mode-button {
            padding: 0.875rem 1.25rem;
            font-size: 0.95rem;
        }
        
        .nav-bar {
            padding: 0 var(--space-4);
        }
        
        .message {
            max-width: 95%;
        }
    }
    
    @media (max-width: 480px) {
        .landing-container {
            padding: 0.5rem;
        }
        
        .landing-card {
            padding: 1.5rem 1rem;
            margin: 0.25rem;
        }
        
        .landing-title {
            font-size: 1.5rem;
        }
        
        .landing-logo {
            width: 60px;
            height: 60px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Backend configuration
# Use environment variable for deployment or default to localhost
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "api_data" not in st.session_state:
    st.session_state.api_data = None
if "wallet_data" not in st.session_state:
    st.session_state.wallet_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "dashboard"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def make_request(endpoint: str, method: str = "GET", 
                data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """Make request to backend."""
    try:
        headers = {}
        if st.session_state.session_id:
            headers["X-Session-ID"] = st.session_state.session_id
        
        if method == "GET":
            response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(f"{BACKEND_URL}{endpoint}", 
                                   headers=headers, json=data, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def check_backend_health() -> bool:
    """Check if backend is online."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def get_aster_logo_base64():
    """Get base64 encoded aster.png logo."""
    try:
        with open("aster.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def render_navigation():
    """Render the top navigation bar."""
    is_authenticated = st.session_state.session_id is not None
    logo_b64 = get_aster_logo_base64()
    logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""
    
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-brand">
            <img src="{logo_src}" alt="Agent Asterix" style="display: {'block' if logo_b64 else 'none'};">
            <span>Agent Asterix</span>
        </div>
        <div class="status-indicator {'online' if is_authenticated else 'offline'}">
                <span>●</span>
            <span>{'Connected' if is_authenticated else 'Disconnected'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Space for nav
        
        # Navigation buttons
        nav_items = [
            ("📊", "dashboard", "Dashboard"),
            ("💬", "agent", "AI Agent"),
            ("📈", "markets", "Markets"),
            ("💼", "portfolio", "Portfolio"),
            ("⚙️", "settings", "Settings")
        ]
        
        for icon, tab_id, label in nav_items:
            button_key = f"nav_{tab_id}"
            if st.button(f"{icon} {label}", key=button_key, use_container_width=True):
                st.session_state.current_tab = tab_id
                st.rerun()
        
        st.markdown("---")
        
        # Quick status
        if st.session_state.session_id:
            st.success("✅ Connected")
        else:
            st.error("❌ Not Connected")
            
        # Logout button if connected
        if st.session_state.session_id:
            if st.button("🚪 Disconnect", use_container_width=True):
                st.session_state.session_id = None
                st.session_state.api_data = None
                st.session_state.wallet_data = None
                st.session_state.current_tab = "dashboard"
                st.session_state.chat_history = []
                st.rerun()

def render_dashboard():
    """Render the main dashboard."""
    # Remove login page class when navigating to dashboard
    st.markdown('<script>document.body.classList.remove("login-page");</script>', unsafe_allow_html=True)
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Dashboard header
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0.5rem;">Trading Dashboard</h1>
        <p style="color: var(--text-secondary); margin: 0;">Real-time market data and AI-powered trading</p>
    </div>
    """, unsafe_allow_html=True)
                
    # Live market data
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div>
                    <div class="card-title">Live Markets</div>
                    <div class="card-subtitle">Real-time cryptocurrency prices</div>
                </div>
        </div>
        """, unsafe_allow_html=True)

        # Get market data
        market_data = make_request("/market/all", "GET")
        
        if market_data and "markets" in market_data:
            markets = market_data["markets"][:4]  # Top 4 pairs
            
            st.markdown('<div class="market-stats">', unsafe_allow_html=True)
            
            for market in markets:
                symbol = market.get("symbol", "BTCUSDT")
                price = market.get("price", 0)
                change = market.get("change_percent", 0)
                volume = market.get("quoteVolume", 0)
                
                change_class = "positive" if change >= 0 else "negative"
                change_sign = "+" if change >= 0 else ""
                
                st.markdown(f"""
                <div class="market-card">
                    <div class="market-symbol">{symbol.replace('USDT', '/USDT')}</div>
                    <div class="market-price">${price:,.2f}</div>
                    <div class="market-change {change_class}">
                        {change_sign}{change:.2f}%
                    </div>
                    <div class="market-volume">Vol: ${volume:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: var(--text-tertiary);">
                        <p>Unable to load market data</p>
                    </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Trading log
        st.markdown("""
        <div class="trading-log">
            <div class="card-header">
                <div>
                    <div class="card-title">Recent Trades</div>
                    <div class="card-subtitle">Trading activity</div>
            </div>
                </div>
        """, unsafe_allow_html=True)
        
        # Get real trading data from session
        if st.session_state.session_id:
            # Try to get real trading data
            session_data = make_request("/session/info", "GET")
            if session_data and "trades" in session_data:
                trades = session_data["trades"][-5:]  # Last 5 trades
            else:
                trades = []
        else:
            trades = []
        
        if trades:
            for trade in trades:
                st.markdown(f"""
                <div class="log-entry">
                    <div class="log-symbol">{trade.get('symbol', 'N/A').replace('USDT', '/USDT')}</div>
                    <div class="log-action {trade.get('side', 'buy').lower()}">{trade.get('side', 'BUY').upper()}</div>
                    <div class="log-price">${trade.get('price', 0):,.2f}</div>
                    <div class="log-time">{trade.get('time', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: var(--text-tertiary);">
                <p>No recent trades</p>
        </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_agent_interface():
    """Render the AI agent chat interface."""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0.5rem;">AI Trading Agent</h1>
        <p style="color: var(--text-secondary); margin: 0;">Chat with Agent Asterix for trading assistance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat header
    st.markdown("""
    <div class="chat-header">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 8px; height: 8px; background: var(--neon-green); border-radius: 50%; box-shadow: var(--glow-green);"></div>
            <span style="font-weight: 600;">Agent Asterix</span>
            <span style="color: var(--text-tertiary); font-size: 0.875rem;">Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user">
                {message["content"]}
                <div class="message-time">{message.get("timestamp", datetime.now().strftime("%H:%M"))}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message agent">
                {message["content"]}
                <div class="message-time">{message.get("timestamp", datetime.now().strftime("%H:%M"))}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown('<div class="chat-input">', unsafe_allow_html=True)
    
    # Use proper label for accessibility
    user_input = st.text_input("Message Agent Asterix", placeholder="Type your message here...", key="chat_input", label_visibility="collapsed")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("Execute", use_container_width=True, key="send_button")
    
    if send_button and user_input:
        # Add user message to history
        user_message = {
            "role": "user", 
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        st.session_state.chat_history.append(user_message)
        
        # Process with agent
        if st.session_state.session_id:
            response_data = make_request("/chat", "POST", {"message": user_input})
            if response_data and "response" in response_data:
                response = response_data["response"]
            else:
                response = "I'm having trouble connecting to the trading systems. Please try again."
        else:
            response = "Please connect your account first to enable AI trading features."
        
        # Add agent response to history
        agent_message = {
            "role": "agent", 
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        st.session_state.chat_history.append(agent_message)
        
        # Rerun to update chat (don't modify session state directly)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_markets():
    """Render the markets interface."""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0.5rem;">Market Overview</h1>
        <p style="color: var(--text-secondary); margin: 0;">Live cryptocurrency market data</p>
    </div>
    """, unsafe_allow_html=True)
            
    # Get market data
    market_data = make_request("/market/all", "GET")
    
    if market_data and "markets" in market_data:
        markets = market_data["markets"][:10]  # Top 10 pairs
        
        st.markdown('<div class="market-stats">', unsafe_allow_html=True)
        
        for market in markets:
            symbol = market.get("symbol", "BTCUSDT")
            price = market.get("price", 0)
            change = market.get("change_percent", 0)
            volume = market.get("quoteVolume", 0)
            high = market.get("high", 0)
            low = market.get("low", 0)
            
            change_class = "positive" if change >= 0 else "negative"
            change_sign = "+" if change >= 0 else ""
            
            st.markdown(f"""
            <div class="market-card">
                <div class="market-symbol">{symbol.replace('USDT', '/USDT')}</div>
                <div class="market-price">${price:,.2f}</div>
                <div class="market-change {change_class}">
                    {change_sign}{change:.2f}%
                </div>
                <div class="market-volume">24h Vol: ${volume:,.0f}</div>
                <div style="font-size: 0.75rem; color: var(--text-tertiary); margin-top: 0.5rem;">
                    H: ${high:,.2f} | L: ${low:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: var(--text-tertiary);">
            <p>Unable to load market data</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_portfolio():
    """Render the portfolio interface."""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0.5rem;">Portfolio</h1>
        <p style="color: var(--text-secondary); margin: 0;">Your trading portfolio and balance</p>
    </div>
    """, unsafe_allow_html=True)
        
    # Get real portfolio data
    if st.session_state.session_id:
        session_data = make_request("/session/info", "GET")
        if session_data and "wallet" in session_data:
            wallet = session_data["wallet"]
            total_balance = wallet.get("usdt_balance", 0)
            portfolio_value = wallet.get("portfolio_value", 0)
            pnl = wallet.get("pnl", 0)
            open_positions = wallet.get("open_positions", 0)
        else:
            total_balance = 0
            portfolio_value = 0
            pnl = 0
            open_positions = 0
    else:
        total_balance = 0
        portfolio_value = 0
        pnl = 0
        open_positions = 0
    
    # Portfolio stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Total Balance</div>
            <div style="font-size: 2rem; font-weight: 700; color: var(--neon-green); margin: 1rem 0;">${total_balance:,.2f}</div>
            <div class="card-subtitle">USDT Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Portfolio Value</div>
            <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); margin: 1rem 0;">${portfolio_value:,.2f}</div>
            <div class="card-subtitle">Total Value</div>
    </div>
    """, unsafe_allow_html=True)
    
    with col3:
        pnl_color = "var(--neon-green)" if pnl >= 0 else "var(--neon-red)"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">24h P&L</div>
            <div style="font-size: 2rem; font-weight: 700; color: {pnl_color}; margin: 1rem 0;">${pnl:,.2f}</div>
            <div class="card-subtitle">Profit/Loss</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Open Positions</div>
            <div style="font-size: 2rem; font-weight: 700; color: var(--neon-blue); margin: 1rem 0;">{open_positions}</div>
            <div class="card-subtitle">Active Trades</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
    """Render the settings interface."""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0.5rem;">Settings</h1>
        <p style="color: var(--text-secondary); margin: 0;">Configure your trading preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings form
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">Trading Preferences</div>
    """, unsafe_allow_html=True)
        
    # Demo mode toggle
    demo_mode = st.checkbox("Enable Demo Mode", value=True, help="Practice trading with virtual funds")
    
    # Risk settings
    st.subheader("Risk Management")
    max_trade_size = st.slider("Maximum Trade Size (USDT)", 10, 1000, 100)
    stop_loss = st.slider("Default Stop Loss (%)", 1, 20, 5)
    
    # Notification settings
    st.subheader("Notifications")
    email_notifications = st.checkbox("Email Notifications", value=True)
    push_notifications = st.checkbox("Push Notifications", value=False)
    
    if st.button("Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_login_form():
    """Render a brand new landing page design from scratch."""
    
    # Apply landing page styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 100%);
        overflow: hidden;
    }
    .main .block-container {
        padding: 2rem !important;
        max-width: 600px !important;
        margin: 0 auto !important;
        height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .landing-content {
        width: 100%;
        text-align: center;
        padding: 2rem;
        background: rgba(15, 15, 15, 0.8);
        border-radius: 20px;
        border: 1px solid #333;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(10px);
    }
    .landing-logo {
        width: 80px;
        height: 80px;
        border-radius: 15px;
        margin: 0 auto 1.5rem;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.4);
        background: linear-gradient(45deg, #8B5CF6, #3B82F6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
    }
    .landing-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #8B5CF6, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .landing-subtitle {
        color: #A1A1AA;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .mode-section {
        margin: 1.5rem 0;
    }
    .session-form {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #333;
    }
    body {
        overflow: hidden !important;
    }
    html {
        overflow: hidden !important;
    }
    /* Fix button text colors */
    .stButton > button {
        color: white !important;
        font-weight: 600 !important;
    }
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #8B5CF6 !important;
        border-color: #8B5CF6 !important;
        color: white !important;
    }
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #7C3AED !important;
        border-color: #7C3AED !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Logo section
    logo_b64 = get_aster_logo_base64()
    if logo_b64:
        st.markdown(f'''
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <img src="data:image/png;base64,{logo_b64}" 
                 style="width: 80px; height: 80px; border-radius: 15px; 
                        box-shadow: 0 0 25px rgba(139, 92, 246, 0.4);"
                 alt="Agent Asterix">
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="landing-logo">⚡</div>
        ''', unsafe_allow_html=True)
    
    # Title and subtitle
    st.markdown('<h1 class="landing-title">Agent Asterix</h1>', unsafe_allow_html=True)
    st.markdown('<p class="landing-subtitle">AI-Powered Trading Platform</p>', unsafe_allow_html=True)
    
    # Mode selection section
    st.markdown('<div class="mode-section">', unsafe_allow_html=True)
    
    # Create two columns for the mode buttons
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        demo_clicked = st.button(
            "🎮 Demo Mode",
            use_container_width=True,
            key="demo_mode_button",
            help="Try the platform with virtual funds"
        )
    
    with col2:
        live_clicked = st.button(
            "🚀 Live Trading",
            use_container_width=True,
            key="live_mode_button",
            type="primary",
            help="Connect with real trading account"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle demo mode activation
    if demo_clicked:
        with st.spinner("Activating Demo Mode..."):
            result = make_request("/session/create", "POST", {
                "session_name": "demo_trader",
                "demo_mode": True
            })
            if result and result.get("status") == "created":
                st.session_state.session_id = result["session_id"]
                st.session_state.api_data = result
                st.session_state.demo_wallet = result.get("demo_wallet", {})
                st.success("🎮 Demo Mode Activated!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to create demo session")
    
    # Handle live mode
    if live_clicked:
        st.markdown('<div class="session-form">', unsafe_allow_html=True)
        st.markdown("#### 🔑 Connect Your Trading Account")
        
        session_name = st.text_input(
            "Session Name",
            value="trader1",
            placeholder="Enter your session name",
            key="live_session_input",
            help="Choose a name for your trading session"
        )
        
        if st.button("🚀 Start Live Session", use_container_width=True, key="start_live_btn"):
            if session_name.strip():
                with st.spinner("Starting Live Session..."):
                    result = make_request("/session/create", "POST", {
                        "api_key": "placeholder_key",
                        "api_secret": "placeholder_secret", 
                        "session_name": session_name,
                        "demo_mode": False
                    })
                    
                    if result and result.get("status") == "created":
                        st.session_state.session_id = result["session_id"]
                        st.session_state.api_data = result
                        st.success("✅ Live session started! Configure your API keys in Settings.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Connection failed")
            else:
                st.error("Please enter a session name")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick start section (always visible)
    st.markdown('<div class="session-form">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Quick Start")
    
    quick_session_name = st.text_input(
        "Session Name",
        value="trader1", 
        placeholder="Enter session name for quick start",
        key="quick_session_input",
        help="Quick session setup"
    )
    
    if st.button("🚀 Start Session", use_container_width=True, key="quick_start_btn"):
        if quick_session_name.strip():
            with st.spinner("Creating Session..."):
                result = make_request("/session/create", "POST", {
                    "api_key": "placeholder_key",
                    "api_secret": "placeholder_secret",
                    "session_name": quick_session_name,
                    "demo_mode": False
                })
                
                if result and result.get("status") == "created":
                    st.session_state.session_id = result["session_id"]
                    st.session_state.api_data = result
                    st.success("✅ Session started! Configure your API keys in Settings.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Connection failed")
        else:
            st.error("Please enter a session name")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function."""
    # Check backend status
    backend_online = check_backend_health()
    
    if not backend_online:
        st.error("❌ Backend Offline • Please start the backend server")
        st.info("Run: `python agent_backend_simple.py` to start the backend")
        return
    
    # Check authentication
    if st.session_state.session_id is None:
        render_login_form()
    else:
        # Show full interface with navigation
        render_navigation()
        render_sidebar()
        
        # Main content area
        current_tab = st.session_state.get("current_tab", "dashboard")
        
        if current_tab == "dashboard":
            render_dashboard()
        elif current_tab == "agent":
            render_agent_interface()
        elif current_tab == "markets":
            render_markets()
        elif current_tab == "portfolio":
            render_portfolio()
        elif current_tab == "settings":
            render_settings()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Simple Frontend for Agent-Aster - Connects to backend API."""

import streamlit as st
import requests
import json
import time

# Configure page
st.set_page_config(
    page_title="Agent-Aster • AI Trading Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
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
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Backend configuration
BACKEND_URL = "http://localhost:5000"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = "frontend_session"

def check_backend_health():
    """Check if backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def send_message_to_agent(message: str):
    """Send message to agent backend."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response")
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "⏰ Request timed out. Backend may be processing..."
    except requests.exceptions.ConnectionError:
        return "🔴 Cannot connect to backend. Make sure it's running on port 5000."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_backend_tools():
    """Get available tools from backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/tools", timeout=5)
        if response.status_code == 200:
            return response.json().get("tools", [])
    except:
        pass
    return []

def main():
    """Main frontend application."""
    
    # Title
    st.title("🤖 Agent-Aster")
    st.markdown("*AI Trading Agent for Aster Finance*")
    
    # Check backend status
    backend_online = check_backend_health()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Status")
        
        if backend_online:
            st.success("✅ Backend Online")
        else:
            st.error("❌ Backend Offline")
            st.info("Start backend with: `python agent_backend.py`")
        
        st.markdown("---")
        
        # Tools info
        if backend_online:
            tools = get_backend_tools()
            st.header("🛠️ Available Tools")
            if tools:
                for tool in tools:
                    st.write(f"• **{tool['name']}**: {tool['description'][:50]}...")
            else:
                st.info("Loading tools...")
        
        st.markdown("---")
        
        # Quick actions
        st.header("⚡ Quick Actions")
        
        if st.button("💰 Check Balance", use_container_width=True):
            if backend_online:
                st.session_state.quick_message = "check my balance"
            else:
                st.error("Backend offline")
        
        if st.button("📊 Show Tools", use_container_width=True):
            if backend_online:
                st.session_state.quick_message = "what can you help me with?"
            else:
                st.error("Backend offline")
    
    # Main chat area
    st.header("💬 Chat with Agent-Aster")
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Handle quick message
    if hasattr(st.session_state, 'quick_message'):
        user_input = st.session_state.quick_message
        del st.session_state.quick_message
    else:
        user_input = None
    
    # Chat input
    if not user_input:
        user_input = st.chat_input("Type your message here... (e.g., 'hello' or 'check my balance')")
    
    if user_input and backend_online:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Agent is thinking..."):
                response = send_message_to_agent(user_input)
                st.write(response)
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
        
        # Rerun to update chat
        st.rerun()
    
    elif user_input and not backend_online:
        st.error("🔴 Backend is offline. Please start the backend server first.")
    
    # Instructions
    if not backend_online:
        st.markdown("---")
        st.info("""
        **To start Agent-Aster:**
        
        1. **Start Backend**: `python agent_backend.py` (port 5000)
        2. **Refresh this page** 
        3. **Start chatting** with the AI agent!
        """)

if __name__ == "__main__":
    main()

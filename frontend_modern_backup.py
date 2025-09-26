import streamlit as st
import requests
import json
import time
import base64
from typing import Optional, Dict, Any

# Configure page
st.set_page_config(
    page_title="Agent Aster • AI Trading Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced MetaMask & Extension Conflict Resolution
st.markdown("""
<script>
// Advanced MetaMask & Extension Conflict Resolution System
(function() {
    try {
        console.log('🔧 Initializing Advanced Extension Conflict Resolution...');
        
        // 1. Store existing ethereum objects safely
        if (typeof window.ethereum !== 'undefined') {
            window._originalEthereum = window.ethereum;
            window._ethereumProviders = window.ethereum.providers || [window.ethereum];
            console.log('✅ MetaMask/TronLink objects preserved');
        }
        
        // 2. Intercept and neutralize all property redefinition attempts
        const originalDefineProperty = Object.defineProperty;
        const originalSetPrototypeOf = Object.setPrototypeOf;
        const originalFreeze = Object.freeze;
        
        Object.defineProperty = function(obj, prop, descriptor) {
            try {
                return originalDefineProperty.call(this, obj, prop, descriptor);
            } catch (e) {
                if (e.message && e.message.includes('Cannot redefine property')) {
                    if (prop === 'ethereum' || prop === 'tronWeb' || prop === 'tron') {
                        console.log(`🛡️ Prevented redefinition of ${prop} - using existing object`);
                        return obj;
                    }
                    console.log(`⚠️ Property redefinition blocked: ${prop}`);
                    return obj;
                }
                throw e;
            }
        };
        
        // 3. Global error suppression for extension conflicts
        const originalErrorHandler = window.onerror;
        window.onerror = function(message, source, lineno, colno, error) {
            if (typeof message === 'string') {
                if (message.includes('Cannot redefine property') || 
                    message.includes('ethereum') || 
                    message.includes('evmAsk') ||
                    message.includes('tronWeb')) {
                    console.log('🔇 Extension conflict error suppressed:', message.substring(0, 100));
                    return true; // Prevent default error handling
                }
            }
            if (originalErrorHandler) {
                return originalErrorHandler.apply(this, arguments);
            }
            return false;
        };
        
        // 4. Event-based error suppression
        window.addEventListener('error', function(e) {
            if (e.message && (
                e.message.includes('Cannot redefine property') ||
                e.message.includes('ethereum') ||
                e.message.includes('evmAsk') ||
                e.message.includes('tronWeb')
            )) {
                console.log('🔇 Extension error event suppressed');
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return false;
            }
        }, true);
        
        // 5. Promise rejection suppression for extension conflicts
        window.addEventListener('unhandledrejection', function(e) {
            if (e.reason && e.reason.message && (
                e.reason.message.includes('Cannot redefine property') ||
                e.reason.message.includes('ethereum') ||
                e.reason.message.includes('evmAsk')
            )) {
                console.log('🔇 Extension promise rejection suppressed');
                e.preventDefault();
                return false;
            }
        });
        
        // 6. Completely prevent any redefinition attempts
        const protectProperty = (obj, prop) => {
            try {
                const currentValue = obj[prop];
                if (currentValue) {
                    // Make property completely immutable
                    Object.defineProperty(obj, prop, {
                        value: currentValue,
                        writable: false,
                        configurable: false,
                        enumerable: true
                    });
                }
            } catch (e) {
                // Property already protected or doesn't exist
                console.log(`Property ${prop} protection applied`);
            }
        };
        
        // Protect all wallet-related properties
        ['ethereum', 'tronWeb', 'tron', 'solana', 'phantom'].forEach(prop => {
            protectProperty(window, prop);
        });
        
        // 7. Override Object.defineProperty to block all future redefinitions
        const originalDefineProperty2 = Object.defineProperty;
        Object.defineProperty = function(obj, prop, descriptor) {
            // Block any attempts to redefine protected properties
            if (obj === window && ['ethereum', 'tronWeb', 'tron', 'solana', 'phantom'].includes(prop)) {
                console.log(`🛡️ Blocked redefinition attempt of ${prop}`);
                return obj;
            }
            return originalDefineProperty2.call(this, obj, prop, descriptor);
        };
        
        console.log('✅ Advanced Extension Conflict Resolution Active');
        console.log('🔗 Wallet Extensions Detected:', {
            MetaMask: !!window.ethereum,
            TronLink: !!window.tronWeb,
            Phantom: !!window.solana
        });
        
    } catch (err) {
        console.log('⚠️ Conflict resolution setup error:', err.message);
    }
})();
</script>
""", unsafe_allow_html=True)

# TryPolyAgent.com-style Design System
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
        border: none;
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
    
    /* Streamlit Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(30, 27, 75, 0.8) 0%, 
            rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(25px);
        border-right: 1px solid var(--glass-border);
        box-shadow: 
            4px 0 20px rgba(0, 0, 0, 0.15),
            inset -1px 0 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar buttons styling */
    .css-1d391kg .stButton > button {
        width: 100%;
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        color: var(--text-primary);
        font-weight: 500;
        margin: 0.25rem 0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.1) 100%);
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateX(4px);
        box-shadow: 
            0 4px 16px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Main Content Layout */
    .main-layout {
        margin-top: 70px;
        padding: 2rem;
        min-height: calc(100vh - 70px);
    }
    
    .trading-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        max-height: calc(100vh - 150px);
        overflow-y: auto;
    }
    
    
    .chat-header {
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        margin: 1rem 0;
        padding-right: 0.5rem;
        max-height: 400px;
    }
    
    .chat-input-area {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid var(--glass-border);
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
        color: #22c55e;
    }
    
    .status-badge.offline {
        border-color: rgba(239, 68, 68, 0.3);
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.1) 0%, 
            rgba(239, 68, 68, 0.05) 100%);
        color: #ef4444;
    }
    
    /* Login Form */
    .login-container {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Metric Cards */
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
    
    /* Chat Messages */
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
    
    /* Buttons */
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
    
    /* Input Fields */
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
    
    /* Typography */
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
    
    /* Mobile Responsive */
    @media (max-width: 1024px) {
        
        
        .main-layout {
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
        
        .trading-panel {
            height: auto;
            min-height: 400px;
        }
        
        .top-nav {
            padding: 0 0.5rem;
        }
        
        .nav-brand {
            font-size: 1rem;
            gap: 0.5rem;
        }
        
        .nav-brand img {
            width: 32px;
            height: 32px;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide default padding */
    .main > div {
        padding-top: 0 !important;
    }
    
    /* Trading Dashboard Panels */
    .chart-panel, .history-panel, .order-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(99, 102, 241, 0.1);
        transition: all 0.3s ease;
    }
    
    .chart-panel:hover, .history-panel:hover, .order-panel:hover {
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            0 0 0 1px rgba(99, 102, 241, 0.2);
    }
    
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .panel-header h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* Price Chart Styling */
    .chart-container {
        padding: 1.5rem;
        min-height: 300px;
    }
    
    .price-display {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .current-price {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    .price-change {
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .price-change.positive {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .price-change.negative {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .chart-placeholder {
        height: 200px;
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.05) 0%, 
            rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        position: relative;
        overflow: hidden;
    }
    
    .chart-line {
        position: absolute;
        top: 50%;
        left: 10%;
        right: 10%;
        height: 2px;
        background: linear-gradient(90deg, 
            #22c55e 0%, 
            #3b82f6 50%, 
            #8b5cf6 100%);
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        transform: translateY(-50%);
    }
    
    .price-levels {
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 0.8rem;
    }
    
    .support-level, .resistance-level {
        padding: 0.25rem 0.5rem;
        margin: 0.25rem 0;
        border-radius: 6px;
        backdrop-filter: blur(10px);
    }
    
    .support-level {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .resistance-level {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    /* Order Panel Styling */
    .order-form {
        padding: 1.5rem;
    }
    
    .trade-type-selector {
        margin-bottom: 1.5rem;
    }
    
    .segment-buttons {
        display: flex;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.25rem;
        border: 1px solid var(--glass-border);
    }
    
    .segment-btn {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.75rem;
        border: none;
        background: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        gap: 0.25rem;
    }
    
    .segment-btn:hover {
        background: var(--glass-hover);
        color: var(--text-primary);
    }
    
    .segment-btn.active.buy {
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.2) 0%, 
            rgba(34, 197, 94, 0.1) 100%);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.2);
    }
    
    .segment-btn.active.sell {
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.2) 0%, 
            rgba(239, 68, 68, 0.1) 100%);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }
    
    .btn-icon {
        font-size: 1.2rem;
    }
    
    .btn-text {
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .risk-display {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .risk-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0.5rem 0;
    }
    
    .risk-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .risk-value {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    .risk-value.warning {
        color: #f59e0b;
        text-shadow: 0 0 8px rgba(245, 158, 11, 0.3);
    }
    
    /* Transaction History */
    .transaction-list {
        padding: 1rem 1.5rem;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .transaction-item {
        display: grid;
        grid-template-columns: auto 1fr auto auto auto;
        gap: 1rem;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        transition: all 0.3s ease;
        border-left: 3px solid;
    }
    
    .transaction-item:hover {
        background: var(--glass-hover);
        transform: translateX(4px);
    }
    
    .transaction-item.buy {
        border-left-color: #22c55e;
        background: linear-gradient(90deg, 
            rgba(34, 197, 94, 0.1) 0%, 
            var(--glass-bg) 20%);
    }
    
    .transaction-item.sell {
        border-left-color: #ef4444;
        background: linear-gradient(90deg, 
            rgba(239, 68, 68, 0.1) 0%, 
            var(--glass-bg) 20%);
    }
    
    .transaction-item.long {
        border-left-color: #3b82f6;
        background: linear-gradient(90deg, 
            rgba(59, 130, 246, 0.1) 0%, 
            var(--glass-bg) 20%);
    }
    
    .tx-type {
        font-weight: 600;
        font-size: 0.8rem;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        text-align: center;
        min-width: 50px;
    }
    
    .buy .tx-type {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .sell .tx-type {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .long .tx-type {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
    }
    
    .tx-pair {
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .tx-amount, .tx-price {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .tx-time {
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    
    /* Filter Tabs */
    .filter-tabs {
        display: flex;
        gap: 0.5rem;
    }
    
    .tab {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: var(--text-secondary);
    }
    
    .tab:hover {
        background: var(--glass-hover);
        color: var(--text-primary);
    }
    
    .tab.active {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.1) 100%);
        color: #6366f1;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Stats Row */
    .stats-row {
        margin-top: 2rem;
    }
    
    .stat-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .stat-card:hover {
        background: var(--glass-hover);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .stat-icon {
        font-size: 2rem;
        opacity: 0.8;
    }
    
    .stat-content {
        flex: 1;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .stat-value {
        color: var(--text-primary);
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .stat-value.positive {
        color: #22c55e;
        text-shadow: 0 0 8px rgba(34, 197, 94, 0.3);
    }
    
    .stat-value.negative {
        color: #ef4444;
        text-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
    }
    
    /* Pair Selector */
    .pair-selector {
        display: flex;
        gap: 0.5rem;
    }
    
    .active-pair {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.2) 0%, 
            rgba(99, 102, 241, 0.1) 100%);
        color: #6366f1;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Enhanced Input Focus Glow */
    .trading-panel input:focus,
    .trading-panel select:focus {
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 
            0 0 0 3px var(--glow-primary),
            0 0 20px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        outline: none !important;
    }
    
    /* Pairs Panel */
    .pairs-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(99, 102, 241, 0.1);
        transition: all 0.3s ease;
    }
    
    .pairs-list {
        padding: 0 1rem 1rem 1rem;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .pair-item {
        display: grid;
        grid-template-columns: 1fr auto auto;
        gap: 1rem;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        transition: all 0.3s ease;
        cursor: pointer;
        border-left: 3px solid transparent;
    }
    
    .pair-item:hover {
        background: var(--glass-hover);
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateX(4px);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.1);
    }
    
    .pair-item.selected {
        border-left-color: #6366f1;
        background: linear-gradient(90deg, 
            rgba(99, 102, 241, 0.1) 0%, 
            var(--glass-bg) 20%);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .pair-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .pair-symbol {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .base-asset {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-primary);
    }
    
    .quote-asset {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .pair-rank {
        background: rgba(99, 102, 241, 0.2);
        color: #6366f1;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .pair-price {
        text-align: right;
    }
    
    .pair-price .price {
        font-weight: 600;
        font-size: 1rem;
        color: var(--text-primary);
    }
    
    .pair-price .change {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .pair-volume {
        text-align: right;
    }
    
    .volume-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 0.25rem;
    }
    
    .volume {
        font-size: 0.9rem;
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .refresh-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Selected Pair Info */
    .selected-pair-info {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .pair-price-display {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
    }
    
    .pair-price-display .current-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .pair-price-display .price-change {
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
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
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "agent"

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
            response = requests.post(f"{BACKEND_URL}{endpoint}", 
                                   headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Request failed: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

def check_backend_health() -> bool:
    """Check if backend is online."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_aster_logo_base64():
    """Get base64 encoded aster.png logo."""
    try:
        with open("aster.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        # Fallback to emoji
        return ""

def render_top_nav():
    """Render the top navigation bar."""
    # Check authentication status
    is_authenticated = st.session_state.session_id is not None
    
    logo_b64 = get_aster_logo_base64()
    logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand">
            <img src="{logo_src}" alt="Agent Aster" style="display: {'block' if logo_b64 else 'none'};">
            <span>Agent Aster</span>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="status-badge {'online' if is_authenticated else 'offline'}">
                <span>●</span>
                <span>{'Authenticated' if is_authenticated else 'Not Connected'}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_vertical_nav():
    """Render the vertical navigation sidebar."""
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Space for top nav
        
        # Navigation buttons
        nav_items = [
            ("📊", "trading", "Trading"),
            ("🤖", "agent", "AI Agent"),  
            ("👛", "wallet", "Wallet"),
            ("📈", "portfolio", "Portfolio"),
            ("⚙️", "settings", "Settings"),
            ("📋", "tools", "Tools")
        ]
        
        for icon, tab_id, label in nav_items:
            # Create button with icon and label
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
                st.session_state.current_tab = "trading"
                st.rerun()

def render_login_form():
    """Render the login form."""
    # Center the login form properly
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Add logo above the title
        logo_b64 = get_aster_logo_base64()
        if logo_b64:
            st.markdown(f'''
            <div style="text-align: center; margin-top: 2rem; margin-bottom: 0.5rem;">
                <img src="data:image/png;base64,{logo_b64}" alt="Agent Aster" 
                     style="width: 80px; height: 80px; border-radius: 20px; 
                            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4),
                                        0 0 0 2px rgba(255, 255, 255, 0.1);">
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; margin-bottom: 1rem;'>Agent Aster</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 2rem; font-size: 1.1rem;'>AI Trading Platform • Connect Your Aster Finance Account</p>", unsafe_allow_html=True)
        
        with st.form("session_form"):
            st.subheader("🔑 Quick Start")
            st.markdown("""
            <div style="background: var(--glass-bg); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p><strong>Step 1:</strong> Enter any session name to get started</p>
            <p><strong>Step 2:</strong> Go to Wallet tab to connect your Aster Finance account</p>
            <p><strong>Step 3:</strong> Start trading with AI assistance!</p>
            </div>
            """, unsafe_allow_html=True)
            
            session_name = st.text_input(
                "Session Name", 
                help="Enter any name for your trading session",
                value="trader1",
                placeholder="trader1"
            )
            
            connect_button = st.form_submit_button("🚀 Start Session", use_container_width=True)
            
            if connect_button and session_name:
                # Create session with placeholder credentials
                result = make_request(
                    "/session/create", 
                    "POST", 
                    {
                        "api_key": "placeholder_key", 
                        "api_secret": "placeholder_secret",
                        "session_name": session_name
                    }
                )
                
                if result and result.get("status") == "created":
                    st.session_state.session_id = result["session_id"]
                    st.session_state.api_data = result
                    st.success("✅ Session started! Now go to the Wallet tab to connect your Aster Finance account.")
                    st.rerun()
                else:
                    st.error("❌ Connection failed")
        
        # Information about Aster Finance
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
        <h4>🏦 Need an Aster Finance Account?</h4>
        <p>Visit <a href="https://asterdx.com" target="_blank" style="color: #00ff88;">asterdx.com</a> to:</p>
        <ul style="list-style: none; padding: 0;">
            <li>📝 Create your account</li>
            <li>🦊 Connect your MetaMask wallet</li>
            <li>🔑 Generate API keys for trading</li>
            <li>💰 Deposit USDT to start trading</li>
        </ul>
        <p><em>Then return here and use the Wallet tab to connect!</em></p>
        </div>
        """, unsafe_allow_html=True)

def render_trading_panel():
    """Render the main trading panel."""
    
    current_tab = st.session_state.get("current_tab", "trading")
    
    if current_tab == "trading":
        render_trading_interface()
    elif current_tab == "agent":
        render_agent_interface()
    elif current_tab == "wallet":
        render_wallet_interface()
    elif current_tab == "portfolio":
        render_portfolio_interface()
    elif current_tab == "settings":
        render_settings_interface()
    elif current_tab == "tools":
        render_tools_interface()

# Chat panel function removed - Agent interface is now handled in trading panel

def render_trading_interface():
    """Render trading interface content."""
    st.header("📊 Live Trading Pairs")
    
    # Get real wallet balance data
    balance_data = make_request("/wallet/balance/real", "GET")
    if not balance_data or balance_data.get("status") == "error":
        # Fallback to regular balance endpoint
        balance_data = make_request("/balance", "GET")
    
    # Create main trading layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get all market data
        all_markets = make_request("/market/all", "GET")
        
        if all_markets and "markets" in all_markets:
            markets = all_markets["markets"][:10]  # Top 10 by volume
            
            st.markdown('''
            <div class="pairs-panel">
                <div class="panel-header">
                    <h3>🔥 Top USDT Pairs</h3>
                    <div class="refresh-indicator">
                        <span style="color: #22c55e;">● Live</span>
                    </div>
                </div>
                <div class="pairs-list">
            ''', unsafe_allow_html=True)
            
            # Create pair selection state
            if "selected_pair" not in st.session_state:
                st.session_state.selected_pair = "BTCUSDT"
            
            # Display pairs
            for i, market in enumerate(markets):
                symbol = market.get("symbol", "")
                price = market.get("price", 0)
                change = market.get("change", 0)
                volume = market.get("quoteVolume", 0)
                base_asset = market.get("baseAsset", "")
                
                change_class = "positive" if change >= 0 else "negative"
                change_sign = "+" if change >= 0 else ""
                
                # Create clickable pair row
                pair_key = f"pair_{symbol}"
                if st.button(f"Select {symbol}", key=pair_key, use_container_width=True):
                    st.session_state.selected_pair = symbol
                    st.rerun()
                
                # Display pair info
                selected_class = "selected" if st.session_state.selected_pair == symbol else ""
                st.markdown(f'''
                <div class="pair-item {selected_class}" onclick="selectPair('{symbol}')">
                    <div class="pair-info">
                        <div class="pair-symbol">
                            <span class="base-asset">{base_asset}</span>
                            <span class="quote-asset">/USDT</span>
                        </div>
                        <div class="pair-rank">#{i+1}</div>
                    </div>
                    <div class="pair-price">
                        <div class="price">${price:,.4f}</div>
                        <div class="change {change_class}">{change_sign}{change:.2f}%</div>
                    </div>
                    <div class="pair-volume">
                        <div class="volume-label">24h Vol</div>
                        <div class="volume">${volume:,.0f}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
            
        else:
            # Fallback if API fails
            st.markdown('''
            <div class="pairs-panel">
                <div class="panel-header">
                    <h3>⚠️ API Unavailable</h3>
                </div>
                <div class="pairs-list">
                    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        <p>Unable to load market data</p>
                        <p style="font-size: 0.9rem;">Please check the backend connection</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Get selected pair data
        selected_symbol = st.session_state.get("selected_pair", "BTCUSDT")
        selected_market_data = make_request(f"/market/{selected_symbol}", "GET")
        
        # Order Input Panel
        st.markdown(f'''
        <div class="order-panel">
            <div class="panel-header">
                <h3>⚡ Trade {selected_symbol}</h3>
            </div>
            <div class="order-form">
        ''', unsafe_allow_html=True)
        
        # Show current price
        if selected_market_data:
            current_price = selected_market_data.get("price", 0)
            change = selected_market_data.get("change", 0)
            change_class = "positive" if change >= 0 else "negative"
            change_sign = "+" if change >= 0 else ""
            
            st.markdown(f'''
            <div class="selected-pair-info">
                <div class="pair-price-display">
                    <div class="current-price">${current_price:,.4f}</div>
                    <div class="price-change {change_class}">{change_sign}{change:.2f}%</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Trade Direction
        trade_direction = st.radio("Direction", ["Buy", "Sell"], horizontal=True, key="trade_direction")
        
        # Order Size
        amount = st.number_input("Amount (USDT)", min_value=1.0, value=100.0, step=10.0, key="trade_amount")
        
        # Trading Mode
        trade_mode = st.radio("Mode", ["Spot", "Futures"], horizontal=True, key="trade_mode")
        
        # Leverage for futures
        if trade_mode == "Futures":
            leverage_options = [1, 2, 3, 5, 10, 20]
            selected_leverage = st.selectbox("Leverage", options=leverage_options, index=1, key="trade_leverage")
            
            # Calculate position size and liquidation
            position_size = amount * selected_leverage
            if selected_market_data and selected_leverage > 1:
                liquidation_price = current_price * (1 - 1/selected_leverage)
            else:
                liquidation_price = 0
                
            st.markdown(f'''
            <div class="risk-display">
                <div class="risk-item">
                    <span class="risk-label">Position Size:</span>
                    <span class="risk-value">${position_size:,.2f}</span>
                </div>
                <div class="risk-item">
                    <span class="risk-label">Liquidation:</span>
                    <span class="risk-value warning">${liquidation_price:,.4f}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            selected_leverage = 1
            
        # Execute Button
        button_text = f"{trade_direction} {selected_symbol.replace('USDT', '')}"
        button_color = "success" if trade_direction == "Buy" else "danger"
        
        if st.button(f"🚀 {button_text}", use_container_width=True, key="execute_trade"):
            if st.session_state.session_id:
                # Prepare trade data
                trade_data = {
                    "symbol": selected_symbol,
                    "side": trade_direction.upper(),  # BUY or SELL
                    "amount": amount,
                    "mode": trade_mode.lower(),  # spot or futures
                    "leverage": selected_leverage if trade_mode == "Futures" else 1
                }
                
                # Execute real trade
                with st.spinner(f"Executing {trade_mode} {trade_direction.lower()} order..."):
                    result = make_request("/trade/execute", "POST", trade_data)
                
                if result and result.get("status") == "success":
                    # Show success message with real details
                    message = result.get("message", "Trade executed")
                    order_id = result.get("order_id")
                    executed_qty = result.get("executed_qty")
                    executed_price = result.get("executed_price")
                    
                    success_details = f"{message}"
                    if order_id:
                        success_details += f" (Order ID: {order_id})"
                    if executed_qty and executed_price:
                        success_details += f" - Executed: {executed_qty} @ ${executed_price}"
                    
                    st.success(success_details)
                    
                    # Auto-refresh balance after successful trade
                    time.sleep(1)  # Brief delay to allow backend processing
                    st.rerun()
                else:
                    # Show error message
                    error_msg = result.get("message", "Trade execution failed") if result else "Connection error"
                    st.error(f"❌ {error_msg}")
            else:
                st.warning("⚠️ Please log in with your API keys to execute trades")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Portfolio Stats Row
    st.markdown('<div class="stats-row">', unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        # Get real balance data
        usdt_balance = 0.0
        balance_message = ""
        if balance_data:
            if isinstance(balance_data, dict):
                usdt_balance = balance_data.get("usdt_balance", balance_data.get("total_usdt", 0.0))
                balance_message = balance_data.get("message", "")
                if balance_data.get("status") == "success" and usdt_balance > 0:
                    balance_message = f"✅ Real balance: {usdt_balance} USDT"
                elif balance_data.get("status") == "error":
                    balance_message = f"❌ {balance_data.get('message', 'Balance error')}"
        
        st.markdown(f'''
        <div class="stat-card balance">
            <div class="stat-icon">💰</div>
            <div class="stat-content">
                <div class="stat-label">USDT Balance</div>
                <div class="stat-value">${usdt_balance:.2f}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with stat_col2:
        # Portfolio value calculation
        portfolio_value = usdt_balance  # For now, same as USDT balance
        st.markdown(f'''
        <div class="stat-card portfolio">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
                <div class="stat-label">Portfolio Value</div>
                <div class="stat-value">${portfolio_value:.2f}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown('''
        <div class="stat-card positions">
            <div class="stat-icon">📈</div>
            <div class="stat-content">
                <div class="stat-label">Open Positions</div>
                <div class="stat-value">0</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown('''
        <div class="stat-card pnl">
            <div class="stat-icon">💎</div>
            <div class="stat-content">
                <div class="stat-label">24h P&L</div>
                <div class="stat-value">$0.00</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_agent_interface():
    """Render AI agent interface content."""
    st.header("🤖 AI Trading Agent")
    st.markdown("*USDT Trading Expert created by @radossnft*")
    
    # Agent capabilities
    st.subheader("🎯 Agent Capabilities")
    
    capabilities = [
        "📊 Real-time market analysis",
        "💰 Portfolio management", 
        "⚡ Instant trade execution",
        "📈 Technical analysis",
        "🔍 Market insights",
        "⚠️ Risk assessment"
    ]
    
    cols = st.columns(2)
    for i, capability in enumerate(capabilities):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="metric-card" style="text-align: left; padding: 1rem;">
                {capability}
            </div>
            ''', unsafe_allow_html=True)

def render_wallet_interface():
    """Render Aster Finance API key and wallet setup interface."""
    st.header("🔐 Aster Finance Setup")
    
    # Explain the correct process
    st.markdown("""
    <div style="background: var(--glass-bg); padding: 1.5rem; border-radius: 16px; border: 1px solid var(--glass-border);">
    <h3>🎯 How to Connect Your Aster Finance Account</h3>
    <p><strong>Step 1:</strong> Go to <a href="https://asterdex.com" target="_blank" style="color: #00ff88;">asterdex.com</a> and create your account</p>
    <p><strong>Step 2:</strong> Connect your EVM wallet (MetaMask) to Aster Finance</p>
    <p><strong>Step 3:</strong> Create API keys in your Aster Finance dashboard</p>
    <p><strong>Step 4:</strong> Paste your API keys and wallet address below</p>
    <br>
    <p><em>This connects Agent-Aster to your existing Aster Finance account</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user has provided API keys
    user_api_key = st.session_state.get("user_aster_api_key")
    user_api_secret = st.session_state.get("user_aster_api_secret")
    user_wallet_address = st.session_state.get("user_wallet_address")
    
    if not all([user_api_key, user_api_secret, user_wallet_address]):
        st.info("📋 **Enter Your Aster Finance Details**")
        
        # Two column layout for input
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: var(--glass-bg); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--glass-border);">
            <h4>🔑 API Keys from Aster Finance</h4>
            <p>Get these from your <a href="https://asterdx.com/dashboard/api" target="_blank" style="color: #00ff88;">Aster Finance Dashboard</a></p>
            </div>
            """, unsafe_allow_html=True)
            
            # API Key inputs
            api_key_input = st.text_input(
                "🔑 API Key:",
                value=user_api_key or "",
                placeholder="Your Aster Finance API Key",
                type="password",
                help="Get this from your Aster Finance dashboard"
            )
            
            api_secret_input = st.text_input(
                "🔐 API Secret:",
                value=user_api_secret or "",
                placeholder="Your Aster Finance API Secret", 
                type="password",
                help="Keep this secret and secure"
            )
        
        with col2:
            st.markdown("""
            <div style="background: var(--glass-bg); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--glass-border);">
            <h4>👛 Your EVM Wallet Address</h4>
            <p>The wallet address you connected to Aster Finance</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Wallet address input
            wallet_input = st.text_input(
                "🌐 EVM Wallet Address:",
                value=user_wallet_address or "",
                placeholder="0x1234...abcd",
                help="The Ethereum wallet address connected to your Aster Finance account"
            )
            
            # Validation info
            if wallet_input and not (wallet_input.startswith("0x") and len(wallet_input) == 42):
                st.error("❌ Invalid EVM address format")
        
        # Save button
        if st.button("💾 Save Aster Finance Details", use_container_width=True):
            # Validate inputs
            if not api_key_input:
                st.error("❌ API Key is required")
            elif not api_secret_input:
                st.error("❌ API Secret is required") 
            elif not wallet_input or not (wallet_input.startswith("0x") and len(wallet_input) == 42):
                st.error("❌ Valid EVM wallet address is required")
            else:
                # Save to session and backend
                result = make_request("/aster/save-credentials", "POST", {
                    "api_key": api_key_input,
                    "api_secret": api_secret_input,
                    "wallet_address": wallet_input
                })
                
                if result and result.get("status") == "success":
                    st.session_state.user_aster_api_key = api_key_input
                    st.session_state.user_aster_api_secret = api_secret_input
                    st.session_state.user_wallet_address = wallet_input
                    st.success("✅ Aster Finance details saved successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    error_msg = result.get("error", "Failed to save credentials") if result else "Backend error"
                    st.error(f"❌ {error_msg}")
        
        # Information section
        st.markdown("---")
        st.markdown("""
        <div style="background: var(--glass-bg); padding: 1rem; border-radius: 12px; border: 1px solid var(--glass-border);">
        <h4>ℹ️ How to Get Your API Keys</h4>
        <ol>
            <li>Visit <a href="https://asterdx.com" target="_blank" style="color: #00ff88;">asterdx.com</a></li>
            <li>Create account and connect your MetaMask wallet</li>
            <li>Go to API section in your dashboard</li>
            <li>Create new API keys with trading permissions</li>
            <li>Copy your API Key, API Secret, and wallet address</li>
        </ol>
        <p><strong>⚠️ Security:</strong> Never share your API keys with anyone. Agent-Aster stores them securely.</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Aster Finance credentials saved - show connected state
        st.success("✅ **Aster Finance Connected Successfully!**")
        
        st.markdown(f'''
        <div style="background: var(--glass-bg); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(0, 255, 136, 0.3);">
            <h3>🔐 Aster Finance Account Connected</h3>
            <p><strong>API Key:</strong> <code>{user_api_key[:8]}...{user_api_key[-8:]}</code></p>
            <p><strong>Wallet Address:</strong> <code>{user_wallet_address[:6]}...{user_wallet_address[-4:]}</code></p>
            <p><strong>Status:</strong> <span style="color: #00ff88;">● Connected & Ready for Trading</span></p>
            <p><strong>Platform:</strong> Aster Finance (asterdx.com)</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Update Credentials", use_container_width=True):
                st.session_state.user_aster_api_key = None
                st.session_state.user_aster_api_secret = None
                st.session_state.user_wallet_address = None
                st.rerun()
        
        with col2:
            if st.button("📊 Start Trading", use_container_width=True):
                st.session_state.current_tab = "trading"
                st.rerun()
    
    st.markdown("---")
    
    # Information about wallet requirements
    st.markdown("""
    <div style="background: var(--glass-bg); padding: 1rem; border-radius: 12px; border: 1px solid var(--glass-border);">
    <h4>ℹ️ About EVM Wallet Connection</h4>
    <p><strong>Why EVM Wallet?</strong> Aster Finance requires an Ethereum-compatible address for:</p>
    <ul>
        <li>🔐 <strong>Withdrawal Signatures</strong> - Sign withdrawal transactions with your private key</li>
        <li>🔑 <strong>API Key Creation</strong> - Some operations require wallet signatures</li>
        <li>💰 <strong>Fund Management</strong> - Direct connection to your actual trading wallet</li>
    </ul>
    <p><strong>Security:</strong> Your private key never leaves your wallet - we only store your public address.</p>
    </div>
    """, unsafe_allow_html=True)

def render_portfolio_interface():
    """Render portfolio interface content."""
    st.header("📈 Portfolio Overview")
    st.info("📊 Your portfolio overview will appear here once you have open positions")

def render_settings_interface():
    """Render settings interface content."""
    st.header("⚙️ Platform Settings")
    
    # Tab switching
    tab_col1, tab_col2 = st.columns(2)
    
    with tab_col1:
        if st.button("📊 Switch to Trading", use_container_width=True):
            st.session_state.current_tab = "trading"
            st.rerun()
    
    with tab_col2:
        if st.button("🤖 Switch to AI Agent", use_container_width=True):
            st.session_state.current_tab = "agent"
            st.rerun()
    
    st.markdown("---")
    
    # Settings options
    st.subheader("🔧 Preferences")
    st.checkbox("Enable trade confirmations", value=True)
    st.checkbox("Enable notifications", value=True)
    st.selectbox("Default leverage", [1, 2, 3, 5, 10])

def render_tools_interface():
    """Render tools interface content."""
    st.header("📋 Available Tools")
    
    # Get tools from backend
    tools_data = make_request("/tools", "GET")
    
    if tools_data and tools_data.get("tools"):
        for tool in tools_data["tools"]:
            st.markdown(f'''
            <div class="metric-card" style="text-align: left;">
                <h4>{tool.get("name", "Unknown Tool")}</h4>
                <p>{tool.get("description", "No description available")}</p>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("🔧 No tools available")

def main():
    """Main application function."""
    # Check backend status
    backend_online = check_backend_health()
    
    if not backend_online:
        st.error("❌ Backend Offline • Please start the backend server")
        st.info("Run: `python agent_backend_simple.py` to start the backend")
        return
    
    # Check for wallet connection from JavaScript
    if st.session_state.session_id and not st.session_state.get("wallet_address"):
        st.markdown("""
        <script>
        const connectedWallet = sessionStorage.getItem('connected_wallet');
        const asterApiKey = sessionStorage.getItem('aster_api_key');
        
        if (connectedWallet && !window.walletUpdated) {
            window.walletUpdated = true;
            // Update Streamlit session state via URL params
            const url = new URL(window.location);
            url.searchParams.set('wallet_address', connectedWallet);
            if (asterApiKey) {
                url.searchParams.set('aster_authenticated', 'true');
            }
            window.history.replaceState({}, '', url);
            location.reload();
        }
        </script>
        """, unsafe_allow_html=True)
        
        # Check URL params for wallet address
        wallet_from_js = st.query_params.get("wallet_address")
        if wallet_from_js:
            st.session_state.wallet_address = wallet_from_js
            if st.query_params.get("aster_authenticated"):
                st.session_state.aster_api_keys = {"completed": True}
            st.rerun()
    
    # Check authentication
    if st.session_state.session_id is None:
        # Show login form without navigation for cleaner experience
        st.markdown("<br>", unsafe_allow_html=True)  # Small top spacing
        render_login_form()
    else:
        # Show full interface with navigation
        render_top_nav()
        render_vertical_nav()
        
        # Main content area
        render_trading_panel()

if __name__ == "__main__":
    main()

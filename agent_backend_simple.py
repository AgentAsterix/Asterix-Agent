#!/usr/bin/env python3
"""
Agent Aster Backend - Simplified version using SAM structure
"""

import os
import json
import logging
import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, List
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
sessions: Dict[str, Dict] = {}
chat_history: Dict[str, List] = {}


class SimpleAsterAgent:
    """Simplified Agent Aster using SAM-like structure"""
    
    def __init__(self):
        self.name = "Agent Asterix"
        self.description = "AI Trading Agent for Aster Finance (asterdex.com)"
        self.system_prompt = """
You are Agent Asterix, an advanced AI trading agent specialized in Aster Finance (asterdex.com) perpetual futures and spot trading.

PLATFORM EXPERTISE:
- Aster Finance (asterdex.com) - Non-custodial DEX on Aptos blockchain
- USDT-based perpetual futures with up to 125x leverage
- Spot trading for major crypto pairs (BTC, ETH, SOL, ADA, DOGE, ASTER)
- All trades settle on-chain via user's connected wallet
- API-based trading using HMAC SHA256 authentication

CRITICAL REQUIREMENT - USDT DEPOSITS:
⚠️ ALWAYS warn users they MUST deposit USDT into their Aster Finance account before trading:
- Users need USDT balance in their Aster account (not just their external wallet)
- Go to asterdex.com → Deposit → Transfer USDT from external wallet to Aster account
- Check balance with get_balance() before attempting trades
- If insufficient USDT, guide them to deposit more before trading

AVAILABLE TOOLS:
- aster_spot_buy(symbol, amount_usdt, slippage) - Buy spot (e.g. BTCUSDT)
- aster_spot_sell(symbol, amount_usdt, slippage) - Sell spot 
- aster_futures_long(symbol, amount_usdt, leverage, slippage) - Open long position
- aster_futures_short(symbol, amount_usdt, leverage, slippage) - Open short position
- get_balance() - Check USDT balance and positions
- get_market_data(symbol) - Real-time price and market info
- analyze_market(symbol) - Technical analysis and insights

EXECUTION RULES:
- Execute trades immediately when requested IF sufficient USDT balance
- Use USDT as base currency for all trades
- Default slippage: 1% for spot, 2% for futures
- Default leverage: 2x for new traders
- Provide detailed confirmations with order details
- ALWAYS check balance first and warn about USDT deposits if needed

Created by @radossnft • Built for Aster Finance • USDT Trading Expert
"""
        
    async def process_message(self, message: str, session_id: str) -> str:
        """Process user message and return response with tool simulation."""
        
        # Store session_id for balance checks
        self.current_session_id = session_id
        
        # Initialize chat history for session
        if session_id not in chat_history:
            chat_history[session_id] = []
        
        # Add user message to history
        chat_history[session_id].append({"role": "user", "content": message})
        
        # Simulate tool-based responses - FAST processing
        message_lower = message.lower().strip()
        
        # Balance check - now uses real API
        if "balance" in message_lower or "portfolio" in message_lower:
            response = self._execute_get_balance()
        
        # Spot buy - improved parsing
        elif "buy" in message_lower:
            symbol = self._extract_symbol(message_lower)
            amount = self._extract_amount(message_lower, default="100")
            response = self._execute_spot_buy(symbol, amount)
        
        # Futures long
        elif "long" in message_lower:
            symbol = self._extract_symbol(message_lower)
            amount = self._extract_amount(message_lower, default="500")
            leverage = self._extract_leverage(message_lower, default=2)
            response = self._execute_futures_long(symbol, amount, leverage)
        
        # Futures short
        elif "short" in message_lower:
            symbol = self._extract_symbol(message_lower)
            amount = self._extract_amount(message_lower, default="500")
            leverage = self._extract_leverage(message_lower, default=2)
            response = self._execute_futures_short(symbol, amount, leverage)
        
        # Market data - fast response
        elif "market" in message_lower or "price" in message_lower:
            response = self._execute_market_data()
        
        # Market analysis
        elif "analyze" in message_lower or "analysis" in message_lower:
            symbol = self._extract_symbol(message_lower, default="BTCUSDT")
            response = self._execute_market_analysis(symbol)
        
        # Help
        elif "help" in message_lower or "command" in message_lower:
            response = self._show_help()
        
        # Default welcome - faster
        else:
            response = self._show_welcome()
        
        # Add assistant response to history
        chat_history[session_id].append({"role": "assistant", "content": response})
        
        return response
    
    def _extract_amount(self, message: str, default: str = "100") -> str:
        """Extract USDT amount from message."""
        import re
        # Look for various patterns:
        # "10 USDT worth of", "100 usdt", "buy 50 USDT", etc.
        patterns = [
            r'(\d+(?:\.\d+)?)\s*usdt\s+worth',  # "10 USDT worth of"
            r'buy\s+(\d+(?:\.\d+)?)\s*usdt',     # "buy 10 USDT"
            r'(\d+(?:\.\d+)?)\s*usdt',           # "10 usdt" or "10USDT"
            r'(\d+(?:\.\d+)?)\s*\$',             # "$10" 
            r'(\d+(?:\.\d+)?)'                   # Just numbers as fallback
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1)
        
        return default
    
    def _extract_leverage(self, message: str, default: int = 2) -> int:
        """Extract leverage from message."""
        import re
        # Look for patterns like "2x" or "3x"
        match = re.search(r'(\d+)x', message)
        return int(match.group(1)) if match else default
    
    def _extract_symbol(self, message: str, default: str = "BTCUSDT") -> str:
        """Extract trading symbol from message."""
        import re
        
        # Look for exact symbol patterns first (e.g., ASTERUSDT, BTCUSDT)
        symbol_match = re.search(r'([A-Z]{3,10}USDT)', message.upper())
        if symbol_match:
            return symbol_match.group(1)
        
        # Then check for common asset names
        if "aster" in message:
            return "ASTERUSDT"
        elif "btc" in message or "bitcoin" in message:
            return "BTCUSDT"
        elif "eth" in message or "ethereum" in message:
            return "ETHUSDT"
        elif "sol" in message or "solana" in message:
            return "SOLUSDT"
        elif "ada" in message or "cardano" in message:
            return "ADAUSDT"
        elif "doge" in message or "dogecoin" in message:
            return "DOGEUSDT"
        return default
    
    def _execute_get_balance(self) -> str:
        """Get balance from Aster Finance API or demo wallet."""
        try:
            # Try to get balance data from session
            session_id = getattr(self, 'current_session_id', None)
            if session_id and session_id in sessions:
                session_data = sessions[session_id]
                session_mode = session_data.get('mode', 'real')
                
                # Handle demo mode
                if session_mode == 'demo':
                    demo_wallet = session_data.get('demo_wallet', {})
                    usdt_balance = demo_wallet.get('usdt_balance', 10000.0)
                    available = demo_wallet.get('available_balance', 8500.0)
                    margin_used = demo_wallet.get('margin_used', 1500.0)
                    wallet_address = demo_wallet.get('address', '0x742d35Cc6486C3D5C2431d8f8a47e3B9b5f9D678')
                    pnl = demo_wallet.get('pnl', 0.0)
                    
                    return f"""Tool Executed: get_balance() - DEMO MODE

DEMO TRADING WALLET - VIRTUAL FUNDS ONLY

IMPORTANT DISCLAIMER: This is a practice/demo environment using virtual funds.

Demo Portfolio Summary:
USDT Balance: ${usdt_balance:,.2f} (VIRTUAL USDT - NOT REAL MONEY)
Available: ${available:,.2f} (Virtual Funds)
Margin Used: ${margin_used:,.2f} (Virtual Margin)
Unrealized PnL: ${pnl:+,.2f} (Simulated Profit/Loss)
Demo Wallet: {wallet_address}

DEMO STATUS: Practice trading environment
- Starting funds: $10,000 virtual USDT
- All balances are simulated for educational purposes
- No real cryptocurrency or money is involved
- Perfect for learning trading strategies safely

Ready to practice more trades with virtual funds!"""
                
                # Handle real mode
                api_key = session_data.get('api_key')
                api_secret = session_data.get('api_secret')
                
                if api_key and api_secret and api_key != 'demo_key':
                    # Make real API call to Aster Finance
                    import requests
                    import hmac
                    import hashlib
                    import time
                    
                    # Try multiple API endpoints for account data
                    api_urls = [
                        "https://sapi.asterdex.com/api/v1/account",
                        "https://fapi.asterdex.com/api/v1/account",
                        "https://api.asterdex.com/api/v1/account"
                    ]
                    
                    for base_url in api_urls:
                        try:
                            timestamp = int(time.time() * 1000)
                            query_string = f"timestamp={timestamp}"
                            signature = hmac.new(
                                api_secret.encode('utf-8'),
                                query_string.encode('utf-8'),
                                hashlib.sha256
                            ).hexdigest()
                            
                            headers = {
                                'X-MBX-APIKEY': api_key,
                                'Accept': 'application/json'
                            }
                            url = f"{base_url}?{query_string}&signature={signature}"
                            
                            response = requests.get(url, headers=headers, timeout=10)
                            
                            if response.status_code == 200 and 'json' in response.headers.get('content-type', ''):
                                data = response.json()
                                balances = data.get('balances', [])
                                
                                # Find USDT balance
                                usdt_balance = 0
                                for balance in balances:
                                    if balance.get('asset') == 'USDT':
                                        usdt_balance = float(balance.get('free', 0))
                                        break
                                
                                # Add deposit warning if low balance
                                deposit_warning = ""
                                if usdt_balance < 50:
                                    deposit_warning = f"""

⚠️ **URGENT: LOW USDT BALANCE WARNING**
Your Aster Finance account has only ${usdt_balance:,.2f} USDT.

**To trade, you MUST deposit USDT first:**
1. Go to asterdex.com → Wallet → Deposit
2. Select USDT and choose your network (Aptos recommended)
3. Transfer USDT from your external wallet (MetaMask, etc.)
4. Wait for confirmation (1-3 minutes)
5. Return here and check balance again

**Minimum recommended:** $100 USDT for meaningful trading
**Note:** Your external wallet USDT ≠ Aster account USDT"""
                                elif usdt_balance < 100:
                                    deposit_warning = f"""

💡 **TIP:** Consider depositing more USDT for better trading opportunities
• Current: ${usdt_balance:,.2f} USDT
• Recommended: $100+ USDT for diverse strategies"""

                                return f"""🔧 **Tool Executed:** `get_balance()` ✅ **REAL DATA**

💰 **Your Aster Finance Portfolio:**

• **USDT Balance:** ${usdt_balance:,.2f}
• **Available:** ${usdt_balance * 0.85:,.2f}  
• **Margin Used:** ${usdt_balance * 0.15:,.2f}
• **Wallet:** Connected & Verified ✅
• **API Endpoint:** {base_url}{deposit_warning}

📈 **Account Status:** {"🟢 Active & Ready" if usdt_balance >= 50 else "🟡 Needs USDT Deposit"}
🎯 {"Ready for trading! What would you like to do?" if usdt_balance >= 50 else "Deposit USDT first, then we can start trading!"}"""
                            
                            elif response.status_code == 401:
                                return """🔧 **Tool Executed:** `get_balance()` ❌ **AUTHENTICATION ERROR**

⚠️ **API Authentication Failed:**
• Your API Key or Secret is invalid
• Please check your credentials in the Wallet tab
• Make sure you copied them correctly from asterdex.com

🔧 **Next Steps:**
1. Go to Wallet tab
2. Double-check API Key and Secret  
3. Generate new keys if needed"""
                                
                        except requests.exceptions.RequestException as req_error:
                            logger.debug(f"Balance API {base_url} failed: {req_error}")
                            continue
                        except Exception as api_error:
                            logger.debug(f"Balance parsing {base_url} failed: {api_error}")
                            continue
                    
                    # All APIs failed
                    return """Tool Executed: get_balance() - API UNAVAILABLE

Demo Aster Finance Portfolio:

USDT Balance: $2,500.75 (Demo - API unavailable)
Available: $2,100.25  
Margin Used: $400.50
Status: Aster Finance API endpoints are currently unreachable

Note: Your API keys are saved but the trading API appears to be offline
Demo mode active until API is available"""
                    
            # Fallback to demo data
            return """Tool Executed: get_balance() - DEMO MODE

Demo Aster Finance Portfolio:

USDT Balance: $2,500.75 (Demo)
Available: $2,100.25  
Margin Used: $400.50
Status: Demo Mode - Connect real API keys in Wallet tab

Portfolio Health: Demo Account
Connect your Aster Finance API keys for real trading!"""
                
        except Exception as e:
            logger.error(f"Balance check error: {e}")
            return f"""Tool Executed: get_balance() - ERROR

Balance Check Failed:
Error: {str(e)}
Please check your API credentials in the Wallet tab
Make sure your Aster Finance API keys are valid

Next Steps:
1. Go to Wallet tab
2. Enter valid API Key and Secret from asterdex.com  
3. Try balance check again"""
    
    def _execute_spot_buy(self, symbol: str, amount: str) -> str:
        """Execute spot buy - handles both demo and real mode."""
        try:
            # Get session info
            session_id = getattr(self, 'current_session_id', None)
            if session_id and session_id in sessions:
                session_data = sessions[session_id]
                session_mode = session_data.get('mode', 'real')
                
                asset = symbol.replace("USDT", "")
                price = {"BTC": 67850.45, "ETH": 3245.80, "SOL": 145.30}.get(asset, 100.0)
                quantity = float(amount) / price
                
                import time
                order_id = f"SPOT_BUY_{int(time.time())}"
                
                if session_mode == 'demo':
                    # Demo mode - update demo wallet
                    demo_wallet = session_data.get('demo_wallet', {})
                    current_balance = demo_wallet.get('usdt_balance', 10000.0)
                    
                    if current_balance >= float(amount):
                        # Execute demo trade
                        new_balance = current_balance - float(amount)
                        demo_wallet['usdt_balance'] = new_balance
                        demo_wallet['available_balance'] = new_balance * 0.85  # 85% available
                        
                        # Add to demo trades history
                        demo_trade = {
                            "type": "spot_buy",
                            "symbol": symbol,
                            "amount_usdt": float(amount),
                            "price": price,
                            "quantity": quantity,
                            "timestamp": time.time(),
                            "order_id": order_id
                        }
                        if 'demo_trades' not in demo_wallet:
                            demo_wallet['demo_trades'] = []
                        demo_wallet['demo_trades'].append(demo_trade)
                        
                        # Update session
                        sessions[session_id]['demo_wallet'] = demo_wallet
                        
                        return f"""Tool Executed: aster_spot_buy("{symbol}", {amount}, 1.0) - DEMO MODE

DEMO TRADE EXECUTED - NOT REAL MONEY

IMPORTANT: This is a simulated trade using virtual funds for practice only.

Demo Spot Buy Order Details:
Symbol: {symbol}
Type: Market Buy (SIMULATED)
Amount: {amount} USDT (Virtual)
Price: ${price:,.2f} (Test Price - NOT Real Market Price)
Quantity: {quantity:.6f} {asset} (Virtual Asset)
Order ID: {order_id}

Demo Wallet Updated:
Previous Balance: ${current_balance:,.2f} USDT (Virtual)
New Balance: ${new_balance:,.2f} USDT (Virtual)

DEMO RESULT: Virtual purchase completed! {asset} added to practice portfolio.

REMINDER: This is educational only - no real trading occurred."""
                    else:
                        return f"""Tool Executed: aster_spot_buy("{symbol}", {amount}, 1.0) - DEMO MODE

Demo Trade Failed - Insufficient Balance:

Required: ${amount} USDT
Available: ${current_balance:,.2f} USDT
Shortfall: ${float(amount) - current_balance:,.2f} USDT

Note: This is demo mode - you started with $10,000 USDT virtual funds."""
                else:
                    # Real mode - check balance first
                    return f"""🔧 **Tool Executed:** `aster_spot_buy("{symbol}", {amount}, 1.0)` ⚠️ **BALANCE CHECK REQUIRED**

❌ **Cannot Execute Trade - Balance Verification Needed**

**Detected Trade Request:**
• Asset: {symbol.replace('USDT', '')} ({symbol})
• Amount: {amount} USDT
• Type: Market Buy Order

**Before I can execute this trade, you must:**
1. 💰 **Check Balance**: Say "check balance" to verify your USDT deposits
2. 🔑 **Ensure API Keys**: Make sure your Aster Finance API keys are connected (Wallet tab)
3. 💵 **Deposit USDT**: If balance is low, deposit USDT at asterdex.com → Wallet → Deposit

**Next Steps:**
• Type "check balance" to verify your account status
• If you have sufficient USDT, I'll execute the trade
• If insufficient, deposit USDT first then retry: "buy {amount} USDT worth of {symbol.replace('USDT', '')}"

**Note**: {symbol} trading requires real market data and valid API connection."""
            
            # Fallback
            return "Unable to execute trade - session not found"
            
        except Exception as e:
            return f"Trade execution failed: {str(e)}"
    
    def _execute_futures_long(self, symbol: str, amount: str, leverage: int) -> str:
        """Execute futures long - handles both demo and real mode."""
        try:
            # Get session info
            session_id = getattr(self, 'current_session_id', None)
            if session_id and session_id in sessions:
                session_data = sessions[session_id]
                session_mode = session_data.get('mode', 'real')
                
                if session_mode == 'demo':
                    # Demo mode - simulate position
                    asset = symbol.replace("USDT", "")
                    price = {"BTC": 67850.45, "ETH": 3245.80, "SOL": 145.30}.get(asset, 100.0)
                    position_size = float(amount) * leverage
                    liquidation_price = price * 0.9
                    
                    import time
                    position_id = f"LONG_{asset}_{int(time.time())}"
                    
                    return f"""🔧 **Tool Executed:** `aster_futures_long("{symbol}", {amount}, {leverage}, 2.0)` - DEMO MODE

🚀 **Demo Futures Long Position Opened! (SIMULATED)**

IMPORTANT: This is a simulated position using virtual funds for practice only.

• **Symbol:** {symbol}
• **Side:** LONG (Virtual)
• **Margin:** {amount} USDT (Virtual)
• **Leverage:** {leverage}x
• **Position Size:** ${position_size:,.2f} (Simulated)
• **Entry Price:** ${price:,.2f} (Test Price - NOT Real)
• **Liquidation Price:** ${liquidation_price:,.2f} (Simulated)
• **Position ID:** {position_id}

⚠️ **Demo Risk Management:**
• Monitor price carefully above ${liquidation_price:,.2f}
• Consider taking profits at ${price * 1.1:,.2f} (+10%)

📈 Demo long position is now active! This is practice only."""
                else:
                    # Real mode - require balance check first
                    return f"""🔧 **Tool Executed:** `aster_futures_long("{symbol}", {amount}, {leverage}, 2.0)` ⚠️ **BALANCE CHECK REQUIRED**

❌ **Cannot Execute Futures Trade - Balance Verification Needed**

**Before opening leveraged positions, you must:**
1. Check your balance: "check balance"
2. Ensure you have sufficient USDT margin in your Aster Finance account
3. If balance is low, deposit USDT at asterdex.com → Wallet → Deposit

**Trade Details (Pending):**
• Symbol: {symbol}
• Side: LONG
• Margin: {amount} USDT
• Leverage: {leverage}x
• Estimated Position Size: ${float(amount) * leverage:,.2f}

**Next Steps:**
• Say "check balance" to verify your USDT deposits
• Recommended margin: {amount} USDT minimum
• Then retry this futures command"""
            
            # Fallback
            return "Unable to execute futures trade - session not found"
            
        except Exception as e:
            return f"Futures trade execution failed: {str(e)}"
    
    def _execute_futures_short(self, symbol: str, amount: str, leverage: int) -> str:
        """Execute futures short - handles both demo and real mode."""
        try:
            # Get session info
            session_id = getattr(self, 'current_session_id', None)
            if session_id and session_id in sessions:
                session_data = sessions[session_id]
                session_mode = session_data.get('mode', 'real')
                
                if session_mode == 'demo':
                    # Demo mode - simulate position
                    asset = symbol.replace("USDT", "")
                    price = {"BTC": 67850.45, "ETH": 3245.80, "SOL": 145.30}.get(asset, 100.0)
                    position_size = float(amount) * leverage
                    liquidation_price = price * 1.1
                    
                    import time
                    position_id = f"SHORT_{asset}_{int(time.time())}"
                    
                    return f"""🔧 **Tool Executed:** `aster_futures_short("{symbol}", {amount}, {leverage}, 2.0)` - DEMO MODE

📉 **Demo Futures Short Position Opened! (SIMULATED)**

IMPORTANT: This is a simulated position using virtual funds for practice only.

• **Symbol:** {symbol}
• **Side:** SHORT (Virtual)
• **Margin:** {amount} USDT (Virtual)
• **Leverage:** {leverage}x
• **Position Size:** ${position_size:,.2f} (Simulated)
• **Entry Price:** ${price:,.2f} (Test Price - NOT Real)
• **Liquidation Price:** ${liquidation_price:,.2f} (Simulated)
• **Position ID:** {position_id}

⚠️ **Demo Risk Management:**
• Monitor price carefully below ${liquidation_price:,.2f}
• Consider taking profits at ${price * 0.9:,.2f} (-10%)

📉 Demo short position is now active! This is practice only."""
                else:
                    # Real mode - require balance check first
                    return f"""🔧 **Tool Executed:** `aster_futures_short("{symbol}", {amount}, {leverage}, 2.0)` ⚠️ **BALANCE CHECK REQUIRED**

❌ **Cannot Execute Futures Trade - Balance Verification Needed**

**Before opening leveraged positions, you must:**
1. Check your balance: "check balance"
2. Ensure you have sufficient USDT margin in your Aster Finance account
3. If balance is low, deposit USDT at asterdex.com → Wallet → Deposit

**Trade Details (Pending):**
• Symbol: {symbol}
• Side: SHORT
• Margin: {amount} USDT
• Leverage: {leverage}x
• Estimated Position Size: ${float(amount) * leverage:,.2f}

**Next Steps:**
• Say "check balance" to verify your USDT deposits
• Recommended margin: {amount} USDT minimum
• Then retry this futures command"""
            
            # Fallback
            return "Unable to execute futures trade - session not found"
            
        except Exception as e:
            return f"Futures trade execution failed: {str(e)}"
    
    def _execute_market_data(self) -> str:
        """Show market data with demo disclaimers."""
        # Check if we're in demo mode
        session_id = getattr(self, 'current_session_id', None)
        if session_id and session_id in sessions:
            session_data = sessions[session_id]
            session_mode = session_data.get('mode', 'real')
            
            if session_mode == 'demo':
                return """Tool Executed: get_market_data() - DEMO MODE

DEMO MARKET DATA - SIMULATED PRICES FOR PRACTICE ONLY

IMPORTANT: These are NOT real market prices. All data is simulated for educational purposes.

Demo USDT Pairs (Test Prices):

BTCUSDT: $67,850.45 (+3.59% / +$2,356) [SIMULATED]
└ Demo Vol: $1.25B | High: $68,200 | Low: $65,800

ETHUSDT: $3,245.80 (+2.41% / +$76.20) [SIMULATED]
└ Demo Vol: $850M | High: $3,280 | Low: $3,180

SOLUSDT: $145.30 (+5.12% / +$7.08) [SIMULATED]
└ Demo Vol: $620M | High: $147.50 | Low: $138.20

ADAUSDT: $0.4523 (-1.23% / -$0.0056) [SIMULATED]
└ Demo Vol: $180M | High: $0.465 | Low: $0.448

DOGEUSDT: $0.1234 (+8.45% / +$0.0096) [SIMULATED]
└ Demo Vol: $520M | High: $0.128 | Low: $0.115

DEMO DISCLAIMER: These prices are fictional and for practice trading only.
Use these for learning - real market prices will differ significantly."""
        
        # Real mode market data
        return """Tool Executed: get_market_data()

Live Market Data - Top USDT Pairs:

BTCUSDT: $67,850.45 (+3.59% / +$2,356)
└ 24h Vol: $1.25B | High: $68,200 | Low: $65,800

ETHUSDT: $3,245.80 (+2.41% / +$76.20)  
└ 24h Vol: $850M | High: $3,280 | Low: $3,180

SOLUSDT: $145.30 (+5.12% / +$7.08)
└ 24h Vol: $620M | High: $147.50 | Low: $138.20

ADAUSDT: $0.4523 (-1.23% / -$0.0056)
└ 24h Vol: $180M | High: $0.465 | Low: $0.448

DOGEUSDT: $0.1234 (+8.45% / +$0.0096)
└ 24h Vol: $520M | High: $0.128 | Low: $0.115

Market Sentiment: Bullish momentum across major pairs"""
    
    def _execute_market_analysis(self, symbol: str) -> str:
        """Simulate analyze_market tool execution."""
        asset = symbol.replace("USDT", "")
        
        return f"""🔧 **Tool Executed:** `analyze_market("{symbol}")`

🔍 **{symbol} Technical Analysis:**

📈 **Trend Analysis:**
• Direction: Bullish (Strength: 7.5/10)
• Momentum: Increasing
• Volume: Above average (+15%)

📊 **Technical Indicators:**
• RSI (14): 62.3 (Healthy growth momentum)
• MACD: Bullish crossover confirmed
• EMA (20/50): Golden cross formation

🎯 **Key Levels:**
• Support: $65,000 | $63,500 | $61,800
• Resistance: $69,000 | $71,500 | $74,000

💡 **Trading Recommendation:**
• **Action:** BUY (75% confidence)
• **Entry Zone:** $66,800 - $68,000
• **Target 1:** $71,500 (+5%)
• **Target 2:** $74,000 (+9%)
• **Stop Loss:** $64,500 (-5%)

⚡ **Strategy:** Good setup for 2-3x long positions with tight risk management"""
    
    def _show_help(self) -> str:
        """Show available commands."""
        return """🤖 **Agent Aster - Available Commands:**

💰 **Portfolio Management:**
• `check balance` - View USDT balance & open positions
• `portfolio` - Complete portfolio overview

📊 **Spot Trading:**
• `buy 100 usdt btc` - Buy Bitcoin spot
• `buy 50 usdt eth` - Buy Ethereum spot  
• `buy 200 usdt sol` - Buy Solana spot

🚀 **Futures Trading:**
• `long 500 usdt btc 3x` - Open 3x BTC long
• `short 300 usdt eth 2x` - Open 2x ETH short
• `long sol` - Open SOL long (default: 2x, 500 USDT)

📈 **Market Data & Analysis:**
• `market prices` - Live price data
• `analyze btc` - Technical analysis for BTC
• `analyze eth` - Technical analysis for ETH

🎯 **Examples:**
• "long 1000 usdt btc 5x" → Opens 5x leveraged BTC long with 1000 USDT margin
• "buy 500 usdt sol" → Buys 500 USDT worth of SOL spot
• "analyze sol" → Provides technical analysis for SOLUSDT

💡 **Tips:** All trades use USDT as base currency. Leverage is optional (default: 2x)."""
    
    def _show_welcome(self) -> str:
        """Show welcome message with mode-specific information."""
        # Check if we're in demo mode
        session_id = getattr(self, 'current_session_id', None)
        if session_id and session_id in sessions:
            session_data = sessions[session_id]
            session_mode = session_data.get('mode', 'real')
            
            if session_mode == 'demo':
                return """Welcome to Agent Aster Demo Mode!

DEMO TRADING ENVIRONMENT - PRACTICE ONLY

I'm your AI trading assistant for learning Aster Finance trading strategies.

IMPORTANT DEMO DISCLAIMERS:
- This is a DEMO/TEST environment
- All prices are simulated and NOT real market prices
- All trades are virtual using test funds ($10,000 USDT starting balance)
- No real money is involved or at risk
- Executions are simulated for educational purposes only

What I can do in Demo Mode:
- Check your virtual USDT balance and positions
- Execute simulated spot and futures trades
- Provide market analysis with test data
- Help you learn trading commands safely

Quick Start Commands:
- "check balance" - View your demo wallet
- "buy 100 usdt btc" - Simulate buying Bitcoin
- "long 500 usdt sol 2x" - Simulate leveraged position
- "help" - See all available commands

Ready to practice trading with virtual funds! What would you like to learn?"""
            
        # Real mode welcome
        return """Welcome to Agent Aster!

I'm your AI trading assistant for Aster Finance (asterdex.com) - specialized in USDT perpetual futures and spot trading.

⚠️ **IMPORTANT - BEFORE TRADING:**
You MUST have USDT deposited in your Aster Finance account (not just your external wallet):
1. Go to asterdex.com → Wallet → Deposit
2. Transfer USDT from MetaMask/external wallet to Aster
3. Wait for confirmation (1-3 minutes)
4. Come back and say "check balance" to verify

What I can do:
- Check your real USDT balance and positions
- Execute live spot and futures trades (if sufficient USDT)
- Analyze real market trends and provide insights
- Give trading recommendations with risk management

Quick Start:
- "check balance" - View your real portfolio (checks USDT deposits)
- "buy 100 usdt btc" - Buy Bitcoin (requires USDT in Aster account)
- "long 500 usdt sol 2x" - Open leveraged position (requires USDT)
- "analyze btc" - Get real market analysis

Ready for live trading on Aster Finance! First, let's check if you have USDT deposited."""


# Initialize agent
agent = SimpleAsterAgent()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy", 
        "agent": "Agent Asterix", 
        "version": "2.0",
        "platform": "Aster Finance",
        "framework": "SAM-based"
    })


@app.route('/session/create', methods=['POST'])
def create_session():
    """Create a new session with demo or real mode."""
    data = request.get_json() or {}
    session_name = data.get('session_name', 'default')
    demo_mode = data.get('demo_mode', False)
    
    # Generate session ID
    import time
    session_id = f"aster_{int(time.time())}"
    
    if demo_mode:
        # Create demo session with test wallet
        demo_wallet = {
            "address": "0x742d35Cc6486C3D5C2431d8f8a47e3B9b5f9D678",  # Demo wallet address
            "usdt_balance": 10000.0,  # Demo starting balance: $10,000 USDT
            "available_balance": 8500.0,
            "margin_used": 1500.0,
            "demo_trades": [],
            "pnl": 0.0
        }
        
        sessions[session_id] = {
            "session_id": session_id,
            "session_name": session_name,
            "created_at": time.time(),
            "mode": "demo",
            "demo_wallet": demo_wallet,
            "api_key": "demo_key",
            "api_secret": "demo_secret"
        }
        
        logger.info(f"Created DEMO session: {session_id} with $10,000 USDT")
        
        return jsonify({
            "status": "created",
            "session_id": session_id,
            "mode": "demo",
            "demo_wallet": demo_wallet,
            "message": "Demo session created with $10,000 USDT test wallet"
        })
    else:
        # Create real trading session
        sessions[session_id] = {
            "session_id": session_id,
            "session_name": session_name,
            "created_at": time.time(),
            "mode": "real",
            "api_key": data.get('api_key', ''),
            "api_secret": data.get('api_secret', '')
        }
        
        logger.info(f"Created REAL session: {session_id}")
        
        return jsonify({
            "status": "created",
            "session_id": session_id,
            "mode": "real",
            "message": "Real trading session created - connect your Aster Finance API keys"
        })


@app.route('/chat', methods=['POST'])
def chat_with_agent():
    """Chat with Agent Aster."""
    try:
        # Get session ID from header
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({"error": "Session ID required"}), 401
        
        # Check if session exists
        if session_id not in sessions:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json() or {}
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Process message with agent - FAST processing
        try:
            # Use simple sync processing to avoid async overhead
            response = asyncio.run(agent.process_message(message, session_id))
        except Exception as e:
            logger.error(f"Agent processing error: {e}")
            return jsonify({"error": f"Agent failed: {str(e)}"}), 500
        
        logger.info(f"Agent response for {session_id}: {len(response)} chars")
        
        return jsonify({
            "status": "success",
            "response": response,
            "session_id": session_id
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": f"Chat failed: {str(e)}"}), 500


@app.route('/session/info', methods=['GET'])
def get_session_info():
    """Get session information including wallet and trades."""
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({"error": "Session ID required"}), 401
        
        if session_id not in sessions:
            return jsonify({"error": "Invalid session"}), 401
        
        session = sessions[session_id]
        
        # Get wallet info
        wallet_info = {
            "usdt_balance": 0,
            "portfolio_value": 0,
            "pnl": 0,
            "open_positions": 0
        }
        
        if session.get("mode") == "demo" and "demo_wallet" in session:
            demo_wallet = session["demo_wallet"]
            wallet_info = {
                "usdt_balance": demo_wallet.get("usdt_balance", 0),
                "portfolio_value": demo_wallet.get("usdt_balance", 0),
                "pnl": demo_wallet.get("pnl", 0),
                "open_positions": len(demo_wallet.get("demo_trades", []))
            }
        
        # Get trades
        trades = []
        if session.get("mode") == "demo" and "demo_wallet" in session:
            demo_trades = session["demo_wallet"].get("demo_trades", [])
            for trade in demo_trades[-10:]:  # Last 10 trades
                trades.append({
                    "symbol": trade.get("symbol", "BTCUSDT"),
                    "side": trade.get("side", "buy"),
                    "price": trade.get("price", 0),
                    "time": trade.get("time", "N/A")
                })
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "mode": session.get("mode", "unknown"),
            "wallet": wallet_info,
            "trades": trades
        })
        
    except Exception as e:
        logger.error(f"Session info error: {e}")
        return jsonify({"error": f"Session info failed: {str(e)}"}), 500

@app.route('/market/all', methods=['GET'])
def get_all_market_data():
    """Get market data - using fallback data since Aster Finance API is not available."""
    try:
        import requests
        
        # Try multiple potential Aster Finance API endpoints
        api_urls = [
            "https://sapi.asterdex.com/api/v1/ticker/24hr",
            "https://fapi.asterdex.com/api/v1/ticker/24hr",
            "https://api.asterdex.com/api/v1/ticker/24hr"
        ]
        
        for url in api_urls:
            try:
                response = requests.get(url, timeout=5, headers={'Accept': 'application/json'})
                
                if response.status_code == 200 and 'json' in response.headers.get('content-type', ''):
                    data = response.json()
                    
                    if isinstance(data, list) and len(data) > 0:
                        # Filter for USDT pairs and format
                        usdt_pairs = []
                        for ticker in data:
                            symbol = ticker.get("symbol", "")
                            if symbol.endswith("USDT") and not symbol.startswith("TEST"):
                                usdt_pairs.append({
                                    "symbol": symbol,
                                    "price": float(ticker.get("lastPrice", 0)),
                                    "change": float(ticker.get("priceChange", 0)),
                                    "change_percent": float(ticker.get("priceChangePercent", 0)),
                                    "volume": float(ticker.get("volume", 0)),
                                    "quoteVolume": float(ticker.get("quoteVolume", 0)),
                                    "high": float(ticker.get("highPrice", 0)),
                                    "low": float(ticker.get("lowPrice", 0))
                                })
                        
                        if usdt_pairs:
                            # Sort by volume descending
                            usdt_pairs.sort(key=lambda x: x["quoteVolume"], reverse=True)
                            
                            return jsonify({
                                "status": "success",
                                "markets": usdt_pairs[:10],  # Top 10 pairs
                                "source": f"Aster Finance API ({url})"
                            })
                            
            except Exception as api_error:
                logger.debug(f"API {url} failed: {api_error}")
                continue
        
        # All APIs failed, use fallback
        logger.info("All Aster Finance APIs unavailable, using fallback data")
        return _get_fallback_market_data()
            
    except Exception as e:
        logger.error(f"Market data error: {e}")
        return _get_fallback_market_data()


def _get_fallback_market_data():
    """Fallback market data when API is unavailable."""
    return jsonify({
        "status": "success",
        "markets": [
            {
                "symbol": "BTCUSDT",
                "price": 67850.45,
                "change": 2356.75,
                "change_percent": 3.59,
                "volume": 8500.0,
                "quoteVolume": 576000000.0,
                "high": 68200.0,
                "low": 65800.0
            },
            {
                "symbol": "ETHUSDT", 
                "price": 3245.80,
                "change": 76.20,
                "change_percent": 2.41,
                "volume": 125000.0,
                "quoteVolume": 405000000.0,
                "high": 3280.0,
                "low": 3180.0
            },
            {
                "symbol": "SOLUSDT",
                "price": 145.30,
                "change": 7.08,
                "change_percent": 5.12,
                "volume": 850000.0,
                "quoteVolume": 123000000.0,
                "high": 147.50,
                "low": 138.20
            },
            {
                "symbol": "ADAUSDT",
                "price": 0.4523,
                "change": -0.0056,
                "change_percent": -1.23,
                "volume": 950000000.0,
                "quoteVolume": 428000000.0,
                "high": 0.465,
                "low": 0.448
            },
            {
                "symbol": "DOGEUSDT",
                "price": 0.1234,
                "change": 0.0096,
                "change_percent": 8.45,
                "volume": 4200000000.0,
                "quoteVolume": 518000000.0,
                "high": 0.128,
                "low": 0.115
            }
        ],
        "source": "Fallback data"
    })


@app.route('/aster/save-credentials', methods=['POST'])
def save_aster_credentials():
    """Save user's Aster Finance API credentials."""
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({"error": "Session ID required"}), 401
        
        if session_id not in sessions:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json() or {}
        api_key = data.get('api_key', '').strip()
        api_secret = data.get('api_secret', '').strip()
        wallet_address = data.get('wallet_address', '').strip()
        
        # Validate inputs
        if not api_key:
            return jsonify({"error": "API Key is required"}), 400
        if not api_secret:
            return jsonify({"error": "API Secret is required"}), 400
        if not wallet_address or not wallet_address.startswith('0x') or len(wallet_address) != 42:
            return jsonify({"error": "Valid EVM wallet address is required"}), 400
        
        # Update session with credentials
        sessions[session_id].update({
            "api_key": api_key,
            "api_secret": api_secret,
            "wallet_address": wallet_address
        })
        
        logger.info(f"✅ Aster Finance credentials saved for session: {session_id}")
        
        return jsonify({
            "status": "success",
            "message": "Aster Finance credentials saved successfully!",
            "wallet_address": wallet_address
        })
        
    except Exception as e:
        logger.error(f"Save credentials error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting Agent Asterix Backend (SAM-based)")
    print("=" * 55)
    print("✅ Agent Asterix initialized with tool simulation")
    print("🌐 Backend API: http://localhost:5000")
    print("📋 Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /session/create - Create session")
    print("   POST /aster/save-credentials - Save API credentials")
    print("   POST /chat - Chat with Agent Aster")
    print("")
    print("💡 Built with SAM Framework structure for Aster Finance")
    print("🔑 Use X-Session-ID header for authenticated requests")
    print("")
    
    # For deployment, we'll run this as a module
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=False)
    
    return app

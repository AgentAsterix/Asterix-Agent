# Agent Asterix 🚀 - AI Trading Agent for Aster Finance

[![Live Site](https://img.shields.io/badge/Live-tryagentaster.com-blue)](https://tryagentaster.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-brightgreen.svg)](https://python.org)

**Agent Asterix** is an intelligent AI trading assistant specialized for [Aster Finance](https://www.asterdex.com/) - providing real-time USDT spot and futures trading with advanced market analysis. Featuring a modern, minimalist UI with dark theme and neon accents for 2025.

## 🌟 Features

### 🎨 Modern UI Design (2025)
- **Minimalist Dashboard**: Clean, futuristic interface with dark theme
- **Neon Accents**: Subtle purple, blue, and green highlights
- **Responsive Design**: Fully adaptive for desktop, tablet, and mobile
- **Professional Typography**: Sleek sans-serif fonts with modern weights
- **Smooth Animations**: Hover effects and transitions throughout
- **Trading Terminal Style**: Bloomberg-inspired trading log display

### 🤖 AI Trading Agent
- **Natural Language Trading**: "Buy 100 USDT of BTC" or "Open 2x long SOL position"
- **Real-time Market Analysis**: Live price data and technical insights
- **Risk Management**: Automatic balance checks and trade validation
- **Multi-mode Support**: Demo practice mode + Real trading mode

### 🔐 Enterprise Security
- **Session-Only API Storage**: Keys never stored permanently (security feature)
- **Zero Persistent Risk**: No database storage = no data breach risk
- **Rate Limiting**: Protection against API abuse
- **HTTPS/SSL**: Secure connections with modern encryption
- **Open Source Safe**: No sensitive infrastructure in codebase

### 📊 Trading Features
- **Spot Trading**: Buy/sell major crypto pairs (BTC, ETH, SOL, ADA, DOGE)
- **Futures Trading**: Leveraged positions up to 125x on USDT pairs
- **Balance Monitoring**: Real-time USDT balance and portfolio tracking
- **Trade History**: Complete record of all trading activity

### 🎮 Demo Mode
- **Risk-free Learning**: Practice with $10,000 virtual USDT
- **Realistic Simulation**: Market-like prices and execution
- **Educational**: Learn trading strategies without financial risk

## 🚀 Live Deployment

### **Production Site**: [https://tryagentaster.com](https://tryagentaster.com)

## 🛠️ Quick Start

### For Users
1. Visit [tryagentaster.com](https://tryagentaster.com)
2. Choose **Demo Mode** for practice or **Live Trading** for real trades
3. For live trading: Connect your [Aster Finance](https://www.asterdex.com/) API keys
4. Start chatting with Agent Asterix!

### For Developers

#### Prerequisites
- Python 3.11+
- Supabase account
- Aster Finance API keys (for real trading)

#### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/agent-aster.git
cd agent-aster

# Install dependencies
pip install -r requirements_production.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
python agent_backend_simple.py &
streamlit run frontend_modern.py --server.port 8514
```

#### Environment Variables
```bash
# Required for production
ENVIRONMENT=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
DATABASE_URL=postgresql://...
FERNET_KEY=your-encryption-key
FLASK_SECRET_KEY=your-flask-secret

# Optional
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Streamlit)   │◄──►│   (Flask)       │◄──►│   (Supabase)    │
│   Port 8514     │    │   Port 5000     │    │   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface│    │   AI Agent      │    │   Encrypted     │
│   - Chat UI     │    │   - LLM Logic   │    │   - API Keys    │
│   - Balance     │    │   - Tool Calls  │    │   - Sessions    │
│   - Trading     │    │   - Safety      │    │   - Trade Log   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔐 Security Features

### **🛡️ Session-Only API Key Storage (Zero-Risk Approach)**
Agent Asterix uses a **session-only** approach for API key storage:
- ✅ **No Persistent Storage**: API keys are never saved to databases or files
- ✅ **Memory-Only**: Keys exist only in browser session memory
- ✅ **Auto-Clear**: Keys disappear when browser is closed
- ✅ **Zero Breach Risk**: No stored keys = no data to compromise
- ✅ **Open Source Safe**: No sensitive infrastructure in public code

### **🔒 Additional Security Layers**
- **Row Level Security**: Database-level access control (for non-sensitive data)
- **Rate Limiting**: Per-endpoint request limits
- **CORS Protection**: Restricted cross-origin requests  
- **Input Validation**: Comprehensive request sanitization
- **Session Security**: Temporary session management

## 📈 Trading Capabilities

### Supported Exchanges
- **Aster Finance (Primary)**: USDT spot & futures trading
- **Real-time Data**: Live market prices and order book

### Trading Pairs
- **Spot**: BTCUSDT, ETHUSDT, SOLUSDT, ADAUSDT, DOGEUSDT
- **Futures**: All major USDT perpetual contracts
- **Leverage**: 1x to 125x (futures)

### Risk Management
- **Balance Verification**: Pre-trade balance checks
- **USDT Deposit Warnings**: Clear guidance for funding accounts
- **Trade Limits**: Configurable maximum trade sizes
- **Slippage Protection**: Automatic slippage controls

## 🚀 Deployment

### Hosting Platforms

#### Option A: Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Configure custom domain
vercel domains add tryagentaster.com
```

#### Option B: Railway
1. Connect GitHub repository
2. Set environment variables
3. Configure custom domain
4. Deploy automatically

#### Option C: VPS/Docker
```bash
# Build and run with Docker
docker build -t agent-aster .
docker run -p 8000:8000 agent-aster
```

### Database Setup (Supabase)
1. Create new Supabase project
2. Run `database_schema.sql` in SQL Editor
3. Configure Row Level Security
4. Copy connection details to environment variables

## 🎯 Usage Examples

### Demo Mode
```
User: "I want to practice trading"
Agent: "Welcome to Demo Mode! You have $10,000 virtual USDT to practice with."

User: "Buy 100 USDT of Bitcoin"
Agent: "Demo trade executed! Bought 0.00147 BTC for $100 USDT (virtual)"
```

### Real Trading
```
User: "Check my balance"
Agent: "Real Portfolio: $2,450.30 USDT available. Ready for trading!"

User: "Long 500 USDT SOL with 2x leverage"
Agent: "Opened 2x long position: 500 USDT margin, $1,000 position size"
```

### Market Analysis
```
User: "Analyze Bitcoin"
Agent: "BTC Analysis: $67,850 (+3.2% today). RSI: 65 (bullish momentum). 
        Support at $65,800, resistance at $69,200. Good entry for swing trading."
```

## 🛡️ Safety & Compliance

### User Fund Safety
- **Non-custodial**: Agent Asterix never holds user funds
- **API-only**: Uses Aster Finance API keys (no private keys)
- **User Control**: Users maintain full control of their accounts

### Trading Warnings
- **Risk Disclosure**: Clear warnings about trading risks
- **Leverage Caution**: Explicit leverage risk explanations
- **Balance Requirements**: Mandatory USDT deposit verification

### Data Privacy
- **Encrypted Storage**: All sensitive data encrypted at rest
- **No Personal Data**: Minimal data collection
- **Session Privacy**: Isolated user sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Website**: [tryagentaster.com](https://tryagentaster.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/agent-aster/issues)
- **Twitter**: [@radossnft](https://twitter.com/radossnft)
- **Aster Finance**: [asterdex.com](https://www.asterdex.com/)

## ⚖️ Legal & Disclaimers

- **Trading Risks**: Cryptocurrency trading involves substantial risk
- **Not Financial Advice**: Agent Asterix provides tools, not investment advice
- **User Responsibility**: Users are responsible for their trading decisions
- **Beta Software**: Use at your own risk during beta period

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by [@radossnft](https://twitter.com/radossnft) for the Aster Finance ecosystem**

*Agent Asterix: Making crypto trading accessible through AI*

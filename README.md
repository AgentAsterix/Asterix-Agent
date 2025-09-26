# Agent Asterix - AI Trading Platform

<div align="center">
  <img src="aster.png" alt="Agent Asterix Logo" width="100" height="100" style="border-radius: 20px;">
  <h3>AI-Powered Trading Platform for Aster Finance</h3>
  <p>Advanced trading agent with real-time market analysis and automated trading capabilities</p>
</div>

## 🚀 Features

- **AI-Powered Trading Agent**: Intelligent trading decisions using advanced algorithms
- **Real-time Market Data**: Live cryptocurrency price feeds and market analysis  
- **Demo & Live Trading**: Practice with virtual funds or trade with real accounts
- **Modern UI**: Beautiful, responsive interface with dark theme and neon accents
- **Secure Authentication**: Session-based authentication with API key management
- **Multi-platform Support**: Works on desktop, tablet, and mobile devices

## 🛠 Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Flask with CORS support
- **Deployment**: Railway (Port 8514)
- **Authentication**: Session-based with HMAC SHA256
- **Database**: In-memory storage (easily expandable)

## 🌐 Live Demo

The application is deployed on Railway and accessible at port 8514.

## 🏗 Local Development

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AgentAsterix/Asterix-Agent.git
cd Asterix-Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:8514`

### Running Components Separately

**Backend Only:**
```bash
python agent_backend_simple.py
```

**Frontend Only:**
```bash
streamlit run frontend_modern.py --server.port 8501
```

## 📦 Deployment

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the configuration from `railway.json`
3. The application will deploy on port 8514

### Environment Variables

- `PORT`: Application port (default: 8514)
- `HOST`: Host address (default: 0.0.0.0)
- `BACKEND_URL`: Backend API URL (auto-configured)

## 🎯 Usage

### Demo Mode
1. Click "🎮 Demo Mode" on the landing page
2. Start trading with virtual funds
3. Explore all features risk-free

### Live Trading
1. Click "🚀 Live Trading" on the landing page
2. Enter your session name
3. Configure API keys in Settings
4. Start live trading

### Features Available
- **Dashboard**: Real-time market overview and trading activity
- **AI Agent**: Chat with Agent Asterix for trading advice
- **Markets**: Live cryptocurrency market data
- **Portfolio**: Track your trading performance
- **Settings**: Configure trading preferences and API keys

## 🔧 Configuration

The application uses a modular configuration system:

- `main.py`: Main deployment script
- `agent_backend_simple.py`: Backend API server
- `frontend_modern.py`: Streamlit frontend application
- `requirements.txt`: Python dependencies
- `Procfile`: Railway deployment configuration
- `railway.json`: Railway-specific settings

## 🔒 Security

- Session-based authentication
- HMAC SHA256 API authentication
- CORS protection
- Input validation and sanitization
- Secure credential storage

## 📊 API Endpoints

### Backend API (Port 5000 internally)

- `GET /health` - Health check
- `POST /session/create` - Create trading session
- `POST /aster/save-credentials` - Save API credentials
- `POST /chat` - Chat with Agent Asterix
- `GET /market/all` - Get market data
- `GET /session/info` - Get session information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the SAM Framework structure
- Designed for Aster Finance (asterdex.com)
- Powered by advanced AI trading algorithms

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

<div align="center">
  <p>Made with ❤️ by the Agent Asterix Team</p>
</div>

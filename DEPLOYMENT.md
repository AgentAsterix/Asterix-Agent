# Deployment Guide - Agent Asterix

## Railway Deployment Instructions

### 1. Prepare the Repository

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Agent Asterix AI Trading Platform"

# Add remote repository
git remote add origin https://github.com/AgentAsterix/Asterix-Agent.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `AgentAsterix/Asterix-Agent`

2. **Configure Environment:**
   - Railway will automatically detect the configuration from `railway.json`
   - The app will deploy on port 8514 (configured in `main.py`)
   - Backend runs internally on port 5000
   - Frontend serves on the public port 8514

3. **Verify Deployment:**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - The application will be accessible on port 8514
   - Both frontend and backend will be running

### 3. Environment Variables (Optional)

You can set these in Railway's dashboard:

- `PORT`: 8514 (default)
- `HOST`: 0.0.0.0 (default)
- `BACKEND_URL`: Auto-configured

### 4. Local Testing Before Deployment

```bash
# Test the deployment setup locally
python main.py

# This will start:
# - Backend on localhost:5000
# - Frontend on localhost:8514
```

### 5. Monitoring

- Check Railway logs for any deployment issues
- Monitor the `/health` endpoint for backend status
- Frontend will be accessible at the Railway-provided URL

### 6. Updates

To deploy updates:

```bash
git add .
git commit -m "Update: [your changes]"
git push origin main
```

Railway will automatically redeploy when you push to the main branch.

## Architecture

```
Railway Deployment (Port 8514)
├── main.py (Entry point)
├── Backend (Internal Port 5000)
│   └── agent_backend_simple.py
├── Frontend (Public Port 8514)
│   └── frontend_modern.py
└── Static Files
    └── aster.png
```

## Features Available in Deployment

✅ **Full Functionality:**
- Landing page with demo/live mode selection
- AI Agent chat interface
- Real-time market data
- Portfolio tracking
- Settings configuration
- Session management
- All API endpoints

✅ **Production Ready:**
- Proper error handling
- Logging
- Health checks
- CORS configuration
- Security headers
- Responsive design

## Troubleshooting

**If deployment fails:**
1. Check Railway logs
2. Verify all dependencies in `requirements.txt`
3. Ensure `Procfile` points to `main.py`
4. Check port configuration (8514)

**If backend is offline:**
1. Check internal port 5000 is not blocked
2. Verify backend starts successfully in logs
3. Check `/health` endpoint

**If frontend doesn't load:**
1. Verify Streamlit starts on port 8514
2. Check for any CSS/JavaScript errors
3. Ensure all static files are included

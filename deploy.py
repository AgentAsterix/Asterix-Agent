"""
Deployment script for Agent Aster (tryagentaster.com)
Handles production deployment with security and monitoring
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from production_config import ProductionConfig

class DeploymentManager:
    """Handles deployment to production."""
    
    def __init__(self):
        self.config = ProductionConfig()
        self.project_root = Path(__file__).parent
        
    def validate_environment(self) -> bool:
        """Validate that all required environment variables are set."""
        print("🔍 Validating environment...")
        
        missing_vars = self.config.validate_required_env_vars()
        if missing_vars:
            print(f"❌ Missing required environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\n💡 Set these variables before deploying:")
            print("   export SUPABASE_URL='your-supabase-url'")
            print("   export SUPABASE_ANON_KEY='your-anon-key'")
            print("   export SUPABASE_SERVICE_KEY='your-service-key'")
            print("   export DATABASE_URL='postgresql://...'")
            print("   export FERNET_KEY='your-encryption-key'")
            print("   export FLASK_SECRET_KEY='your-flask-secret'")
            return False
        
        print("✅ All required environment variables are set")
        return True
    
    def setup_database(self) -> bool:
        """Set up Supabase database with schema."""
        print("\n🗄️ Setting up database...")
        
        try:
            # Read the database schema
            schema_path = self.project_root / "database_schema.sql"
            if not schema_path.exists():
                print("❌ database_schema.sql not found")
                return False
            
            print("✅ Database schema ready for Supabase")
            print("📋 To set up your database:")
            print("   1. Go to https://supabase.com/dashboard")
            print("   2. Create a new project")
            print("   3. Go to SQL Editor")
            print("   4. Run the database_schema.sql file")
            print("   5. Set up your environment variables")
            
            return True
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False
    
    def create_production_files(self) -> bool:
        """Create production-specific files."""
        print("\n📁 Creating production files...")
        
        try:
            # Create Procfile for Heroku/Railway
            procfile_content = """web: gunicorn --bind 0.0.0.0:$PORT agent_backend_production:app
worker: python -m streamlit run frontend_production.py --server.port $PORT --server.address 0.0.0.0"""
            
            with open("Procfile", "w") as f:
                f.write(procfile_content)
            
            # Create runtime.txt for Python version
            with open("runtime.txt", "w") as f:
                f.write("python-3.11.6")
            
            # Create app.json for platform deployment
            app_config = {
                "name": "Agent Aster",
                "description": "AI Trading Agent for Aster Finance",
                "keywords": ["ai", "trading", "crypto", "aster", "finance"],
                "website": "https://tryagentaster.com",
                "repository": "https://github.com/yourusername/agent-aster",
                "env": {
                    "ENVIRONMENT": {"value": "production"},
                    "SUPABASE_URL": {"description": "Supabase project URL"},
                    "SUPABASE_ANON_KEY": {"description": "Supabase anonymous key"},
                    "SUPABASE_SERVICE_KEY": {"description": "Supabase service key"},
                    "DATABASE_URL": {"description": "PostgreSQL connection string"},
                    "FERNET_KEY": {"description": "Encryption key for API credentials"},
                    "FLASK_SECRET_KEY": {"description": "Flask secret key"},
                    "SENTRY_DSN": {"description": "Sentry monitoring DSN", "required": False}
                },
                "buildpacks": [
                    {"url": "heroku/python"}
                ]
            }
            
            with open("app.json", "w") as f:
                json.dump(app_config, f, indent=2)
            
            print("✅ Production files created:")
            print("   - Procfile")
            print("   - runtime.txt") 
            print("   - app.json")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create production files: {e}")
            return False
    
    def create_dockerfile(self) -> bool:
        """Create optimized Dockerfile for production."""
        print("\n🐳 Creating Dockerfile...")
        
        dockerfile_content = """# Production Dockerfile for Agent Aster (tryagentaster.com)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_production.txt .
RUN pip install --no-cache-dir -r requirements_production.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60", "agent_backend_production:app"]"""

        try:
            with open("Dockerfile", "w") as f:
                f.write(dockerfile_content)
            
            print("✅ Dockerfile created")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create Dockerfile: {e}")
            return False
    
    def create_nginx_config(self) -> bool:
        """Create nginx configuration for reverse proxy."""
        print("\n🌐 Creating nginx configuration...")
        
        nginx_config = """# Nginx configuration for tryagentaster.com
server {
    listen 80;
    server_name tryagentaster.com www.tryagentaster.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tryagentaster.com www.tryagentaster.com;
    
    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tryagentaster.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tryagentaster.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    # Frontend (Streamlit)
    location / {
        proxy_pass http://localhost:8514;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 30;
    }
    
    # Health check
    location /health {
        proxy_pass http://localhost:5000/health;
        access_log off;
    }
}"""

        try:
            os.makedirs("nginx", exist_ok=True)
            with open("nginx/agent-aster.conf", "w") as f:
                f.write(nginx_config)
            
            print("✅ Nginx configuration created")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create nginx config: {e}")
            return False
    
    def create_deployment_guide(self) -> bool:
        """Create comprehensive deployment guide."""
        print("\n📖 Creating deployment guide...")
        
        guide_content = """# Agent Aster Deployment Guide - tryagentaster.com

## Prerequisites
1. Domain: tryagentaster.com (configured)
2. GitHub repository set up
3. Supabase account and project
4. Hosting platform account (Vercel/Railway/VPS)

## Quick Deployment Options

### Option A: Vercel (Recommended)
1. Push code to GitHub
2. Connect GitHub repo to Vercel
3. Configure environment variables
4. Set custom domain to tryagentaster.com
5. Deploy!

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Option B: Railway
1. Connect GitHub repository
2. Configure environment variables
3. Set custom domain
4. Deploy automatically

### Option C: VPS (Advanced)
1. Set up Ubuntu VPS
2. Install Docker & Docker Compose
3. Configure nginx & SSL
4. Deploy with Docker

## Environment Variables Setup

### Required Variables
```bash
ENVIRONMENT=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.your-project.supabase.co:5432/postgres
FERNET_KEY=your-encryption-key
FLASK_SECRET_KEY=your-flask-secret
```

### Optional Variables
```bash
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
HEALTH_CHECK_TOKEN=your-health-token
```

## Supabase Database Setup
1. Create new Supabase project
2. Go to SQL Editor
3. Run database_schema.sql
4. Copy connection details to environment variables

## Security Checklist
- ✅ SSL/HTTPS enabled
- ✅ Environment variables secured
- ✅ Database Row Level Security enabled
- ✅ Rate limiting configured
- ✅ CORS properly configured
- ✅ API keys encrypted
- ✅ Health checks enabled

## Monitoring Setup
1. Configure Sentry for error tracking
2. Set up uptime monitoring
3. Configure log aggregation
4. Set up performance monitoring

## Domain Configuration
1. Point tryagentaster.com to your hosting platform
2. Configure SSL certificate
3. Set up www redirect
4. Configure CDN if needed

## Post-Deployment
1. Test all functionality
2. Verify SSL certificate
3. Test rate limiting
4. Monitor error logs
5. Set up backups

## Support
- GitHub Issues: https://github.com/yourusername/agent-aster/issues
- Documentation: https://tryagentaster.com/docs
"""

        try:
            with open("DEPLOYMENT.md", "w") as f:
                f.write(guide_content)
            
            print("✅ Deployment guide created: DEPLOYMENT.md")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create deployment guide: {e}")
            return False
    
    def run_deployment(self) -> bool:
        """Run complete deployment process."""
        print("🚀 Starting Agent Aster deployment for tryagentaster.com")
        print("=" * 60)
        
        steps = [
            ("Validate Environment", self.validate_environment),
            ("Setup Database", self.setup_database),
            ("Create Production Files", self.create_production_files),
            ("Create Dockerfile", self.create_dockerfile),
            ("Create Nginx Config", self.create_nginx_config),
            ("Create Deployment Guide", self.create_deployment_guide),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            if not step_func():
                print(f"❌ Deployment failed at: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 Deployment preparation complete!")
        print("\n📋 Next Steps:")
        print("1. Read DEPLOYMENT.md for detailed instructions")
        print("2. Set up your Supabase database")
        print("3. Configure environment variables")
        print("4. Push to GitHub and deploy to your chosen platform")
        print("5. Point tryagentaster.com to your deployment")
        print("\n🌟 Your Agent Aster will be live at https://tryagentaster.com!")
        
        return True

if __name__ == "__main__":
    deployer = DeploymentManager()
    success = deployer.run_deployment()
    sys.exit(0 if success else 1)

"""
Production Configuration for Agent Aster (tryagentaster.com)
Secure, scalable configuration for live deployment
"""

import os
from typing import Optional
from cryptography.fernet import Fernet
import secrets

class ProductionConfig:
    """Production configuration with security hardening."""
    
    # Domain and URLs
    DOMAIN = "tryagentaster.com"
    BASE_URL = f"https://{DOMAIN}"
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_urlsafe(32))
    DEBUG = False
    TESTING = False
    
    # Database Configuration (Supabase)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY') 
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')  # PostgreSQL connection string
    
    # Encryption
    FERNET_KEY = os.getenv('FERNET_KEY')  # For encrypting API keys
    JWT_SECRET = os.getenv('JWT_SECRET', secrets.token_urlsafe(32))
    JWT_EXPIRATION_HOURS = 24
    
    # Aster Finance API
    ASTER_API_TIMEOUT = 30
    ASTER_MAX_RETRIES = 3
    ASTER_RATE_LIMIT = 100  # requests per minute
    
    # Security Settings
    CORS_ORIGINS = [
        f"https://{DOMAIN}",
        f"https://www.{DOMAIN}",
        "https://www.asterdex.com",  # Allow Aster Finance
    ]
    
    # Content Security Policy
    CSP_DIRECTIVES = {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
        'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        'font-src': ["'self'", "https://fonts.gstatic.com"],
        'img-src': ["'self'", "data:", "https:"],
        'connect-src': ["'self'", "https://sapi.asterdx.com", "https://fapi.asterdx.com"],
    }
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_PER_METHOD = True
    
    # Default rate limits (requests per minute)
    RATE_LIMITS = {
        'chat': 30,
        'balance': 10,
        'trade': 5,
        'market_data': 60,
        'session_create': 5,
    }
    
    # Session Management
    SESSION_TIMEOUT_HOURS = 24
    MAX_SESSIONS_PER_IP = 10
    
    # Trading Limits
    MAX_TRADE_AMOUNT_USDT = 10000.0
    MIN_TRADE_AMOUNT_USDT = 1.0
    MAX_LEVERAGE = 125
    DEFAULT_LEVERAGE = 2
    
    # Demo Mode Settings
    DEMO_STARTING_BALANCE = 10000.0
    DEMO_SESSION_DURATION_HOURS = 48
    
    # Monitoring & Logging
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Health Check
    HEALTH_CHECK_TOKEN = os.getenv('HEALTH_CHECK_TOKEN', secrets.token_urlsafe(16))
    
    # Feature Flags
    MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'false').lower() == 'true'
    DEMO_MODE_ENABLED = True
    REAL_TRADING_ENABLED = True
    
    @classmethod
    def get_encryption_key(cls) -> Fernet:
        """Get or generate encryption key for API credentials."""
        key = cls.FERNET_KEY
        if not key:
            key = Fernet.generate_key().decode()
            print(f"Generated new encryption key: {key}")
            print("Set this as FERNET_KEY environment variable")
        return Fernet(key.encode() if isinstance(key, str) else key)
    
    @classmethod
    def validate_required_env_vars(cls) -> list[str]:
        """Validate that all required environment variables are set."""
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY', 
            'SUPABASE_SERVICE_KEY',
            'DATABASE_URL',
            'FERNET_KEY',
            'FLASK_SECRET_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        return missing_vars

class DevelopmentConfig(ProductionConfig):
    """Development configuration - less strict security for local development."""
    
    DEBUG = True
    DOMAIN = "localhost:8514"
    BASE_URL = f"http://{DOMAIN}"
    
    # Allow local CORS
    CORS_ORIGINS = [
        "http://localhost:8514",
        "http://localhost:5000", 
        "http://127.0.0.1:8514",
        "http://127.0.0.1:5000"
    ]
    
    # Relaxed CSP for development
    CSP_DIRECTIVES = {
        'default-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        'connect-src': ["'self'", "https://sapi.asterdx.com", "https://fapi.asterdx.com"],
    }
    
    # Higher rate limits for development
    RATE_LIMITS = {
        'chat': 100,
        'balance': 50,
        'trade': 20,
        'market_data': 200,
        'session_create': 20,
    }

def get_config() -> ProductionConfig:
    """Get configuration based on environment."""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Global config instance
config = get_config()

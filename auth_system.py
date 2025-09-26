#!/usr/bin/env python3
"""
Enterprise-Grade Authentication & Wallet Integration for Agent-Aster
Built for Aster Finance API with industry-standard security patterns
"""

import os
import json
import time
import hmac
import hashlib
import base64
import secrets
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt
from dataclasses import dataclass, asdict
import sqlite3
import aiofiles
import asyncio

# Import for blockchain wallet operations
try:
    from eth_account import Account
    from eth_account.messages import encode_defunct
    from web3 import Web3
    ETH_SUPPORT = True
except ImportError:
    ETH_SUPPORT = False

@dataclass
class UserSession:
    """User session data structure."""
    user_id: str
    email: str
    api_key: str
    api_secret_hash: str
    wallet_address: Optional[str] = None
    wallet_type: Optional[str] = None  # 'ethereum', 'solana', 'aptos'
    permissions: list = None
    created_at: float = None
    expires_at: float = None
    last_activity: float = None
    ip_address: Optional[str] = None
    session_token: Optional[str] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = ['read', 'trade']
        if self.created_at is None:
            self.created_at = time.time()
        if self.expires_at is None:
            self.expires_at = time.time() + (24 * 3600)  # 24 hours

@dataclass 
class WalletInfo:
    """Wallet information structure."""
    address: str
    wallet_type: str  # 'ethereum', 'solana', 'aptos'
    public_key: str
    encrypted_private_key: str
    derivation_path: Optional[str] = None
    created_at: float = None
    last_used: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class AsterAPIAuth:
    """Aster Finance API Authentication Handler."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        
    def generate_signature(self, query_string: str, timestamp: int) -> str:
        """Generate HMAC SHA256 signature for Aster API."""
        # Aster API signature format: timestamp + HTTP_METHOD + requestPath + body
        message = f"{timestamp}GET/api/v1/account{query_string}"
        
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def get_auth_headers(self, endpoint: str = "/api/v1/account", 
                        query_params: Dict[str, Any] = None) -> Dict[str, str]:
        """Get authentication headers for Aster API requests."""
        timestamp = int(time.time() * 1000)  # milliseconds
        
        # Build query string
        query_string = ""
        if query_params:
            query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
            if query_string:
                query_string = f"?{query_string}"
        
        signature = self.generate_signature(query_string, timestamp)
        
        return {
            "X-MBX-APIKEY": self.api_key,
            "X-MBX-SIGNATURE": signature,
            "X-MBX-TIMESTAMP": str(timestamp),
            "Content-Type": "application/json"
        }

class WalletManager:
    """Enterprise wallet management with multi-chain support."""
    
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
        self.db_path = ".agent_aster/wallets.db"
        self._init_db()
    
    def _init_db(self):
        """Initialize wallet database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wallets (
                    user_id TEXT PRIMARY KEY,
                    address TEXT NOT NULL,
                    wallet_type TEXT NOT NULL,
                    public_key TEXT NOT NULL,
                    encrypted_private_key TEXT NOT NULL,
                    derivation_path TEXT,
                    created_at REAL NOT NULL,
                    last_used REAL,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    tx_hash TEXT NOT NULL,
                    wallet_address TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    amount REAL NOT NULL,
                    price REAL,
                    signature TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            """)
    
    def create_ethereum_wallet(self, user_id: str) -> WalletInfo:
        """Create new Ethereum wallet."""
        if not ETH_SUPPORT:
            raise RuntimeError("Ethereum support not available. Install web3 and eth-account")
        
        # Generate new account
        account = Account.create()
        
        # Encrypt private key
        private_key_bytes = account.key
        encrypted_private_key = self.fernet.encrypt(private_key_bytes).decode('utf-8')
        
        wallet_info = WalletInfo(
            address=account.address,
            wallet_type="ethereum",
            public_key=account.address,  # For ETH, address is derived from public key
            encrypted_private_key=encrypted_private_key
        )
        
        # Save to database
        self._save_wallet(user_id, wallet_info)
        
        return wallet_info
    
    def import_ethereum_wallet(self, user_id: str, private_key: str) -> WalletInfo:
        """Import existing Ethereum wallet."""
        if not ETH_SUPPORT:
            raise RuntimeError("Ethereum support not available")
        
        try:
            # Validate private key
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            private_key_bytes = bytes.fromhex(private_key)
            account = Account.from_key(private_key_bytes)
            
            # Encrypt private key
            encrypted_private_key = self.fernet.encrypt(private_key_bytes).decode('utf-8')
            
            wallet_info = WalletInfo(
                address=account.address,
                wallet_type="ethereum",
                public_key=account.address,
                encrypted_private_key=encrypted_private_key
            )
            
            self._save_wallet(user_id, wallet_info)
            return wallet_info
            
        except Exception as e:
            raise ValueError(f"Invalid Ethereum private key: {e}")
    
    def _save_wallet(self, user_id: str, wallet_info: WalletInfo):
        """Save wallet to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO wallets 
                (user_id, address, wallet_type, public_key, encrypted_private_key, 
                 derivation_path, created_at, last_used, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, wallet_info.address, wallet_info.wallet_type,
                wallet_info.public_key, wallet_info.encrypted_private_key,
                wallet_info.derivation_path, wallet_info.created_at,
                wallet_info.last_used, json.dumps({})
            ))
    
    def get_wallet(self, user_id: str) -> Optional[WalletInfo]:
        """Get wallet for user."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM wallets WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return WalletInfo(
                    address=row['address'],
                    wallet_type=row['wallet_type'],
                    public_key=row['public_key'],
                    encrypted_private_key=row['encrypted_private_key'],
                    derivation_path=row['derivation_path'],
                    created_at=row['created_at'],
                    last_used=row['last_used']
                )
        return None
    
    def sign_transaction(self, user_id: str, transaction_data: Dict[str, Any]) -> str:
        """Sign transaction with user's wallet."""
        wallet = self.get_wallet(user_id)
        if not wallet:
            raise ValueError("No wallet found for user")
        
        # Decrypt private key
        encrypted_key = wallet.encrypted_private_key.encode('utf-8')
        private_key_bytes = self.fernet.decrypt(encrypted_key)
        
        if wallet.wallet_type == "ethereum":
            if not ETH_SUPPORT:
                raise RuntimeError("Ethereum support not available")
            
            account = Account.from_key(private_key_bytes)
            
            # Create message to sign (simplified for trading)
            message_data = {
                "symbol": transaction_data.get("symbol"),
                "side": transaction_data.get("side"),
                "amount": transaction_data.get("amount"),
                "timestamp": int(time.time() * 1000),
                "nonce": secrets.randbits(64)
            }
            
            message_json = json.dumps(message_data, sort_keys=True)
            message = encode_defunct(text=message_json)
            
            # Sign message
            signed_message = account.sign_message(message)
            
            # Update last used
            self._update_wallet_last_used(user_id)
            
            return signed_message.signature.hex()
        
        else:
            raise ValueError(f"Unsupported wallet type: {wallet.wallet_type}")
    
    def _update_wallet_last_used(self, user_id: str):
        """Update wallet last used timestamp."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE wallets SET last_used = ? WHERE user_id = ?",
                (time.time(), user_id)
            )

class AuthenticationManager:
    """Enterprise authentication system for Agent-Aster."""
    
    def __init__(self, encryption_key: bytes, jwt_secret: str):
        self.fernet = Fernet(encryption_key)
        self.jwt_secret = jwt_secret
        self.db_path = ".agent_aster/auth.db"
        self.wallet_manager = WalletManager(encryption_key)
        self._init_db()
    
    def _init_db(self):
        """Initialize authentication database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    api_key TEXT UNIQUE NOT NULL,
                    api_secret_hash TEXT NOT NULL,
                    permissions TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_login REAL,
                    is_active BOOLEAN DEFAULT 1,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_token TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    last_activity REAL NOT NULL,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
    
    def create_user(self, email: str, password: str, 
                   api_key: str, api_secret: str) -> UserSession:
        """Create new user account."""
        # Generate user ID
        user_id = secrets.token_urlsafe(16)
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Hash API secret
        api_secret_hash = bcrypt.hashpw(api_secret.encode('utf-8'), bcrypt.gensalt())
        
        # Default permissions
        permissions = ['read', 'trade', 'withdraw']
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO users 
                (user_id, email, password_hash, api_key, api_secret_hash, 
                 permissions, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, email, password_hash.decode('utf-8'), api_key,
                api_secret_hash.decode('utf-8'), json.dumps(permissions),
                time.time(), json.dumps({})
            ))
        
        return UserSession(
            user_id=user_id,
            email=email,
            api_key=api_key,
            api_secret_hash=api_secret_hash.decode('utf-8'),
            permissions=permissions
        )
    
    def authenticate_user(self, email: str, password: str, 
                         ip_address: str = None) -> Optional[UserSession]:
        """Authenticate user and create session."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM users WHERE email = ? AND is_active = 1", 
                (email,)
            )
            user_row = cursor.fetchone()
            
            if not user_row:
                return None
            
            # Verify password
            stored_hash = user_row['password_hash'].encode('utf-8')
            if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return None
            
            # Create session
            session_token = secrets.token_urlsafe(32)
            session_expires = time.time() + (24 * 3600)  # 24 hours
            
            conn.execute("""
                INSERT INTO sessions 
                (session_token, user_id, ip_address, created_at, expires_at, last_activity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_token, user_row['user_id'], ip_address,
                time.time(), session_expires, time.time()
            ))
            
            # Update last login
            conn.execute(
                "UPDATE users SET last_login = ? WHERE user_id = ?",
                (time.time(), user_row['user_id'])
            )
            
            return UserSession(
                user_id=user_row['user_id'],
                email=user_row['email'],
                api_key=user_row['api_key'],
                api_secret_hash=user_row['api_secret_hash'],
                permissions=json.loads(user_row['permissions']),
                session_token=session_token,
                expires_at=session_expires,
                ip_address=ip_address
            )
    
    def validate_session(self, session_token: str) -> Optional[UserSession]:
        """Validate session token."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT s.*, u.email, u.api_key, u.api_secret_hash, u.permissions
                FROM sessions s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.session_token = ? AND s.is_active = 1 AND s.expires_at > ?
            """, (session_token, time.time()))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Update last activity
            conn.execute(
                "UPDATE sessions SET last_activity = ? WHERE session_token = ?",
                (time.time(), session_token)
            )
            
            return UserSession(
                user_id=row['user_id'],
                email=row['email'],
                api_key=row['api_key'],
                api_secret_hash=row['api_secret_hash'],
                permissions=json.loads(row['permissions']),
                session_token=session_token,
                expires_at=row['expires_at'],
                last_activity=time.time(),
                ip_address=row['ip_address']
            )
    
    def create_api_auth(self, user_session: UserSession) -> AsterAPIAuth:
        """Create Aster API authentication handler for user."""
        # In production, you'd decrypt the API secret here
        # For now, using the provided API secret
        api_secret = os.environ.get('ASTER_API_SECRET', '')
        
        return AsterAPIAuth(user_session.api_key, api_secret)

class SecureTradeManager:
    """Secure trade execution with wallet signing."""
    
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
    
    async def execute_secure_trade(self, user_session: UserSession, 
                                 trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trade with wallet signature for security."""
        
        # Check permissions
        if 'trade' not in user_session.permissions:
            raise PermissionError("User does not have trading permissions")
        
        # Get wallet for signing
        wallet = self.auth_manager.wallet_manager.get_wallet(user_session.user_id)
        if not wallet:
            raise ValueError("No wallet configured for user")
        
        # Sign transaction
        signature = self.auth_manager.wallet_manager.sign_transaction(
            user_session.user_id, trade_data
        )
        
        # Create Aster API auth
        api_auth = self.auth_manager.create_api_auth(user_session)
        
        # Add signature to trade data
        signed_trade_data = {
            **trade_data,
            "userSignature": signature,
            "walletAddress": wallet.address,
            "timestamp": int(time.time() * 1000)
        }
        
        # Get auth headers
        headers = api_auth.get_auth_headers("/api/v1/order", signed_trade_data)
        
        return {
            "trade_data": signed_trade_data,
            "headers": headers,
            "signature": signature,
            "wallet_address": wallet.address,
            "status": "ready_for_execution"
        }

# Example usage and demo functions
def demo_authentication_system():
    """Demonstrate the authentication system."""
    print("🔐 Agent-Aster Enterprise Authentication Demo")
    print("=" * 55)
    
    # Generate encryption key
    encryption_key = Fernet.generate_key()
    jwt_secret = secrets.token_urlsafe(32)
    
    # Initialize auth manager
    auth_manager = AuthenticationManager(encryption_key, jwt_secret)
    
    # Create demo user
    print("1. Creating demo user...")
    user_session = auth_manager.create_user(
        email="trader@example.com",
        password="secure_password_123",
        api_key="demo_api_key_12345",
        api_secret="demo_api_secret_67890"
    )
    print(f"✅ User created: {user_session.email}")
    
    # Create wallet
    print("\n2. Creating Ethereum wallet...")
    if ETH_SUPPORT:
        wallet = auth_manager.wallet_manager.create_ethereum_wallet(user_session.user_id)
        print(f"✅ Wallet created: {wallet.address}")
    else:
        print("⚠️  Ethereum support not available")
    
    # Authenticate user
    print("\n3. Authenticating user...")
    auth_session = auth_manager.authenticate_user(
        "trader@example.com", 
        "secure_password_123",
        "192.168.1.100"
    )
    
    if auth_session:
        print(f"✅ Authentication successful")
        print(f"   Session token: {auth_session.session_token[:20]}...")
        print(f"   Permissions: {auth_session.permissions}")
    
    # Create secure trade
    print("\n4. Creating secure trade...")
    trade_manager = SecureTradeManager(auth_manager)
    
    if ETH_SUPPORT and auth_session:
        try:
            trade_result = asyncio.run(trade_manager.execute_secure_trade(
                auth_session,
                {
                    "symbol": "BTCUSDT",
                    "side": "BUY", 
                    "amount": 0.001,
                    "type": "MARKET"
                }
            ))
            print(f"✅ Trade prepared with signature")
            print(f"   Signature: {trade_result['signature'][:20]}...")
            print(f"   Wallet: {trade_result['wallet_address']}")
        except Exception as e:
            print(f"❌ Trade preparation failed: {e}")
    
    print("\n🎉 Authentication system demo complete!")

if __name__ == "__main__":
    demo_authentication_system()

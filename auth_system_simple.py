#!/usr/bin/env python3
"""
Simplified Authentication & Wallet Integration for Agent-Aster
Direct API key authentication without email/password complexity
"""

import os
import json
import time
import hmac
import hashlib
import secrets
from typing import Dict, Any, Optional
from dataclasses import dataclass
import sqlite3
from cryptography.fernet import Fernet

# Import for blockchain wallet operations
try:
    from eth_account import Account
    from eth_account.messages import encode_defunct
    from web3 import Web3
    ETH_SUPPORT = True
except ImportError:
    ETH_SUPPORT = False

@dataclass
class SimpleSession:
    """Simplified session data structure."""
    session_id: str
    api_key: str
    api_secret: str
    wallet_address: Optional[str] = None
    wallet_type: Optional[str] = None
    created_at: float = None
    last_activity: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
        if self.last_activity is None:
            self.last_activity = time.time()

@dataclass 
class WalletInfo:
    """Wallet information structure."""
    address: str
    wallet_type: str  # 'ethereum', 'solana', 'aptos'
    public_key: str
    encrypted_private_key: str
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

class SimpleWalletManager:
    """Simplified wallet management."""
    
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
        self.db_path = ".agent_aster/simple_wallets.db"
        self._init_db()
    
    def _init_db(self):
        """Initialize wallet database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wallets (
                    session_id TEXT PRIMARY KEY,
                    address TEXT NOT NULL,
                    wallet_type TEXT NOT NULL,
                    public_key TEXT NOT NULL,
                    encrypted_private_key TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_used REAL,
                    metadata TEXT
                )
            """)
    
    def create_ethereum_wallet(self, session_id: str) -> WalletInfo:
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
            public_key=account.address,
            encrypted_private_key=encrypted_private_key
        )
        
        # Save to database
        self._save_wallet(session_id, wallet_info)
        
        return wallet_info
    
    def import_ethereum_wallet(self, session_id: str, private_key: str) -> WalletInfo:
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
            
            self._save_wallet(session_id, wallet_info)
            return wallet_info
            
        except Exception as e:
            raise ValueError(f"Invalid Ethereum private key: {e}")
    
    def _save_wallet(self, session_id: str, wallet_info: WalletInfo):
        """Save wallet to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO wallets 
                (session_id, address, wallet_type, public_key, encrypted_private_key, 
                 created_at, last_used, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, wallet_info.address, wallet_info.wallet_type,
                wallet_info.public_key, wallet_info.encrypted_private_key,
                wallet_info.created_at, wallet_info.last_used, json.dumps({})
            ))
    
    def get_wallet(self, session_id: str) -> Optional[WalletInfo]:
        """Get wallet for session."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM wallets WHERE session_id = ?", (session_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return WalletInfo(
                    address=row['address'],
                    wallet_type=row['wallet_type'],
                    public_key=row['public_key'],
                    encrypted_private_key=row['encrypted_private_key'],
                    created_at=row['created_at'],
                    last_used=row['last_used']
                )
        return None
    
    def sign_transaction(self, session_id: str, transaction_data: Dict[str, Any]) -> str:
        """Sign transaction with session's wallet."""
        wallet = self.get_wallet(session_id)
        if not wallet:
            raise ValueError("No wallet found for session")
        
        # Decrypt private key
        encrypted_key = wallet.encrypted_private_key.encode('utf-8')
        private_key_bytes = self.fernet.decrypt(encrypted_key)
        
        if wallet.wallet_type == "ethereum":
            if not ETH_SUPPORT:
                raise RuntimeError("Ethereum support not available")
            
            account = Account.from_key(private_key_bytes)
            
            # Create message to sign
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
            self._update_wallet_last_used(session_id)
            
            return signed_message.signature.hex()
        
        else:
            raise ValueError(f"Unsupported wallet type: {wallet.wallet_type}")
    
    def _update_wallet_last_used(self, session_id: str):
        """Update wallet last used timestamp."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE wallets SET last_used = ? WHERE session_id = ?",
                (time.time(), session_id)
            )

class SimpleAuthManager:
    """Simplified authentication - just API keys, no email/password."""
    
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
        self.wallet_manager = SimpleWalletManager(encryption_key)
        self.sessions = {}  # In-memory session storage
    
    def create_session(self, api_key: str, api_secret: str) -> SimpleSession:
        """Create a new session with API credentials."""
        session_id = secrets.token_urlsafe(16)
        
        session = SimpleSession(
            session_id=session_id,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # Store in memory
        self.sessions[session_id] = session
        
        return session
    
    def get_session(self, session_id: str) -> Optional[SimpleSession]:
        """Get session by ID."""
        session = self.sessions.get(session_id)
        if session:
            session.last_activity = time.time()
        return session
    
    def update_session(self, session: SimpleSession) -> None:
        """Update existing session in memory storage."""
        if session.session_id in self.sessions:
            session.last_activity = time.time()
            self.sessions[session.session_id] = session
    
    def create_api_auth(self, session: SimpleSession) -> AsterAPIAuth:
        """Create Aster API authentication handler for session."""
        return AsterAPIAuth(session.api_key, session.api_secret)

class SimpleTradeManager:
    """Simplified secure trade execution."""
    
    def __init__(self, auth_manager: SimpleAuthManager):
        self.auth_manager = auth_manager
    
    async def execute_secure_trade(self, session: SimpleSession, 
                                 trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trade with wallet signature."""
        
        # Get wallet for signing
        wallet = self.auth_manager.wallet_manager.get_wallet(session.session_id)
        if not wallet:
            raise ValueError("No wallet configured for session")
        
        # Sign transaction
        signature = self.auth_manager.wallet_manager.sign_transaction(
            session.session_id, trade_data
        )
        
        # Create Aster API auth
        api_auth = self.auth_manager.create_api_auth(session)
        
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

def demo_simple_auth():
    """Demo the simplified authentication system."""
    print("🔑 Agent-Aster Simplified Authentication Demo")
    print("=" * 50)
    
    # Generate encryption key
    encryption_key = Fernet.generate_key()
    
    # Initialize auth manager
    auth_manager = SimpleAuthManager(encryption_key)
    
    # Create session with API credentials
    print("1. Creating session with API credentials...")
    session = auth_manager.create_session(
        api_key="9889c4ca2a8612bbdc801df6f1fba74c6365b094df19d878b8a21a420e04436a",
        api_secret="748c304002a5b1e4d841b079d636f0c8c8eeb96fb055f6b98684c65f56fe2fb3"
    )
    print(f"✅ Session created: {session.session_id}")
    
    # Create wallet
    print("\n2. Creating Ethereum wallet...")
    if ETH_SUPPORT:
        wallet = auth_manager.wallet_manager.create_ethereum_wallet(session.session_id)
        print(f"✅ Wallet created: {wallet.address}")
        session.wallet_address = wallet.address
        session.wallet_type = wallet.wallet_type
    else:
        print("⚠️  Ethereum support not available")
    
    # Test API auth
    print("\n3. Testing API authentication...")
    api_auth = auth_manager.create_api_auth(session)
    headers = api_auth.get_auth_headers()
    print(f"✅ API headers generated: {len(headers)} headers")
    
    print("\n🎉 Simplified authentication demo complete!")

if __name__ == "__main__":
    demo_simple_auth()

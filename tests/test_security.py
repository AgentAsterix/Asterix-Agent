"""Unit tests for Agent-Aster security module."""

import pytest
from unittest.mock import Mock, patch
import time

from agent_aster.utils.security import (
    AsterSecurityValidator, get_security_validator, validate_trade_request,
    is_testnet_mode, get_base_url, ASTER_APPROVED_SYMBOLS
)


class TestAsterSecurityValidator:
    """Test cases for security validator."""
    
    def test_validate_trading_pair_valid_symbols(self):
        """Test validation of valid trading pairs."""
        validator = AsterSecurityValidator()
        
        valid_symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
        
        for symbol in valid_symbols:
            result = validator.validate_trading_pair(symbol)
            assert result["valid"] is True
            assert result["symbol"] == symbol
    
    def test_validate_trading_pair_invalid_symbols(self):
        """Test validation of invalid trading pairs."""
        validator = AsterSecurityValidator()
        
        invalid_symbols = ["BTCUSD", "INVALID", "ETHBTC", ""]
        
        for symbol in invalid_symbols:
            result = validator.validate_trading_pair(symbol)
            assert result["valid"] is False
            assert "error" in result
    
    def test_validate_trading_pair_case_insensitive(self):
        """Test that symbol validation is case insensitive."""
        validator = AsterSecurityValidator()
        
        result = validator.validate_trading_pair("btcusdt")
        assert result["valid"] is True
        assert result["symbol"] == "BTCUSDT"
    
    def test_validate_trade_amount_valid_amounts(self):
        """Test validation of valid trade amounts."""
        validator = AsterSecurityValidator()
        
        valid_amounts = [5.0, 10.0, 100.0, 1000.0, 10000.0]
        
        for amount in valid_amounts:
            result = validator.validate_trade_amount(amount)
            assert result["valid"] is True
            assert result["amount"] == amount
    
    def test_validate_trade_amount_invalid_amounts(self):
        """Test validation of invalid trade amounts."""
        validator = AsterSecurityValidator()
        
        invalid_amounts = [0, -10, 0.01, 100000.0]  # Too small or too large
        
        for amount in invalid_amounts:
            result = validator.validate_trade_amount(amount)
            assert result["valid"] is False
            assert "error" in result
    
    def test_validate_trade_amount_with_warning(self):
        """Test trade amount validation with warnings for high amounts."""
        validator = AsterSecurityValidator()
        
        # Test futures trade with high amount
        result = validator.validate_trade_amount(15000.0, "futures")
        assert result["valid"] is True
        assert "warning" in result
        assert result["amount"] == 15000.0
    
    def test_validate_leverage_valid_values(self):
        """Test validation of valid leverage values."""
        validator = AsterSecurityValidator()
        
        valid_leverages = [1, 2, 5, 10, 50, 100]
        
        for leverage in valid_leverages:
            result = validator.validate_leverage(leverage)
            assert result["valid"] is True
            assert result["leverage"] == leverage
    
    def test_validate_leverage_invalid_values(self):
        """Test validation of invalid leverage values."""
        validator = AsterSecurityValidator()
        
        invalid_leverages = [0, -1, 150, "invalid"]
        
        for leverage in invalid_leverages:
            result = validator.validate_leverage(leverage)
            assert result["valid"] is False
            assert "error" in result
    
    def test_validate_leverage_with_warning(self):
        """Test leverage validation with warnings for high values."""
        validator = AsterSecurityValidator()
        
        result = validator.validate_leverage(50)
        assert result["valid"] is True
        assert "warning" in result
        assert "High leverage" in result["warning"]
    
    def test_validate_slippage_valid_values(self):
        """Test validation of valid slippage values."""
        validator = AsterSecurityValidator()
        
        valid_slippages = [0.1, 1.0, 5.0, 10.0, 20.0]
        
        for slippage in valid_slippages:
            result = validator.validate_slippage(slippage)
            assert result["valid"] is True
            assert result["slippage"] == slippage
    
    def test_validate_slippage_invalid_values(self):
        """Test validation of invalid slippage values."""
        validator = AsterSecurityValidator()
        
        invalid_slippages = [0, -1, 25.0, "invalid"]
        
        for slippage in invalid_slippages:
            result = validator.validate_slippage(slippage)
            assert result["valid"] is False
            assert "error" in result
    
    def test_validate_wallet_address_ethereum(self):
        """Test validation of Ethereum wallet addresses."""
        validator = AsterSecurityValidator()
        
        valid_addresses = [
            "0x742d35Cc6634C0532925a3b8D1C6C5D8c4c59ae1",
            "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        ]
        
        for address in valid_addresses:
            result = validator.validate_wallet_address(address, "ethereum")
            assert result["valid"] is True
            assert result["address"] == address
            assert result["network"] == "ethereum"
    
    def test_validate_wallet_address_invalid(self):
        """Test validation of invalid wallet addresses."""
        validator = AsterSecurityValidator()
        
        invalid_addresses = [
            "invalid_address",
            "0x123",  # Too short
            "742d35Cc6634C0532925a3b8D1C6C5D8c4c59ae1",  # Missing 0x
            ""
        ]
        
        for address in invalid_addresses:
            result = validator.validate_wallet_address(address, "ethereum")
            assert result["valid"] is False
            assert "error" in result
    
    def test_validate_api_signature(self):
        """Test HMAC signature validation."""
        validator = AsterSecurityValidator()
        
        payload = "symbol=BTCUSDT&quantity=1.0&timestamp=1699123456789"
        secret = "test_secret_key"
        
        # Generate valid signature
        import hmac
        import hashlib
        expected_sig = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Test valid signature
        assert validator.validate_api_signature(payload, expected_sig, secret) is True
        
        # Test invalid signature
        assert validator.validate_api_signature(payload, "invalid_sig", secret) is False
    
    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        validator = AsterSecurityValidator()
        
        endpoint = "test_endpoint"
        user_id = "test_user"
        
        # Should allow requests within limit
        for i in range(10):
            result = validator.check_rate_limit(endpoint, user_id)
            assert result["allowed"] is True
            assert result["requests"] == i + 1
        
        # Mock time to simulate rate limiting
        with patch('time.time', return_value=time.time()):
            # Exceed rate limit
            for i in range(700):  # Exceed 600 per minute limit
                validator.check_rate_limit(endpoint, user_id)
            
            result = validator.check_rate_limit(endpoint, user_id)
            assert result["allowed"] is False
            assert "Rate limit exceeded" in result["error"]
    
    def test_sanitize_log_data(self):
        """Test log data sanitization."""
        validator = AsterSecurityValidator()
        
        sensitive_data = {
            "private_key": "secret_private_key",
            "api_secret": "secret_api_key",
            "password": "secret_password",
            "normal_field": "normal_value",
            "nested": {
                "secret": "nested_secret",
                "normal": "nested_normal"
            },
            "auth_token": "very_long_auth_token_that_should_be_redacted"
        }
        
        sanitized = validator.sanitize_log_data(sensitive_data)
        
        # Check sensitive fields are redacted
        assert sanitized["private_key"] == "***REDACTED***"
        assert sanitized["api_secret"] == "***REDACTED***"
        assert sanitized["password"] == "***REDACTED***"
        
        # Check normal fields are preserved
        assert sanitized["normal_field"] == "normal_value"
        
        # Check nested data is processed
        assert sanitized["nested"]["secret"] == "***REDACTED***"
        assert sanitized["nested"]["normal"] == "nested_normal"
        
        # Check long auth tokens are partially redacted
        assert sanitized["auth_token"].startswith("very")
        assert sanitized["auth_token"].endswith("cted")
        assert "***" in sanitized["auth_token"]
    
    def test_create_audit_log(self):
        """Test audit log creation."""
        validator = AsterSecurityValidator()
        
        action = "trade_executed"
        user_id = "test_user"
        details = {
            "symbol": "BTCUSDT",
            "amount": 100.0,
            "private_key": "secret_key",
            "ip_address": "192.168.1.1"
        }
        
        audit_log = validator.create_audit_log(action, user_id, details)
        
        assert audit_log["action"] == action
        assert audit_log["user_id"] == user_id
        assert "timestamp" in audit_log
        assert "ip_hash" in audit_log
        
        # Check sensitive data is sanitized
        assert audit_log["details"]["private_key"] == "***REDACTED***"
        assert audit_log["details"]["symbol"] == "BTCUSDT"
        
        # Check IP is hashed, not stored in plain text
        assert audit_log["ip_hash"] != "192.168.1.1"
        assert len(audit_log["ip_hash"]) == 16  # SHA256 hash truncated to 16 chars


class TestSecurityHelperFunctions:
    """Test security helper functions."""
    
    def test_validate_trade_request_valid(self):
        """Test valid trade request validation."""
        result = validate_trade_request("BTCUSDT", 100.0, "spot")
        
        assert result["valid"] is True
        assert result["symbol"] == "BTCUSDT"
        assert result["amount"] == 100.0
    
    def test_validate_trade_request_invalid_symbol(self):
        """Test trade request validation with invalid symbol."""
        result = validate_trade_request("INVALID", 100.0, "spot")
        
        assert result["valid"] is False
        assert "not approved" in result["error"]
    
    def test_validate_trade_request_invalid_amount(self):
        """Test trade request validation with invalid amount."""
        result = validate_trade_request("BTCUSDT", 0, "spot")
        
        assert result["valid"] is False
        assert "below minimum" in result["error"]
    
    def test_validate_trade_request_futures_with_leverage(self):
        """Test futures trade request validation with leverage."""
        result = validate_trade_request("BTCUSDT", 500.0, "futures", leverage=5)
        
        assert result["valid"] is True
        assert result["leverage"] == 5
    
    def test_validate_trade_request_invalid_leverage(self):
        """Test trade request validation with invalid leverage."""
        result = validate_trade_request("BTCUSDT", 500.0, "futures", leverage=150)
        
        assert result["valid"] is False
        assert "exceeds maximum" in result["error"]
    
    @patch.dict('os.environ', {'ASTER_TESTNET': 'true'})
    def test_is_testnet_mode_true(self):
        """Test testnet mode detection when enabled."""
        assert is_testnet_mode() is True
    
    @patch.dict('os.environ', {'ASTER_TESTNET': 'false'})
    def test_is_testnet_mode_false(self):
        """Test testnet mode detection when disabled."""
        assert is_testnet_mode() is False
    
    @patch.dict('os.environ', {'ASTER_TESTNET': 'true', 'ASTER_TESTNET_BASE_URL': 'https://testnet.example.com'})
    def test_get_base_url_testnet(self):
        """Test base URL retrieval in testnet mode."""
        url = get_base_url()
        assert "testnet" in url
    
    @patch.dict('os.environ', {'ASTER_TESTNET': 'false', 'ASTER_BASE_URL': 'https://api.example.com'})
    def test_get_base_url_mainnet(self):
        """Test base URL retrieval in mainnet mode."""
        url = get_base_url()
        assert "testnet" not in url


class TestSecurityConstants:
    """Test security constants and configuration."""
    
    def test_approved_symbols_coverage(self):
        """Test that approved symbols cover major trading pairs."""
        required_symbols = {"BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"}
        
        assert required_symbols.issubset(ASTER_APPROVED_SYMBOLS)
        assert len(ASTER_APPROVED_SYMBOLS) >= 20  # Should have good coverage
    
    def test_approved_symbols_format(self):
        """Test that all approved symbols follow USDT format."""
        for symbol in ASTER_APPROVED_SYMBOLS:
            assert symbol.endswith("USDT")
            assert len(symbol) >= 6  # At least 3 chars + USDT
            assert symbol.isupper()
            assert symbol.isalnum()

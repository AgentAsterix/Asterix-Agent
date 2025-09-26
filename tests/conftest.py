"""Pytest configuration and fixtures for Agent-Aster tests."""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock
from aioresponses import aioresponses
import tempfile
import os
from pathlib import Path

# Set test environment
os.environ["ASTER_TESTNET"] = "true"
os.environ["ASTER_FERNET_KEY"] = "test_key_for_testing_only_not_secure_do_not_use_in_production="


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_api_responses():
    """Mock API responses for Aster Finance."""
    return {
        "ping": {},
        "server_time": {"serverTime": 1699123456789},
        "exchange_info": {
            "timezone": "UTC",
            "serverTime": 1699123456789,
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "status": "TRADING",
                    "baseAsset": "BTC",
                    "quoteAsset": "USDT"
                }
            ]
        },
        "account": {
            "feeTier": 0,
            "canTrade": True,
            "canDeposit": True,
            "canWithdraw": True,
            "balances": [
                {"asset": "USDT", "free": "1000.00", "locked": "0.00"},
                {"asset": "BTC", "free": "0.05", "locked": "0.00"}
            ]
        },
        "order_response": {
            "symbol": "BTCUSDT",
            "orderId": 12345,
            "clientOrderId": "test_order_123",
            "transactTime": 1699123456789,
            "price": "35000.00",
            "origQty": "0.001",
            "executedQty": "0.001",
            "status": "FILLED",
            "type": "MARKET",
            "side": "BUY"
        },
        "futures_account": {
            "feeTier": 0,
            "canTrade": True,
            "totalWalletBalance": "1000.00",
            "totalUnrealizedPnl": "0.00",
            "assets": [
                {
                    "asset": "USDT",
                    "walletBalance": "1000.00",
                    "unrealizedPnl": "0.00",
                    "marginBalance": "1000.00",
                    "availableBalance": "1000.00"
                }
            ]
        },
        "positions": [
            {
                "symbol": "BTCUSDT",
                "positionAmt": "0.001",
                "entryPrice": "35000.00",
                "markPrice": "35100.00",
                "unrealizedPnl": "0.10",
                "leverage": "1",
                "marginType": "isolated"
            }
        ]
    }


@pytest.fixture
def mock_http_session():
    """Mock aiohttp session with Aster API responses."""
    with aioresponses() as m:
        # Spot API endpoints
        m.get("https://testnet-api.asterdx.com/api/v1/ping", payload={})
        m.get("https://testnet-api.asterdx.com/api/v1/time", 
              payload={"serverTime": 1699123456789})
        m.get("https://testnet-api.asterdx.com/api/v1/account", 
              payload={
                  "balances": [
                      {"asset": "USDT", "free": "1000.00", "locked": "0.00"},
                      {"asset": "BTC", "free": "0.05", "locked": "0.00"}
                  ]
              })
        m.post("https://testnet-api.asterdx.com/api/v1/order",
               payload={
                   "symbol": "BTCUSDT",
                   "orderId": 12345,
                   "status": "FILLED",
                   "executedQty": "0.001"
               })
        
        # Futures API endpoints
        m.get("https://testnet-fapi.asterdx.com/fapi/v3/ping", payload={})
        m.get("https://testnet-fapi.asterdx.com/fapi/v3/balance",
              payload=[
                  {
                      "asset": "USDT",
                      "walletBalance": "1000.00",
                      "availableBalance": "1000.00"
                  }
              ])
        m.get("https://testnet-fapi.asterdx.com/fapi/v3/positionRisk",
              payload=[
                  {
                      "symbol": "BTCUSDT",
                      "positionAmt": "0.000",
                      "entryPrice": "0.00",
                      "unrealizedPnl": "0.00"
                  }
              ])
        m.post("https://testnet-fapi.asterdx.com/fapi/v3/order",
               payload={
                   "symbol": "BTCUSDT",
                   "orderId": 54321,
                   "status": "FILLED"
               })
        
        yield m


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    try:
        os.unlink(db_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    return {
        "ASTER_API_KEY": "test_api_key",
        "ASTER_API_SECRET": "test_api_secret", 
        "ASTER_TESTNET": True,
        "ASTER_TESTNET_BASE_URL": "https://testnet-api.asterdx.com",
        "MAX_TRANSACTION_USDT": 10000.0,
        "DEFAULT_SLIPPAGE": 1.0,
        "OPENAI_API_KEY": "test_openai_key"
    }


@pytest.fixture
def mock_llm_provider():
    """Mock LLM provider for testing."""
    mock_llm = AsyncMock()
    mock_llm.chat_completion = AsyncMock()
    
    # Default response
    mock_response = Mock()
    mock_response.content = "I'll help you with that trade."
    mock_response.tool_calls = []
    mock_response.usage = {"total_tokens": 100, "prompt_tokens": 50, "completion_tokens": 50}
    
    mock_llm.chat_completion.return_value = mock_response
    
    return mock_llm


@pytest.fixture
def sample_trade_data():
    """Sample trade data for testing."""
    return {
        "spot_buy": {
            "symbol": "BTCUSDT",
            "amount_usdt": 100.0,
            "order_type": "MARKET"
        },
        "futures_long": {
            "symbol": "BTCUSDT", 
            "amount_usdt": 500.0,
            "leverage": 2,
            "margin_type": "ISOLATED"
        },
        "expected_order_response": {
            "success": True,
            "symbol": "BTCUSDT",
            "order_id": 12345,
            "executed_qty": "0.001",
            "status": "FILLED"
        }
    }


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    test_env = {
        "ASTER_TESTNET": "true",
        "ASTER_API_KEY": "test_key",
        "ASTER_API_SECRET": "test_secret",
        "ASTER_FERNET_KEY": "test_fernet_key_base64_encoded_32_bytes",
        "OPENAI_API_KEY": "test_openai_key",
        "LOG_LEVEL": "DEBUG"
    }
    
    # Set test environment variables
    for key, value in test_env.items():
        os.environ[key] = value
    
    yield
    
    # Cleanup (restore original values)
    for key in test_env.keys():
        os.environ.pop(key, None)

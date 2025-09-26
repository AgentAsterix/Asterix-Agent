"""Unit tests for Agent-Aster trading tools."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import asyncio

from agent_aster.integrations.aster.tools import (
    SpotBuyTool, SpotSellTool, FuturesLongTool, FuturesShortTool,
    GetBalanceTool, GetPositionTool, ClosePositionTool
)


class TestSpotBuyTool:
    """Test cases for SpotBuyTool."""
    
    @pytest.mark.asyncio
    async def test_spot_buy_valid_order(self, mock_http_session, sample_trade_data):
        """Test successful spot buy order."""
        tool = SpotBuyTool()
        
        # Mock the spot client
        with patch.object(tool, 'get_spot_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.market_buy.return_value = {
                "success": True,
                "orderId": 12345,
                "executedQty": "0.001",
                "status": "FILLED"
            }
            mock_client_getter.return_value = mock_client
            
            # Execute buy order
            result = await tool.execute(sample_trade_data["spot_buy"])
            
            # Verify result
            assert result["success"] is True
            assert result["symbol"] == "BTCUSDT"
            assert result["amount_usdt"] == 100.0
            assert result["order_id"] == 12345
            assert "Successfully bought" in result["message"]
    
    @pytest.mark.asyncio
    async def test_spot_buy_invalid_symbol(self):
        """Test spot buy with invalid symbol."""
        tool = SpotBuyTool()
        
        args = {
            "symbol": "INVALID",
            "amount_usdt": 100.0,
            "order_type": "MARKET"
        }
        
        result = await tool.execute(args)
        
        assert result["error"] is True
        assert "Invalid symbol" in result["message"]
    
    @pytest.mark.asyncio 
    async def test_spot_buy_invalid_amount(self):
        """Test spot buy with invalid amount."""
        tool = SpotBuyTool()
        
        args = {
            "symbol": "BTCUSDT",
            "amount_usdt": 0,  # Invalid amount
            "order_type": "MARKET"
        }
        
        result = await tool.execute(args)
        
        assert result["error"] is True
        assert "Invalid amount" in result["message"]
    
    @pytest.mark.asyncio
    async def test_spot_buy_client_error(self):
        """Test spot buy when client returns error."""
        tool = SpotBuyTool()
        
        with patch.object(tool, 'get_spot_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.market_buy.return_value = {
                "error": True,
                "message": "Insufficient balance"
            }
            mock_client_getter.return_value = mock_client
            
            args = {
                "symbol": "BTCUSDT",
                "amount_usdt": 100.0,
                "order_type": "MARKET"
            }
            
            result = await tool.execute(args)
            
            assert result["error"] is True
            assert "Insufficient balance" in result["message"]


class TestFuturesLongTool:
    """Test cases for FuturesLongTool."""
    
    @pytest.mark.asyncio
    async def test_futures_long_valid_order(self, sample_trade_data):
        """Test successful futures long position."""
        tool = FuturesLongTool()
        
        with patch.object(tool, 'get_futures_client') as mock_client_getter:
            mock_client = AsyncMock()
            
            # Mock price data
            mock_client.get_symbol_price.return_value = {
                "price": "35000.00"
            }
            
            # Mock long position creation
            mock_client.market_long.return_value = {
                "success": True,
                "orderId": 54321,
                "status": "FILLED"
            }
            
            mock_client_getter.return_value = mock_client
            
            result = await tool.execute(sample_trade_data["futures_long"])
            
            assert result["success"] is True
            assert result["symbol"] == "BTCUSDT"
            assert result["leverage"] == 2
            assert result["order_id"] == 54321
            assert "Successfully opened long position" in result["message"]
    
    @pytest.mark.asyncio
    async def test_futures_long_invalid_leverage(self):
        """Test futures long with invalid leverage."""
        tool = FuturesLongTool()
        
        args = {
            "symbol": "BTCUSDT",
            "amount_usdt": 500.0,
            "leverage": 150,  # Exceeds max leverage
            "margin_type": "ISOLATED"
        }
        
        result = await tool.execute(args)
        
        assert result["error"] is True
        assert "Invalid leverage" in result["message"]
    
    @pytest.mark.asyncio
    async def test_futures_long_price_fetch_error(self):
        """Test futures long when price fetch fails."""
        tool = FuturesLongTool()
        
        with patch.object(tool, 'get_futures_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.get_symbol_price.return_value = {
                "error": True,
                "message": "Price fetch failed"
            }
            mock_client_getter.return_value = mock_client
            
            args = {
                "symbol": "BTCUSDT",
                "amount_usdt": 500.0,
                "leverage": 2,
                "margin_type": "ISOLATED"
            }
            
            result = await tool.execute(args)
            
            assert result["error"] is True


class TestGetBalanceTool:
    """Test cases for GetBalanceTool."""
    
    @pytest.mark.asyncio
    async def test_get_spot_balance(self):
        """Test getting spot balance."""
        tool = GetBalanceTool()
        
        with patch.object(tool, 'get_spot_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.get_balances.return_value = {
                "balances": [
                    {"asset": "USDT", "free": "1000.00", "locked": "0.00"},
                    {"asset": "BTC", "free": "0.05", "locked": "0.00"}
                ]
            }
            mock_client_getter.return_value = mock_client
            
            args = {"account_type": "spot"}
            result = await tool.execute(args)
            
            assert result["success"] is True
            assert result["account_type"] == "spot"
            assert len(result["balances"]) >= 1
            assert result["usdt_balance"] == 1000.0
    
    @pytest.mark.asyncio
    async def test_get_futures_balance(self):
        """Test getting futures balance."""
        tool = GetBalanceTool()
        
        with patch.object(tool, 'get_futures_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.get_balance.return_value = [
                {
                    "asset": "USDT",
                    "walletBalance": "1000.00",
                    "unrealizedPnl": "0.00",
                    "marginBalance": "1000.00",
                    "availableBalance": "1000.00"
                }
            ]
            mock_client_getter.return_value = mock_client
            
            args = {"account_type": "futures"}
            result = await tool.execute(args)
            
            assert result["success"] is True
            assert result["account_type"] == "futures"
            assert result["total_wallet_balance"] == 1000.0


class TestGetPositionTool:
    """Test cases for GetPositionTool."""
    
    @pytest.mark.asyncio
    async def test_get_positions_with_open_position(self):
        """Test getting positions with open position."""
        tool = GetPositionTool()
        
        with patch.object(tool, 'get_futures_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.get_position_info.return_value = [
                {
                    "symbol": "BTCUSDT",
                    "positionAmt": "0.001",  # Active position
                    "entryPrice": "35000.00",
                    "markPrice": "35100.00",
                    "unrealizedPnl": "0.10",
                    "leverage": "2",
                    "marginType": "isolated"
                }
            ]
            mock_client_getter.return_value = mock_client
            
            result = await tool.execute({})
            
            assert result["success"] is True
            assert len(result["positions"]) == 1
            assert result["positions"][0]["symbol"] == "BTCUSDT"
            assert result["positions"][0]["side"] == "LONG"
            assert result["total_unrealized_pnl"] == 0.10
    
    @pytest.mark.asyncio
    async def test_get_positions_no_open_positions(self):
        """Test getting positions with no open positions."""
        tool = GetPositionTool()
        
        with patch.object(tool, 'get_futures_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.get_position_info.return_value = [
                {
                    "symbol": "BTCUSDT",
                    "positionAmt": "0.000",  # No position
                    "entryPrice": "0.00",
                    "unrealizedPnl": "0.00"
                }
            ]
            mock_client_getter.return_value = mock_client
            
            result = await tool.execute({})
            
            assert result["success"] is True
            assert len(result["positions"]) == 0
            assert result["total_unrealized_pnl"] == 0.0


class TestClosePositionTool:
    """Test cases for ClosePositionTool."""
    
    @pytest.mark.asyncio
    async def test_close_position_success(self):
        """Test successful position closing."""
        tool = ClosePositionTool()
        
        with patch.object(tool, 'get_futures_client') as mock_client_getter:
            mock_client = AsyncMock()
            mock_client.close_position.return_value = {
                "success": True,
                "orderId": 67890,
                "status": "FILLED"
            }
            mock_client_getter.return_value = mock_client
            
            args = {
                "symbol": "BTCUSDT",
                "position_side": "BOTH"
            }
            
            result = await tool.execute(args)
            
            assert result["success"] is True
            assert result["symbol"] == "BTCUSDT"
            assert result["order_id"] == 67890
            assert "Successfully closed" in result["message"]
    
    @pytest.mark.asyncio
    async def test_close_position_invalid_symbol(self):
        """Test closing position with invalid symbol."""
        tool = ClosePositionTool()
        
        args = {
            "symbol": "INVALID",
            "position_side": "BOTH"
        }
        
        result = await tool.execute(args)
        
        assert result["error"] is True
        assert "Invalid symbol" in result["message"]


class TestToolSafetyValidation:
    """Test safety validation across all tools."""
    
    @pytest.mark.asyncio
    async def test_amount_validation_across_tools(self):
        """Test amount validation is consistent across tools."""
        tools = [SpotBuyTool(), FuturesLongTool(), FuturesShortTool()]
        
        for tool in tools:
            # Test with zero amount
            if hasattr(tool, 'validate_trade_amount'):
                result = tool.validate_trade_amount(0)
                assert not result, f"{tool.__class__.__name__} should reject zero amount"
            
            # Test with negative amount
            if hasattr(tool, 'validate_trade_amount'):
                result = tool.validate_trade_amount(-100)
                assert not result, f"{tool.__class__.__name__} should reject negative amount"
    
    @pytest.mark.asyncio  
    async def test_symbol_validation_across_tools(self):
        """Test symbol validation is consistent across tools."""
        tools = [SpotBuyTool(), SpotSellTool(), FuturesLongTool(), FuturesShortTool()]
        
        invalid_symbols = ["BTCUSD", "INVALID", "", "btcusdt"]
        valid_symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        
        for tool in tools:
            for symbol in invalid_symbols:
                args = {"symbol": symbol, "amount_usdt": 100.0}
                if tool.__class__.__name__.startswith("Spot"):
                    args["order_type"] = "MARKET"
                elif tool.__class__.__name__.startswith("Futures"):
                    args["leverage"] = 1
                
                result = await tool.execute(args)
                assert result.get("error") is True, f"{tool.__class__.__name__} should reject {symbol}"

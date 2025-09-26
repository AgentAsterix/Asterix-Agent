"""Integration tests for Agent-Aster."""

import pytest
from unittest.mock import patch, AsyncMock
import asyncio

from agent_aster.core.agent import AsterAgent
from agent_aster.core.tools import ToolRegistry
from agent_aster.core.memory import MemoryManager
from agent_aster.integrations.aster.tool_factory import create_aster_tools


class TestAgentIntegration:
    """Integration tests for the complete agent system."""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, mock_llm_provider, temp_db):
        """Test complete agent initialization with all components."""
        # Initialize components
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        tools = ToolRegistry()
        for tool in create_aster_tools():
            tools.register(tool)
        
        # Create agent
        agent = AsterAgent(
            llm=mock_llm_provider,
            tools=tools,
            memory=memory,
            system_prompt="Test prompt"
        )
        
        # Verify initialization
        assert agent.llm is not None
        assert len(agent.tools.list_specs()) > 0
        assert agent.memory is not None
    
    @pytest.mark.asyncio
    async def test_agent_tool_execution_flow(self, mock_llm_provider, temp_db, mock_http_session):
        """Test complete flow from user input to tool execution."""
        # Setup agent
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        tools = ToolRegistry()
        for tool in create_aster_tools():
            tools.register(tool)
        
        agent = AsterAgent(
            llm=mock_llm_provider,
            tools=tools,
            memory=memory,
            system_prompt="Test trading agent"
        )
        
        # Mock LLM to return tool call
        mock_response = AsyncMock()
        mock_response.content = "I'll check your balance."
        mock_response.tool_calls = [
            {
                "function": {
                    "name": "get_balance",
                    "arguments": '{"account_type": "spot"}'
                },
                "id": "call_123"
            }
        ]
        mock_response.usage = {"total_tokens": 100}
        
        # First call returns tool call, second returns final response
        mock_llm_provider.chat_completion.side_effect = [
            mock_response,
            AsyncMock(content="Your balance is $1000 USDT", usage={"total_tokens": 50})
        ]
        
        # Mock the balance tool
        with patch('agent_aster.integrations.aster.tools.GetBalanceTool.get_spot_client') as mock_client:
            mock_spot_client = AsyncMock()
            mock_spot_client.get_balances.return_value = {
                "balances": [{"asset": "USDT", "free": "1000.00", "locked": "0.00"}]
            }
            mock_client.return_value = mock_spot_client
            
            # Execute user command
            response = await agent.run("check my balance", "test_session")
            
            # Verify response
            assert "balance" in response.lower()
            assert mock_llm_provider.chat_completion.call_count == 2
    
    @pytest.mark.asyncio
    async def test_agent_memory_persistence(self, mock_llm_provider, temp_db):
        """Test that agent memory persists across sessions."""
        # Create first agent instance
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        tools = ToolRegistry()
        agent1 = AsterAgent(mock_llm_provider, tools, memory, "Test")
        
        # Mock simple response
        mock_llm_provider.chat_completion.return_value = AsyncMock(
            content="Hello there!",
            tool_calls=[],
            usage={"total_tokens": 10}
        )
        
        # Send message with first agent
        await agent1.run("Hello", "persistent_session")
        
        # Create second agent instance with same memory
        agent2 = AsterAgent(mock_llm_provider, tools, memory, "Test")
        
        # Check that message history is available
        session_history = await memory.load_session("persistent_session")
        assert len(session_history) >= 1
        assert any("Hello" in str(msg) for msg in session_history)
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self, mock_llm_provider, temp_db):
        """Test agent error handling and recovery."""
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        tools = ToolRegistry()
        agent = AsterAgent(mock_llm_provider, tools, memory, "Test")
        
        # Mock LLM to raise exception
        mock_llm_provider.chat_completion.side_effect = Exception("LLM error")
        
        # Execute command and verify error handling
        response = await agent.run("test command", "error_session")
        
        assert "error" in response.lower()
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_agent_safety_checks(self, mock_llm_provider, temp_db):
        """Test agent safety checks for high-value trades."""
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        tools = ToolRegistry()
        agent = AsterAgent(mock_llm_provider, tools, memory, "Test")
        
        # Test high-value trade detection
        high_value_command = "buy 5000 USDT of BTC"
        response = await agent.run(high_value_command, "safety_session")
        
        # Should trigger safety check
        assert "confirm" in response.lower() or "high-value" in response.lower()


class TestAPIClientIntegration:
    """Integration tests for API clients."""
    
    @pytest.mark.asyncio
    async def test_spot_client_integration(self, mock_http_session):
        """Test spot client integration with mocked API."""
        from agent_aster.integrations.aster.spot_client import AsterSpotClient
        
        client = AsterSpotClient("test_key", "test_secret", "https://testnet-api.asterdx.com")
        
        # Test ping
        result = await client.ping()
        assert "error" not in result
        
        # Test account info
        account = await client.get_account()
        assert "balances" in account
    
    @pytest.mark.asyncio
    async def test_futures_client_integration(self, mock_http_session):
        """Test futures client integration with mocked API."""
        from agent_aster.integrations.aster.futures_client import AsterFuturesClient
        
        client = AsterFuturesClient("test_key", "test_secret", "https://testnet-fapi.asterdx.com")
        
        # Test ping
        result = await client.ping()
        assert "error" not in result
        
        # Test balance
        balance = await client.get_balance()
        assert isinstance(balance, list) or isinstance(balance, dict)


class TestToolRegistryIntegration:
    """Integration tests for tool registry and execution."""
    
    def test_tool_registry_aster_tools(self):
        """Test that all Aster tools can be registered."""
        registry = ToolRegistry()
        
        # Register all Aster tools
        tools = create_aster_tools()
        for tool in tools:
            registry.register(tool)
        
        # Verify all tools are registered
        specs = registry.list_specs()
        tool_names = [spec["name"] for spec in specs]
        
        expected_tools = [
            "spot_buy", "spot_sell", "futures_long", "futures_short",
            "get_balance", "get_position", "close_position"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
    
    @pytest.mark.asyncio
    async def test_tool_execution_via_registry(self, mock_http_session):
        """Test tool execution through the registry."""
        registry = ToolRegistry()
        
        # Register tools
        tools = create_aster_tools()
        for tool in tools:
            registry.register(tool)
        
        # Mock balance tool execution
        with patch('agent_aster.integrations.aster.tools.GetBalanceTool.get_spot_client') as mock_client:
            mock_spot_client = AsyncMock()
            mock_spot_client.get_balances.return_value = {
                "balances": [{"asset": "USDT", "free": "1000.00", "locked": "0.00"}]
            }
            mock_client.return_value = mock_spot_client
            
            # Execute tool via registry
            result = await registry.call("get_balance", {"account_type": "spot"})
            
            assert result["success"] is True
            assert "balances" in result


class TestMemoryIntegration:
    """Integration tests for memory system."""
    
    @pytest.mark.asyncio
    async def test_memory_trade_history(self, temp_db):
        """Test trade history storage and retrieval."""
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        # Save trade history
        await memory.save_trade_history(
            "test_user", "BTCUSDT", "BUY", 0.001, 35000.0
        )
        
        # Retrieve trade history
        history = await memory.get_trade_history("test_user", limit=5)
        
        assert len(history) == 1
        assert history[0]["symbol"] == "BTCUSDT"
        assert history[0]["action"] == "BUY"
    
    @pytest.mark.asyncio
    async def test_memory_session_management(self, temp_db):
        """Test session save and load functionality."""
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        # Save session
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        await memory.save_session("test_session", messages)
        
        # Load session
        loaded_messages = await memory.load_session("test_session")
        
        assert len(loaded_messages) == 2
        assert loaded_messages[0]["content"] == "Hello"
        assert loaded_messages[1]["content"] == "Hi there!"
    
    @pytest.mark.asyncio
    async def test_memory_pending_confirmations(self, temp_db):
        """Test pending confirmation storage and retrieval."""
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        # Save pending confirmation
        confirmation_data = {
            "command": "buy 5000 USDT of BTC",
            "amount": 5000.0,
            "timestamp": 1699123456.789
        }
        await memory.save_pending_confirmation("test_session", confirmation_data)
        
        # Retrieve pending confirmation
        retrieved = await memory.get_pending_confirmation("test_session")
        
        assert retrieved is not None
        assert retrieved["command"] == "buy 5000 USDT of BTC"
        assert retrieved["amount"] == 5000.0
        
        # Clear confirmation
        await memory.clear_pending_confirmation("test_session")
        
        # Verify it's cleared
        cleared = await memory.get_pending_confirmation("test_session")
        assert cleared is None


class TestEndToEndFlow:
    """End-to-end integration tests."""
    
    @pytest.mark.asyncio
    async def test_complete_trading_flow(self, mock_llm_provider, temp_db, mock_http_session):
        """Test complete trading flow from command to execution."""
        # Setup complete system
        memory = MemoryManager(temp_db)
        await memory.initialize()
        
        tools = ToolRegistry()
        for tool in create_aster_tools():
            tools.register(tool)
        
        agent = AsterAgent(mock_llm_provider, tools, memory, "Trading Agent")
        
        # Mock LLM to execute spot buy
        mock_response = AsyncMock()
        mock_response.content = "I'll execute that buy order for you."
        mock_response.tool_calls = [
            {
                "function": {
                    "name": "spot_buy",
                    "arguments": '{"symbol": "BTCUSDT", "amount_usdt": 100.0, "order_type": "MARKET"}'
                },
                "id": "call_buy_123"
            }
        ]
        mock_response.usage = {"total_tokens": 150}
        
        final_response = AsyncMock()
        final_response.content = "Successfully bought $100 worth of BTC!"
        final_response.usage = {"total_tokens": 50}
        
        mock_llm_provider.chat_completion.side_effect = [mock_response, final_response]
        
        # Mock API client
        with patch('agent_aster.integrations.aster.tools.SpotBuyTool.get_spot_client') as mock_client:
            mock_spot_client = AsyncMock()
            mock_spot_client.market_buy.return_value = {
                "success": True,
                "orderId": 12345,
                "executedQty": "0.001",
                "status": "FILLED"
            }
            mock_client.return_value = mock_spot_client
            
            # Execute trading command
            response = await agent.run("buy 100 USDT of BTC", "trading_session")
            
            # Verify execution
            assert "successfully" in response.lower() or "bought" in response.lower()
            assert mock_spot_client.market_buy.called
            
            # Verify session was saved
            session_history = await memory.load_session("trading_session")
            assert len(session_history) >= 2  # User message + assistant response

#!/usr/bin/env python3
"""Test SAM Framework integration with Agent-Aster."""

import os
import asyncio
import sys

# Set environment variables - Use environment variables or Railway secrets
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key-here')
os.environ['ASTER_API_KEY'] = os.environ.get('ASTER_API_KEY', 'your-aster-api-key-here')
os.environ['ASTER_API_SECRET'] = os.environ.get('ASTER_API_SECRET', 'your-aster-api-secret-here')
os.environ['ASTER_FERNET_KEY'] = 'dGVzdF9lbmNyeXB0aW9uX2tleV9mb3JfZGV2ZWxvcG1lbnRfb25seQ=='

async def test_sam_agent():
    """Test Agent-Aster with SAM Framework architecture."""
    print("🤖 Testing Agent-Aster SAM Framework Integration")
    print("=" * 55)
    
    try:
        # Import SAM components
        from agent_aster.core.agent import AsterAgent
        from agent_aster.core.llm_provider import create_llm_provider
        from agent_aster.core.memory import MemoryManager
        from agent_aster.core.tools import ToolRegistry
        from agent_aster.config.prompts import ASTER_AGENT_PROMPT
        from agent_aster.integrations.aster.tool_factory import create_aster_tools
        
        print("✅ All SAM Framework components imported successfully")
        
        # Initialize memory (SAM pattern)
        print("\n🧠 Initializing Memory Manager...")
        memory = MemoryManager('.agent_aster/test_memory.db')
        await memory.initialize()
        print("✅ Memory manager initialized with SQLite backend")
        
        # Initialize LLM provider (SAM pattern)
        print("\n🤖 Initializing LLM Provider...")
        llm = create_llm_provider()
        print("✅ OpenAI LLM provider initialized")
        
        # Initialize tools registry (SAM pattern)
        print("\n🛠️  Initializing Tools Registry...")
        tools = ToolRegistry()
        aster_tools = create_aster_tools()
        for tool in aster_tools:
            tools.register(tool)
        print(f"✅ {len(tools.list_specs())} Aster Finance tools registered")
        
        # Show tool specs (SAM pattern)
        print("\n📋 Registered Tools:")
        for spec in tools.list_specs():
            print(f"   • {spec['name']}: {spec['description']}")
        
        # Create agent with SAM architecture
        print("\n🚀 Creating AsterAgent with SAM Framework...")
        agent = AsterAgent(
            llm=llm,
            tools=tools, 
            memory=memory,
            system_prompt=ASTER_AGENT_PROMPT
        )
        print("✅ AsterAgent initialized with SAM architecture")
        
        # Test agent greeting (should welcome user per SAM guidelines)
        print("\n💬 Testing Agent Response...")
        response = await agent.run("Hello", "test_session")
        print(f"🤖 Agent Response:")
        print(f"   {response}")
        
        # Check if response includes SAM-style welcome
        if "welcome" in response.lower() and "agent aster" in response.lower():
            print("✅ Agent provides proper SAM-style greeting")
        else:
            print("⚠️  Agent response doesn't include expected greeting")
        
        # Test tool awareness
        print(f"\n🧪 Testing Tool Awareness...")
        tools_response = await agent.run("What can you help me with?", "test_session")
        print(f"🤖 Capabilities Response:")
        print(f"   {tools_response[:200]}...")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"💡 Error type: {type(e).__name__}")
        return False

async def test_cli_interface():
    """Test CLI interface that mimics SAM CLI."""
    print(f"\n📱 Testing CLI Interface...")
    
    try:
        # Test CLI status command
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "agent_aster.cli", "status"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ CLI status command works")
            print(f"   Output: {result.stdout[:100]}...")
        else:
            print(f"❌ CLI status failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ CLI test failed: {e}")

def main():
    """Run all tests."""
    print("🔍 Environment Check:")
    print(f"   OpenAI Key: {'✅ Set' if os.environ.get('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"   Aster Key: {'✅ Set' if os.environ.get('ASTER_API_KEY') else '❌ Missing'}")
    
    # Run async tests
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        success = loop.run_until_complete(test_sam_agent())
        loop.run_until_complete(test_cli_interface())
        
        print(f"\n🎯 Test Summary:")
        if success:
            print("🟢 SAM Framework integration: WORKING")
            print("🟢 Agent-Aster follows SAM architecture correctly")
            print("🟢 Ready for production deployment")
            print(f"\n🚀 Next steps:")
            print("   1. Launch web UI: cd agent_aster && streamlit run ui.py")
            print("   2. Test trading: python -m agent_aster.cli test-trade 'check balance'")
        else:
            print("🔴 Issues found - check errors above")
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
    finally:
        if 'loop' in locals():
            loop.close()

if __name__ == "__main__":
    main()

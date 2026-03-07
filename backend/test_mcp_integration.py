#!/usr/bin/env python3.11
"""
Test MCP integration with the API.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.mcp_agent import MCPSQLAnalyticsAgent


async def test_mcp_agent():
    """Test MCP agent integration."""
    print("🧪 Testing MCP Agent Integration...")
    print("=" * 60)
    
    # Initialize agent
    print("\n1️⃣  Initializing MCP Agent...")
    try:
        agent = MCPSQLAnalyticsAgent()
        print("   ✅ Agent initialized successfully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test sample queries
    print("\n2️⃣  Getting sample queries...")
    try:
        samples = agent.get_sample_queries()
        print(f"   ✅ Got {len(samples)} sample queries:")
        for i, sample in enumerate(samples[:3], 1):
            print(f"      {i}. {sample}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test simple query
    print("\n3️⃣  Testing query: 'How many customers do we have?'")
    try:
        result = await agent.query("How many customers do we have?")
        print(f"   ✅ Query completed!")
        print(f"   SQL: {result.get('sql_query')}")
        if result.get('results'):
            print(f"   Results: {result['results'].get('data')}")
        print(f"   Response: {result.get('response')[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test another query
    print("\n4️⃣  Testing query: 'What are the top 3 products by price?'")
    try:
        result = await agent.query("What are the top 3 products by price?")
        print(f"   ✅ Query completed!")
        print(f"   SQL: {result.get('sql_query')}")
        if result.get('results') and result['results'].get('success'):
            print(f"   Row count: {result['results'].get('row_count')}")
            print(f"   Columns: {result['results'].get('columns')}")
        print(f"   Response: {result.get('response')[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ MCP Agent Integration Test Completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Test via API: curl -X POST http://localhost:8000/api/query/mcp \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"question\": \"How many customers do we have?\"}'")
    print("  2. Test via web UI with use_mcp flag")
    print("  3. Compare results with direct agent")


if __name__ == "__main__":
    asyncio.run(test_mcp_agent())

# Made with Bob

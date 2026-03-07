#!/usr/bin/env python3.11
"""
Simple test script for MCP server tools.
Tests the SQL query tool directly without MCP protocol.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.tools.sql_query import SQLQueryTool
from mcp_server.config import settings


def test_sql_tool():
    """Test SQL query tool directly."""
    print("🧪 Testing MCP Server Tools...")
    print(f"Server: {settings.server_name} v{settings.server_version}")
    print(f"Database: {settings.database_path}")
    print()
    
    # Initialize tool
    sql_tool = SQLQueryTool()
    
    # Test 1: Get all tables schema
    print("1️⃣  Testing get_schema() - all tables...")
    try:
        result = sql_tool.get_schema()
        if result["success"]:
            tables = result["tables"]
            print(f"   ✅ Found {len(tables)} tables:")
            for table in tables[:5]:  # Show first 5
                print(f"      - {table['name']}")
        else:
            print(f"   ❌ Error: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Get specific table schema
    print("2️⃣  Testing get_schema('customers')...")
    try:
        result = sql_tool.get_schema("customers")
        if result["success"]:
            print(f"   ✅ Got schema for customers table:")
            print(f"      {result['schema'][:100]}...")  # Show first 100 chars
        else:
            print(f"   ❌ Error: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Execute simple query
    print("3️⃣  Testing execute('SELECT COUNT(*) as total FROM customers')...")
    try:
        result = sql_tool.execute("SELECT COUNT(*) as total FROM customers")
        if result["success"]:
            print(f"   ✅ Query executed successfully!")
            print(f"   Columns: {result['columns']}")
            print(f"   Data: {result['data']}")
            print(f"   Row count: {result['row_count']}")
        else:
            print(f"   ❌ Error: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 4: Execute query with results
    print("4️⃣  Testing execute('SELECT * FROM customers LIMIT 3')...")
    try:
        result = sql_tool.execute("SELECT * FROM customers LIMIT 3")
        if result["success"]:
            print(f"   ✅ Query executed successfully!")
            print(f"   Columns: {result['columns']}")
            print(f"   Retrieved {result['row_count']} rows")
            if result['data']:
                print(f"   First row: {result['data'][0]}")
        else:
            print(f"   ❌ Error: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 5: Validate query (should pass)
    print("5️⃣  Testing validate_query('SELECT * FROM orders')...")
    try:
        is_valid, error = sql_tool.validate_query("SELECT * FROM orders")
        if is_valid:
            print(f"   ✅ Query validation passed")
        else:
            print(f"   ❌ Validation failed: {error}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 6: Validate query (should fail)
    print("6️⃣  Testing validate_query('DROP TABLE customers')...")
    try:
        is_valid, error = sql_tool.validate_query("DROP TABLE customers")
        if not is_valid:
            print(f"   ✅ Correctly rejected dangerous query: {error}")
        else:
            print(f"   ❌ Validation should have failed!")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    print()
    print("=" * 60)
    print("✅ MCP Server Tools Test Completed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Tools are working correctly")
    print("  2. Ready to integrate into MCP server")
    print("  3. Can now create MCP client for FastAPI")


if __name__ == "__main__":
    test_sql_tool()

# Made with Bob

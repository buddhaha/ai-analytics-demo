"""
MCP Server for SQL Analytics
Exposes database tools via Model Context Protocol.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from .tools.sql_query import SQLQueryTool
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
app = Server(settings.server_name)

# Initialize tools
sql_tool = SQLQueryTool()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="sql_query",
            description="Execute SQL SELECT queries on the e-commerce database. "
                       "Returns query results with row data and metadata. "
                       "Only SELECT statements are allowed for safety.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query to execute"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_schema",
            description="Get database schema information. Can retrieve schema for "
                       "a specific table or all tables in the database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Optional: specific table name to get schema for"
                    }
                }
            }
        ),
        Tool(
            name="list_tables",
            description="List all tables in the database with their names.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "sql_query":
            # Execute SQL query
            query = arguments.get("query", "")
            if not query:
                return [TextContent(
                    type="text",
                    text="Error: 'query' parameter is required"
                )]
            
            logger.info(f"Executing SQL query: {query[:100]}...")
            result = sql_tool.execute(query)
            
            if result["success"]:
                response_text = f"Query executed successfully.\n"
                response_text += f"Rows returned: {result['row_count']}\n"
                if result.get("truncated"):
                    response_text += f"(Results truncated to {settings.max_query_results} rows)\n"
                response_text += f"\nColumns: {', '.join(result['columns'])}\n"
                response_text += f"\nData:\n{result['data']}"
                
                return [TextContent(
                    type="text",
                    text=response_text
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Query failed: {result['error']}"
                )]
        
        elif name == "get_schema":
            # Get schema information
            table_name = arguments.get("table_name")
            logger.info(f"Getting schema for: {table_name or 'all tables'}")
            result = sql_tool.get_schema(table_name)
            
            if result["success"]:
                if "table" in result:
                    # Single table schema
                    response_text = f"Schema for table '{result['table']}':\n\n"
                    response_text += result["schema"]
                else:
                    # All tables
                    response_text = f"Database schema ({len(result['tables'])} tables):\n\n"
                    for table in result["tables"]:
                        response_text += f"Table: {table['name']}\n"
                        response_text += f"{table['schema']}\n\n"
                
                return [TextContent(
                    type="text",
                    text=response_text
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Schema retrieval failed: {result['error']}"
                )]
        
        elif name == "list_tables":
            # List all tables
            logger.info("Listing all tables")
            result = sql_tool.get_schema()
            
            if result["success"]:
                tables = [table["name"] for table in result["tables"]]
                response_text = f"Available tables ({len(tables)}):\n"
                response_text += "\n".join(f"- {table}" for table in tables)
                
                return [TextContent(
                    type="text",
                    text=response_text
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to list tables: {result['error']}"
                )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error in tool call: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"Error executing tool: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    logger.info(f"Starting {settings.server_name} v{settings.server_version}")
    logger.info(f"Database: {sql_tool.db_path}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob

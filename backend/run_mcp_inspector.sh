#!/bin/bash
# Launch MCP Inspector with our SQL Analytics MCP Server
# This provides a web UI to test and debug the MCP server

echo "🔍 Starting MCP Inspector..."
echo "This will open a web UI at http://localhost:6274"
echo ""
echo "In the Inspector UI, you can:"
echo "  - View all available tools"
echo "  - Test tool calls manually"
echo "  - See request/response logs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"

# Load environment variables (but MCP server doesn't need them)
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate virtual environment
source venv/bin/activate

# Run MCP Inspector with our server
# The inspector will handle the stdio communication
npx @modelcontextprotocol/inspector python3.11 -m mcp_server.server

# Made with Bob

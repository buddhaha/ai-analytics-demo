# MCP Inspector Setup Guide

## Authentication Issue

If the MCP Inspector asks for authentication when starting, this is likely because:

1. **The Inspector itself may require authentication** - Some versions of the MCP Inspector have authentication features
2. **Environment variables** - The inspector might be looking for API keys

## Solution: Skip Authentication

The MCP Inspector authentication is optional for local development. Here's how to handle it:

### Option 1: Use "Skip" or "Cancel"
When the authentication dialog appears, look for:
- A "Skip" button
- A "Cancel" button  
- An "X" to close the dialog
- A "Continue without authentication" option

The inspector should work without authentication for local MCP servers.

### Option 2: Provide Dummy Credentials
If authentication is required, you can provide dummy values:
- Username: `admin`
- Password: `admin`

### Option 3: Run Without Inspector
You can test the MCP server directly without the Inspector:

```bash
cd backend
source venv/bin/activate
python3.11 test_mcp_server.py
```

This runs our custom test script that doesn't require authentication.

## Alternative: Direct MCP Server Testing

### Method 1: Python Test Script
```bash
cd backend
source venv/bin/activate
python3.11 test_mcp_server.py
```

This will:
- Initialize the MCP server
- Test all 3 tools (sql_query, get_schema, list_tables)
- Show results in the terminal
- No authentication needed

### Method 2: Manual Testing
You can also test the MCP server by integrating it into our existing web app (next step in the implementation).

## Understanding MCP Inspector Authentication

The MCP Inspector is a debugging tool that:
- Provides a web UI to interact with MCP servers
- May have optional authentication for security
- Is NOT required for the MCP server to work
- Is only needed for debugging/testing

**Important:** Our MCP server itself does NOT require authentication. It's a local tool that:
- Reads from a local SQLite database
- Runs on your machine
- Doesn't expose any external APIs
- Only accepts SELECT queries (read-only)

## Next Steps

If you want to skip the Inspector entirely and see the MCP server in action:

1. **Test with Python script:**
   ```bash
   cd backend
   ./test_mcp_server.py
   ```

2. **Integrate into web app** (recommended):
   - We'll create an MCP client in the FastAPI backend
   - The client will connect to the MCP server
   - You'll use the existing web UI at http://localhost:5173
   - No authentication needed

3. **Use Claude Desktop** (optional):
   - Configure Claude Desktop to use our MCP server
   - See MCP_USAGE_GUIDE.md for instructions

## Troubleshooting

### Inspector won't start
```bash
# Check if inspector is installed
npm list -g @modelcontextprotocol/inspector

# Reinstall if needed
npm install -g @modelcontextprotocol/inspector
```

### Authentication keeps appearing
This is normal for some versions of the Inspector. Just skip it or use the Python test script instead.

### Want to see MCP in action without Inspector?
Run the test script:
```bash
cd backend
source venv/bin/activate
python3.11 test_mcp_server.py
```

This will show you all the MCP tools working without any UI or authentication.
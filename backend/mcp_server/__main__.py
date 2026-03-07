"""
Entry point for running MCP server as a module.
Usage: python -m mcp_server.server
"""

from .server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob

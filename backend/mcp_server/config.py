"""
MCP Server Configuration
Settings for the SQL Analytics MCP server.
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class MCPServerSettings(BaseSettings):
    """Configuration for MCP server."""
    
    # Server identification
    server_name: str = "sql-analytics-mcp"
    server_version: str = "1.0.0"
    
    # Database configuration
    database_path: str = "../database/ecommerce.db"
    
    # Query limits and safety
    max_query_results: int = 1000
    query_timeout: int = 30  # seconds
    
    # Allowed SQL operations
    allowed_operations: list[str] = ["SELECT"]
    
    # Dangerous keywords to block
    dangerous_keywords: list[str] = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", 
        "CREATE", "TRUNCATE", "REPLACE", "GRANT", "REVOKE"
    ]
    
    class Config:
        env_file = ".env"
        env_prefix = "MCP_"
        extra = "ignore"  # Ignore extra fields from .env


# Global settings instance
settings = MCPServerSettings()

# Made with Bob

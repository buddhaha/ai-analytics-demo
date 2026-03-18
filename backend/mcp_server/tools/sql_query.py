"""
SQL Query Tool for MCP Server
Executes SELECT queries with safety validation.
"""

import sqlite3
import re
from pathlib import Path
from typing import Any, Dict, List
from ..config import settings


class SQLQueryTool:
    """Tool for executing SQL queries safely."""
    
    def __init__(self):
        """Initialize the SQL query tool."""
        self.db_path = self._resolve_db_path()
        
    def _resolve_db_path(self) -> Path:
        """Resolve the database path relative to this file."""
        # Path: sql_query.py -> tools -> mcp_server -> backend -> project_root
        project_root = Path(__file__).parent.parent.parent.parent
        db_path = project_root / settings.database_path.lstrip("../")
        
        if not db_path.exists():
            raise FileNotFoundError(f"Database not found at: {db_path}")
            
        return db_path
    
    def validate_query(self, query: str) -> tuple[bool, str]:
        """
        Validate SQL query for safety.
        
        Args:
            query: SQL query string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        query_upper = query.upper().strip()
        
        # Check for dangerous keywords (but allow them in function calls)
        for keyword in settings.dangerous_keywords:
            # Use word boundaries and check it's not part of a function call
            pattern = rf'\b{keyword}\b(?!\s*\()'
            if re.search(pattern, query_upper):
                return False, f"Query contains forbidden keyword: {keyword}"
        
        # Ensure query is SELECT only
        if not query_upper.startswith("SELECT"):
            return False, "Only SELECT queries are allowed"
        
        # Check for multiple statements (SQL injection attempt)
        statements = query.split(";")
        if len(statements) > 2 or (len(statements) == 2 and statements[1].strip()):
            return False, "Multiple SQL statements are not allowed"
        
        return True, ""
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute SQL query and return results.
        
        Args:
            query: SQL SELECT query to execute
            
        Returns:
            Dictionary with success status, data, and metadata
        """
        # Validate query first
        is_valid, error = self.validate_query(query)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "data": [],
                "row_count": 0
            }
        
        try:
            # Connect to database
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Execute query with timeout
            cursor.execute(f"PRAGMA busy_timeout = {settings.query_timeout * 1000}")
            cursor.execute(query)
            
            # Fetch results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows[:settings.max_query_results]:
                results.append(dict(row))
            
            # Get column names
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            cursor.close()
            conn.close()
            
            return {
                "success": True,
                "data": results,
                "row_count": len(results),
                "columns": columns,
                "truncated": len(rows) > settings.max_query_results
            }
            
        except sqlite3.Error as e:
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "data": [],
                "row_count": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "data": [],
                "row_count": 0
            }
    
    def get_schema(self, table_name: str = None) -> Dict[str, Any]:
        """
        Get database schema information.
        
        Args:
            table_name: Optional specific table name
            
        Returns:
            Dictionary with schema information
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            if table_name:
                # Get specific table schema
                cursor.execute(
                    "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,)
                )
                result = cursor.fetchone()
                
                if not result:
                    return {
                        "success": False,
                        "error": f"Table '{table_name}' not found"
                    }
                
                schema_info = {
                    "success": True,
                    "table": table_name,
                    "schema": result[0]
                }
            else:
                # Get all tables
                cursor.execute(
                    "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                tables = cursor.fetchall()
                
                schema_info = {
                    "success": True,
                    "tables": [
                        {"name": name, "schema": sql}
                        for name, sql in tables
                        if name != "sqlite_sequence"
                    ]
                }
            
            cursor.close()
            conn.close()
            
            return schema_info
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error retrieving schema: {str(e)}"
            }

# Made with Bob

"""
SQL Agent using LangChain and OpenAI GPT-4 for natural language to SQL translation.
Includes safety validations and query execution.
"""

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.callbacks.base import BaseCallbackHandler
from typing import Dict, Any, List, Optional
import re
import sqlite3
from ..config import settings
from ..database import get_db_connection

# Langfuse integration
try:
    from langfuse import Langfuse
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    Langfuse = None
    LangfuseCallbackHandler = None


class SQLCaptureCallback(BaseCallbackHandler):
    """Callback handler to capture SQL queries and results."""
    
    def __init__(self):
        self.sql_queries: List[str] = []
        self.last_sql: Optional[str] = None
        
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        """Capture SQL queries when sql_db_query tool is called."""
        tool_name = serialized.get("name", "")
        if tool_name == "sql_db_query":
            # Extract SQL from input
            if isinstance(input_str, dict):
                sql = input_str.get("query", "")
                self.last_sql = sql
                self.sql_queries.append(sql)
            elif isinstance(input_str, str):
                # Try to parse as dict string representation
                import ast
                try:
                    parsed = ast.literal_eval(input_str)
                    if isinstance(parsed, dict):
                        sql = parsed.get("query", input_str)
                        self.last_sql = sql
                        self.sql_queries.append(sql)
                    else:
                        self.last_sql = input_str
                        self.sql_queries.append(input_str)
                except (ValueError, SyntaxError):
                    # If parsing fails, use as-is
                    self.last_sql = input_str
                    self.sql_queries.append(input_str)


class SQLAnalyticsAgent:
    """
    AI Agent for analyzing e-commerce data using natural language queries.
    Uses OpenAI GPT-4 via LangChain to convert questions to SQL and analyze results.
    """
    
    # Dangerous SQL keywords that should be blocked
    DANGEROUS_KEYWORDS = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE",
        "TRUNCATE", "REPLACE", "GRANT", "REVOKE", "EXEC", "EXECUTE"
    ]
    
    def __init__(self):
        """Initialize the SQL agent with OpenAI and database connection."""
        # Initialize Langfuse callback if enabled
        self.langfuse_handler = None
        self.langfuse_client = None
        if settings.langfuse_enabled and LANGFUSE_AVAILABLE:
            try:
                print(f"🔍 Initializing Langfuse with host: {settings.langfuse_host}")
                # Initialize Langfuse client
                self.langfuse_client = Langfuse(
                    public_key=settings.langfuse_public_key,
                    secret_key=settings.langfuse_secret_key,
                    host=settings.langfuse_host
                )
                # Create callback handler
                self.langfuse_handler = LangfuseCallbackHandler(
                    public_key=settings.langfuse_public_key
                )
                print("✅ Langfuse handler initialized successfully")
            except Exception as e:
                print(f"❌ Warning: Failed to initialize Langfuse: {e}")
                import traceback
                traceback.print_exc()
                self.langfuse_handler = None
                self.langfuse_client = None
        elif not settings.langfuse_enabled:
            print("ℹ️  Langfuse is disabled in settings")
        elif not LANGFUSE_AVAILABLE:
            print("⚠️  Langfuse package not available")
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            openai_api_key=settings.openai_api_key,
            temperature=0,
            max_tokens=4096
        )
        
        # Connect to SQLite database
        db_url = settings.database_url.replace("sqlite:///", "sqlite:///")
        self.db = SQLDatabase.from_uri(db_url)
        
        # Create SQL agent with the new API
        self.agent = create_sql_agent(
            llm=self.llm,
            db=self.db,
            verbose=settings.debug,
            agent_type="openai-tools",
        )
        
        # Initialize callback handler
        self.sql_callback = SQLCaptureCallback()
    
    def validate_query(self, query: str) -> tuple[bool, str]:
        """
        Validate SQL query for safety.
        
        Args:
            query: SQL query string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        query_upper = query.upper()
        
        # Check for dangerous keywords (but allow them in function calls)
        for keyword in self.DANGEROUS_KEYWORDS:
            # Use word boundaries and check it's not part of a function call
            pattern = rf'\b{keyword}\b(?!\s*\()'
            if re.search(pattern, query_upper):
                return False, f"Query contains forbidden keyword: {keyword}"
        
        # Ensure query is SELECT only
        if not query_upper.strip().startswith("SELECT"):
            return False, "Only SELECT queries are allowed"
        
        # Check for multiple statements (SQL injection attempt)
        # Allow semicolons in string literals and at the end
        statements = query.split(";")
        if len(statements) > 2 or (len(statements) == 2 and statements[1].strip()):
            return False, "Multiple SQL statements are not allowed"
        
        return True, ""
    
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results.
        
        Args:
            sql: SQL query to execute
            
        Returns:
            List of dictionaries containing query results
        """
        # Validate query first
        is_valid, error = self.validate_query(sql)
        if not is_valid:
            raise ValueError(f"Invalid query: {error}")
        
        # Execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        finally:
            cursor.close()
            conn.close()
    
    def analyze_results(self, question: str, sql: str, results: List[Dict[str, Any]]) -> str:
        """
        Use OpenAI to analyze query results and generate insights.
        
        Args:
            question: Original user question
            sql: SQL query that was executed
            results: Query results
            
        Returns:
            AI-generated analysis and insights
        """
        if not results:
            return "No data found for this query."
        
        # Prepare context for OpenAI
        results_summary = f"Found {len(results)} results."
        if len(results) <= 10:
            results_text = str(results)
        else:
            results_text = f"First 10 results: {str(results[:10])}\n... and {len(results) - 10} more"
        
        analysis_prompt = f"""
You are a data analyst. Analyze the following query results and provide insights.

Original Question: {question}
SQL Query: {sql}
Results: {results_summary}
{results_text}

Provide:
1. A brief summary of what the data shows
2. Key insights or patterns
3. Any notable trends or anomalies
4. Actionable recommendations if applicable

Keep your response concise and focused on business value.
"""
        
        # Prepare callbacks
        callbacks = [self.langfuse_handler] if self.langfuse_handler else []
        
        response = self.llm.invoke(
            analysis_prompt,
            config={"callbacks": callbacks} if callbacks else {}
        )
        return response.content
    
    def determine_visualization(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determine the best visualization type for the results.
        
        Args:
            question: Original user question
            results: Query results
            
        Returns:
            Visualization configuration
        """
        if not results:
            return {"type": "none"}
        
        # Get column names and types
        columns = list(results[0].keys())
        num_columns = len(columns)
        num_rows = len(results)
        
        # Determine if we have numeric data
        numeric_columns = []
        for col in columns:
            if any(isinstance(results[i].get(col), (int, float)) for i in range(min(5, len(results)))):
                numeric_columns.append(col)
        
        # Decision logic for chart type
        viz_config = {
            "type": "table",  # Default
            "data": results,
            "columns": columns
        }
        
        # Time series detection
        time_keywords = ["date", "month", "year", "day", "time", "period"]
        has_time_column = any(any(kw in col.lower() for kw in time_keywords) for col in columns)
        
        if has_time_column and len(numeric_columns) >= 1 and num_rows > 1:
            viz_config["type"] = "line"
            viz_config["xAxis"] = columns[0]
            viz_config["yAxis"] = numeric_columns[0] if numeric_columns else columns[1]
        
        # Bar chart for comparisons
        elif num_rows <= 20 and len(numeric_columns) >= 1:
            viz_config["type"] = "bar"
            viz_config["xAxis"] = columns[0]
            viz_config["yAxis"] = numeric_columns[0] if numeric_columns else columns[1]
        
        # Pie chart for distributions (small number of categories)
        elif num_rows <= 10 and len(numeric_columns) == 1:
            question_lower = question.lower()
            if any(word in question_lower for word in ["distribution", "breakdown", "share", "percentage", "proportion"]):
                viz_config["type"] = "pie"
                viz_config["nameKey"] = columns[0]
                viz_config["valueKey"] = numeric_columns[0]
        
        return viz_config
    
    async def process_query(self, question: str) -> Dict[str, Any]:
        """
        Process a natural language question and return results with analysis.
        
        Args:
            question: Natural language question from user
            
        Returns:
            Dictionary containing SQL, results, analysis, and visualization config
        """
        try:
            # Reset callback
            self.sql_callback = SQLCaptureCallback()
            
            # Prepare callbacks list
            callbacks = [self.sql_callback]
            if self.langfuse_handler:
                callbacks.append(self.langfuse_handler)
            
            # Use agent to generate and execute SQL with callbacks
            response = self.agent.invoke(
                {"input": question},
                config={"callbacks": callbacks}
            )
            
            # Get the last SQL query from callback
            sql_query = self.sql_callback.last_sql
            
            # Execute query to get results if we have SQL
            results = []
            if sql_query:
                try:
                    # Ensure it's a string
                    if isinstance(sql_query, dict):
                        sql_query = sql_query.get("query", "")
                    
                    if isinstance(sql_query, str) and sql_query.strip():
                        results = self.execute_query(sql_query)
                except Exception as e:
                    # Log error but don't fail the request
                    print(f"Error executing SQL: {e}")
            
            # Get the final answer from the agent
            analysis = response.get("output", "No analysis available.")
            
            # Determine visualization
            viz_config = self.determine_visualization(question, results)
            
            return {
                "success": True,
                "question": question,
                "sql": sql_query,
                "results": results,
                "analysis": analysis,
                "visualization": viz_config,
                "row_count": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "question": question,
                "error": str(e),
                "sql": None,
                "results": [],
                "analysis": f"Error processing query: {str(e)}",
                "visualization": {"type": "none"},
                "row_count": 0
            }
    
    def get_schema_info(self) -> str:
        """Get database schema information."""
        return self.db.get_table_info()
    
    def get_sample_queries(self) -> List[str]:
        """Return sample queries users can try."""
        return [
            "Show me the top 10 customers by total revenue",
            "What are the best selling products this year?",
            "Compare monthly sales for 2024 vs 2025",
            "Which product categories have the highest profit margins?",
            "Show me customers who haven't ordered in the last 3 months",
            "What is the average order value by country?",
            "Which products have low ratings but high sales?",
            "Show me the revenue trend for the last 12 months",
            "What are the top 5 products in the Electronics category?",
            "How many orders are pending or processing?"
        ]


# Global agent instance
_agent_instance = None


def get_agent() -> SQLAnalyticsAgent:
    """Get or create the global agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SQLAnalyticsAgent()
    return _agent_instance

# Made with Bob

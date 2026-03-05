"""
SQL Agent using LangChain and Claude for natural language to SQL translation.
Includes safety validations and query execution.
"""

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from typing import Dict, Any, List
import re
import sqlite3
from ..config import settings
from ..database import get_db_connection


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
            return_intermediate_steps=True,  # Enable intermediate steps
        )
    
    def validate_query(self, query: str) -> tuple[bool, str]:
        """
        Validate SQL query for safety.
        
        Args:
            query: SQL query string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        query_upper = query.upper()
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            if re.search(rf'\b{keyword}\b', query_upper):
                return False, f"Query contains forbidden keyword: {keyword}"
        
        # Ensure query is SELECT only
        if not query_upper.strip().startswith("SELECT"):
            return False, "Only SELECT queries are allowed"
        
        # Check for multiple statements (SQL injection attempt)
        if ";" in query[:-1]:  # Allow trailing semicolon
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
        Use Claude to analyze query results and generate insights.
        
        Args:
            question: Original user question
            sql: SQL query that was executed
            results: Query results
            
        Returns:
            AI-generated analysis and insights
        """
        if not results:
            return "No data found for this query."
        
        # Prepare context for Claude
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
        
        response = self.llm.invoke(analysis_prompt)
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
            # Use agent to generate and execute SQL
            response = self.agent.invoke({"input": question})
            
            # Debug: Print response structure
            print(f"\n=== Agent Response Structure ===")
            print(f"Keys: {response.keys()}")
            print(f"Intermediate steps count: {len(response.get('intermediate_steps', []))}")
            
            # Extract SQL and results from agent's intermediate steps
            sql_query = None
            results = []
            
            for i, step in enumerate(response.get("intermediate_steps", [])):
                print(f"\n--- Step {i} ---")
                if len(step) >= 2:
                    action, observation = step[0], step[1]
                    print(f"Action type: {type(action)}")
                    print(f"Has 'tool' attr: {hasattr(action, 'tool')}")
                    
                    if hasattr(action, "tool"):
                        print(f"Tool name: {action.tool}")
                        
                        # Check if this is a SQL query action
                        if action.tool == "sql_db_query":
                            print(f"Found SQL query action!")
                            print(f"Has 'tool_input' attr: {hasattr(action, 'tool_input')}")
                            
                            if hasattr(action, "tool_input"):
                                print(f"Tool input type: {type(action.tool_input)}")
                                print(f"Tool input: {action.tool_input}")
                                
                                # Extract SQL from tool_input
                                if isinstance(action.tool_input, dict):
                                    sql_query = action.tool_input.get("query", "")
                                elif isinstance(action.tool_input, str):
                                    sql_query = action.tool_input
                                
                                print(f"Extracted SQL: {sql_query}")
                                
                                # Execute query to get results
                                if sql_query:
                                    try:
                                        results = self.execute_query(sql_query)
                                        print(f"Query executed successfully, got {len(results)} results")
                                    except Exception as e:
                                        print(f"Error executing query: {e}")
            
            print(f"\n=== Final Extraction ===")
            print(f"SQL: {sql_query}")
            print(f"Results count: {len(results)}")
            
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

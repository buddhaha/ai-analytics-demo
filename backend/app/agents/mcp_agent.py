"""
MCP-based SQL Analytics Agent
Uses Model Context Protocol tools with direct LLM integration.
"""

import json
import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from mcp_server.tools.sql_query import SQLQueryTool

# Langfuse integration
try:
    from langfuse import Langfuse
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    Langfuse = None
    LangfuseCallbackHandler = None

logger = logging.getLogger(__name__)


class MCPSQLAnalyticsAgent:
    """
    SQL Analytics Agent using MCP tools.
    
    This agent uses the MCP server's SQL tools to query the database
    and provide analytical insights using a simpler, more direct approach.
    """
    
    def __init__(self):
        """Initialize the MCP-based agent."""
        # Initialize Langfuse callback if enabled
        self.langfuse_handler = None
        self.langfuse_client = None
        if settings.langfuse_enabled and LANGFUSE_AVAILABLE:
            try:
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
                logger.info("✅ Langfuse handler initialized for MCP agent")
            except Exception as e:
                logger.warning(f"Failed to initialize Langfuse: {e}")
                self.langfuse_handler = None
                self.langfuse_client = None
        
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0,
            api_key=settings.openai_api_key
        )
        
        # Initialize MCP SQL tool
        self.sql_tool = SQLQueryTool()
        
        # Track last SQL query
        self.last_sql_query: Optional[str] = None
        self.last_results: Optional[Dict[str, Any]] = None
        
        # System prompt
        self.system_prompt = """You are a SQL analytics expert helping users analyze an e-commerce database.

Database Schema:
- customers: Customer information (id, name, email, country, city, registration_date, lifetime_value)
- products: Product catalog (id, name, category_id, price, stock_quantity, description)
- categories: Product categories (id, name, description)
- orders: Customer orders (id, customer_id, order_date, total_amount, status)
- order_items: Items in each order (id, order_id, product_id, quantity, unit_price)
- reviews: Product reviews (id, product_id, customer_id, rating, comment, review_date)
- inventory: Inventory tracking (id, product_id, warehouse_location, quantity, last_updated)

Your task:
1. Understand the user's question
2. Write appropriate SQL SELECT queries to answer it
3. Execute the queries and analyze the results
4. Provide clear, insightful answers with relevant statistics

Guidelines:
- Only use SELECT queries (no modifications)
- Use proper SQL syntax for SQLite
- Explain findings in a clear, business-friendly way
- Include relevant numbers and trends
- Suggest follow-up analyses when appropriate

Response format:
1. First, write the SQL query you'll use
2. Then provide your analysis of the results
3. Include key insights and recommendations"""
    
    async def query(self, question: str) -> Dict[str, Any]:
        """
        Query the agent and return complete response.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with response, SQL query, and results
        """
        self.last_sql_query = None
        self.last_results = None
        
        try:
            # Step 1: Get schema if needed
            schema_info = self.sql_tool.get_schema()
            
            # Step 2: Ask LLM to generate SQL query
            sql_prompt = f"""Given this question: "{question}"

Write a SQL SELECT query to answer it. Return ONLY the SQL query, nothing else.
Available tables: customers, products, categories, orders, order_items, reviews, inventory"""
            
            # Prepare callbacks
            config = {}
            if self.langfuse_handler:
                config["callbacks"] = [self.langfuse_handler]
            
            sql_response = await self.llm.ainvoke(
                [
                    SystemMessage(content=self.system_prompt),
                    HumanMessage(content=sql_prompt)
                ],
                config=config
            )
            
            # Extract SQL query
            sql_query = sql_response.content.strip()
            # Remove markdown code blocks if present
            if "```sql" in sql_query:
                sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
            elif "```" in sql_query:
                sql_query = sql_query.split("```")[1].split("```")[0].strip()
            
            self.last_sql_query = sql_query
            
            # Step 3: Execute query
            result = self.sql_tool.execute(sql_query)
            self.last_results = result
            
            if not result["success"]:
                return {
                    "response": f"Error executing query: {result['error']}",
                    "sql_query": sql_query,
                    "results": None
                }
            
            # Step 4: Ask LLM to analyze results
            analysis_prompt = f"""Question: {question}

SQL Query executed:
{sql_query}

Results ({result['row_count']} rows):
{json.dumps(result['data'][:10], indent=2)}  

Analyze these results and provide a clear, insightful answer to the user's question.
Include key statistics, trends, and actionable insights."""
            
            analysis_response = await self.llm.ainvoke(
                [
                    SystemMessage(content=self.system_prompt),
                    HumanMessage(content=analysis_prompt)
                ],
                config=config
            )
            
            return {
                "response": analysis_response.content,
                "sql_query": sql_query,
                "results": result
            }
            
        except Exception as e:
            logger.error(f"Error in MCP agent query: {e}", exc_info=True)
            return {
                "response": f"Error: {str(e)}",
                "sql_query": self.last_sql_query,
                "results": None
            }
    
    def get_last_query_info(self) -> Dict[str, Any]:
        """Get information about the last executed query."""
        return {
            "sql_query": self.last_sql_query,
            "results": self.last_results
        }
    
    def get_sample_queries(self) -> list[str]:
        """Get sample queries for users to try."""
        return [
            "How many customers do we have?",
            "What are the top 5 selling products?",
            "Show me total revenue by month",
            "Which countries have the most customers?",
            "What's the average order value?",
            "Show me products with low stock",
            "What are the highest rated products?",
            "Show me customer lifetime value distribution"
        ]

# Made with Bob

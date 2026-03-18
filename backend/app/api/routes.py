"""
API routes for the AI Analytics Demo.
Handles query processing, schema info, and sample queries.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..agents.sql_agent import get_agent
from ..agents.mcp_agent import MCPSQLAnalyticsAgent

router = APIRouter()

# Global MCP agent instance
_mcp_agent: Optional[MCPSQLAnalyticsAgent] = None


def get_mcp_agent() -> MCPSQLAnalyticsAgent:
    """Get or create MCP agent instance."""
    global _mcp_agent
    if _mcp_agent is None:
        _mcp_agent = MCPSQLAnalyticsAgent()
    return _mcp_agent


class QueryRequest(BaseModel):
    """Request model for natural language queries."""
    question: str
    session_id: Optional[str] = None
    use_mcp: bool = False  # Feature flag to use MCP agent


class QueryResponse(BaseModel):
    """Response model for query results."""
    success: bool
    question: str
    sql: Optional[str]
    results: List[Dict[str, Any]]
    analysis: str
    visualization: Dict[str, Any]
    row_count: int
    error: Optional[str] = None


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a natural language query and return results with analysis.
    
    Args:
        request: QueryRequest containing the user's question
        
    Returns:
        QueryResponse with SQL, results, analysis, and visualization config
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        if request.use_mcp:
            # Use MCP agent
            mcp_agent = get_mcp_agent()
            result = await mcp_agent.query(request.question)
            
            # Convert MCP result to QueryResponse format
            return QueryResponse(
                success=result.get("results", {}).get("success", False) if result.get("results") else True,
                question=request.question,
                sql=result.get("sql_query"),
                results=result.get("results", {}).get("data", []) if result.get("results") else [],
                analysis=result.get("response", ""),
                visualization={},  # MCP agent doesn't generate viz config yet
                row_count=result.get("results", {}).get("row_count", 0) if result.get("results") else 0,
                error=result.get("results", {}).get("error") if result.get("results") else None
            )
        else:
            # Use original agent
            agent = get_agent()
            result = await agent.process_query(request.question)
            return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/schema")
async def get_schema():
    """
    Get database schema information directly from the database.
    
    Returns:
        Dictionary containing schema details
    """
    try:
        # Get schema directly from database without using the agent
        import sqlite3
        from pathlib import Path
        from ..config import settings
        
        # Get the database path - use absolute path
        # Path: routes.py -> api -> app -> backend -> project_root
        project_root = Path(__file__).parent.parent.parent.parent
        db_path = project_root / "database" / "ecommerce.db"
        
        if not db_path.exists():
            raise HTTPException(status_code=500, detail=f"Database not found at: {db_path}")
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        schema_text = ""
        for (table_name,) in tables:
            # Get CREATE TABLE statement
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            create_stmt = cursor.fetchone()
            if create_stmt:
                schema_text += f"\n{create_stmt[0]};\n"
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "schema": schema_text,
            "table_count": len(tables),
            "db_path": str(db_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving schema: {str(e)}")


@router.get("/sample-queries")
async def get_sample_queries(use_mcp: bool = Query(False, description="Use MCP agent")):
    """
    Get sample queries that users can try.
    
    Args:
        use_mcp: Whether to get samples from MCP agent
    
    Returns:
        List of sample query strings
    """
    try:
        if use_mcp:
            mcp_agent = get_mcp_agent()
            samples = mcp_agent.get_sample_queries()
        else:
            agent = get_agent()
            samples = agent.get_sample_queries()
        
        return {
            "success": True,
            "queries": samples,
            "agent_type": "mcp" if use_mcp else "direct"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving samples: {str(e)}")


@router.post("/query/mcp")
async def process_mcp_query(request: QueryRequest):
    """
    Process a query using the MCP agent specifically.
    This is a dedicated endpoint for testing MCP integration.
    
    Args:
        request: QueryRequest containing the user's question
        
    Returns:
        Raw MCP agent response
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        mcp_agent = get_mcp_agent()
        result = await mcp_agent.query(request.question)
        
        return {
            "success": True,
            "question": request.question,
            "response": result.get("response"),
            "sql_query": result.get("sql_query"),
            "results": result.get("results"),
            "agent_type": "mcp"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing MCP query: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status information
    """
    return {
        "status": "healthy",
        "service": "AI Analytics API",
        "version": "1.0.0"
    }

# Made with Bob

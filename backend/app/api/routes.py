"""
API routes for the AI Analytics Demo.
Handles query processing, schema info, and sample queries.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..agents.sql_agent import get_agent

router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for natural language queries."""
    question: str
    session_id: Optional[str] = None


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
async def get_sample_queries():
    """
    Get sample queries that users can try.
    
    Returns:
        List of sample query strings
    """
    try:
        agent = get_agent()
        samples = agent.get_sample_queries()
        return {
            "success": True,
            "queries": samples
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving samples: {str(e)}")


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

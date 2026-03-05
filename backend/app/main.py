"""
Main FastAPI application for AI Analytics Demo.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import router

# Create FastAPI app
app = FastAPI(
    title="AI Analytics API",
    description="Natural language interface for e-commerce data analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["analytics"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Analytics API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("🚀 Starting AI Analytics API...")
    print(f"📊 Database: {settings.database_url}")
    print(f"🤖 AI Model: Claude 3.5 Sonnet")
    print(f"🌐 CORS Origins: {settings.cors_origins}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 Shutting down AI Analytics API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

# Made with Bob

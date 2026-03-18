"""
Configuration management for the AI Analytics Demo.
Loads environment variables and provides application settings.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # OpenAI API
    openai_api_key: str
    openai_model: str = "gpt-4"
    
    # Database
    database_url: str = "sqlite:///./database/ecommerce.db"
    
    # CORS
    cors_origins: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # LangChain
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    
    # Langfuse (LLM Observability)
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_enabled: bool = False
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Made with Bob

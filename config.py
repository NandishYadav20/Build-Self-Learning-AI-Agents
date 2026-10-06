"""Configuration management for AI Agents"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2048

    # Mem0 Configuration
    mem0_api_key: Optional[str] = None
    mem0_version: str = "prod"

    # Qdrant Configuration
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None

    # Application Configuration
    log_level: str = "INFO"
    debug: bool = False
    max_retries: int = 3
    request_timeout: int = 30

    # Database Configuration
    sqlite_db_path: str = "data/agents.db"
    memory_db_path: str = "data/memory.db"

    # Agent Configuration
    agent_name: str = "AIAgent"
    agent_description: str = "A self-learning AI agent"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

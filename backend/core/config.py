"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List, Literal


class Settings(BaseSettings):
    """Application settings"""

    # LLM Configuration
    LLM_PROVIDER: Literal["ollama", "anthropic"] = "ollama"  # Default to local Ollama

    # Ollama Settings (for local open source models)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"  # or "mistral", "qwen2.5:7b", etc.

    # Anthropic Settings (optional, for cloud API)
    ANTHROPIC_API_KEY: str = ""

    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ClinicalTrials.gov API
    CLINICALTRIALS_API_URL: str = "https://clinicaltrials.gov/api/v2"

    # Cache
    ENABLE_CACHE: bool = True
    CACHE_EXPIRY_HOURS: int = 24

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    # e.g: "http://localhost,http://localhost:8080,http://localhost:3000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost", 
        "http://localhost:8080",
        "http://localhost:3000"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Claude API Application"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Token settings
    TOKEN_ALGORITHM: str = os.getenv("TOKEN_ALGORITHM", "HS256")
    
    # Claude API settings
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_API_URL: str = os.getenv("CLAUDE_API_URL", "https://api.anthropic.com/v1")
    
    # Default limits (in euros)
    DEFAULT_DAILY_LIMIT: float = float(os.getenv("DEFAULT_DAILY_LIMIT", "5.0"))
    DEFAULT_MONTHLY_LIMIT: float = float(os.getenv("DEFAULT_MONTHLY_LIMIT", "50.0"))
    
    # Brave API key for MCP
    BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

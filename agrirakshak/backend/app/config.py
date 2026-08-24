import os
from pydantic_settings import BaseSettings
from typing import List, Union, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgriRakshak Backend API"
    VERSION: str = "1.0.0"
    
    PREDICTION_API_URL: str = "http://127.0.0.1:8000"
    PREDICTION_CONFIDENCE_THRESHOLD: float = 0.60
    
    DATABASE_URL: str = "sqlite:///./agrirakshak.db"
    
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    LLM_PROVIDER: str = "gemini"
    
    OPENWEATHER_API_KEY: str = ""
    
    JWT_SECRET: str = "agrirakshak_super_secret_jwt_key_sih_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()

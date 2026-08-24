import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgriRakshak MVP API"
    VERSION: str = "2.0.0"
    API_PORT: int = 8001
    
    # Existing prediction microservice URL
    PREDICTION_API_URL: str = os.getenv("PREDICTION_API_URL", "http://127.0.0.1:8000")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))
    
    # Database URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./agrirakshak.db")
    
    # OpenWeatherMap API Key
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    
    # LLM API Config
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai | anthropic
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    
    # Secret Key for JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "agrirakshak-secret-key-change-in-production")
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

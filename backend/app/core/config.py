"""
Core configuration module for the Dermatology AI Assistant.
Loads settings from environment variables with validation.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Dermatology AI Assistant"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Database
    DATABASE_URL: str
    DB_USER: str = "admin"
    DB_PASSWORD: str
    DB_NAME: str = "dermatology_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    HEATMAP_DIR: str = "./heatmaps"
    REPORT_DIR: str = "./reports"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # ML Models
    MODEL_PATH: str = "./models/skin_multiclass.pth"
    BIOBERT_MODEL_PATH: str = "./models/biobert"
    RISK_MODEL_PATH: str = "./models/risk_predictor.pkl"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 500
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@dermatology-ai.com"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 9090
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Medical Compliance
    REQUIRE_DOCTOR_REVIEW: bool = True
    HIGH_RISK_THRESHOLD: float = 0.7
    CONFIDENCE_THRESHOLD: float = 0.6
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Create necessary directories
def create_directories():
    """Create required directories if they don't exist."""
    directories = [
        settings.UPLOAD_DIR,
        settings.HEATMAP_DIR,
        settings.REPORT_DIR,
        os.path.dirname(settings.LOG_FILE),
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


create_directories()

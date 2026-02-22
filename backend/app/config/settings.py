"""
AIComplianceGuard - Configuration Module
Handles environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "AIComplianceGuard"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Backend API
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "development-secret-key-change-in-production"
    AES_ENCRYPTION_KEY: str = "dev-32-byte-key-change-prod!!"
    JWT_SECRET: str = "jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Firebase
    FIREBASE_API_KEY: str = ""
    FIREBASE_AUTH_DOMAIN: str = ""
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_PATH: str = "./firebase-credentials.json"
    
    # AI/ML Configuration
    MODEL_CACHE_DIR: str = "./data/models"
    USE_GPU: bool = False
    MAX_DOCUMENT_SIZE_MB: int = 10
    SUPPORTED_FORMATS: List[str] = ["pdf", "docx"]
    
    # Document Processing
    TEMP_UPLOAD_DIR: str = "./temp_uploads"
    AUTO_DELETE_AFTER_MINUTES: int = 5
    
    # Compliance Frameworks
    FRAMEWORKS_DATA_DIR: str = "./data/frameworks"
    
    # Audit Prediction Model
    AUDIT_MODEL_PATH: str = "./data/models/audit_predictor.pkl"
    AUDIT_SCALER_PATH: str = "./data/models/audit_scaler.pkl"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/aicomplianceguard.log"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Database
    DB_ENCRYPTION_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure directories exist
Path(settings.TEMP_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.FRAMEWORKS_DATA_DIR).mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(exist_ok=True)

"""
Configuration module for the Data Analyst Agent backend
"""
import os
import pathlib
from dotenv import load_dotenv
from typing import Optional

# Base directory is the backend folder itself
BACKEND_DIR = pathlib.Path(__file__).parent.absolute()
load_dotenv(BACKEND_DIR / ".env")

class Config:
    """Base configuration"""
    
    # API Settings
    API_TITLE = "Autonomous Data Analyst Agent API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Backend API for Natural Language to SQL Data Analysis"
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # Database - use absolute path so it works regardless of working directory
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(BACKEND_DIR / "analytics.db"))
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")
    
    # LLM Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.0))
    
    # LangChain Settings
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "data-analyst-agent")
    
    # Query Limits
    MAX_QUERY_LIMIT = int(os.getenv("MAX_QUERY_LIMIT", 1000))
    MAX_QUERY_TIMEOUT = int(os.getenv("MAX_QUERY_TIMEOUT", 30))  # seconds
    
    # Visualization
    PLOT_WIDTH = int(os.getenv("PLOT_WIDTH", 12))
    PLOT_HEIGHT = int(os.getenv("PLOT_HEIGHT", 6))
    DPI = int(os.getenv("DPI", 100))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    # Cache Settings
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get database URL based on type"""
        if "postgresql" in cls.DATABASE_URL or "postgres" in cls.DATABASE_URL:
            return cls.DATABASE_URL
        return f"sqlite:///{cls.SQLITE_DB_PATH}"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"

class TestingConfig(Config):
    """Testing configuration"""
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True

# Select config based on environment
ENV = os.getenv("ENVIRONMENT", "development")
if ENV == "production":
    config = ProductionConfig()
elif ENV == "testing":
    config = TestingConfig()
else:
    config = DevelopmentConfig()
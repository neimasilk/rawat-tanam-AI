import os
from typing import List, Optional

class Settings:
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Rawat Tanam AI API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Indonesian Flora Identification API Platform"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "rawat_tanam_ai"
    POSTGRES_PORT: int = 5432
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_FREE: str = "100/hour"
    RATE_LIMIT_PROFESSIONAL: str = "1000/hour"
    RATE_LIMIT_ENTERPRISE: str = "10000/hour"
    RATE_LIMIT_PARTNER: str = "unlimited"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/webp"]
    
    # ML Model Configuration
    MODEL_PATH: str = "models/"
    CONFIDENCE_THRESHOLD: float = 0.7
    
    # External APIs
    TANAM_RAWAT_API_URL: str = "http://localhost:3000/api"
    TANAM_RAWAT_API_KEY: Optional[str] = None
    
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    def __init__(self):
        # Load from environment variables with defaults
        self.API_V1_STR = os.getenv("API_V1_STR", self.API_V1_STR)
        self.PROJECT_NAME = os.getenv("PROJECT_NAME", self.PROJECT_NAME)
        self.VERSION = os.getenv("VERSION", self.VERSION)
        self.DESCRIPTION = os.getenv("DESCRIPTION", self.DESCRIPTION)
        self.HOST = os.getenv("HOST", self.HOST)
        self.PORT = int(os.getenv("PORT", str(self.PORT)))
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        self.POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", self.POSTGRES_SERVER)
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", self.POSTGRES_USER)
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", self.POSTGRES_DB)
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", str(self.POSTGRES_PORT)))
        self.SECRET_KEY = os.getenv("SECRET_KEY", self.SECRET_KEY)
        self.ALGORITHM = os.getenv("ALGORITHM", self.ALGORITHM)
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(self.ACCESS_TOKEN_EXPIRE_MINUTES)))
        self.RATE_LIMIT_FREE = os.getenv("RATE_LIMIT_FREE", self.RATE_LIMIT_FREE)
        self.RATE_LIMIT_PROFESSIONAL = os.getenv("RATE_LIMIT_PROFESSIONAL", self.RATE_LIMIT_PROFESSIONAL)
        self.RATE_LIMIT_ENTERPRISE = os.getenv("RATE_LIMIT_ENTERPRISE", self.RATE_LIMIT_ENTERPRISE)
        self.RATE_LIMIT_PARTNER = os.getenv("RATE_LIMIT_PARTNER", self.RATE_LIMIT_PARTNER)
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(self.MAX_FILE_SIZE)))
        self.MODEL_PATH = os.getenv("MODEL_PATH", self.MODEL_PATH)
        self.CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", str(self.CONFIDENCE_THRESHOLD)))
        self.TANAM_RAWAT_API_URL = os.getenv("TANAM_RAWAT_API_URL", self.TANAM_RAWAT_API_URL)
        self.TANAM_RAWAT_API_KEY = os.getenv("TANAM_RAWAT_API_KEY", self.TANAM_RAWAT_API_KEY)

settings = Settings()
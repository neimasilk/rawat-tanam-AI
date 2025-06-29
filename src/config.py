import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = Field(default="/api/v1")
    PROJECT_NAME: str = Field(default="Rawat Tanam AI API")
    VERSION: str = Field(default="1.0.0")
    DESCRIPTION: str = Field(default="Indonesian Flora Identification API Platform")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)
    
    # Database Configuration
    DATABASE_URL: str = Field(default="sqlite:///./rawat_tanam_ai.db")
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="password")
    POSTGRES_DB: str = Field(default="rawat_tanam_ai")
    POSTGRES_PORT: int = Field(default=5432)
    
    # Authentication
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Rate Limiting
    RATE_LIMIT_FREE: str = Field(default="100/hour")
    RATE_LIMIT_PROFESSIONAL: str = Field(default="1000/hour")
    RATE_LIMIT_ENTERPRISE: str = Field(default="10000/hour")
    RATE_LIMIT_PARTNER: str = Field(default="unlimited")
    
    # File Upload
    MAX_FILE_SIZE: int = Field(default=10485760)  # 10MB
    ALLOWED_IMAGE_TYPES: str = Field(default="image/jpeg,image/png,image/webp")
    
    # ML Model Configuration
    MODEL_PATH: str = Field(default="models/")
    CONFIDENCE_THRESHOLD: float = Field(default=0.7)
    
    # External APIs
    TANAM_RAWAT_API_URL: str = Field(default="http://localhost:3000/api")
    TANAM_RAWAT_API_KEY: Optional[str] = Field(default=None)
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        """Convert comma-separated string to list"""
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",")]
    
    @property
    def postgres_database_url(self) -> str:
        """Generate PostgreSQL database URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
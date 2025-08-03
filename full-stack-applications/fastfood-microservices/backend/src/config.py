import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carrega .env apenas se existir (para ambiente local)
if os.path.exists('.env'):
    load_dotenv('.env')

class Settings(BaseSettings):
    # Database - Get from Render environment
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/fastfood")
    
    # Security - Get from Render environment
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fastfood-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Admin Authentication - Get from Render environment
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Environment - Get from Render environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # CORS - Get from Render environment
    CORS_ALLOW_ORIGINS_STR: str = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://localhost:8000,https://fastfood-frontend.vercel.app,https://fastfood-murex.vercel.app")
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: List[str] = ["*", "Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"]
    
    # API - Get from Render environment
    API_TITLE: str = os.getenv("PROJECT_NAME", "FastFood API")
    API_DESCRIPTION: str = "API para sistema de autoatendimento de fast food"
    API_VERSION: str = os.getenv("VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/v1")
    
    # Logging - Get from Render environment
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate DATABASE_URL
        self._validate_database_url()
    
    def _validate_database_url(self):
        """Validate DATABASE_URL format"""
        if self.DATABASE_URL.startswith("DATABASE_URL="):
            raise ValueError(
                f"Invalid DATABASE_URL format. Got: {self.DATABASE_URL}\n"
                "Expected: postgresql://user:pass@host:port/db\n"
                "Make sure the environment variable is set correctly in Render."
            )
        
        if not self.DATABASE_URL.startswith("postgresql://"):
            raise ValueError(
                f"Invalid DATABASE_URL. Must start with 'postgresql://'. Got: {self.DATABASE_URL}"
            )
    
    @property
    def CORS_ALLOW_ORIGINS(self) -> List[str]:
        """Convert CORS_ALLOW_ORIGINS_STR to list"""
        if not self.CORS_ALLOW_ORIGINS_STR:
            return ["http://localhost:3000", "http://localhost:8000", "https://fastfood-frontend.vercel.app", "https://fastfood-murex.vercel.app"]
        
        origins = []
        for origin in self.CORS_ALLOW_ORIGINS_STR.split(","):
            origin = origin.strip()
            if origin:
                origins.append(origin)
        
        return origins if origins else ["http://localhost:3000", "http://localhost:8000", "https://fastfood-frontend.vercel.app", "https://fastfood-murex.vercel.app"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings() 
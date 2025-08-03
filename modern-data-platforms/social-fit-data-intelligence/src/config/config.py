import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Optional
import base64
import json

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration with enhanced security."""
    
    # Supabase Configuration
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    DATABASE_SCHEMA: str = "social_fit"  # Schema for all tables
    
    # Data Paths
    DATA_DIR: str = "data"
    STUDENTS_FILE: str = "social_fit_alunos.csv"
    INSTAGRAM_FILE: str = "social_fit_instagram.csv"
    
    # Application Configuration
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    BATCH_SIZE: int = 100
    
    # Analytics Configuration
    ANALYTICS_CACHE_TTL: int = 3600
    ANALYTICS_UPDATE_INTERVAL: int = 300
    
    # Dashboard Configuration
    DASHBOARD_HOST: str = "localhost"
    DASHBOARD_PORT: int = 8050
    DASHBOARD_DEBUG: bool = True
    
    # Security Configuration
    SECRET_KEY: Optional[str] = None
    ENCRYPTION_KEY: Optional[str] = None
    
    # Social FIT Business Configuration
    GYM_NAME: str = "Social FIT"
    GYM_CNPJ: str = "50.056.362/0001-72"
    GYM_ADDRESS: str = "Avenida Nossa Senhora da Luz 850 - Cabral, Curitiba/PR - CEP: 82510-020"
    
    @validator('SUPABASE_URL')
    def validate_supabase_url(cls, v):
        if not v:
            raise ValueError('SUPABASE_URL is required in .env file')
        if not v.startswith('https://'):
            raise ValueError('SUPABASE_URL must be a valid HTTPS URL')
        return v
    
    @validator('SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY')
    def validate_supabase_keys(cls, v):
        if not v:
            raise ValueError('Supabase keys are required in .env file')
        if not v.startswith('eyJ'):
            raise ValueError('Invalid Supabase JWT token format')
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

class CredentialManager:
    """Professional credential management for Supabase integration."""
    
    def __init__(self):
        self.settings = settings
    
    def get_supabase_config(self) -> dict:
        """Get Supabase configuration for client initialization."""
        return {
            'url': self.settings.SUPABASE_URL,
            'key': self.settings.SUPABASE_ANON_KEY,
            'service_key': self.settings.SUPABASE_SERVICE_ROLE_KEY
        }
    
    def validate_credentials(self) -> bool:
        """Validate that all required credentials are present and valid."""
        try:
            # Check if URL is valid
            if not self.settings.SUPABASE_URL:
                print("❌ SUPABASE_URL not found in .env file")
                return False
            
            # Check if keys are present and valid format
            if not self.settings.SUPABASE_ANON_KEY:
                print("❌ SUPABASE_ANON_KEY not found in .env file")
                return False
            if not self.settings.SUPABASE_SERVICE_ROLE_KEY:
                print("❌ SUPABASE_SERVICE_ROLE_KEY not found in .env file")
                return False
            
            # Validate JWT token format
            if not self.settings.SUPABASE_ANON_KEY.startswith('eyJ'):
                print("❌ Invalid SUPABASE_ANON_KEY format")
                return False
            if not self.settings.SUPABASE_SERVICE_ROLE_KEY.startswith('eyJ'):
                print("❌ Invalid SUPABASE_SERVICE_ROLE_KEY format")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error validating credentials: {e}")
            return False
    
    def get_connection_string(self) -> str:
        """Get database connection string for direct database access."""
        if self.settings.DATABASE_URL:
            return self.settings.DATABASE_URL
        
        # Construct connection string from Supabase credentials
        # Extract database info from service key (simplified approach)
        return f"postgresql://postgres:[password]@db.{self.settings.SUPABASE_URL.replace('https://', '').replace('.supabase.co', '')}.supabase.co:5432/postgres"

# Global credential manager instance
credential_manager = CredentialManager() 
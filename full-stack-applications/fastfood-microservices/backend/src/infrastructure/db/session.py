from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import settings
import os

# Use the centralized settings
DATABASE_URL = settings.DATABASE_URL

# Configure engine with better error handling and SSL
def create_database_engine():
    """Create database engine with proper configuration"""
    try:
        # Check if we're on Render
        is_render = "render.com" in DATABASE_URL
        
        if is_render:
            # Render-specific configuration
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=10,
                max_overflow=20,
                connect_args={
                    "sslmode": "require",
                    "connect_timeout": 10
                }
            )
        else:
            # Local development configuration
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300
            )
        
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise

engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

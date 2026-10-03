import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "WOODPLAN AI"
    API_V1_STR: str = "/api"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Check serverless environment (Vercel)
    is_serverless: bool = bool(os.getenv("VERCEL"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:////tmp/woodplan.db" if os.getenv("VERCEL") else "sqlite:///./woodplan.db"
    )
    
    # AI Keys & Models
    AI_API_KEY: Optional[str] = os.getenv("AI_API_KEY", os.getenv("GEMINI_API_KEY", None))
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini") # "gemini", "openai", "fallback"
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")
    VISION_MODEL: str = os.getenv("VISION_MODEL", "gemini-1.5-flash")
    
    # Storage
    STORAGE_DIR: str = os.getenv(
        "STORAGE_DIR", 
        "/tmp/storage" if os.getenv("VERCEL") else "./storage"
    )
    STORAGE_URL: Optional[str] = os.getenv("STORAGE_URL", None)
    
    # Upload limits (50MB)
    MAX_UPLOAD_SIZE_MB: int = 50

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure storage directories exist safely
try:
    os.makedirs(os.path.join(settings.STORAGE_DIR, "uploads"), exist_ok=True)
    os.makedirs(os.path.join(settings.STORAGE_DIR, "diagrams"), exist_ok=True)
    os.makedirs(os.path.join(settings.STORAGE_DIR, "pdfs"), exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create storage directory: {e}")

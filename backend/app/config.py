"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/review_analyzer"
    )
    
    # Hugging Face
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # Google Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

settings = Settings()

"""Configuration de l'application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application avec validation Pydantic."""
    
    # Base de données
    DATABASE_URL: str
    
    # API
    API_TITLE: str = "Concert Viewer API"
    API_VERSION: str = "1.0.0"
    
    # CORS (à ajuster selon ton frontend)
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js dev
        "http://localhost:5173",  # Vite alternative
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instance globale
settings = Settings()
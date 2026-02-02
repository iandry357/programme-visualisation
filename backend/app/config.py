"""Configuration de l'application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application avec validation Pydantic."""
    
    # Base de données
    DATABASE_URL: str
    
    # API
    API_TITLE: str = "Concert Viewer API"
    API_VERSION: str = "1.0.0"
    
    # Frontend URL pour Railway (optionnel)
    FRONTEND_URL: str | None = None
    
    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Retourne les origines CORS incluant FRONTEND_URL si défini."""
        origins = [
            "http://localhost:3000",  # Next.js dev local
            "http://localhost:5173",  # Vite alternative
        ]
        if self.FRONTEND_URL:
            origins.append(self.FRONTEND_URL)
        return origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instance globale
settings = Settings()
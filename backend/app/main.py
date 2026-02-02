"""Point d'entrée FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import concerts

from app.database import engine, Base
from app import models

# Création de l'app FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(concerts.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }


@app.get("/health")
def health():
    """Health check détaillé."""
    return {
        "status": "healthy",
        "database": "connected"  # Phase 3: vérifier vraiment la connexion
    }


@app.on_event("startup")
def startup():
    """Crée toutes les tables au démarrage."""
    Base.metadata.create_all(bind=engine)
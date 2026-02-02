"""Dependencies pour les endpoints API."""
from typing import Generator
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency pour obtenir une session DB.
    
    Yields:
        Session: Session SQLAlchemy pour les opérations DB
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
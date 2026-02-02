"""Endpoints API pour les concerts."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO

from app.api.deps import get_db
from app import models, schemas

router = APIRouter(prefix="/api/concerts", tags=["concerts"])


@router.get("/", response_model=list[schemas.ConcertList])
def list_concerts(db: Session = Depends(get_db)):
    """Liste tous les concerts publiés."""
    # Phase 3: Implémenter la logique
    return []


@router.get("/{concert_id}", response_model=schemas.ConcertWithPages)
def get_concert(concert_id: int, db: Session = Depends(get_db)):
    """Récupère les détails d'un concert avec la liste des pages."""
    # Phase 3: Implémenter la logique
    raise HTTPException(status_code=404, detail="Concert not found")


@router.get("/{concert_id}/pages", response_model=list[schemas.ProgramPageMetadata])
def list_pages(concert_id: int, db: Session = Depends(get_db)):
    """Liste les pages d'un concert."""
    # Phase 3: Implémenter la logique
    return []


@router.get("/{concert_id}/pages/{page_number}/png")
def get_page_png(
    concert_id: int, 
    page_number: int, 
    db: Session = Depends(get_db)
):
    """Stream le PNG d'une page spécifique."""
    # Phase 3: Implémenter la logique
    raise HTTPException(status_code=404, detail="Page not found")


@router.get("/{concert_id}/pdf")
def get_concert_pdf(concert_id: int, db: Session = Depends(get_db)):
    """Télécharge le PDF complet du concert."""
    # Phase 3: Implémenter la logique
    raise HTTPException(status_code=404, detail="Concert not found")
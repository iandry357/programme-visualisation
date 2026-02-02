"""Endpoints API pour les concerts."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from io import BytesIO

from app.api.deps import get_db
from app import models, schemas

router = APIRouter(prefix="/api/concerts", tags=["concerts"])


@router.get("/", response_model=list[schemas.ConcertList])
def list_concerts(db: Session = Depends(get_db)):
    """Liste tous les concerts publiés."""
    try:
        concerts = (
            db.query(
                models.Concert,
                func.count(models.ProgramPage.id).label("page_count")
            )
            .outerjoin(models.ProgramPage)
            .filter(models.Concert.is_published == True)
            .group_by(models.Concert.id)
            .all()
        )
        
        return [
            schemas.ConcertList(
                id=concert.id,
                title=concert.title,
                concert_date=concert.concert_date,
                location=concert.location,
                is_published=concert.is_published,
                page_count=page_count
            )
            for concert, page_count in concerts
        ]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{concert_id}", response_model=schemas.ConcertWithPages)
def get_concert(concert_id: int, db: Session = Depends(get_db)):
    """Récupère les détails d'un concert avec la liste des pages."""
    try:
        concert = (
            db.query(models.Concert)
            .options(joinedload(models.Concert.pages))
            .filter(models.Concert.id == concert_id)
            .first()
        )
        
        if not concert:
            raise HTTPException(status_code=404, detail="Concert not found")
        
        return concert
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{concert_id}/pages", response_model=list[schemas.ProgramPageMetadata])
def list_pages(concert_id: int, db: Session = Depends(get_db)):
    """Liste les pages d'un concert."""
    try:
        concert = db.query(models.Concert).filter(models.Concert.id == concert_id).first()
        if not concert:
            raise HTTPException(status_code=404, detail="Concert not found")
        
        pages = (
            db.query(models.ProgramPage)
            .filter(models.ProgramPage.concert_id == concert_id)
            .order_by(models.ProgramPage.page_number)
            .all()
        )
        
        return pages
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{concert_id}/pages/{page_number}/png")
def get_page_png(
    concert_id: int, 
    page_number: int, 
    db: Session = Depends(get_db)
):
    """Stream le PNG d'une page spécifique."""
    try:
        page = (
            db.query(models.ProgramPage)
            .filter(
                models.ProgramPage.concert_id == concert_id,
                models.ProgramPage.page_number == page_number
            )
            .first()
        )
        
        if not page or not page.png_data:
            raise HTTPException(status_code=404, detail="Page not found")
        
        return StreamingResponse(
            BytesIO(page.png_data),
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=page_{page_number}.png"
            }
        )
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{concert_id}/pdf")
def get_concert_pdf(concert_id: int, db: Session = Depends(get_db)):
    """Télécharge le PDF complet du concert."""
    try:
        concert = (
            db.query(models.Concert)
            .filter(models.Concert.id == concert_id)
            .first()
        )
        
        if not concert:
            raise HTTPException(status_code=404, detail="Concert not found")
        
        if not concert.pdf_full:
            raise HTTPException(status_code=404, detail="PDF not available")
        
        return StreamingResponse(
            BytesIO(concert.pdf_full),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={concert.pdf_filename}"
            }
        )
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
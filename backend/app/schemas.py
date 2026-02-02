"""Schémas Pydantic pour validation et sérialisation."""
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class ProgramPageBase(BaseModel):
    """Schema de base pour une page."""
    page_number: int
    width: int | None = None
    height: int | None = None


class ProgramPageMetadata(ProgramPageBase):
    """Metadata d'une page (sans le binaire)."""
    id: int
    png_size: int
    
    model_config = ConfigDict(from_attributes=True)


class ConcertBase(BaseModel):
    """Schema de base pour un concert."""
    title: str
    concert_date: date | None = None
    location: str | None = None
    is_published: bool = True


class ConcertDetail(ConcertBase):
    """Détails complets d'un concert (sans binaires)."""
    id: int
    pdf_filename: str
    pdf_size: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ConcertWithPages(ConcertDetail):
    """Concert avec la liste de ses pages."""
    pages: list[ProgramPageMetadata] = []
    
    model_config = ConfigDict(from_attributes=True)


class ConcertList(ConcertBase):
    """Résumé concert pour liste."""
    id: int
    page_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)
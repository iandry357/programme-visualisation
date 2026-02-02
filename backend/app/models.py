"""Models SQLAlchemy pour MariaDB."""
from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Date, Boolean, 
    LargeBinary, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGBLOB

from app.database import Base


class Concert(Base):
    """Table des concerts."""
    __tablename__ = "concerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    concert_date = Column(Date, nullable=True)
    location = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=True)
    
    # PDF complet
    pdf_full = Column(LONGBLOB, nullable=False)
    pdf_filename = Column(String(255), nullable=False)
    pdf_size = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    pages = relationship("ProgramPage", back_populates="concert", cascade="all, delete-orphan")


class ProgramPage(Base):
    """Table des pages du programme (PNG)."""
    __tablename__ = "program_pages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    concert_id = Column(Integer, ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer, nullable=False)
    
    # PNG data
    png_data = Column(LONGBLOB, nullable=False)
    png_size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relation
    concert = relationship("Concert", back_populates="pages")
    
    # Index
    __table_args__ = (
        Index('idx_concert_pages', 'concert_id', 'page_number'),
    )
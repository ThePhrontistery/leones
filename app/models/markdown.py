"""
Pydantic and SQLAlchemy models for MarkdownDocument.
"""
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MarkdownDocumentORM(Base):
    __tablename__ = "markdown_documents"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

class MarkdownDocument(BaseModel):
    """Pydantic model for Markdown document."""
    id: Optional[int] = None
    content: str

    class Config:
        orm_mode = True

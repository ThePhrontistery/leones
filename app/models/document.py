"""
Pydantic model for uploaded documents.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UploadedDocument(BaseModel):
    """Schema for an uploaded document."""
    fecha_carga: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de carga del documento.")
    file_name: str
    file_path: str
    proyecto: str = "demo_metasketch"
    categoria: str
    descripcion: Optional[str] = None

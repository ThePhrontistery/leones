"""
Service for handling document uploads and metadata persistence.
"""
import os
from datetime import datetime
from typing import Optional
from app.models.document import UploadedDocument

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")

async def save_uploaded_document(
    file_bytes: bytes,
    file_name: str,
    categoria: str,
    descripcion: Optional[str] = None,
    proyecto: str = "demo_metasketch",
) -> UploadedDocument:
    """
    Save uploaded file to disk and return metadata as UploadedDocument.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    doc = UploadedDocument(
        fecha_carga=datetime.utcnow(),
        file_name=file_name,
        file_path=file_path,
        proyecto=proyecto,
        categoria=categoria,
        descripcion=descripcion,
    )
    return doc

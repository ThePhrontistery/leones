"""
Service for handling document uploads and metadata persistence.
"""
import os
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import UploadedDocument
from app.db.models import UploadedFile
from app.db.session import AsyncSessionLocal

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")

async def save_uploaded_document(
    file_bytes: bytes,
    file_name: str,
    categoria: str,
    descripcion: Optional[str] = None,
    proyecto: str = "demo_metasketch",
) -> UploadedDocument:
    """
    Save uploaded file to disk and persist metadata in DB.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    fecha_carga = datetime.utcnow()
    async with AsyncSessionLocal() as session:
        db_file = UploadedFile(
            filename=file_name,
            file_path=file_path,
            categoria=categoria,
            descripcion=descripcion,
            proyecto=proyecto,
            upload_time=fecha_carga,
        )
        session.add(db_file)
        await session.commit()
    doc = UploadedDocument(
        fecha_carga=fecha_carga,
        file_name=file_name,
        file_path=file_path,
        proyecto=proyecto,
        categoria=categoria,
        descripcion=descripcion,
    )
    return doc

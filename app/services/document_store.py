"""
In-memory store for uploaded documents (demo only).
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import AsyncSessionLocal
from app.db.models import UploadedFile
from app.models.document import UploadedDocument
from typing import List
import asyncio

def add_document(doc: UploadedDocument) -> None:
    # Deprecated: now handled by DB
    pass

async def get_documents() -> List[UploadedDocument]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UploadedFile))
        files = result.scalars().all()
        return [
            UploadedDocument(
                fecha_carga=f.upload_time,
                file_name=f.filename,
                file_path=f.file_path,
                proyecto=f.proyecto,
                categoria=f.categoria,
                descripcion=f.descripcion,
            ) for f in files
        ]

def clear_documents() -> None:
    # Deprecated: use DB for clearing
    pass

async def clear_documents_async() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute("DELETE FROM uploaded_files")
        await session.commit()

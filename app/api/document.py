"""
API routes for document upload and management.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.document_service import save_uploaded_document, generate_functional_document
from app.services.document_store import get_documents, clear_documents_async
from app.models.document import UploadedDocument
from typing import Optional
import asyncio
from app.db.session import AsyncSessionLocal
from app.db.models import UploadedFile
from sqlalchemy.future import select
from sqlalchemy import text
import os
import logging

router = APIRouter(prefix="/api/document", tags=["document"])
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

@router.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    """
    Render the upload form in a new window.
    """
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/upload", response_class=HTMLResponse)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    categoria: str = Form(...),
    descripcion: Optional[str] = Form(None),
    proyecto: str = Form("demo_metasketch"),
):
    """
    Upload a document and return its metadata as HTML (for HTMX swap).
    """
    try:
        file_bytes = await file.read()
        doc = await save_uploaded_document(
            file_bytes=file_bytes,
            file_name=file.filename,
            categoria=categoria,
            descripcion=descripcion,
            proyecto=proyecto,
        )
        return templates.TemplateResponse(
            "upload_result.html",
            {"request": request, "doc": doc}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_class=HTMLResponse)
async def list_documents(request: Request):
    """
    Render the list of uploaded documents for the main panel.
    """
    docs = await get_documents()
    return templates.TemplateResponse("document_list.html", {"request": request, "documents": docs})

@router.post("/clear", response_class=HTMLResponse)
async def clear_documents(request: Request):
    """
    Borra todos los documentos subidos (en base de datos y en disco).
    """
    # Borrar archivos en disco
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UploadedFile))
        files = result.scalars().all()
        for f in files:
            try:
                if os.path.exists(f.file_path):
                    os.remove(f.file_path)
            except Exception:
                pass
        await session.execute(text("DELETE FROM uploaded_files"))
        await session.commit()
    docs = await get_documents()
    return templates.TemplateResponse("document_list.html", {"request": request, "documents": docs})

@router.post("/generar-funcional", response_class=HTMLResponse)
async def generar_funcional(request: Request):
    """
    Genera el documento funcional usando la plantilla y los documentos cargados, llamando a la IA.
    Devuelve el documento generado, el índice de secciones y el prompt usado.
    Si la petición es HTMX, devuelve un fragmento HTML para actualizar el frontend.
    """
    try:
        doc_funcional, indice, prompt = await generate_functional_document()
        if request.headers.get("hx-request") == "true":
            return templates.TemplateResponse(
                "funcional_result.html",
                {
                    "request": request,
                    "documento": doc_funcional,
                    "indice": indice,
                    "prompt": prompt,
                }
            )
        return {"documento": doc_funcional, "indice": indice, "prompt": prompt}
    except Exception as e:
        logger.exception("Error en /api/document/generar-funcional")
        return HTMLResponse(f"<div class='text-red-600'>Error: {str(e)}</div>", status_code=500)

@router.post("/generar-indice", response_class=HTMLResponse)
async def generar_indice(request: Request):
    """
    Genera el índice del documento funcional generado (no solo la plantilla) y lo devuelve como fragmento HTML para el árbol de contenidos.
    """
    try:
        _, indice, _ = await generate_functional_document()
        return templates.TemplateResponse(
            "arbol_contenidos.html",
            {"request": request, "indice": indice}
        )
    except Exception as e:
        return HTMLResponse(f"<div class='text-red-600'>Error: {str(e)}</div>", status_code=500)

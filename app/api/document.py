"""
API routes for document upload and management.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request, Query
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
from app.utils.parse_template import parse_template_tree
from app.utils.file_text import markdown_to_html
import re
from PIL import Image
import io

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
    Upload a document or image and return its metadata as HTML (for HTMX swap).
    """
    allowed_exts = {".pdf", ".docx", ".md", ".txt", ".jpg", ".jpeg", ".png"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no soportado: {ext}")
    try:
        file_bytes = await file.read()
        # Si es imagen, validarla con Pillow
        if ext in {".jpg", ".jpeg", ".png"}:
            try:
                img = Image.open(io.BytesIO(file_bytes))
                img.verify()  # Verifica que sea una imagen válida
            except Exception:
                raise HTTPException(status_code=400, detail="La imagen está corrupta o no es válida.")
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
    except HTTPException:
        raise
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

@router.get("/arbol-contenidos", response_class=HTMLResponse)
async def arbol_contenidos(request: Request):
    """
    Muestra el árbol de contenidos de la plantilla funcional en formato HTML (panel lateral).
    """
    plantilla_path = os.path.join(os.path.dirname(__file__), "..", "Documents", "Plantilla_Funcional.md")
    plantilla_path = os.path.abspath(plantilla_path)
    indice = parse_template_tree(plantilla_path)
    return templates.TemplateResponse(
        "arbol_contenidos.html",
        {"request": request, "indice": indice}
    )

@router.get("/funcional", response_class=HTMLResponse)
async def mostrar_funcional(request: Request, section: str = Query(None)):
    """
    Devuelve el documento funcional completo en HTML, resaltando la sección indicada (anchor) si se proporciona.
    """
    try:
        doc_funcional, _, _ = await generate_functional_document()
        # Convertir markdown a HTML y resaltar la sección
        html = markdown_to_html(doc_funcional)
        if section:
            # Añadir clase Tailwind al heading correspondiente (h1 o h2 con id=section)
            def resaltar_heading(match):
                tag, id_, contenido = match.group(1), match.group(2), match.group(3)
                if id_ == section:
                    return f'<{tag} id="{id_}" class="bg-yellow-100 border-l-4 border-yellow-400 pl-2">{contenido}</{tag}>'
                return match.group(0)
            html = re.sub(r'<(h[12]) id="([a-z0-9_\-]+)">(.*?)</h[12]>', resaltar_heading, html, flags=re.DOTALL)
        return templates.TemplateResponse(
            "funcional_result.html",
            {"request": request, "resultado": doc_funcional, "html": html, "section": section}
        )
    except Exception as e:
        logger.exception("Error en /api/document/funcional")
        return HTMLResponse(f"<div class='text-red-600'>Error: {str(e)}</div>", status_code=500)

@router.post("/delete/{file_name}", response_class=HTMLResponse)
async def delete_document(request: Request, file_name: str):
    """
    Borra un documento individual por nombre de archivo.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UploadedFile).where(UploadedFile.filename == file_name))
        file = result.scalar_one_or_none()
        if file:
            try:
                # Elimina el archivo físico si existe
                if file.file_path and os.path.exists(file.file_path):
                    os.remove(file.file_path)
            except Exception as e:
                logger.warning(f"No se pudo eliminar el archivo físico: {file.file_path}. Error: {e}")
            await session.delete(file)
            await session.commit()
    docs = await get_documents()
    return templates.TemplateResponse("document_list.html", {"request": request, "documents": docs})

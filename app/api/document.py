"""
API routes for document upload and management.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.document_service import save_uploaded_document
from app.services.document_store import add_document, get_documents
from app.models.document import UploadedDocument
from typing import Optional

router = APIRouter(prefix="/api/document", tags=["document"])
templates = Jinja2Templates(directory="templates")

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
        add_document(doc)
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
    docs = get_documents()
    return templates.TemplateResponse("document_list.html", {"request": request, "documents": docs})

@router.post("/clear", response_class=HTMLResponse)
async def clear_documents(request: Request):
    """
    Borra todos los documentos subidos (solo memoria, demo).
    """
    from app.services.document_store import clear_documents
    clear_documents()
    docs = get_documents()
    return templates.TemplateResponse("document_list.html", {"request": request, "documents": docs})

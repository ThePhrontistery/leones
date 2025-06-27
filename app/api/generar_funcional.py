"""
API route for generating functional summary using Azure OpenAI.
"""
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from app.services.generar_funcional_service import generar_funcional_ia
from fastapi.templating import Jinja2Templates
from app.utils.parse_template import parse_template_tree
from app.db.session import get_async_session
from app.db.markdown import save_markdown_document
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import os
import logging
import markdown
import tempfile
import io

router = APIRouter(prefix="/api/generar-funcional", tags=["generar-funcional"])
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

async def _render_panel_funcional_fragment(request: Request, resultado_md: str, resultado_html: str):
    """
    Devuelve solo el fragmento del panel funcional (editor, preview, árbol) para insertar en #panel-markdown.
    """
    return templates.TemplateResponse(
        "panel_funcional.html",
        {
            "request": request,
            "resultado_md": resultado_md,
            "resultado_html": resultado_html,
        }
    )

@router.post("/", response_class=HTMLResponse)
async def generar_funcional(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Llama a la IA para generar el resumen funcional y retorna SOLO el fragmento del panel funcional para la home.
    """
    try:
        resultado_md = await generar_funcional_ia()
        # Guardar en BBDD
        doc = await save_markdown_document(session, content=resultado_md)
        resultado_md_db = doc.content if doc else resultado_md
        import markdown as md
        resultado_html = md.markdown(resultado_md_db or "", extensions=["extra", "tables", "fenced_code"])
        return await _render_panel_funcional_fragment(request, resultado_md_db, resultado_html)
    except Exception as e:
        logger.exception("Error en /api/generar-funcional/")
        import traceback
        tb = traceback.format_exc()
        error_html = f'<span class="ml-2 text-red-600" hx-swap-oob="true" id="generar-funcional-indicador">Error: {str(e)}</span>'
        debug_html = f'<pre class="text-xs text-red-500 bg-red-50 p-2 rounded mt-2">{tb}</pre>'
        return HTMLResponse(error_html + debug_html, status_code=500)

@router.post("/guardar", response_class=HTMLResponse)
async def guardar_funcional(request: Request, markdown_content: str = Form(...), session: AsyncSession = Depends(get_async_session)):
    """
    Guarda el contenido markdown editado por el usuario y retorna SOLO el fragmento del panel funcional para la home.
    """
    try:
        doc = await save_markdown_document(session, content=markdown_content)
        resultado_md_db = doc.content if doc else markdown_content
        import markdown as md
        resultado_html = md.markdown(resultado_md_db or "", extensions=["extra", "tables", "fenced_code"])
        return await _render_panel_funcional_fragment(request, resultado_md_db, resultado_html)
    except Exception as e:
        logger.exception("Error al guardar el funcional editado")
        return HTMLResponse(f'<div class="text-red-600">Error: {str(e)}</div>', status_code=500)

@router.post("/exportar")
async def exportar_funcional(
    markdown_content: str = Form(...),
    formato: str = Form(...)
):
    """
    Exporta el markdown guardado (si existe) o el contenido recibido como Word o PDF.
    """
    try:
        temp_path = "/tmp/funcional_guardado.md"
        use_temp = False
        if os.path.exists(temp_path):
            with open(temp_path, encoding="utf-8") as f:
                contenido = f.read()
            # Si el archivo temporal está vacío, usar el contenido recibido
            if contenido.strip():
                use_temp = True
            else:
                contenido = markdown_content
        else:
            contenido = markdown_content
        # Exportar a Word
        if formato == "word":
            from docx import Document
            doc = Document()
            for line in contenido.splitlines():
                doc.add_paragraph(line)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                doc.save(tmp.name)
                tmp.seek(0)
                return FileResponse(tmp.name, filename="funcional.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        # Exportar a PDF
        elif formato == "pdf":
            import markdown as md
            html = md.markdown(contenido)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                # pdfkit.from_string(html, tmp.name)  # Comentado para evitar error de importación
                tmp.seek(0)
                return FileResponse(tmp.name, filename="funcional.pdf", media_type="application/pdf")
        else:
            return JSONResponse({"success": False, "message": "Formato no soportado"}, status_code=400)
    except Exception as e:
        logger.exception("Error al exportar el funcional")
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

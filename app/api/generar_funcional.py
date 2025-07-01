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

@router.post("/", response_class=HTMLResponse)
async def generar_funcional(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Llama a la IA para generar el resumen funcional y retorna el bloque completo de análisis funcional para la home.
    """
    try:
        resultado_md = await generar_funcional_ia()
        # Guardar en BBDD
        doc = await save_markdown_document(session, content=resultado_md)
        resultado_md_db = doc.content if doc else resultado_md
        import markdown as md
        resultado_html = md.markdown(resultado_md_db or "", extensions=["extra", "tables", "fenced_code"])
        # Obtener el árbol de contenidos (índice)
        plantilla_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Documents", "Plantilla_Funcional.md"))
        indice = parse_template_tree(plantilla_path)
        return templates.TemplateResponse(
            "funcional_result_y_indice.html",
            {
                "request": request,
                "markdown_content": resultado_md_db,
                "vista_previa": resultado_html,
                "indice": indice,
                # Para compatibilidad con el template actual:
                "resultado_md": resultado_md_db,
                "resultado_html": resultado_html,
            }
        )
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
        # Obtener el árbol de contenidos (índice)
        plantilla_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Documents", "Plantilla_Funcional.md"))
        indice = parse_template_tree(plantilla_path)
        return templates.TemplateResponse(
            "funcional_result_y_indice.html",
            {
                "request": request,
                "markdown_content": resultado_md_db,
                "vista_previa": resultado_html,
                "indice": indice,
                # Para compatibilidad con el template actual:
                "resultado_md": resultado_md_db,
                "resultado_html": resultado_html,
            }
        )
    except Exception as e:
        logger.exception("Error al guardar el funcional editado")
        return HTMLResponse(f'<div class="text-red-600">Error: {str(e)}</div>', status_code=500)

# [EXPORTAR_WORD_COMENTADO] @router.post("/exportar")
# [EXPORTAR_WORD_COMENTADO] async def exportar_funcional(
# [EXPORTAR_WORD_COMENTADO]     markdown_content: str = Form(...),
# [EXPORTAR_WORD_COMENTADO]     formato: str = Form(...)
# [EXPORTAR_WORD_COMENTADO] ):
# [EXPORTAR_WORD_COMENTADO]     """
# [EXPORTAR_WORD_COMENTADO]     Exporta el markdown guardado (si existe) o el contenido recibido como Word o PDF.
# [EXPORTAR_WORD_COMENTADO]     """
# [EXPORTAR_WORD_COMENTADO]     try:
# [EXPORTAR_WORD_COMENTADO]         temp_path = "/tmp/funcional_guardado.md"
# [EXPORTAR_WORD_COMENTADO]         use_temp = False
# [EXPORTAR_WORD_COMENTADO]         if os.path.exists(temp_path):
# [EXPORTAR_WORD_COMENTADO]             with open(temp_path, encoding="utf-8") as f:
# [EXPORTAR_WORD_COMENTADO]                 contenido = f.read()
# [EXPORTAR_WORD_COMENTADO]             # Si el archivo temporal está vacío, usar el contenido recibido
# [EXPORTAR_WORD_COMENTADO]             if contenido.strip():
# [EXPORTAR_WORD_COMENTADO]                 use_temp = True
# [EXPORTAR_WORD_COMENTADO]             else:
# [EXPORTAR_WORD_COMENTADO]                 contenido = markdown_content
# [EXPORTAR_WORD_COMENTADO]         else:
# [EXPORTAR_WORD_COMENTADO]             contenido = markdown_content
# [EXPORTAR_WORD_COMENTADO]         # Exportar a Word
# [EXPORTAR_WORD_COMENTADO]         if formato == "word":
# [EXPORTAR_WORD_COMENTADO]             from docx import Document
# [EXPORTAR_WORD_COMENTADO]             doc = Document()
# [EXPORTAR_WORD_COMENTADO]             for line in contenido.splitlines():
# [EXPORTAR_WORD_COMENTADO]                 doc.add_paragraph(line)
# [EXPORTAR_WORD_COMENTADO]             with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
# [EXPORTAR_WORD_COMENTADO]                 doc.save(tmp.name)
# [EXPORTAR_WORD_COMENTADO]                 tmp.seek(0)
# [EXPORTAR_WORD_COMENTADO]                 return FileResponse(tmp.name, filename="funcional.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
# [EXPORTAR_WORD_COMENTADO]         # Exportar a PDF
# [EXPORTAR_WORD_COMENTADO]         elif formato == "pdf":
# [EXPORTAR_WORD_COMENTADO]             import markdown as md
# [EXPORTAR_WORD_COMENTADO]             html = md.markdown(contenido)
# [EXPORTAR_WORD_COMENTADO]             with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
# [EXPORTAR_WORD_COMENTADO]                 # pdfkit.from_string(html, tmp.name)  # Comentado para evitar error de importación
# [EXPORTAR_WORD_COMENTADO]                 tmp.seek(0)
# [EXPORTAR_WORD_COMENTADO]                 return FileResponse(tmp.name, filename="funcional.pdf", media_type="application/pdf")
# [EXPORTAR_WORD_COMENTADO]         else:
# [EXPORTAR_WORD_COMENTADO]             return JSONResponse({"success": False, "message": "Formato no soportado"}, status_code=400)
# [EXPORTAR_WORD_COMENTADO]     except Exception as e:
# [EXPORTAR_WORD_COMENTADO]         logger.exception("Error al exportar el funcional")
# [EXPORTAR_WORD_COMENTADO]         return JSONResponse({"success": False, "message": str(e)}, status_code=500)

@router.get("/loading", response_class=HTMLResponse)
async def loading_panel(request: Request):
    """
    Devuelve un panel de loading para mostrar mientras se genera el funcional.
    """
    return templates.TemplateResponse("panel_loading_funcional.html", {"request": request})

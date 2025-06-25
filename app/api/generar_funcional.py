"""
API route for generating functional summary using Azure OpenAI.
"""
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from app.services.generar_funcional_service import generar_funcional_ia
from fastapi.templating import Jinja2Templates
from app.utils.parse_template import parse_template_tree
import os
import logging
import markdown
import tempfile
import io

router = APIRouter(prefix="/api/generar-funcional", tags=["generar-funcional"])
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

@router.post("/", response_class=HTMLResponse)
async def generar_funcional(request: Request):
    """
    Llama a la IA para generar el resumen funcional y retorna HTML para el panel markdown y el árbol de contenidos.
    También actualiza el indicador de estado junto al botón.
    """
    try:
        resultado_md = await generar_funcional_ia()
        resultado_html = markdown.markdown(resultado_md or "", extensions=["extra", "tables", "fenced_code"])
        plantilla_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Documents", "Plantilla_Funcional.md"))
        indice = parse_template_tree(plantilla_path)
        return templates.TemplateResponse(
            "funcional_result_y_indice.html",
            {
                "request": request,
                "resultado_html": resultado_html,
                "resultado_md": resultado_md,
                "indice": indice
            }
        )
    except Exception as e:
        logger.exception("Error en /api/generar-funcional/")
        import traceback
        tb = traceback.format_exc()
        error_html = f'<span class="ml-2 text-red-600" hx-swap-oob="true" id="generar-funcional-indicador">Error: {str(e)}</span>'
        debug_html = f'<pre class="text-xs text-red-500 bg-red-50 p-2 rounded mt-2">{tb}</pre>'
        return HTMLResponse(error_html + debug_html, status_code=500)

@router.post("/guardar")
async def guardar_funcional(markdown_content: str = Form(...)):
    """
    Guarda el contenido markdown editado por el usuario.
    """
    try:
        # Por ahora, guardar en un archivo temporal. Se puede cambiar a base de datos si se requiere.
        with open("/tmp/funcional_guardado.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        return JSONResponse({"success": True, "message": "Cambios guardados correctamente."})
    except Exception as e:
        logger.exception("Error al guardar el funcional editado")
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

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
            import pdfkit
            html = md.markdown(contenido)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                pdfkit.from_string(html, tmp.name)
                tmp.seek(0)
                return FileResponse(tmp.name, filename="funcional.pdf", media_type="application/pdf")
        else:
            return JSONResponse({"success": False, "message": "Formato no soportado"}, status_code=400)
    except Exception as e:
        logger.exception("Error al exportar el funcional")
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

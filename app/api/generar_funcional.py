"""
API route for generating functional summary using Azure OpenAI.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.generar_funcional_service import generar_funcional_ia
from fastapi.templating import Jinja2Templates
from app.utils.parse_template import parse_template_tree
import os
import logging
import markdown

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

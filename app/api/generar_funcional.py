"""
API route for generating functional summary using Azure OpenAI.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.generar_funcional_service import generar_funcional_ia
from fastapi.templating import Jinja2Templates
from app.utils.parse_template import parse_template_tree
import os

router = APIRouter(prefix="/api/generar-funcional", tags=["generar-funcional"])
templates = Jinja2Templates(directory="templates")

@router.post("/", response_class=HTMLResponse)
async def generar_funcional(request: Request):
    """
    Llama a la IA para generar el resumen funcional y retorna HTML para el panel markdown y el árbol de contenidos.
    """
    resultado = await generar_funcional_ia()
    # Obtener el índice actualizado de la plantilla funcional
    plantilla_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Documents", "Plantilla_Funcional.md"))
    indice = parse_template_tree(plantilla_path)
    # Renderizar ambos fragmentos usando hx-swap-oob
    return templates.TemplateResponse(
        "funcional_result_y_indice.html",
        {"request": request, "resultado": resultado, "indice": indice}
    )

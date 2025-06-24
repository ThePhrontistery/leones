"""
API route for generating functional summary using Azure OpenAI.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.generar_funcional_service import generar_funcional_ia
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/api/generar-funcional", tags=["generar-funcional"])
templates = Jinja2Templates(directory="templates")

@router.post("/", response_class=HTMLResponse)
async def generar_funcional(request: Request):
    """
    Llama a la IA para generar el resumen funcional y retorna HTML para el panel markdown.
    """
    resultado = await generar_funcional_ia()
    return templates.TemplateResponse(
        "funcional_result.html", {"request": request, "resultado": resultado}
    )

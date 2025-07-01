"""
Rutas de frontend para el panel Chat IA (Agent) y sugerencias.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from fastapi import status
from fastapi.responses import RedirectResponse
from app.api.chat_sugerencias import SugerenciaResponse, generar_sugerencias

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/chat/sugerencias", response_class=HTMLResponse)
async def chat_sugerencias_panel(request: Request, contexto: str = ""):
    """
    Renderiza el panel de sugerencias de texto IA.
    """
    return templates.TemplateResponse(
        "chat_sugerencias.html",
        {"request": request, "contexto": contexto}
    )

@router.post("/api/chat/sugerencias", response_class=HTMLResponse)
async def chat_sugerencias_api(
    request: Request,
    prompt: str = Form(...),
    contexto: str = Form("")
):
    """
    Devuelve sugerencias de texto como HTML parcial para HTMX.
    """
    sugerencias = generar_sugerencias(prompt, contexto)
    return templates.TemplateResponse(
        "partials/sugerencias_list.html",
        {"request": request, "sugerencias": sugerencias}
    )

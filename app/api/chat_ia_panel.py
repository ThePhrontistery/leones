from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from app.api.chat_sugerencias import generar_sugerencias
from app.services.chat_ia_service import chat_ia_azure_openai
from app.services.markdown_funcional_service import get_markdown_funcional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Estado simple en memoria (solo para demo, no producción)
ultimo_prompt = ""
ultima_respuesta = ""

@router.post("/api/chat/ask", response_class=HTMLResponse)
async def chat_ia_ask(request: Request, prompt: str = Form(...)):
    global ultimo_prompt, ultima_respuesta
    ultimo_prompt = prompt
    contexto = get_markdown_funcional()
    ultima_respuesta = await chat_ia_azure_openai(prompt, contexto=contexto)
    return templates.TemplateResponse(
        "partials/chat_ia_panel.html",
        {"request": request, "prompt": ultimo_prompt, "respuesta": ultima_respuesta}
    )

@router.get("/api/chat/ultimo", response_class=HTMLResponse)
async def chat_ia_ultimo(request: Request):
    return templates.TemplateResponse(
        "partials/chat_ia_panel.html",
        {"request": request, "prompt": ultimo_prompt, "respuesta": ultima_respuesta}
    )

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
async def chat_ia_ask(request: Request, prompt: str = Form(...), contexto: str = Form("")):
    global ultimo_prompt, ultima_respuesta
    ultimo_prompt = prompt
    # DEBUG: Log para asegurar que el contexto no está vacío
    if not contexto or len(contexto.strip()) < 10:
        print("[ADVERTENCIA] El contexto enviado al chat IA está vacío o es muy corto.")
    else:
        print(f"[DEBUG] Longitud del contexto enviado a la IA: {len(contexto)} caracteres")
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

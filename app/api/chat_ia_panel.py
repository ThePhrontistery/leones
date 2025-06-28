from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from app.api.chat_sugerencias import generar_sugerencias
from app.services.chat_ia_service import chat_ia_azure_openai
from app.services.markdown_funcional_service import get_markdown_funcional_from_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Estado simple en memoria (solo para demo, no producción)
ultimo_prompt = ""
ultima_respuesta = ""

@router.post("/api/chat/ask", response_class=HTMLResponse)
async def chat_ia_ask(request: Request, prompt: str = Form(...), contexto: str = Form("")):
    global ultimo_prompt, ultima_respuesta
    ultimo_prompt = prompt

    # Obtener el contenido del documento funcional desde la base de datos
    markdown_context = await get_markdown_funcional_from_db()
    if not markdown_context.strip():
        print("[ADVERTENCIA] El documento funcional está vacío o no se pudo cargar desde la BBDD.")
    else:
        print(f"[DEBUG] Longitud del documento funcional enviado como contexto: {len(markdown_context)} caracteres")

    # Combinar el contexto proporcionado con el contenido del documento funcional
    contexto_completo = f"{contexto}\n\n{markdown_context}" if contexto.strip() else markdown_context

    ultima_respuesta = await chat_ia_azure_openai(prompt, contexto=contexto_completo)
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

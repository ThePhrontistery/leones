"""
API route for a simple chat endpoint that sends a fixed question to Azure OpenAI.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.chat_service import saludar_ia
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/api/chat", tags=["chat"])
templates = Jinja2Templates(directory="templates")

@router.post("/saludo", response_class=HTMLResponse)
async def saludo_chat(request: Request):
    """
    Llama a la IA para que dé los buenos días y retorna la respuesta.
    """
    resultado = await saludar_ia()
    return templates.TemplateResponse(
        "chat_result.html", {"request": request, "resultado": resultado}
    )

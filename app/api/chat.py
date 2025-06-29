"""
API route for a simple chat endpoint that sends a fixed question to Azure OpenAI.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.chat_service import saludar_ia
from app.services.document_store import get_documents

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

@router.get("/ultimo", response_class=HTMLResponse)
async def chat_ultimo(request: Request):
    """Devuelve el último mensaje del chat IA o el mensaje vacío si no hay documentos cargados."""
    docs = await get_documents()
    if not docs:
        # No hay documentos cargados
        return HTMLResponse(
            '<div class="min-h-[160px] max-h-[200px] overflow-y-auto font-mono text-xs bg-white rounded shadow p-2 border border-slate-200 w-full">No hay consulta aún.</div>'
        )
    # Validar que el último documento tenga un mensaje legible
    ultimo_doc = docs[-1]
    # Si el documento no es un string, mostrar mensaje amigable
    if not isinstance(ultimo_doc, str):
        return HTMLResponse(
            '<div class="min-h-[160px] max-h-[200px] overflow-y-auto font-mono text-xs bg-white rounded shadow p-2 border border-red-200 text-red-700 w-full">No hay mensajes de chat disponibles aún.</div>'
        )
    return templates.TemplateResponse(
        "chat_result.html", {"request": request, "resultado": ultimo_doc}
    )

"""
Servicio para interactuar con Azure OpenAI desde el chat IA (Agent).
"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

async def chat_ia_azure_openai(prompt: str, contexto: str | None = None) -> str:
    """
    Envía el prompt a Azure OpenAI y devuelve la respuesta del modelo.
    """
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT:
        return "[ERROR] Faltan variables de entorno para Azure OpenAI."
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_OPENAI_API_KEY,
        "Content-Type": "application/json",
    }
    messages = [
        {"role": "system", "content": "Eres un asistente experto en análisis y redacción de documentos funcionales."},
        {"role": "user", "content": prompt},
    ]
    if contexto:
        messages.insert(1, {"role": "user", "content": f"Contexto del documento funcional: {contexto}"})
    data = {
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[ERROR] {str(e)}"

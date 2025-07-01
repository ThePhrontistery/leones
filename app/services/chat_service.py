"""
Service for sending a fixed greeting question to Azure OpenAI.
"""
import os
from dotenv import load_dotenv
import httpx
from typing import Any

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

async def saludar_ia() -> str:
    """
    Envía una pregunta fija a la IA para que dé los buenos días.
    """
    prompt = "Da los buenos días de forma simpática."
    headers = {
        "api-key": AZURE_OPENAI_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "messages": [
            {"role": "system", "content": "Eres un asistente simpático."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result: Any = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] Ocurrió un error al llamar a la IA: {str(e)}"

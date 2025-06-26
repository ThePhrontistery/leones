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
    El prompt del sistema fuerza a la IA a responder solo usando el documento funcional proporcionado.
    Además, imprime en consola el detalle de la llamada y la respuesta para depuración.
    """
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT:
        return "[ERROR] Faltan variables de entorno para Azure OpenAI."
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_OPENAI_API_KEY,
        "Content-Type": "application/json",
    }
    system_prompt = (
        "Eres un asistente experto en análisis funcional. "
        "Responde la siguiente pregunta del usuario usando solo la información del documento funcional proporcionado como contexto. "
        "La respuesta debe ser relativa y específica al documento funcional de entrada."
    )
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    if contexto:
        messages.append({
            "role": "user",
            "content": f"DOCUMENTO FUNCIONAL (contexto):\n\n{contexto}"
        })
    messages.append({
        "role": "user",
        "content": f"PREGUNTA DEL USUARIO: {prompt}"
    })
    data = {
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    # DEBUG: Mostrar el prompt completo que se envía a la IA
    print("\n========== PROMPT ENVIADO A AZURE OPENAI ==========")
    for m in messages:
        print(f"[{m['role'].upper()}]:\n{m['content']}\n")
    print("==================================================\n")
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            # DEBUG: Mostrar la respuesta cruda de la IA
            print("========== RESPUESTA DE AZURE OPENAI =============")
            print(result)
            print("==================================================\n")
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[ERROR] {str(e)}"

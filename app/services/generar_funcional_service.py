"""
Service for generating functional summary using Azure OpenAI.
"""
import os
from dotenv import load_dotenv
import httpx
from typing import Any
import asyncio
from app.services.document_store import get_documents
from app.utils.file_text import extract_text_from_file
from app.utils.parse_template import parse_template_tree

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

async def generar_funcional_ia() -> str:
    """
    Llama a Azure OpenAI para generar el resumen funcional del documento más reciente cargado,
    siguiendo la estructura de la plantilla funcional (índice).
    Devuelve texto plano. Si ocurre un error, devuelve el mensaje de error.
    """
    try:
        documentos = await get_documents()
        if not documentos:
            return "No hay documentos cargados para analizar."
        # Usar solo el documento más reciente
        doc = max(documentos, key=lambda d: d.fecha_carga)
        texto = await extract_text_from_file(doc.file_path)
        if not texto or (isinstance(texto, str) and texto.strip() == ""):
            return f"No se pudo extraer texto del documento: {doc.file_name}"
        if isinstance(texto, str) and texto.strip().startswith("[ERROR]"):
            return texto  # Devuelve el mensaje de error detallado
        # Obtener el índice de la plantilla funcional
        import os
        plantilla_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Documents", "Plantilla_Funcional.md"))
        indice = parse_template_tree(plantilla_path)
        # Construir el esquema de secciones en markdown
        import re
        def safe_anchor(title: str) -> str:
            anchor = title.lower()
            anchor = re.sub(r'[áÁ]', 'a', anchor)
            anchor = re.sub(r'[éÉ]', 'e', anchor)
            anchor = re.sub(r'[íÍ]', 'i', anchor)
            anchor = re.sub(r'[óÓ]', 'o', anchor)
            anchor = re.sub(r'[úÚ]', 'u', anchor)
            anchor = re.sub(r'[ñÑ]', 'n', anchor)
            anchor = re.sub(r'[^a-z0-9_\- ]', '', anchor)
            anchor = anchor.replace(' ', '_')
            return anchor
        def secciones_markdown(arbol):
            md = ""
            for nodo in arbol:
                anchor = safe_anchor(nodo['title'])
                md += f"# {nodo['title']} {{#{anchor}}}\n\n"
                for hijo in nodo.get("children", []):
                    child_anchor = safe_anchor(hijo['title'])
                    md += f"## {hijo['title']} {{#{child_anchor}}}\n\n"
            return md
        esquema = secciones_markdown(indice)
        prompt = (
            f"A continuación tienes el contenido del documento '{doc.file_name}'. "
            "Resume su información en un análisis funcional claro y estructurado, siguiendo exactamente el siguiente esquema de secciones en markdown. "
            "Rellena cada sección y subsección con la información relevante del documento. Si alguna sección no aplica, indícalo brevemente.\n\n"
            f"ESQUEMA:\n{esquema}\n\nCONTENIDO DEL DOCUMENTO:\n{texto}"
        )
        headers = {
            "api-key": AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json",
        }
        data = {
            "messages": [
                {"role": "system", "content": "Eres un analista funcional experto."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 1800,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result: Any = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] Ocurrió un error al procesar el documento o llamar a la IA: {str(e)}"

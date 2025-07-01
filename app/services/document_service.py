"""
Service for handling document uploads and metadata persistence.
"""
import os
from datetime import datetime
from typing import Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.models.document import UploadedDocument
from app.db.models import UploadedFile
from app.db.session import AsyncSessionLocal
from app.utils.parse_template import parse_template_sections
from app.utils.file_text import extract_text_from_file, extract_text_from_pdf, extract_image_info
from app.services.document_store import get_documents
from app.config import settings

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")

async def save_uploaded_document(
    file_bytes: bytes,
    file_name: str,
    categoria: str,
    descripcion: Optional[str] = None,
    proyecto: str = "demo_metasketch",
) -> UploadedDocument:
    """
    Save uploaded file to disk and persist metadata in DB.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    fecha_carga = datetime.utcnow()
    async with AsyncSessionLocal() as session:
        db_file = UploadedFile(
            filename=file_name,
            file_path=file_path,
            categoria=categoria,
            descripcion=descripcion,
            proyecto=proyecto,
            upload_time=fecha_carga,
        )
        session.add(db_file)
        await session.commit()
    doc = UploadedDocument(
        fecha_carga=fecha_carga,
        file_name=file_name,
        file_path=file_path,
        proyecto=proyecto,
        categoria=categoria,
        descripcion=descripcion,
    )
    return doc

async def generate_functional_document() -> Tuple[str, List[str], str]:
    """
    Genera el documento funcional usando la plantilla y los documentos cargados en base de datos, llamando a Azure OpenAI.
    Returns:
        Tuple con (documento funcional generado, índice de secciones, prompt usado)
    """
    docs = await get_documents()  # Siempre lee de la tabla UploadedFile
    documentos_entrada = []
    archivos_sin_texto = []
    for doc in docs:
        texto = await extract_text_from_file(doc.file_path)
        if texto and texto.strip():
            documentos_entrada.append(f"--- {doc.file_name} ---\n{texto}")
        else:
            archivos_sin_texto.append(doc.file_name)
    if not documentos_entrada:
        raise Exception("No se pudo extraer texto ni información útil de los documentos subidos.")
    documentos_entrada_md = "\n\n".join(documentos_entrada)
    # Leer plantilla y extraer secciones
    template_path = "app/Documents/Plantilla_Funcional.md"
    sections = parse_template_sections(template_path)
    with open(template_path, encoding="utf-8") as f:
        plantilla_md = f.read()
    # Prompt explícito para la IA: NO puede usar imágenes como contexto visual o referencia
    prompt = f"""
Eres un analista funcional experto en software. A continuación tienes una plantilla de documento funcional y una serie de documentos de entrada (pueden incluir archivos Word, PDF, TXT, MD y también imágenes). Analiza cuidadosamente el contenido de los documentos de entrada y genera un documento funcional completo siguiendo EXACTAMENTE la estructura y secciones de la plantilla (no añadas ni elimines secciones, solo rellena el contenido de cada una). El resultado debe estar en formato Markdown y debe ser lo más detallado y profesional posible.

IMPORTANTE: NO puedes usar la información de imágenes (JPG, PNG, etc.) como contexto visual ni referencia. Ignora cualquier archivo que no sea texto. Devuelve únicamente el documento funcional generado en Markdown, sin explicaciones adicionales, encabezados, ni comentarios fuera del documento.

---

Plantilla de documento funcional:
{plantilla_md}

Documentos de entrada:
{documentos_entrada_md}

---

Genera el documento funcional completo siguiendo la plantilla y usando toda la información relevante de los documentos de entrada.
"""

    # 4. Llamar a Azure OpenAI (API REST)
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not (api_key and endpoint and deployment):
        raise RuntimeError("Faltan variables de entorno para Azure OpenAI")
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-02-15-preview"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": "Eres un analista funcional experto en documentación de software."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.2,
        "top_p": 1.0,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

    # 5. Devuelve el documento funcional generado, el índice y el prompt
    return content, sections, prompt

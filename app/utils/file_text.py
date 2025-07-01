"""
Utility for extracting text from uploaded files for AI processing.
Soporta: .txt, .md, .pdf, .docx. (No OCR de imágenes por defecto)
"""
from typing import Optional
import os
import markdown
import re
import base64
from PIL import Image
import io

async def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extrae texto de archivos .txt, .md, .pdf, .docx. Si es imagen, devuelve None (no error).
    Devuelve errores detallados para depuración.
    """
    import traceback
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in {".txt", ".md"}:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".pdf":
            from .file_text import extract_text_from_pdf
            return extract_text_from_pdf(file_path)
        elif ext == ".docx":
            try:
                import docx
            except ImportError:
                return "[ERROR] Falta python-docx para leer DOCX."
            try:
                doc = docx.Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                return f"[ERROR] python-docx no pudo leer el archivo: {e}\n{traceback.format_exc()}"
        elif ext in {".jpg", ".jpeg", ".png"}:
            # Es imagen, no extraer texto ni devolver error
            return None
        else:
            return f"[ERROR] Formato no soportado: {ext}"
    except Exception as e:
        return f"[ERROR] Error inesperado: {e}\n{traceback.format_exc()}"

def markdown_to_html(md: str) -> str:
    """
    Convierte markdown a HTML, añadiendo id a los headings si tienen {#anchor} al final.
    """
    # Reemplaza encabezados tipo '# Título {#anchor}' por '# Título' y guarda el id
    def heading_id_replacer(match):
        hashes, title, anchor = match.group(1), match.group(2), match.group(3)
        return f"{hashes} {title} <span data-anchor='{anchor}'></span>"
    md = re.sub(r'^(#+)\s+(.+?)\s*\{#([a-z0-9_\-]+)\}$', heading_id_replacer, md, flags=re.MULTILINE)
    html = markdown.markdown(md, extensions=["extra", "toc"])
    # Añade el id a los headings usando el span auxiliar
    html = re.sub(r'<(h[12])>([^<]+?) <span data-anchor=\'([a-z0-9_\-]+)\'></span></h[12]>',
                  lambda m: f'<{m.group(1)} id="{m.group(3)}">{m.group(2)}</{m.group(1)}>',
                  html)
    return html

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrae el texto de un archivo PDF usando pypdf (puro Python).
    Devuelve el texto concatenado de todas las páginas.
    """
    from pypdf import PdfReader
    text = []
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)

def extract_image_info(file_path: str) -> str:
    """
    Extrae información básica de una imagen: dimensiones, modo y base64 (primeros bytes).
    No hace OCR ni análisis visual profundo.
    """
    try:
        with open(file_path, "rb") as f:
            img_bytes = f.read()
        img = Image.open(io.BytesIO(img_bytes))
        info = f"Imagen: {os.path.basename(file_path)}\nDimensiones: {img.width}x{img.height}\nModo: {img.mode}\n"
        # Adjuntar una muestra base64 (limitada para no saturar el prompt)
        b64 = base64.b64encode(img_bytes[:2048]).decode("utf-8")
        info += f"Base64 (primeros 2KB): {b64}"
        return info
    except Exception as e:
        return f"[ERROR] No se pudo procesar la imagen {file_path}: {e}"

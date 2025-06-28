"""
Utility for extracting text from uploaded files for AI processing.
Soporta: .txt, .md, .pdf, .docx. (No OCR de imágenes por defecto)
"""
from typing import Optional
import os
import markdown
import re

async def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extrae texto de archivos .txt, .md, .pdf, .docx. Ignora imágenes si no hay OCR disponible.
    Devuelve errores detallados para depuración.
    """
    import traceback
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in {".txt", ".md"}:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".pdf":
            try:
                import pdfplumber
            except ImportError:
                return "[ERROR] Falta pdfplumber para leer PDF."
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
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
    Extrae el texto de un archivo PDF usando pdfplumber.
    Devuelve el texto concatenado de todas las páginas.
    """
    import pdfplumber
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

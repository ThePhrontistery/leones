"""
Utility for extracting text from uploaded files for AI processing.
Soporta: .txt, .md, .pdf, .docx. (No OCR de imágenes por defecto)
"""
from typing import Optional
import os

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

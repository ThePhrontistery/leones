"""
Utility for extracting text from uploaded files for AI processing.
Soporta: .txt, .md, .pdf, .docx. (No OCR de imágenes por defecto)
"""
from typing import Optional
import os

async def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extrae texto de archivos .txt, .md, .pdf, .docx. Ignora imágenes si no hay OCR disponible.
    """
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in {".txt", ".md"}:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".pdf":
            try:
                import pdfplumber
            except ImportError:
                return None
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        elif ext == ".docx":
            try:
                import docx
            except ImportError:
                return None
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        # No OCR ni pytesseract por defecto
        else:
            return None
    except Exception:
        return None

"""
Utilidad para parsear la plantilla funcional y extraer las secciones principales.
"""
from typing import List


def parse_template_sections(template_path: str) -> List[str]:
    """
    Parsea un archivo Markdown de plantilla y extrae los títulos de primer y segundo nivel como índice.
    Args:
        template_path: Ruta al archivo de plantilla Markdown.
    Returns:
        Lista de secciones (títulos) en orden.
    """
    sections = []
    with open(template_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("# ") or line.startswith("## "):
                sections.append(line.strip("# ").strip())
    return sections

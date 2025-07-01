"""
Utilidad para parsear la plantilla funcional y extraer las secciones principales.
"""
from typing import List, Dict, Any


def parse_template_tree(template_path: str) -> List[Dict[str, Any]]:
    """
    Parsea un archivo Markdown y devuelve una estructura de árbol de encabezados (nivel 1 y 2).
    Args:
        template_path: Ruta al archivo Markdown.
    Returns:
        Lista de dicts con 'title' y opcionalmente 'children'.
    """
    tree = []
    current = None
    with open(template_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("# "):
                current = {"title": line.strip("# ").strip(), "children": []}
                tree.append(current)
            elif line.startswith("## ") and current:
                current["children"].append({"title": line.strip("# ").strip()})
    return tree


def parse_template_sections(template_path: str) -> list[str]:
    """
    Parsea un archivo Markdown de plantilla y extrae los títulos de primer y segundo nivel como índice plano.
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

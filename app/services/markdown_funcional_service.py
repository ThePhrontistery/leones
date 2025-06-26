"""
Servicio para obtener el contenido actual del documento funcional en edición (Markdown).
"""
import os

def get_markdown_funcional() -> str:
    """
    Devuelve el contenido markdown del documento funcional actualmente en edición.
    """
    temp_path = "/tmp/funcional_guardado.md"
    if os.path.exists(temp_path):
        with open(temp_path, encoding="utf-8") as f:
            contenido = f.read()
        return contenido
    return ""

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
    # Si no existe el archivo temporal, intentar obtener el contenido del editor (última generación)
    # Buscar en la última generación de funcional_result_y_indice.html
    # (opcional: aquí podrías buscar en base de datos o en otro almacenamiento)
    return ""

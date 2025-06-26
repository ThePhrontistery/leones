"""
Servicio para obtener el contenido actual del documento funcional en edición (Markdown).
"""
import os

def get_markdown_funcional() -> str:
    """
    Devuelve el contenido markdown del documento funcional actualmente en edición.
    Si no existe el archivo temporal, intenta obtener el contenido desde el último documento funcional generado.
    """
    temp_path = "/tmp/funcional_guardado.md"
    if os.path.exists(temp_path):
        with open(temp_path, encoding="utf-8") as f:
            contenido = f.read()
        if contenido.strip():
            return contenido

    # Intentar obtener el contenido desde el último documento funcional generado
    generated_path = "uploaded_docs/MVP Metasketch MRS_funcional-Margarita OK.docx"
    if os.path.exists(generated_path):
        try:
            import docx
            doc = docx.Document(generated_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"[ERROR] No se pudo leer el documento funcional generado: {e}")

    # Si no se encuentra contenido, devolver una advertencia
    return "[ADVERTENCIA] No se encontró contenido funcional para enviar como contexto."

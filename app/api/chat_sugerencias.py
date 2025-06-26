"""
API para sugerencias de texto generadas por IA en el panel Chat IA (Agent).
Define modelos y función utilitaria para sugerencias.
"""
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

class SugerenciaRequest(BaseModel):
    prompt: str
    contexto: str | None = None

class SugerenciaResponse(BaseModel):
    sugerencias: List[str]

def generar_sugerencias(prompt: str, contexto: str | None = None) -> list[str]:
    """
    Devuelve sugerencias de texto generadas por IA según el prompt y contexto opcional.
    """
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt vacío.")
    return [
        f"Sugerencia 1 para: {prompt}",
        f"Sugerencia 2 para: {prompt}",
        f"Sugerencia 3 para: {prompt}",
    ]

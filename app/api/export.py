"""
API para exportar documentos funcionales en formato Word (.docx).
"""
from fastapi import APIRouter, Form, Response
from fastapi.responses import StreamingResponse
from app.services.export_service import markdown_to_docx
from typing import Annotated

router = APIRouter(prefix="/api/export", tags=["export"])

@router.post("/", response_class=StreamingResponse)
async def export_markdown(
    markdown_text: Annotated[str, Form(...)],
    format: Annotated[str, Form(...)] = "word",
):
    """
    Exporta el markdown recibido a un archivo Word (.docx) y lo descarga.
    """
    if format != "word":
        return Response("Formato no soportado", status_code=400)
    docx_io = await markdown_to_docx(markdown_text)
    headers = {
        "Content-Disposition": "attachment; filename=funcional.docx"
    }
    return StreamingResponse(docx_io, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers=headers)

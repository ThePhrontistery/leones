"""
API endpoints for saving and retrieving Markdown documents.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.markdown import MarkdownDocument
from app.db.markdown import get_markdown_document, save_markdown_document
from app.db.session import get_async_session
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/api/markdown", tags=["markdown"])
templates = Jinja2Templates(directory="templates")

@router.post("/save", response_model=MarkdownDocument)
async def save_markdown(
    data: MarkdownDocument,
    session: AsyncSession = Depends(get_async_session),
):
    """Save or update the markdown document (single global doc)."""
    doc = await save_markdown_document(session, content=data.content)
    return MarkdownDocument.from_orm(doc)

@router.get("/get", response_class=HTMLResponse)
async def get_markdown_html(session: AsyncSession = Depends(get_async_session)):
    """Devuelve el textarea con el contenido markdown guardado (para HTMX)."""
    doc = await get_markdown_document(session)
    content = doc.content if doc else ""
    return HTMLResponse(
        f'<textarea class="whitespace-pre-wrap font-mono text-sm bg-slate-50 p-3 rounded border border-slate-200 overflow-x-auto overflow-y-auto h-full min-h-0 w-full resize-none focus:outline-none focus:ring-2 focus:ring-blue-400" id="markdown-editor-content" name="markdown-editor-content" spellcheck="false" hx-get=\"/api/markdown/get\" hx-trigger=\"load\" hx-target=\"#markdown-editor-content\" hx-swap=\"outerHTML\">{content}</textarea>'
    )

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.db.markdown import get_markdown_document
import markdown as mdlib

router = APIRouter()

@router.post("/api/markdown/preview", response_class=HTMLResponse)
async def markdown_preview(request: Request, session: AsyncSession = Depends(get_async_session)):
    data = await request.json()
    content = data.get("content", "")
    html = mdlib.markdown(content or "", extensions=["extra", "tables", "fenced_code"])
    return HTMLResponse(html)

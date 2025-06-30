"""Metasketch: un experimento VibeCoding
Entry-point & composition root."""
import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.router import router as api_router
from app.db import init
from app.db.init_db import init_markdown_table
from app.db.session import engine, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.markdown import get_markdown_document
import markdown as mdlib

templates = Jinja2Templates(directory="templates")
app = FastAPI(title="AI Web Template")

@app.on_event("startup")
async def on_startup() -> None:
    # Inicializa la tabla users y el usuario admin
    await init.init_db()
    # Inicializa la tabla markdown_documents
    await init_markdown_table(engine)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, session: AsyncSession = Depends(get_async_session)):
    user = request.cookies.get("user")
    if not user:
        # Siempre redirige a login si no hay cookie
        return RedirectResponse("/login")
    doc = await get_markdown_document(session)
    markdown_content = doc.content if doc else ""
    vista_previa = mdlib.markdown(markdown_content or "", extensions=["extra", "tables", "fenced_code"])
    funcional_existe = bool(doc and doc.content.strip())
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Metasketch: un experimento VibeCoding",
            "user": user,
            "markdown_content": markdown_content,
            "vista_previa": vista_previa,
            "funcional_existe": funcional_existe
        }
    )

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploaded_docs", StaticFiles(directory="uploaded_docs"), name="uploaded_docs")

if __name__ == "__main__":             # `python -m app.main`
    import uvicorn
    
    uvicorn.run(
        "app.__main__:app",  # Import the FastAPI app instance,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

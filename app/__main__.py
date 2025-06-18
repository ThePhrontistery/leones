"""Entry‑point & composition root."""
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.router import router as api_router
from app.db import init

import asyncio

templates = Jinja2Templates(directory="templates")
app = FastAPI(title="AI Web Template")

@app.on_event("startup")
async def on_startup() -> None:
    # Inicializa la tabla users y el usuario admin
    await init.init_db()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Home", "user": user}
    )

app.include_router(api_router)

if __name__ == "__main__":             # `python -m app.main`
    import uvicorn
    
    uvicorn.run(
        "app.__main__:app",  # Import the FastAPI app instance,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

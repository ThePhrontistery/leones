"""Rutas de autenticación: login de usuario."""
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import init
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """Renderiza el formulario de login."""
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login", "error": None})

@router.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request, user: str = Form(...), password: str = Form(...)):
    """Procesa el login y redirige a home si es correcto."""
    db_user = await init.get_user(user)
    if db_user and pwd_context.verify(password, db_user["password"]):
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie("user", user, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login", "error": "Usuario o contraseña incorrectos"})

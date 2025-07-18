"""Example endpoints — extend or split into sub‑routers as needed."""
from fastapi import APIRouter

from .ping import router as ping_router
from .auth import router as auth_router
from .logout import router as logout_router
from .document import router as document_router
from .generar_funcional import router as generar_funcional_router
from .chat import router as chat_router
from .chat_sugerencias_panel import router as chat_sugerencias_panel_router
from .chat_ia_panel import router as chat_ia_panel_router
from .markdown import router as markdown_router
from .markdown_preview import router as markdown_preview_router
from .export import router as export_router

router = APIRouter()
router.include_router(ping_router)
router.include_router(auth_router)
router.include_router(logout_router)
router.include_router(document_router)
router.include_router(generar_funcional_router)
router.include_router(chat_router)
router.include_router(chat_sugerencias_panel_router)
router.include_router(chat_ia_panel_router)
router.include_router(markdown_router)
router.include_router(markdown_preview_router)
router.include_router(export_router)


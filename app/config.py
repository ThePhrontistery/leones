"""Configuración global de la aplicación: carga variables de entorno."""
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    env: str = os.getenv("ENV", "development")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", 8000))
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./leones.db")

settings = Settings()

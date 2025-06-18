"""Inicialización y acceso a la base de datos SQLite (async) ."""
import aiosqlite
from passlib.context import CryptContext

DB_PATH = "./app.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_db() -> None:
    """Crea la tabla 'users' si no existe e inserta admin si es necesario."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
            """
        )
        # Verifica si existe el usuario admin
        async with db.execute("SELECT * FROM users WHERE user = 'admin'") as cursor:
            row = await cursor.fetchone()
            if not row:
                hashed = pwd_context.hash("admin")
                await db.execute(
                    "INSERT INTO users (user, password) VALUES (?, ?)",

                    ("admin", hashed)
                )
        await db.commit()

async def get_user(user: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user = ?", (user,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

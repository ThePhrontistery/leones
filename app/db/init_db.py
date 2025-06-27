"""
Inicializa la tabla markdown_documents si no existe.
"""
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

async def init_markdown_table(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS markdown_documents (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL
                )
                """
            )
        )

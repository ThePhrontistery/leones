"""
CRUD and DB logic for MarkdownDocument.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.markdown import MarkdownDocumentORM

async def get_markdown_document(session: AsyncSession, doc_id: int = 1) -> MarkdownDocumentORM | None:
    result = await session.execute(select(MarkdownDocumentORM).where(MarkdownDocumentORM.id == doc_id))
    return result.scalars().first()

async def save_markdown_document(session: AsyncSession, content: str, doc_id: int = 1) -> MarkdownDocumentORM:
    doc = await get_markdown_document(session, doc_id)
    if doc:
        await session.execute(
            update(MarkdownDocumentORM)
            .where(MarkdownDocumentORM.id == doc_id)
            .values(content=content)
        )
    else:
        doc = MarkdownDocumentORM(id=doc_id, content=content)
        session.add(doc)
    await session.commit()
    return await get_markdown_document(session, doc_id)

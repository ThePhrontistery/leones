"""
In-memory store for uploaded documents (demo only).
"""
from typing import List
from app.models.document import UploadedDocument

documents: List[UploadedDocument] = []

def add_document(doc: UploadedDocument) -> None:
    documents.append(doc)

def get_documents() -> List[UploadedDocument]:
    return documents

def clear_documents() -> None:
    documents.clear()

"""
Utility for extracting text from uploaded files for AI processing.
"""
from typing import Optional

async def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extract text content from a file for AI usage. (Simple plain text for now)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

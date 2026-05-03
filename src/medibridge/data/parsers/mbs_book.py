"""MBS Book PDF -> chunks (configured page range)."""
from __future__ import annotations

from pathlib import Path

import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

from medibridge.config import MBS_BOOK_EXPLANATORY_PAGES

_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " "]
)


def parse_mbs_book(path: Path, page_range: tuple[int, int] | None = None) -> list[dict]:
    start, end = page_range or MBS_BOOK_EXPLANATORY_PAGES
    chunks: list[dict] = []
    doc = pymupdf.open(str(path))
    try:
        end = min(end, doc.page_count)
        for page_idx in range(start, end + 1):
            page = doc[page_idx - 1]
            text = page.get_text()
            if not text.strip():
                continue
            for ci, chunk in enumerate(_SPLITTER.split_text(text)):
                chunks.append({
                    "text": chunk,
                    "metadata": {
                        "source": "mbs_book",
                        "page_num": page_idx,
                        "chunk_index": ci,
                    },
                })
    finally:
        doc.close()
    return chunks

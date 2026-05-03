"""MBS Item Information PDF -> chunks."""
from __future__ import annotations

from pathlib import Path

import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " "]
)


def parse_mbs_item_info(path: Path) -> list[dict]:
    chunks: list[dict] = []
    doc = pymupdf.open(str(path))
    try:
        for page_idx, page in enumerate(doc, start=1):
            text = page.get_text()
            if not text.strip():
                continue
            for ci, chunk in enumerate(_SPLITTER.split_text(text)):
                chunks.append({
                    "text": chunk,
                    "metadata": {
                        "source": "mbs_item_info",
                        "page_num": page_idx,
                        "chunk_index": ci,
                    },
                })
    finally:
        doc.close()
    return chunks

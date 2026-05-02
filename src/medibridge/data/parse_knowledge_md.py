"""Curated knowledge .md -> chunks."""
from __future__ import annotations

import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from medibridge.config import INSURERS_KNOWLEDGE_DIR, REFERENCE_KNOWLEDGE_DIR

_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " "]
)

_INSURER_KEYS = ("allianz", "bupa", "cbhs", "medibank", "ahm", "nib")


def _infer_insurer_id(path: Path) -> str | None:
    # Prefer parent folder name (e.g. knowledge/insurers/allianz/ → "allianz")
    parent = path.parent.name.lower()
    for key in _INSURER_KEYS:
        if key in parent:
            return key
    # Fall back to filename
    for key in _INSURER_KEYS:
        if key in path.name.lower():
            return key
    return None


def _split_by_h2(text: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, body) sections by ## headers."""
    parts = re.split(r"(^## .+$)", text, flags=re.MULTILINE)
    sections: list[tuple[str, str]] = []
    current_heading = ""
    buffer: list[str] = []
    for part in parts:
        if part.startswith("## "):
            if buffer:
                sections.append((current_heading, "".join(buffer).strip()))
                buffer = []
            current_heading = part.strip()
        else:
            buffer.append(part)
    if buffer:
        sections.append((current_heading, "".join(buffer).strip()))
    return [(h, b) for h, b in sections if b]


def parse_knowledge_md() -> list[dict]:
    chunks: list[dict] = []

    # Collect all .md files: insurers/**/*.md + reference/*.md
    md_files: list[Path] = []
    if INSURERS_KNOWLEDGE_DIR.exists():
        md_files.extend(INSURERS_KNOWLEDGE_DIR.rglob("*.md"))
    if REFERENCE_KNOWLEDGE_DIR.exists():
        md_files.extend(REFERENCE_KNOWLEDGE_DIR.glob("*.md"))

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        insurer_id = _infer_insurer_id(path)
        is_comparison = path.name.startswith("comparison-")
        is_reference = path.parent == REFERENCE_KNOWLEDGE_DIR

        for heading, body in _split_by_h2(text):
            section_chunks = [body] if len(body) <= 1000 else _SPLITTER.split_text(body)
            for ci, chunk in enumerate(section_chunks):
                chunks.append({
                    "text": chunk,
                    "metadata": {
                        "source": "reference_md" if is_reference else "knowledge_md",
                        "insurer_id": insurer_id,
                        "is_comparison": is_comparison,
                        "section": heading,
                        "filename": path.name,
                        "chunk_index": ci,
                    },
                })
    return chunks

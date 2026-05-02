"""Hybrid search: ChromaDB vector + SQLite FTS5."""
from __future__ import annotations

from langchain_core.tools import tool

from medibridge.config import CHROMA_MBS_COLLECTION
from medibridge.data import db as dbmod
from medibridge.data.vectorstore import get_client, get_or_create_collection, query_mbs


def _hybrid_search(query: str, top_k: int = 5) -> list[dict]:
    # Vector results
    try:
        client = get_client()
        coll = get_or_create_collection(client, CHROMA_MBS_COLLECTION)
        vec_results = query_mbs(coll, query, n_results=20)
    except Exception:
        vec_results = []
    vec_scores: dict[str, float] = {}
    for i, r in enumerate(vec_results):
        item_num = r["metadata"].get("item_num")
        if not item_num:
            continue
        # smaller distance = better; convert to score in [0,1]
        dist = r.get("distance") or 0.0
        vec_scores[item_num] = max(vec_scores.get(item_num, 0.0), 1.0 - dist)

    # FTS5 results
    fts_scores: dict[str, float] = {}
    with dbmod.get_conn() as conn:
        fts_rows = dbmod.search_items_by_keyword(conn, query, limit=20)
    for i, r in enumerate(fts_rows):
        item_num = r["item_num"]
        # rank is negative; rows ordered best-first. score = 1/(i+1)
        fts_scores[item_num] = 1.0 / (i + 1)

    # Merge
    all_items = set(vec_scores) | set(fts_scores)
    merged = []
    for item_num in all_items:
        score = 0.6 * vec_scores.get(item_num, 0.0) + 0.4 * fts_scores.get(item_num, 0.0)
        merged.append((item_num, score))
    merged.sort(key=lambda x: x[1], reverse=True)
    top_items = [m[0] for m in merged[:top_k]]

    # Hydrate from SQLite
    out: list[dict] = []
    with dbmod.get_conn() as conn:
        for item_num in top_items:
            row = dbmod.get_item_by_number(conn, item_num)
            if row:
                out.append(row)
    return out


@tool
def search_mbs_items(query: str, top_k: int = 5) -> list[dict]:
    """Search MBS items by natural-language description or keyword.
    Returns up to top_k items with item_num, description, schedule_fee, benefits, category."""
    return _hybrid_search(query, top_k)


@tool
def lookup_mbs_item(item_num: str) -> dict | None:
    """Look up a specific MBS item by its item number."""
    with dbmod.get_conn() as conn:
        return dbmod.get_item_by_number(conn, str(item_num))

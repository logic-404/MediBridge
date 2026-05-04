from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from medibridge.tools.mbs_lookup import lookup_mbs_item, search_mbs_items

router = APIRouter()


@router.get("/mbs/search")
def get_search(q: str = Query(..., min_length=1), limit: int = Query(8, ge=1, le=25)) -> list[dict]:
    return search_mbs_items.invoke({"query": q, "top_k": limit})


@router.get("/mbs/{item_num}")
def get_item(item_num: str) -> dict:
    item = lookup_mbs_item.invoke({"item_num": item_num})
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_num} not found")
    return item

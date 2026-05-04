from __future__ import annotations

from fastapi import APIRouter

from medibridge.profile import list_insurers

router = APIRouter()


@router.get("/insurers")
def get_insurers() -> list[dict]:
    return list_insurers()

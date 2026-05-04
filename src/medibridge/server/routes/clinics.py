from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from medibridge.data.queries import ALLOWED_BILLING, ALLOWED_CLINIC_TYPES
from medibridge.tools.clinic_search import search_clinics

router = APIRouter()


@router.get("/clinics/types")
def get_types() -> list[str]:
    return sorted(ALLOWED_CLINIC_TYPES)


@router.get("/clinics/billing")
def get_billing() -> list[str]:
    # Surface in student-priority order so the frontend can render chips top-down.
    return ["bulk", "mixed", "private", "unknown"]


@router.get("/clinics")
def get_clinics(
    postcode: str | None = Query(None),
    suburb: str | None = Query(None),
    type: str | None = Query(None, description="One of GP, Psychology, Pharmacy, Psychiatry, Hospital"),
    billing: str | None = Query(None, description="One of bulk, mixed, private, unknown"),
) -> list[dict]:
    if not postcode and not suburb:
        return []
    if type and type not in ALLOWED_CLINIC_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"type must be one of {sorted(ALLOWED_CLINIC_TYPES)}",
        )
    if billing and billing.lower() not in ALLOWED_BILLING:
        raise HTTPException(
            status_code=400,
            detail=f"billing must be one of {sorted(ALLOWED_BILLING)}",
        )
    rows = search_clinics.invoke(
        {"postcode": postcode, "suburb": suburb, "clinic_type": type, "billing": billing}
    )
    # tool returns a single-element error list when nothing matched — normalize to []
    if rows and isinstance(rows[0], dict) and "error" in rows[0]:
        return []
    return rows

"""Clinic directory lookup (Queensland). Postcode/suburb match — no geo radius."""
from __future__ import annotations

from langchain_core.tools import tool

from medibridge.data import db as dbmod
from medibridge.data import queries
from medibridge.data.queries import ALLOWED_CLINIC_TYPES

_DROP_FIELDS = {"phone", "hours", "latitude", "longitude"}


@tool
def search_clinics(
    postcode: str | None = None,
    suburb: str | None = None,
    clinic_type: str | None = None,
) -> list[dict]:
    """Find Queensland clinics, pharmacies, or hospitals by postcode or suburb.

    Args:
        postcode: 4-digit Australian postcode (e.g. "4000"). Provide this OR suburb.
        suburb: Suburb name (e.g. "Brisbane City"). Provide this OR postcode.
        clinic_type: Optional filter. One of: GP, Psychology, Pharmacy, Psychiatry, Hospital.

    Returns up to 10 clinics with name, address, suburb, postcode, type, billing.
    Phone numbers and coordinates are not in the dataset. Coverage: Queensland only.
    """
    if not postcode and not suburb:
        return [{"error": "Provide postcode or suburb."}]
    if clinic_type and clinic_type not in ALLOWED_CLINIC_TYPES:
        return [{"error": f"clinic_type must be one of {sorted(ALLOWED_CLINIC_TYPES)}"}]
    with dbmod.get_conn() as conn:
        rows = queries.search_clinics(conn, postcode, suburb, clinic_type)
    if not rows:
        return [{"error": "No clinics found.", "postcode": postcode, "suburb": suburb,
                 "clinic_type": clinic_type}]
    return [
        {k: v for k, v in r.items() if k not in _DROP_FIELDS and v is not None}
        for r in rows
    ]

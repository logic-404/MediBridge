from __future__ import annotations

from fastapi import APIRouter, HTTPException

from medibridge.api.schemas import CoverageRequest
from medibridge.tools.coverage_calculator import calculate_oshc_coverage

router = APIRouter()


@router.post("/coverage")
def post_coverage(req: CoverageRequest) -> dict:
    try:
        return calculate_oshc_coverage.invoke(
            {"item_num": req.item_num, "setting": req.setting}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

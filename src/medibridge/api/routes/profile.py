from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from medibridge.api.schemas import ProfileSavePayload
from medibridge.profile import clear_profile, load_profile, save_profile

router = APIRouter()


@router.get("/profile")
def get_profile() -> dict:
    p = load_profile()
    if p is None:
        raise HTTPException(status_code=404, detail="No profile")
    return p


@router.put("/profile")
def put_profile(payload: ProfileSavePayload) -> dict:
    try:
        return save_profile(payload.tier_id, payload.cover_type, payload.policy_start_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/profile", status_code=204)
def delete_profile() -> Response:
    clear_profile()
    return Response(status_code=204)

"""HTTP request/response models."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ProfileSavePayload(BaseModel):
    tier_id: str
    cover_type: Literal["single", "couple", "family", "sole_parent"]
    policy_start_date: str = Field(..., description="YYYY-MM-DD")


class CoverageRequest(BaseModel):
    item_num: str
    setting: Literal["in_hospital", "out_of_hospital"]


class ChatRequest(BaseModel):
    message: str
    history: list[dict] | None = None

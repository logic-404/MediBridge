"""Coverage result model."""
from __future__ import annotations

from pydantic import BaseModel


class CoverageResult(BaseModel):
    item_num: str
    description: str
    setting: str  # in_hospital | out_of_hospital
    provider_type: str | None  # gp | specialist | None
    schedule_fee: float | None
    oshc_benefit: float
    estimated_out_of_pocket: float
    is_covered: bool
    benefit_pct: float
    waiting_period_months: int | None = None
    waiting_remaining_months: int | None = None
    notes: list[str] = []

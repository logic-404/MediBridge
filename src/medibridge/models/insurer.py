"""Insurer / tier / user profile models."""
from __future__ import annotations

from pydantic import BaseModel


class Insurer(BaseModel):
    insurer_id: str
    insurer_name: str
    phone: str | None = None
    website: str | None = None


class InsurerTier(BaseModel):
    tier_id: str
    insurer_id: str
    tier_name: str
    gp_benefit_pct: float
    specialist_benefit_pct: float
    in_hospital_benefit_pct: float = 100.0
    private_uncontracted_pct: float | None = None
    pharma_max_per_item: float | None = None
    pharma_annual_single: float | None = None
    pharma_annual_family: float | None = None
    pharma_copayment_type: str | None = None
    pharma_copayment_amount: float | None = None
    has_repatriation: int = 0
    repatriation_limit: float | None = None
    has_mental_health_extras: int = 0
    mental_health_annual: float | None = None
    has_boarder_fee: int = 0
    boarder_fee_limit: float | None = None
    has_extras_addon: int = 0
    has_online_doctor: int = 0
    ed_facility_fee_limit: float | None = None
    waived_psychiatric_waiting: int = 0


class UserProfile(BaseModel):
    tier_id: str
    cover_type: str  # single | couple | family | sole_parent
    policy_start_date: str  # YYYY-MM-DD

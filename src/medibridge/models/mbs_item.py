"""Pydantic models for MBS items + IMAP mappings."""
from __future__ import annotations

from pydantic import BaseModel


class MBSItem(BaseModel):
    item_num: str
    sub_item_num: str | None = None
    description: str
    schedule_fee: float | None = None
    benefit_100: float | None = None
    benefit_75: float | None = None
    benefit_85: float | None = None
    benefit_type: str | None = None
    item_type: str | None = None
    fee_type: str | None = None
    provider_type: str | None = None
    category: str
    group_code: str
    sub_group: str | None = None
    sub_heading: str | None = None
    basic_units: float | None = None
    derived_fee_formula: str | None = None
    fee_start_date: str | None = None
    item_start_date: str | None = None
    item_end_date: str | None = None  # NULL when active (sentinel "31/12/9999" normalized)
    emsn_max_cap: float | None = None
    emsn_pct_cap: float | None = None
    description_start_date: str | None = None


class IMAPMapping(BaseModel):
    item_num: str
    mapped_item: str
    item_start_date: str | None = None
    item_end_date: str | None = None
    item_reuse_flag: str | None = None
    mapped_item_desc: str | None = None
    category_code: str | None = None
    group_code: str | None = None
    subgroup_code: str | None = None
    subheading_code: str | None = None
    category_desc: str | None = None
    group_desc: str | None = None
    subgroup_desc: str | None = None
    subheading_desc: str | None = None
    btos_code: str | None = None
    btos_desc: str | None = None

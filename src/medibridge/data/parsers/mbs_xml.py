"""Parse MBS XML -> list[MBSItem]. Active items only."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterator

from medibridge.models.mbs_item import MBSItem


def _txt(elem: ET.Element, tag: str) -> str | None:
    node = elem.find(tag)
    if node is None or node.text is None:
        return None
    val = node.text.strip()
    return val or None


def _flt(elem: ET.Element, tag: str) -> float | None:
    val = _txt(elem, tag)
    if val is None:
        return None
    try:
        return float(val)
    except ValueError:
        return None


def _norm_end_date(val: str | None) -> str | None:
    """Sentinel '31/12/9999' or empty -> NULL."""
    if val is None:
        return None
    if val in ("31/12/9999", "31.12.9999", ""):
        return None
    return val


def parse_mbs_xml(path: Path, include_expired: bool = False) -> Iterator[MBSItem]:
    """Stream MBSItems from XML file."""
    for _, elem in ET.iterparse(str(path), events=("end",)):
        if elem.tag != "Data":
            continue
        end_date = _norm_end_date(_txt(elem, "ItemEndDate"))
        if end_date is not None and not include_expired:
            elem.clear()
            continue
        item_num = _txt(elem, "ItemNum")
        category = _txt(elem, "Category")
        group_code = _txt(elem, "Group")
        if not item_num or not category or not group_code:
            elem.clear()
            continue
        yield MBSItem(
            item_num=item_num,
            sub_item_num=_txt(elem, "SubItemNum"),
            description=_txt(elem, "Description") or "",
            schedule_fee=_flt(elem, "ScheduleFee"),
            benefit_100=_flt(elem, "Benefit100"),
            benefit_75=_flt(elem, "Benefit75"),
            benefit_85=_flt(elem, "Benefit85"),
            benefit_type=_txt(elem, "BenefitType"),
            item_type=_txt(elem, "ItemType"),
            fee_type=_txt(elem, "FeeType"),
            provider_type=_txt(elem, "ProviderType"),
            category=category,
            group_code=group_code,
            sub_group=_txt(elem, "SubGroup"),
            sub_heading=_txt(elem, "SubHeading"),
            basic_units=_flt(elem, "BasicUnits"),
            derived_fee_formula=_txt(elem, "DerivedFee"),
            fee_start_date=_txt(elem, "FeeStartDate"),
            item_start_date=_txt(elem, "ItemStartDate"),
            item_end_date=end_date,
            emsn_max_cap=_flt(elem, "EMSNMaximumCap"),
            emsn_pct_cap=_flt(elem, "EMSNPercentageCap"),
            description_start_date=_txt(elem, "DescriptionStartDate"),
        )
        elem.clear()

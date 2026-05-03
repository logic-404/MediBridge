"""Parse IMAP TSV -> list[IMAPMapping]."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator

from medibridge.models.mbs_item import IMAPMapping


def _strip_leading_zeros(val: str | None) -> str | None:
    if val is None:
        return None
    val = val.strip()
    if not val:
        return None
    stripped = val.lstrip("0")
    return stripped or "0"


def _norm_end_date(val: str | None) -> str | None:
    if val is None:
        return None
    val = val.strip()
    if val in ("31/12/9999", ""):
        return None
    return val


def _txt(val: str | None) -> str | None:
    if val is None:
        return None
    val = val.strip()
    return val or None


def parse_imap(path: Path) -> Iterator[IMAPMapping]:
    with open(path, "r", encoding="cp1252", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            item_num = _strip_leading_zeros(row.get("ITEM"))
            mapped_item = _strip_leading_zeros(row.get("MAPPED_ITEM"))
            if not item_num or not mapped_item:
                continue
            yield IMAPMapping(
                item_num=item_num,
                mapped_item=mapped_item,
                item_start_date=_txt(row.get("Item_Start_Date")),
                item_end_date=_norm_end_date(row.get("Item_End_Date")),
                item_reuse_flag=_txt(row.get("Item_reuse_flag")),
                mapped_item_desc=_txt(row.get("Mapped_Item_Desc")),
                category_code=_txt(row.get("Mapped_Item_Category")),
                group_code=_txt(row.get("Mapped_Item_Group")),
                subgroup_code=_txt(row.get("Mapped_Item_Subgroup")),
                subheading_code=_txt(row.get("Mapped_Item_Subheading")),
                category_desc=_txt(row.get("CATEGORY_DESC")),
                group_desc=_txt(row.get("GROUP_DESC")),
                subgroup_desc=_txt(row.get("SUBGROUP_DESC")),
                subheading_desc=_txt(row.get("SUBHEADING_DESC")),
                btos_code=_txt(row.get("BTOS")),
                btos_desc=_txt(row.get("BTOS_DESC")),
            )

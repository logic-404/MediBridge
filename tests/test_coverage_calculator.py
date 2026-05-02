"""Coverage calculator golden-case tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from medibridge.data import db as dbmod
from medibridge.data.seed_insurers import seed_all
from medibridge.models.mbs_item import IMAPMapping, MBSItem
from medibridge.tools.coverage_calculator import _calculate


@pytest.fixture()
def conn(tmp_path: Path):
    db_path = tmp_path / "test.db"
    c = dbmod.connect(db_path)
    dbmod.init_schema(c)
    items = [
        MBSItem(item_num="23", description="GP Level B",
                schedule_fee=43.90, benefit_100=43.90, benefit_type="E",
                category="1", group_code="A1"),
        MBSItem(item_num="104", description="Specialist initial",
                schedule_fee=101.35, benefit_85=86.15, benefit_75=76.05,
                benefit_type="C", category="1", group_code="A4"),
    ]
    dbmod.insert_mbs_items(c, items)
    dbmod.insert_imap_mappings(c, [
        IMAPMapping(item_num="23", mapped_item="23"),
        IMAPMapping(item_num="104", mapped_item="104"),
    ])
    dbmod.populate_fts(c)
    seed_all(c)
    c.commit()
    yield c
    c.close()


def _set_profile(conn, tier_id: str) -> None:
    conn.execute("DELETE FROM user_profile")
    conn.execute(
        "INSERT INTO user_profile (id, tier_id, cover_type, policy_start_date) VALUES (1, ?, 'single', '2025-01-01')",
        (tier_id,),
    )
    conn.commit()


def test_allianz_essentials_gp_100pct(conn) -> None:
    _set_profile(conn, "allianz_essentials")
    res = _calculate("23", "out_of_hospital", conn)
    assert res.benefit_pct == 100
    assert res.oshc_benefit == 43.90
    assert res.estimated_out_of_pocket == 0.0
    assert res.provider_type == "gp"


def test_allianz_essentials_specialist_85pct(conn) -> None:
    _set_profile(conn, "allianz_essentials")
    res = _calculate("104", "out_of_hospital", conn)
    assert res.benefit_pct == 85
    assert res.oshc_benefit == 86.15
    assert round(res.estimated_out_of_pocket, 2) == 15.20
    assert res.provider_type == "specialist"


def test_cbhs_standard_specialist_100pct(conn) -> None:
    _set_profile(conn, "cbhs_standard")
    res = _calculate("104", "out_of_hospital", conn)
    assert res.benefit_pct == 100
    assert round(res.oshc_benefit, 2) == 101.35
    assert res.estimated_out_of_pocket == 0.0


def test_in_hospital_100pct(conn) -> None:
    _set_profile(conn, "allianz_essentials")
    res = _calculate("104", "in_hospital", conn)
    assert res.benefit_pct == 100
    assert res.oshc_benefit == 101.35
    assert res.estimated_out_of_pocket == 0.0


def test_no_imap_mapping_excluded(conn) -> None:
    """Item with no IMAP mapping (non-MBS program) is excluded by deed eligibility gate."""
    # Insert item with NO matching IMAP row — simulates CDBS dental (cat 10, group U)
    conn.execute("INSERT OR REPLACE INTO mbs_items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        ("88586", None, "Crown-metallic with tooth preparation", 297.75, 297.75, None, None,
         "E", "S", "N", None, "10", "U5", None, None, None, None, None, None, None, None, None, None))
    conn.commit()
    # No IMAP row inserted for 88586 — IMAP gate fires
    _set_profile(conn, "allianz_essentials")
    for setting in ("out_of_hospital", "in_hospital"):
        res = _calculate("88586", setting, conn)
        assert res.is_covered is False, f"Expected IMAP gate to exclude for {setting}"
        assert res.oshc_benefit == 0.0
        assert res.estimated_out_of_pocket == 297.75
        assert "IMAP" in res.notes[0] or "standard MBS" in res.notes[0].lower()


def test_imap_mapped_item_not_excluded_by_imap_gate(conn) -> None:
    """Category 4 oral/maxillofacial item with IMAP mapping IS covered in-hospital."""
    from medibridge.models.mbs_item import IMAPMapping
    conn.execute("INSERT OR REPLACE INTO mbs_items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        ("51300", None, "Surgical extraction complex", 180.0, 180.0, None, 153.0,
         "C", "S", "N", None, "4", "D1", None, None, None, None, None, None, None, None, None, None))
    # IMAP row present → passes deed eligibility gate
    conn.execute(
        "INSERT INTO imap_mappings (item_num, mapped_item, category_desc, group_desc, btos_desc) VALUES (?,?,?,?,?)",
        ("51300", "51300", "ORAL AND MAXILLOFACIAL SERVICES", "DENTAL SURGERY", "Operations"),
    )
    conn.commit()
    _set_profile(conn, "allianz_essentials")
    res = _calculate("51300", "in_hospital", conn)
    assert res.is_covered is True
    assert res.oshc_benefit == 180.0

"""DB schema + FTS5 + lookup tests against an isolated SQLite DB."""
from __future__ import annotations

from pathlib import Path

import pytest

from medibridge.data import db as dbmod
from medibridge.models.mbs_item import IMAPMapping, MBSItem


@pytest.fixture()
def conn(tmp_path: Path):
    db_path = tmp_path / "test.db"
    c = dbmod.connect(db_path)
    dbmod.init_schema(c)
    yield c
    c.close()


def _seed(conn) -> None:
    items = [
        MBSItem(item_num="23", description="GP Level B attendance",
                schedule_fee=43.90, benefit_100=43.90, benefit_type="E",
                category="1", group_code="A1"),
        MBSItem(item_num="104", description="Specialist initial consultation",
                schedule_fee=101.35, benefit_85=86.15, benefit_75=76.05,
                benefit_type="C", category="1", group_code="A4"),
        MBSItem(item_num="73807", description="Blood test full count",
                schedule_fee=16.95, benefit_85=14.45, benefit_75=12.75,
                benefit_type="C", category="6", group_code="P1"),
    ]
    dbmod.insert_mbs_items(conn, items)
    mappings = [
        IMAPMapping(item_num="23", mapped_item="23", category_desc="PROFESSIONAL ATTENDANCES",
                    group_desc="GENERAL PRACTITIONER ATTENDANCES", btos_desc="Non-referred attendances GP/VR GP"),
        IMAPMapping(item_num="104", mapped_item="104", category_desc="PROFESSIONAL ATTENDANCES",
                    group_desc="CONSULTANT PHYSICIAN", btos_desc="Specialist attendances"),
        IMAPMapping(item_num="73807", mapped_item="73807", category_code="06",
                    group_code="P1", btos_code="0601",
                    category_desc="PATHOLOGY SERVICES",
                    group_desc="HAEMATOLOGY", btos_desc="Pathology Tests"),
    ]
    dbmod.insert_imap_mappings(conn, mappings)
    dbmod.populate_lookup_tables(conn)
    dbmod.populate_fts(conn)


def test_get_item_by_number(conn) -> None:
    _seed(conn)
    item = dbmod.get_item_by_number(conn, "23")
    assert item is not None
    assert item["schedule_fee"] == 43.90
    assert item["benefit_type"] == "E"
    assert item["group_desc"] == "GENERAL PRACTITIONER ATTENDANCES"


def test_fts5_blood_test(conn) -> None:
    _seed(conn)
    rows = dbmod.search_items_by_keyword(conn, "blood test", limit=5)
    assert any(r["item_num"] == "73807" for r in rows)


def test_fts5_populated(conn) -> None:
    _seed(conn)
    assert dbmod.fts_count(conn) == 3


def test_lookup_tables_built(conn) -> None:
    _seed(conn)
    cat = conn.execute("SELECT * FROM categories").fetchall()
    assert any(r["category_desc"] == "PATHOLOGY SERVICES" for r in cat)

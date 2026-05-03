"""Clinic search query helper + tool wrapper tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from medibridge.data import db as dbmod
from medibridge.data import queries


CLINIC_ROWS = [
    # id, name, address, suburb, state, postcode, phone, hours, billing, type, lat, lon, nhsd_id
    (1, "Queen St Medical", "141 Queen St", "BRISBANE CITY", "QLD", "4000",
     None, None, "mixed", "GP, Pharmacy", None, None, "n1"),
    (2, "Brisbane Psychology", "10 Adelaide St", "BRISBANE CITY", "QLD", "4000",
     None, None, "private", "Psychology", None, None, "n2"),
    (3, "Brisbane Psychiatry Clinic", "20 George St", "BRISBANE CITY", "QLD", "4000",
     None, None, "private", "Psychiatry", None, None, "n3"),
    (4, "Royal Brisbane Hospital", "Bowen Bridge Rd", "HERSTON", "QLD", "4029",
     None, None, "public", "Hospital", None, None, "n4"),
    (5, "South Bank Pharmacy", "5 Grey St", "SOUTH BRISBANE", "QLD", "4101",
     None, None, "private", "Pharmacy", None, None, "n5"),
]


@pytest.fixture()
def conn(tmp_path: Path):
    db_path = tmp_path / "test.db"
    c = dbmod.connect(db_path)
    dbmod.init_schema(c)
    c.executemany(
        """INSERT INTO clinics (id, name, address, suburb, state, postcode,
            phone, hours, billing, type, latitude, longitude, nhsd_id)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        CLINIC_ROWS,
    )
    c.commit()
    yield c
    c.close()


def test_postcode_exact_match(conn) -> None:
    rows = queries.search_clinics(conn, postcode="4000")
    assert len(rows) == 3
    assert {r["id"] for r in rows} == {1, 2, 3}


def test_suburb_case_insensitive(conn) -> None:
    rows = queries.search_clinics(conn, suburb="Brisbane City")
    assert len(rows) == 3
    rows2 = queries.search_clinics(conn, suburb="south brisbane")
    assert len(rows2) == 1 and rows2[0]["id"] == 5


def test_type_filter_does_not_confuse_psychology_psychiatry(conn) -> None:
    psych_only = queries.search_clinics(conn, postcode="4000", clinic_type="Psychiatry")
    assert [r["id"] for r in psych_only] == [3]
    psyc_only = queries.search_clinics(conn, postcode="4000", clinic_type="Psychology")
    assert [r["id"] for r in psyc_only] == [2]


def test_type_filter_matches_multivalue_column(conn) -> None:
    """Row 1 has 'GP, Pharmacy' — both atoms should match."""
    gp = queries.search_clinics(conn, postcode="4000", clinic_type="GP")
    assert [r["id"] for r in gp] == [1]
    pharma = queries.search_clinics(conn, postcode="4000", clinic_type="Pharmacy")
    assert [r["id"] for r in pharma] == [1]


def test_unknown_postcode_empty(conn) -> None:
    rows = queries.search_clinics(conn, postcode="9999")
    assert rows == []


def test_no_filters_empty(conn) -> None:
    assert queries.search_clinics(conn) == []


def test_tool_wrapper_strips_null_fields(tmp_path: Path) -> None:
    """The @tool wrapper drops always-NULL columns from output."""
    db_path = tmp_path / "test.db"
    c = dbmod.connect(db_path)
    dbmod.init_schema(c)
    c.executemany(
        """INSERT INTO clinics (id, name, address, suburb, state, postcode,
            phone, hours, billing, type, latitude, longitude, nhsd_id)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        CLINIC_ROWS,
    )
    c.commit()
    c.close()

    from medibridge.tools.clinic_search import search_clinics

    with patch("medibridge.tools.clinic_search.dbmod.get_conn") as mock_conn:
        mock_conn.return_value.__enter__.return_value = dbmod.connect(db_path)
        mock_conn.return_value.__exit__.return_value = False
        result = search_clinics.invoke({"postcode": "4000", "clinic_type": "Psychology"})
    assert len(result) == 1
    assert "phone" not in result[0]
    assert "latitude" not in result[0]
    assert result[0]["name"] == "Brisbane Psychology"


def test_tool_wrapper_invalid_type() -> None:
    from medibridge.tools.clinic_search import search_clinics

    result = search_clinics.invoke({"postcode": "4000", "clinic_type": "Dentist"})
    assert "error" in result[0]


def test_tool_wrapper_no_args() -> None:
    from medibridge.tools.clinic_search import search_clinics

    result = search_clinics.invoke({})
    assert "error" in result[0]

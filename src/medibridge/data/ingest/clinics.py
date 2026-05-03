"""Read-only seed copy: data/sources/clinics_qld.db → medibridge.db.clinics."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from medibridge.config import CLINICS_SOURCE_PATH


def ingest_clinics(conn: sqlite3.Connection, source_path: Path = CLINICS_SOURCE_PATH) -> int:
    if not source_path.exists():
        raise FileNotFoundError(f"Clinics source DB missing: {source_path}")
    src = sqlite3.connect(str(source_path))
    src.row_factory = sqlite3.Row
    rows = src.execute("SELECT * FROM clinics").fetchall()
    src.close()

    conn.execute("DELETE FROM clinics")
    cur = conn.executemany(
        """INSERT INTO clinics (id, name, address, suburb, state, postcode,
            phone, hours, billing, type, latitude, longitude, nhsd_id)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                int(r["id"]) if r["id"] is not None else None,
                r["name"], r["address"], r["suburb"], r["state"], r["postcode"],
                r["phone"], r["hours"], r["billing"], r["type"],
                float(r["latitude"]) if r["latitude"] not in (None, "") else None,
                float(r["longitude"]) if r["longitude"] not in (None, "") else None,
                r["nhsd_id"],
            )
            for r in rows
        ],
    )
    return cur.rowcount

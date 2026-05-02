"""SQLite schema + ops + FTS5."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from medibridge.config import DB_PATH
from medibridge.models.mbs_item import IMAPMapping, MBSItem

SCHEMA = """
CREATE TABLE IF NOT EXISTS mbs_items (
    item_num TEXT PRIMARY KEY,
    sub_item_num TEXT,
    description TEXT NOT NULL,
    schedule_fee REAL,
    benefit_100 REAL,
    benefit_75 REAL,
    benefit_85 REAL,
    benefit_type TEXT,
    item_type TEXT,
    fee_type TEXT,
    provider_type TEXT,
    category TEXT NOT NULL,
    group_code TEXT NOT NULL,
    sub_group TEXT,
    sub_heading TEXT,
    basic_units REAL,
    derived_fee_formula TEXT,
    fee_start_date TEXT,
    item_start_date TEXT,
    item_end_date TEXT,
    emsn_max_cap REAL,
    emsn_pct_cap REAL,
    description_start_date TEXT
);

CREATE TABLE IF NOT EXISTS imap_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_num TEXT NOT NULL,
    mapped_item TEXT NOT NULL,
    item_start_date TEXT,
    item_end_date TEXT,
    item_reuse_flag TEXT,
    mapped_item_desc TEXT,
    category_code TEXT,
    group_code TEXT,
    subgroup_code TEXT,
    subheading_code TEXT,
    category_desc TEXT,
    group_desc TEXT,
    subgroup_desc TEXT,
    subheading_desc TEXT,
    btos_code TEXT,
    btos_desc TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    category_code TEXT PRIMARY KEY,
    category_desc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS groups (
    group_code TEXT PRIMARY KEY,
    group_desc TEXT NOT NULL,
    category_code TEXT
);

CREATE TABLE IF NOT EXISTS btos_types (
    btos_code TEXT PRIMARY KEY,
    btos_desc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS oshc_coverage_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_type TEXT NOT NULL,
    setting TEXT,
    provider_type TEXT,
    benefit_pct REAL,
    category_code TEXT,
    btos_code TEXT,
    waiting_months INTEGER,
    description TEXT NOT NULL,
    deed_reference TEXT
);

CREATE TABLE IF NOT EXISTS insurers (
    insurer_id TEXT PRIMARY KEY,
    insurer_name TEXT NOT NULL,
    phone TEXT,
    website TEXT
);

CREATE TABLE IF NOT EXISTS insurer_tiers (
    tier_id TEXT PRIMARY KEY,
    insurer_id TEXT NOT NULL,
    tier_name TEXT NOT NULL,
    gp_benefit_pct REAL NOT NULL,
    specialist_benefit_pct REAL NOT NULL,
    in_hospital_benefit_pct REAL NOT NULL DEFAULT 100,
    private_uncontracted_pct REAL,
    pharma_max_per_item REAL,
    pharma_annual_single REAL,
    pharma_annual_family REAL,
    pharma_copayment_type TEXT,
    pharma_copayment_amount REAL,
    has_repatriation INTEGER DEFAULT 0,
    repatriation_limit REAL,
    has_mental_health_extras INTEGER DEFAULT 0,
    mental_health_annual REAL,
    has_boarder_fee INTEGER DEFAULT 0,
    boarder_fee_limit REAL,
    has_extras_addon INTEGER DEFAULT 0,
    has_online_doctor INTEGER DEFAULT 0,
    ed_facility_fee_limit REAL,
    waived_psychiatric_waiting INTEGER DEFAULT 0,
    FOREIGN KEY (insurer_id) REFERENCES insurers(insurer_id)
);

CREATE TABLE IF NOT EXISTS insurer_exclusions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_id TEXT NOT NULL,
    exclusion_desc TEXT NOT NULL,
    is_deed_exclusion INTEGER DEFAULT 0,
    FOREIGN KEY (tier_id) REFERENCES insurer_tiers(tier_id)
);

CREATE TABLE IF NOT EXISTS insurer_waiting_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_id TEXT NOT NULL,
    condition_type TEXT NOT NULL,
    waiting_months INTEGER NOT NULL,
    notes TEXT,
    FOREIGN KEY (tier_id) REFERENCES insurer_tiers(tier_id)
);

CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY DEFAULT 1,
    tier_id TEXT NOT NULL,
    cover_type TEXT NOT NULL,
    policy_start_date TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (tier_id) REFERENCES insurer_tiers(tier_id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS mbs_fts USING fts5(
    item_num UNINDEXED,
    description,
    category_desc,
    group_desc,
    subgroup_desc,
    btos_desc,
    tokenize = 'porter unicode61'
);

CREATE INDEX IF NOT EXISTS idx_mbs_category ON mbs_items(category);
CREATE INDEX IF NOT EXISTS idx_mbs_group ON mbs_items(group_code);
CREATE INDEX IF NOT EXISTS idx_mbs_benefit_type ON mbs_items(benefit_type);
CREATE INDEX IF NOT EXISTS idx_mbs_active ON mbs_items(item_end_date) WHERE item_end_date IS NULL;
CREATE INDEX IF NOT EXISTS idx_imap_mapped ON imap_mappings(mapped_item);
CREATE INDEX IF NOT EXISTS idx_imap_btos ON imap_mappings(btos_code);
CREATE INDEX IF NOT EXISTS idx_coverage_type ON oshc_coverage_rules(rule_type);
"""


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_conn(db_path: Path = DB_PATH) -> Iterator[sqlite3.Connection]:
    conn = connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def reset_db(db_path: Path = DB_PATH) -> None:
    if db_path.exists():
        db_path.unlink()


def insert_mbs_items(conn: sqlite3.Connection, items: Iterable[MBSItem]) -> int:
    cur = conn.cursor()
    rows = (
        (
            it.item_num, it.sub_item_num, it.description, it.schedule_fee,
            it.benefit_100, it.benefit_75, it.benefit_85, it.benefit_type,
            it.item_type, it.fee_type, it.provider_type, it.category,
            it.group_code, it.sub_group, it.sub_heading, it.basic_units,
            it.derived_fee_formula, it.fee_start_date, it.item_start_date,
            it.item_end_date, it.emsn_max_cap, it.emsn_pct_cap,
            it.description_start_date,
        )
        for it in items
    )
    cur.executemany(
        """INSERT OR REPLACE INTO mbs_items VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        rows,
    )
    return cur.rowcount


def insert_imap_mappings(conn: sqlite3.Connection, mappings: Iterable[IMAPMapping]) -> int:
    cur = conn.cursor()
    rows = (
        (
            m.item_num, m.mapped_item, m.item_start_date, m.item_end_date,
            m.item_reuse_flag, m.mapped_item_desc, m.category_code, m.group_code,
            m.subgroup_code, m.subheading_code, m.category_desc, m.group_desc,
            m.subgroup_desc, m.subheading_desc, m.btos_code, m.btos_desc,
        )
        for m in mappings
    )
    cur.executemany(
        """INSERT INTO imap_mappings (
            item_num, mapped_item, item_start_date, item_end_date,
            item_reuse_flag, mapped_item_desc, category_code, group_code,
            subgroup_code, subheading_code, category_desc, group_desc,
            subgroup_desc, subheading_desc, btos_code, btos_desc
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        rows,
    )
    return cur.rowcount


def populate_lookup_tables(conn: sqlite3.Connection) -> None:
    """Build categories / groups / btos_types from imap_mappings."""
    conn.execute(
        """INSERT OR IGNORE INTO categories (category_code, category_desc)
        SELECT DISTINCT category_code, category_desc FROM imap_mappings
        WHERE category_code IS NOT NULL AND category_desc IS NOT NULL"""
    )
    conn.execute(
        """INSERT OR IGNORE INTO groups (group_code, group_desc, category_code)
        SELECT DISTINCT group_code, group_desc, category_code FROM imap_mappings
        WHERE group_code IS NOT NULL AND group_desc IS NOT NULL"""
    )
    conn.execute(
        """INSERT OR IGNORE INTO btos_types (btos_code, btos_desc)
        SELECT DISTINCT btos_code, btos_desc FROM imap_mappings
        WHERE btos_code IS NOT NULL AND btos_desc IS NOT NULL"""
    )


def populate_fts(conn: sqlite3.Connection) -> int:
    conn.execute("DELETE FROM mbs_fts")
    cur = conn.execute(
        """INSERT INTO mbs_fts (item_num, description, category_desc, group_desc, subgroup_desc, btos_desc)
        SELECT m.item_num, m.description,
               COALESCE(i.category_desc, ''), COALESCE(i.group_desc, ''),
               COALESCE(i.subgroup_desc, ''), COALESCE(i.btos_desc, '')
        FROM mbs_items m
        LEFT JOIN (
            SELECT mapped_item,
                   MAX(category_desc) AS category_desc,
                   MAX(group_desc) AS group_desc,
                   MAX(subgroup_desc) AS subgroup_desc,
                   MAX(btos_desc) AS btos_desc
            FROM imap_mappings
            WHERE item_end_date IS NULL
            GROUP BY mapped_item
        ) i ON m.item_num = i.mapped_item
        WHERE m.item_end_date IS NULL"""
    )
    return cur.rowcount


# -------- Hardcoded deed rules --------

DEED_RULES = [
    ("benefit_rate", "out_of_hospital", None, 85.0, None, None, None,
     "Out-of-hospital medical: 85% of MBS schedule fee", "Schedule 1c"),
    ("benefit_rate", "in_hospital", None, 100.0, None, None, None,
     "In-hospital medical: 100% of MBS schedule fee", "Schedule 1d"),
    ("benefit_rate", "public_hospital", None, 100.0, None, None, None,
     "Public hospital: 100% of charges", "Schedule 1f"),
    ("benefit_rate", "ambulance", None, 100.0, None, None, None,
     "Ambulance: 100% of charge when medically necessary", "Schedule 1a"),
    ("waiting_period", None, None, None, None, None, 0,
     "Nil waiting: out-of-hospital MBS groups A1, A2, A7(2,10), A22, A23, A40(1,2), A46", "Schedule 4"),
    ("waiting_period", None, None, None, None, None, 0,
     "Nil waiting: emergency treatment", "Schedule 4"),
    ("waiting_period", None, "psychiatric", None, None, None, 2,
     "2 months: psychiatric hospital treatment (non-emergency)", "Schedule 4"),
    ("waiting_period", None, "pre_existing", None, None, None, 12,
     "12 months: pre-existing condition hospital treatment", "Schedule 4"),
    ("waiting_period", None, "pregnancy", None, None, None, 12,
     "12 months: pregnancy (OSHC < 2 years)", "Schedule 4"),
    ("waiting_period", None, "general", None, None, None, 2,
     "2 months: all other Schedule 1 services", "Schedule 4"),
    ("exclusion", None, None, None, None, None, None,
     "Treatment outside Australia (unless medical repatriation)", "Schedule 3"),
    ("exclusion", None, None, None, None, None, None,
     "Compensable injury/illness (workers comp, motor vehicle)", "Schedule 3"),
    ("exclusion", None, None, None, None, None, None,
     "Treatment that is not medically necessary", "Schedule 3"),
    ("limit", None, "pharmaceutical", None, None, None, None,
     "Pharmaceutical: PBS co-payment excess, up to $50/item, min $500/yr single $1000/yr family", "Schedule 1b"),
]


def insert_deed_rules(conn: sqlite3.Connection) -> int:
    cur = conn.executemany(
        """INSERT INTO oshc_coverage_rules
        (rule_type, setting, provider_type, benefit_pct, category_code, btos_code,
         waiting_months, description, deed_reference)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        DEED_RULES,
    )
    return cur.rowcount


# -------- Query helpers --------

def get_item_by_number(conn: sqlite3.Connection, item_num: str) -> dict | None:
    row = conn.execute(
        """SELECT m.*,
               (SELECT category_desc FROM imap_mappings WHERE mapped_item = m.item_num
                AND category_desc IS NOT NULL LIMIT 1) AS category_desc,
               (SELECT group_desc FROM imap_mappings WHERE mapped_item = m.item_num
                AND group_desc IS NOT NULL LIMIT 1) AS group_desc,
               (SELECT btos_desc FROM imap_mappings WHERE mapped_item = m.item_num
                AND btos_desc IS NOT NULL LIMIT 1) AS btos_desc
        FROM mbs_items m WHERE m.item_num = ? AND m.item_end_date IS NULL""",
        (item_num.lstrip("0") or "0",),
    ).fetchone()
    return dict(row) if row else None


def search_items_by_keyword(conn: sqlite3.Connection, query: str, limit: int = 10) -> list[dict]:
    # FTS5 MATCH; sanitize quotes
    safe = query.replace('"', '""')
    try:
        rows = conn.execute(
            f"""SELECT item_num, description, rank FROM mbs_fts
            WHERE mbs_fts MATCH ? ORDER BY rank LIMIT ?""",
            (safe, limit),
        ).fetchall()
    except sqlite3.OperationalError:
        # fallback: quote phrase
        rows = conn.execute(
            f"""SELECT item_num, description, rank FROM mbs_fts
            WHERE mbs_fts MATCH ? ORDER BY rank LIMIT ?""",
            (f'"{safe}"', limit),
        ).fetchall()
    return [dict(r) for r in rows]


def get_items_by_category(conn: sqlite3.Connection, category: str) -> list[dict]:
    rows = conn.execute(
        "SELECT item_num, description, schedule_fee FROM mbs_items "
        "WHERE category = ? AND item_end_date IS NULL",
        (category,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_items_by_btos(conn: sqlite3.Connection, btos_desc: str) -> list[dict]:
    rows = conn.execute(
        """SELECT DISTINCT m.item_num, m.description, m.schedule_fee
        FROM mbs_items m
        JOIN imap_mappings i ON m.item_num = i.mapped_item
        WHERE i.btos_desc = ? AND m.item_end_date IS NULL""",
        (btos_desc,),
    ).fetchall()
    return [dict(r) for r in rows]


def fts_count(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT COUNT(*) FROM mbs_fts").fetchone()[0]

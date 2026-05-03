"""MBS XML + IMAP TSV → mbs_items, imap_mappings, lookup tables, FTS5."""
from __future__ import annotations

import sqlite3
from typing import Iterable

from medibridge.models.mbs_item import IMAPMapping, MBSItem


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

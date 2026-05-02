"""Ingestion orchestrator.

Run: python -m medibridge.data.ingest
"""
from __future__ import annotations

import argparse

from rich.console import Console

from medibridge.config import (
    CHROMA_MBS_COLLECTION,
    CHROMA_RULES_COLLECTION,
    DB_PATH,
    DEED_PDF_PATH,
    IMAP_PATH,
    MBS_BOOK_PDF_PATH,
    MBS_ITEM_INFO_PDF_PATH,
    MBS_XML_PATH,
    ensure_data_dir,
    settings,
)
from medibridge.data import db as dbmod
from medibridge.data.parse_imap import parse_imap
from medibridge.data.parse_knowledge_md import parse_knowledge_md
from medibridge.data.parse_mbs_book import parse_mbs_book
from medibridge.data.parse_mbs_item_info import parse_mbs_item_info
from medibridge.data.parse_mbs_xml import parse_mbs_xml
from medibridge.data.parse_oshc_deed import parse_deed
from medibridge.data.seed_insurers import seed_all
from medibridge.data.vectorstore import (
    add_mbs_items,
    add_rule_chunks,
    get_client,
    reset_collection,
)

console = Console()


def ingest_sqlite(reset: bool = True) -> dict:
    if reset:
        dbmod.reset_db(DB_PATH)
    with dbmod.get_conn(DB_PATH) as conn:
        dbmod.init_schema(conn)
        console.print("[cyan]Parsing MBS XML...[/cyan]")
        items = list(parse_mbs_xml(MBS_XML_PATH))
        console.print(f"  {len(items)} active items")
        dbmod.insert_mbs_items(conn, items)

        console.print("[cyan]Parsing IMAP TSV...[/cyan]")
        mappings = list(parse_imap(IMAP_PATH))
        console.print(f"  {len(mappings)} mapping rows")
        dbmod.insert_imap_mappings(conn, mappings)

        console.print("[cyan]Populating lookup tables...[/cyan]")
        dbmod.populate_lookup_tables(conn)

        console.print("[cyan]Populating FTS5...[/cyan]")
        n_fts = dbmod.populate_fts(conn)
        console.print(f"  {n_fts} FTS rows")

        console.print("[cyan]Seeding insurers...[/cyan]")
        seed_all(conn)

        console.print("[cyan]Inserting deed rules...[/cyan]")
        dbmod.insert_deed_rules(conn)

        cat_count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
        grp_count = conn.execute("SELECT COUNT(*) FROM groups").fetchone()[0]
        btos_count = conn.execute("SELECT COUNT(*) FROM btos_types").fetchone()[0]
        return {
            "items": len(items),
            "mappings": len(mappings),
            "fts_rows": n_fts,
            "categories": cat_count,
            "groups": grp_count,
            "btos": btos_count,
        }


def ingest_chroma(reset: bool = True) -> dict:
    if not settings.openai_api_key:
        console.print("[yellow]OPENAI_API_KEY not set; skipping ChromaDB ingest.[/yellow]")
        return {"mbs_chunks": 0, "rule_chunks": 0, "skipped": True}

    client = get_client()

    console.print("[cyan]Building MBS embedding docs from SQLite...[/cyan]")
    with dbmod.get_conn(DB_PATH) as conn:
        rows = conn.execute(
            """SELECT m.item_num, m.description, m.schedule_fee, m.benefit_type,
                       m.benefit_100, m.benefit_85, m.benefit_75, m.category, m.group_code,
                       (SELECT category_desc FROM imap_mappings WHERE mapped_item = m.item_num
                        AND category_desc IS NOT NULL LIMIT 1) AS category_desc,
                       (SELECT group_desc FROM imap_mappings WHERE mapped_item = m.item_num
                        AND group_desc IS NOT NULL LIMIT 1) AS group_desc,
                       (SELECT btos_desc FROM imap_mappings WHERE mapped_item = m.item_num
                        AND btos_desc IS NOT NULL LIMIT 1) AS btos_desc
               FROM mbs_items m WHERE m.item_end_date IS NULL"""
        ).fetchall()
    items = [dict(r) for r in rows]
    mbs_coll = reset_collection(client, CHROMA_MBS_COLLECTION) if reset else \
        get_client().get_or_create_collection(CHROMA_MBS_COLLECTION)
    n_mbs = add_mbs_items(mbs_coll, items)
    console.print(f"  embedded {n_mbs} MBS items")

    console.print("[cyan]Parsing rule docs (deed + book + item-info + knowledge md)...[/cyan]")
    deed_chunks = parse_deed(DEED_PDF_PATH) if DEED_PDF_PATH.exists() else []
    book_chunks = parse_mbs_book(MBS_BOOK_PDF_PATH) if MBS_BOOK_PDF_PATH.exists() else []
    info_chunks = parse_mbs_item_info(MBS_ITEM_INFO_PDF_PATH) if MBS_ITEM_INFO_PDF_PATH.exists() else []
    md_chunks   = parse_knowledge_md()
    console.print(f"  deed={len(deed_chunks)} book={len(book_chunks)} info={len(info_chunks)} md={len(md_chunks)}")

    rules_coll = reset_collection(client, CHROMA_RULES_COLLECTION) if reset else \
        get_client().get_or_create_collection(CHROMA_RULES_COLLECTION)
    total_rules = 0
    total_rules += add_rule_chunks(rules_coll, deed_chunks, "deed")
    total_rules += add_rule_chunks(rules_coll, book_chunks, "book")
    total_rules += add_rule_chunks(rules_coll, info_chunks, "info")
    total_rules += add_rule_chunks(rules_coll, md_chunks, "md")
    console.print(f"  embedded {total_rules} rule chunks")

    return {"mbs_chunks": n_mbs, "rule_chunks": total_rules, "skipped": False}


def main() -> None:
    parser = argparse.ArgumentParser(description="MediBridge ingest")
    parser.add_argument("--skip-chroma", action="store_true", help="SQLite only")
    parser.add_argument("--no-reset", action="store_true", help="Append, don't reset")
    args = parser.parse_args()

    ensure_data_dir()
    sql_stats = ingest_sqlite(reset=not args.no_reset)
    console.print(f"[green]SQLite done:[/green] {sql_stats}")

    if not args.skip_chroma:
        chroma_stats = ingest_chroma(reset=not args.no_reset)
        console.print(f"[green]Chroma done:[/green] {chroma_stats}")

    db_size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    console.print(f"[bold]DB size: {db_size_mb:.1f} MB[/bold]")


if __name__ == "__main__":
    main()

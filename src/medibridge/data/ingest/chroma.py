"""Embed MBS items + rule docs into ChromaDB."""
from __future__ import annotations

from rich.console import Console

from medibridge.config import (
    CHROMA_MBS_COLLECTION,
    CHROMA_RULES_COLLECTION,
    DB_PATH,
    DEED_PDF_PATH,
    MBS_BOOK_PDF_PATH,
    MBS_ITEM_INFO_PDF_PATH,
    settings,
)
from medibridge.data import db as dbmod
from medibridge.data.parsers.knowledge_md import parse_knowledge_md
from medibridge.data.parsers.mbs_book import parse_mbs_book
from medibridge.data.parsers.mbs_item_info import parse_mbs_item_info
from medibridge.data.parsers.oshc_deed import parse_deed
from medibridge.data.vectorstore import (
    add_mbs_items,
    add_rule_chunks,
    get_client,
    reset_collection,
)

console = Console()


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
    md_chunks = parse_knowledge_md()
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

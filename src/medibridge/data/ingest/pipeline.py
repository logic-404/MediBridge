"""Ingestion orchestrator. Run: python -m medibridge.data.ingest"""
from __future__ import annotations

import argparse

from rich.console import Console

from medibridge.config import DB_PATH, IMAP_PATH, MBS_XML_PATH, ensure_data_dir
from medibridge.data import db as dbmod
from medibridge.data.ingest.chroma import ingest_chroma
from medibridge.data.ingest.clinics import ingest_clinics
from medibridge.data.ingest.insurers import seed_all
from medibridge.data.ingest.mbs import (
    insert_imap_mappings,
    insert_mbs_items,
    populate_fts,
    populate_lookup_tables,
)
from medibridge.data.ingest.oshc_rules import insert_deed_rules
from medibridge.data.parsers.imap import parse_imap
from medibridge.data.parsers.mbs_xml import parse_mbs_xml

console = Console()


def ingest_sqlite(reset: bool = True) -> dict:
    if reset:
        dbmod.reset_db(DB_PATH)
    with dbmod.get_conn(DB_PATH) as conn:
        dbmod.init_schema(conn)
        console.print("[cyan]Parsing MBS XML...[/cyan]")
        items = list(parse_mbs_xml(MBS_XML_PATH))
        console.print(f"  {len(items)} active items")
        insert_mbs_items(conn, items)

        console.print("[cyan]Parsing IMAP TSV...[/cyan]")
        mappings = list(parse_imap(IMAP_PATH))
        console.print(f"  {len(mappings)} mapping rows")
        insert_imap_mappings(conn, mappings)

        console.print("[cyan]Populating lookup tables...[/cyan]")
        populate_lookup_tables(conn)

        console.print("[cyan]Populating FTS5...[/cyan]")
        n_fts = populate_fts(conn)
        console.print(f"  {n_fts} FTS rows")

        console.print("[cyan]Seeding insurers...[/cyan]")
        seed_all(conn)

        console.print("[cyan]Inserting deed rules...[/cyan]")
        insert_deed_rules(conn)

        console.print("[cyan]Loading clinics...[/cyan]")
        try:
            n_clinics = ingest_clinics(conn)
            console.print(f"  {n_clinics} clinic rows")
        except FileNotFoundError as e:
            console.print(f"[yellow]Skipping clinics: {e}[/yellow]")
            n_clinics = 0

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
            "clinics": n_clinics,
        }


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

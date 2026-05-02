"""CLI onboarding flow."""
from __future__ import annotations

import json
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from medibridge.config import USER_PROFILE_JSON
from medibridge.data import db as dbmod

console = Console()

COVER_TYPES = ["single", "couple", "family", "sole_parent"]


def _list_insurers(conn) -> list[dict]:
    rows = conn.execute(
        "SELECT insurer_id, insurer_name FROM insurers ORDER BY insurer_name"
    ).fetchall()
    return [dict(r) for r in rows]


def _list_tiers(conn, insurer_id: str) -> list[dict]:
    rows = conn.execute(
        "SELECT tier_id, tier_name FROM insurer_tiers WHERE insurer_id = ? ORDER BY tier_name",
        (insurer_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def _save_profile(tier_id: str, cover_type: str, policy_start: str) -> None:
    with dbmod.get_conn() as conn:
        conn.execute("DELETE FROM user_profile")
        conn.execute(
            "INSERT INTO user_profile (id, tier_id, cover_type, policy_start_date) VALUES (1, ?, ?, ?)",
            (tier_id, cover_type, policy_start),
        )
    USER_PROFILE_JSON.parent.mkdir(parents=True, exist_ok=True)
    USER_PROFILE_JSON.write_text(
        json.dumps({"tier_id": tier_id, "cover_type": cover_type, "policy_start_date": policy_start}),
        encoding="utf-8",
    )


def has_profile() -> bool:
    try:
        with dbmod.get_conn() as conn:
            row = conn.execute("SELECT 1 FROM user_profile WHERE id = 1").fetchone()
        return row is not None
    except Exception:
        return False


def run_onboarding() -> None:
    console.print("[bold cyan]Welcome to MediBridge![/bold cyan]")
    console.print("Tell me about your OSHC policy for accurate coverage info.\n")

    with dbmod.get_conn() as conn:
        insurers = _list_insurers(conn)

    table = Table(title="OSHC Providers")
    table.add_column("#", justify="right")
    table.add_column("Provider")
    for i, ins in enumerate(insurers, 1):
        table.add_row(str(i), ins["insurer_name"])
    console.print(table)

    choice = int(Prompt.ask("Provider number", choices=[str(i) for i in range(1, len(insurers) + 1)]))
    insurer = insurers[choice - 1]

    with dbmod.get_conn() as conn:
        tiers = _list_tiers(conn, insurer["insurer_id"])

    if len(tiers) == 1:
        tier = tiers[0]
        console.print(f"Tier: [bold]{tier['tier_name']}[/bold] (only option)")
    else:
        tier_table = Table(title=f"{insurer['insurer_name']} Tiers")
        tier_table.add_column("#", justify="right")
        tier_table.add_column("Tier")
        for i, t in enumerate(tiers, 1):
            tier_table.add_row(str(i), t["tier_name"])
        console.print(tier_table)
        tchoice = int(Prompt.ask("Tier number", choices=[str(i) for i in range(1, len(tiers) + 1)]))
        tier = tiers[tchoice - 1]

    while True:
        date_str = Prompt.ask("Policy start date (YYYY-MM-DD)")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            console.print("[red]Invalid date format.[/red]")

    cover = Prompt.ask("Cover type", choices=COVER_TYPES, default="single")

    _save_profile(tier["tier_id"], cover, date_str)
    console.print(f"\n[green]Profile saved.[/green] {insurer['insurer_name']} / {tier['tier_name']} / {cover} / {date_str}\n")

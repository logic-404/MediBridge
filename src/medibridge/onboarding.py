"""CLI onboarding flow."""
from __future__ import annotations

from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from medibridge.data import db as dbmod
from medibridge.profile import COVER_TYPES as _COVER_TYPES_TUPLE
from medibridge.profile import has_profile, save_profile

console = Console()

COVER_TYPES = list(_COVER_TYPES_TUPLE)

__all__ = ["has_profile", "run_onboarding", "COVER_TYPES"]


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

    save_profile(tier["tier_id"], cover, date_str)
    console.print(f"\n[green]Profile saved.[/green] {insurer['insurer_name']} / {tier['tier_name']} / {cover} / {date_str}\n")

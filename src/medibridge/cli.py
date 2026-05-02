"""Rich CLI entry point."""
from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from medibridge.agent.graph import build_graph
from medibridge.config import DB_PATH, settings
from medibridge.data import db as dbmod
from medibridge.onboarding import has_profile, run_onboarding
from medibridge.tools.mbs_lookup import lookup_mbs_item

console = Console()

BANNER = """[bold cyan]MediBridge[/bold cyan] — your OSHC coverage assistant
Type your question, or use a command:
  [yellow]/quit[/yellow]    exit
  [yellow]/reset[/yellow]   clear conversation
  [yellow]/item <num>[/yellow]  look up an MBS item
  [yellow]/profile[/yellow] re-run onboarding
"""


def _ensure_db_ready() -> bool:
    if not DB_PATH.exists():
        console.print("[red]Database not found.[/red] Run: [bold]python -m medibridge.data.ingest[/bold]")
        return False
    return True


def _print_item(item_num: str) -> None:
    item = lookup_mbs_item.invoke({"item_num": item_num})
    if not item:
        console.print(f"[red]Item {item_num} not found.[/red]")
        return
    console.print(Panel(
        f"[bold]Item {item['item_num']}[/bold]  fee=${item.get('schedule_fee')}\n"
        f"Group: {item.get('group_code')} ({item.get('group_desc') or '?'})\n"
        f"Category: {item.get('category')} ({item.get('category_desc') or '?'})\n\n"
        f"{(item.get('description') or '').strip()}",
        title=f"MBS {item['item_num']}",
    ))


def main() -> None:
    if not _ensure_db_ready():
        return
    if not settings.openai_api_key:
        console.print("[red]OPENAI_API_KEY not set in .env[/red]")
        return

    console.print(Panel(BANNER, expand=False))

    if not has_profile():
        run_onboarding()

    graph = build_graph()
    history: list = []

    while True:
        try:
            user_input = console.input("[bold green]you>[/bold green] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nbye")
            return
        if not user_input:
            continue
        if user_input == "/quit":
            return
        if user_input == "/reset":
            history = []
            console.print("[yellow]conversation cleared[/yellow]")
            continue
        if user_input == "/profile":
            run_onboarding()
            graph = build_graph()  # rebuild with new system prompt context
            continue
        if user_input.startswith("/item "):
            _print_item(user_input.split(maxsplit=1)[1].strip())
            continue

        history.append(HumanMessage(content=user_input))
        result = graph.invoke({"messages": history})
        history = result["messages"]
        last = history[-1]
        if isinstance(last, AIMessage) and last.content:
            content = last.content if isinstance(last.content, str) else str(last.content)
            console.print(Panel(Markdown(content), title="MediBridge", border_style="cyan"))


if __name__ == "__main__":
    main()

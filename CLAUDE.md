# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Conventions

- **Always run inside the project venv.** Activate first (`.venv\Scripts\Activate.ps1` on Windows PowerShell, `source .venv/bin/activate` on POSIX), then call `python`/`pip`/`medibridge`/`medibridge-cli` as plain commands. The `.venv/` directory is gitignored — never hardcode `.venv/Scripts/...` paths in scripts, configs, or docs that get committed.

## Commands

(Activate the venv first.)

```bash
# Install
pip install -e .

# Run web app (FastAPI + mounted SPA)
medibridge                  # uvicorn on http://localhost:8000

# Run CLI
medibridge-cli
# or: python -m medibridge.cli

# Ingest data (one-time after clone — requires knowledge/ directory)
python -m medibridge.data.ingest
python -m medibridge.data.ingest --skip-chroma   # skip vector embeddings
python -m medibridge.data.ingest --no-reset      # preserve existing SQLite, append only

# Tests
python -m pytest tests/ -v
python -m pytest tests/test_coverage_calculator.py -v

# Build wheel
python -m build
```

**Required env:** `OPENAI_API_KEY` in `.env` (see `.env.example`). Optional: `LANGSMITH_*` vars for tracing.

**`knowledge/` directory is not in repo** — must be provided externally before ingestion. Contains: MBS XML, IMAP TSV, Deed PDF, MBS Book PDF, Item Info PDF, per-insurer markdown.

## Architecture

Dual-store agentic RAG: SQLite for structured MBS/insurer/clinic data, ChromaDB for semantic policy search. LangGraph drives a ReAct loop over 6 tools.

```
CLI (cli.py + onboarding.py)
  └─> LangGraph ReAct agent (agent/graph.py)
        └─> 6 LangChain @tools (tools/)
              ├─> SQLite: mbs_items, insurer_tiers, oshc_coverage_rules, clinics, ...
              └─> ChromaDB: mbs_descriptions, oshc_rules
```

**Data layer layout (`src/medibridge/data/`):**

| Module | Role |
|--------|------|
| `db.py` | Connection helpers only: `connect`, `get_conn`, `init_schema`, `reset_db` |
| `schema.py` | All `CREATE TABLE` / `CREATE INDEX` / FTS5 DDL |
| `queries.py` | Read helpers: `get_item_by_number`, `search_items_by_keyword`, `search_clinics`, `ALLOWED_CLINIC_TYPES`, … |
| `parsers/` | Raw input → in-memory: `mbs_xml`, `imap`, `oshc_deed`, `mbs_book`, `mbs_item_info`, `knowledge_md` |
| `ingest/` | In-memory → SQLite/Chroma writes: `mbs`, `insurers`, `oshc_rules`, `clinics`, `chroma`. Orchestrator in `__init__.py`; entry point in `__main__.py` |
| `vectorstore.py` | Chroma client + add/query helpers |

**Other key modules:**

| Module | Role |
|--------|------|
| `config.py` | Paths (incl. `CLINICS_SOURCE_PATH`), env vars (pydantic-settings), model names (`CHAT_MODEL = "gpt-5-nano"`, `EMBEDDING_MODEL = "text-embedding-3-small"`) |
| `models/` | Pydantic data classes: `MBSItem`, `CoverageResult`, `UserProfile`, `Insurer`, `InsurerTier` |
| `tools/` | 6 tools: `search_mbs_items` (hybrid RRF), `lookup_mbs_item`, `calculate_oshc_coverage`, `check_waiting_period`, `query_oshc_rules`, `search_clinics` |
| `agent/graph.py` | `build_graph()` — LangGraph state machine entry point |
| `agent/prompts.py` | `SYSTEM_TEMPLATE` + `system_prompt()` — injected per-turn with live user profile |

**Adding a new data source:** drop the raw file under `data/sources/`, add a parser under `data/parsers/`, add a writer under `data/ingest/<source>.py`, wire it into `data/ingest/__init__.py:ingest_sqlite()`, and extend `data/schema.py` with the table.

## Coverage Calculator Logic

Two eligibility gates, strict order:
1. **IMAP gate** — item with no IMAP mapping → excluded (non-MBS program, e.g. CDBS)
2. **Insurer exclusions** — keyword match on item text (cosmetic, IVF, repatriation…)

Benefit priority: `benefit_100/85/75` XML fields → fallback to `schedule_fee × tier_pct`. Cap: benefit ≤ schedule_fee (Clause 3.6d). In-hospital always 100%.

Special cases: anaesthesia (`benefit_type='A'`) = time-based estimate + warning; derived-fee items (`fee_type='D'`) = cannot auto-calculate.

## Hybrid Search (search_mbs_items)

Reciprocal rank fusion: 60% vector (ChromaDB `mbs_descriptions`) + 40% FTS5 (SQLite `mbs_fts`, Porter stemming). Results hydrated from SQLite.

## Clinic Search (search_clinics)

Queensland-only clinic directory (620 rows). Source DB at `data/sources/clinics_qld.db` is ingested into the `clinics` table in `medibridge.db`. Filters: `postcode` and/or `suburb` (case-insensitive), optional `clinic_type` ∈ {GP, Psychology, Pharmacy, Psychiatry, Hospital}. The `type` column is comma-separated multi-value — the query wraps it with commas to avoid `Psych*` substring collisions. `phone`, `hours`, `latitude`, `longitude` are NULL across the dataset; the tool drops them from output.

## Data Not in Repo

- `data/` — gitignored runtime data (SQLite DB, ChromaDB, user profile JSON, source seeds)
- `data/sources/clinics_qld.db` — raw QLD clinics DB (read-only seed input)
- `knowledge/` — source documents for ingestion (must be provided)
- `.env` — secrets

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

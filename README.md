# MediBridge

**MediBridge** is an agentic RAG assistant for **Overseas Student Health Cover (OSHC)** in Australia. It answers natural-language questions about MBS items, insurer benefits, waiting periods, policy rules, and (for Queensland) clinic lookup. A **LangGraph** ReAct agent orchestrates tools over **SQLite** (structured MBS, insurers, clinics) and **ChromaDB** (semantic search over item text and policy chunks).

You can use MediBridge via a **Rich terminal CLI**, a **web UI** (static SPA + streaming chat), or the **HTTP API** under `/api`.

---

## Features

- **Hybrid MBS search** - Reciprocal rank fusion of Chroma embeddings (60%) and SQLite FTS5 keyword search (40%); degrades to FTS-only if the vector store is unavailable.
- **Coverage calculator** - IMAP eligibility gate, insurer exclusion keywords, benefit fields from MBS XML (with schedule-fee cap per deed), in-hospital 100%, anaesthesia and derived-fee handling.
- **Waiting periods** - Tier-specific rules with deed defaults.
- **Policy RAG** - `query_oshc_rules` over deed PDF, MBS book/item PDFs, and curated insurer markdown in Chroma.
- **Clinic search (Queensland)** - Filter by postcode and/or suburb; optional clinic type and billing mode; data ingested from a bundled seed SQLite file.

---

## Requirements

- **Python 3.11+**
- **OpenAI API key** - chat (`CHAT_MODEL` in `config.py`, currently `gpt-5-nano`) and embeddings (`text-embedding-3-small`) for the agent and Chroma ingest.
- **Optional:** LangSmith env vars for tracing (see `.env.example`).

Work inside a virtual environment. Install the package in editable mode from the repository root:

```bash
pip install -e .
```

For tests and building a wheel, install tooling separately (not declared in `pyproject.toml`):

```bash
pip install pytest build
```

---

## Configuration

Copy `.env.example` to `.env` at the project root and set at least:

```bash
OPENAI_API_KEY=sk-...
```

Optional LangSmith variables are documented in `.env.example`.

Runtime paths are defined in `src/medibridge/config.py`: SQLite and Chroma live under `data/`, profile backup at `data/user_profile.json`, and raw seeds under `data/sources/` (for example `clinics_qld.db`).

---

## Data you must supply (`knowledge/`)

The repository does **not** include government source files. Before ingestion, create a `knowledge/` directory at the repo root with (paths must match `config.py`):

| Path | Purpose |
|------|---------|
| `knowledge/data/MBS-XML-20260301-version 2.XML` | MBS XML export |
| `knowledge/data/20260301_MBSONLINE_IMAP.TXT` | IMAP TSV (Windows-1252) |
| `knowledge/documents/deed-for-the-provision-of-overseas-student-health-cover-1-july-2025.pdf` | OSHC deed |
| `knowledge/documents/MBS Book - March 2026.pdf` | MBS book (explanatory pages ingested per config) |
| `knowledge/documents/MBS Item Information.pdf` | Item information PDF |
| `knowledge/insurers/` | Per-insurer markdown (and comparisons if present) |
| `knowledge/reference/` | Additional reference markdown for rules embedding |

Place **`data/sources/clinics_qld.db`** in the repo (read-only seed) so clinic ingestion can run; if the file is missing, ingest continues and prints a skip message for clinics.

Generated artifacts (`data/medibridge.db`, `data/chroma/`, local profile JSON) are gitignored.

---

## Ingestion

After `knowledge/` (and optionally `data/sources/clinics_qld.db`) are in place, run:

```bash
python -m medibridge.data.ingest
```

| Flag | Effect |
|------|--------|
| `--skip-chroma` | SQLite (and clinics) only; no embeddings |
| `--no-reset` | Do not reset the database before writing (append-oriented re-run) |

Chroma ingestion **requires** `OPENAI_API_KEY`. If it is unset, the pipeline skips vector indexing and prints a warning.

---

## Running MediBridge

### Web app

```bash
medibridge
```

Starts **Uvicorn** on **http://localhost:8000** with reload enabled: the **React SPA** is served from `ui/`, and JSON routes are mounted under **`/api`** (for example chat, profile, insurers, MBS helpers, coverage, clinics).

### CLI

```bash
medibridge-cli
# or
python -m medibridge.cli
```

The CLI checks that `data/medibridge.db` exists and that `OPENAI_API_KEY` is set. On first use it runs an onboarding wizard (insurer, tier, policy start date, cover type). Commands: `/quit`, `/reset`, `/item <num>`, `/profile`.

### Docker

Build the image (no frontend build step needed — SPA uses CDN React):

```bash
docker build -t medibridge .
```

Run, mounting pre-ingested data and your knowledge sources:

```bash
docker run \
  -e OPENAI_API_KEY=sk-... \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/knowledge:/app/knowledge" \
  -p 8000:8000 \
  medibridge
```

The `data/` volume must contain an already-ingested `medibridge.db` (and optionally `chroma/`). To ingest inside the container first:

```bash
docker run --rm \
  -e OPENAI_API_KEY=sk-... \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/knowledge:/app/knowledge" \
  medibridge python -m medibridge.data.ingest
```

Then start the server with the run command above.

---

## Agent tools

The LangGraph agent binds **six** LangChain tools with **parallel tool calling enabled** — when the model issues multiple independent lookups in one turn, they execute concurrently:

1. `search_mbs_items` - hybrid search
2. `lookup_mbs_item` - exact item by number
3. `calculate_oshc_coverage` - out-of-pocket estimate
4. `check_waiting_period` - waiting months / served status
5. `query_oshc_rules` - semantic policy retrieval
6. `search_clinics` - Queensland clinic directory

---

## Project layout

```
MediBridge/
  src/medibridge/
    cli.py              Rich REPL
    onboarding.py       Profile wizard (CLI)
    config.py           Paths, settings, models
    server/             FastAPI app, routers, schemas
    agent/              graph.py, prompts.py, state
    tools/              LangChain @tool implementations
    models/             Pydantic models
    data/
      db.py, schema.py, queries.py, vectorstore.py
      parsers/          mbs_xml, imap, PDFs, knowledge_md, ...
      ingest/           pipeline, mbs, insurers, chroma, clinics, ...
  ui/                   Static SPA (mounted by FastAPI)
  tests/
  knowledge/            Not committed; you provide sources
  data/                 Gitignored runtime DB, Chroma, profile
  pyproject.toml
  .env.example
  ARCHITECTURE.md       Deeper design (some paths may lag code)
  CLAUDE.md             Maintainer conventions for this repo
```

---

## Tests

```bash
python -m pytest tests/ -v
```

Notable modules under `tests/`: coverage calculator golden cases, MBS XML parsing, DB queries, clinic search.

---

## Building a wheel

```bash
python -m build
```

Output goes to `dist/`.

---

## Further reading

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - data pipeline, schema overview, coverage logic, insurer seeding (treat layout/file names as conceptual where they differ from `src/medibridge/data/`).
- **[CLAUDE.md](CLAUDE.md)** - venv usage, commands, and how to extend ingestion.

---

## Disclaimer

MediBridge is for **informational** use only. Always confirm coverage, fees, and waiting periods with your insurer and care providers.

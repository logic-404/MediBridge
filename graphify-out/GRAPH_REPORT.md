# Graph Report - .  (2026-04-27)

## Corpus Check
- 34 files · ~8,029 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 293 nodes · 528 edges · 20 communities detected
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 110 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Config, Ingest & Vector Store|Config, Ingest & Vector Store]]
- [[_COMMUNITY_SQLite DB & MBS Data Models|SQLite DB & MBS Data Models]]
- [[_COMMUNITY_Architecture Agent & Coverage Docs|Architecture: Agent & Coverage Docs]]
- [[_COMMUNITY_Architecture Data & Search Docs|Architecture: Data & Search Docs]]
- [[_COMMUNITY_Coverage Calculator & Tests|Coverage Calculator & Tests]]
- [[_COMMUNITY_MBS XML Parser|MBS XML Parser]]
- [[_COMMUNITY_CLI, Agent Graph & Onboarding|CLI, Agent Graph & Onboarding]]
- [[_COMMUNITY_Waiting Period Checker|Waiting Period Checker]]
- [[_COMMUNITY_MBS Lookup Tool|MBS Lookup Tool]]
- [[_COMMUNITY_Knowledge MD Parser|Knowledge MD Parser]]
- [[_COMMUNITY_Insurer & Profile Models|Insurer & Profile Models]]
- [[_COMMUNITY_IMAP TSV Parser|IMAP TSV Parser]]
- [[_COMMUNITY_Agent System Prompt|Agent System Prompt]]
- [[_COMMUNITY_LangGraph State|LangGraph State]]
- [[_COMMUNITY_MBS Book PDF Parser|MBS Book PDF Parser]]
- [[_COMMUNITY_MBS Item Info Parser|MBS Item Info Parser]]
- [[_COMMUNITY_LangSmith & Config Docs|LangSmith & Config Docs]]
- [[_COMMUNITY_Package Init Files|Package Init Files]]
- [[_COMMUNITY_OSHC Domain Concepts|OSHC Domain Concepts]]
- [[_COMMUNITY_Architecture Insurer Models Docs|Architecture: Insurer Models Docs]]

## God Nodes (most connected - your core abstractions)
1. `_calculate()` - 16 edges
2. `MBSItem` - 15 edges
3. `get_conn()` - 14 edges
4. `ingest_sqlite()` - 14 edges
5. `ingest_chroma()` - 13 edges
6. `IMAPMapping` - 13 edges
7. `parse_mbs_xml()` - 12 edges
8. `_seed()` - 12 edges
9. `CoverageResult` - 10 edges
10. `conn()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Sentinel '31/12/9999' or empty -> NULL.` --uses--> `MBSItem`  [INFERRED]
  C:\Users\tsingh01\Dev\MediBridge\src\medibridge\data\parse_mbs_xml.py → C:\Users\tsingh01\Dev\MediBridge\src\medibridge\models\mbs_item.py
- `Stream MBSItems from XML file.` --uses--> `MBSItem`  [INFERRED]
  C:\Users\tsingh01\Dev\MediBridge\src\medibridge\data\parse_mbs_xml.py → C:\Users\tsingh01\Dev\MediBridge\src\medibridge\models\mbs_item.py
- `items: list of dicts with item_num, description, category_desc, group_desc, btos` --uses--> `Settings`  [INFERRED]
  C:\Users\tsingh01\Dev\MediBridge\src\medibridge\data\vectorstore.py → C:\Users\tsingh01\Dev\MediBridge\src\medibridge\config.py
- `Chroma metadata accepts only str/int/float/bool. None -> drop key.` --uses--> `Settings`  [INFERRED]
  C:\Users\tsingh01\Dev\MediBridge\src\medibridge\data\vectorstore.py → C:\Users\tsingh01\Dev\MediBridge\src\medibridge\config.py
- `_save_profile()` --calls--> `get_conn()`  [INFERRED]
  C:\Users\tsingh01\Dev\MediBridge\src\medibridge\onboarding.py → C:\Users\tsingh01\Dev\MediBridge\src\medibridge\data\db.py

## Hyperedges (group relationships)
- **Ingest Stage 1: SQLite Population** — architecture_parse_mbs_xml_py, architecture_parse_imap_py, architecture_seed_insurers_py, architecture_db_py, architecture_mbs_items_table, architecture_imap_mappings_table, architecture_mbs_fts_table, architecture_insurer_tiers_table, architecture_insurer_exclusions_table, architecture_insurer_waiting_periods_table, architecture_oshc_coverage_rules_table [EXTRACTED 1.00]
- **Ingest Stage 2: ChromaDB Population** — architecture_parse_oshc_deed_py, architecture_parse_mbs_book_py, architecture_parse_mbs_item_info_py, architecture_parse_knowledge_md_py, architecture_vectorstore_py, architecture_text_embedding_3_small, architecture_mbs_descriptions_collection, architecture_oshc_rules_collection [EXTRACTED 1.00]
- **LangGraph ReAct Loop** — architecture_agent_node, architecture_should_continue, architecture_toolnode, architecture_medibridge_state, architecture_gpt5_mini [EXTRACTED 1.00]
- **Coverage Calculator Gate Sequence** — architecture_imap_gate, architecture_imap_mappings_table, architecture_insurer_exclusions_table, architecture_insurer_tiers_table, architecture_clause_3_6d_cap, architecture_coverageresult_model [EXTRACTED 1.00]
- **Hybrid Search RRF Fusion** — architecture_search_mbs_items, architecture_mbs_descriptions_collection, architecture_mbs_fts_table, architecture_hybrid_search [EXTRACTED 1.00]

## Communities

### Community 0 - "Config, Ingest & Vector Store"
Cohesion: 0.1
Nodes (29): BaseSettings, _enable_langsmith(), ensure_data_dir(), Paths, env vars, model config., Push LangSmith vars into os.environ so LangChain auto-traces., Settings, ingest_chroma(), main() (+21 more)

### Community 1 - "SQLite DB & MBS Data Models"
Cohesion: 0.13
Nodes (31): connect(), fts_count(), get_conn(), get_items_by_btos(), get_items_by_category(), init_schema(), insert_deed_rules(), insert_imap_mappings() (+23 more)

### Community 2 - "Architecture: Agent & Coverage Docs"
Cohesion: 0.07
Nodes (39): Agent Node (GPT-5-mini), calculate_oshc_coverage Tool, check_waiting_period Tool, Clause 3.6d Benefit Cap, CLI (Rich), cli.py, tools/coverage_calculator.py, data/db.py (+31 more)

### Community 3 - "Architecture: Data & Search Docs"
Cohesion: 0.08
Nodes (34): ChromaDB (2 collections), models/coverage.py, CoverageResult Pydantic Model, OSHC Deed PDF Source, Hybrid Search (Vector + FTS5 RRF), imap_mappings Table, IMAP TSV Source File, IMAPMapping Pydantic Model (+26 more)

### Community 4 - "Coverage Calculator & Tests"
Cohesion: 0.17
Nodes (22): _calculate(), calculate_oshc_coverage(), _check_insurer_exclusions(), _get_user_tier(), _has_imap_mapping(), _is_gp_item(), _not_covered(), OSHC benefit calculation, insurer-aware.  Coverage eligibility is determined by (+14 more)

### Community 5 - "MBS XML Parser"
Cohesion: 0.26
Nodes (13): _flt(), _norm_end_date(), parse_mbs_xml(), Parse MBS XML -> list[MBSItem]. Active items only., Sentinel '31/12/9999' or empty -> NULL., Stream MBSItems from XML file., _txt(), Golden tests for MBS XML parser. (+5 more)

### Community 6 - "CLI, Agent Graph & Onboarding"
Cohesion: 0.23
Nodes (10): _ensure_db_ready(), main(), _print_item(), Rich CLI entry point., build_graph(), has_profile(), _list_insurers(), _list_tiers() (+2 more)

### Community 7 - "Waiting Period Checker"
Cohesion: 0.4
Nodes (8): check_waiting_period(), _classify(), _get_user_tier_id(), _months_elapsed(), _parse_iso(), Waiting period checker, insurer-aware., Map item + optional condition hint -> condition_type used in waiting table., Check if a waiting period applies to a service.      Args:         item_num: MBS

### Community 8 - "MBS Lookup Tool"
Cohesion: 0.36
Nodes (7): get_item_by_number(), _hybrid_search(), lookup_mbs_item(), Hybrid search: ChromaDB vector + SQLite FTS5., Search MBS items by natural-language description or keyword.     Returns up to t, Look up a specific MBS item by its item number., search_mbs_items()

### Community 9 - "Knowledge MD Parser"
Cohesion: 0.52
Nodes (5): _infer_insurer_id(), parse_knowledge_md(), Curated knowledge .md -> chunks., Split markdown into (heading, body) sections by ## headers., _split_by_h2()

### Community 10 - "Insurer & Profile Models"
Cohesion: 0.52
Nodes (5): BaseModel, Insurer, InsurerTier, Insurer / tier / user profile models., UserProfile

### Community 11 - "IMAP TSV Parser"
Cohesion: 0.62
Nodes (5): _norm_end_date(), parse_imap(), Parse IMAP TSV -> list[IMAPMapping]., _strip_leading_zeros(), _txt()

### Community 12 - "Agent System Prompt"
Cohesion: 0.7
Nodes (3): System prompt with insurer context., system_prompt(), _user_context()

### Community 13 - "LangGraph State"
Cohesion: 0.5
Nodes (2): MediBridgeState, TypedDict

### Community 14 - "MBS Book PDF Parser"
Cohesion: 0.67
Nodes (2): parse_mbs_book(), MBS Book PDF -> chunks (configured page range).

### Community 15 - "MBS Item Info Parser"
Cohesion: 0.67
Nodes (2): parse_mbs_item_info(), MBS Item Information PDF -> chunks.

### Community 16 - "LangSmith & Config Docs"
Cohesion: 0.5
Nodes (4): config.py, LangSmith Observability, pydantic-settings, Rationale: LangSmith Enabled at Config Import

### Community 17 - "Package Init Files"
Cohesion: 0.67
Nodes (1): MediBridge — Agentic RAG for OSHC insurance queries.

### Community 18 - "OSHC Domain Concepts"
Cohesion: 0.67
Nodes (3): MBS (Medicare Benefits Schedule), MediBridge, OSHC (Overseas Student Health Cover)

### Community 19 - "Architecture: Insurer Models Docs"
Cohesion: 1.0
Nodes (2): models/insurer.py, UserProfile Pydantic Model

## Knowledge Gaps
- **35 isolated node(s):** `Push LangSmith vars into os.environ so LangChain auto-traces.`, `Split markdown into (heading, body) sections by ## headers.`, `Return list of {text, metadata} chunks.`, `Search MBS items by natural-language description or keyword.     Returns up to t`, `Look up a specific MBS item by its item number.` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `LangGraph State`** (4 nodes): `state.py`, `state.py`, `MediBridgeState`, `TypedDict`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MBS Book PDF Parser`** (4 nodes): `parse_mbs_book.py`, `parse_mbs_book()`, `MBS Book PDF -> chunks (configured page range).`, `parse_mbs_book.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MBS Item Info Parser`** (4 nodes): `parse_mbs_item_info.py`, `parse_mbs_item_info()`, `MBS Item Information PDF -> chunks.`, `parse_mbs_item_info.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package Init Files`** (3 nodes): `__init__.py`, `MediBridge — Agentic RAG for OSHC insurance queries.`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Architecture: Insurer Models Docs`** (2 nodes): `models/insurer.py`, `UserProfile Pydantic Model`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_conn()` connect `SQLite DB & MBS Data Models` to `Config, Ingest & Vector Store`, `Coverage Calculator & Tests`, `CLI, Agent Graph & Onboarding`, `Waiting Period Checker`, `MBS Lookup Tool`, `Agent System Prompt`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Why does `ingest_chroma()` connect `Config, Ingest & Vector Store` to `SQLite DB & MBS Data Models`, `Knowledge MD Parser`, `MBS Book PDF Parser`, `MBS Item Info Parser`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `ingest_sqlite()` connect `SQLite DB & MBS Data Models` to `Config, Ingest & Vector Store`, `IMAP TSV Parser`, `MBS XML Parser`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `_calculate()` (e.g. with `get_item_by_number()` and `CoverageResult`) actually correct?**
  _`_calculate()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MBSItem` (e.g. with `SQLite schema + ops + FTS5.` and `Build categories / groups / btos_types from imap_mappings.`) actually correct?**
  _`MBSItem` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `get_conn()` (e.g. with `_save_profile()` and `has_profile()`) actually correct?**
  _`get_conn()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ingest_sqlite()` (e.g. with `reset_db()` and `get_conn()`) actually correct?**
  _`ingest_sqlite()` has 11 INFERRED edges - model-reasoned connections that need verification._
"""FastAPI application — wraps the MediBridge agent + tools and serves the SPA."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from medibridge.agent.graph import build_graph
from medibridge.server.routes import chat, clinics, coverage, insurers, mbs, profile
from medibridge.config import DB_PATH, ROOT_DIR, settings

WEB_DIR = ROOT_DIR / "ui"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not DB_PATH.exists():
        raise RuntimeError(
            f"Database missing at {DB_PATH}. Run: python -m medibridge.data.ingest"
        )
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not set (provide via .env or environment variable)")
    app.state.graph = build_graph()
    yield


app = FastAPI(title="MediBridge", lifespan=lifespan)

api_routers = [
    insurers.router,
    profile.router,
    coverage.router,
    mbs.router,
    clinics.router,
    chat.router,
]
for r in api_routers:
    app.include_router(r, prefix="/api")


if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")


def run() -> None:
    import uvicorn

    reload = os.environ.get("MEDIBRIDGE_RELOAD", "").lower() in ("1", "true")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("medibridge.server.main:app", host="0.0.0.0", port=port, reload=reload)


if __name__ == "__main__":
    run()

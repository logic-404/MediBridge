"""LangGraph state."""
from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class MediBridgeState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    mbs_results: list[dict] | None
    selected_item: dict | None
    coverage_result: dict | None

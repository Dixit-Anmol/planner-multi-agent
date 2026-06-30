"""
Shared state schema and LLM/tool initialization.
"""

import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()


# ─── Shared State Schema ─────────────────────────────────────────────────────
class AgentState(TypedDict):
    goal: str
    tasks: List[str]
    results: List[str]
    critique: str
    approved: bool
    iterations: int


# ─── Singleton-style accessors ────────────────────────────────────────────────
_llm = None
_search = None


def get_llm() -> ChatGroq:
    """Return a cached ChatGroq instance."""
    global _llm
    if _llm is None:
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set.")
        _llm = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
            groq_api_key=api_key,
        )
    return _llm


def get_search() -> DuckDuckGoSearchRun:
    """Return a cached DuckDuckGoSearchRun instance."""
    global _search
    if _search is None:
        _search = DuckDuckGoSearchRun()
    return _search

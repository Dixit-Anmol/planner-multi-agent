#!/usr/bin/env python3
"""
Planner Multi-Agent System
===========================
A LangGraph-based multi-agent system that uses a Planner → Executor → Verifier
loop to break down goals, execute tasks with web search, and verify quality.

Token-optimized for Groq free-tier reliability.
"""

import os
import json
import time
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

# ─── Environment Setup ───────────────────────────────────────────────────────
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set.")

llm = ChatGroq(
    temperature=0.3,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    max_tokens=512,
)

search = DuckDuckGoSearchRun()


# ─── Shared State Schema ─────────────────────────────────────────────────────
class AgentState(TypedDict):
    goal: str
    tasks: List[str]
    results: List[str]
    summary: str
    critique: str
    approved: bool
    iterations: int


# ─── Agent 1: Planner ────────────────────────────────────────────────────────
def planner(state: AgentState) -> AgentState:
    """Breaks the user's goal into at most 3 high-level tasks."""
    system = (
        "Break the goal into 1-3 high-level tasks. "
        "For simple questions, use just 1 task. "
        "Respond ONLY with a JSON array of strings."
    )

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=state["goal"]),
    ]
    response = llm.invoke(messages).content.strip()

    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        tasks = json.loads(clean)
        tasks = tasks[:3]  # Enforce max 3 tasks
    except json.JSONDecodeError:
        tasks = [response]

    print(f"\n[Planner] Generated {len(tasks)} tasks:")
    for i, t in enumerate(tasks):
        print(f"  {i+1}. {t}")

    return {**state, "tasks": tasks}


# ─── Agent 2: Executor ───────────────────────────────────────────────────────
_EXEC_PROMPT = (
    "Answer the task in 150-200 words. Be concise and informative. "
    "Do not repeat information already covered."
)

def executor(state: AgentState) -> AgentState:
    """Executes each task with concise responses and minimal search context."""
    results = []
    critique_ctx = ""
    if state["critique"]:
        critique_ctx = f" Improve based on: {state['critique']}"

    for task in state["tasks"]:
        time.sleep(2)  # Rate-limit protection

        # Try web search — truncate to 400 chars
        search_ctx = ""
        try:
            search_result = search.invoke(task[:80])
            search_ctx = f"\n\nContext: {search_result[:400]}"
        except Exception as e:
            print(f"[Executor] Search failed: {e}")

        messages = [
            SystemMessage(content=_EXEC_PROMPT + critique_ctx),
            HumanMessage(content=f"{task}{search_ctx}"),
        ]

        result = llm.invoke(messages).content
        results.append(result)
        print(f"\n[Executor] Task: {task[:60]}...")
        print(f"  Result: {result[:200]}...")

    return {**state, "results": results, "iterations": state["iterations"] + 1}


# ─── Agent 3: Verifier (LLM-as-a-Judge) ──────────────────────────────────────
_VERIFIER_PROMPT = (
    "Rate these results for the given goal. "
    "Score 0.0-1.0 (completeness, accuracy, clarity). "
    'Respond ONLY as JSON: {"score":0.9,"approved":true,"critique":"..."}'
)

def verifier(state: AgentState) -> AgentState:
    """Evaluates quality using only task titles and short summaries."""
    if state["iterations"] >= 2:
        print("[Verifier] Max iterations reached — force approving.")
        summary = _build_summary(state)
        return {**state, "approved": True, "summary": summary}

    # Send only task titles + first 100 chars of each result
    condensed = "\n".join(
        f"- {t}: {r[:100]}..."
        for t, r in zip(state["tasks"], state["results"])
    )

    messages = [
        SystemMessage(content=_VERIFIER_PROMPT),
        HumanMessage(content=f"Goal: {state['goal']}\n\nResults:\n{condensed}"),
    ]
    raw = llm.invoke(messages).content.strip()

    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        verdict = json.loads(clean)
        approved = verdict.get("approved", False)
        critique = verdict.get("critique", "")
        score = verdict.get("score", 0)
    except Exception:
        approved, critique, score = False, raw, 0

    print(f"\n[Verifier] Score: {score:.2f} | Approved: {approved}")
    if not approved:
        print(f"  Critique: {critique}")

    summary = _build_summary(state) if approved else state.get("summary", "")
    return {**state, "approved": approved, "critique": critique, "summary": summary}


def _build_summary(state: AgentState) -> str:
    """Combine task results into a single clean response."""
    parts = []
    for task, result in zip(state["tasks"], state["results"]):
        parts.append(f"### {task}\n{result}")
    return "\n\n".join(parts)


def route_after_verify(state: AgentState) -> str:
    """Routes back to executor if not approved, otherwise ends."""
    return "end" if state["approved"] else "executor"


# ─── Build & Run the Graph ────────────────────────────────────────────────────
def main():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("verifier", verifier)

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "verifier")
    graph.add_conditional_edges(
        "verifier",
        route_after_verify,
        {"end": END, "executor": "executor"},
    )

    graph.set_entry_point("planner")
    app = graph.compile()

    initial_state: AgentState = {
        "goal": "Research and summarise the top 3 trends in agriculture for 2025",
        "tasks": [],
        "results": [],
        "summary": "",
        "critique": "",
        "approved": False,
        "iterations": 0,
    }

    print("=" * 60)
    print("  PLANNER MULTI-AGENT SYSTEM")
    print(f"  Goal: {initial_state['goal']}")
    print("=" * 60)

    final_state = app.invoke(initial_state)

    print("\n" + "=" * 60)
    print("  FINAL RESULTS")
    print("=" * 60)
    for i, (t, r) in enumerate(
        zip(final_state["tasks"], final_state["results"])
    ):
        print(f"\n--- Task {i+1}: {t} ---")
        print(r)

    print(f"\nApproved: {final_state['approved']}")
    print(f"Total iterations: {final_state['iterations']}")


if __name__ == "__main__":
    main()

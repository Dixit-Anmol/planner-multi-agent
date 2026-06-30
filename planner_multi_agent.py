#!/usr/bin/env python3
"""
Planner Multi-Agent System
===========================
A LangGraph-based multi-agent system that uses a Planner → Executor → Verifier
loop to break down goals, execute tasks with web search, and verify quality.

Uses Groq's Llama 3.1 LLM and DuckDuckGo for web search.
"""

import os
import json
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
    temperature=0,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
)

search = DuckDuckGoSearchRun()


# ─── Shared State Schema ─────────────────────────────────────────────────────
class AgentState(TypedDict):
    goal: str
    tasks: List[str]
    results: List[str]
    critique: str
    approved: bool
    iterations: int


# ─── Agent 1: Planner ────────────────────────────────────────────────────────
def planner(state: AgentState) -> AgentState:
    """Breaks the user's goal into at most 5 concrete, actionable tasks."""
    system = """You are a planning agent. Break the user's goal into
at most 5 concrete, actionable tasks. Respond ONLY with a
valid JSON array of strings. No preamble, no markdown."""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=f"Goal: {state['goal']}"),
    ]
    response = llm.invoke(messages).content.strip()

    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        tasks = json.loads(clean)
    except json.JSONDecodeError:
        tasks = [response]  # fallback: treat whole response as one task

    print(f"\n[Planner] Generated {len(tasks)} tasks:")
    for i, t in enumerate(tasks):
        print(f"  {i+1}. {t}")

    return {**state, "tasks": tasks}


# ─── Agent 2: Executor ───────────────────────────────────────────────────────
def executor(state: AgentState) -> AgentState:
    """Executes each task, optionally using DuckDuckGo web search for context."""
    results = []
    critique_ctx = ""
    if state["critique"]:
        critique_ctx = (
            f"\n\nYour previous attempt was rejected. "
            f"Previous critique: {state['critique']}"
        )

    for task in state["tasks"]:
        system = (
            f"You are an execution agent. Complete the task thoroughly. "
            f"Use web search if you need current information. {critique_ctx}"
        )

        # Try web search for research tasks
        search_ctx = ""
        try:
            search_result = search.run(task[:100])
            search_ctx = (
                f"\n\nWeb search result for context: \n{search_result[:800]}"
            )
        except Exception:
            pass

        messages = [
            SystemMessage(content=system),
            HumanMessage(content=f"Task: {task}{search_ctx}"),
        ]

        result = llm.invoke(messages).content
        results.append(result)
        print(f"\n[Executor] Task: {task[:60]}...")
        print(f"  Result: {result[:200]}...")

    return {**state, "results": results, "iterations": state["iterations"] + 1}


# ─── Agent 3: Verifier (LLM-as-a-Judge) ──────────────────────────────────────
def verifier(state: AgentState) -> AgentState:
    """Evaluates the quality of results using a scoring rubric."""
    # Safety net — approve after 3 iterations regardless
    if state["iterations"] >= 3:
        print("[Verifier] Max iterations reached — force approving.")
        return {**state, "approved": True}

    combined_results = "\n\n".join(
        f"Task {i+1}: {t}\nResult: {r}"
        for i, (t, r) in enumerate(zip(state["tasks"], state["results"]))
    )

    system = """You are a quality verifier. Evaluate the results against the
original goal using this rubric:
- Completeness: Does it fully address the goal? (0-0.4)
- Accuracy:     Is the information correct and specific? (0-0.3)
- Clarity:      Is it well-structured and clear? (0-0.3)
Sum the scores for a total between 0.0 and 1.0.
Respond ONLY as JSON: {"score":0.9, "approved": true, "critique": "..."}"""

    messages = [
        SystemMessage(content=system),
        HumanMessage(
            content=(
                f"Original goal: {state['goal']}\n\nResults:\n{combined_results}"
            )
        ),
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

    return {**state, "approved": approved, "critique": critique}


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

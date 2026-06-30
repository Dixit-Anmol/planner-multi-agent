"""
Planner Agent — breaks a goal into actionable sub-tasks.
"""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import AgentState, get_llm


def planner(state: AgentState) -> AgentState:
    """Breaks the user's goal into at most 5 concrete, actionable tasks."""
    llm = get_llm()

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

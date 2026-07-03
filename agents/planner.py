"""
Planner Agent — breaks a goal into actionable sub-tasks.
"""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import AgentState, get_llm


def planner(state: AgentState) -> AgentState:
    """Breaks the user's goal into at most 3 high-level tasks."""
    llm = get_llm()

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
        # Enforce max 3 tasks
        tasks = tasks[:3]
    except json.JSONDecodeError:
        tasks = [response]

    print(f"\n[Planner] Generated {len(tasks)} tasks:")
    for i, t in enumerate(tasks):
        print(f"  {i+1}. {t}")

    return {**state, "tasks": tasks}

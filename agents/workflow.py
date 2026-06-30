"""
LangGraph workflow builder — assembles and runs the multi-agent graph.
"""

from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.planner import planner
from agents.executor import executor
from agents.verifier import verifier, route_after_verify


def build_graph():
    """Build and compile the Planner → Executor → Verifier state graph."""
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
    return graph.compile()


def run_workflow(goal: str) -> dict:
    """Run the full multi-agent workflow for a given goal and return final state."""
    app = build_graph()

    initial_state: AgentState = {
        "goal": goal,
        "tasks": [],
        "results": [],
        "critique": "",
        "approved": False,
        "iterations": 0,
    }

    final_state = app.invoke(initial_state)
    return final_state

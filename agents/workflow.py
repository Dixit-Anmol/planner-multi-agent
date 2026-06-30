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


def run_workflow_generator(goal: str):
    """
    Yields (status_message, progress_percentage, state_so_far)
    so the Streamlit app can display step-by-step progress updates.
    """
    app = build_graph()
    
    initial_state: AgentState = {
        "goal": goal,
        "tasks": [],
        "results": [],
        "critique": "",
        "approved": False,
        "iterations": 0,
    }
    
    yield "🧠 Understanding your question...", 15, None
    yield "📋 Planning the best approach...", 30, None
    
    current_state = initial_state
    for event in app.stream(initial_state):
        node_name = list(event.keys())[0]
        state_update = event[node_name]
        current_state = {**current_state, **state_update}
        
        if node_name == "planner":
            yield "🌐 Researching reliable sources...", 50, current_state
        elif node_name == "executor":
            yield "🤖 Generating answer...", 75, current_state
        elif node_name == "verifier":
            if not current_state["approved"] and current_state["iterations"] < 3:
                yield f"✅ Verifying quality (Refining answers, iteration {current_state['iterations']})...", 85, current_state
            else:
                yield "✨ Finalizing response...", 95, current_state
                
    yield "✨ Done", 100, current_state

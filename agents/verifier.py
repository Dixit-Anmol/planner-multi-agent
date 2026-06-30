"""
Verifier Agent — LLM-as-a-Judge quality evaluator.
"""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import AgentState, get_llm


def verifier(state: AgentState) -> AgentState:
    """Evaluates the quality of results using a scoring rubric."""
    # Safety net — approve after 3 iterations regardless
    if state["iterations"] >= 3:
        print("[Verifier] Max iterations reached — force approving.")
        return {**state, "approved": True}

    llm = get_llm()

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

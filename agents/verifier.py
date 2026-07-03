"""
Verifier Agent — LLM-as-a-Judge quality evaluator.
"""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import AgentState, get_llm

_VERIFIER_PROMPT = (
    "Rate these results for the given goal. "
    "Score 0.0-1.0 (completeness, accuracy, clarity). "
    'Respond ONLY as JSON: {"score":0.9,"approved":true,"critique":"..."}'
)


def verifier(state: AgentState) -> AgentState:
    """Evaluates quality using only task titles and short summaries."""
    # Safety net — approve after 2 iterations to save tokens
    if state["iterations"] >= 2:
        print("[Verifier] Max iterations reached — force approving.")
        # Build summary from results
        summary = _build_summary(state)
        return {**state, "approved": True, "summary": summary}

    llm = get_llm()

    # Send only task titles + first 100 chars of each result (not full output)
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

    # Build summary on approval
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

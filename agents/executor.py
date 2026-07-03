"""
Executor Agent — executes tasks with optional DuckDuckGo web search.
"""

import time
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import AgentState, get_llm, get_search

# Concise system prompt — reused across all tasks
_SYSTEM_PROMPT = (
    "Answer the task in 150-200 words. Be concise and informative. "
    "Do not repeat information already covered."
)


def executor(state: AgentState) -> AgentState:
    """Executes each task with concise responses and minimal search context."""
    llm = get_llm()
    search_tool = get_search()

    results = []
    critique_ctx = ""
    if state["critique"]:
        critique_ctx = f" Improve based on: {state['critique']}"

    for task in state["tasks"]:
        # Rate-limit protection
        time.sleep(2)

        # Try web search — truncate to 400 chars for token savings
        search_ctx = ""
        try:
            search_result = search_tool.invoke(task[:80])
            search_ctx = f"\n\nContext: {search_result[:400]}"
        except Exception as e:
            print(f"[Executor] Search failed: {e}")

        prompt = f"{task}{search_ctx}"
        messages = [
            SystemMessage(content=_SYSTEM_PROMPT + critique_ctx),
            HumanMessage(content=prompt),
        ]

        result = llm.invoke(messages).content
        results.append(result)
        print(f"\n[Executor] Task: {task[:60]}...")
        print(f"  Result: {result[:200]}...")

    return {**state, "results": results, "iterations": state["iterations"] + 1}

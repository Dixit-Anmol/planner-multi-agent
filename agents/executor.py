"""
Executor Agent — executes tasks with optional DuckDuckGo web search.
"""

import time
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import AgentState, get_llm, get_search


def executor(state: AgentState) -> AgentState:
    """Executes each task, optionally using DuckDuckGo web search for context."""
    llm = get_llm()
    search_tool = get_search()

    results = []
    critique_ctx = ""
    if state["critique"]:
        critique_ctx = (
            f"\n\nYour previous attempt was rejected. "
            f"Previous critique: {state['critique']}"
        )

    for task in state["tasks"]:
        # Sleep to respect Groq rate limits
        time.sleep(1)

        system = (
            f"You are an execution agent. Complete the task thoroughly. "
            f"Use web search if you need current information. {critique_ctx}"
        )

        # Try web search for research tasks
        search_ctx = ""
        try:
            search_result = search_tool.invoke(task[:100])
            search_ctx = (
                f"\n\nWeb search result for context: \n{search_result[:800]}"
            )
        except Exception as e:
            print(f"[Executor] Search failed for '{task[:30]}...': {e}")

        messages = [
            SystemMessage(content=system),
            HumanMessage(content=f"Task: {task}{search_ctx}"),
        ]

        result = llm.invoke(messages).content
        results.append(result)
        print(f"\n[Executor] Task: {task[:60]}...")
        print(f"  Result: {result[:200]}...")

    return {**state, "results": results, "iterations": state["iterations"] + 1}


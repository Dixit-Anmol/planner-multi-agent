# Planner Multi-Agent System — Report

## What Is It?

The **Planner Multi-Agent System** is an AI-powered workflow built using **LangGraph** (by LangChain) that automates the process of researching and summarizing information on any given goal. Instead of relying on a single LLM call, it orchestrates **three specialized AI agents** that collaborate in a structured loop to produce high-quality, verified output.

## Architecture — The Three Agents

The system follows a **Planner → Executor → Verifier** pipeline:

| Agent       | Role                                                                                         |
|-------------|----------------------------------------------------------------------------------------------|
| **Planner** | Receives the user's goal and breaks it down into up to 5 concrete, actionable sub-tasks.     |
| **Executor**| Takes each sub-task and completes it using the LLM, augmented with live **DuckDuckGo web search** results for up-to-date context. |
| **Verifier**| Acts as an **LLM-as-a-Judge** — evaluates all results against the original goal on a rubric (Completeness, Accuracy, Clarity) and scores them 0–1.0. |

### The Feedback Loop

The key innovation is the **iterative refinement loop**:

1. If the Verifier **approves** the results (score meets threshold), the workflow ends.
2. If the Verifier **rejects** the results, it provides a **critique** — and the Executor re-runs all tasks with the critique as additional context, producing improved results.
3. A **safety cap of 3 iterations** prevents infinite loops.

This design mirrors how real teams work: a planner creates a roadmap, workers execute, and a reviewer provides feedback until quality standards are met.

## Technology Stack

- **LangGraph** (StateGraph): Orchestrates the multi-agent workflow as a directed graph with conditional edges.
- **Groq API** (Llama 3.1 8B Instant): Provides fast, low-latency LLM inference for all three agents.
- **DuckDuckGo Search** (via LangChain Community Tools): Gives the Executor real-time web search capability.
- **LangChain Core**: Provides the message abstractions (SystemMessage, HumanMessage) used to prompt each agent.

## Use Case Demonstrated

The notebook demonstrates the system with the goal: *"Research and summarise the top 3 trends in agriculture for 2025."*

The Planner generated 5 sub-tasks (identify sources, research trends, analyze, prioritize, summarize). The Executor completed each task using web search for current data, and the Verifier scored the final output at **0.85/1.0** — approving it in a single iteration.

## Deployment

The system is deployed via **GitHub Actions** — on every push to `main` (or manual trigger), the workflow installs dependencies and runs the agent end-to-end, with the Groq API key securely stored as a GitHub Secret.

## Key Takeaway

This project demonstrates how **multi-agent orchestration** with LLM-as-a-Judge verification can produce significantly higher-quality AI outputs compared to single-shot prompting, by introducing planning, execution with real-time data, and automated quality control in a structured feedback loop.

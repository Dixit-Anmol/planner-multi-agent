# Planner Multi-Agent System: A LangGraph-Based Autonomous Research Pipeline

## Introduction

The rapid evolution of large language models (LLMs) has given rise to multi-agent architectures that decompose complex tasks into manageable sub-tasks, each handled by a specialized agent. This report presents a **Planner Multi-Agent System** built using LangGraph, wherein three autonomous agents — Planner, Executor, and Verifier — collaborate in a structured feedback loop to research, execute, and quality-assure a given goal. The system is deployed as a fully automated CI/CD pipeline via GitHub Actions, demonstrating production-grade orchestration of AI agents.

## Objective

The primary objective of this project is to design and implement an AI-driven multi-agent workflow capable of accepting a high-level goal (e.g., *"Research and summarise the top 3 trends in agriculture for 2025"*), autonomously decomposing it into sub-tasks, executing those tasks with real-time web data, and iteratively verifying the quality of the output until an acceptable standard is met — all without human intervention.

## Technologies Used

The system is built upon the following technology stack: **LangGraph** for stateful graph-based agent orchestration, **LangChain Core** for prompt abstractions and message schemas, **Groq API** with the **Llama-3.1-8B-Instant** model for low-latency LLM inference, **DuckDuckGo Search** (via LangChain Community Tools and the `ddgs` package) for real-time web search augmentation, and **GitHub Actions** for automated CI/CD deployment. The implementation is written in Python 3.12 and managed through a `requirements.txt` dependency file.

## Agent Architecture

### The Planner Agent

The Planner agent serves as the entry point of the workflow. It receives the user-defined goal and instructs the LLM to decompose it into at most five concrete, actionable sub-tasks. The agent enforces a strict JSON-only response format to ensure reliable parsing. In the event of a malformed response, a fallback mechanism treats the entire output as a single task, thereby guaranteeing forward progress regardless of LLM output variability.

### The Executor Agent

The Executor agent iterates over each sub-task produced by the Planner and completes it using the LLM, augmented with live web search context from DuckDuckGo. For every task, the agent issues a search query (truncated to 100 characters) and injects the top results (up to 800 characters) into the LLM prompt as supplementary context. Critically, if the Verifier has previously rejected the output, the Executor receives the critique as additional context, enabling it to refine its responses in subsequent iterations.

### The Verifier Agent (LLM-as-a-Judge)

The Verifier agent implements the LLM-as-a-Judge paradigm. It evaluates the combined results against the original goal using a structured scoring rubric comprising three dimensions: Completeness (0–0.4), Accuracy (0–0.3), and Clarity (0–0.3), yielding a composite score between 0.0 and 1.0. The agent returns a JSON verdict containing the score, an approval flag, and a written critique. A safety cap of three iterations prevents infinite feedback loops, after which the system force-approves the results.

## LangGraph Workflow and Agent Communication

The three agents are orchestrated as nodes in a LangGraph `StateGraph`. A shared `AgentState` typed dictionary — containing fields for the goal, tasks, results, critique, approval status, and iteration count — flows through the graph as the single source of truth. The edges are defined as Planner → Executor → Verifier, with a conditional edge from the Verifier that either routes back to the Executor (if rejected) or terminates the graph (if approved). This architecture ensures that agents communicate exclusively through the shared state, maintaining a clean separation of concerns.

## Role of DuckDuckGo Search and Groq Llama-3.1-8B

DuckDuckGo Search provides the Executor agent with real-time web data, ensuring that the system produces current and factually grounded responses rather than relying solely on the LLM's training data. The Groq-hosted Llama-3.1-8B-Instant model was selected for its exceptionally low inference latency, which is essential for a multi-agent system where each iteration involves multiple sequential LLM calls across three agents.

## GitHub Actions CI/CD Deployment

The system is deployed via a GitHub Actions workflow (`run-agent.yml`) that triggers on every push to the `main` branch and supports manual dispatch. The workflow provisions an Ubuntu runner, installs Python 3.12, resolves dependencies from `requirements.txt`, and executes the agent script with the `GROQ_API_KEY` injected securely from GitHub Secrets. This ensures fully reproducible, automated execution in a clean environment.

## Advantages of the Multi-Agent Architecture

The multi-agent design offers several advantages over single-shot prompting. First, task decomposition enables the LLM to focus on narrower, well-defined sub-problems, improving output quality. Second, the Verifier introduces an automated quality gate that catches incomplete or inaccurate responses. Third, the iterative feedback loop mirrors human review processes, allowing progressive refinement. Finally, the modular architecture permits each agent to be independently modified, tested, or replaced without affecting the others.

## Conclusion

This project demonstrates a practical implementation of a multi-agent AI system that combines task planning, web-augmented execution, and automated quality verification in a single, cohesive pipeline. By leveraging LangGraph for orchestration, Groq for high-speed inference, and DuckDuckGo for real-time data retrieval, the system achieves a level of autonomy and output quality that surpasses conventional single-agent approaches. Its deployment via GitHub Actions further establishes it as a production-ready, reproducible workflow suitable for real-world AI applications.

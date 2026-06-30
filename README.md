# Planner Multi-Agent System

🤖 An autonomous AI research pipeline built with **LangGraph** that orchestrates three specialized agents — **Planner**, **Executor**, and **Verifier** — to break down, research, and verify any goal.

![Agent Workflow Flowchart](agent_flowchart.png)

---

## Architecture

```
User Goal
   ↓
┌──────────────────┐
│  Planner Agent   │  → Breaks goal into up to 5 tasks
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Executor Agent  │  → Executes each task + DuckDuckGo search
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Verifier Agent  │  → Scores on Completeness, Accuracy, Clarity
└────────┬─────────┘
         ↓
   Approved? → Done
   Rejected? → Back to Executor (max 3 iterations)
```

### Project Structure

```
planner-multi-agent/
├── agents/
│   ├── __init__.py       # Package exports
│   ├── state.py          # AgentState schema + LLM/search init
│   ├── planner.py        # Planner agent
│   ├── executor.py       # Executor agent
│   ├── verifier.py       # Verifier agent (LLM-as-a-Judge)
│   └── workflow.py       # LangGraph builder + runner
├── .github/
│   └── workflows/
│       └── run-agent.yml # GitHub Actions CI/CD
├── app.py                # Streamlit UI
├── planner_multi_agent.py # Original standalone script
├── requirements.txt
├── REPORT.md
├── README.md
└── .env                  # GROQ_API_KEY (not committed)
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **LangGraph** | Stateful multi-agent orchestration |
| **LangChain Core** | Prompt/message abstractions |
| **Groq (Llama-3.1-8B-Instant)** | Fast LLM inference |
| **DuckDuckGo Search** | Real-time web search |
| **Streamlit** | Interactive web UI |
| **GitHub Actions** | CI/CD pipeline |
| **Python 3.12** | Runtime |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/Dixit-Anmol/planner-multi-agent.git
cd planner-multi-agent

# Install dependencies
pip install -r requirements.txt
```

### Set up your API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key from [console.groq.com/keys](https://console.groq.com/keys).

---

## Running Locally

### Streamlit App (Recommended)

```bash
streamlit run app.py
```

Opens a browser with the full interactive UI where you can enter goals, run the agents, and see results.

### CLI Mode

```bash
python planner_multi_agent.py
```

Runs the agents in the terminal with a default goal.

---

## GitHub Actions

The CI/CD pipeline (`.github/workflows/run-agent.yml`) runs on every push to `main` and supports manual dispatch.

**What it does:**
1. Sets up Python 3.12
2. Installs all dependencies
3. Verifies Streamlit app imports successfully
4. Runs the standalone agent script

**Required:** Add `GROQ_API_KEY` as a repository secret in Settings → Secrets → Actions.

---

## Screenshots

> *Add screenshots of the running Streamlit app here after deployment.*

| View | Description |
|---|---|
| Main page | Goal input + Run button |
| Results | Tasks, executor output, verifier status |
| Sidebar | Tech stack, workflow diagram, metrics |

---

## Report

See [REPORT.md](REPORT.md) for a detailed technical write-up of the multi-agent architecture.

---

## License

This project is part of an AI training assignment.

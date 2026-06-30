"""
Planner Multi-Agent System — Streamlit Application
====================================================
A professional UI for the LangGraph-based Planner → Executor → Verifier
multi-agent workflow.
"""

import streamlit as st
from agents.workflow import run_workflow

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Planner Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0;
    }
    .agent-header {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.3rem 0;
    }
    .workflow-box {
        background: #1e1e2e;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.85rem;
        line-height: 1.8;
        color: #e2e8f0;
    }
    .stExpander {
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Project Info")
    st.markdown(
        "A **LangGraph** multi-agent system where three AI agents collaborate "
        "to research any topic autonomously."
    )

    st.divider()

    st.markdown("### 🛠️ Technologies")
    tech_items = [
        ("🧠", "LangGraph", "Agent orchestration"),
        ("⚡", "Groq Llama-3.1-8B", "LLM inference"),
        ("🔍", "DuckDuckGo Search", "Live web data"),
        ("🔗", "LangChain Core", "Prompt framework"),
        ("🐍", "Python 3.12", "Runtime"),
        ("🚀", "GitHub Actions", "CI/CD"),
    ]
    for icon, name, desc in tech_items:
        st.markdown(f"{icon} **{name}** — {desc}")

    st.divider()

    st.markdown("### 📊 Workflow")
    st.markdown("""
<div class="workflow-box">
  👤 User Goal<br>
  &nbsp;&nbsp;&nbsp;↓<br>
  📋 <b>Planner Agent</b><br>
  &nbsp;&nbsp;&nbsp;↓ (up to 5 tasks)<br>
  ⚙️ <b>Executor Agent</b> + 🔍 Search<br>
  &nbsp;&nbsp;&nbsp;↓<br>
  ✅ <b>Verifier Agent</b> (LLM Judge)<br>
  &nbsp;&nbsp;&nbsp;↓<br>
  Approved? → 🏁 <b>Done</b><br>
  Rejected? → ↩️ Back to Executor
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Show iteration count after a run
    if "final_state" in st.session_state:
        fs = st.session_state["final_state"]
        col1, col2 = st.columns(2)
        col1.metric("Iterations", fs["iterations"])
        col2.metric("Status", "✅ Approved" if fs["approved"] else "❌ Rejected")


# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Planner Multi-Agent System</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">'
    'An autonomous AI pipeline that plans, executes, and verifies research goals '
    'using three specialized agents.'
    '</p>',
    unsafe_allow_html=True,
)

st.markdown("")

# ─── Input Section ────────────────────────────────────────────────────────────
with st.container():
    goal = st.text_area(
        "🎯 Enter your research goal",
        value="Research and summarise the top 3 trends in agriculture for 2025",
        height=100,
        placeholder="e.g., Research the latest breakthroughs in quantum computing...",
    )

    run_btn = st.button("🚀 Run Multi-Agent", type="primary", use_container_width=True)

# ─── Execution ────────────────────────────────────────────────────────────────
if run_btn:
    if not goal.strip():
        st.error("⚠️ Please enter a goal before running.")
        st.stop()

    try:
        with st.spinner("🔄 Agents are working... This may take 1–2 minutes."):
            final_state = run_workflow(goal.strip())
            st.session_state["final_state"] = final_state

    except RuntimeError as e:
        st.error(f"❌ Configuration Error: {e}")
        st.info("💡 Make sure `GROQ_API_KEY` is set in your `.env` file.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        st.stop()

    # ─── Results Display ──────────────────────────────────────────────────
    st.divider()

    # Verification Status
    if final_state["approved"]:
        st.success(
            f"✅ **Verified & Approved** after {final_state['iterations']} "
            f"iteration(s)"
        )
    else:
        st.warning(
            f"⚠️ **Not fully approved** after {final_state['iterations']} "
            f"iteration(s)"
        )

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Tasks Generated", len(final_state["tasks"]))
    col2.metric("🔄 Iterations", final_state["iterations"])
    col3.metric("✅ Approved", "Yes" if final_state["approved"] else "No")

    st.markdown("")

    # ─── Planner Output ──────────────────────────────────────────────────
    st.markdown("### 📋 Planner — Generated Tasks")
    for i, task in enumerate(final_state["tasks"], 1):
        st.markdown(f"**{i}.** {task}")

    st.markdown("")

    # ─── Executor Output ─────────────────────────────────────────────────
    st.markdown("### ⚙️ Executor — Task Results")
    for i, (task, result) in enumerate(
        zip(final_state["tasks"], final_state["results"]), 1
    ):
        with st.expander(f"Task {i}: {task[:80]}{'...' if len(task) > 80 else ''}"):
            st.markdown(result)

    st.markdown("")

    # ─── Verifier Output ─────────────────────────────────────────────────
    st.markdown("### ✅ Verifier — Quality Assessment")

    if final_state["critique"]:
        st.warning(f"**Critique:** {final_state['critique']}")
    else:
        st.success("No critique — results met quality standards.")

    st.markdown("")

    # ─── Final Combined Response ─────────────────────────────────────────
    st.markdown("### 📝 Final Combined Response")
    with st.container():
        combined = "\n\n---\n\n".join(
            f"**Task {i}: {t}**\n\n{r}"
            for i, (t, r) in enumerate(
                zip(final_state["tasks"], final_state["results"]), 1
            )
        )
        st.markdown(combined)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("")
st.divider()
st.markdown(
    "<div style='text-align:center; color:#64748b; font-size:0.85rem;'>"
    "Built with LangGraph · Groq · LangChain · Streamlit"
    "</div>",
    unsafe_allow_html=True,
)

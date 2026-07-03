"""
Planner Multi-Agent System — Premium Streamlit UI
===================================================
A polished, consumer-facing AI search and research experience.
"""

import streamlit as st
import time
from styles import get_css
from components import (
    render_navbar,
    render_hero,
    render_progress_view,
    render_disclaimer,
    render_footer,
)
from agents.workflow import run_workflow_generator

# ─── Page & Style Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Planner Multi-Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject Premium Styles
st.markdown(get_css(), unsafe_allow_html=True)

# Navigation Bar
render_navbar()

# ─── Query Param Handling ─────────────────────────────────────────────────────
# If user clicked a suggestion chip, prefill the query
query_params = st.query_params
default_query = query_params.get("query", "")

# ─── Hero Section ─────────────────────────────────────────────────────────────
render_hero()

# ─── Input Container ──────────────────────────────────────────────────────────
st.markdown('<div class="input-card fade-in delay-1">', unsafe_allow_html=True)
st.markdown('<div class="input-label">What would you like to know?</div>', unsafe_allow_html=True)

# Goal Input Field (using text_input so pressing Enter triggers search)
user_goal = st.text_input(
    label="Goal Input Area",
    value=default_query,
    placeholder="Ask anything...",
    label_visibility="collapsed"
)

# Columns to align button right
col_left, col_right = st.columns([5, 1.2])
with col_right:
    submit_btn = st.button("Get Answer", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Track if we should run the search
if "last_run_query" not in st.session_state:
    st.session_state["last_run_query"] = ""

should_run = False
query_to_run = ""

if submit_btn and user_goal.strip():
    query_to_run = user_goal.strip()
    should_run = True
elif user_goal.strip() and user_goal.strip() != st.session_state["last_run_query"]:
    query_to_run = user_goal.strip()
    should_run = True
elif default_query.strip() and not st.session_state["last_run_query"]:
    query_to_run = default_query.strip()
    should_run = True

# ─── Main Execution Workflow ──────────────────────────────────────────────────
if should_run:
    st.session_state["last_run_query"] = query_to_run
    st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
    
    # Progress placeholders
    progress_box = st.empty()
    
    try:
        final_state = None
        # Stream workflow generator
        for status_msg, progress_pct, state_so_far in run_workflow_generator(query_to_run):
            with progress_box.container():
                # Map progress status index
                if "Understanding" in status_msg:
                    step_idx = 1
                elif "Planning" in status_msg:
                    step_idx = 1
                elif "Researching" in status_msg:
                    step_idx = 2
                elif "Generating" in status_msg:
                    step_idx = 2
                elif "Verifying" in status_msg:
                    step_idx = 3
                else:
                    step_idx = 4
                render_progress_view(step_idx)
            # Small delay for smooth UI update
            time.sleep(0.3)
            
            if state_so_far:
                final_state = state_so_far
                
        # Clear progress bar
        progress_box.empty()
        
        # Display Results
        if final_state:
            # HTML Anchor & JS scroll to response
            st.markdown(
                """
                <div id="response-section"></div>
                <script>
                    setTimeout(function() {
                        var el = window.parent.document.getElementById("response-section");
                        if (el) {
                            el.scrollIntoView({behavior: "smooth", block: "start"});
                        }
                    }, 100);
                </script>
                """,
                unsafe_allow_html=True
            )

            st.markdown('<div class="result-card fade-in">', unsafe_allow_html=True)
            
            # Header actions: Title, Download & Share
            st.markdown(
                """
                <div class="result-header">
                    <div class="result-title">
                        <span class="result-title-icon">✨</span>
                        Final Answer
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Action Buttons Row
            btn_col1, btn_col2, btn_col3 = st.columns([6, 1.2, 1.2])
            with btn_col2:
                combined_text = "\n\n".join(
                    f"### Task: {t}\n{r}" 
                    for t, r in zip(final_state["tasks"], final_state["results"])
                )
                st.download_button(
                    label="📥 Download",
                    data=combined_text,
                    file_name="research_results.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with btn_col3:
                if st.button("🔗 Share", use_container_width=True):
                    st.toast("Link copied to clipboard! (Simulated)")
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Extract summary if exists
            summary = ""
            if len(final_state["results"]) > 0:
                summary = final_state["results"][-1]
                
            # Render Summary Highlight
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-label">Key Summary</div>
                    <div class="summary-text">{summary[:400]}...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Display detailed numbered sections
            st.markdown('<div class="response-body">', unsafe_allow_html=True)
            for i, (task, result) in enumerate(zip(final_state["tasks"], final_state["results"]), 1):
                st.markdown(
                    f"""
                    <div class="section-block">
                        <div class="section-number">{i:02d}</div>
                        <div class="section-content">
                            <h3>{task}</h3>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quality assessment badge
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            if final_state["approved"]:
                st.success(f"Verified & Approved by AI quality guardrails (Score: Met standard | Iterations: {final_state['iterations']}).")
            else:
                st.warning(f"Response compiled after maximum refinement cycles ({final_state['iterations']} iterations).")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        progress_box.empty()
        st.error(f"An unexpected error occurred during processing: {e}")
        st.info("Please verify your GROQ_API_KEY environment variable is configured correctly.")

# Footer & Disclaimer
render_disclaimer()
render_footer()

"""
Planner Multi-Agent System — Premium Streamlit UI
===================================================
A polished, consumer-facing AI search and research experience.
Token-optimized for Groq free-tier reliability.
"""

import streamlit as st
import time
from styles import get_css
from components import (
    render_navbar,
    render_hero,
    render_suggestion_chips,
    render_progress_view,
    render_final_response,
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

# ─── Session State Initialization ─────────────────────────────────────────────
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""
if "last_run_query" not in st.session_state:
    st.session_state["last_run_query"] = ""
if "final_response" not in st.session_state:
    st.session_state["final_response"] = None
if "is_running" not in st.session_state:
    st.session_state["is_running"] = False

# ─── Query Param Handling ─────────────────────────────────────────────────────
# If user clicked a suggestion chip, ONLY prefill the text box — do NOT auto-execute
query_params = st.query_params
default_query = query_params.get("query", "")
if default_query:
    st.session_state["search_query"] = default_query
    st.query_params.clear()

# ─── Hero Section ─────────────────────────────────────────────────────────────
render_hero()

# ─── Input Container ──────────────────────────────────────────────────────────
st.markdown('<div class="input-card fade-in delay-1">', unsafe_allow_html=True)
st.markdown('<div class="input-label">What would you like to know?</div>', unsafe_allow_html=True)

# Goal Input Field
user_goal = st.text_input(
    label="Goal Input Area",
    key="search_query",
    placeholder="Ask anything...",
    label_visibility="collapsed"
)

# Columns to align button right
col_left, col_right = st.columns([5, 1.2])
with col_right:
    submit_btn = st.button("Get Answer", type="primary", use_container_width=True)

# Render Suggestion Chips
render_suggestion_chips()
st.markdown('</div>', unsafe_allow_html=True)

# ─── Determine if workflow should run ─────────────────────────────────────────
# ONLY run when the "Get Answer" button is clicked — never on text change or rerun
should_run = False
query_to_run = ""

if submit_btn and user_goal.strip():
    query_to_run = user_goal.strip()
    # Only run if it's a new query OR user explicitly clicked the button again
    if query_to_run != st.session_state["last_run_query"] or submit_btn:
        should_run = True

# ─── Main Execution Workflow ──────────────────────────────────────────────────
if should_run and not st.session_state["is_running"]:
    st.session_state["is_running"] = True
    st.session_state["last_run_query"] = query_to_run
    st.session_state["final_response"] = None  # Clear previous results
    st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
    
    progress_box = st.empty()
    
    try:
        final_state = None
        for status_msg, progress_pct, state_so_far in run_workflow_generator(query_to_run):
            with progress_box.container():
                if "Understanding" in status_msg or "Planning" in status_msg:
                    step_idx = 1
                elif "Researching" in status_msg or "Generating" in status_msg:
                    step_idx = 2
                elif "Verifying" in status_msg:
                    step_idx = 3
                else:
                    step_idx = 4
                render_progress_view(step_idx)
            time.sleep(0.3)
            
            if state_so_far:
                final_state = state_so_far
                
        progress_box.empty()
        
        if final_state:
            # Cache the result in session state
            st.session_state["final_response"] = final_state
            render_final_response(final_state)
            
    except Exception as e:
        progress_box.empty()
        error_msg = str(e)
        
        # User-friendly error messages
        if "429" in error_msg or "rate_limit" in error_msg.lower() or "rate limit" in error_msg.lower():
            st.warning(
                "⏳ **You're making requests a little too quickly.**\n\n"
                "The free-tier API has a token limit per minute. "
                "Please wait 20–30 seconds and try again."
            )
        elif "401" in error_msg or "auth" in error_msg.lower() or "api_key" in error_msg.lower():
            st.error(
                "🔑 **Authentication Error**\n\n"
                "Your API key appears to be invalid or missing. "
                "Please check your `GROQ_API_KEY` environment variable."
            )
        elif "connection" in error_msg.lower() or "network" in error_msg.lower() or "timeout" in error_msg.lower():
            st.error(
                "🌐 **Network Error**\n\n"
                "Could not connect to the AI service. "
                "Please check your internet connection and try again."
            )
        else:
            st.error(f"❌ **An unexpected error occurred:**\n\n{error_msg}")
    finally:
        st.session_state["is_running"] = False

# ─── Display Cached Results on Rerun ──────────────────────────────────────────
elif st.session_state["final_response"] and not should_run:
    st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
    render_final_response(st.session_state["final_response"])

# Footer & Disclaimer
render_disclaimer()
render_footer()

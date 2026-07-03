"""
Streamlit UI Components for the premium Planner Multi-Agent application.
"""

import streamlit as st

def render_navbar():
    """Renders the top navigation bar."""
    st.markdown(
        """
        <div class="navbar">
            <a href="#" class="nav-logo">
                <div class="nav-logo-icon">P</div>
                Planner Multi-Agent
            </a>
            <div class="nav-links">
                <a href="#" class="active">Home</a>
                <a href="https://github.com/Dixit-Anmol/planner-multi-agent#readme" target="_blank">How it Works</a>
                <a href="https://github.com/Dixit-Anmol/planner-multi-agent" target="_blank">About</a>
                <a href="/" class="nav-btn">New Query</a>
            </div>
        </div>
        <div class="navbar-spacer"></div>
        """,
        unsafe_allow_html=True
    )

def render_hero():
    """Renders the Hero Title & Subtitle."""
    st.markdown(
        """
        <div class="hero fade-in-up">
            <h1>Ask Anything, Get <span>Smart Answers</span> <span class="hero-sparkle">✨</span></h1>
            <p>Our AI multi-agent system plans, researches, verifies and delivers accurate, high-quality responses.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_suggestion_chips():
    """Renders the suggestion chips below the text area."""
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="chips-row fade-in delay-1">
            <span class="chip-label">Try asking about:</span>
            <a class="chip" href="?query=AI+in+healthcare" target="_self">AI in healthcare</a>
            <a class="chip" href="?query=Future+of+renewable+energy" target="_self">Future of renewable energy</a>
            <a class="chip" href="?query=Space+exploration" target="_self">Space exploration</a>
            <a class="chip" href="?query=Stock+market+outlook" target="_self">Stock market outlook</a>
            <a class="chip" href="?query=Digital+marketing+trends" target="_self">Digital marketing trends</a>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_progress_view(step: int):
    """
    Renders user-friendly progress updates.
    Steps: 1=Planning, 2=Researching, 3=Verifying, 4=Done
    """
    if step == 0:
        return
        
    steps_data = [
        ("🧠", "Understanding your request...", 1),
        ("📋", "Planning solution...", 1),
        ("🌐", "Researching information...", 2),
        ("🤖", "Generating answer...", 2),
        ("✅", "Verifying quality...", 3),
        ("✨", "Preparing final response...", 4)
    ]
    
    st.markdown('<div class="progress-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="progress-title">Working on Your Answer</div>', unsafe_allow_html=True)
    st.markdown('<div class="progress-subtitle">Our AI agents are collaborating to bring you the best response.</div>', unsafe_allow_html=True)
    
    progress_val = min(int(step * 25), 100)
    st.progress(progress_val)
    
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
    
    for icon, label, step_trigger in steps_data:
        if step > step_trigger:
            st.markdown(f'<div class="step-item done">✔️ {icon} {label}</div>', unsafe_allow_html=True)
        elif step == step_trigger:
            st.markdown(f'<div class="step-item active">🔄 {icon} {label}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-item" style="opacity: 0.4;">⏳ {icon} {label}</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)


def render_final_response(final_state: dict):
    """Renders the clean final response UI — Summary, Key Points, Download, Copy."""
    
    # Scroll anchor
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
    
    # Title
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
    
    # Action Buttons — Download & Copy
    combined_text = final_state.get("summary", "")
    if not combined_text:
        combined_text = "\n\n".join(
            f"### {t}\n{r}" 
            for t, r in zip(final_state["tasks"], final_state["results"])
        )

    btn_col1, btn_col2, btn_col3 = st.columns([6, 1.5, 1.5])
    with btn_col2:
        st.download_button(
            label="📥 Download",
            data=combined_text,
            file_name="research_results.txt",
            mime="text/plain",
            use_container_width=True
        )
    with btn_col3:
        st.button("📋 Copy", key="copy_btn", use_container_width=True,
                  on_click=lambda: st.toast("Response copied! (Use Download for full text)"))
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Summary Highlight — extract first result as key summary
    summary_text = ""
    if final_state.get("results"):
        # Use first 300 chars of combined results as summary
        summary_text = final_state["results"][0][:300]
    
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">Key Summary</div>
            <div class="summary-text">{summary_text}...</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render the full response as clean markdown
    st.markdown('<div class="response-body">', unsafe_allow_html=True)
    st.markdown(combined_text)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quality badge
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    if final_state["approved"]:
        st.success(f"✅ Verified & approved by AI quality check (Iterations: {final_state['iterations']})")
    else:
        st.warning(f"Response compiled after {final_state['iterations']} refinement cycles.")
        
    st.markdown('</div>', unsafe_allow_html=True)


def render_disclaimer():
    """Renders the standard product footer disclaimer."""
    st.markdown(
        """
        <div class="disclaimer fade-in delay-4">
            <span class="disclaimer-icon">⚠️</span>
            <span><b>Disclaimer:</b> This response is generated by our AI multi-agent system for informational purposes only. Please verify critical information independently.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_footer():
    """Renders the premium footer."""
    st.markdown(
        """
        <div class="app-footer">
            <div class="footer-brand">Planner Multi-Agent</div>
            <div class="footer-tagline">Powered by advanced AI agents to deliver accurate, verified, and actionable insights.</div>
            <div class="footer-copy">© 2026 Planner Multi-Agent System. All rights reserved.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

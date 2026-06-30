"""
Premium CSS styles for the Planner Multi-Agent Streamlit app.
"""


def get_css() -> str:
    return """
<style>
/* ═══════════════════════════════════════════════════════════════════
   RESET & GLOBALS
   ═══════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stSidebar"] {display: none;}
[data-testid="stSidebarCollapsedControl"] {display: none;}
.block-container {padding-top: 0 !important; max-width: 900px;}
.stApp {background-color: #FAFAFA; font-family: 'Inter', sans-serif;}

/* ═══════════════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(24px);}
    to   {opacity: 1; transform: translateY(0);}
}
@keyframes fadeIn {
    from {opacity: 0;}
    to   {opacity: 1;}
}
@keyframes shimmer {
    0%   {background-position: -200% 0;}
    100% {background-position: 200% 0;}
}
@keyframes pulse {
    0%, 100% {opacity: 1;}
    50%      {opacity: 0.5;}
}
.fade-in-up {animation: fadeInUp 0.6s ease-out forwards;}
.fade-in    {animation: fadeIn 0.5s ease-out forwards;}
.delay-1    {animation-delay: 0.1s; opacity: 0;}
.delay-2    {animation-delay: 0.2s; opacity: 0;}
.delay-3    {animation-delay: 0.35s; opacity: 0;}
.delay-4    {animation-delay: 0.5s; opacity: 0;}

/* ═══════════════════════════════════════════════════════════════════
   NAVBAR
   ═══════════════════════════════════════════════════════════════════ */
.navbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid #f0f0f0;
    padding: 0.7rem 2rem;
    display: flex; align-items: center; justify-content: space-between;
}
.nav-logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.15rem; font-weight: 700; color: #1a1a1a;
    text-decoration: none;
}
.nav-logo-icon {
    width: 32px; height: 32px; border-radius: 8px;
    background: linear-gradient(135deg, #F97316, #FB923C);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1rem; font-weight: 700;
}
.nav-links {
    display: flex; gap: 2rem; align-items: center;
}
.nav-links a {
    text-decoration: none; color: #64748b; font-size: 0.9rem;
    font-weight: 500; transition: color 0.2s;
}
.nav-links a:hover, .nav-links a.active {color: #F97316;}
.nav-btn {
    background: linear-gradient(135deg, #F97316, #FB923C);
    color: white !important; border: none; padding: 0.5rem 1.2rem;
    border-radius: 10px; font-size: 0.85rem; font-weight: 600;
    cursor: pointer; text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(249,115,22,0.25);
}
.nav-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(249,115,22,0.35);
}
.navbar-spacer {height: 70px;}

/* ═══════════════════════════════════════════════════════════════════
   HERO
   ═══════════════════════════════════════════════════════════════════ */
.hero {
    text-align: center; padding: 3rem 1rem 1.5rem;
}
.hero h1 {
    font-size: 2.6rem; font-weight: 800; color: #1a1a1a;
    margin-bottom: 0.5rem; line-height: 1.2;
}
.hero h1 span {
    background: linear-gradient(135deg, #F97316, #FB923C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sparkle {
    display: inline-block; font-size: 1.5rem;
    animation: pulse 2s ease-in-out infinite;
}
.hero p {
    font-size: 1.05rem; color: #64748b; max-width: 600px;
    margin: 0 auto; line-height: 1.6; font-weight: 400;
}

/* ═══════════════════════════════════════════════════════════════════
   INPUT CARD
   ═══════════════════════════════════════════════════════════════════ */
.input-card {
    background: #fff; border-radius: 18px; padding: 1.8rem 2rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    border: 1px solid #f0f0f0;
    margin: 0 auto; max-width: 780px;
}
.input-label {
    font-size: 0.95rem; font-weight: 600; color: #F97316;
    margin-bottom: 0.7rem;
}
/* Override Streamlit text area */
.input-card .stTextArea textarea {
    border: 1.5px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    resize: none !important;
    transition: border-color 0.2s !important;
    background: #FAFAFA !important;
}
.input-card .stTextArea textarea:focus {
    border-color: #F97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.1) !important;
}

/* ═══════════════════════════════════════════════════════════════════
   SUGGESTION CHIPS
   ═══════════════════════════════════════════════════════════════════ */
.chips-row {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin-top: 1rem; justify-content: flex-start;
}
.chip-label {
    font-size: 0.8rem; color: #94a3b8; font-weight: 500;
    margin-right: 0.3rem; display: flex; align-items: center;
}
.chip {
    display: inline-flex; align-items: center;
    padding: 0.4rem 0.9rem; border-radius: 20px;
    border: 1px solid #e2e8f0; background: #fff;
    font-size: 0.82rem; color: #475569; font-weight: 500;
    cursor: pointer; transition: all 0.2s;
    text-decoration: none;
}
.chip:hover {
    border-color: #F97316; color: #F97316;
    background: #FFF7ED;
}

/* ═══════════════════════════════════════════════════════════════════
   ORANGE PRIMARY BUTTON
   ═══════════════════════════════════════════════════════════════════ */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #F97316, #FB923C) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 4px 14px rgba(249,115,22,0.3) !important;
    transition: all 0.25s ease !important;
    min-height: 48px !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(249,115,22,0.4) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) !important;
}
/* Secondary buttons */
div[data-testid="stButton"] > button[kind="secondary"] {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    background: white !important;
    color: #475569 !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: #F97316 !important;
    color: #F97316 !important;
}

/* ═══════════════════════════════════════════════════════════════════
   PROGRESS / PROCESSING
   ═══════════════════════════════════════════════════════════════════ */
.progress-container {
    max-width: 600px; margin: 2rem auto; text-align: center;
}
.progress-title {
    font-size: 1.3rem; font-weight: 700; color: #1a1a1a;
    margin-bottom: 0.3rem;
}
.progress-subtitle {
    font-size: 0.9rem; color: #94a3b8; margin-bottom: 1.5rem;
}
.step-item {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.6rem 1rem; margin: 0.4rem 0;
    border-radius: 12px; font-size: 0.92rem;
    font-weight: 500; color: #475569;
    animation: fadeInUp 0.4s ease-out forwards;
}
.step-item.active {
    background: #FFF7ED; color: #F97316; font-weight: 600;
}
.step-item.done {
    color: #22C55E;
}
/* Override Streamlit progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #F97316, #FB923C) !important;
    border-radius: 8px !important;
}
.stProgress > div {
    background: #f1f5f9 !important;
    border-radius: 8px !important;
}

/* ═══════════════════════════════════════════════════════════════════
   RESULT CARD
   ═══════════════════════════════════════════════════════════════════ */
.result-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;
}
.result-title {
    display: flex; align-items: center; gap: 0.5rem;
    font-size: 1.5rem; font-weight: 700; color: #1a1a1a;
}
.result-title-icon {
    font-size: 1.3rem;
    background: linear-gradient(135deg, #F97316, #FB923C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.result-actions {
    display: flex; gap: 0.5rem;
}
.result-action-btn {
    display: inline-flex; align-items: center; gap: 0.35rem;
    padding: 0.4rem 1rem; border-radius: 8px;
    border: 1px solid #e2e8f0; background: #fff;
    font-size: 0.82rem; color: #475569; font-weight: 500;
    cursor: pointer; transition: all 0.2s; text-decoration: none;
}
.result-action-btn:hover {
    border-color: #F97316; color: #F97316;
}
.result-action-btn.share {color: #F97316; border-color: #FDBA74;}
.result-card {
    background: #fff; border-radius: 18px;
    padding: 2rem; box-shadow: 0 2px 20px rgba(0,0,0,0.05);
    border: 1px solid #f0f0f0;
    animation: fadeInUp 0.5s ease-out forwards;
    margin-bottom: 1.5rem;
}

/* Summary highlight */
.summary-card {
    background: linear-gradient(135deg, #FFF7ED, #FFEDD5);
    border-left: 4px solid #F97316;
    border-radius: 12px; padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.summary-label {
    font-size: 0.82rem; font-weight: 700; color: #F97316;
    text-transform: uppercase; letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}
.summary-text {
    font-size: 0.95rem; color: #44403c; line-height: 1.65;
}

/* Numbered sections */
.section-block {
    display: flex; gap: 1.2rem; padding: 1.2rem 0;
    border-top: 1px solid #f5f5f5;
    animation: fadeInUp 0.5s ease-out forwards;
}
.section-number {
    flex-shrink: 0; width: 42px; height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #FFF7ED, #FFEDD5);
    border: 2px solid #FDBA74;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; color: #F97316;
    margin-top: 0.2rem;
}
.section-content {
    flex: 1;
}
.section-content h3 {
    font-size: 1.05rem; font-weight: 700; color: #1a1a1a;
    margin: 0 0 0.5rem 0;
}
.section-content p, .section-content li {
    font-size: 0.92rem; color: #475569; line-height: 1.65;
}
.section-content ul {
    padding-left: 1.2rem; margin: 0.3rem 0;
}

/* ═══════════════════════════════════════════════════════════════════
   DISCLAIMER
   ═══════════════════════════════════════════════════════════════════ */
.disclaimer {
    display: flex; align-items: center; gap: 0.5rem;
    background: #FEF2F2; border: 1px solid #FECACA;
    border-radius: 12px; padding: 0.8rem 1.2rem;
    font-size: 0.82rem; color: #991B1B;
    margin: 1rem 0 1.5rem;
}
.disclaimer-icon {
    font-size: 1rem; flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════════════════════ */
.app-footer {
    text-align: center; padding: 2rem 1rem;
    border-top: 1px solid #f0f0f0;
    margin-top: 2rem;
}
.footer-brand {
    font-size: 1rem; font-weight: 700; color: #1a1a1a;
    margin-bottom: 0.25rem;
}
.footer-tagline {
    font-size: 0.82rem; color: #94a3b8; margin-bottom: 1rem;
}
.footer-copy {
    font-size: 0.78rem; color: #cbd5e1;
}

/* ═══════════════════════════════════════════════════════════════════
   RESPONSE MARKDOWN OVERRIDES
   ═══════════════════════════════════════════════════════════════════ */
.response-body h1, .response-body h2, .response-body h3 {
    color: #1a1a1a; margin-top: 1.2rem;
}
.response-body h1 {font-size: 1.3rem; font-weight: 700;}
.response-body h2 {font-size: 1.15rem; font-weight: 700;}
.response-body h3 {font-size: 1.05rem; font-weight: 600;}
.response-body p {
    font-size: 0.93rem; color: #475569; line-height: 1.7;
}
.response-body ul, .response-body ol {
    padding-left: 1.3rem; color: #475569;
}
.response-body li {
    font-size: 0.93rem; line-height: 1.7; margin-bottom: 0.25rem;
}
.response-body strong {color: #1e293b;}
.response-body code {
    background: #f1f5f9; padding: 0.15rem 0.4rem;
    border-radius: 4px; font-size: 0.85rem; color: #e11d48;
}
.response-body pre {
    background: #1e293b; color: #e2e8f0;
    border-radius: 12px; padding: 1rem 1.2rem;
    overflow-x: auto; font-size: 0.85rem;
}
.response-body table {
    width: 100%; border-collapse: collapse; margin: 1rem 0;
}
.response-body th {
    background: #FFF7ED; color: #F97316; font-weight: 600;
    padding: 0.6rem 1rem; text-align: left; font-size: 0.85rem;
    border-bottom: 2px solid #FDBA74;
}
.response-body td {
    padding: 0.5rem 1rem; border-bottom: 1px solid #f1f5f9;
    font-size: 0.88rem; color: #475569;
}
.response-body blockquote {
    border-left: 3px solid #F97316; background: #FFF7ED;
    padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;
    margin: 1rem 0; color: #92400e; font-style: italic;
}

/* ═══════════════════════════════════════════════════════════════════
   MISC
   ═══════════════════════════════════════════════════════════════════ */
.spacer-sm {height: 0.5rem;}
.spacer-md {height: 1rem;}
.spacer-lg {height: 2rem;}
.divider {
    height: 1px; background: #f0f0f0;
    margin: 1.5rem 0; border: none;
}
</style>
"""

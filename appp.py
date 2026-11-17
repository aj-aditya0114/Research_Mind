import time
import streamlit as st

from pipeline import run_research_pipeline


# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(
    page_title="ResearchMind | AI Research Studio",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -------------------------------------------------------------------
# CUSTOM THEME — original charcoal + orange palette preserved
# -------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0a0a0f;
        --surface: #111116;
        --surface-2: #17171d;
        --orange: #ff8c32;
        --orange-2: #ff5a1a;
        --text: #f0ebe0;
        --muted: #a09890;
        --line: rgba(255,255,255,.075);
        --green: #50c878;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    .stApp {
        background:
            radial-gradient(ellipse 70% 42% at 12% -8%, rgba(255,140,50,.14), transparent 68%),
            radial-gradient(ellipse 55% 40% at 100% 90%, rgba(255,90,26,.075), transparent 65%),
            var(--bg);
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        max-width: 1320px;
        padding: 1.5rem 3rem 3.5rem;
    }

    /* Subtle background texture */
    .stApp:before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: .16;
        z-index: 0;
        background-image: linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
        background-size: 54px 54px;
        mask-image: linear-gradient(to bottom, black, transparent 85%);
    }

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: .35rem 0 1.2rem;
        border-bottom: 1px solid var(--line);
        margin-bottom: 2.2rem;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: .65rem;
        font-family: 'Syne', sans-serif;
        font-size: .95rem;
        font-weight: 800;
        letter-spacing: .02em;
    }
    .brand-mark {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        color: #15100c;
        background: linear-gradient(135deg, var(--orange), var(--orange-2));
        box-shadow: 0 0 22px rgba(255,140,50,.24);
    }
    .top-meta {
        color: #77716c;
        font: .66rem 'DM Mono', monospace;
        letter-spacing: .13em;
        text-transform: uppercase;
    }
    .live-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: .45rem;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 10px rgba(80,200,120,.75);
    }

    .hero {
        position: relative;
        text-align: center;
        padding: 2.1rem 0 2.25rem;
        animation: rise .7s ease both;
    }
    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: .55rem;
        padding: .42rem .8rem;
        border: 1px solid rgba(255,140,50,.22);
        border-radius: 999px;
        background: rgba(255,140,50,.055);
        color: var(--orange);
        font: .66rem 'DM Mono', monospace;
        letter-spacing: .18em;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: 1.15rem 0 .8rem;
        color: var(--text);
        font: 800 clamp(3rem, 7vw, 5.6rem)/.98 'Syne', sans-serif;
        letter-spacing: -.065em;
    }
    .hero h1 span {
        color: var(--orange);
        text-shadow: 0 0 42px rgba(255,140,50,.22);
    }
    .hero-sub {
        max-width: 610px;
        margin: 0 auto;
        color: var(--muted);
        font-size: 1rem;
        font-weight: 300;
        line-height: 1.75;
    }
    .hero-sub strong { color: #d7cfc5; font-weight: 500; }

    .section-kicker {
        color: var(--orange);
        font: .68rem 'DM Mono', monospace;
        letter-spacing: .17em;
        text-transform: uppercase;
        margin-bottom: .55rem;
    }
    .section-title {
        color: var(--text);
        font: 700 1.45rem 'Syne', sans-serif;
        letter-spacing: -.025em;
        margin: 0 0 .35rem;
    }
    .section-copy {
        color: #817a74;
        font-size: .84rem;
        margin-bottom: 1.2rem;
    }

    .input-shell {
        padding: 1.55rem 1.6rem 1.35rem;
        border: 1px solid rgba(255,140,50,.19);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.018));
        box-shadow: 0 18px 55px rgba(0,0,0,.2), inset 0 1px rgba(255,255,255,.035);
        backdrop-filter: blur(12px);
    }
    .stTextInput > label {
        color: var(--orange) !important;
        font: 500 .68rem 'DM Mono', monospace !important;
        letter-spacing: .16em !important;
        text-transform: uppercase !important;
        margin-bottom: .55rem !important;
    }
    .stTextInput > div > div > input {
        min-height: 3.15rem;
        color: var(--text) !important;
        background: rgba(255,255,255,.055) !important;
        border: 1px solid rgba(255,140,50,.22) !important;
        border-radius: 10px !important;
        font: 500 .96rem 'DM Sans', sans-serif !important;
        padding: .8rem 1rem !important;
        transition: border .2s ease, box-shadow .2s ease, background .2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--orange) !important;
        background: rgba(255,140,50,.045) !important;
        box-shadow: 0 0 0 3px rgba(255,140,50,.11), 0 0 25px rgba(255,140,50,.08) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #716b66 !important; }

    .stButton > button, .stDownloadButton > button {
        min-height: 2.9rem;
        border: 0 !important;
        border-radius: 10px !important;
        color: #17100b !important;
        background: linear-gradient(115deg, #ff9b43 0%, #ff7628 52%, #ff5a1a 100%) !important;
        font: 700 .88rem 'Syne', sans-serif !important;
        letter-spacing: .025em;
        box-shadow: 0 7px 24px rgba(255,112,35,.22), inset 0 1px rgba(255,255,255,.25) !important;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.07);
        box-shadow: 0 11px 32px rgba(255,112,35,.34) !important;
    }
    .stButton > button:active { transform: translateY(0); }
    .stButton > button:focus:not(:active) { box-shadow: 0 0 0 3px rgba(255,140,50,.2) !important; }

    .examples-label {
        margin: 1.35rem 0 .7rem;
        color: #6f6862;
        font: .65rem 'DM Mono', monospace;
        letter-spacing: .15em;
        text-transform: uppercase;
    }
    .chip-caption {
        color: #8e8780;
        font-size: .75rem;
        margin-top: .15rem;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="column"] {
        min-width: 0;
    }

    .pipeline-head {
        display: flex;
        align-items: end;
        justify-content: space-between;
        margin: .15rem 0 1rem;
    }
    .pipeline-count {
        color: #716b65;
        font: .65rem 'DM Mono', monospace;
        letter-spacing: .12em;
    }
    .step-card {
        position: relative;
        overflow: hidden;
        padding: 1.15rem 1.25rem 1.1rem 1.35rem;
        margin-bottom: .78rem;
        border: 1px solid rgba(255,255,255,.075);
        border-radius: 15px;
        background: linear-gradient(125deg, rgba(255,255,255,.045), rgba(255,255,255,.018));
        box-shadow: 0 9px 28px rgba(0,0,0,.13);
        transition: transform .22s ease, border-color .22s ease, background .22s ease;
        animation: rise .45s ease both;
    }
    .step-card:hover { transform: translateY(-2px); border-color: rgba(255,140,50,.22); }
    .step-card:before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 3px;
        background: rgba(255,255,255,.07);
    }
    .step-card.active {
        border-color: rgba(255,140,50,.42);
        background: linear-gradient(115deg, rgba(255,140,50,.09), rgba(255,255,255,.02));
        box-shadow: 0 0 28px rgba(255,140,50,.07);
    }
    .step-card.active:before { background: var(--orange); box-shadow: 0 0 15px var(--orange); }
    .step-card.done {
        border-color: rgba(80,200,120,.27);
        background: linear-gradient(115deg, rgba(80,200,120,.055), rgba(255,255,255,.018));
    }
    .step-card.done:before { background: var(--green); }
    .step-top {
        display: flex;
        align-items: center;
        gap: .72rem;
    }
    .step-num {
        color: var(--orange);
        font: 500 .68rem 'DM Mono', monospace;
        letter-spacing: .12em;
    }
    .step-title {
        color: var(--text);
        font: 700 .94rem 'Syne', sans-serif;
    }
    .step-status {
        margin-left: auto;
        font: .61rem 'DM Mono', monospace;
        letter-spacing: .1em;
        white-space: nowrap;
    }
    .status-waiting { color: #625d59; }
    .status-running { color: var(--orange); }
    .status-done { color: var(--green); }
    .step-desc {
        margin: .62rem 0 0 2.1rem;
        color: #827b75;
        font-size: .76rem;
        line-height: 1.5;
    }
    .pulse {
        display: inline-block;
        width: 6px;
        height: 6px;
        margin-right: .35rem;
        border-radius: 50%;
        background: var(--orange);
        box-shadow: 0 0 0 0 rgba(255,140,50,.55);
        animation: pulse 1.5s infinite;
    }

    .divider {
        height: 1px;
        margin: 2.3rem 0 1.8rem;
        background: linear-gradient(90deg, transparent, rgba(255,140,50,.32), rgba(255,255,255,.07), transparent);
    }
    .result-heading {
        display: flex;
        align-items: center;
        gap: .8rem;
        margin: .2rem 0 1.2rem;
    }
    .result-heading h2 {
        margin: 0;
        color: var(--text);
        font: 700 1.5rem 'Syne', sans-serif;
    }
    .result-tag {
        padding: .28rem .58rem;
        border: 1px solid rgba(80,200,120,.22);
        border-radius: 999px;
        color: var(--green);
        background: rgba(80,200,120,.06);
        font: .6rem 'DM Mono', monospace;
        letter-spacing: .1em;
    }
    .report-shell, .feedback-shell {
        padding: 1.5rem 1.7rem;
        border: 1px solid rgba(255,140,50,.2);
        border-radius: 16px;
        background: rgba(255,255,255,.025);
        box-shadow: 0 14px 42px rgba(0,0,0,.14);
    }
    .feedback-shell {
        border-color: rgba(80,200,120,.2);
        margin-top: 1.2rem;
    }
    .panel-label {
        margin-bottom: 1rem;
        padding-bottom: .7rem;
        border-bottom: 1px solid rgba(255,140,50,.15);
        color: var(--orange);
        font: .66rem 'DM Mono', monospace;
        letter-spacing: .17em;
        text-transform: uppercase;
    }
    .feedback-shell .panel-label {
        color: var(--green);
        border-color: rgba(80,200,120,.15);
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,.075) !important;
        border-radius: 12px !important;
        background: rgba(255,255,255,.018) !important;
    }
    [data-testid="stExpander"] summary {
        color: #c9c1b8 !important;
        font: 500 .82rem 'DM Sans', sans-serif !important;
    }
    .stSpinner > div { color: var(--orange) !important; }
    [data-testid="stAlert"] { border-radius: 12px; }
    .footer {
        margin-top: 3.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid var(--line);
        color: #625c57;
        text-align: center;
        font: .63rem 'DM Mono', monospace;
        letter-spacing: .09em;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,140,50,.5); }
        70% { box-shadow: 0 0 0 7px rgba(255,140,50,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,140,50,0); }
    }
    @keyframes rise {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 850px) {
        .block-container { padding: 1rem 1.1rem 2.5rem; }
        .hero { padding: 1.5rem 0 1.7rem; }
        .hero h1 { font-size: clamp(2.8rem, 13vw, 4.4rem); }
        .input-shell { padding: 1.2rem; }
        .top-meta { font-size: .55rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------------
defaults = {
    "results": {},
    "running": False,
    "done": False,
    "error": None,
    "topic_input": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def choose_topic(value: str) -> None:
    """Set the topic input when an example chip is selected."""
    st.session_state.topic_input = value


def get_step_state(step: str) -> str:
    """Return the visible state for each pipeline stage."""
    steps = ["search", "reader", "writer", "critic"]
    results = st.session_state.results

    if step in results:
        return "done"

    if st.session_state.running:
        for current in steps:
            if current not in results:
                return "running" if current == step else "waiting"

    return "waiting"


def render_step(number: str, title: str, description: str, state: str) -> None:
    status = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ('<span class="pulse"></span>RUNNING', "status-running"),
        "done": ("✓ COMPLETE", "status-done"),
    }
    label, status_class = status[state]
    card_class = "active" if state == "running" else ("done" if state == "done" else "")

    st.markdown(
        f"""
        <div class="step-card {card_class}">
            <div class="step-top">
                <span class="step-num">{number}</span>
                <span class="step-title">{title}</span>
                <span class="step-status {status_class}">{label}</span>
            </div>
            <div class="step-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# TOP BAR + HERO
# -------------------------------------------------------------------
st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <span class="brand-mark">✳</span>
            <span>RESEARCHMIND</span>
        </div>
        <div class="top-meta"><span class="live-dot"></span>Multi-agent system · Ready</div>
    </div>

    <div class="hero">
        <div class="hero-eyebrow">✦ &nbsp; MULTI-AGENT AI RESEARCH STUDIO</div>
        <h1>Research<span>Mind.</span></h1>
        <p class="hero-sub">
            From a single research question to a structured report.
            Four specialized agents <strong>search, explore, write, and critique</strong>
            to turn information into insight.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# MAIN WORKSPACE
# -------------------------------------------------------------------
col_input, col_gap, col_pipeline = st.columns([5.2, 0.45, 4.35], gap="small")

with col_input:
    st.markdown(
        """
        <div class="section-kicker">01 / Define your research</div>
        <div class="section-title">What do you want to explore?</div>
        <div class="section-copy">Enter a topic and let your research agents do the heavy lifting.</div>
        <div class="input-shell">
        """,
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Reproduction in dogs, AI agents, quantum computing...",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="examples-label">✦ &nbsp; Need inspiration? Try a topic</div>', unsafe_allow_html=True)
    example_cols = st.columns(3)
    examples = [
        ("LLM agents 2025", "LLM agents 2025"),
        ("CRISPR gene editing", "CRISPR gene editing"),
        ("Fusion energy", "Fusion energy progress"),
    ]
    for col, (label, value) in zip(example_cols, examples):
        with col:
            st.button(
                label,
                key=f"example_{label}",
                use_container_width=True,
                on_click=choose_topic,
                args=(value,),
                type="secondary",
            )

    if st.session_state.done:
        st.markdown(
            """
            <div class="chip-caption">Your latest research run is complete. You can enter another topic anytime.</div>
            """,
            unsafe_allow_html=True,
        )

with col_pipeline:
    st.markdown(
        """
        <div class="pipeline-head">
            <div>
                <div class="section-kicker">02 / Live workflow</div>
                <div class="section-title">Your pipeline</div>
            </div>
            <div class="pipeline-count">04 STAGES</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_step("01", "Searcher", "Finds relevant web sources and recent information", get_step_state("search"))
    render_step("02", "Reader", "Opens sources and extracts deeper context", get_step_state("reader"))
    render_step("03", "Writer", "Transforms research into a structured report", get_step_state("writer"))
    render_step("04", "Evaluator", "Reviews the report and provides feedback", get_step_state("critic"))


# -------------------------------------------------------------------
# START PIPELINE
# -------------------------------------------------------------------
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic before starting.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.error = None
        st.rerun()


# -------------------------------------------------------------------
# EXECUTION
# -------------------------------------------------------------------
if st.session_state.running and not st.session_state.done:
    topic_value = st.session_state.topic_input.strip()

    try:
        with st.spinner("Research agents are working... This may take a little while."):
            pipeline_output = run_research_pipeline(topic_value)

        if not isinstance(pipeline_output, dict):
            raise TypeError("The research pipeline did not return a dictionary.")

        st.session_state.results = {
            "search": pipeline_output.get("search_results", ""),
            "reader": pipeline_output.get("scraped_content", ""),
            "writer": pipeline_output.get("report", ""),
            "critic": pipeline_output.get("feedback", ""),
        }
        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as exc:
        st.session_state.running = False
        st.session_state.done = False
        st.session_state.error = str(exc)
        st.error("The research pipeline could not complete. Check the error details below.")
        with st.expander("Technical error details", expanded=True):
            st.code(st.session_state.error)


if st.session_state.error and not st.session_state.running:
    st.error("Last run failed. Correct the issue and try again.")
    with st.expander("Technical error details", expanded=False):
        st.code(st.session_state.error)


# -------------------------------------------------------------------
# RESULTS
# -------------------------------------------------------------------
results = st.session_state.results

if results and st.session_state.done:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="result-heading">
            <h2>Research output</h2>
            <span class="result-tag">✓ RUN COMPLETED</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Raw intermediate outputs
    with st.expander("🔍  Searching — source discovery", expanded=False):
        st.text(results.get("search") or "No search output was returned.")

    with st.expander("📚  Reading — extracted content", expanded=False):
        st.text(results.get("reader") or "No scraped content was returned.")

    # Final report
    report = results.get("writer") or "The writer chain did not return a report."
    st.markdown('<div class="report-shell">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">✦ &nbsp; Final research report</div>', unsafe_allow_html=True)
    st.markdown(report)
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="⬇  Download research report (.md)",
        data=report,
        file_name=f"research_report_{int(time.time())}.md",
        mime="text/markdown",
        use_container_width=True,
    )

    # Critic feedback
    feedback = results.get("critic") or "The critic chain did not return feedback."
    st.markdown('<div class="feedback-shell">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">◈ &nbsp; Critic review & feedback</div>', unsafe_allow_html=True)
    st.markdown(feedback)
    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        RESEARCHMIND &nbsp;·&nbsp; POWERED BY Aditya Prasad Jena
        &nbsp;·&nbsp; BUILT WITH EMOTIONS TO SOLVE REAL WORLD PROBLEM
    </div>
    """,
    unsafe_allow_html=True,
)

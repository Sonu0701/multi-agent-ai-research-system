import streamlit as st

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --bg:          #0e0e0e;
    --surface:     #161616;
    --card:        #1a1a1a;
    --border:      #272727;
    --orange:      #ff6b1a;
    --orange-dim:  rgba(255,107,26,0.12);
    --orange-glow: rgba(255,107,26,0.22);
    --text:        #f0f0f0;
    --muted:       #666;
    --green:       #22c55e;
    --green-dim:   rgba(34,197,94,0.12);
    --red:         #ef4444;
    --red-dim:     rgba(239,68,68,0.10);
  }

  /* ── Global reset ── */
  html, body,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  .main, .block-container {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding-top: 0 !important;
  }
  [data-testid="stHeader"],
  [data-testid="stToolbar"],
  [data-testid="stDecoration"] { display: none !important; }
  section[data-testid="stSidebar"] { display: none !important; }
  .block-container { padding: 2rem 2.5rem !important; max-width: 100% !important; }

  /* ── Labels ── */
  .mono-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--orange);
    text-transform: uppercase;
    display: block;
    margin-bottom: 0.55rem;
  }

  /* ── Page title ── */
  .page-title {
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--text);
    margin: 0 0 0.35rem;
  }
  .page-sub {
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 400;
    margin-bottom: 2rem;
    letter-spacing: 0.01em;
  }

  /* ── Input ── */
  .stTextInput > label { display: none !important; }
  .stTextInput > div > div {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.93rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .stTextInput > div > div:focus-within {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px var(--orange-glow) !important;
  }
  .stTextInput input { color: var(--text) !important; background: transparent !important; }
  .stTextInput input::placeholder { color: var(--muted) !important; }

  /* ── Run button ── */
  .stButton > button {
    background: var(--orange) !important;
    color: #0e0e0e !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    margin-top: 0.35rem !important;
    transition: opacity 0.15s, transform 0.1s !important;
  }
  .stButton > button:hover  { opacity: 0.87 !important; transform: translateY(-1px) !important; }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Suggestion chips ── */
  .try-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.4rem;
    margin-top: 1.1rem;
  }
  .try-arrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: var(--muted);
    text-transform: uppercase;
    margin-right: 0.2rem;
  }
  .chip {
    background: var(--card);
    border: 1px solid var(--border);
    color: #999;
    font-size: 0.75rem;
    padding: 0.28rem 0.75rem;
    border-radius: 20px;
    display: inline-block;
  }

  /* ── Panel heading ── */
  .panel-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 1rem;
    letter-spacing: -0.01em;
  }

  /* ── Agent cards ── */
  .agent-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 0.95rem 1.2rem;
    margin-bottom: 0.55rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, box-shadow 0.25s, opacity 0.25s;
  }
  .agent-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
    background: transparent;
    transition: background 0.25s;
  }

  .agent-card.waiting { opacity: 0.45; }

  .agent-card.running {
    border-color: var(--orange);
    box-shadow: 0 0 22px var(--orange-glow);
    opacity: 1;
  }
  .agent-card.running::before { background: var(--orange); }

  .agent-card.done { border-color: rgba(34,197,94,0.38); opacity: 1; }
  .agent-card.done::before { background: var(--green); }

  .agent-card.error { border-color: rgba(239,68,68,0.38); opacity: 0.85; }
  .agent-card.error::before { background: var(--red); }

  .agent-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--orange);
    font-weight: 500;
    width: 1.7rem;
    flex-shrink: 0;
  }
  .agent-body { flex: 1; min-width: 0; }
  .agent-name {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.12rem;
  }
  .agent-desc {
    font-size: 0.73rem;
    color: var(--muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .agent-card.running .agent-desc { color: #999; }

  .status-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    flex-shrink: 0;
    font-weight: 500;
  }
  .badge-waiting { background: rgba(255,255,255,0.04); color: var(--muted); }
  .badge-running {
    background: var(--orange-dim);
    color: var(--orange);
    animation: blink 1.1s ease-in-out infinite;
  }
  .badge-done  { background: var(--green-dim); color: var(--green); }
  .badge-error { background: var(--red-dim);   color: var(--red);   }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
  }

  /* ── Intermediate output blocks ── */
  .section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--orange);
    text-transform: uppercase;
    margin: 1.6rem 0 0.75rem;
  }

  .out-block {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
  }
  .out-block-head {
    font-size: 0.72rem;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
  }
  .out-block-body {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.7;
    color: #bbb;
    white-space: pre-wrap;
    max-height: 180px;
    overflow-y: auto;
    padding-right: 0.2rem;
  }
  .out-block-body::-webkit-scrollbar { width: 3px; }
  .out-block-body::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* ── Final report ── */
  .report-block {
    background: #111;
    border: 1.5px solid rgba(255,107,26,0.28);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.7rem;
  }
  .report-block-head {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--orange);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .report-block-body {
    font-size: 0.87rem;
    line-height: 1.8;
    color: #ddd;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 0.3rem;
  }
  .report-block-body::-webkit-scrollbar { width: 3px; }
  .report-block-body::-webkit-scrollbar-thumb { background: var(--orange); border-radius: 3px; }

  /* ── Critic ── */
  .critic-block {
    background: #111;
    border: 1.5px solid rgba(34,197,94,0.22);
    border-radius: 12px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 0.7rem;
  }
  .critic-block-head {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--green);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .critic-block-body {
    font-size: 0.87rem;
    line-height: 1.8;
    color: #ccc;
    white-space: pre-wrap;
    max-height: 250px;
    overflow-y: auto;
  }

  /* ── Download button ── */
  [data-testid="stDownloadButton"] button {
    background: transparent !important;
    color: var(--orange) !important;
    border: 1.5px solid var(--orange) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
  }

  hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  AGENT DEFINITIONS
# ─────────────────────────────────────────────
AGENTS = [
    {"num": "01", "key": "search",  "name": "Search Agent",  "desc": "Gathers recent web information via Tavily"},
    {"num": "02", "key": "reader",  "name": "Reader Agent",  "desc": "Scrapes & extracts deep content from best URL"},
    {"num": "03", "key": "writer",  "name": "Writer Agent",  "desc": "Drafts the full structured research report"},
    {"num": "04", "key": "critic",  "name": "Critic Agent",  "desc": "Reviews & scores — retries if score < 7"},
]


def agent_cards_html(active_key=None, done_keys=None, error_keys=None):
    done_keys  = done_keys  or []
    error_keys = error_keys or []
    html = '<div class="panel-title">Pipeline</div>'
    for a in AGENTS:
        k = a["key"]
        if k in error_keys:
            state, badge_cls, badge_txt = "error",   "badge-error",   "✗ Error"
        elif k in done_keys:
            state, badge_cls, badge_txt = "done",    "badge-done",    "Done"
        elif k == active_key:
            state, badge_cls, badge_txt = "running", "badge-running", "● Running"
        else:
            state, badge_cls, badge_txt = "waiting", "badge-waiting", "Waiting"

        html += f"""
        <div class="agent-card {state}">
          <div class="agent-num">{a['num']}</div>
          <div class="agent-body">
            <div class="agent-name">{a['name']}</div>
            <div class="agent-desc">{a['desc']}</div>
          </div>
          <span class="status-badge {badge_cls}">{badge_txt}</span>
        </div>"""
    return html


def results_html(results):
    if not results:
        return ""
    html = ""

    intermediates = [
        ("search", "🔍 Search Results"),
        ("urls",   "🔗 Extracted URLs"),
        ("reader", "📄 Scraped Content"),
    ]
    if any(k in results for k, _ in intermediates):
        html += '<div class="section-label">Intermediate Outputs</div>'
        for k, title in intermediates:
            if k in results:
                html += f"""
                <div class="out-block">
                  <div class="out-block-head">{title}</div>
                  <div class="out-block-body">{results[k]}</div>
                </div>"""

    if "report" in results:
        html += f"""
        <div class="report-block">
          <div class="report-block-head">⚡ Research Report</div>
          <div class="report-block-body">{results['report']}</div>
        </div>"""

    if "feedback" in results:
        html += f"""
        <div class="critic-block">
          <div class="critic-block-head">✦ Critic Feedback</div>
          <div class="critic-block-body">{results['feedback']}</div>
        </div>"""

    return html


# ─────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────
left, right = st.columns([1, 1.35], gap="large")

with left:
    st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Research<br>Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Four AI agents · LangGraph powered · One topic</div>', unsafe_allow_html=True)

    st.markdown('<span class="mono-label">Research Topic</span>', unsafe_allow_html=True)
    topic = st.text_input("topic", placeholder="e.g. Quantum computing breakthroughs in 2025",
                          label_visibility="collapsed")

    run_btn = st.button("⚡  Run Research Pipeline")

    st.markdown("""
    <div class="try-row">
      <span class="try-arrow">TRY →</span>
      <span class="chip">LLM agents 2025</span>
      <span class="chip">CRISPR gene editing</span>
      <span class="chip">Fusion energy progress</span>
      <span class="chip">Quantum computing</span>
      <span class="chip">Climate tech 2025</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    download_slot = st.empty()

with right:
    st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)
    agents_slot  = st.empty()
    results_slot = st.empty()
    agents_slot.markdown(agent_cards_html(), unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        left.warning("⚠️  Please enter a research topic.")
        st.stop()

    from pipeline import build_research_graph

    done_keys  = []
    error_keys = []
    results    = {}

    def refresh(active=None):
        agents_slot.markdown(
            agent_cards_html(active_key=active, done_keys=done_keys, error_keys=error_keys),
            unsafe_allow_html=True,
        )

    def push_results():
        results_slot.markdown(results_html(results), unsafe_allow_html=True)

    research_graph = build_research_graph()

    refresh("search")

    initial_state = {
        "topic": topic,
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "score": 0,
        "retry_count": 0,
        "urls": ""
    }

    try:
        for step in research_graph.stream(initial_state, stream_mode="updates"):
            node_name = list(step.keys())[0]
            node_output = step[node_name]

            if node_name == "search":
                results["search"] = node_output.get("search_results", "")
                results["urls"]   = node_output.get("urls", "")
                done_keys.append("search")
                refresh("reader")

            elif node_name == "reader":
                results["reader"] = node_output.get("scraped_content", "")
                done_keys.append("reader")
                refresh("writer")

            elif node_name == "writer":
                results["report"] = node_output.get("report", "")
                if "writer" not in done_keys:
                    done_keys.append("writer")
                refresh("critic")

            elif node_name == "critic":
                results["feedback"] = node_output.get("feedback", "")
                score = node_output.get("score", 0)
                retry = node_output.get("retry_count", 0)

                if score < 7 and retry < 2:
                    done_keys = [k for k in done_keys if k != "writer"]
                    refresh("writer")
                    st.toast(f"Score {score}/10 — refining report...", icon="🔄")
                else:
                    done_keys.append("critic")
                    refresh(None)

            push_results()

    except Exception as e:
        st.error(f"Pipeline error: {e}")

    dl = (
        f"TOPIC: {topic}\n\n"
        f"{'='*60}\nREPORT\n{'='*60}\n{results.get('report','')}\n\n"
        f"{'='*60}\nFEEDBACK\n{'='*60}\n{results.get('feedback','')}"
    )
    with download_slot:
        st.download_button(
            "⬇  Download Report (.txt)",
            data=dl,
            file_name=f"research_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

import streamlit as st

st.set_page_config(
    page_title="Hybrid Fraud Detection",
    layout="wide",
    page_icon="⚡"
)

st.markdown("""
<style>
:root {
  --bg: #0B0E14;
  --panel: rgba(255,255,255,0.06);
  --panel-strong: rgba(255,255,255,0.10);
  --text: #E6E9EF;
  --muted: #AAB0BC;
  --accent: #7C5CFF;
  --accent-2: #00E5FF;
  --good: #2ECC71;
  --warn: #F1C40F;
  --bad:  #FF6B6B;
  --radius: 18px;
}

html, body, [class*="css"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
}

.block-container { padding-top: 1.2rem; }

.hero {
  background: radial-gradient(1200px circle at 0% -20%, rgba(124,92,255,0.35), transparent 50%),
              radial-gradient(1000px circle at 100% -30%, rgba(0,229,255,0.25), transparent 45%),
              linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: calc(var(--radius) + 6px);
  padding: 1.6rem 1.8rem;
  box-shadow: 0 12px 40px rgba(0,0,0,0.45);
}

.hero h1 { font-size: 2.0rem; margin-bottom: 0.2rem; }
.hero p  { color: var(--muted); font-size: 1.02rem; line-height: 1.6; }

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
@media (max-width: 1100px){
  .grid { grid-template-columns: 1fr; }
}

.card {
  background: var(--panel);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: var(--radius);
  padding: 1.1rem 1.2rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

.card h3 { font-size: 1.15rem; margin-bottom: 0.4rem; }
.card p { color: var(--muted); line-height: 1.55; }

.pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(124,92,255,0.12);
  border: 1px solid rgba(124,92,255,0.35);
  font-size: 0.85rem;
}

.footer { color: var(--muted); font-size: 0.9rem; margin-top: 0.5rem; }

hr {
  border: none;
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 1.1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="pill">⚡ Hybrid ML + Rules</div>
  <h1>Real-Time Bitcoin Fraud Detection Console</h1>
  <p>
    A production-style decision system that combines an <b>XGBoost illicit probability model</b>
    with a <b>transparent rule engine</b>. Analysts can tune risk appetite live, inspect decisions,
    and verify new transactions in real time through the backend.
  </p>
</div>
""", unsafe_allow_html=True)

# ---------- Quick start cards ----------
st.markdown("""
<div class="grid">
  <div class="card">
    <h3>⚡ Real-Time Verification</h3>
    <p>
      Submit a single transaction to the backend. The system computes:
      <b>ML Probability</b>, <b>Rule Score</b>, and a final hybrid decision.
    </p>
    <p class="footer">Open in sidebar → “Real-Time Verification”.</p>
  </div>
  <div class="card">
    <h3>🎛️ Risk Appetite Tuner</h3>
    <p>
      Redefine “suspicious” on the fly. Change rule thresholds and weights,
      and instantly see how KPIs and detection behavior shift.
    </p>
    <p class="footer">Open in sidebar → “Risk Appetite Tuner”.</p>
  </div>
  <div class="card">
    <h3>🔍 Forensic Inspection</h3>
    <p>
      Drill into false positives / false negatives to see which rules fired,
      and how ML confidence interacted with human logic.
    </p>
    <p class="footer">Built into the tuner page.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

colA, colB = st.columns([1.2, 1])

with colA:
    st.subheader("How decisions are made")
    st.latex(r"""
    \text{Flagged} =
    (\text{XGBoost\_Prob} \ge \tau_{\text{ML}})
    \ \lor \
    \left(\sum_i \text{Rule}_i \cdot w_i \ge \tau_{\text{Rules}}\right)
    """)

with colB:
    st.subheader("Backend status")
    st.write("Start backend first:")
    st.code("uvicorn backend.app:app --reload", language="bash")
    st.write("Then run Streamlit:")
    st.code("streamlit run streamlit_app/Home.py", language="bash")

st.info("Use the left sidebar to navigate between modules.")

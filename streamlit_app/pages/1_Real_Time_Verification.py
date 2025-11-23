import streamlit as st
import requests
import pandas as pd
from components.theme_toggle import render_theme_toggle, render_animated_background

st.set_page_config(page_title="Real-Time Verification", layout="wide", page_icon="⚡")

# -------------------------------------------------------------------
# Global premium layers
# -------------------------------------------------------------------
render_theme_toggle()
render_animated_background()

# -------------------------------------------------------------------
# PREMIUM CSS + TRUE ANIMATED BACKGROUND LAYERS
# -------------------------------------------------------------------
st.markdown("""
<style>
/* ====== DESIGN TOKENS (MATCH HOME) ====== */
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

  --glow-1: rgba(124,92,255,0.55);
  --glow-2: rgba(0,229,255,0.45);
}

/* LIGHT THEME OVERRIDES */
.light-theme {
  --bg: #F5F7FA;
  --text: #131722;
  --panel: rgba(0,0,0,0.06);
  --panel-strong: rgba(0,0,0,0.10);
  --muted: #4A5568;
  --accent: #6C4BFF;
  --accent-2: #00A7D6;

  --glow-1: rgba(108,75,255,0.45);
  --glow-2: rgba(0,167,214,0.40);
}

/* Global App Styling */
html, body, [class*="css"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
}
.block-container { padding-top: 1.2rem; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

.stApp { background: transparent !important; }

.main, .block-container, [data-testid="stSidebar"] {
  position: relative;
  z-index: 2;
}

/* ===== BACKGROUND LAYERS ===== */
.bg-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.orb {
  position: absolute;
  width: 70vmax;
  height: 70vmax;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.55;
  mix-blend-mode: screen;
  animation: orbFloat 18s ease-in-out infinite;
}
.orb1 {
  background: radial-gradient(circle, var(--glow-1), transparent 60%);
  top: -20vmax;
  left: -10vmax;
  animation-duration: 22s;
}
.orb2 {
  background: radial-gradient(circle, var(--glow-2), transparent 60%);
  top: -10vmax;
  right: -15vmax;
  animation-duration: 19s;
}
.orb3 {
  background: radial-gradient(circle, rgba(255,255,255,0.08), transparent 60%);
  bottom: -25vmax;
  left: 10vmax;
  animation-duration: 26s;
}

@keyframes orbFloat {
  0%   { transform: translate(0, 0) scale(1); }
  50%  { transform: translate(4vmax, -3vmax) scale(1.08); }
  100% { transform: translate(0, 0) scale(1); }
}

/* Neon Moving Grid */
.grid-overlay {
  position: absolute;
  inset: -50%;
  background:
    linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
  background-size: 64px 64px;
  opacity: 0.25;
  animation: gridDrift 30s linear infinite;
  mask-image: radial-gradient(circle at 50% 10%, black 0%, transparent 70%);
}

@keyframes gridDrift {
  0%   { transform: translateY(0) translateX(0); }
  100% { transform: translateY(8%) translateX(-6%); }
}

/* ===== PAGE TITLE ===== */
.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: 0.2px;
}
.page-sub {
  color: var(--muted);
  font-size: 1.05rem;
  margin-bottom: 1.6rem;
}

/* ===== CARDS ===== */
.card {
  position: relative;
  background: rgba(0,0,0,0.48);
  backdrop-filter: blur(9px);
  border-radius: var(--radius);
  padding: 1.2rem 1.3rem;
  border: 1px solid rgba(255,255,255,0.12);
  transition: 0.25s;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 50px rgba(0,0,0,0.62);
}

/* ===== RESULT CARDS ===== */
.result-card {
  background: rgba(0,0,0,0.55);
  padding: 1.4rem;
  border-radius: 16px;
  text-align: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.12);
}

.result-icon { font-size: 2.4rem; }
.result-value { font-size: 2rem; font-weight: 800; }

/* ===== ALERTS ===== */
.alert {
  background: rgba(0,0,0,0.54);
  border-radius: 16px;
  padding: 1.2rem;
  display: flex;
  gap: 1.1rem;
  border-left: 4px solid var(--accent);
}
.alert-error { border-left-color: var(--bad); }
.alert-success { border-left-color: var(--good); }

/* ===== INPUTS ===== */
.stTextInput input,
.stNumberInput input {
  background: rgba(255,255,255,0.05) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}
</style>

<div class="bg-layer">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
  <div class="grid-overlay"></div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------
st.markdown('<div class="page-title">⚡ Real-Time Transaction Verification</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Submit transactions to the backend and receive instant hybrid fraud decisions.</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# BACKEND URL (REMOVED FROM SIDEBAR)
# -------------------------------------------------------------------
API_URL = "http://localhost:8000/transactions"   # ← FIXED backend URL

# -------------------------------------------------------------------
# Layout
# -------------------------------------------------------------------
col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown('<div class="card"><div class="card-title">📝 Transaction Input</div>', unsafe_allow_html=True)

    user_id = st.number_input("👤 User ID", min_value=1, value=1)
    tx_id = st.text_input("🔖 Transaction ID", value="TX_001")
    time_step = st.number_input("⏱️ Time Step", min_value=0, value=10)

    st.markdown("---")
    st.markdown("<p style='font-weight:700;'>Key Elliptic Features</p>", unsafe_allow_html=True)

    feat_3 = st.number_input("💰 feat_3 — Amount", value=1000.0)
    feat_4 = st.number_input("💸 feat_4 — Fee", value=0.1)
    feat_100 = st.number_input("🔗 feat_100 — Neighbor Agg", value=0.5)
    feat_10 = st.number_input("⚡ feat_10 — Velocity", value=5.0)
    feat_15 = st.number_input("📊 feat_15", value=1.0)
    feat_20 = st.number_input("📈 feat_20", value=1.0)

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card"><div class="card-title">🎯 Quick Presets</div>', unsafe_allow_html=True)

    preset = st.selectbox("📋 Select Preset", ["Custom", "Likely Licit", "Likely Illicit (High-Value + Zero Fee)"])

    if preset == "Likely Licit":
        feat_3, feat_4, time_step, feat_100, feat_10, feat_15, feat_20 = 1200.0, 0.2, 9, 0.2, 3.0, 1.0, 1.0
        st.success("✓ Preset loaded")
    elif preset == "Likely Illicit (High-Value + Zero Fee)":
        feat_3, feat_4, time_step, feat_100, feat_10, feat_15, feat_20 = 80000.0, 0.0, 2, 1.4, 15.0, 4.0, 1.0
        st.warning("⚠ Preset loaded")

    st.markdown("---")
    st.markdown("<p style='font-weight:700;'>Payload Preview</p>", unsafe_allow_html=True)

    features = {
        "feat_3": feat_3, "feat_4": feat_4, "feat_100": feat_100,
        "feat_10": feat_10, "feat_15": feat_15, "feat_20": feat_20
    }
    st.json(features)

    st.markdown("</div>", unsafe_allow_html=True)

payload = {"user_id": user_id, "tx_id": tx_id, "time_step": int(time_step), "features": features}

verify = st.button("🚀 Verify Transaction", use_container_width=True, type="primary")

# -------------------------------------------------------------------
# Verification
# -------------------------------------------------------------------
if verify:
    with st.spinner("🔄 Analyzing transaction..."):
        try:
            res = requests.post(API_URL, json=payload, timeout=10)
            if res.status_code != 200:
                st.error(f"❌ Backend error: {res.status_code}")
                st.code(res.text)
                st.stop()

            result = res.json()
            ml_prob = result.get("ml_probability", result.get("fraud_probability", 0.0))
            is_fraud = result.get("fraud", False)
            if "fraud" not in result and "status" in result:
                is_fraud = (result["status"] == "REJECTED")

            st.markdown("---")
            st.markdown("<h2 style='font-size:1.7rem; font-weight:800;'>📊 Decision Results</h2>", unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)

            with k1:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-icon">🧠</div>
                    <div class="result-value">{ml_prob:.1%}</div>
                    <div class="result-label">ML Probability</div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-icon">⚙️</div>
                    <div class="result-value">{result.get('rule_score', 0.0):.0f}</div>
                    <div class="result-label">Rule Score</div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                status_icon = "🚨" if is_fraud else "✅"
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-icon">{status_icon}</div>
                    <div class="result-value">{result.get('status', 'UNKNOWN')}</div>
                    <div class="result-label">Final Status</div>
                </div>
                """, unsafe_allow_html=True)

            if is_fraud:
                st.markdown("""
                <div class="alert alert-error">
                    <div class="alert-icon">🚨</div>
                    <div>
                        <div class="alert-title">FRAUD DETECTED — Block Transaction</div>
                        <div class="alert-message">This transaction has been flagged as suspicious.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert alert-success">
                    <div class="alert-icon">✅</div>
                    <div>
                        <div class="alert-title">CLEAN TRANSACTION — Allow</div>
                        <div class="alert-message">This transaction appears legitimate.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if "fired_rules" in result:
                st.markdown("---")
                st.markdown("<h2 style='font-size:1.5rem; font-weight:800;'>🔍 Rule Breakdown</h2>", unsafe_allow_html=True)

                fired_df = pd.DataFrame({
                    "Rule": list(result["fired_rules"].keys()),
                    "Status": ["🔴 Fired" if v == 1 else "⚪ Not Fired" for v in result["fired_rules"].values()]
                })
                st.dataframe(fired_df, use_container_width=True, hide_index=True)

        except requests.exceptions.ConnectionError:
            st.error("❌ Backend not reachable")
            st.code("uvicorn backend.app:app --reload", language="bash")
        except Exception as e:
            st.error("❌ Error occurred")
            st.exception(e)

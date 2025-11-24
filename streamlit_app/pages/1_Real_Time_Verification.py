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
# CLOUD URL LOGIC (Synced with Home.py)
# -------------------------------------------------------------------
# Grab URL from Session State (set by Home.py) or fallback to localhost
default_url = st.session_state.get("api_url", "http://localhost:8000/transactions")

API_URL = st.sidebar.text_input(
    "Backend URL",
    value=default_url,
    help="The endpoint where transaction data is sent."
)

# -------------------------------------------------------------------
# PREMIUM CSS
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
  --text: #101525;
  --panel: rgba(0,0,0,0.06);
  --panel-strong: rgba(0,0,0,0.10);
  --muted: #4A5568;
  --accent: #6C4BFF;
  --accent-2: #00A7D6;
  --glow-1: rgba(108,75,255,0.45);
  --glow-2: rgba(0,167,214,0.40);
}

.section-title { font-family:'Orbitron'; font-size: 1.4rem; font-weight: 700; margin: 1.5rem 0 0.8rem 0; color: var(--accent-2); }
.panel {
  background: var(--panel);
  border: 1px solid var(--panel-strong);
  border-radius: var(--radius);
  padding: 1.5rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* ALERTS */
.alert {
  padding: 1rem; border-radius: 12px; margin-top: 1rem;
  display: flex; align-items: center; gap: 1rem;
  animation: fadeIn 0.5s ease;
}
.alert-danger { background: rgba(255, 107, 107, 0.15); border: 1px solid var(--bad); color: var(--bad); }
.alert-success { background: rgba(46, 204, 113, 0.15); border: 1px solid var(--good); color: var(--good); }
.alert-icon { font-size: 1.8rem; }
.alert-title { font-weight: 800; font-size: 1.1rem; letter-spacing: 0.5px; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Real-Time Transaction Verification")

# -------------------------------------------------------------------
# INPUT FORM
# -------------------------------------------------------------------
st.markdown("<div class='section-title'>Transaction Parameters</div>", unsafe_allow_html=True)

col_l, col_r = st.columns([1.2, 1])

with col_l:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("📝 Core Details")
    c1, c2, c3 = st.columns(3)
    user_id = c1.number_input("User ID", min_value=1, value=101)
    tx_id = c2.text_input("TX ID", value="TX_LIVE_001")
    time_step = c3.number_input("Time Step", min_value=1, value=10)
    
    st.markdown("---")
    st.subheader("📊 Elliptic Features")
    f1, f2 = st.columns(2)
    feat_3 = f1.number_input("feat_3 (Value)", value=1000.0)
    feat_4 = f2.number_input("feat_4 (Fee)", value=0.1)
    
    f3, f4 = st.columns(2)
    feat_10 = f3.number_input("feat_10 (Velocity)", value=5.0)
    feat_100 = f4.number_input("feat_100 (Agg)", value=0.5)
    
    f5, f6 = st.columns(2)
    feat_15 = f5.number_input("feat_15", value=1.0)
    feat_20 = f6.number_input("feat_20", value=1.0)
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🚀 Quick Scenarios")
    preset = st.selectbox("Load Scenario", ["Custom", "Licit (Normal)", "Illicit (High Value + 0 Fee)"])
    
    if preset == "Licit (Normal)":
        feat_3, feat_4, feat_10, feat_100 = 500.0, 0.5, 2.0, 0.1
        st.info("Loaded 'Normal' values.")
    elif preset == "Illicit (High Value + 0 Fee)":
        feat_3, feat_4, feat_10, feat_100 = 60000.0, 0.0, 15.0, 1.2
        st.warning("Loaded 'Suspicious' values.")
        
    st.markdown("---")
    st.caption("Payload Preview")
    st.code({
        "feat_3": feat_3, "feat_4": feat_4, "feat_10": feat_10, "feat_100": feat_100
    }, language="json")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SUBMISSION LOGIC
# -------------------------------------------------------------------
payload = {
    "user_id": user_id,
    "tx_id": tx_id,
    "time_step": int(time_step),
    "features": {
        "feat_3": feat_3, "feat_4": feat_4, "feat_100": feat_100,
        "feat_10": feat_10, "feat_15": feat_15, "feat_20": feat_20
    }
}

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 ANALYZE TRANSACTION", use_container_width=True):
    with st.spinner("Querying Hybrid Model..."):
        try:
            res = requests.post(API_URL, json=payload, timeout=10)
            
            if res.status_code != 200:
                st.error(f"Backend Error: {res.status_code}")
                st.stop()
                
            result = res.json()
            
            # Display Decision
            st.markdown("<div class='section-title'>Hybrid Decision</div>", unsafe_allow_html=True)
            
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("ML Probability", f"{result.get('ml_probability', 0):.2%}")
            m2.metric("Rule Score", f"{result.get('rule_score', 0):.1f}")
            m3.metric("Status", result.get('status', 'UNKNOWN'))
            
            # Final Verdict Banner
            is_fraud = result.get("fraud", False) or (result.get("status") == "REJECTED")
            
            if is_fraud:
                st.markdown("""
                <div class="alert alert-danger">
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
            st.error("❌ Backend not reachable. Is the Render/FastAPI server running?")
        except Exception as e:
            st.error("❌ Error occurred")
            st.exception(e)
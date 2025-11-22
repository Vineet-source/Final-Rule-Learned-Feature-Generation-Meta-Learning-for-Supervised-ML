import streamlit as st
import requests
import pandas as pd

st.markdown("""
<style>
.section-title { font-size: 1.35rem; font-weight: 700; margin: 0.2rem 0 0.6rem 0; }
.panel {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 1rem 1.1rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
.kpi {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px;
  padding: 0.8rem 0.9rem;
}
.badge {
  display:inline-flex; align-items:center; gap:6px;
  padding: 4px 10px; border-radius: 999px;
  font-size: 0.85rem; font-weight: 600;
  border: 1px solid rgba(255,255,255,0.12);
}
.badge-good{ background: rgba(46,204,113,0.12); border-color: rgba(46,204,113,0.5); }
.badge-bad{ background: rgba(255,107,107,0.12); border-color: rgba(255,107,107,0.5); }
.badge-warn{ background: rgba(241,196,15,0.12); border-color: rgba(241,196,15,0.5); }
hr { border:none; height:1px; background: rgba(255,255,255,0.08); margin: 1rem 0; }
small { color: #AAB0BC; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Real-Time Transaction Verification")

# Check if API URL is in secrets, else default to localhost
API_URL = st.sidebar.text_input(
    "Backend URL",
    value="http://localhost:8000/transactions",
    help="FastAPI endpoint. Start it with: uvicorn app:app --reload"
)

st.markdown("<div class='section-title'>Transaction Input</div>", unsafe_allow_html=True)

with st.container():
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Core Transaction Fields")

        user_id = st.number_input("User ID", min_value=1, value=1)
        tx_id = st.text_input("Transaction ID", value="TX_001")
        time_step = st.number_input("Time Step", min_value=0, value=10)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Key Elliptic Features")
        st.caption("These map to the rules + ML model. Missing features default to 0 in backend.")

        feat_3 = st.number_input("feat_3 — Amount / Value", value=1000.0)
        feat_4 = st.number_input("feat_4 — Fee", value=0.1)
        feat_100 = st.number_input("feat_100 — Neighbor Aggregation", value=0.5)
        feat_10 = st.number_input("feat_10 — Velocity Proxy", value=5.0)
        feat_15 = st.number_input("feat_15", value=1.0)
        feat_20 = st.number_input("feat_20", value=1.0)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Quick Presets")

        preset = st.selectbox(
            "Load a preset",
            ["Custom", "Likely Licit", "Likely Illicit (High-Value + Zero Fee)"],
            index=0
        )

        if preset == "Likely Licit":
            feat_3, feat_4, time_step, feat_100, feat_10, feat_15, feat_20 = 1200.0, 0.2, 9, 0.2, 3.0, 1.0, 1.0
            st.success("Preset loaded.")
        elif preset == "Likely Illicit (High-Value + Zero Fee)":
            feat_3, feat_4, time_step, feat_100, feat_10, feat_15, feat_20 = 80000.0, 0.0, 2, 1.4, 15.0, 4.0, 1.0
            st.warning("Preset loaded.")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("What will be sent?")
        features = {
            "feat_3": feat_3,
            "feat_4": feat_4,
            "feat_100": feat_100,
            "feat_10": feat_10,
            "feat_15": feat_15,
            "feat_20": feat_20,
        }
        st.json(features)
        st.markdown("</div>", unsafe_allow_html=True)

payload = {
    "user_id": user_id,
    "tx_id": tx_id,
    "time_step": int(time_step),
    "features": features
}

col_btn1, col_btn2 = st.columns([1, 2])
with col_btn1:
    verify = st.button("Verify Transaction", use_container_width=True)

if verify:
    try:
        res = requests.post(API_URL, json=payload, timeout=10)
        if res.status_code != 200:
            st.error(f"Backend error: {res.status_code}")
            st.code(res.text)
            st.stop()

        result = res.json()

        # Compatibility Logic: Handle different variable names from Backend
        # Checks for 'ml_probability' OR 'fraud_probability'
        ml_prob = result.get("ml_probability", result.get("fraud_probability", 0.0))
        
        # Checks for 'fraud' boolean OR infers it from Status
        is_fraud = result.get("fraud", False)
        if "fraud" not in result and "status" in result:
            is_fraud = (result["status"] == "REJECTED")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Decision</div>", unsafe_allow_html=True)

        k1, k2, k3 = st.columns(3)
        k1.metric("ML Probability", f"{ml_prob:.3f}")
        k2.metric("Rule Score", f"{result.get('rule_score', 0.0):.1f}")
        k3.metric("Status", result.get("status", "UNKNOWN"))

        verdict_badge = "badge-bad" if is_fraud else "badge-good"
        verdict_text = "🚨 FRAUD — Block Transaction" if is_fraud else "✅ CLEAN — Allow Transaction"

        st.markdown(f"""
        <div class='panel'>
          <span class='badge {verdict_badge}'>{verdict_text}</span>
          <small style='display:block;margin-top:6px;'>
            Decision = (ML ≥ τML) OR (Rules ≥ τRules)
          </small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Fired Rules</div>", unsafe_allow_html=True)

        if "fired_rules" in result:
            fired_df = pd.DataFrame({
                "Rule": list(result["fired_rules"].keys()),
                "Fired": list(result["fired_rules"].values())
            })
            st.dataframe(
                fired_df.style.applymap(
                    lambda v: "background-color: rgba(255,107,107,0.18);" if v == 1 else ""
                ),
                use_container_width=True
            )
        else:
            st.info("No rule details returned from backend.")

    except requests.exceptions.ConnectionError:
        st.error("Backend not reachable. Start FastAPI first.")
        st.code("uvicorn app:app --reload", language="bash")
    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Real-Time Verification", layout="wide", page_icon="⚡")

if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

theme = st.session_state.theme

if theme == 'dark':
    bg, card_bg, text, accent, accent2 = "#0a0e27", "rgba(255,255,255,0.05)", "#ffffff", "#00d4ff", "#ff006e"
else:
    bg, card_bg, text, accent, accent2 = "#f0f4f8", "rgba(255,255,255,0.9)", "#1a1a2e", "#0066ff", "#ff006e"

st.markdown(f"""
<style>
@keyframes wave {{ 0%, 100% {{ transform: translateX(0); }} 50% {{ transform: translateX(-25%); }} }}
@keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

/* Hide default Streamlit elements */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
.stDeployButton {{display: none;}}

.stApp {{ background: {bg} !important; }}
.stApp::before {{
    content: ''; position: fixed; top: 0; left: 0; width: 200%; height: 200%;
    background: radial-gradient(circle at 20% 50%, {accent}20 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, {accent2}20 0%, transparent 50%);
    animation: wave 20s ease-in-out infinite; z-index: 0; pointer-events: none;
}}

.particle {{ position: fixed; border-radius: 50%; pointer-events: none; z-index: 0; }}
.p1 {{ width: 300px; height: 300px; background: radial-gradient(circle, {accent}15 0%, transparent 70%);
       top: 10%; left: 10%; animation: float 8s ease-in-out infinite; }}

.main .block-container {{ position: relative; z-index: 10 !important; }}

.card {{
    background: {card_bg}; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem; animation: fadeIn 0.8s ease-out;
    transition: all 0.3s ease;
}}

.card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.3); border-color: {accent}; }}

.card-title {{ font-size: 1.5rem; font-weight: 700; color: {text}; margin-bottom: 1.5rem; }}

.result-card {{
    background: {card_bg}; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 2rem; text-align: center; transition: all 0.3s ease;
}}

.result-card:hover {{ transform: translateY(-10px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}

.result-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
.result-value {{ font-size: 2.5rem; font-weight: 800; color: {text}; margin-bottom: 0.5rem; }}
.result-label {{ font-size: 0.875rem; color: {text}; opacity: 0.7; text-transform: uppercase; }}

.alert {{
    background: {card_bg}; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 2rem; margin: 2rem 0; display: flex; align-items: center; gap: 1.5rem;
}}

.alert-success {{ border-left: 4px solid #00d25b; }}
.alert-error {{ border-left: 4px solid {accent2}; }}
.alert-icon {{ font-size: 3rem; }}
.alert-title {{ font-size: 1.25rem; font-weight: 700; color: {text}; margin-bottom: 0.5rem; }}
.alert-message {{ color: {text}; opacity: 0.9; }}

.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{ color: {text} !important; }}
[data-testid="stSidebar"] {{ background: {card_bg} !important; backdrop-filter: blur(20px); }}

.stButton > button {{
    background: linear-gradient(135deg, {accent}, {accent2}) !important; color: white !important;
    border: none !important; border-radius: 50px !important; padding: 1rem 3rem !important;
    font-weight: 600 !important; font-size: 1.125rem !important;
}}

.stButton > button:hover {{ transform: translateY(-3px); box-shadow: 0 8px 25px {accent}60; }}

.stTextInput label, .stNumberInput label, .stSelectbox label {{ color: {text} !important; }}
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select {{
    background: rgba(0,0,0,0.2) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    color: {text} !important; border-radius: 12px !important;
}}

.dataframe {{ background: {card_bg} !important; backdrop-filter: blur(20px); border-radius: 12px !important; }}

/* Sidebar styling */
[data-testid="stSidebar"] {{
    background: {card_bg} !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}}

[data-testid="stSidebar"] * {{
    color: {text} !important;
}}

[data-testid="stSidebar"] label {{
    color: {text} !important;
}}

[data-testid="stSidebar"] .stTextInput > div > div > input {{
    background: rgba(0,0,0,0.3) !important;
    color: {text} !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {{
    background: {card_bg} !important;
    color: {text} !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s ease !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    border-color: {accent} !important;
    transform: translateY(-2px) !important;
}}

[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[data-baseweb="button"][kind="primary"] {{
    background: linear-gradient(135deg, {accent}, {accent2}) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 12px {accent}40 !important;
}}
</style>

<div class="particle p1"></div>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color: {text}; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem;">⚡ Real-Time Transaction Verification</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="color: {text}; opacity: 0.9; font-size: 1.125rem; margin-bottom: 2rem;">Submit transactions to the backend API and get instant fraud detection results</p>', unsafe_allow_html=True)

API_URL = st.sidebar.text_input("🔗 Backend URL", value="http://localhost:8000/transactions")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown(f'<div class="card"><h3 class="card-title">📝 Transaction Input</h3></div>', unsafe_allow_html=True)
    user_id = st.number_input("👤 User ID", min_value=1, value=1)
    tx_id = st.text_input("🔖 Transaction ID", value="TX_001")
    time_step = st.number_input("⏱️ Time Step", min_value=0, value=10)
    st.markdown("---")
    st.markdown(f"<p style='color: {text}; font-weight: 600;'>Key Elliptic Features</p>", unsafe_allow_html=True)
    feat_3 = st.number_input("💰 feat_3 — Amount", value=1000.0)
    feat_4 = st.number_input("💸 feat_4 — Fee", value=0.1)
    feat_100 = st.number_input("🔗 feat_100 — Neighbor Agg", value=0.5)
    feat_10 = st.number_input("⚡ feat_10 — Velocity", value=5.0)
    feat_15 = st.number_input("📊 feat_15", value=1.0)
    feat_20 = st.number_input("📈 feat_20", value=1.0)

with col_right:
    st.markdown(f'<div class="card"><h3 class="card-title">🎯 Quick Presets</h3></div>', unsafe_allow_html=True)
    preset = st.selectbox("📋 Select Preset", ["Custom", "Likely Licit", "Likely Illicit (High-Value + Zero Fee)"])
    
    if preset == "Likely Licit":
        feat_3, feat_4, time_step, feat_100, feat_10, feat_15, feat_20 = 1200.0, 0.2, 9, 0.2, 3.0, 1.0, 1.0
        st.success("✓ Preset loaded")
    elif preset == "Likely Illicit (High-Value + Zero Fee)":
        feat_3, feat_4, time_step, feat_100, feat_10, feat_15, feat_20 = 80000.0, 0.0, 2, 1.4, 15.0, 4.0, 1.0
        st.warning("⚠ Preset loaded")
    
    st.markdown("---")
    st.markdown(f"<p style='color: {text}; font-weight: 600;'>Payload Preview</p>", unsafe_allow_html=True)
    features = {"feat_3": feat_3, "feat_4": feat_4, "feat_100": feat_100, "feat_10": feat_10, "feat_15": feat_15, "feat_20": feat_20}
    st.json(features)

payload = {"user_id": user_id, "tx_id": tx_id, "time_step": int(time_step), "features": features}

verify = st.button("🚀 Verify Transaction", use_container_width=True, type="primary")

if verify:
    with st.spinner("🔄 Analyzing..."):
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
            st.markdown(f"<h2 style='color: {text}; font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem;'>📊 Decision Results</h2>", unsafe_allow_html=True)
            
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
                        <div class="alert-message">This transaction has been flagged as suspicious</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert alert-success">
                    <div class="alert-icon">✅</div>
                    <div>
                        <div class="alert-title">CLEAN TRANSACTION — Allow</div>
                        <div class="alert-message">This transaction appears legitimate</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if "fired_rules" in result:
                st.markdown("---")
                st.markdown(f"<h2 style='color: {text}; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;'>🔍 Rule Breakdown</h2>", unsafe_allow_html=True)
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

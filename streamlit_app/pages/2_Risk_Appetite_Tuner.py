import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score

from components.theme_toggle import render_theme_toggle, render_animated_background

st.set_page_config(
    page_title="Risk Appetite Tuner | Fraud Detection",
    layout="wide",
    page_icon="🎛️"
)

# -------------------------------------------------------------------
# Premium global layers (same as Home / Verification)
# -------------------------------------------------------------------
render_theme_toggle()
render_animated_background()

# keep session_state theme for Plotly (CSS theme is body-class based)
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
theme = st.session_state.theme
plot_template = "plotly_dark" if theme == "dark" else "plotly_white"
plot_bg = "rgba(26,29,41,0.55)" if theme == "dark" else "rgba(255,255,255,0.75)"

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

/* Apply vars */
html, body, [class*="css"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
}

.block-container { padding-top: 1.0rem; }

/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* ====== ANIMATED AURA BACKGROUND ====== */
.aura {
  position: fixed;
  inset: -20%;
  z-index: -5;
  background:
    radial-gradient(800px circle at 10% 5%, var(--glow-1), transparent 55%),
    radial-gradient(700px circle at 90% 10%, var(--glow-2), transparent 55%),
    radial-gradient(900px circle at 50% 100%, rgba(255,255,255,0.06), transparent 60%);
  animation: auraShift 14s ease-in-out infinite;
  filter: blur(45px);
  opacity: 0.9;
  pointer-events: none;
}

@keyframes auraShift {
  0%   { transform: translateY(0px) translateX(0px) scale(1); }
  50%  { transform: translateY(-35px) translateX(25px) scale(1.06); }
  100% { transform: translateY(0px) translateX(0px) scale(1); }
}

/* ====== NEON GRID OVERLAY ====== */
.grid-overlay {
  position: fixed;
  inset: 0;
  z-index: -4;
  background:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(circle at 50% 20%, black 0%, transparent 70%);
  opacity: 0.35;
  pointer-events: none;
}

/* ====== PAGE HEADER ====== */
.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  margin-bottom: .25rem;
}
.page-subtitle {
  color: var(--muted);
  font-size: 1.05rem;
  margin-bottom: 1.2rem;
}

/* ====== PREMIUM CARDS ====== */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card {
  position: relative;
  background: rgba(0,0,0,0.50);
  backdrop-filter: blur(10px);
  border-radius: var(--radius);
  padding: 1.15rem 1.25rem;
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow:
    0 10px 32px rgba(0,0,0,0.45),
    0 0 0 1px rgba(255,255,255,0.03);
  animation: fadeUp 0.7s ease-out;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  overflow: hidden;
}

.light-theme .card { background: rgba(255,255,255,0.82); }

.card:before {
  content: "";
  position: absolute;
  inset: -120% -60%;
  background: conic-gradient(from 140deg, transparent, var(--glow-2), transparent 30%);
  opacity: 0.25;
  transition: opacity 0.25s ease;
}

.card:hover {
  transform: translateY(-5px);
  border-color: rgba(124,92,255,0.55);
  box-shadow:
    0 18px 50px rgba(0,0,0,0.62),
    0 0 0 1px rgba(124,92,255,0.18),
    0 0 30px var(--glow-1);
}

.card:hover:before { opacity: 0.45; }

.card-title {
  font-size: 1.25rem;
  font-weight: 750;
  margin-bottom: .8rem;
}

/* ====== KPI CARDS ====== */
.kpi-card {
  position: relative;
  background: rgba(0,0,0,0.58);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.35rem 1.1rem;
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 10px 28px rgba(0,0,0,0.4);
  text-align: center;
  transition: all .22s ease;
  animation: fadeUp .6s ease-out;
}
.light-theme .kpi-card { background: rgba(255,255,255,0.9); }

.kpi-card:hover {
  transform: translateY(-7px) scale(1.02);
  box-shadow: 0 18px 48px rgba(0,0,0,0.55), 0 0 25px var(--glow-2);
}

.kpi-icon  { font-size: 2rem; margin-bottom: .5rem; }
.kpi-value { font-size: 1.9rem; font-weight: 800; margin-bottom: .15rem; }
.kpi-label { font-size: .78rem; letter-spacing:.6px; color: var(--muted); text-transform: uppercase; }

/* ====== INPUTS / SLIDERS ====== */
.stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label {
  color: var(--text) !important;
  font-weight: 600;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > select {
  background: rgba(0,0,0,0.35) !important;
  color: var(--text) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  border-radius: 12px !important;
}
.light-theme .stTextInput > div > div > input,
.light-theme .stNumberInput > div > div > input,
.light-theme .stSelectbox > div > div > select {
  background: rgba(255,255,255,0.9) !important;
  border: 1px solid rgba(0,0,0,0.12) !important;
}

/* ====== BUTTONS ====== */
.stButton > button {
  background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
  color: white !important;
  border: none !important;
  border-radius: 999px !important;
  padding: .7rem 1.4rem !important;
  font-weight: 700 !important;
  transition: all .22s ease !important;
  box-shadow: 0 8px 22px rgba(0,0,0,0.45), 0 0 18px var(--glow-1);
}
.stButton > button:hover {
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 12px 35px rgba(0,0,0,0.6), 0 0 26px var(--glow-2);
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.62) !important;
  backdrop-filter: blur(12px);
  border-right: 1px solid rgba(255,255,255,0.12);
}
.light-theme [data-testid="stSidebar"] {
  background: rgba(255,255,255,0.92) !important;
  border-right: 1px solid rgba(0,0,0,0.12);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* dataframe */
[data-testid="stDataFrame"] {
  background: var(--panel) !important;
  border-radius: 12px !important;
  overflow: hidden;
}

</style>

<div class="aura"></div>
<div class="grid-overlay"></div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------
st.markdown('<div class="page-title">🎛️ Risk Appetite Tuner</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">'
    'Dynamically adjust rule thresholds and weights to see real-time impact on detection performance.'
    '</div>',
    unsafe_allow_html=True
)

# -------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("simulation_data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ simulation_data.csv not found. Please run hybrid_pipeline.py first.")
    st.stop()

# -------------------------------------------------------------------
# Sidebar Controls
# -------------------------------------------------------------------
st.sidebar.markdown("<h2 style='font-weight:800;'>🎛️ Policy Controls</h2>", unsafe_allow_html=True)

with st.sidebar.expander("🎯 Rule Definitions", expanded=True):
    th_high_val = st.slider("R1: High Value (>)", 1000.0, 100000.0, 50000.0, 1000.0)
    th_zero_fee = st.slider("R2: Zero Fee (<=)", 0.0, 1.0, 0.0, 0.1)
    th_early_step = st.slider("R3: Early Step (<=)", 1, 10, 5)
    th_agg = st.slider("R5: Neighbor Agg (>)", 0.1, 5.0, 0.8, 0.1)
    th_struct_ratio = st.slider("R7: Structural (>)", 1.0, 5.0, 2.0, 0.1)

with st.sidebar.expander("⚖️ Rule Weights", expanded=True):
    w_r1 = st.slider("Weight R1", 0, 50, 15)
    w_r2 = st.slider("Weight R2", 0, 50, 10)
    w_r3 = st.slider("Weight R3", 0, 50, 5)
    w_r4 = st.slider("Weight R4", 0, 50, 10)
    w_r5 = st.slider("Weight R5", 0, 50, 15)
    w_r6 = st.slider("Weight R6", 0, 50, 5)
    w_r7 = st.slider("Weight R7", 0, 50, 10)

with st.sidebar.expander("🎚️ Decision Boundary", expanded=True):
    rule_threshold = st.slider("Alert Threshold", 0, 150, 40)
    ml_threshold = st.slider("ML Threshold", 0.0, 1.0, 0.5, 0.05)

# -------------------------------------------------------------------
# REAL-TIME RULE ENGINE (unchanged)
# -------------------------------------------------------------------
df['R1_Fired'] = np.where(df['feat_3'] > th_high_val, 1, 0)
df['R2_Fired'] = np.where(df['feat_4'] <= th_zero_fee, 1, 0)
df['R3_Fired'] = np.where(df['time_step'] <= th_early_step, 1, 0)
df['R4_Fired'] = np.where((df['feat_3'] < 50.0) & (df['R1_Fired'] == 0), 1, 0)
df['R5_Fired'] = np.where(df['feat_100'] > th_agg, 1, 0)
df['R6_Fired'] = np.where(df['feat_10'] > 10.0, 1, 0)
df['R7_Fired'] = np.where(df['feat_15'] / (df['feat_20'] + 1e-6) > th_struct_ratio, 1, 0)

df['Dynamic_Rule_Score'] = (
    (df['R1_Fired'] * w_r1) + (df['R2_Fired'] * w_r2) + (df['R3_Fired'] * w_r3) +
    (df['R4_Fired'] * w_r4) + (df['R5_Fired'] * w_r5) + (df['R6_Fired'] * w_r6) +
    (df['R7_Fired'] * w_r7)
)

df['Final_Prediction'] = np.where(
    (df['Hybrid_Confidence'] >= ml_threshold) | (df['Dynamic_Rule_Score'] >= rule_threshold), 1, 0
)

# -------------------------------------------------------------------
# Metrics
# -------------------------------------------------------------------
y_true = df['True_Label']
y_pred = df['Final_Prediction']
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()
f1 = f1_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)
precision = precision_score(y_true, y_pred, zero_division=0)

# -------------------------------------------------------------------
# KPI Dashboard
# -------------------------------------------------------------------
st.markdown("<h2 style='font-size:1.5rem; font-weight:800;'>📊 Live Performance Metrics</h2>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">✅</div>
        <div class="kpi-value" style="color: var(--good);">{tp}</div>
        <div class="kpi-label">True Positives</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">❌</div>
        <div class="kpi-value" style="color: var(--bad);">{fn}</div>
        <div class="kpi-label">False Negatives</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-value" style="color: var(--warn);">{fp}</div>
        <div class="kpi-label">False Positives</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-value">{f1:.3f}</div>
        <div class="kpi-label">F1 Score</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-value">{recall:.1%}</div>
        <div class="kpi-label">Recall</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# Charts Section
# -------------------------------------------------------------------
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="card"><div class="card-title">📈 Decision Space Analysis</div></div>', unsafe_allow_html=True)

    plot_df = df.sample(n=min(2500, len(df)), random_state=42).copy()
    plot_df['Type'] = plot_df['True_Label'].map({1: 'Illicit', 0: 'Licit'})

    fig = px.scatter(
        plot_df, x="Dynamic_Rule_Score", y="Hybrid_Confidence", color="Type",
        opacity=0.65,
        color_discrete_map={'Illicit': '#FF6B6B', 'Licit': '#2ECC71'}
    )

    fig.update_layout(
        template=plot_template,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=plot_bg,
        margin=dict(l=0, r=0, t=25, b=0),
        height=460,
        font=dict(color="#E6E9EF" if theme == "dark" else "#131722")
    )
    fig.add_vline(x=rule_threshold, line_dash="dash", line_color="#00E5FF", line_width=2)
    fig.add_hline(y=ml_threshold, line_dash="dash", line_color="#00E5FF", line_width=2)

    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown('<div class="card"><div class="card-title">📊 Confusion Matrix</div></div>', unsafe_allow_html=True)

    # ====== HIGH-CONTRAST CONFUSION MATRIX COLORS ======
    if theme == "dark":
        cm_colors = [
            [0.0, "#101217"],
            [0.25, "#003644"],
            [0.5, "#007A99"],
            [0.75, "#00AEDD"],
            [1.0, "#00E5FF"]
        ]
        cm_text_color = "white"
        cm_grid = "rgba(255,255,255,0.22)"
    else:
        cm_colors = [
            [0.0, "#E8F1FF"],
            [0.25, "#C7DFFF"],
            [0.5, "#5BA9FF"],
            [0.75, "#1A73FF"],
            [1.0, "#003E9E"]
        ]
        cm_text_color = "#131722"
        cm_grid = "rgba(0,0,0,0.18)"

    fig_cm = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=['Pred Licit', 'Pred Illicit'],
            y=['True Licit', 'True Illicit'],
            colorscale=cm_colors,
            showscale=False,
            text=cm,
            texttemplate='%{text}',
            textfont={"size": 22, "color": cm_text_color},
            hoverinfo="skip"
        )
    )

    fig_cm.update_layout(
        template=plot_template,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=25, b=0),
        height=460,
        font=dict(color=cm_text_color)
    )

    fig_cm.update_xaxes(showgrid=True, gridcolor=cm_grid, zeroline=False)
    fig_cm.update_yaxes(showgrid=True, gridcolor=cm_grid, zeroline=False)

    st.plotly_chart(fig_cm, use_container_width=True)

# Optional small footer
st.markdown(
    f"<div style='margin-top:1rem; color:var(--muted);'>Precision: {precision:.2%} • "
    f"Rule Threshold: {rule_threshold} • ML Threshold: {ml_threshold:.2f}</div>",
    unsafe_allow_html=True
)

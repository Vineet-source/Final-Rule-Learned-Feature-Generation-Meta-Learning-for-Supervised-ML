import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score
from components.theme_toggle import render_theme_toggle, render_animated_background

st.set_page_config(
    page_title="Risk Appetite Tuner | Fraud Detection",
    layout="wide",
    page_icon="🎛️"
)

# -------------------------------------------------------------------
# Premium global layers
# -------------------------------------------------------------------
render_theme_toggle()
render_animated_background()

# keep session_state theme for Plotly
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
}
.light-theme {
  --bg: #F5F7FA;
  --text: #101525;
  --panel: rgba(0,0,0,0.06);
  --panel-strong: rgba(0,0,0,0.10);
}
.section-title { font-size: 1.35rem; font-weight: 700; margin: 0.2rem 0 0.6rem 0; }
.panel {
  background: var(--panel);
  border: 1px solid var(--panel-strong);
  border-radius: 18px;
  padding: 1rem 1.1rem;
  backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

st.title("🎛️ Risk Appetite Tuner")
st.caption("Tune rule definitions, weights, and ML thresholds live on historical data.")

# -------------------------------------------------------------------
# DATA LOADING (ROBUST)
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    # Try to find the file in likely locations
    possible_paths = [
        "simulation_data.csv",
        "../simulation_data.csv",
        "streamlit_app/simulation_data.csv"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    
    # If not found, return empty DF to prevent crash
    st.error("⚠️ simulation_data.csv not found. Please ensure it is uploaded to the repo root.")
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# -------------------------------------------------------------------
# TUNING SIDEBAR
# -------------------------------------------------------------------
with st.sidebar:
    st.header("🔧 Rule Config")
    
    st.subheader("Thresholds")
    th_ml = st.slider("ML Confidence (τ_ML)", 0.0, 1.0, 0.5, 0.05)
    th_rules = st.slider("Rule Score Threshold (τ_Rules)", 0, 100, 40, 5)
    
    st.markdown("---")
    st.subheader("Rule Definitions")
    th_high_val = st.number_input("R1: High Value (> $)", value=50000)
    th_agg = st.slider("R5: Aggregation >", 0.0, 5.0, 0.8)
    th_vel = st.slider("R6: Velocity >", 0.0, 50.0, 10.0)
    
    st.markdown("---")
    st.subheader("Weights")
    w_r1 = st.slider("W1 (High Value)", 0, 20, 15)
    w_r2 = st.slider("W2 (Zero Fee)", 0, 20, 10)
    w_r5 = st.slider("W5 (Aggregation)", 0, 20, 15)
    w_r6 = st.slider("W6 (Velocity)", 0, 20, 5)
    
    # Constants for untuned rules
    w_r3, w_r4, w_r7 = 5, 10, 10

# -------------------------------------------------------------------
# LOGIC ENGINE
# -------------------------------------------------------------------
def apply_logic(row):
    # Re-calculate rules based on new sliders
    r1 = 1 if row['feat_3'] > th_high_val else 0
    r2 = 1 if row['feat_4'] <= 0.0 else 0
    r5 = 1 if row['feat_100'] > th_agg else 0
    r6 = 1 if row['feat_10'] > th_vel else 0
    
    # Keep others static for demo simplicity (or add sliders for them too)
    r3 = 1 if row['time_step'] <= 5 else 0
    r4 = 1 if (row['feat_3'] < 50 and r1 == 0) else 0
    r7 = 1 if (row['feat_15'] / (row['feat_20'] + 1e-6)) > 2.0 else 0
    
    score = (r1*w_r1) + (r2*w_r2) + (r3*w_r3) + (r4*w_r4) + (r5*w_r5) + (r6*w_r6) + (r7*w_r7)
    
    # Hybrid Decision
    ml_fraud = row['Hybrid_Confidence'] >= th_ml
    rule_fraud = score >= th_rules
    
    return pd.Series([score, int(ml_fraud or rule_fraud), r1, r2, r3, r4, r5, r6, r7])

# Apply to sample
results = df.apply(apply_logic, axis=1)
results.columns = ['Score', 'Pred_Label', 'R1_Fired', 'R2_Fired', 'R3_Fired', 'R4_Fired', 'R5_Fired', 'R6_Fired', 'R7_Fired']
df_final = pd.concat([df, results], axis=1)

# -------------------------------------------------------------------
# KPIs
# -------------------------------------------------------------------
y_true = df_final['True_Label']
y_pred = df_final['Pred_Label']

f1 = f1_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
blocked = y_pred.sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Blocked Tx", int(blocked), delta_color="inverse")
k2.metric("Recall (Caught)", f"{rec:.1%}")
k3.metric("Precision", f"{prec:.1%}")
k4.metric("F1-Score", f"{f1:.1%}")

# -------------------------------------------------------------------
# VISUALIZATIONS
# -------------------------------------------------------------------
c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Score Distribution")
    fig_hist = px.histogram(
        df_final, x="Score", color="True_Label", 
        nbins=30, marginal="box", 
        color_discrete_map={0: "#00E5FF", 1: "#FF6B6B"},
        template=plot_template
    )
    fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=plot_bg)
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_true, y_pred)
    
    fig_cm = px.imshow(
        cm, text_auto=True, color_continuous_scale="Blues",
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=['Licit', 'Illicit'], y=['Licit', 'Illicit'],
        template=plot_template
    )
    fig_cm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=plot_bg)
    st.plotly_chart(fig_cm, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
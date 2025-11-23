import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score

st.set_page_config(
    page_title="Risk Appetite Tuner | Fraud Detection",
    layout="wide",
    page_icon="🎛️"
)

# Initialize theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

theme = st.session_state.theme

if theme == 'dark':
    bg, card_bg, text, accent, accent2 = "#0a0e27", "rgba(255,255,255,0.05)", "#ffffff", "#00d4ff", "#ff006e"
    plot_bg = "rgba(26, 29, 41, 0.5)"
else:
    bg, card_bg, text, accent, accent2 = "#f0f4f8", "rgba(255,255,255,0.9)", "#1a1a2e", "#0066ff", "#ff006e"
    plot_bg = "rgba(255, 255, 255, 0.5)"

# Themed CSS
st.markdown(f"""
<style>
@keyframes wave {{ 0%, 100% {{ transform: translateX(0); }} 50% {{ transform: translateX(-25%); }} }}
@keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}

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

.main .block-container {{ position: relative; z-index: 10 !important; padding: 2rem !important; }}

.page-title {{
  font-size: 2rem;
  font-weight: 700;
  color: {text};
  margin-bottom: 0.5rem;
}}

.page-subtitle {{
  font-size: 1rem;
  color: {text};
  opacity: 0.8;
  margin-bottom: 2rem;
}}

.kpi-card {{
  background: {card_bg};
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}}

.kpi-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 8px 16px {accent}40;
  border-color: {accent};
}}

.kpi-icon {{
  font-size: 2rem;
  margin-bottom: 0.75rem;
}}

.kpi-value {{
  font-size: 2rem;
  font-weight: 700;
  color: {text};
  margin-bottom: 0.5rem;
}}

.kpi-label {{
  font-size: 0.75rem;
  color: {text};
  opacity: 0.7;
  text-transform: uppercase;
}}

.card {{
  background: {card_bg};
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}}

.card-title {{
  font-size: 1.25rem;
  font-weight: 600;
  color: {text};
  margin-bottom: 1rem;
}}

.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{ color: {text} !important; }}

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

[data-testid="stSidebar"] .stMarkdown {{
    color: {text} !important;
}}

/* Slider styling */
.stSlider label {{
    color: {text} !important;
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

.stButton > button {{
  background: linear-gradient(135deg, {accent}, {accent2}) !important;
  color: white !important;
  border: none !important;
  border-radius: 50px !important;
  padding: 0.75rem 2rem !important;
  font-weight: 600 !important;
}}
</style>

<div class="particle p1"></div>
""", unsafe_allow_html=True)

# Page Header
st.markdown(f"""
<h1 class="page-title">🎛️ Risk Appetite Tuner</h1>
<p class="page-subtitle">
    Dynamically adjust rule thresholds and weights to see real-time impact on detection performance
</p>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("simulation_data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ simulation_data.csv not found. Please run hybrid_pipeline.py first.")
    st.stop()

# Sidebar Controls
st.sidebar.markdown(f"<h2 style='color: {text};'>🎛️ Policy Controls</h2>", unsafe_allow_html=True)

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

# Calculate Rules
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

# Calculate Metrics
y_true = df['True_Label']
y_pred = df['Final_Prediction']
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()
f1 = f1_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)

# KPI Dashboard
st.markdown(f"<h2 style='color: {text};'>📊 Live Performance Metrics</h2>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">✅</div>
        <div class="kpi-value" style="color: #00d25b;">{tp}</div>
        <div class="kpi-label">True Positives</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">❌</div>
        <div class="kpi-value" style="color: {accent2};">{fn}</div>
        <div class="kpi-label">False Negatives</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-value" style="color: #FFAB00;">{fp}</div>
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

# Charts Section
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown(f'<div class="card"><h3 class="card-title">📈 Decision Space Analysis</h3></div>', unsafe_allow_html=True)
    
    plot_df = df.sample(n=min(2500, len(df)), random_state=42).copy()
    plot_df['Type'] = plot_df['True_Label'].map({1: 'Illicit', 0: 'Licit'})
    
    fig = px.scatter(plot_df, x="Dynamic_Rule_Score", y="Hybrid_Confidence", color="Type",
                     opacity=0.6, color_discrete_map={'Illicit': accent2, 'Licit': '#00D25B'})
    
    fig.update_layout(template="plotly_dark" if theme == 'dark' else "plotly_white", 
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg,
                      margin=dict(l=0, r=0, t=20, b=0), height=450,
                      font=dict(color=text))
    fig.add_vline(x=rule_threshold, line_dash="dash", line_color=accent2, line_width=2)
    fig.add_hline(y=ml_threshold, line_dash="dash", line_color=accent2, line_width=2)
    
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown(f'<div class="card"><h3 class="card-title">📊 Confusion Matrix</h3></div>', unsafe_allow_html=True)
    
    fig_cm = go.Figure(data=go.Heatmap(z=cm, x=['Pred Licit', 'Pred Illicit'], y=['True Licit', 'True Illicit'],
                                        text=cm, texttemplate='%{text}', textfont={"size": 20, "color": "white"},
                                        colorscale=[[0, plot_bg], [1, accent2]], showscale=False))
    
    fig_cm.update_layout(template="plotly_dark" if theme == 'dark' else "plotly_white",
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg,
                         margin=dict(l=0, r=0, t=20, b=0), height=450,
                         font=dict(color=text))
    
    st.plotly_chart(fig_cm, use_container_width=True)

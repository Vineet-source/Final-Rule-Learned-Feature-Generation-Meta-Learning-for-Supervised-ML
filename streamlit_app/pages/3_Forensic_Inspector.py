import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Forensic Inspector | Fraud Detection",
    layout="wide",
    page_icon="🔍"
)

# Initialize theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

theme = st.session_state.theme

if theme == 'dark':
    bg, card_bg, text, accent, accent2 = "#0a0e27", "rgba(255,255,255,0.05)", "#ffffff", "#00d4ff", "#ff006e"
    plot_bg = "rgba(26, 29, 41, 0.5)"
    radio_bg = "rgba(0, 0, 0, 0.3)"
else:
    bg, card_bg, text, accent, accent2 = "#f0f4f8", "rgba(255,255,255,0.9)", "#1a1a2e", "#0066ff", "#ff006e"
    plot_bg = "rgba(255, 255, 255, 0.5)"
    radio_bg = "rgba(0, 0, 0, 0.05)"

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

/* Radio button styling */
.stRadio > label {{
    color: {text} !important;
    font-weight: 600 !important;
}}

.stRadio > div {{
    background: {radio_bg} !important;
    padding: 1rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}}

.stRadio > div > label {{
    color: {text} !important;
    background: {card_bg} !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    margin: 0.25rem !important;
    transition: all 0.3s ease !important;
}}

.stRadio > div > label:hover {{
    border-color: {accent} !important;
    transform: translateY(-2px) !important;
}}

.stRadio > div > label > div {{
    color: {text} !important;
}}

/* Selectbox styling */
.stSelectbox label {{
    color: {text} !important;
    font-weight: 600 !important;
}}

.stSelectbox > div > div {{
    background: {card_bg} !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: {text} !important;
}}

.stSelectbox > div > div > div {{
    color: {text} !important;
}}

/* Metric styling */
.stMetric {{
    background: {card_bg} !important;
    backdrop-filter: blur(20px) !important;
    padding: 1rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}}

.stMetric label {{
    color: {text} !important;
}}

.stMetric [data-testid="stMetricValue"] {{
    color: {text} !important;
}}

/* Dataframe styling */
.dataframe {{
    background: {card_bg} !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 12px !important;
    color: {text} !important;
}}

.dataframe th {{
    background: {radio_bg} !important;
    color: {text} !important;
}}

.dataframe td {{
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
<h1 class="page-title">🔍 Forensic Transaction Inspector</h1>
<p class="page-subtitle">
    Deep-dive into specific cases to understand decision logic and rule triggers
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

# Use default thresholds
th_high_val, th_zero_fee, th_early_step, th_agg, th_struct_ratio = 50000.0, 0.0, 5, 0.8, 2.0
w_r1, w_r2, w_r3, w_r4, w_r5, w_r6, w_r7 = 15, 10, 5, 10, 15, 5, 10
rule_threshold, ml_threshold = 40, 0.5

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

# Case Type Selection
st.markdown(f'<div class="card"><h3 class="card-title">🎯 Select Case Type</h3></div>', unsafe_allow_html=True)

case_type = st.radio(
    "Case Type",
    ["False Positives (flagged licit)", "False Negatives (missed illicit)", 
     "True Positives (caught illicit)", "True Negatives (correctly cleared)"],
    horizontal=True,
    label_visibility="collapsed"
)

# Filter data
if "False Positives" in case_type:
    subset = df[(df['Final_Prediction'] == 1) & (df['True_Label'] == 0)]
elif "False Negatives" in case_type:
    subset = df[(df['Final_Prediction'] == 0) & (df['True_Label'] == 1)]
elif "True Positives" in case_type:
    subset = df[(df['Final_Prediction'] == 1) & (df['True_Label'] == 1)]
else:
    subset = df[(df['Final_Prediction'] == 0) & (df['True_Label'] == 0)]

# Display statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Cases", len(subset))
with col2:
    avg_rule = subset['Dynamic_Rule_Score'].mean() if len(subset) > 0 else 0
    st.metric("Avg Rule Score", f"{avg_rule:.1f}")
with col3:
    avg_ml = subset['Hybrid_Confidence'].mean() if len(subset) > 0 else 0
    st.metric("Avg ML Probability", f"{avg_ml:.1%}")

st.markdown("---")

# Transaction Selection
if subset.empty:
    st.info("ℹ️ No transactions found in this category")
else:
    subset = subset.copy()
    subset['Label'] = (
        "Tx #" + subset.index.astype(str) +
        " | Score: " + subset['Dynamic_Rule_Score'].astype(int).astype(str) +
        " | ML: " + (subset['Hybrid_Confidence']*100).round(0).astype(int).astype(str) + "%"
    )
    
    st.markdown(f'<div class="card"><h3 class="card-title">🔍 Select Transaction</h3></div>', unsafe_allow_html=True)
    
    selected_label = st.selectbox("Transaction", subset['Label'].head(50), label_visibility="collapsed")
    selected_idx = int(selected_label.split(" |")[0].split("#")[1])
    
    row = df.loc[selected_idx]
    
    st.markdown("---")
    
    # Transaction Details
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="card"><h3 class="card-title">📝 Transaction Profile</h3></div>', unsafe_allow_html=True)
        
        st.metric("Transaction Index", selected_idx)
        st.metric("Rule Score", f"{row['Dynamic_Rule_Score']:.0f}")
        st.metric("ML Probability", f"{row['Hybrid_Confidence']:.1%}")
        
        st.markdown("---")
        
        actual = "🔴 Illicit" if row['True_Label'] == 1 else "🟢 Licit"
        predicted = "🔴 Illicit" if row['Final_Prediction'] == 1 else "🟢 Licit"
        
        st.markdown(f"<p style='color: {text};'><strong>Actual:</strong> {actual}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {text};'><strong>Predicted:</strong> {predicted}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<p style='color: {text};'><strong>Key Features:</strong></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {text};'>- Amount: {row['feat_3']:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {text};'>- Fee: {row['feat_4']:.4f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {text};'>- Time Step: {row['time_step']}</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="card"><h3 class="card-title">⚙️ Rule Contribution Breakdown</h3></div>', unsafe_allow_html=True)
        
        contrib_data = {
            'Rule': ['High Value (R1)', 'Zero Fee (R2)', 'Early Time (R3)', 'Low Value (R4)',
                    'Neighbor Agg (R5)', 'High Velocity (R6)', 'Structural (R7)'],
            'Contribution': [
                row['R1_Fired'] * w_r1, row['R2_Fired'] * w_r2, row['R3_Fired'] * w_r3,
                row['R4_Fired'] * w_r4, row['R5_Fired'] * w_r5, row['R6_Fired'] * w_r6,
                row['R7_Fired'] * w_r7
            ],
            'Fired': [row['R1_Fired'], row['R2_Fired'], row['R3_Fired'], row['R4_Fired'],
                     row['R5_Fired'], row['R6_Fired'], row['R7_Fired']]
        }
        contrib_df = pd.DataFrame(contrib_data)
        colors = [accent2 if x == 1 else text for x in contrib_df['Fired']]
        
        fig = go.Figure(data=[go.Bar(y=contrib_df['Rule'], x=contrib_df['Contribution'],
                                     orientation='h', marker=dict(color=colors),
                                     text=contrib_df['Contribution'], textposition='auto')])
        
        fig.update_layout(template="plotly_dark" if theme == 'dark' else "plotly_white",
                         paper_bgcolor='rgba(0,0,0,0)',
                         plot_bgcolor=plot_bg, height=400,
                         margin=dict(l=0, r=0, t=20, b=0), showlegend=False,
                         xaxis_title="Contribution", yaxis_title="",
                         font=dict(color=text))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown(f"<p style='color: {text};'><strong>Rule Status:</strong></p>", unsafe_allow_html=True)
        rule_status = pd.DataFrame({
            'Rule': contrib_df['Rule'],
            'Status': ['🔴 Fired' if x == 1 else '⚪ Not Fired' for x in contrib_df['Fired']],
            'Contribution': contrib_df['Contribution']
        })
        st.dataframe(rule_status, use_container_width=True, hide_index=True)

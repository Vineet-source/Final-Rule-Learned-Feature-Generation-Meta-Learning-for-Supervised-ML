import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

from components.theme_toggle import render_theme_toggle, render_animated_background

st.set_page_config(
    page_title="Forensic Inspector | Fraud Detection",
    layout="wide",
    page_icon="🔍"
)

# ---------------------------
# Theme & Layers
# ---------------------------
render_theme_toggle()
render_animated_background()

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme = st.session_state.theme
plot_template = "plotly_dark" if theme == "dark" else "plotly_white"
plot_bg = "rgba(26,29,41,0.55)" if theme == "dark" else "rgba(255,255,255,0.75)"
text_color = "#E6E9EF" if theme == "dark" else "#1A1A2E"

st.markdown("""
<style>
:root {
  --panel: rgba(255,255,255,0.06);
  --panel-strong: rgba(255,255,255,0.10);
}
.light-theme {
  --panel: rgba(0,0,0,0.06);
  --panel-strong: rgba(0,0,0,0.10);
}
.panel {
  background: var(--panel);
  border: 1px solid var(--panel-strong);
  border-radius: 18px;
  padding: 1rem;
  backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Forensic Inspector")

# ---------------------------
# DATA LOADING (ROBUST)
# ---------------------------
@st.cache_data
def load_data():
    possible_paths = ["simulation_data.csv", "../simulation_data.csv", "streamlit_app/simulation_data.csv"]
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    st.error("Data file not found.")
    return pd.DataFrame()

df = load_data()
if df.empty: st.stop()

# ---------------------------
# SELECTOR
# ---------------------------
col_sel, col_info = st.columns([1, 3])

with col_sel:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Select Case")
    # Filter for interesting cases (High risk or False Positives)
    mask = (df['Hybrid_Confidence'] > 0.3) | (df['True_Label'] == 1)
    filtered_df = df[mask].reset_index()
    
    case_id = st.selectbox(
        "Choose Transaction Index",
        filtered_df.index,
        format_func=lambda x: f"Tx #{x} (Conf: {filtered_df.loc[x, 'Hybrid_Confidence']:.2f})"
    )
    st.markdown("</div>", unsafe_allow_html=True)

row = filtered_df.loc[case_id]

# ---------------------------
# ANALYSIS VIEW
# ---------------------------
# Simulate Rule Firing (Hardcoded logic for viz, ideally matches backend)
w_r1, w_r2, w_r3, w_r4, w_r5, w_r6, w_r7 = 15, 10, 5, 10, 15, 5, 10

# Calculate firings locally for inspection
r1 = 1 if row['feat_3'] > 50000 else 0
r2 = 1 if row['feat_4'] <= 0 else 0
r5 = 1 if row['feat_100'] > 0.8 else 0
# ... (simplified for viz)

with col_info:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Overview")
        
        score = (r1*w_r1 + r2*w_r2 + r5*w_r5) # Partial sum for demo
        
        st.metric("Rule Score (Est)", f"{score}")
        st.metric("ML Probability", f"{row['Hybrid_Confidence']:.1%}")
        st.markdown(f"**Actual:** {'🔴 Illicit' if row['True_Label']==1 else '🟢 Licit'}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Rule Contribution")
        
        # Mock data for the graph
        contrib_data = {
            'Rule': ["High Val (R1)", "Zero Fee (R2)", "Agg (R5)"],
            'Contribution': [r1*w_r1, r2*w_r2, r5*w_r5],
            'Fired': [r1, r2, r5]
        }
        
        colors = ['#FF6B6B' if x == 1 else '#7A8191' for x in contrib_data['Fired']]
        
        fig = go.Figure(go.Bar(
            y=contrib_data['Rule'],
            x=contrib_data['Contribution'],
            orientation='h',
            marker_color=colors
        ))
        fig.update_layout(
            template=plot_template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plot_bg,
            font=dict(color=text_color),
            height=250,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
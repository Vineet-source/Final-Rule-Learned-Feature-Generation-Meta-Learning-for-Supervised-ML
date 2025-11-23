import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Forensic Inspector | Fraud Detection",
    layout="wide",
    page_icon="🔍"
)

# ---------------------------
# Theme init (reuse your app theme state)
# ---------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme = st.session_state.theme

if theme == "dark":
    bg, text = "#0A0E1A", "#E6E9EF"
    card_bg = "rgba(255,255,255,0.06)"
    accent, accent2 = "#7C5CFF", "#00E5FF"
    plot_bg = "rgba(12,18,30,0.6)"
else:
    bg, text = "#F5F7FA", "#1A1A2E"
    card_bg = "rgba(0,0,0,0.06)"
    accent, accent2 = "#6C4BFF", "#00A7D6"
    plot_bg = "rgba(255,255,255,0.6)"

# ---------------------------
# Premium CSS (closed blocks)
# ---------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Inter:wght@400;500;600&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

html, body, [class*="css"] {{
    background: {bg} !important;
    color: {text} !important;
    font-family: 'Inter', sans-serif;
}}

.aura {{
  position: fixed;
  inset: -20%;
  z-index: 0;
  background:
    radial-gradient(900px circle at 10% 5%, {accent}33, transparent 60%),
    radial-gradient(900px circle at 90% 10%, {accent2}33, transparent 60%),
    radial-gradient(1200px circle at 50% 100%, rgba(255,255,255,0.07), transparent 60%);
  animation: auramove 15s ease-in-out infinite;
  filter: blur(48px);
  opacity: .95;
  pointer-events: none;
}}
@keyframes auramove {{
  0% {{ transform: translateY(0px) translateX(0px); }}
  50% {{ transform: translateY(-28px) translateX(22px) scale(1.06); }}
  100% {{ transform: translateY(0px) translateX(0px); }}
}}

.particle {{
  position: fixed;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  background: radial-gradient(circle, {accent}25 0%, transparent 70%);
  top: 12%; left: 12%;
  animation: float 8s ease-in-out infinite;
  pointer-events: none;
  z-index: 0;
}}
@keyframes float {{
  0%, 100% {{ transform: translateY(0px); }}
  50% {{ transform: translateY(-25px); }}
}}

.main .block-container {{
    position: relative;
    z-index: 5 !important;
    padding-top: 2rem !important;
}}

.page-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2rem;
    letter-spacing: .6px;
    margin-bottom: .25rem;
}}
.page-subtitle {{
    font-size: 1rem;
    opacity: .75;
    margin-bottom: 2rem;
}}

.card {{
  background: {card_bg};
  backdrop-filter: blur(18px);
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  padding: 1.4rem;
  margin-bottom: 1.4rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  transition: all .25s ease;
}}
.card:hover {{
  transform: translateY(-6px);
  border-color: {accent};
  box-shadow: 0 12px 40px rgba(0,0,0,0.45), 0 0 25px {accent}44;
}}
.card-title {{
  font-family: 'Orbitron';
  font-size: 1.3rem;
  margin-bottom: 1rem;
}}

.stMetric {{
  background: {card_bg};
  backdrop-filter: blur(20px);
  border-radius: 14px;
  padding: 1rem;
  border: 1px solid rgba(255,255,255,0.08);
}}

[data-testid="stSidebar"] {{
  background: {card_bg} !important;
  backdrop-filter: blur(24px);
  border-right: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 0 30px {accent}55, 0 0 40px {accent2}55;
}}
</style>

<div class="aura"></div>
<div class="particle"></div>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<h1 class="page-title">🔍 Forensic Transaction Inspector</h1>
<p class="page-subtitle">Deep-dive into cases to understand decision logic and rule triggers.</p>
""", unsafe_allow_html=True)

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("simulation_data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ simulation_data.csv not found. Please run hybrid_pipeline.py first.")
    st.stop()

# ---------------------------
# Guard for missing columns (prevents silent crashes)
# ---------------------------
required_cols = {
    "feat_3","feat_4","feat_100","feat_10","feat_15","feat_20",
    "time_step","Hybrid_Confidence","True_Label"
}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"❌ Your CSV is missing required columns: {sorted(missing)}")
    st.stop()

# ---------------------------
# Thresholds + weights
# ---------------------------
th_high_val, th_zero_fee, th_early_step, th_agg, th_struct_ratio = 50000.0, 0.0, 5, 0.8, 2.0
w_r1, w_r2, w_r3, w_r4, w_r5, w_r6, w_r7 = 15, 10, 5, 10, 15, 5, 10
rule_threshold, ml_threshold = 40, 0.5

# ---------------------------
# Rules
# ---------------------------
df["R1_Fired"] = (df["feat_3"] > th_high_val).astype(int)
df["R2_Fired"] = (df["feat_4"] <= th_zero_fee).astype(int)
df["R3_Fired"] = (df["time_step"] <= th_early_step).astype(int)
df["R4_Fired"] = ((df["feat_3"] < 50.0) & (df["R1_Fired"] == 0)).astype(int)
df["R5_Fired"] = (df["feat_100"] > th_agg).astype(int)
df["R6_Fired"] = (df["feat_10"] > 10.0).astype(int)
df["R7_Fired"] = ((df["feat_15"] / (df["feat_20"] + 1e-6)) > th_struct_ratio).astype(int)

df["Dynamic_Rule_Score"] = (
    df["R1_Fired"]*w_r1 + df["R2_Fired"]*w_r2 + df["R3_Fired"]*w_r3 +
    df["R4_Fired"]*w_r4 + df["R5_Fired"]*w_r5 + df["R6_Fired"]*w_r6 +
    df["R7_Fired"]*w_r7
)

df["Final_Prediction"] = np.where(
    (df["Hybrid_Confidence"] >= ml_threshold) |
    (df["Dynamic_Rule_Score"] >= rule_threshold),
    1, 0
)

# ---------------------------
# Case type selection
# ---------------------------
st.markdown("""
<div class="card">
  <div class="card-title">🎯 Select Case Type</div>
</div>
""", unsafe_allow_html=True)

case_type = st.radio(
    "Case Type",
    ["False Positives (flagged licit)",
     "False Negatives (missed illicit)",
     "True Positives (caught illicit)",
     "True Negatives (correctly cleared)"],
    horizontal=True,
    label_visibility="collapsed"
)

if "False Positives" in case_type:
    subset = df[(df["Final_Prediction"]==1) & (df["True_Label"]==0)]
elif "False Negatives" in case_type:
    subset = df[(df["Final_Prediction"]==0) & (df["True_Label"]==1)]
elif "True Positives" in case_type:
    subset = df[(df["Final_Prediction"]==1) & (df["True_Label"]==1)]
else:
    subset = df[(df["Final_Prediction"]==0) & (df["True_Label"]==0)]

# ---------------------------
# Stats
# ---------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Total Cases", len(subset))
c2.metric("Avg Rule Score", f"{subset['Dynamic_Rule_Score'].mean():.1f}" if len(subset) else "0")
c3.metric("Avg ML Probability", f"{subset['Hybrid_Confidence'].mean():.1%}" if len(subset) else "0%")

st.markdown("---")

# ---------------------------
# Transaction selection
# ---------------------------
if subset.empty:
    st.info("ℹ️ No transactions found in this category.")
    st.stop()

subset = subset.copy()
subset["Label"] = (
    "Tx #" + subset.index.astype(str) +
    " | Score: " + subset["Dynamic_Rule_Score"].astype(int).astype(str) +
    " | ML: " + (subset["Hybrid_Confidence"]*100).round(0).astype(int).astype(str) + "%"
)

st.markdown("""
<div class="card">
  <div class="card-title">🔍 Select Transaction</div>
</div>
""", unsafe_allow_html=True)

selected_label = st.selectbox("Transaction", subset["Label"].head(50), label_visibility="collapsed")
selected_idx = int(selected_label.split(" |")[0].split("#")[1])
row = df.loc[selected_idx]

st.markdown("---")

# ---------------------------
# Layout
# ---------------------------
left, right = st.columns([1, 2])

with left:
    st.markdown("""
    <div class="card">
      <div class="card-title">📝 Transaction Profile</div>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Transaction Index", selected_idx)
    st.metric("Rule Score", f"{row['Dynamic_Rule_Score']:.0f}")
    st.metric("ML Probability", f"{row['Hybrid_Confidence']:.1%}")

    st.markdown("---")
    actual = "🔴 Illicit" if row["True_Label"]==1 else "🟢 Licit"
    predicted = "🔴 Illicit" if row["Final_Prediction"]==1 else "🟢 Licit"
    st.write("**Actual:**", actual)
    st.write("**Predicted:**", predicted)

    st.markdown("---")
    st.write("**Key Features:**")
    st.write(f"- Amount: {row['feat_3']:.2f}")
    st.write(f"- Fee: {row['feat_4']:.4f}")
    st.write(f"- Time Step: {int(row['time_step'])}")

with right:
    st.markdown("""
    <div class="card">
      <div class="card-title">⚙️ Rule Contribution Breakdown</div>
    </div>
    """, unsafe_allow_html=True)

    contrib_df = pd.DataFrame({
        "Rule": ["High Value (R1)", "Zero Fee (R2)", "Early Time (R3)", "Low Value (R4)",
                 "Neighbor Agg (R5)", "High Velocity (R6)", "Structural (R7)"],
        "Contribution": [
            row["R1_Fired"]*w_r1, row["R2_Fired"]*w_r2, row["R3_Fired"]*w_r3,
            row["R4_Fired"]*w_r4, row["R5_Fired"]*w_r5, row["R6_Fired"]*w_r6,
            row["R7_Fired"]*w_r7
        ],
        "Fired": [
            row["R1_Fired"], row["R2_Fired"], row["R3_Fired"], row["R4_Fired"],
            row["R5_Fired"], row["R6_Fired"], row["R7_Fired"]
        ]
    })

    colors = [accent2 if f==1 else text for f in contrib_df["Fired"]]

    fig = go.Figure(go.Bar(
        y=contrib_df["Rule"],
        x=contrib_df["Contribution"],
        orientation="h",
        marker=dict(color=colors, line=dict(color=accent2, width=1)),
        text=contrib_df["Contribution"],
        textposition="auto"
    ))

    fig.update_layout(
        template="plotly_dark" if theme=="dark" else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=plot_bg,
        font=dict(color=text),
        height=420,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Contribution",
        yaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.dataframe(
        pd.DataFrame({
            "Rule": contrib_df["Rule"],
            "Status": ["🔴 Fired" if x==1 else "⚪ Not Fired" for x in contrib_df["Fired"]],
            "Contribution": contrib_df["Contribution"]
        }),
        use_container_width=True,
        hide_index=True
    )

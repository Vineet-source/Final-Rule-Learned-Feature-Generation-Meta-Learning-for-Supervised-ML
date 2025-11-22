import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import confusion_matrix, f1_score, recall_score

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
hr { border:none; height:1px; background: rgba(255,255,255,0.08); margin: 1rem 0; }
small { color: #AAB0BC; }
</style>
""", unsafe_allow_html=True)

st.title("🎛️ Risk Appetite Tuner")
st.caption("Tune rule definitions, weights, and ML threshold — see impact in real time.")

# ---------- Load Data ----------
@st.cache_data
def load_data():
    return pd.read_csv("simulation_data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("simulation_data.csv not found. Please run hybrid_pipeline.py first.")
    st.stop()

# ---------- Sidebar ----------
st.sidebar.title("Policy Controls")

with st.sidebar.expander("1) Rule Definitions (Thresholds)", expanded=True):
    th_high_val = st.slider("R1: High Value Amount (>)", 1000.0, 100000.0, 50000.0, 1000.0)
    th_zero_fee = st.slider("R2: Zero Fee Limit (<=)", 0.0, 1.0, 0.0, 0.1)
    th_early_step = st.slider("R3: Early Time Step (<=)", 1, 10, 5)
    th_agg = st.slider("R5: Neighbor Aggregation (>)", 0.1, 5.0, 0.8, 0.1)
    th_struct_ratio = st.slider("R7: Structural Anomaly Ratio (>)", 1.0, 5.0, 2.0, 0.1)

with st.sidebar.expander("2) Rule Importance (Weights)", expanded=True):
    w_r1 = st.slider("Weight: High Value (R1)", 0, 50, 15)
    w_r2 = st.slider("Weight: Zero Fee (R2)", 0, 50, 10)
    w_r3 = st.slider("Weight: Early Step (R3)", 0, 50, 5)
    w_r4 = st.slider("Weight: Low Value Structuring (R4)", 0, 50, 10)
    w_r5 = st.slider("Weight: Neighbor Agg (R5)", 0, 50, 15)
    w_r6 = st.slider("Weight: High Velocity (R6)", 0, 50, 5)
    w_r7 = st.slider("Weight: Structural (R7)", 0, 50, 10)

with st.sidebar.expander("3) Decision Boundary", expanded=True):
    rule_threshold = st.slider("Alert Threshold (Total Score)", 0, 150, 40)
    ml_threshold = st.slider("ML Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

# ---------- REAL-TIME CALCULATION ENGINE (same logic) ----------
df['R1_Fired'] = np.where(df['feat_3'] > th_high_val, 1, 0)
df['R2_Fired'] = np.where(df['feat_4'] <= th_zero_fee, 1, 0)
df['R3_Fired'] = np.where(df['time_step'] <= th_early_step, 1, 0)
df['R4_Fired'] = np.where((df['feat_3'] < 50.0) & (df['R1_Fired'] == 0), 1, 0)
df['R5_Fired'] = np.where(df['feat_100'] > th_agg, 1, 0)
df['R6_Fired'] = np.where(df['feat_10'] > 10.0, 1, 0)
df['R7_Fired'] = np.where(df['feat_15'] / (df['feat_20'] + 1e-6) > th_struct_ratio, 1, 0)

df['Dynamic_Rule_Score'] = (
    (df['R1_Fired'] * w_r1) +
    (df['R2_Fired'] * w_r2) +
    (df['R3_Fired'] * w_r3) +
    (df['R4_Fired'] * w_r4) +
    (df['R5_Fired'] * w_r5) +
    (df['R6_Fired'] * w_r6) +
    (df['R7_Fired'] * w_r7)
)

df['Final_Prediction'] = np.where(
    (df['Hybrid_Confidence'] >= ml_threshold) |
    (df['Dynamic_Rule_Score'] >= rule_threshold),
    1, 0
)

# ---------- Metrics ----------
y_true = df['True_Label']
y_pred = df['Final_Prediction']
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()

f1 = f1_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)

st.markdown("<div class='section-title'>Live KPIs</div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("TP (Caught Fraud)", f"{tp}")
k2.metric("FN (Missed Fraud)", f"{fn}")
k3.metric("FP (False Alarms)", f"{fp}")
k4.metric("F1 Score", f"{f1:.3f}")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- Charts ----------
c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='section-title'>Logic Distribution (Brain Scan)</div>", unsafe_allow_html=True)
    plot_df = df.sample(n=min(2500, len(df)), random_state=42).copy()
    plot_df['Type'] = plot_df['True_Label'].map({1: 'Illicit (Real)', 0: 'Licit (Real)'})

    fig = px.scatter(
        plot_df, x="Dynamic_Rule_Score", y="Hybrid_Confidence", color="Type",
        opacity=0.7, title="Where do the Model and Rules Agree?"
    )
    fig.update_layout(
        template="plotly_dark",
        legend_title_text="True Class",
        margin=dict(l=0, r=0, t=40, b=0),
        height=480
    )
    fig.add_vline(x=rule_threshold, line_dash="dash", line_color="rgba(46,204,113,0.9)")
    fig.add_hline(y=ml_threshold, line_dash="dash", line_color="rgba(46,204,113,0.9)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("<div class='section-title'>Confusion Matrix</div>", unsafe_allow_html=True)
    fig_cm = px.imshow(
        cm, text_auto=True,
        x=['Pred Licit', 'Pred Illicit'],
        y=['True Licit', 'True Illicit'],
        color_continuous_scale='Blues'
    )
    fig_cm.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=0),
        height=480
    )
    st.plotly_chart(fig_cm, use_container_width=True)

# ---------- Forensic Inspector ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔍 Forensic Transaction Inspector</div>", unsafe_allow_html=True)
st.caption("Select a case type and inspect individual transactions.")

case_type = st.radio(
    "Case Type",
    ["False Positives (flagged licit)", "False Negatives (missed illicit)", "True Positives (caught illicit)"],
    horizontal=True
)

if "False Positives" in case_type:
    subset = df[(df['Final_Prediction'] == 1) & (df['True_Label'] == 0)]
elif "False Negatives" in case_type:
    subset = df[(df['Final_Prediction'] == 0) & (df['True_Label'] == 1)]
else:
    subset = df[(df['Final_Prediction'] == 1) & (df['True_Label'] == 1)]

if subset.empty:
    st.info("No transactions found in this category under current thresholds.")
else:
    subset = subset.copy()
    subset['Label'] = (
        "Tx Index: " + subset.index.astype(str) +
        " | Score: " + subset['Dynamic_Rule_Score'].astype(int).astype(str) +
        " | ML: " + (subset['Hybrid_Confidence']*100).round(0).astype(int).astype(str) + "%"
    )
    selected_label = st.selectbox("Pick a transaction", subset['Label'].head(25))
    selected_idx = int(selected_label.split(" |")[0].split(": ")[1])

    row = df.loc[selected_idx]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Transaction Profile")
        st.metric("Rule Score", f"{row['Dynamic_Rule_Score']:.1f}")
        st.metric("ML Probability", f"{row['Hybrid_Confidence']:.1%}")
        st.markdown(f"**Actual:** {'🔴 Illicit' if row['True_Label']==1 else '🟢 Licit'}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Rule Breakdown")

        contrib_data = {
            'Rule': ['High Val (R1)', 'Zero Fee (R2)', 'Early (R3)', 'Struct (R4)', 'Agg (R5)', 'Vel (R6)', 'Anom (R7)'],
            'Contribution': [
                row['R1_Fired'] * w_r1, row['R2_Fired'] * w_r2, row['R3_Fired'] * w_r3,
                row['R4_Fired'] * w_r4, row['R5_Fired'] * w_r5, row['R6_Fired'] * w_r6,
                row['R7_Fired'] * w_r7
            ],
            'Fired?': [row[c] for c in ['R1_Fired','R2_Fired','R3_Fired','R4_Fired','R5_Fired','R6_Fired','R7_Fired']]
        }
        contrib_df = pd.DataFrame(contrib_data)
        colors = ['#FF6B6B' if x == 1 else '#7A8191' for x in contrib_df['Fired?']]

        fig_breakdown = px.bar(
            contrib_df, x='Contribution', y='Rule', orientation='h',
            title="Which rules triggered this decision?",
            text='Contribution'
        )
        fig_breakdown.update_traces(marker_color=colors)
        fig_breakdown.update_layout(template="plotly_dark", height=420, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig_breakdown, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

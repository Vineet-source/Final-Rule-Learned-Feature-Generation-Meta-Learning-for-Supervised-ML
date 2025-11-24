import streamlit as st
from components.theme_toggle import render_theme_toggle, render_animated_background

# --------------------------------------------
# 1. Page Config
# --------------------------------------------
st.set_page_config(
    page_title="Hybrid Fraud Detection",
    layout="wide",
    page_icon="⚡"
)

# --------------------------------------------
# 2. Cloud Deployment URL Logic (FIXED)
# --------------------------------------------
# Default to localhost for local testing
default_url = "http://localhost:8000/transactions"

# We wrap this in try-except because checking st.secrets crashes locally if no file exists
try:
    if "API_URL" in st.secrets:
        default_url = st.secrets["API_URL"]
except Exception:
    # If secrets.toml is missing (running locally), we just keep the default_url
    pass

# Store in Session State so other pages (Risk Tuner, Verification) can access it
if "api_url" not in st.session_state:
    st.session_state["api_url"] = default_url

# Optional: Show the connected backend in sidebar (read-only)
with st.sidebar:
    st.header("🔌 System Config")
    st.text_input("Backend API", value=st.session_state["api_url"], disabled=True, help="Loaded from secrets")


# --------------------------------------------
# 3. Theme & Background (Imported from components)
# --------------------------------------------
render_theme_toggle()
render_animated_background()


# --------------------------------------------
# 4. PREMIUM GLOBAL CSS & ANIMATIONS
# --------------------------------------------
st.markdown("""
<style>

/* PREMIUM FONTS */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* DESIGN TOKENS */
:root {
  --bg: #0B0E14;
  --panel: rgba(255,255,255,0.06);
  --panel-strong: rgba(255,255,255,0.10);
  --text: #E6E9EF;
  --muted: #AAB0BC;
  --accent: #7C5CFF;
  --accent-2: #00E5FF;
  --glow-1: rgba(124,92,255,0.55);
  --glow-2: rgba(0,229,255,0.45);
}
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

html, body, [class*="css"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: "Inter", system-ui, sans-serif;
}

/* Hide default UI but KEEP sidebar */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}


/* AURA BACKGROUND */
.aura {
  position: fixed;
  inset: -25%;
  z-index: 0;
  background:
    radial-gradient(900px circle at 10% 5%, var(--glow-1), transparent 60%),
    radial-gradient(900px circle at 95% 10%, var(--glow-2), transparent 60%),
    radial-gradient(1200px circle at 50% 100%, rgba(255,255,255,0.1), transparent 70%);
  animation: auraShift 16s ease-in-out infinite;
  filter: blur(50px);
  opacity: 0.95;
  pointer-events: none;
}
@keyframes auraShift {
  0% { transform: translate(0,0) scale(1); }
  50% { transform: translate(-30px,25px) scale(1.05); }
  100% { transform: translate(0,0) scale(1); }
}


/* UFO DRONE */
.fraud-drone-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 3;
}
.fraud-drone {
  position: absolute;
  font-size: 140px;
  animation: droneFly 22s linear infinite;
  filter:
    drop-shadow(0 0 25px var(--accent-2))
    drop-shadow(0 0 45px var(--accent));
}
.fraud-drone::before {
  content: "◯";
  position: absolute;
  top: -80px; left: -30px;
  font-size: 210px; color: var(--accent-2);
  opacity: 0.4;
  animation: rotateRing 6s linear infinite;
  filter: blur(1px);
}
.fraud-drone::after {
  content: "";
  position: absolute;
  top: 110px; left: 50px;
  width: 70px; height: 430px;
  background: linear-gradient(180deg, transparent, rgba(0,229,255,0.85), rgba(124,92,255,0.7), transparent);
  opacity: 0.8; filter: blur(3px);
  mix-blend-mode: screen;
  animation: beamPulse 2.2s ease-in-out infinite;
}

@keyframes droneFly {
  0%   { transform: translate(3vw, 7vh) rotate(6deg); }
  25%  { transform: translate(80vw, 6vh) rotate(8deg); }
  50%  { transform: translate(88vw, 40vh) rotate(-6deg); }
  75%  { transform: translate(18vw, 32vh) rotate(-12deg); }
  100% { transform: translate(3vw, 7vh) rotate(6deg); }
}
@keyframes rotateRing { to { transform: rotate(360deg); } }
@keyframes beamPulse {
  0%,100% { opacity: .4; height: 300px; }
  50%     { opacity: 1; height: 440px; }
}


/* FLOATING BITCOINS */
.coin-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}
.coin {
  position: absolute;
  font-size: 44px;
  color: gold;
  opacity: 0.9;
  animation: coinFloat 12s ease-in-out infinite;
}
@keyframes coinFloat {
  0%,100% { transform: translateY(0) rotate(0); opacity: 0.5; }
  50%     { transform: translateY(-45px) rotate(180deg); opacity: 1; }
}
.coin-1 { top: 18%; left: 9%; }
.coin-2 { top: 32%; left: 70%; animation-duration: 14s; }
.coin-3 { top: 75%; left: 16%; animation-duration: 15s; }
.coin-4 { top: 64%; left: 85%; animation-duration: 13s; }
.coin-5 { top: 12%; left: 48%; animation-duration: 11s; }


/* FLOATING UI MOTION */
@keyframes floatSoft {
  0%,100% { transform: translateY(0px); }
  50%     { transform: translateY(-8px); }
}
.float-ui { animation: floatSoft 6s ease-in-out infinite; }
.delay1 { animation-delay: 1.2s; }
.delay2 { animation-delay: 2.4s; }


/* HERO + CARDS */
.hero {
  background: rgba(0,0,0,0.55);
  padding: 2rem;
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(12px);
  box-shadow:
    0 16px 60px rgba(0,0,0,0.6),
    0 0 40px var(--glow-1);
}
.hero h1 {
  font-family: "Orbitron";
  font-weight: 700;
}
.hero p {
  color: var(--muted);
  font-size: 1.05rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 1.2rem;
  margin-top: 1.3rem;
}
.card {
  background: rgba(0,0,0,0.45);
  padding: 1.3rem;
  border-radius: 18px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.15);
  transition: .25s;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 45px rgba(0,0,0,0.6), 0 0 28px var(--glow-2);
}
.card h3 {
  font-family: "Orbitron";
}


/* SIDEBAR GLOW */
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.45) !important;
  backdrop-filter: blur(14px);
  border-right: 1px solid rgba(255,255,255,0.15);
  box-shadow: 0 0 40px var(--glow-1);
}


/* REMOVE KEYB BUTTON — add arrow instead */
[data-testid="stKeyboardButton"],
button[title="Keyboard shortcuts"],
span[title="Keyboard shortcuts"],
.st-keyboard-shortcut,
kbd {
    display: none !important;
}

.custom-arrow-btn {
  position: fixed;
  top: 12px;
  right: 18px;
  z-index: 99999;
  background: rgba(255,255,255,0.08);
  padding: 10px 13px;
  border-radius: 12px;
  font-size: 22px;
  border: 1px solid rgba(255,255,255,0.18);
  color: var(--text);
  backdrop-filter: blur(8px);
  transition: .22s;
}
.custom-arrow-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 25px var(--glow-2);
  background: rgba(124,92,255,0.25);
}

            /* ====== IMPROVED VISIBLE WATERMARK ====== */
.watermark {
  position: fixed;
  bottom: 18px;
  right: 22px;
  font-size: 0.95rem;
  font-weight: 700;
  opacity: 0.55; /* stronger */
  color: var(--text);
  z-index: 9999;
  pointer-events: none;
  text-shadow:
      0 0 6px rgba(0,0,0,0.45),
      0 0 14px rgba(0,0,0,0.35);   /* makes it readable on glow */
}

/* ====== BOTTOM-LEFT WATERMARK (Vineet) ====== */
.watermark-left {
  position: fixed;
  bottom: 18px;
  left: 22px;
  font-size: 0.95rem;
  font-weight: 700;
  opacity: 0.55;
  color: var(--text);
  z-index: 9999;
  pointer-events: none;
  text-shadow:
      0 0 6px rgba(0,0,0,0.45),
      0 0 14px rgba(0,0,0,0.35);
}

</style>

<div class="custom-arrow-btn">↗</div>
<div class="aura"></div>

<div class="fraud-drone-layer"><div class="fraud-drone">🛸</div></div>

<div class="coin-layer">
  <div class="coin coin-1">₿</div>
  <div class="coin coin-2">₿</div>
  <div class="coin coin-3">₿</div>
  <div class="coin coin-4">₿</div>
  <div class="coin coin-5">₿</div>
</div>
<div class="watermark-left">Vineet Dungdung</div>

<div class="watermark">Pratishtha Sheetal</div>

""", unsafe_allow_html=True)

# --------------------------------------------
# Floating hero
# --------------------------------------------
st.markdown("""
<div class="hero float-ui">
  <h1>🧠 CipherSentinel Crypto Behavior Monitoring Suite</h1>
  <p>Hybrid ML + Rule-Based Decision Engine with Live Tuning</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------
# Cards
# --------------------------------------------
st.markdown("""
<div class="grid">
  <div class="card float-ui delay1">
    <h3>⚡ Real-Time Verification</h3>
    <p>Submit a single transaction and compute ML + Rules instantly.</p>
  </div>

  <div class="card float-ui delay2">
    <h3>🎛️ Risk Appetite Tuner</h3>
    <p>Adjust rule thresholds + ML confidence live.</p>
  </div>

  <div class="card float-ui">
    <h3>🔍 Forensic Inspection</h3>
    <p>Investigate FP / FN cases and rule contributions.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.subheader("How decisions are made")
st.latex(r"""
\text{Flagged} =
(\text{XGBoost\_Prob} \ge \tau_{\text{ML}}) \lor
\left(\sum_i \text{Rule}_i \cdot w_i \ge \tau_{\text{Rules}}\right)
""")
# ⚡ Quick Start - Premium UI

## Run the Dashboard

```bash
streamlit run streamlit_app/Home_Premium.py
```

## File Overview

### Pages (Run These)
- `Home_Premium.py` - Landing page
- `pages/1_Real_Time_Verification_Premium.py` - Transaction verification
- `pages/2_Risk_Tuner_Premium.py` - Risk tuning dashboard

### Components (Import These)
- `components/theme_toggle.py` - Theme switcher
- `components/icons.py` - SVG icons

### Styles (Load This)
- `assets/premium_styles.css` - Complete CSS framework

## Basic Page Template

```python
import streamlit as st
from components.theme_toggle import render_theme_toggle, render_animated_background
from components.icons import *

st.set_page_config(page_title="Title", layout="wide", page_icon="⚡")

with open("streamlit_app/assets/premium_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_animated_background()
render_theme_toggle()

# Your content here
```

## Common Components

### Glass Card
```python
st.markdown('<div class="glass-card">Content</div>', unsafe_allow_html=True)
```

### KPI Card
```python
st.markdown(f'''
<div class="kpi-card">
    <div class="kpi-icon">{icon_ml_model()}</div>
    <div class="kpi-value">94.2%</div>
    <div class="kpi-label">Accuracy</div>
</div>
''', unsafe_allow_html=True)
```

### Badge
```python
st.markdown('<span class="badge badge-success">✓ Verified</span>', unsafe_allow_html=True)
```

### Alert
```python
st.markdown(f'''
<div class="alert-panel">
    <div class="alert-header">
        <div class="alert-icon alert-icon-danger">{icon_warning()}</div>
        <div class="alert-title">Title</div>
    </div>
    <div class="alert-body">Message</div>
</div>
''', unsafe_allow_html=True)
```

## Documentation

- **DESIGN_SYSTEM.md** - Complete reference
- **PREMIUM_UI_GUIDE.md** - Detailed guide
- **HTML_SNIPPETS.md** - Copy-paste examples

## Features

✅ Dark/Light theme toggle  
✅ Animated background  
✅ Glassmorphism cards  
✅ 12 custom icons  
✅ Fully responsive  
✅ CSS-only animations  
✅ Zero dependencies  

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Set main file: `streamlit_app/Home_Premium.py`
4. Deploy ✅

---

**That's it! You're ready to go. 🚀**

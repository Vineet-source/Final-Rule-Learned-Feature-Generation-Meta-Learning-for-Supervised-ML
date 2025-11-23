# HTML/CSS Snippets for Streamlit

Quick copy-paste snippets for common UI components.

## 🎴 Glass Card

```python
st.markdown("""
<div class="glass-card">
    <h3>Card Title</h3>
    <p>Card content goes here</p>
</div>
""", unsafe_allow_html=True)
```

## 📊 KPI Metric Card

```python
from components.icons import icon_ml_model

st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">{icon_ml_model()}</div>
    <div class="kpi-value">94.2%</div>
    <div class="kpi-label">Accuracy</div>
    <div class="kpi-trend kpi-trend-up">↑ Improving</div>
</div>
""", unsafe_allow_html=True)
```

## 🎯 Badge

```python
st.markdown("""
<span class="badge badge-success">✓ Verified</span>
<span class="badge badge-danger">🚨 Fraud</span>
<span class="badge badge-warning">⚠ Alert</span>
<span class="badge badge-info">ℹ Info</span>
""", unsafe_allow_html=True)
```

## 🚨 Alert Panel

```python
from components.icons import icon_warning

st.markdown(f"""
<div class="alert-panel alert-panel-danger">
    <div class="alert-header">
        <div class="alert-icon alert-icon-danger">
            {icon_warning()}
        </div>
        <div class="alert-title">Alert Title</div>
    </div>
    <div class="alert-body">
        Alert message content goes here
    </div>
</div>
""", unsafe_allow_html=True)
```

## 🎨 Hero Section

```python
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ Feature Badge</div>
    <h1 class="hero-title">Main Title</h1>
    <p class="hero-subtitle">
        Subtitle description text
    </p>
</div>
""", unsafe_allow_html=True)
```

## 🔘 Button (Streamlit Native)

```python
# Primary button
st.button("Primary Action", type="primary", use_container_width=True)

# Secondary button
st.button("Secondary Action", use_container_width=True)
```

## 📏 Horizontal Rule

```python
st.markdown("""
<hr style="border: none; height: 1px; background: var(--border-color); margin: 2rem 0;">
""", unsafe_allow_html=True)
```

## 🎯 Icon with Wrapper

```python
from components.icons import icon_ml_model, icon_wrapper

# Standard size
st.markdown(icon_wrapper(icon_ml_model(), "24px"), unsafe_allow_html=True)

# Large size
st.markdown(icon_wrapper(icon_ml_model(), "48px"), unsafe_allow_html=True)
```

## 📊 KPI Grid Layout

```python
st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""<div class="kpi-card">...</div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="kpi-card">...</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
```

## 🎨 Text with Gradient

```python
st.markdown("""
<h2 class="text-gradient">Gradient Text</h2>
""", unsafe_allow_html=True)
```

## ⚡ Progress Bar

```python
progress_value = 75  # 0-100

st.markdown(f"""
<div class="progress-container">
    <div class="progress-bar" style="width: {progress_value}%;"></div>
</div>
""", unsafe_allow_html=True)
```

## 🎯 Complete Page Template

```python
import streamlit as st
from components.theme_toggle import render_theme_toggle, render_animated_background
from components.icons import *

# Page config
st.set_page_config(
    page_title="Page Title",
    layout="wide",
    page_icon="⚡"
)

# Load CSS
with open("streamlit_app/assets/premium_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render components
render_animated_background()
render_theme_toggle()

# Your content here
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Page Title</h1>
</div>
""", unsafe_allow_html=True)
```

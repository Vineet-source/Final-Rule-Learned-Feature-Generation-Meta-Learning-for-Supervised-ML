"""
Theme Toggle Component
Pure CSS/HTML theme switcher for Streamlit
"""

import streamlit as st

def render_theme_toggle():
    """Render a CSS-only theme toggle button"""
    
    # Initialize theme state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Theme toggle HTML/CSS
    theme_html = """
    <div class="theme-toggle-container">
        <div class="theme-toggle" onclick="toggleTheme()">
            <span class="theme-icon" id="theme-icon">🌙</span>
        </div>
    </div>
    
    <script>
    function toggleTheme() {
        const body = document.body;
        const icon = document.getElementById('theme-icon');
        
        if (body.classList.contains('light-theme')) {
            body.classList.remove('light-theme');
            icon.textContent = '🌙';
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.add('light-theme');
            icon.textContent = '☀️';
            localStorage.setItem('theme', 'light');
        }
    }
    
    // Load saved theme
    window.addEventListener('DOMContentLoaded', (event) => {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        const body = document.body;
        const icon = document.getElementById('theme-icon');
        
        if (savedTheme === 'light') {
            body.classList.add('light-theme');
            icon.textContent = '☀️';
        } else {
            icon.textContent = '🌙';
        }
    });
    </script>
    """
    
    st.markdown(theme_html, unsafe_allow_html=True)


def render_animated_background():
    """Render CSS-only animated background"""
    
    bg_html = """
    <div class="animated-bg">
        <div class="particle particle-1"></div>
        <div class="particle particle-2"></div>
        <div class="particle particle-3"></div>
    </div>
    """
    
    st.markdown(bg_html, unsafe_allow_html=True)

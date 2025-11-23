"""
SVG Icon Library for Fraud Detection Dashboard
All icons are inline SVG for Streamlit compatibility
"""

def icon_fraud_detected():
    """Red alert icon for fraud detection"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="#EF4444" stroke-width="2" fill="rgba(239, 68, 68, 0.1)"/>
        <path d="M12 7V13" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
        <circle cx="12" cy="16" r="1" fill="#EF4444"/>
    </svg>
    """

def icon_verified():
    """Green checkmark for verified transactions"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="#10B981" stroke-width="2" fill="rgba(16, 185, 129, 0.1)"/>
        <path d="M8 12L11 15L16 9" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """

def icon_ml_model():
    """AI/ML brain icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C10.9 2 10 2.9 10 4C10 4.7 10.4 5.4 11 5.7V7C9.3 7 8 8.3 8 10V11.3C7.4 11.6 7 12.3 7 13C7 14.1 7.9 15 9 15C9.7 15 10.4 14.6 10.7 14H13.3C13.6 14.6 14.3 15 15 15C16.1 15 17 14.1 17 13C17 12.3 16.6 11.6 16 11.3V10C16 8.3 14.7 7 13 7V5.7C13.6 5.4 14 4.7 14 4C14 2.9 13.1 2 12 2Z" fill="url(#gradient1)"/>
        <circle cx="12" cy="19" r="2" fill="url(#gradient1)"/>
        <defs>
            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#7C5CFF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#00E5FF;stop-opacity:1" />
            </linearGradient>
        </defs>
    </svg>
    """

def icon_rule_engine():
    """Rule engine/logic icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="3" width="7" height="7" rx="1" stroke="#00E5FF" stroke-width="2" fill="rgba(0, 229, 255, 0.1)"/>
        <rect x="14" y="3" width="7" height="7" rx="1" stroke="#00E5FF" stroke-width="2" fill="rgba(0, 229, 255, 0.1)"/>
        <rect x="3" y="14" width="7" height="7" rx="1" stroke="#00E5FF" stroke-width="2" fill="rgba(0, 229, 255, 0.1)"/>
        <rect x="14" y="14" width="7" height="7" rx="1" stroke="#00E5FF" stroke-width="2" fill="rgba(0, 229, 255, 0.1)"/>
        <line x1="10" y1="6.5" x2="14" y2="6.5" stroke="#00E5FF" stroke-width="2"/>
        <line x1="6.5" y1="10" x2="6.5" y2="14" stroke="#00E5FF" stroke-width="2"/>
        <line x1="17.5" y1="10" x2="17.5" y2="14" stroke="#00E5FF" stroke-width="2"/>
    </svg>
    """

def icon_dashboard():
    """Dashboard/analytics icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="3" width="7" height="7" rx="1" stroke="url(#gradient2)" stroke-width="2" fill="rgba(124, 92, 255, 0.1)"/>
        <rect x="3" y="14" width="7" height="7" rx="1" stroke="url(#gradient2)" stroke-width="2" fill="rgba(124, 92, 255, 0.1)"/>
        <rect x="14" y="3" width="7" height="12" rx="1" stroke="url(#gradient2)" stroke-width="2" fill="rgba(124, 92, 255, 0.1)"/>
        <rect x="14" y="19" width="7" height="2" rx="1" stroke="url(#gradient2)" stroke-width="2" fill="rgba(124, 92, 255, 0.1)"/>
        <defs>
            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#7C5CFF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#00E5FF;stop-opacity:1" />
            </linearGradient>
        </defs>
    </svg>
    """

def icon_settings():
    """Settings/tuner icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="3" stroke="#00E5FF" stroke-width="2"/>
        <path d="M12 1V4M12 20V23M4.22 4.22L6.34 6.34M17.66 17.66L19.78 19.78M1 12H4M20 12H23M4.22 19.78L6.34 17.66M17.66 6.34L19.78 4.22" stroke="#00E5FF" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """

def icon_transaction():
    """Transaction/money icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="url(#gradient3)" stroke-width="2" fill="rgba(0, 229, 255, 0.05)"/>
        <path d="M12 6V18M9 9H13.5C14.3284 9 15 9.67157 15 10.5C15 11.3284 14.3284 12 13.5 12H9M9 12H14C14.8284 12 15.5 12.6716 15.5 13.5C15.5 14.3284 14.8284 15 14 15H9M9 12V15" stroke="url(#gradient3)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <defs>
            <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00E5FF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#7C5CFF;stop-opacity:1" />
            </linearGradient>
        </defs>
    </svg>
    """

def icon_shield():
    """Security/protection icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L4 6V11C4 16 7 20.5 12 22C17 20.5 20 16 20 11V6L12 2Z" stroke="#10B981" stroke-width="2" fill="rgba(16, 185, 129, 0.1)"/>
        <path d="M9 12L11 14L15 10" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """

def icon_warning():
    """Warning/alert icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 20H22L12 2Z" stroke="#F59E0B" stroke-width="2" fill="rgba(245, 158, 11, 0.1)"/>
        <path d="M12 9V13" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
        <circle cx="12" cy="16" r="1" fill="#F59E0B"/>
    </svg>
    """

def icon_chart():
    """Chart/analytics icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 3V21H21" stroke="#00E5FF" stroke-width="2" stroke-linecap="round"/>
        <path d="M7 14L11 10L15 14L21 8" stroke="url(#gradient4)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="7" cy="14" r="2" fill="#00E5FF"/>
        <circle cx="11" cy="10" r="2" fill="#7C5CFF"/>
        <circle cx="15" cy="14" r="2" fill="#00E5FF"/>
        <circle cx="21" cy="8" r="2" fill="#7C5CFF"/>
        <defs>
            <linearGradient id="gradient4" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#00E5FF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#7C5CFF;stop-opacity:1" />
            </linearGradient>
        </defs>
    </svg>
    """

def icon_lightning():
    """Speed/real-time icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="url(#gradient5)" stroke="url(#gradient5)" stroke-width="1"/>
        <defs>
            <linearGradient id="gradient5" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#EF4444;stop-opacity:1" />
            </linearGradient>
        </defs>
    </svg>
    """

def icon_search():
    """Search/forensic icon"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="11" cy="11" r="7" stroke="#00E5FF" stroke-width="2"/>
        <path d="M16 16L21 21" stroke="#00E5FF" stroke-width="2" stroke-linecap="round"/>
        <circle cx="11" cy="11" r="3" fill="rgba(0, 229, 255, 0.2)"/>
    </svg>
    """

# Helper function to wrap icons in styled containers
def icon_wrapper(icon_svg, size="24px", color=None):
    """Wrap SVG icon with optional styling"""
    style = f"width: {size}; height: {size}; display: inline-block; vertical-align: middle;"
    if color:
        style += f" color: {color};"
    
    return f'<span style="{style}">{icon_svg}</span>'

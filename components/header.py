"""
Larry Header Component
"""

import streamlit as st


def render_larry_header():
    """Render the Larry Navigator header."""
    st.markdown("""
    <div class="larry-header">
        <div class="larry-logo">🧠</div>
        <h1 class="larry-title">Larry Navigator</h1>
        <p class="larry-subtitle">Your Socratic guide to finding problems worth solving</p>
        <div class="pws-badges">
            <span class="pws-badge badge-real">✓ REAL</span>
            <span class="pws-badge badge-winnable">🏆 WINNABLE</span>
            <span class="pws-badge badge-worth">💎 WORTH IT</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

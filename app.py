"""CreditBridge Analytics — Streamlit Demo App"""
import streamlit as st
import sys
import os
import pages.explorer

# ── Fix import path for Streamlit Cloud ──────────────────────────────────────
# On Streamlit Cloud the working directory is the repo root.
# We add the directory containing app.py to sys.path so that
# 'utils' and 'pages' are always found regardless of where the server runs.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

st.set_page_config(
    page_title="CreditBridge Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_css
inject_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-mark">CB</div>
        <div>
            <div class="logo-name">CreditBridge</div>
            <div class="logo-sub">Analytics Ltd</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠  Home",
         "🎯  Score an SME",
         "📊  Data Explorer",
         "🤖  Model Insights",
         "📖  API Reference"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div class="sidebar-badge">
        <div class="badge-dot"></div>
        <span>Model v1.0 · Live Demo</span>
    </div>
    <div class="sidebar-footer" style="margin-top:12px">
        Built on synthetic R&amp;D data.<br>
        Pilot partnerships open Q3 2025.
    </div>
    """, unsafe_allow_html=True)

# ── Route ─────────────────────────────────────────────────────────────────────
if   page == "🏠  Home":
    from pages.home           import render
elif page == "🎯  Score an SME":
    from pages.scorer         import render
elif page == "📊  Data Explorer":
    from pages.explorer       import render
elif page == "🤖  Model Insights":
    from pages.model_insights import render
elif page == "📖  API Reference":
    from pages.api_docs       import render

render()

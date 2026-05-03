"""CreditBridge Analytics — Streamlit Demo App"""
import streamlit as st
st.set_page_config(
    page_title="CreditBridge Analytics",
    page_icon="🏦", layout="wide",
    initial_sidebar_state="expanded",
)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils.styles import inject_css
inject_css()

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-mark">CB</div>
        <div><div class="logo-name">CreditBridge</div>
        <div class="logo-sub">Analytics Ltd</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", [
        "🏠  Home","🎯  Score an SME",
        "📊  Data Explorer","🤖  Model Insights","📖  API Reference"],
        label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-badge"><div class="badge-dot"></div>
    <span>Model v1.0 · Live Demo</span></div>
    <div class="sidebar-footer" style="margin-top:12px">
    Built on synthetic R&D data.<br>Pilot partnerships open Q3 2025.</div>
    """, unsafe_allow_html=True)

if   page == "🏠  Home":           from pages.home           import render
elif page == "🎯  Score an SME":   from pages.scorer         import render
elif page == "📊  Data Explorer":  from pages.explorer       import render
elif page == "🤖  Model Insights": from pages.model_insights import render
elif page == "📖  API Reference":  from pages.api_docs       import render
render()

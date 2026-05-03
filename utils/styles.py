"""CreditBridge — shared styles injected into every Streamlit page."""

import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Reset & base ─────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background: #0a0f1e;
        color: #e8eaf0;
    }

    /* ── Sidebar ──────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #080c18 !important;
        border-right: 1px solid #1e2640;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #8892b0 !important;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        padding: 6px 0;
        cursor: pointer;
        transition: color 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #64ffda !important;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 4px;
    }
    .logo-mark {
        background: linear-gradient(135deg, #64ffda, #0ea5e9);
        color: #0a0f1e;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.1rem;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-name {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        color: #e8eaf0;
    }
    .logo-sub {
        font-size: 0.72rem;
        color: #64ffda;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-family: 'DM Mono', monospace;
    }

    .sidebar-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        color: #8892b0;
        font-family: 'DM Mono', monospace;
    }
    .badge-dot {
        width: 8px; height: 8px;
        background: #64ffda;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.3; }
    }
    .sidebar-footer {
        font-size: 0.73rem;
        color: #4a5568;
        line-height: 1.6;
        margin-top: 16px;
    }

    /* ── Page headers ─────────────────────────────────── */
    .page-header {
        margin-bottom: 2rem;
    }
    .page-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.2rem;
        color: #e8eaf0;
        line-height: 1.1;
        margin-bottom: 0.4rem;
    }
    .page-subtitle {
        font-size: 1rem;
        color: #8892b0;
        font-weight: 300;
    }
    .accent { color: #64ffda; }

    /* ── Metric cards ─────────────────────────────────── */
    .metric-card {
        background: #111827;
        border: 1px solid #1e2640;
        border-radius: 12px;
        padding: 20px 24px;
        transition: border-color 0.2s;
    }
    .metric-card:hover { border-color: #64ffda44; }
    .metric-label {
        font-size: 0.75rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-family: 'DM Mono', monospace;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: #e8eaf0;
        line-height: 1;
    }
    .metric-delta {
        font-size: 0.8rem;
        color: #64ffda;
        margin-top: 6px;
        font-family: 'DM Mono', monospace;
    }
    .metric-delta.negative { color: #ff6b6b; }

    /* ── Score display ────────────────────────────────── */
    .score-circle-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 32px 0;
    }
    .score-number {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 5rem;
        line-height: 1;
    }
    .score-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 8px;
    }
    .score-band-LOW       { color: #64ffda; }
    .score-band-LOW-MEDIUM{ color: #4ade80; }
    .score-band-MEDIUM    { color: #fbbf24; }
    .score-band-HIGH      { color: #f97316; }
    .score-band-VERY-HIGH { color: #f87171; }

    /* ── Contributor bars ─────────────────────────────── */
    .contributor-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        border-bottom: 1px solid #1e2640;
    }
    .contributor-dir {
        font-size: 1.1rem;
        width: 20px;
        text-align: center;
    }
    .contributor-name {
        flex: 1;
        font-size: 0.85rem;
        color: #cbd5e1;
        font-family: 'DM Mono', monospace;
    }
    .contributor-bar-wrap {
        width: 120px;
        height: 6px;
        background: #1e2640;
        border-radius: 3px;
        overflow: hidden;
    }
    .contributor-bar-fill {
        height: 100%;
        border-radius: 3px;
    }
    .contributor-weight {
        font-size: 0.75rem;
        color: #8892b0;
        font-family: 'DM Mono', monospace;
        width: 40px;
        text-align: right;
    }

    /* ── Info panels ──────────────────────────────────── */
    .info-panel {
        background: #111827;
        border: 1px solid #1e2640;
        border-left: 3px solid #64ffda;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.9rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    .warning-panel {
        background: #111827;
        border: 1px solid #1e2640;
        border-left: 3px solid #fbbf24;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.9rem;
        color: #cbd5e1;
    }

    /* ── Code blocks ──────────────────────────────────── */
    .code-block {
        background: #060a14;
        border: 1px solid #1e2640;
        border-radius: 10px;
        padding: 20px;
        font-family: 'DM Mono', monospace;
        font-size: 0.82rem;
        color: #64ffda;
        overflow-x: auto;
        line-height: 1.7;
        white-space: pre;
    }
    .code-comment { color: #4a5568; }
    .code-string  { color: #fbbf24; }
    .code-key     { color: #a78bfa; }

    /* ── Dividers ─────────────────────────────────────── */
    .section-divider {
        border: none;
        border-top: 1px solid #1e2640;
        margin: 2rem 0;
    }

    /* ── Tables ───────────────────────────────────────── */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }
    .styled-table th {
        background: #111827;
        color: #8892b0;
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 10px 14px;
        text-align: left;
        border-bottom: 1px solid #1e2640;
    }
    .styled-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #0f1628;
        color: #cbd5e1;
    }
    .styled-table tr:hover td { background: #111827; }

    /* ── Streamlit overrides ──────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #64ffda22, #0ea5e922);
        border: 1px solid #64ffda66;
        color: #64ffda;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #64ffda33, #0ea5e933);
        border-color: #64ffda;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #64ffda, #0ea5e9);
        color: #0a0f1e;
        border: none;
        font-weight: 600;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px #64ffda33;
    }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] select {
        background: #111827 !important;
        border: 1px solid #1e2640 !important;
        border-radius: 8px !important;
        color: #e8eaf0 !important;
    }
    .stSlider [data-testid="stThumbValue"] {
        color: #64ffda;
    }
    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1e2640;
        border-radius: 12px;
        padding: 16px;
    }
    div[data-testid="stMetric"] label {
        color: #8892b0 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #e8eaf0 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8892b0;
        font-family: 'DM Sans', sans-serif;
    }
    .stTabs [aria-selected="true"] {
        color: #64ffda !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background: #64ffda !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        background: #1e2640 !important;
    }
    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
        color: #e8eaf0 !important;
    }
    .stMarkdown p { color: #cbd5e1; }
    [data-testid="stExpander"] {
        background: #111827;
        border: 1px solid #1e2640;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

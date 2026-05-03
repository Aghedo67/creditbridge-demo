import streamlit as st
import plotly.graph_objects as go
from utils.data_engine import generate_dataset, COLOURS, TIER_LABELS

def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Alternative Credit Scoring<br>for Nigerian <span class="accent">SMEs</span></div>
        <div class="page-subtitle">
            Real-time credit risk intelligence for digital lenders — powered by mobile money data
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key metrics row ───────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class="metric-card">
            <div class="metric-label">SME Financing Gap</div>
            <div class="metric-value">$150B+</div>
            <div class="metric-delta">Nigeria annually · World Bank est.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="metric-card">
            <div class="metric-label">SMEs Without Credit</div>
            <div class="metric-value">37M</div>
            <div class="metric-delta">No formal credit history</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="metric-card">
            <div class="metric-label">Score Delivery</div>
            <div class="metric-value">&lt;60s</div>
            <div class="metric-delta">Real-time API response</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="metric-card">
            <div class="metric-label">Data Sources</div>
            <div class="metric-value">150+</div>
            <div class="metric-delta">Alternative signal features</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────────────────
    st.markdown("### How CreditBridge Works")
    col1, col2 = st.columns([1.2, 1])

    with col1:
        steps = [
            ("01", "SME Consent", "Business owner authenticates via consent portal and grants read access to mobile money history, utility records, and open banking data."),
            ("02", "Data Ingestion", "CreditBridge ingests transaction data from OPay, Palmpay, Moniepoint and other platforms via secure API connections."),
            ("03", "Feature Engineering", "Our ML pipeline extracts 150+ features: payment regularity, counterparty diversity, income stability, balance behaviour."),
            ("04", "Score Delivery", "A gradient-boosted ensemble model returns a 0–850 score, risk band, probability of default, and key contributing factors — in one JSON response."),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div style="display:flex;gap:16px;margin-bottom:20px;align-items:flex-start">
                <div style="font-family:'DM Mono',monospace;font-size:0.7rem;
                    color:#64ffda;background:#64ffda15;border:1px solid #64ffda33;
                    border-radius:6px;padding:4px 8px;white-space:nowrap;margin-top:2px">
                    {num}
                </div>
                <div>
                    <div style="font-weight:600;color:#e8eaf0;margin-bottom:4px">{title}</div>
                    <div style="font-size:0.88rem;color:#8892b0;line-height:1.6">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        with st.spinner("Loading demo data..."):
            sme_df, features_df, _ = generate_dataset()

        tier_counts = sme_df["credit_tier"].value_counts()
        labels = [TIER_LABELS.get(t, t) for t in tier_counts.index]
        colours = [COLOURS.get(t, "#888") for t in tier_counts.index]

        fig = go.Figure(go.Pie(
            labels=labels,
            values=tier_counts.values,
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#0a0f1e", width=3)),
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=12, color="#e8eaf0"),
            hovertemplate="<b>%{label}</b><br>%{value} SMEs<br>%{percent}<extra></extra>",
        ))
        fig.add_annotation(text=f"<b>{len(sme_df)}</b><br><span style='font-size:11px'>SMEs</span>",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=22, color="#e8eaf0", family="Syne"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(t=20,b=20,l=20,r=20),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div style="text-align:center;font-size:0.8rem;color:#8892b0;
            font-family:'DM Mono',monospace">Synthetic dataset · Credit tier distribution</div>""",
            unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Score band table ──────────────────────────────────────────────────────
    st.markdown("### Score Interpretation")
    bands = [
        ("750 – 850", "LOW",       "#64ffda", "Standard lending terms. Minimal risk mitigation required."),
        ("600 – 749", "LOW-MEDIUM","#4ade80", "Normal lending with routine monitoring."),
        ("450 – 599", "MEDIUM",    "#fbbf24", "Consider reduced loan amounts or shorter tenors."),
        ("300 – 449", "HIGH",      "#f97316", "Enhanced due diligence and collateral review."),
        ("150 – 299", "VERY HIGH", "#f87171", "Manual underwriting required before approval."),
    ]
    st.markdown("""<table class="styled-table"><tr>
        <th>Score Range</th><th>Risk Band</th><th>Recommended Action</th></tr>""",
        unsafe_allow_html=True)
    for score_range, band, colour, action in bands:
        st.markdown(f"""<tr>
            <td><span style="font-family:'DM Mono',monospace;font-weight:600;color:{colour}">{score_range}</span></td>
            <td><span style="background:{colour}22;color:{colour};padding:2px 10px;
                border-radius:20px;font-size:0.8rem;font-family:'DM Mono',monospace">{band}</span></td>
            <td style="color:#8892b0;font-size:0.87rem">{action}</td>
        </tr>""", unsafe_allow_html=True)
    st.markdown("</table>", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-panel">
        <strong style="color:#64ffda">This is an interactive R&D demonstration.</strong>
        All data shown is synthetic, generated from the CreditBridge ML pipeline.
        Pilot partnerships with Nigerian digital lenders open Q3 2025.
        Contact <a href="mailto:api@creditbridge.co.uk" style="color:#64ffda">api@creditbridge.co.uk</a>
    </div>
    """, unsafe_allow_html=True)

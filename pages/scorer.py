import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.data_engine import score_sme_inputs, COLOURS

PRESETS = {
    "✅ Healthy SME — Market Trader": {
        "total_txn_count":3200,"total_inflow_ngn":4800000,"total_outflow_ngn":3600000,
        "months_active":22,"monthly_inflow_cv":0.18,"mean_balance_ngn":85000,
        "near_zero_rate":0.02,"has_negative_balance":0,"utility_months":11,
        "has_loan_repayment":1,"regular_payment_rate":0.88,"is_growing":1,
    },
    "⚠️ Borderline — Food Vendor": {
        "total_txn_count":1400,"total_inflow_ngn":1200000,"total_outflow_ngn":1050000,
        "months_active":16,"monthly_inflow_cv":0.52,"mean_balance_ngn":18000,
        "near_zero_rate":0.18,"has_negative_balance":0,"utility_months":6,
        "has_loan_repayment":0,"regular_payment_rate":0.42,"is_growing":0,
    },
    "❌ High Risk — Agro Processor": {
        "total_txn_count":620,"total_inflow_ngn":780000,"total_outflow_ngn":890000,
        "months_active":9,"monthly_inflow_cv":1.35,"mean_balance_ngn":3200,
        "near_zero_rate":0.45,"has_negative_balance":1,"utility_months":2,
        "has_loan_repayment":0,"regular_payment_rate":0.08,"is_growing":0,
    },
}

def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Live <span class="accent">SME Scorer</span></div>
        <div class="page-subtitle">Enter transaction data or pick a preset to generate a real-time credit score</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # ── Preset selector ───────────────────────────────────────────────────
        st.markdown("##### Quick Presets")
        preset_name = st.selectbox("Load a preset SME profile",
                                   ["— Enter manually —"] + list(PRESETS.keys()),
                                   label_visibility="collapsed")
        preset = PRESETS.get(preset_name, {})

        def pv(key, default):
            return preset.get(key, default)

        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

        # ── Input form ────────────────────────────────────────────────────────
        st.markdown("##### Transaction Summary")
        st.markdown("""<div class='info-panel' style='font-size:0.82rem'>
            Enter aggregated figures covering the SME's last 12–24 months of activity.
        </div>""", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["💰 Volume", "🏦 Balance", "📅 Behaviour"])

        with tab1:
            txn_count = st.number_input("Total transaction count", min_value=0,
                value=pv("total_txn_count", 500), step=100)
            inflow    = st.number_input("Total inflow (₦)", min_value=0,
                value=pv("total_inflow_ngn", 1000000), step=100000,
                format="%d")
            outflow   = st.number_input("Total outflow (₦)", min_value=0,
                value=pv("total_outflow_ngn", 800000), step=100000,
                format="%d")
            months_active = st.slider("Months with inflow activity", 1, 24,
                value=pv("months_active", 12))
            inflow_cv = st.slider("Monthly inflow volatility (CV)",
                0.0, 2.0, value=float(pv("monthly_inflow_cv", 0.5)), step=0.01,
                help="0 = perfectly stable income. >1 = very volatile.")

        with tab2:
            mean_balance = st.number_input("Mean account balance (₦)", min_value=-50000,
                value=pv("mean_balance_ngn", 20000), step=5000, format="%d")
            near_zero    = st.slider("Near-zero balance rate",
                0.0, 1.0, value=float(pv("near_zero_rate", 0.15)), step=0.01,
                help="Fraction of transactions where balance was below ₦5,000")
            has_negative = st.selectbox("Ever had negative balance?",
                [0, 1], index=pv("has_negative_balance", 0),
                format_func=lambda x: "Yes" if x else "No")

        with tab3:
            util_months  = st.slider("Months with utility payment", 0, 24,
                value=pv("utility_months", 8))
            has_loan     = st.selectbox("Has active loan repayments?",
                [0, 1], index=pv("has_loan_repayment", 0),
                format_func=lambda x: "Yes" if x else "No")
            reg_rate     = st.slider("Regular payment rate", 0.0, 1.0,
                value=float(pv("regular_payment_rate", 0.4)), step=0.01,
                help="Fraction of months where scheduled payments were made on time")
            is_growing   = st.selectbox("Business growing?",
                [0, 1], index=pv("is_growing", 0),
                format_func=lambda x: "Yes — 90d inflow trend up" if x else "No — flat or declining")

        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("⚡ Generate Credit Score", type="primary",
                         use_container_width=True)

    # ── Results panel ─────────────────────────────────────────────────────────
    with col_right:
        if run or preset_name != "— Enter manually —":
            inputs = {
                "total_txn_count":    txn_count,
                "total_inflow_ngn":   inflow,
                "total_outflow_ngn":  outflow,
                "months_active":      months_active,
                "monthly_inflow_cv":  inflow_cv,
                "mean_balance_ngn":   mean_balance,
                "near_zero_rate":     near_zero,
                "has_negative_balance": has_negative,
                "utility_months":     util_months,
                "has_loan_repayment": has_loan,
                "regular_payment_rate": reg_rate,
                "is_growing":         is_growing,
            }
            result = score_sme_inputs(inputs)

            # Score display
            colour = result["band_colour"]
            score  = result["credit_score"]
            band   = result["risk_band"]
            pd_val = result["prob_default"]

            st.markdown(f"""
            <div style="background:#111827;border:1px solid {colour}44;
                border-radius:16px;padding:32px;text-align:center;margin-bottom:20px">
                <div style="font-family:'DM Mono',monospace;font-size:0.75rem;
                    color:#8892b0;letter-spacing:0.15em;text-transform:uppercase;
                    margin-bottom:8px">Request · {result['request_id']}</div>
                <div style="font-family:'Syne',sans-serif;font-weight:800;
                    font-size:5.5rem;color:{colour};line-height:1">{score}</div>
                <div style="font-family:'DM Mono',monospace;font-size:0.9rem;
                    color:{colour};letter-spacing:0.2em;margin-top:6px">{band} RISK</div>
                <div style="margin-top:20px;display:flex;justify-content:center;
                    gap:24px;flex-wrap:wrap">
                    <div>
                        <div style="font-size:0.72rem;color:#8892b0;
                            font-family:'DM Mono',monospace">PROB. DEFAULT</div>
                        <div style="font-size:1.1rem;font-weight:600;color:#e8eaf0">
                            {pd_val:.1%}</div>
                    </div>
                    <div>
                        <div style="font-size:0.72rem;color:#8892b0;
                            font-family:'DM Mono',monospace">CONFIDENCE</div>
                        <div style="font-size:1.1rem;font-weight:600;color:#e8eaf0">
                            {result['confidence']}</div>
                    </div>
                    <div>
                        <div style="font-size:0.72rem;color:#8892b0;
                            font-family:'DM Mono',monospace">SCORE RANGE</div>
                        <div style="font-size:1.1rem;font-weight:600;color:#e8eaf0">
                            150 – 850</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={"font":{"color":colour,"family":"Syne","size":36}},
                gauge={
                    "axis":{"range":[150,850],"tickwidth":1,
                            "tickcolor":"#1e2640","tickfont":{"color":"#8892b0","size":10}},
                    "bar":{"color":colour,"thickness":0.25},
                    "bgcolor":"#111827",
                    "borderwidth":0,
                    "steps":[
                        {"range":[150,299],"color":"#f8717122"},
                        {"range":[299,449],"color":"#f9731622"},
                        {"range":[449,599],"color":"#fbbf2422"},
                        {"range":[599,749],"color":"#4ade8022"},
                        {"range":[749,850],"color":"#64ffda22"},
                    ],
                    "threshold":{"line":{"color":colour,"width":3},"value":score},
                },
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=220,
                margin=dict(t=20,b=0,l=30,r=30),
                font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Lender guidance
            st.markdown(f"""
            <div class="info-panel">
                <strong style="color:#64ffda">Lender Guidance:</strong>
                {result['lender_guidance']}
            </div>
            """, unsafe_allow_html=True)

            # Contributing factors
            st.markdown("##### Top Contributing Factors")
            for name, direction, weight in result["contributors"]:
                bar_colour = "#64ffda" if direction == "positive" else "#f87171"
                arrow = "▲" if direction == "positive" else "▼"
                bar_w = int(weight * 400)
                st.markdown(f"""
                <div class="contributor-row">
                    <span style="color:{bar_colour};font-size:0.85rem">{arrow}</span>
                    <span class="contributor-name">{name}</span>
                    <div class="contributor-bar-wrap">
                        <div class="contributor-bar-fill"
                             style="width:{bar_w}px;background:{bar_colour}"></div>
                    </div>
                    <span class="contributor-weight">{weight:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            # Net flow indicator
            st.markdown("<br>", unsafe_allow_html=True)
            net = inflow - outflow
            net_colour = "#64ffda" if net > 0 else "#f87171"
            st.markdown(f"""
            <div style="display:flex;gap:16px">
                <div class="metric-card" style="flex:1">
                    <div class="metric-label">Net Cash Flow</div>
                    <div class="metric-value" style="color:{net_colour};font-size:1.4rem">
                        ₦{net:,.0f}</div>
                </div>
                <div class="metric-card" style="flex:1">
                    <div class="metric-label">Savings Rate</div>
                    <div class="metric-value" style="font-size:1.4rem">
                        {max(0,(inflow-outflow)/max(inflow,1)):.1%}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background:#111827;border:2px dashed #1e2640;border-radius:16px;
                padding:60px 32px;text-align:center;margin-top:20px">
                <div style="font-size:3rem;margin-bottom:16px">⚡</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.3rem;
                    color:#e8eaf0;margin-bottom:8px">Ready to Score</div>
                <div style="color:#8892b0;font-size:0.9rem">
                    Select a preset or fill in the form,<br>then click Generate Credit Score
                </div>
            </div>
            """, unsafe_allow_html=True)

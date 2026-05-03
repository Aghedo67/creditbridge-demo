import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.data_engine import generate_dataset, COLOURS, TIER_LABELS, TIER_ORDER

def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Data <span class="accent">Explorer</span></div>
        <div class="page-subtitle">Explore the synthetic Nigerian SME dataset — 150 businesses, 24 months, 85 features</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading dataset..."):
        sme_df, features_df, monthly_df = generate_dataset()

    merged = features_df.merge(sme_df[["sme_id","archetype","state","platform"]], on="sme_id")

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🔽 Filter Dataset", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            tier_filter = st.multiselect("Credit Tier",
                options=TIER_ORDER,
                default=TIER_ORDER,
                format_func=lambda x: TIER_LABELS[x])
        with fc2:
            arch_filter = st.multiselect("Archetype",
                options=sme_df["archetype"].unique().tolist(),
                default=sme_df["archetype"].unique().tolist())
        with fc3:
            score_range = st.slider("Credit Score Range", 150, 850, (150, 850))

    mask = (
        merged["credit_tier"].isin(tier_filter) &
        merged["archetype"].isin(arch_filter) &
        merged["credit_score"].between(*score_range)
    )
    filtered = merged[mask]
    st.markdown(f"""<div style="font-family:'DM Mono',monospace;font-size:0.8rem;
        color:#8892b0;margin-bottom:16px">
        Showing <span style="color:#64ffda">{len(filtered)}</span>
        of {len(merged)} SMEs</div>""", unsafe_allow_html=True)

    # ── Row 1: Score distribution + default rate ──────────────────────────────
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.markdown("##### Credit Score Distribution")
        fig = go.Figure()
        for tier in TIER_ORDER:
            sub = filtered[filtered["credit_tier"]==tier]["credit_score"]
            if len(sub) == 0: continue
            fig.add_trace(go.Histogram(
                x=sub, name=TIER_LABELS[tier],
                marker_color=COLOURS[tier],
                opacity=0.75, nbinsx=20,
                hovertemplate=f"<b>{TIER_LABELS[tier]}</b><br>Score: %{{x}}<br>Count: %{{y}}<extra></extra>"
            ))
        fig.update_layout(
            barmode="overlay",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#8892b0",size=11),bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(title="Credit Score",color="#8892b0",gridcolor="#1e2640"),
            yaxis=dict(title="Count",color="#8892b0",gridcolor="#1e2640"),
            margin=dict(t=10,b=40,l=40,r=10), height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with r1c2:
        st.markdown("##### Default Rate by Credit Tier")
        tier_defaults = filtered.groupby("credit_tier").agg(
            count=("label_default","count"),
            default_rate=("label_default","mean"),
        ).reset_index()
        tier_defaults["colour"] = tier_defaults["credit_tier"].map(COLOURS)
        tier_defaults["label"] = tier_defaults["credit_tier"].map(TIER_LABELS)
        tier_defaults = tier_defaults.set_index("credit_tier").loc[
            [t for t in TIER_ORDER if t in tier_defaults["credit_tier"].values]
        ].reset_index()

        fig = go.Figure(go.Bar(
            x=tier_defaults["label"],
            y=tier_defaults["default_rate"] * 100,
            marker_color=tier_defaults["colour"].tolist(),
            text=[f"{v:.1f}%" for v in tier_defaults["default_rate"]*100],
            textposition="outside",
            textfont=dict(color="#e8eaf0", size=11),
            hovertemplate="<b>%{x}</b><br>Default Rate: %{y:.1f}%<extra></extra>",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#8892b0"),
            yaxis=dict(title="Default Rate (%)", color="#8892b0", gridcolor="#1e2640"),
            margin=dict(t=10,b=40,l=40,r=10), height=300,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Monthly inflow by tier ─────────────────────────────────────────
    st.markdown("##### Monthly Inflow Trend by Credit Tier")
    monthly_tier = monthly_df[
        monthly_df["sme_id"].isin(filtered["sme_id"])
    ].groupby(["month","credit_tier"])["inflow_ngn"].mean().reset_index()

    fig = go.Figure()
    for tier in TIER_ORDER:
        sub = monthly_tier[monthly_tier["credit_tier"]==tier]
        if len(sub) == 0: continue
        fig.add_trace(go.Scatter(
            x=sub["month"], y=sub["inflow_ngn"],
            name=TIER_LABELS[tier],
            line=dict(color=COLOURS[tier], width=2.5),
            fill="tozeroy",
            fillcolor=COLOURS[tier] + "15",
            hovertemplate=f"<b>{TIER_LABELS[tier]}</b><br>Month %{{x}}: ₦%{{y:,.0f}}<extra></extra>",
        ))

    month_labels = ["Jan'23","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec'23",
                    "Jan'24","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec'24"]
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#8892b0",size=11),bgcolor="rgba(0,0,0,0)",
                    orientation="h",y=1.1),
        xaxis=dict(color="#8892b0",gridcolor="#1e2640",
                   tickvals=list(range(1,25)),ticktext=month_labels,tickfont=dict(size=9)),
        yaxis=dict(title="Avg Monthly Inflow (₦)",color="#8892b0",gridcolor="#1e2640"),
        margin=dict(t=30,b=40,l=60,r=10), height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Row 3: Scatter + feature heatmap ──────────────────────────────────────
    r3c1, r3c2 = st.columns(2)

    with r3c1:
        st.markdown("##### Balance vs Inflow — by Tier")
        fig = px.scatter(
            filtered,
            x="vol_total_inflow_ngn",
            y="bal_mean_ngn",
            color="credit_tier",
            color_discrete_map=COLOURS,
            hover_data={"sme_id":True,"credit_score":True,"archetype":True},
            labels={"vol_total_inflow_ngn":"Total Inflow (₦)","bal_mean_ngn":"Mean Balance (₦)"},
        )
        fig.update_traces(marker=dict(size=8, opacity=0.8))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#8892b0",size=10),bgcolor="rgba(0,0,0,0)",title=""),
            xaxis=dict(color="#8892b0",gridcolor="#1e2640"),
            yaxis=dict(color="#8892b0",gridcolor="#1e2640"),
            margin=dict(t=10,b=40,l=60,r=10), height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with r3c2:
        st.markdown("##### Avg Feature Values by Credit Tier")
        key_feats = {
            "reg_composite":    "Payment Regularity",
            "bal_mean_ngn":     "Mean Balance",
            "out_utility_reg":  "Utility Regularity",
            "ratio_savings_rate":"Savings Rate",
            "trend_growing":    "Business Growing",
        }
        heatmap_data = []
        valid_tiers = [t for t in TIER_ORDER if t in filtered["credit_tier"].values]
        for feat, label in key_feats.items():
            row = [label]
            for tier in valid_tiers:
                sub = filtered[filtered["credit_tier"]==tier][feat]
                col_min = filtered[feat].min()
                col_max = filtered[feat].max()
                norm = (sub.mean() - col_min) / max(col_max - col_min, 1e-9)
                row.append(round(norm, 3))
            heatmap_data.append(row)

        hm_df = pd.DataFrame(heatmap_data,
            columns=["Feature"]+[TIER_LABELS[t] for t in valid_tiers])
        hm_vals = hm_df[[TIER_LABELS[t] for t in valid_tiers]].values

        fig = go.Figure(go.Heatmap(
            z=hm_vals,
            x=[TIER_LABELS[t] for t in valid_tiers],
            y=list(key_feats.values()),
            colorscale=[[0,"#f87171"],[0.5,"#fbbf24"],[1,"#64ffda"]],
            text=[[f"{v:.2f}" for v in row] for row in hm_vals],
            texttemplate="%{text}",
            textfont=dict(size=11,color="#0a0f1e"),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.3f}<extra></extra>",
            showscale=False,
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#8892b0"),
            yaxis=dict(color="#8892b0"),
            margin=dict(t=10,b=10,l=130,r=10), height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Raw data table ────────────────────────────────────────────────────────
    with st.expander("📋 View Raw Feature Data"):
        display_cols = ["sme_id","archetype","state","credit_tier","credit_score",
                        "vol_total_inflow_ngn","bal_mean_ngn","reg_composite",
                        "out_utility_reg","label_default"]
        st.dataframe(
            filtered[display_cols].rename(columns={
                "sme_id":"SME ID","archetype":"Type","state":"State",
                "credit_tier":"Tier","credit_score":"Score",
                "vol_total_inflow_ngn":"Total Inflow (₦)",
                "bal_mean_ngn":"Mean Balance (₦)",
                "reg_composite":"Regularity","out_utility_reg":"Utility Rate",
                "label_default":"Default Label"
            }).style.format({
                "Total Inflow (₦)":"{:,.0f}",
                "Mean Balance (₦)":"{:,.0f}",
                "Regularity":"{:.2f}","Utility Rate":"{:.2f}",
            }),
            use_container_width=True, height=300,
        )

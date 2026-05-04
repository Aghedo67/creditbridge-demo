"""
CreditBridge — Shared data engine for Streamlit app.
Generates the synthetic dataset once and caches it for all pages.
Uses Streamlit's cache so data is only generated on first load.
"""

import numpy as np
import pandas as pd
from scipy import stats
import uuid
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

# ── Colours used across all pages ────────────────────────────────────────────
COLOURS = {
    "prime":         "#64ffda",
    "near_prime":    "#4ade80",
    "subprime":      "#fbbf24",
    "deep_subprime": "#f87171",
    "brand":         "#0ea5e9",
    "bg":            "#0a0f1e",
    "card":          "#111827",
    "border":        "#1e2640",
    "muted":         "#8892b0",
    "text":          "#e8eaf0",
}

TIER_ORDER  = ["prime", "near_prime", "subprime", "deep_subprime"]
TIER_LABELS = {"prime":"Prime","near_prime":"Near-Prime",
               "subprime":"Subprime","deep_subprime":"Deep Subprime"}


# ── Inline archetype + tier definitions (no external file dependency) ─────────

ARCHETYPES = {
    "Market Trader":    {"avg_daily_txn":9,  "avg_inflow":18500, "avg_outflow":14000, "io_ratio":0.55, "sector":"Trade"},
    "Food Vendor":      {"avg_daily_txn":16, "avg_inflow":3200,  "avg_outflow":8500,  "io_ratio":0.65, "sector":"Food & Hospitality"},
    "Logistics":        {"avg_daily_txn":4,  "avg_inflow":52000, "avg_outflow":38000, "io_ratio":0.50, "sector":"Logistics"},
    "Fashion & Beauty": {"avg_daily_txn":5,  "avg_inflow":22000, "avg_outflow":15000, "io_ratio":0.58, "sector":"Fashion"},
    "Agro Processor":   {"avg_daily_txn":3,  "avg_inflow":85000, "avg_outflow":65000, "io_ratio":0.48, "sector":"Agriculture"},
    "Tech Services":    {"avg_daily_txn":11, "avg_inflow":8500,  "avg_outflow":5000,  "io_ratio":0.62, "sector":"Technology"},
}

CREDIT_TIERS = {
    "prime":         {"score_range":(700,850),"default_prob":0.03,"payment_reg":0.92,"income_stab":0.88,"balance_cushion":0.75},
    "near_prime":    {"score_range":(550,699),"default_prob":0.12,"payment_reg":0.74,"income_stab":0.68,"balance_cushion":0.50},
    "subprime":      {"score_range":(350,549),"default_prob":0.28,"payment_reg":0.51,"income_stab":0.45,"balance_cushion":0.25},
    "deep_subprime": {"score_range":(150,349),"default_prob":0.55,"payment_reg":0.28,"income_stab":0.25,"balance_cushion":0.08},
}

TIER_DIST     = {"prime":0.15,"near_prime":0.35,"subprime":0.30,"deep_subprime":0.20}
ARCHETYPE_DIST= [0.28,0.22,0.12,0.18,0.10,0.10]

MONTHLY_SEASONALITY = {1:0.82,2:0.88,3:0.92,4:0.98,5:0.95,6:0.90,
                        7:0.88,8:0.93,9:0.97,10:1.02,11:1.08,12:1.35}

NIGERIAN_STATES = ["Lagos","Abuja","Kano","Rivers","Oyo","Anambra","Delta","Enugu","Ogun","Kaduna"]
STATE_WEIGHTS   = [0.30,0.12,0.10,0.09,0.08,0.07,0.07,0.06,0.06,0.05]
PLATFORMS       = ["OPay","Palmpay","Moniepoint","Kuda","GTBank","Access_USSD"]
PLATFORM_W      = [0.28,0.22,0.20,0.12,0.10,0.08]


@st.cache_data(show_spinner=False)
def generate_dataset(n_smes: int = 150, random_seed: int = 42) -> tuple:
    """
    Generate the full synthetic dataset.
    Cached by Streamlit — only runs once per session.
    Returns (sme_df, features_df)
    """
    rng = np.random.default_rng(random_seed)
    arch_names = list(ARCHETYPES.keys())

    # ── Build SME registry ────────────────────────────────────────────────────
    smes = []
    for i in range(n_smes):
        arch_name = rng.choice(arch_names, p=ARCHETYPE_DIST)
        tier_name = rng.choice(list(TIER_DIST.keys()), p=list(TIER_DIST.values()))
        tier  = CREDIT_TIERS[tier_name]
        lo,hi = tier["score_range"]
        score = int(rng.integers(lo, hi+1))
        has_loan = rng.random() < {
            "prime":0.92,"near_prime":0.78,"subprime":0.55,"deep_subprime":0.28
        }[tier_name]
        smes.append({
            "sme_id":      f"SME_{i+1:04d}",
            "archetype":   arch_name,
            "sector":      ARCHETYPES[arch_name]["sector"],
            "state":       rng.choice(NIGERIAN_STATES, p=STATE_WEIGHTS),
            "platform":    rng.choice(PLATFORMS, p=PLATFORM_W),
            "credit_tier": tier_name,
            "credit_score":score,
            "default_prob":tier["default_prob"],
            "has_loan":    has_loan,
            "label_default": int(tier["default_prob"] > 0.25),
        })
    sme_df = pd.DataFrame(smes)

    # ── Generate monthly summaries (lighter than full transactions) ───────────
    months = 24
    records = []
    for _, sme in sme_df.iterrows():
        arch  = ARCHETYPES[sme["archetype"]]
        tier  = CREDIT_TIERS[sme["credit_tier"]]
        balance = float(45000 * (0.5 + sme["credit_score"]/850 * 1.5))
        balance = max(balance * (1 + rng.normal(0, 0.15)), 500)

        for m in range(1, months+1):
            season = MONTHLY_SEASONALITY[((m-1) % 12) + 1]
            stab   = tier["income_stab"]
            reg    = tier["payment_reg"]

            inflow_base  = arch["avg_inflow"]  * arch["avg_daily_txn"] * 22 * season
            outflow_base = arch["avg_outflow"] * arch["avg_daily_txn"] * 22 * season * 0.75

            inflow  = max(0, inflow_base  * (1 + rng.normal(0, 0.3*(1-stab))))
            outflow = max(0, outflow_base * (1 + rng.normal(0, 0.2*(1-stab))))

            # tier-based savings adjustment
            tier_adj = {"prime":0.08,"near_prime":0.02,"subprime":-0.06,"deep_subprime":-0.14}
            io_adj = arch["io_ratio"] + tier_adj[sme["credit_tier"]]
            if rng.random() > io_adj:
                outflow = min(outflow * 1.3, inflow * 1.1)

            has_utility = rng.random() > {
                "prime":0.04,"near_prime":0.18,"subprime":0.42,"deep_subprime":0.72
            }[sme["credit_tier"]]
            has_loan_repay = sme["has_loan"] and rng.random() > (1 - reg)

            balance += inflow - outflow
            if sme["credit_tier"] == "deep_subprime" and rng.random() < 0.08:
                balance -= balance * rng.uniform(0.4, 0.9)
            balance = max(balance, -5000 if sme["credit_tier"] in ("subprime","deep_subprime") else 500)

            inflate = (1.018) ** m

            records.append({
                "sme_id":         sme["sme_id"],
                "month":          m,
                "inflow_ngn":     round(inflow * inflate, 0),
                "outflow_ngn":    round(outflow * inflate, 0),
                "balance_ngn":    round(balance, 0),
                "has_utility":    has_utility,
                "has_loan_repay": has_loan_repay,
                "txn_count":      int(max(1, rng.poisson(arch["avg_daily_txn"] * 22 * season))),
                "credit_tier":    sme["credit_tier"],
            })

    monthly_df = pd.DataFrame(records)

    # ── Build feature matrix ──────────────────────────────────────────────────
    feat_rows = []
    for _, sme in sme_df.iterrows():
        m = monthly_df[monthly_df["sme_id"] == sme["sme_id"]]

        total_in  = m["inflow_ngn"].sum()
        total_out = m["outflow_ngn"].sum()
        inflow_cv = m["inflow_ngn"].std() / max(m["inflow_ngn"].mean(), 1)
        bal_mean  = m["balance_ngn"].mean()
        bal_min   = m["balance_ngn"].min()
        near_zero_rate = (m["balance_ngn"] < 5000).mean()
        utility_months = m["has_utility"].sum()
        loan_months    = m["has_loan_repay"].sum()
        reg_rate       = m["has_loan_repay"].mean() if sme["has_loan"] else m["has_utility"].mean() * 0.6

        # trend
        first_half = m[m["month"] <= 12]["inflow_ngn"].mean()
        second_half= m[m["month"] >  12]["inflow_ngn"].mean()
        is_growing = int(second_half > first_half * 1.05)

        savings_rate = (total_in - total_out) / max(total_in, 1)

        feat_rows.append({
            "sme_id":                sme["sme_id"],
            "vol_total_inflow_ngn":  total_in,
            "vol_total_outflow_ngn": total_out,
            "vol_net_flow_ngn":      total_in - total_out,
            "vol_txn_count":         m["txn_count"].sum(),
            "stab_inflow_cv":        inflow_cv,
            "stab_months_active":    int((m["inflow_ngn"] > 0).sum()),
            "bal_mean_ngn":          bal_mean,
            "bal_min_ngn":           bal_min,
            "bal_near_zero_rate":    near_zero_rate,
            "bal_has_negative":      int(bal_min < 0),
            "out_utility_months":    utility_months,
            "out_utility_reg":       utility_months / 24,
            "out_loan_months":       loan_months,
            "out_has_loan":          int(sme["has_loan"]),
            "reg_rate":              reg_rate,
            "reg_composite":         reg_rate * 0.85,
            "trend_growing":         is_growing,
            "ratio_savings_rate":    savings_rate,
            "ratio_balance_health":  max(0, 1 - near_zero_rate),
            "ratio_balance_cover":   bal_mean / max(total_out / 730, 1),
            # target labels
            "credit_tier":           sme["credit_tier"],
            "credit_score":          sme["credit_score"],
            "default_prob":          sme["default_prob"],
            "label_default":         sme["label_default"],
            "archetype":             sme["archetype"],
            "sector":                sme["sector"],
            "state":                 sme["state"],
        })

    features_df = pd.DataFrame(feat_rows)
    return sme_df, features_df, monthly_df


def score_sme_inputs(inputs: dict) -> dict:
    """
    Rule-based + ML-inspired scorer for the interactive demo page.
    Takes user-entered values and returns a full score response.
    """
    # weighted scoring
    score = 0.30

    reg   = inputs.get("regular_payment_rate", 0)
    bal   = inputs.get("mean_balance_ngn", 0)
    cv    = inputs.get("monthly_inflow_cv", 1)
    util  = inputs.get("utility_months", 0)
    loan  = inputs.get("has_loan_repayment", 0)
    neg   = inputs.get("has_negative_balance", 0)
    nzr   = inputs.get("near_zero_rate", 0)
    grow  = inputs.get("is_growing", 0)
    months= inputs.get("months_active", 0)

    # positive
    score -= reg   * 0.14
    score -= min(bal / 500_000, 1) * 0.09
    score -= max(0, (1 - cv)) * 0.07
    score -= (util / 24) * 0.07
    score -= loan  * 0.08
    score -= grow  * 0.04
    score -= (months / 24) * 0.05

    # negative
    score += neg   * 0.13
    score += nzr   * 0.11
    score += min(cv, 2) * 0.04

    prob_default = float(np.clip(score, 0.02, 0.97))

    # log-odds → score
    lo = np.log(prob_default / (1 - prob_default))
    credit_score = int(np.clip(500 - lo * 50, 150, 850))

    bands = [
        (750,850,"LOW",      "#64ffda","Strong profile — recommended for standard lending."),
        (600,749,"LOW-MEDIUM","#4ade80","Good profile — suitable for most products."),
        (450,599,"MEDIUM",   "#fbbf24","Moderate risk — consider reduced limits."),
        (300,449,"HIGH",     "#f97316","Elevated risk — enhanced due diligence recommended."),
        (150,299,"VERY HIGH","#f87171","High default probability — manual review required."),
    ]
    for lo_s, hi_s, band, colour, guidance in bands:
        if lo_s <= credit_score <= hi_s:
            risk_band, band_colour, lender_guidance = band, colour, guidance
            break
    else:
        risk_band, band_colour, lender_guidance = "UNKNOWN", "#8892b0", ""

    dist = abs(prob_default - 0.5)
    confidence = "HIGH" if dist > 0.35 else "MEDIUM" if dist > 0.20 else "LOW"

    contributors = []
    if reg > 0.6:   contributors.append(("Payment regularity",    "positive", reg * 0.22))
    if loan == 1:   contributors.append(("Loan repayment active", "positive", 0.18))
    if bal > 20000: contributors.append(("Healthy balance",       "positive", min(bal/500000,1)*0.15))
    if util >= 10:  contributors.append(("Utility payment habit", "positive", (util/24)*0.10))
    if grow == 1:   contributors.append(("Business growing",      "positive", 0.08))
    if neg == 1:    contributors.append(("Negative balance events","negative", 0.13))
    if nzr > 0.15:  contributors.append(("Near-zero balance rate","negative", nzr * 0.11))
    if cv > 0.5:    contributors.append(("Income volatility",     "negative", min(cv,2)*0.06))
    contributors.sort(key=lambda x: (-{"positive":1,"negative":-1}[x[1]], -x[2]))

    return {
        "credit_score":    credit_score,
        "risk_band":       risk_band,
        "band_colour":     band_colour,
        "prob_default":    prob_default,
        "confidence":      confidence,
        "contributors":    contributors[:5],
        "lender_guidance": lender_guidance,
        "request_id":      f"CB-{str(uuid.uuid4())[:8].upper()}",
    }

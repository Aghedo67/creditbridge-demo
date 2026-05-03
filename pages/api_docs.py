import streamlit as st

def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">API <span class="accent">Reference</span></div>
        <div class="page-subtitle">Integrate CreditBridge scores into your loan origination system</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Base URL + auth ───────────────────────────────────────────────────────
    st.markdown("##### Base URL & Authentication")
    st.markdown("""
    <div class="code-block">
<span class="code-comment"># Base URL</span>
https://api.creditbridge.co.uk/v1

<span class="code-comment"># All endpoints require Bearer token authentication</span>
<span class="code-comment"># Step 1: Exchange your API key for a JWT token</span>
POST /v1/auth/token?api_key=YOUR_API_KEY

<span class="code-comment"># Step 2: Use the token in all subsequent requests</span>
Authorization: Bearer &lt;your_jwt_token&gt;
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Endpoints ─────────────────────────────────────────────────────────────
    endpoints = [
        {
            "method": "POST", "path": "/v1/score",
            "title": "Score a Single SME",
            "desc": "Submit a transaction summary and receive a credit score within 60 seconds.",
            "method_colour": "#64ffda",
            "request": '''{
  "sme_id": "YOUR_INTERNAL_ID",
  "consent_token": "consent-portal-token",
  "observation_months": 12,
  "transaction_summary": {
    "total_txn_count": 3200,
    "total_inflow_ngn": 4800000,
    "total_outflow_ngn": 3600000,
    "active_days": 280,
    "date_range_days": 365,
    "monthly_inflow_cv": 0.18,
    "months_with_inflow": 12,
    "mean_balance_ngn": 85000,
    "min_balance_ngn": 12000,
    "near_zero_rate": 0.02,
    "has_negative_balance": 0,
    "utility_payment_months": 11,
    "loan_repay_count": 12,
    "has_loan_repayment": 1,
    "regular_payment_rate": 0.88,
    "unique_counterparty_types": 6,
    "has_wholesale_buyer": 1,
    "is_growing": 1
  }
}''',
            "response": '''{
  "request_id": "CB-A1B2C3D4",
  "sme_id": "YOUR_INTERNAL_ID",
  "credit_score": 724,
  "risk_band": "LOW-MEDIUM",
  "probability_of_default": 0.0821,
  "model_confidence": "HIGH",
  "score_version": "creditbridge-v1.0.0",
  "scored_at": "2024-06-15T10:32:11Z",
  "observation_months": 12,
  "top_contributors": [
    {
      "feature": "reg_composite_score",
      "direction": "positive",
      "weight": 0.220,
      "description": "Payment regularity across billing cycles"
    },
    {
      "feature": "out_loan_repay_consistency",
      "direction": "positive",
      "weight": 0.180,
      "description": "Consistency of loan repayment amounts"
    }
  ],
  "lender_guidance": "Good profile — suitable for most products.",
  "disclaimer": "Score generated from alternative data..."
}'''
        },
        {
            "method": "POST", "path": "/v1/score/batch",
            "title": "Batch Score (up to 50 SMEs)",
            "desc": "Submit multiple SMEs in one call. Failed individual scores do not fail the batch.",
            "method_colour": "#64ffda",
            "request": '''{
  "requests": [
    { ...score_request_1... },
    { ...score_request_2... }
  ]
}''',
            "response": '''{
  "batch_id": "BATCH-E5F6G7H8",
  "total_requested": 2,
  "total_scored": 2,
  "scored_at": "2024-06-15T10:32:15Z",
  "results": [ ...array of ScoreResponse objects... ],
  "errors": []
}'''
        },
        {
            "method": "GET", "path": "/v1/lender/usage",
            "title": "Query Usage & Billing",
            "desc": "Check your monthly query consumption and estimated cost.",
            "method_colour": "#a78bfa",
            "request": "No request body required.",
            "response": '''{
  "lender_id": "lender_carbon_001",
  "lender_name": "Carbon Digital Lending",
  "tier": "premium",
  "queries_used": 1420,
  "query_limit": 10000,
  "queries_remaining": 8580,
  "period": "June 2024",
  "cost_estimate_gbp": 1704.00
}'''
        },
        {
            "method": "GET", "path": "/v1/health",
            "title": "Health Check",
            "desc": "Check API status and model version. No authentication required.",
            "method_colour": "#a78bfa",
            "request": "No request body required.",
            "response": '''{
  "status": "healthy",
  "model_version": "1.0.0",
  "api_version": "v1",
  "uptime_seconds": 86423.1,
  "model_loaded": true,
  "timestamp": "2024-06-15T10:32:00Z"
}'''
        },
    ]

    for ep in endpoints:
        with st.expander(f"{ep['method']}  {ep['path']} — {ep['title']}"):
            st.markdown(f"""
            <div style="color:#8892b0;font-size:0.88rem;margin-bottom:16px;
                line-height:1.6">{ep['desc']}</div>
            """, unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Request**")
                st.code(ep["request"], language="json")
            with c2:
                st.markdown("**Response**")
                st.code(ep["response"], language="json")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Pricing ───────────────────────────────────────────────────────────────
    st.markdown("##### Pricing")
    tiers = [
        ("Trial",    "500",    "£0",       "£1.20/query", "Pilot onboarding"),
        ("Standard", "3,000",  "£600/mo",  "£1.20/query", "Growing lenders"),
        ("Premium",  "10,000", "£1,800/mo","£0.95/query", "Volume discount"),
        ("Enterprise","Custom","Custom",   "From £0.70",  "Full integration support"),
    ]
    st.markdown("""<table class="styled-table"><tr>
        <th>Tier</th><th>Monthly Queries</th><th>Subscription</th>
        <th>Per Query</th><th>Best For</th></tr>""", unsafe_allow_html=True)
    for tier, queries, sub, pq, best in tiers:
        st.markdown(f"""<tr>
            <td style="font-weight:600;color:#e8eaf0">{tier}</td>
            <td style="font-family:'DM Mono',monospace">{queries}</td>
            <td style="color:#64ffda;font-family:'DM Mono',monospace">{sub}</td>
            <td style="font-family:'DM Mono',monospace">{pq}</td>
            <td style="color:#8892b0">{best}</td>
        </tr>""", unsafe_allow_html=True)
    st.markdown("</table>", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Python SDK snippet ────────────────────────────────────────────────────
    st.markdown("##### Python Quick Start")
    st.code('''import requests

# 1. Get your token
token_r = requests.post(
    "https://api.creditbridge.co.uk/v1/auth/token",
    params={"api_key": "YOUR_API_KEY"}
)
token = token_r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Score an SME
score_r = requests.post(
    "https://api.creditbridge.co.uk/v1/score",
    headers=headers,
    json={
        "sme_id": "YOUR_BORROWER_ID",
        "consent_token": "consent-abc-123",
        "observation_months": 12,
        "transaction_summary": {
            "total_txn_count": 3200,
            "total_inflow_ngn": 4800000,
            # ... other fields
        }
    }
)

result = score_r.json()
print(f"Score: {result['credit_score']} | Band: {result['risk_band']}")
# Score: 724 | Band: LOW-MEDIUM
''', language="python")

    st.markdown("""
    <div class="info-panel">
        <strong style="color:#64ffda">Developer Documentation</strong><br>
        Full API docs, SDK libraries, and integration guides available at
        <a href="https://docs.creditbridge.co.uk" style="color:#64ffda">
        docs.creditbridge.co.uk</a> · API support:
        <a href="mailto:api@creditbridge.co.uk" style="color:#64ffda">
        api@creditbridge.co.uk</a>
    </div>
    """, unsafe_allow_html=True)

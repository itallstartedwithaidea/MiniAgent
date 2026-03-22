"""
MiniAgent Web Demo — Streamlit chat interface.

Usage:
    pip install streamlit
    streamlit run scripts/web_demo.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="MiniAgent", page_icon="🤖", layout="wide")

st.title("🤖 MiniAgent — Advertising AI")
st.caption("The Cowork Agent for Everything. Ask about Google Ads, Meta, PPC math, GAQL, campaign structure.")

# Knowledge base for demo mode
KB = {
    "cpa": "**CPA** (Cost Per Acquisition) = Total Cost ÷ Total Conversions.\n\nBenchmarks:\n- B2B SaaS: $50-200\n- Ecommerce: $10-50\n- Lead Gen: $20-100\n\nTarget: 10-20% of first-year customer value.",
    "roas": "**ROAS** (Return On Ad Spend) = Revenue ÷ Cost.\n\nBenchmarks:\n- Ecommerce: 3-5x\n- Lead Gen: 5-10x\n- Brand: 1-2x\n\nBreak-even ROAS = 1 ÷ Profit Margin.",
    "quality score": "**Quality Score** (1-10) is determined by:\n1. Expected CTR\n2. Ad Relevance\n3. Landing Page Experience\n\nScore 7+ = good. Below 5 = you're overpaying. Each point below 7 increases CPC ~16%.",
    "impression share": "**Impression Share** = Impressions ÷ Eligible Impressions.\n\nLost IS breaks into:\n- **Budget Lost**: Need more daily budget\n- **Rank Lost**: Need better Quality Score or higher bids\n\nBelow 70% = significant missed opportunity.",
    "gaql": "**GAQL Example:**\n```sql\nSELECT campaign.name, metrics.cost_micros,\n       metrics.conversions, metrics.search_impression_share\nFROM campaign\nWHERE segments.date DURING LAST_30_DAYS\nORDER BY metrics.cost_micros DESC\n```\n\nNote: `cost_micros` ÷ 1,000,000 = actual dollars.",
    "negative keywords": "**Universal negatives to add immediately:**\n- free, cheap, DIY, jobs, salary\n- reddit, youtube, how to, what is\n- download, template, sample, example\n\nThen: Search Terms Report weekly → add irrelevant terms.",
    "meta vs google": "**Google Ads** = intent-based (people searching)\n**Meta Ads** = interruption-based (people browsing)\n\nGoogle: Higher CPC ($2-15), higher CVR (3-8%)\nMeta: Lower CPC ($0.50-3), lower CVR (1-3%)\n\nStart 70/30 Google/Meta for demand capture vs creation.",
    "cost_micros": "**cost_micros** is Google Ads API's currency format.\n\nDivide by 1,000,000 for actual dollars.\n- 45000000 = $45.00\n- 1500000 = $1.50\n- 100000000 = $100.00",
    "campaign structure": "**Standard campaign structure:**\n1. **Brand** (10-15% budget) — exact match brand terms\n2. **Non-Brand** (40-50%) — high-intent category keywords\n3. **Shopping/PMax** (25-30%) — product feed campaigns\n4. **Remarketing** (5-10%) — cart abandoners, past visitors\n5. **Competitor** (5-10%) — competitor brand terms (optional)",
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Google Ads, PPC, GAQL, campaign structure..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = None
    for key, answer in KB.items():
        if key in prompt.lower():
            response = answer
            break
    if not response:
        response = ("I can help with:\n- **CPA, ROAS, CTR** calculations\n- **GAQL** query writing\n"
                    "- **Campaign structure** recommendations\n- **Quality Score** optimization\n"
                    "- **Negative keywords** strategy\n- **Google vs Meta** comparison\n"
                    "- **Impression share** analysis\n\nTry asking about any of these!")

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

st.sidebar.markdown("### About")
st.sidebar.markdown("**MiniAgent** — The Cowork Agent for Everything")
st.sidebar.markdown("Train from zero. Run everywhere.")
st.sidebar.markdown("---")
st.sidebar.markdown("[GitHub](https://github.com/itallstartedwithaidea/MiniAgent) · [Website](https://googleadsagent.ai)")

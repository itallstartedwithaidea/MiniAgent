"""
MiniAgent — Google Ads MCP Server
29 tools for Google Ads API v23.

Usage:
    python -m miniagent.mcp.google_ads          # stdio (Claude Code, Cursor)
    python -m miniagent.mcp.google_ads --http    # HTTP (remote clients)

Claude Code:
    claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
"""

from fastmcp import FastMCP

mcp = FastMCP(
    name="MiniAgent — Google Ads MCP",
    mask_error_details=False,
)


# ─── READ TOOLS ───────────────────────────────────────────────────────────────

@mcp.tool()
async def list_accounts() -> str:
    """List all accessible Google Ads accounts (MCC traversal)."""
    return "TODO: Implement — see google-ads-mcp-server for reference implementation"


@mcp.tool()
async def get_campaign_performance(customer_id: str, date_range: str = "LAST_30_DAYS") -> str:
    """Get campaign performance metrics for a Google Ads account."""
    return "TODO: Implement"


@mcp.tool()
async def get_keyword_performance(customer_id: str, campaign_id: str = None) -> str:
    """Get keyword-level performance data."""
    return "TODO: Implement"


@mcp.tool()
async def get_search_terms(customer_id: str, campaign_id: str = None) -> str:
    """Get search terms report — see what people actually searched."""
    return "TODO: Implement"


@mcp.tool()
async def execute_gaql(customer_id: str, query: str) -> str:
    """Execute a raw GAQL query against the Google Ads API."""
    return "TODO: Implement"


@mcp.tool()
async def get_account_budget_summary(customer_id: str) -> str:
    """Get account-level budget summary with spend pacing."""
    return "TODO: Implement"


# ─── AUDIT TOOLS ──────────────────────────────────────────────────────────────

@mcp.tool()
async def audit_account(customer_id: str) -> str:
    """Run a 7-dimension account audit with severity ratings."""
    return "TODO: Implement"


@mcp.tool()
async def audit_quality_score(customer_id: str) -> str:
    """Audit Quality Score distribution across keywords."""
    return "TODO: Implement"


@mcp.tool()
async def audit_wasted_spend(customer_id: str) -> str:
    """Identify wasted spend from irrelevant search terms."""
    return "TODO: Implement"


# ─── WRITE TOOLS (CEP Protocol) ──────────────────────────────────────────────

@mcp.tool()
async def pause_campaign(customer_id: str, campaign_id: str) -> str:
    """Pause a campaign. Uses Confirm-Execute-Postcheck protocol."""
    return "TODO: Implement"


@mcp.tool()
async def update_budget(customer_id: str, campaign_id: str, new_budget_micros: int) -> str:
    """Update daily budget for a campaign."""
    return "TODO: Implement"


@mcp.tool()
async def add_negative_keywords(customer_id: str, campaign_id: str, keywords: list[str]) -> str:
    """Add negative keywords to a campaign."""
    return "TODO: Implement"


# ─── DOC TOOLS ────────────────────────────────────────────────────────────────

@mcp.tool()
async def get_gaql_reference() -> str:
    """Get GAQL syntax reference — callable by the LLM at runtime."""
    return """
GAQL (Google Ads Query Language) Quick Reference:

SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 50

Common resources: campaign, ad_group, ad_group_ad, ad_group_criterion,
keyword_view, search_term_view, shopping_performance_view

Common metrics: impressions, clicks, cost_micros, conversions,
search_impression_share, search_budget_lost_impression_share

Date predicates: LAST_7_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH,
BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'

Note: cost_micros must be divided by 1,000,000 for actual currency.
"""


@mcp.tool()
async def get_workflow_guide() -> str:
    """Get advertising workflow guide for the LLM."""
    return """
Google Ads Workflow Guide for AI Agents:

1. ALWAYS start with list_accounts() to understand account structure
2. Use get_campaign_performance() for top-level health check
3. For deep analysis, use execute_gaql() with custom queries
4. Before any writes, confirm with the user (CEP protocol)
5. After writes, verify with a postcheck query

Common analysis flow:
- Performance declining? → get_search_terms() → audit_wasted_spend()
- CPA too high? → audit_quality_score() → get_keyword_performance()
- Budget questions? → get_account_budget_summary()
"""


# ─── KEYWORD PLANNER ─────────────────────────────────────────────────────────

@mcp.tool()
async def get_keyword_ideas(customer_id: str, seed_keywords: list[str]) -> str:
    """Get keyword ideas from Google's Keyword Planner."""
    return "TODO: Implement"


def main():
    import sys
    if "--http" in sys.argv:
        mcp.run(transport="http", host="0.0.0.0", port=8000)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

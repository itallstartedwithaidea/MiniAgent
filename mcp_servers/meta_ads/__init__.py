"""
MiniAgent — Meta Ads MCP Server
18 tools for Meta Marketing API.

Usage:
    python -m miniagent.mcp.meta_ads
    claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
"""

from fastmcp import FastMCP

mcp = FastMCP(name="MiniAgent — Meta Ads MCP", mask_error_details=False)


@mcp.tool()
async def list_ad_accounts() -> str:
    """List all accessible Meta ad accounts."""
    return "TODO: Implement via /me/adaccounts endpoint"

@mcp.tool()
async def get_campaign_insights(account_id: str, date_preset: str = "last_30d") -> str:
    """Get campaign performance insights (impressions, clicks, spend, conversions)."""
    return "TODO: Implement via /{account_id}/insights"

@mcp.tool()
async def get_ad_set_insights(account_id: str, campaign_id: str = None) -> str:
    """Get ad set level performance data."""
    return "TODO: Implement"

@mcp.tool()
async def get_ad_creative_insights(account_id: str) -> str:
    """Get creative-level performance for A/B test analysis."""
    return "TODO: Implement"

@mcp.tool()
async def get_audience_insights(account_id: str) -> str:
    """Get audience performance breakdown."""
    return "TODO: Implement"

@mcp.tool()
async def create_custom_audience(account_id: str, name: str, source: str) -> str:
    """Create a custom audience from website visitors, email list, or app activity."""
    return "TODO: Implement"

@mcp.tool()
async def create_lookalike_audience(account_id: str, source_audience_id: str, country: str = "US") -> str:
    """Create a lookalike audience from a source custom audience."""
    return "TODO: Implement"

@mcp.tool()
async def pause_campaign(account_id: str, campaign_id: str) -> str:
    """Pause a Meta campaign. Uses CEP protocol."""
    return "TODO: Implement"

@mcp.tool()
async def update_budget(account_id: str, campaign_id: str, new_daily_budget: float) -> str:
    """Update daily budget for a campaign or ad set."""
    return "TODO: Implement"

@mcp.tool()
async def get_platform_reference() -> str:
    """Get Meta Ads platform reference for the LLM."""
    return """
Meta Ads API Quick Reference:

Hierarchy: Campaign → Ad Set → Ad
Budget: Set at campaign level (CBO) or ad set level
Targeting: Custom audiences, lookalike audiences, interest/behavior targeting
Optimization: Conversions, link clicks, impressions, reach, landing page views

Key metrics:
- spend (dollars, not micros like Google)
- impressions, reach, frequency
- link_clicks (actual link clicks)
- actions (conversions by type)
- cost_per_action_type (CPA by conversion type)

Date presets: today, yesterday, this_month, last_month, last_7d, last_14d, last_30d, last_90d
"""


def main():
    import sys
    mcp.run(transport="http" if "--http" in sys.argv else "stdio")

if __name__ == "__main__":
    main()

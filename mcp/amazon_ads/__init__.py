"""MiniAgent — amazon ads MCP Server. Status: Scaffold."""
from fastmcp import FastMCP
mcp = FastMCP(name="MiniAgent — amazon ads MCP", mask_error_details=False)

@mcp.tool()
async def list_campaigns() -> str:
    """List all campaigns in the amazon ads account."""
    return "TODO: Implement amazon ads API integration"

@mcp.tool()
async def get_campaign_performance(campaign_id: str = None) -> str:
    """Get campaign performance metrics."""
    return "TODO: Implement"

@mcp.tool()
async def get_platform_reference() -> str:
    """Get amazon ads platform reference."""
    return "amazon ads MCP server — scaffold. Full implementation coming in v0.3.0."

def main():
    import sys
    mcp.run(transport="http" if "--http" in sys.argv else "stdio")

if __name__ == "__main__":
    main()

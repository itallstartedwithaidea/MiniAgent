"""MiniAgent — criteo MCP Server. Status: Scaffold."""
from fastmcp import FastMCP
mcp = FastMCP(name="MiniAgent — criteo MCP", mask_error_details=False)

@mcp.tool()
async def list_campaigns() -> str:
    """List all campaigns in the criteo account."""
    return "TODO: Implement criteo API integration"

@mcp.tool()
async def get_campaign_performance(campaign_id: str = None) -> str:
    """Get campaign performance metrics."""
    return "TODO: Implement"

@mcp.tool()
async def get_platform_reference() -> str:
    """Get criteo platform reference."""
    return "criteo MCP server — scaffold. Full implementation coming in v0.3.0."

def main():
    import sys
    mcp.run(transport="http" if "--http" in sys.argv else "stdio")

if __name__ == "__main__":
    main()

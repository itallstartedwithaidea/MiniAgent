"""Tests for MCP server tools."""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_google_ads_mcp_imports():
    from mcp_servers.google_ads import mcp
    assert mcp.name == "MiniAgent — Google Ads MCP"

def test_gaql_reference():
    from mcp_servers.google_ads import get_gaql_reference
    result = asyncio.run(get_gaql_reference())
    assert "SELECT" in result
    assert "cost_micros" in result

def test_workflow_guide():
    from mcp_servers.google_ads import get_workflow_guide
    result = asyncio.run(get_workflow_guide())
    assert "list_accounts" in result

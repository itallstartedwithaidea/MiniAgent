---
name: google-ads-mcp
description: "Use when the user needs to SET UP, CONFIGURE, or TROUBLESHOOT MCP server connections for Google Ads or any advertising platform. Trigger for: MCP setup, MCP config, API credentials, OAuth, developer token, authentication errors, connection issues, 'connect to Google Ads', 'set up MCP', or any MCP server configuration question."
---

# Google Ads MCP Setup Skill

Guide for connecting MiniAgent's MCP servers to real ad platform APIs.

## Claude Code Setup

```bash
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
```

Or add to `.mcp.json`:
```json
{
  "mcpServers": {
    "miniagent-google": {
      "command": "python",
      "args": ["-m", "miniagent.mcp.google_ads"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your-token",
        "GOOGLE_ADS_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_ADS_CLIENT_SECRET": "your-secret",
        "GOOGLE_ADS_REFRESH_TOKEN": "your-refresh-token",
        "GOOGLE_ADS_CUSTOMER_ID": "1234567890"
      }
    }
  }
}
```

## Getting Credentials

1. **Developer Token**: Google Ads → Tools → API Center → Apply
2. **OAuth Client**: Google Cloud Console → APIs → Credentials → Create OAuth Client ID
3. **Refresh Token**: Run `python -m miniagent.mcp.google_ads --oauth` to start the OAuth flow
4. **Customer ID**: The 10-digit number in the top-right of Google Ads (no dashes)

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `AUTHENTICATION_ERROR` | Bad credentials | Check all 4 env vars are set |
| `AUTHORIZATION_ERROR` | No access to account | Verify customer_id, check MCC access |
| `DEVELOPER_TOKEN_NOT_APPROVED` | Token pending | Apply at Google Ads API Center |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Add retry logic, check quota |

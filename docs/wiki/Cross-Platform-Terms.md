# Cross-Platform Advertising Terminology

How the same concepts map across platforms.

## Account Hierarchy

| Level | Google Ads | Meta Ads | Microsoft Ads | Amazon Ads | TradeDesk |
|-------|-----------|----------|--------------|------------|-----------|
| Top | MCC (Manager) | Business Manager | Manager Account | Portfolio | Partner |
| Account | Customer ID | Ad Account | Account | Advertiser | Advertiser |
| Container | Campaign | Campaign | Campaign | Campaign | Campaign |
| Targeting | Ad Group | Ad Set | Ad Group | Ad Group | Ad Group |
| Creative | Ad | Ad | Ad | Ad | Creative |

## Metrics Mapping

| Concept | Google Ads | Meta Ads | Microsoft Ads | Amazon Ads |
|---------|-----------|----------|--------------|------------|
| Cost | `cost_micros` (÷1M) | `spend` (dollars) | `Spend` (dollars) | `cost` (dollars) |
| Clicks | `clicks` | `link_clicks` | `Clicks` | `clicks` |
| Impressions | `impressions` | `impressions` | `Impressions` | `impressions` |
| Conversions | `conversions` | `actions` | `Conversions` | `purchases` |
| Conv Value | `conversions_value` | `action_values` | `Revenue` | `sales` |
| CTR | `ctr` | `ctr` | `Ctr` | `clickThroughRate` |
| CPC | `average_cpc` (micros) | `cpc` (dollars) | `AverageCpc` | `costPerClick` |
| Impression Share | `search_impression_share` | N/A | `ImpressionSharePercent` | `impressionShare` |

## Bidding Strategies

| Strategy | Google Ads | Meta Ads | Microsoft Ads |
|----------|-----------|----------|--------------|
| Maximize Clicks | `MAXIMIZE_CLICKS` | `LOWEST_COST_WITHOUT_CAP` | `MaxClicks` |
| Target CPA | `TARGET_CPA` | `COST_CAP` | `TargetCpa` |
| Target ROAS | `TARGET_ROAS` | `MINIMUM_ROAS` | `TargetRoas` |
| Max Conversions | `MAXIMIZE_CONVERSIONS` | `LOWEST_COST_WITH_BID_CAP` | `MaxConversions` |
| Manual CPC | `MANUAL_CPC` | `BID_CAP` | `ManualCpc` |

## Match Types (Search)

| Type | Google Ads | Microsoft Ads | Description |
|------|-----------|--------------|-------------|
| Broad | `BROAD` | `Broad` | Widest reach, loosest matching |
| Phrase | `PHRASE` | `Phrase` | Query must contain phrase |
| Exact | `EXACT` | `Exact` | Query must match exactly |

*Meta and Amazon don't use keyword match types — they use interest/behavior targeting and product targeting respectively.*

## Campaign Types

| Type | Google | Meta | Microsoft | Amazon |
|------|--------|------|-----------|--------|
| Search | Search Campaign | N/A | Search Campaign | Sponsored Products |
| Shopping | Shopping / PMax | Catalog Sales | Shopping Campaign | Sponsored Products |
| Display | Display Campaign | N/A | Audience Campaign | Sponsored Display |
| Video | Video Campaign | Video Views | Video Campaign | Sponsored Brands Video |
| App | App Campaign | App Installs | App Install | N/A |
| Auto-Optimized | Performance Max | Advantage+ | Performance Max | Auto Campaign |

## API Authentication

| Platform | Auth Method | Key Fields |
|----------|-------------|------------|
| Google Ads | OAuth 2.0 + Developer Token | client_id, client_secret, refresh_token, developer_token, customer_id |
| Meta Ads | Long-Lived User Token | access_token, app_id, app_secret, ad_account_id |
| Microsoft Ads | OAuth 2.0 | client_id, client_secret, refresh_token, developer_token, account_id |
| Amazon Ads | OAuth 2.0 + LWA | client_id, client_secret, refresh_token, profile_id |
| TradeDesk | API Key | partner_id, api_key |

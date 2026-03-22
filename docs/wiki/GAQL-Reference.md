# GAQL Reference

Google Ads Query Language (GAQL) reference for MiniAgent.

## Basic Syntax

```sql
SELECT field1, field2, ...
FROM resource
WHERE condition
ORDER BY field [ASC|DESC]
LIMIT n
```

## Common Queries

### Campaign Performance
```sql
SELECT campaign.name, campaign.status, campaign.bidding_strategy_type,
       metrics.impressions, metrics.clicks, metrics.cost_micros,
       metrics.conversions, metrics.conversions_value,
       metrics.search_impression_share,
       metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

### Keyword Performance
```sql
SELECT ad_group_criterion.keyword.text,
       ad_group_criterion.keyword.match_type,
       ad_group_criterion.quality_info.quality_score,
       metrics.impressions, metrics.clicks, metrics.cost_micros,
       metrics.conversions, metrics.average_cpc
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

### Search Terms (Wasted Spend)
```sql
SELECT search_term_view.search_term,
       metrics.impressions, metrics.clicks,
       metrics.cost_micros, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.conversions = 0
  AND metrics.cost_micros > 5000000
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

### Shopping Performance by Product
```sql
SELECT segments.product_item_id, segments.product_title,
       metrics.impressions, metrics.clicks, metrics.cost_micros,
       metrics.conversions, metrics.search_impression_share
FROM shopping_performance_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

### Auction Insights (Competitors)
```sql
SELECT auction_insights.display_url,
       metrics.search_impression_share,
       metrics.search_overlap_rate,
       metrics.search_outranking_share
FROM auction_insights
WHERE segments.date DURING LAST_30_DAYS
```

## Date Predicates

| Predicate | Description |
|-----------|-------------|
| `LAST_7_DAYS` | Last 7 days |
| `LAST_14_DAYS` | Last 14 days |
| `LAST_30_DAYS` | Last 30 days |
| `THIS_MONTH` | Current month to date |
| `LAST_MONTH` | Previous full month |
| `THIS_QUARTER` | Current quarter to date |
| `BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` | Custom range |

**Important**: When using `BETWEEN` or `DURING`, `segments.date` must be in the SELECT clause.

## Resources

| Resource | Description |
|----------|-------------|
| `campaign` | Campaign-level data |
| `ad_group` | Ad group-level data |
| `ad_group_ad` | Ad-level data |
| `ad_group_criterion` | Keyword and targeting criteria |
| `keyword_view` | Keyword performance (join of ad_group_criterion + metrics) |
| `search_term_view` | Actual search queries that triggered ads |
| `shopping_performance_view` | Shopping campaign product-level data |
| `auction_insights` | Competitive metrics |
| `change_event` | Account change history |

## Key Metric Notes

- `cost_micros`: Divide by 1,000,000 for actual currency
- `average_cpc`: Already in micros, divide by 1,000,000
- `conversions`: Can be fractional (data-driven attribution)
- `search_impression_share`: 0.0 to 1.0 (multiply by 100 for percentage)

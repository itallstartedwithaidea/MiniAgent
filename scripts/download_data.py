"""
MiniAgent Data Downloader

Downloads training datasets for each stage.

Usage:
    python scripts/download_data.py --all
    python scripts/download_data.py --pretrain
    python scripts/download_data.py --sft
"""

import os
import json
import argparse


def create_pretrain_data():
    """Generate advertising pretrain corpus."""
    path = "./dataset/pretrain_ads.jsonl"
    os.makedirs("./dataset", exist_ok=True)
    
    # Core advertising knowledge
    texts = [
        "Google Ads uses a pay-per-click model where advertisers bid on keywords. The Quality Score is determined by expected click-through rate, ad relevance, and landing page experience. Higher Quality Scores result in lower cost-per-click and better ad positions. Ad Rank equals Max CPC Bid multiplied by Quality Score.",
        "GAQL (Google Ads Query Language) is used to query the Google Ads API. Resources include campaign, ad_group, ad_group_ad, ad_group_criterion, keyword_view, search_term_view, and shopping_performance_view. Metrics are prefixed with metrics. and include impressions, clicks, cost_micros, conversions, and search_impression_share.",
        "Search impression share is the percentage of impressions received divided by the estimated number of impressions eligible to receive. Lost impression share is divided into budget lost impression share (daily budget too low) and rank lost impression share (Quality Score or bids too low).",
        "Cost per acquisition (CPA) equals total cost divided by total conversions. Return on ad spend (ROAS) equals conversion value divided by cost. Click-through rate (CTR) equals clicks divided by impressions. Conversion rate (CVR) equals conversions divided by clicks.",
        "Negative keywords prevent ads from showing for irrelevant searches. Match types include broad match (widest reach), phrase match (query must contain phrase), and exact match (query must match exactly). Broad match modifier was deprecated and merged into phrase match.",
        "Meta Ads Manager uses a campaign-ad set-ad hierarchy. Campaign Budget Optimization (CBO) sets budget at campaign level. Targeting includes custom audiences (website visitors, email lists), lookalike audiences (similar to custom audiences), and interest-based targeting.",
        "Microsoft Advertising supports importing campaigns directly from Google Ads. Key differences include lower average CPCs, older demographic skew, LinkedIn profile targeting integration, and different auction dynamics with less competition.",
        "Amazon Sponsored Products use automatic and manual targeting. Automatic targeting matches ads to relevant customer searches. Manual targeting uses keyword targeting or product targeting. ACOS (Advertising Cost of Sales) equals ad spend divided by ad revenue.",
        "The TradeDesk is a demand-side platform (DSP) for programmatic advertising across display, video, audio, native, and connected TV inventory. It uses real-time bidding with optimized CPM, target CPA, and maximize conversions strategies.",
        "Performance Max campaigns in Google Ads use machine learning to optimize across Search, Shopping, Display, YouTube, Discover, Gmail, and Maps. They require asset groups with text, image, and video assets plus audience signals.",
        "Google Ads API v23 is the current version. API versions are sunset approximately 12 months after release. The Python client library google-ads version 25.1.0 or higher supports v23. Authentication requires a developer token, OAuth client credentials, and a customer ID.",
        "Conversion tracking in Google Ads uses the global site tag (gtag.js) or Google Tag Manager. Primary conversions are used for Smart Bidding optimization. Secondary conversions are tracked but not used for bidding. Offline conversions can be imported via the API using gclid.",
        "Reddit Ads offers conversation placement targeting, interest targeting, and community (subreddit) targeting. Ad formats include promoted posts, video ads, and carousel ads. Best practices include authentic language and understanding subreddit culture.",
        "LinkedIn Ads uses a campaign-campaign group hierarchy with objective-based campaign creation. Targeting includes job title, company, industry, skills, and matched audiences. Lead Gen Forms capture leads without leaving LinkedIn.",
        "TikTok Ads uses a campaign-ad group-ad hierarchy similar to Meta. The Business API rate limit is 10 requests per second. Key targeting includes interest, behavior, custom audiences, and lookalike audiences. Spark Ads boost organic content.",
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(200):  # Repeat for training volume
            for text in texts:
                f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")
    
    print(f"✅ Pretrain data: {path} ({len(texts) * 200} samples)")


def create_sft_data():
    """Generate advertising SFT instruction-response pairs."""
    path = "./dataset/sft_ads.jsonl"
    os.makedirs("./dataset", exist_ok=True)
    
    pairs = [
        {"user": "What is a good CPA for a B2B SaaS campaign?", "assistant": "For B2B SaaS, target CPA should be 10-20% of your first-year ACV (Annual Contract Value). For a $10K ACV product, aim for $1,000-$2,000 CPA. For $50K ACV, $5,000-$10,000 is acceptable. Key levers: tighten match types, add negatives from search terms report, improve landing page CVR, use target CPA bidding with 2-week learning period."},
        {"user": "Write a GAQL query for top campaigns by spend.", "assistant": "SELECT campaign.name, campaign.status, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.search_impression_share FROM campaign WHERE segments.date DURING LAST_30_DAYS AND campaign.status != 'REMOVED' ORDER BY metrics.cost_micros DESC LIMIT 10. Note: cost_micros divided by 1,000,000 gives actual currency."},
        {"user": "My impression share dropped from 80% to 45%. Why?", "assistant": "A 35-point drop in one week points to three possible causes: 1) Budget constraint — check search_budget_lost_impression_share. If it spiked, daily budget isn't keeping up. 2) Quality Score drop — check search_rank_lost_impression_share. Look at keyword-level QS changes. 3) Competition surge — check Auction Insights for new competitors with aggressive bids. Most likely for a sudden drop: budget. Check daily spend vs daily budget over last 7 days."},
        {"user": "How should I structure campaigns for 500 products?", "assistant": "Tiered structure: Campaign 1 Brand (10-15% budget) — exact match brand terms. Campaign 2 Top Products via Performance Max (40-50%) — top 50 products by margin. Campaign 3 Category Shopping (25-30%) — standard Shopping by category with priority settings. Campaign 4 Non-Brand Search (10-15%) — high-intent category keywords. Campaign 5 Remarketing (5-10%) — cart abandoners. Start with 1-2, prove ROI, then expand."},
        {"user": "Compare Google Ads and Meta Ads for lead gen.", "assistant": "Google Ads Search: intent-based, higher CPC ($2-15), higher CVR (3-8%), best for bottom-funnel. Typical CPL $30-100 B2B. Meta Ads: interruption-based, lower CPC ($0.50-3), lower CVR (1-3%), best for top-funnel and visual products. Typical CPL $15-60 B2B. Use both: Google captures existing demand, Meta creates new demand. Start 70/30 Google/Meta, adjust after 30 days of data."},
        {"user": "What cost_micros means?", "assistant": "cost_micros is Google Ads API's currency format. The value is in millionths of the account's currency. Divide by 1,000,000 to get actual dollars. Examples: 45000000 = $45.00, 1500000 = $1.50, 100000000 = $100.00. This applies to cost_micros, average_cpc, and other monetary fields in GAQL responses."},
        {"user": "How do I find wasted spend in Google Ads?", "assistant": "Run the Search Terms Report via GAQL: SELECT search_term_view.search_term, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS AND metrics.conversions = 0 ORDER BY metrics.cost_micros DESC LIMIT 50. This shows queries spending money with zero conversions. Add irrelevant ones as negative keywords. Typically 20-40% of spend goes to irrelevant terms in unoptimized accounts."},
        {"user": "What negative keywords should I add first?", "assistant": "Universal negatives for most B2B/service campaigns: free, cheap, DIY, jobs, salary, career, intern, reddit, youtube, how to, what is, tutorial, download, template, sample, example, course, training, certification. Then industry-specific: for SaaS add open source and self-hosted, for services add near me if not local, for premium add discount and coupon. Review Search Terms Report weekly."},
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(100):
            for pair in pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    
    print(f"✅ SFT data: {path} ({len(pairs) * 100} pairs)")


def create_dpo_data():
    """Generate DPO preference pairs (good vs bad advice)."""
    path = "./dataset/dpo_ads.jsonl"
    os.makedirs("./dataset", exist_ok=True)
    
    pairs = [
        {"prompt": "How should I set up keyword match types?", "chosen": "Start with exact match for your highest-intent keywords to control spend. After 2 weeks of data, expand top performers to phrase match. Only use broad match with Smart Bidding (target CPA or ROAS) and strong negative keyword lists.", "rejected": "Use broad match on everything to maximize traffic volume. More impressions means more clicks means more conversions."},
        {"prompt": "My CPA is too high. What should I do?", "chosen": "Check these in order: 1) Search Terms Report for irrelevant queries eating budget. 2) Keyword-level performance — pause keywords with CPA 2x above target. 3) Landing page conversion rate — even small improvements compound. 4) Ad copy relevance to search intent. 5) Bid strategy — if using manual CPC, consider target CPA.", "rejected": "Just increase your budget. More spend means the algorithm has more data to optimize. Google's AI will figure it out eventually."},
        {"prompt": "Should I run Performance Max?", "chosen": "PMax works well when you have: 1) strong conversion data (50+ conversions/month), 2) quality creative assets (text, images, video), 3) properly configured conversion tracking. Start with it alongside existing Search campaigns, don't replace them. Monitor Search impression share — PMax can cannibalize your brand traffic.", "rejected": "Yes, switch everything to Performance Max immediately. Google recommends it and their AI is better than manual management."},
        {"prompt": "How much should I spend on Google Ads?", "chosen": "Work backwards from your target: If target CPA is $50 and you want 100 leads/month, budget = $5,000/month. Start at 50-70% of that to test, then scale what works. Never set a budget you can't sustain for 3 months — Smart Bidding needs consistent data.", "rejected": "Start with $10/day and see what happens. You can always increase later if it works."},
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(50):
            for pair in pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    
    print(f"✅ DPO data: {path} ({len(pairs) * 50} pairs)")


def main():
    parser = argparse.ArgumentParser(description="MiniAgent Data Downloader")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--pretrain", action="store_true")
    parser.add_argument("--sft", action="store_true")
    parser.add_argument("--dpo", action="store_true")
    args = parser.parse_args()

    if args.all or args.pretrain:
        create_pretrain_data()
    if args.all or args.sft:
        create_sft_data()
    if args.all or args.dpo:
        create_dpo_data()
    if not any([args.all, args.pretrain, args.sft, args.dpo]):
        print("Usage: python scripts/download_data.py --all")
        print("  --pretrain  Download pretrain corpus")
        print("  --sft       Download SFT instruction pairs")
        print("  --dpo       Download DPO preference pairs")
        print("  --all       Download everything")


if __name__ == "__main__":
    main()

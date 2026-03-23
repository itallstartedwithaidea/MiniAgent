"""
MiniAgent Data & Tokenizer Setup

Downloads minimind's tokenizer (6400 vocab) and generates advertising training data.

Usage:
    python scripts/download_data.py --all          # tokenizer + all data
    python scripts/download_data.py --tokenizer     # just tokenizer
    python scripts/download_data.py --pretrain      # pretrain corpus
    python scripts/download_data.py --sft           # SFT instruction pairs
    python scripts/download_data.py --dpo           # DPO preference pairs
    python scripts/download_data.py --base-model    # minimind pretrained weights (for transfer learning)
"""

import os
import json
import argparse


def download_tokenizer():
    """Download minimind's 6400-vocab tokenizer from HuggingFace."""
    tokenizer_dir = "./model/tokenizer"
    if os.path.exists(os.path.join(tokenizer_dir, "tokenizer.json")):
        print(f"  Tokenizer already exists at {tokenizer_dir}")
        return

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        os.system("pip install -q huggingface_hub")
        from huggingface_hub import hf_hub_download

    os.makedirs(tokenizer_dir, exist_ok=True)

    for fname in ["tokenizer.json", "tokenizer_config.json", "special_tokens_map.json"]:
        print(f"  Downloading {fname}...")
        hf_hub_download(
            "jingyaogong/MiniMind2", fname,
            local_dir=tokenizer_dir, local_dir_use_symlinks=False
        )

    print(f"✅ Tokenizer: {tokenizer_dir} (vocab_size=6400)")


def download_base_model(dim: int = 512):
    """Download minimind's pretrained checkpoint for transfer learning (skip pretrain)."""
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        os.system("pip install -q huggingface_hub")
        from huggingface_hub import hf_hub_download

    out_dir = "./minimind_base"
    os.makedirs(out_dir, exist_ok=True)

    for fname in ["model.safetensors", "config.json", "tokenizer.json",
                  "tokenizer_config.json", "special_tokens_map.json"]:
        print(f"  Downloading {fname}...")
        hf_hub_download(
            "jingyaogong/MiniMind2", fname,
            local_dir=out_dir, local_dir_use_symlinks=False
        )

    print(f"✅ Base model: {out_dir}")
    print(f"   Use: python trainer/sft.py --load_from {out_dir} --from_transformers 1")


def create_pretrain_data():
    """Generate advertising pretrain corpus — diverse knowledge chunks covering 60+ platforms."""
    path = "./dataset/pretrain_ads.jsonl"
    os.makedirs("./dataset", exist_ok=True)

    from scripts.platform_training_data import PLATFORM_PRETRAIN_TEXTS

    texts = [
        # === Google Ads Fundamentals ===
        "Google Ads uses a real-time auction system. When a user searches, Google runs an auction among all ads targeting that query. Ad Rank determines position and is calculated as Max CPC Bid multiplied by Quality Score, plus the expected impact of ad extensions. Higher Ad Rank means better position and often lower actual CPC.",
        "Quality Score in Google Ads is rated 1-10 for each keyword. It has three components: Expected Click-Through Rate (how likely users are to click your ad), Ad Relevance (how closely your ad matches the search intent), and Landing Page Experience (how relevant and useful your landing page is). A Quality Score of 7 or above is considered good.",
        "Google Ads campaign types include Search (text ads on search results), Display (banner ads across websites), Shopping (product listings), Video (YouTube ads), Performance Max (AI-optimized across all channels), App (mobile app installs), Demand Gen (social-style ads on Discover and YouTube), and Local (for physical stores).",
        "Cost Per Click (CPC) in Google Ads is determined by the auction. Actual CPC equals the Ad Rank of the advertiser below you divided by your Quality Score, plus one cent. This means higher Quality Scores directly reduce your costs. Average CPCs vary dramatically by industry: legal ($6-9), insurance ($15-50), B2B SaaS ($3-8), ecommerce ($1-3).",
        "Google Ads account structure follows a hierarchy: Account > Campaign > Ad Group > Ads and Keywords. Each campaign has its own budget and targeting settings. Ad groups contain related keywords and ads. Best practice: 15-20 keywords per ad group maximum, all closely themed. This is called Single Theme Ad Groups (STAGs).",

        # === GAQL ===
        "GAQL (Google Ads Query Language) queries follow the pattern: SELECT fields FROM resource WHERE conditions ORDER BY field LIMIT n. Resources include campaign, ad_group, ad_group_ad, ad_group_criterion, keyword_view, search_term_view, customer, and many more. Fields use dot notation like campaign.name or metrics.impressions.",
        "Common GAQL metrics include metrics.impressions, metrics.clicks, metrics.cost_micros (currency in millionths), metrics.conversions, metrics.conversions_value, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share, and metrics.all_conversions.",
        "GAQL date filtering uses segments.date with special date ranges: DURING TODAY, YESTERDAY, LAST_7_DAYS, LAST_14_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH, THIS_QUARTER, LAST_QUARTER, THIS_YEAR, LAST_YEAR. Custom ranges use BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'.",
        "GAQL supports filtering with WHERE clauses. Common operators: = (equals), != (not equals), > < >= <= (comparisons), IN (list membership), LIKE (pattern matching), CONTAINS ANY/ALL (array operations), IS NULL, IS NOT NULL, DURING (date ranges). Multiple conditions use AND.",
        "The search_term_view resource in GAQL shows what users actually searched. Key query: SELECT search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC. This reveals wasted spend on irrelevant queries.",

        # === Bid Strategies ===
        "Google Ads Smart Bidding strategies use machine learning. Target CPA automatically sets bids to get conversions at your target cost-per-acquisition. Target ROAS sets bids to maximize conversion value at your target return-on-ad-spend. Maximize Conversions gets the most conversions within budget. Maximize Conversion Value gets the most revenue within budget.",
        "Manual CPC bidding gives full control over keyword-level bids. Enhanced CPC (ECPC) adjusts manual bids up or down based on conversion likelihood. Smart Bidding strategies need at least 30 conversions in 30 days to optimize effectively. New campaigns should start with Maximize Clicks or manual CPC until conversion data accumulates.",
        "Target CPA bidding works best with at least 50 conversions per month per campaign. Set the initial target at or slightly above your historical CPA to avoid throttling. Smart Bidding has a learning period of approximately 7-14 days after any change. Avoid making changes during this period or performance data will be unreliable.",
        "Target ROAS bidding requires at least 15 conversions in 30 days per campaign and works best with revenue tracking. Initial target should be set at or below historical ROAS. A target ROAS of 400% means you expect $4 in revenue for every $1 spent. ROAS targets that are too aggressive will severely limit impression volume.",

        # === Match Types ===
        "Keyword match types control which searches trigger your ads. Exact match [keyword] shows ads for searches that match the meaning of your keyword. Phrase match \"keyword\" shows ads for searches that include the meaning of your keyword. Broad match keyword shows ads for searches related to your keyword. Broad match modifier was sunset and merged into phrase match.",
        "Negative keywords prevent ads from showing for irrelevant searches. They also have match types: negative broad (default), negative phrase, and negative exact. Negative broad match excludes searches containing all negative keyword terms in any order. Negative phrase excludes searches containing the exact phrase. Regular review of the Search Terms Report to add negatives is critical for account health.",

        # === Conversion Tracking ===
        "Google Ads conversion tracking uses the global site tag (gtag.js) or Google Tag Manager. Primary conversions are used by Smart Bidding for optimization. Secondary conversions are observed but not used for bidding. Enhanced conversions improve measurement accuracy by securely sending hashed first-party data like email addresses.",
        "Offline conversion tracking imports conversion data back to Google Ads using Google Click ID (gclid) or Enhanced Conversions for Leads. This is critical for B2B where the conversion (e.g., closed deal) happens days or weeks after the click. Upload frequency should be daily or at minimum weekly to give Smart Bidding fresh signals.",
        "Attribution models determine how credit for conversions is assigned. Last click gives 100% credit to the last-clicked ad. Data-driven attribution uses machine learning to distribute credit across touchpoints. Time decay gives more credit to interactions closer to conversion. Google deprecated First Click, Linear, and Position-Based models in favor of Data-Driven Attribution.",

        # === Performance Max ===
        "Performance Max (PMax) campaigns use AI to optimize across all Google channels: Search, Shopping, Display, YouTube, Discover, Gmail, and Maps. They require Asset Groups containing text headlines (up to 15), long headlines (up to 5), descriptions (up to 5), images (up to 20), videos (up to 5), and audience signals.",
        "Performance Max campaigns can cannibalize brand search traffic. Monitor your brand campaign impression share before and after launching PMax. Use brand exclusions (available in PMax settings) to prevent PMax from bidding on your brand terms. PMax should complement, not replace, dedicated brand and non-brand search campaigns.",
        "Asset performance in Performance Max is rated Low, Good, or Best. Replace Low-performing assets regularly. PMax reporting is limited — use Insights tab and asset group reports to understand performance. Third-party scripts can extract more detailed PMax data via the Google Ads API.",

        # === Shopping Campaigns ===
        "Google Shopping campaigns require a Merchant Center feed. Product data must include id, title, description, link, image_link, price, availability, brand, gtin or mpn, and condition. Feed quality directly impacts Shopping ad performance. Optimize titles with primary keywords, brand, and key attributes.",
        "Shopping campaign priority settings (High, Medium, Low) control which campaign serves when multiple campaigns have products matching a search. Common strategy: High priority campaign with low bids for broad terms, Medium for mid-funnel, Low priority with highest bids for proven converters. Combined with shared negative keyword lists for query funneling.",

        # === Meta Ads ===
        "Meta Ads (Facebook and Instagram) use a campaign-ad set-ad hierarchy. Campaign level sets the objective: Awareness, Traffic, Engagement, Leads, App Promotion, or Sales. Campaign Budget Optimization (CBO) distributes budget across ad sets automatically. Ad set level controls targeting, placement, and schedule.",
        "Meta Ads targeting includes Core Audiences (demographics, interests, behaviors), Custom Audiences (website visitors via Pixel, customer lists, app users, video viewers), and Lookalike Audiences (users similar to your custom audiences). Lookalike audience size ranges from 1% (most similar) to 10% (broader reach).",
        "The Meta Pixel tracks website actions for conversion optimization and audience building. Standard events include PageView, ViewContent, AddToCart, InitiateCheckout, Purchase, Lead, CompleteRegistration, and Search. The Conversions API (CAPI) sends server-side events directly to Meta, improving tracking accuracy and attribution.",
        "Meta Ads attribution uses a 7-day click, 1-day view default window. iOS 14.5+ privacy changes via App Tracking Transparency significantly impacted Meta's tracking and attribution. Aggregated Event Measurement limits optimization events to 8 per domain. Server-side Conversions API integration helps recover lost attribution data.",
        "Meta Advantage+ campaigns use AI automation similar to Google's Performance Max. Advantage+ Shopping campaigns require minimal setup: just a catalog, creative assets, and a budget. They automatically optimize targeting, placement, and creative combinations. Best for advertisers with established pixel data and product catalogs.",

        # === Microsoft Ads ===
        "Microsoft Advertising (formerly Bing Ads) offers lower average CPCs than Google Ads, typically 30-50% less. The audience skews older and higher-income. Key differentiator: LinkedIn profile targeting allows targeting by company, job function, and industry. Import campaigns directly from Google Ads to quickly launch on Microsoft.",
        "Universal Event Tracking (UET) is Microsoft Ads' equivalent of Google's conversion tag. It tracks page visits, custom events, and revenue. Microsoft Ads supports automated bidding strategies similar to Google: Target CPA, Target ROAS, Maximize Conversions, and Enhanced CPC.",

        # === Amazon Ads ===
        "Amazon Advertising includes Sponsored Products (keyword-targeted product listings), Sponsored Brands (banner ads with brand logo and multiple products), and Sponsored Display (audience and product targeting across Amazon and third-party sites). ACOS (Advertising Cost of Sales) equals ad spend divided by ad revenue, the primary efficiency metric.",
        "Amazon Sponsored Products use automatic targeting (Amazon matches to relevant searches) and manual targeting (you choose keywords or products). Automatic campaigns are great for keyword research — let them run for 2 weeks, then mine the Search Term Report for converting queries to add to manual campaigns.",

        # === PPC Math ===
        "Cost Per Acquisition (CPA) = Total Cost / Total Conversions. Return on Ad Spend (ROAS) = Conversion Value / Cost. Click-Through Rate (CTR) = Clicks / Impressions. Conversion Rate (CVR) = Conversions / Clicks. Cost Per Mille (CPM) = (Cost / Impressions) × 1000. These are the fundamental PPC metrics.",
        "Break-even ROAS = 1 / Profit Margin. If your profit margin is 25%, break-even ROAS = 400% (you need $4 revenue per $1 ad spend). Target ROAS should exceed break-even ROAS. For a 40% margin business, break-even ROAS is 250%, so targeting 350-400% provides healthy profit.",
        "Impression Share = Impressions Received / Total Eligible Impressions. Lost Impression Share (Budget) = impressions lost because daily budget was exhausted. Lost Impression Share (Rank) = impressions lost because Ad Rank was too low (bid or Quality Score). If Budget Lost IS > 10%, consider increasing budget or narrowing targeting.",
        "Customer Lifetime Value (CLV) should inform your CPA targets. If CLV is $500 and you want 3x return, your max CPA is $167. Most advertisers set CPA targets based only on the first transaction, leaving money on the table. Calculate CLV = (Average Order Value × Purchase Frequency × Customer Lifespan) and set CPA accordingly.",
        "Click-weighted average CPC = Total Cost / Total Clicks. However, different keywords have vastly different CPCs within the same campaign. Segmenting by match type typically shows: Exact < Phrase < Broad in CPC but Exact > Phrase > Broad in conversion rate. The most efficient strategy balances reach and precision.",

        # === Audiences ===
        "Remarketing lists let you re-engage users who previously visited your website. Segment by recency (1-7 days, 8-30 days, 31-90 days) and behavior (viewed product, added to cart, visited pricing page). Cart abandoner audiences typically have 3-5x higher conversion rates than cold traffic. Minimum list size is 1,000 users for Search and 100 for Display.",
        "Customer Match in Google Ads lets you upload customer email lists for targeting. Match rates typically range from 30-60%. Use Customer Match for upselling, cross-selling, and exclusion (exclude existing customers from acquisition campaigns). Combined with Similar Audiences, it extends reach to lookalike prospects.",
        "In-Market audiences target users actively researching or comparing products in specific categories. Google identifies these users through search behavior and content consumption patterns. In-Market audiences are available for both Search and Display campaigns. They work well as observation audiences to gather data before targeting.",

        # === Ad Copy and Creative ===
        "Responsive Search Ads (RSAs) allow up to 15 headlines (30 chars each) and 4 descriptions (90 chars each). Google's AI tests combinations and learns which perform best. Best practices: include keywords in 3+ headlines, add unique value propositions, use numbers and CTAs, and pin critical messages to ensure they always show.",
        "Ad copy best practices: lead with the benefit not the feature, include a clear call to action, use the target keyword in headline 1, differentiate from competitors, include social proof (ratings, awards, numbers), and create urgency without being misleading. Test 2-3 RSA variants per ad group.",

        # === Landing Pages ===
        "Landing page experience is a Quality Score component. Key factors: relevance to ad and keyword, page load speed (under 3 seconds), mobile responsiveness, clear above-the-fold value proposition, prominent CTA, trust signals (testimonials, security badges, logos), and minimal distracting navigation.",
        "Landing page conversion rate optimization: test one element at a time, start with the headline and CTA, remove navigation links that leak traffic, match the landing page message to the ad copy, use form field reduction (every field removed increases completion rates ~10%), and implement exit-intent offers for abandoning visitors.",

        # === Account Optimization ===
        "The 80/20 rule applies to Google Ads: approximately 80% of conversions come from 20% of keywords. Identify your top-performing keywords and ensure they have maximum impression share. Simultaneously, the bottom 20% of keywords by performance often waste significant budget — pause or reduce bids on these.",
        "Search Terms Report review should happen weekly. Look for: irrelevant queries consuming budget (add as negatives), high-converting queries not yet added as keywords (add them), close variants triggering unexpected matches (tighten match types or add negatives), and new market trends appearing in user searches.",
        "Account optimization cadence: daily — check budget pacing and anomalies. Weekly — review search terms, adjust bids, check Quality Score changes. Monthly — full performance review, add/pause keywords, refresh ad copy. Quarterly — strategy review, budget reallocation, landing page testing, competitive analysis.",

        # === Cross-Platform Strategy ===
        "Cross-platform advertising strategy should follow the customer journey. Google Search captures bottom-funnel demand (users actively searching). Meta and TikTok create top-funnel awareness (users discovering). LinkedIn targets B2B decision-makers. YouTube builds mid-funnel consideration. Retarget across all platforms for maximum conversion.",
        "Budget allocation across platforms depends on business model. B2B services: 50% Google Search, 20% LinkedIn, 15% Meta, 15% Display/YouTube. D2C ecommerce: 40% Google (Search + Shopping), 35% Meta/Instagram, 15% TikTok, 10% other. Lead gen: 60% Google Search, 25% Meta, 15% Microsoft. Adjust based on actual CPL/ROAS data.",
        "When comparing metrics across platforms, normalize terminology. Google's CPA is Meta's Cost Per Result. Google's ROAS is Amazon's inverse ACOS (ROAS = 1/ACOS × 100). Google's Search Impression Share has no direct Meta equivalent. Create a unified reporting framework mapping each platform's metrics to standard KPIs.",

        # === Programmatic / DSP ===
        "Demand-Side Platforms (DSPs) like The TradeDesk, DV360, and Amazon DSP enable programmatic buying across display, video, native, audio, and CTV inventory. Real-Time Bidding (RTB) auctions happen in milliseconds. Programmatic excels at scale and audience precision but requires larger budgets ($5K+ monthly) to optimize effectively.",

        # === LinkedIn Ads ===
        "LinkedIn Ads are premium-priced (CPCs of $5-15+) but reach professional audiences with unmatched B2B targeting. Target by job title, company, industry, seniority, skills, and groups. Lead Gen Forms pre-populate with LinkedIn profile data, achieving 2-5x higher conversion rates than website landing pages for B2B lead gen.",

        # === Reddit Ads ===
        "Reddit Ads target communities (subreddits) with shared interests. Successful Reddit ads use authentic language — overly polished corporate messaging gets downvoted. Promoted posts appear in feeds. Interest targeting and conversation placement extend reach beyond specific subreddits. CPCs are typically low ($0.50-3) but engagement quality varies.",

        # === TikTok Ads ===
        "TikTok Ads use a campaign-ad group-ad hierarchy. The platform excels at reaching Gen Z and Millennials with short-form video. Spark Ads boost existing organic content as paid ads. TikTok Shop integrates ecommerce directly into the platform. Smart Performance Campaigns are TikTok's equivalent of PMax — fully automated.",

        # === Seasonality and Trends ===
        "CPCs in Google Ads fluctuate seasonally. Q4 (October-December) has the highest CPCs due to holiday advertising demand. January often sees lower CPCs as advertisers pull back. Industry-specific peaks matter too: tax software in February-April, travel in January and June, back-to-school in July-August. Plan budgets around these patterns.",
        "Auction Insights report shows how you compare to competitors in the same auctions. Key metrics: impression share (your share vs competitors), overlap rate (how often you appear in the same auctions), outranking share (how often your ad ranked higher), position above rate, and top of page rate. Monitor monthly for competitive trends.",

        # === API and Automation ===
        "The Google Ads API (v23) enables programmatic campaign management. Common automation tasks: bid adjustments based on weather or inventory data, automated search terms report processing, scheduled reporting, budget pacing alerts, Quality Score monitoring, and ad copy testing workflows. Rate limits: 15,000 requests per day per developer token.",
        "Google Ads Scripts use JavaScript to automate account tasks without API setup. Common scripts: automatic bid adjustments, broken URL detection, Quality Score tracking, search term mining for negatives, performance anomaly alerts, and automated reporting. Scripts run on a schedule and have a 30-minute execution time limit.",

        # === B2B Specific ===
        "B2B Google Ads strategy differs from B2C: longer sales cycles (30-180 days), multiple decision makers, higher CPAs but higher deal values. Use offline conversion tracking to feed closed-deal data back to Smart Bidding. Target by audience (in-market B2B segments) + keyword for precision. Bid higher during business hours when decision-makers are active.",
        "Lead quality scoring is essential for B2B PPC. Not all leads are equal — track cost per SQL (sales qualified lead), not just cost per lead. Feed lead quality data back via offline conversion imports with value-based bidding. This teaches Smart Bidding to optimize for revenue, not just form fills.",

        # === Ecommerce Specific ===
        "Ecommerce Google Ads strategy centers on Shopping + Performance Max. Optimize your Merchant Center feed: titles should include brand + product type + key attribute + color/size. Use Supplemental feeds for quick changes. Custom labels allow campaign segmentation by margin, price tier, bestseller status, or seasonality.",
        "ROAS calculation for ecommerce: Revenue / Ad Spend × 100. A ROAS of 500% means $5 revenue per $1 spend. But ROAS alone is insufficient — consider profit margin. $100 revenue at 500% ROAS with 20% margin = $20 profit - $20 ad spend = breakeven. Factor in margins, shipping costs, and returns for true profitability.",
    ]

    texts.extend(PLATFORM_PRETRAIN_TEXTS)

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(150):
            for text in texts:
                f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")

    print(f"✅ Pretrain: {path} ({len(texts)} unique texts × 150 = {len(texts) * 150} samples)")


def create_sft_data():
    """Generate advertising SFT instruction-response pairs — 60+ platforms."""
    path = "./dataset/sft_ads.jsonl"
    os.makedirs("./dataset", exist_ok=True)

    from scripts.platform_training_data import PLATFORM_SFT_PAIRS

    pairs = [
        # === PPC Math ===
        {"user": "What is CPA and how do I calculate it?",
         "assistant": "CPA (Cost Per Acquisition) = Total Ad Spend / Total Conversions. If you spent $5,000 and got 100 conversions, your CPA is $50. For target CPA, work backwards from your unit economics: if your product profit margin is $200, a CPA under $200 is profitable. Most B2B SaaS targets CPA at 10-20% of first-year Annual Contract Value."},

        {"user": "How do I calculate ROAS and what's a good target?",
         "assistant": "ROAS (Return On Ad Spend) = Revenue from Ads / Ad Spend. If you spent $1,000 and generated $4,000 in revenue, your ROAS is 4x or 400%. Break-even ROAS = 1 / Profit Margin. For a 25% margin business, break-even is 400%. Your target should exceed break-even: aim for 500-600% to generate actual profit. For a 50% margin business, break-even is 200% so 300%+ is profitable."},

        {"user": "My CTR is 1.2%. Is that good or bad?",
         "assistant": "It depends on campaign type and industry. For Google Search ads, average CTR is 3-5% — so 1.2% is below average and signals your ads aren't resonating. Check: are your keywords too broad? Is your ad copy relevant to search intent? For Display ads, 0.5-1% is normal so 1.2% would be excellent. For Shopping, 1-2% is typical. Fix low Search CTR by improving headline relevance, adding keyword insertion, testing stronger CTAs, and tightening match types."},

        {"user": "Calculate impression share from these numbers: 50,000 impressions received, estimated 125,000 eligible impressions.",
         "assistant": "Search Impression Share = Impressions / Eligible Impressions = 50,000 / 125,000 = 40%. You're missing 60% of eligible auctions. Check the breakdown: if Budget Lost IS is 35%, your daily budget runs out early — increase budget or reduce bids on low-performers. If Rank Lost IS is 25%, your Ad Rank is too low — improve Quality Score or increase bids on high-value keywords."},

        # === GAQL Queries ===
        {"user": "Write a GAQL query to find my top 10 campaigns by spend last 30 days.",
         "assistant": "SELECT campaign.name, campaign.status, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.conversions_value, metrics.search_impression_share FROM campaign WHERE segments.date DURING LAST_30_DAYS AND campaign.status != 'REMOVED' ORDER BY metrics.cost_micros DESC LIMIT 10. Remember: cost_micros is in millionths — divide by 1,000,000 for actual currency. So cost_micros = 45000000 means $45.00."},

        {"user": "Write a GAQL query to find wasted spend — search terms with spend but zero conversions.",
         "assistant": "SELECT search_term_view.search_term, search_term_view.status, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0 AND metrics.conversions = 0 ORDER BY metrics.cost_micros DESC LIMIT 50. This shows your biggest money-wasters. Add irrelevant terms as negative keywords. In unoptimized accounts, 20-40% of spend typically goes to irrelevant search terms."},

        {"user": "Write a GAQL query to check Quality Score for all active keywords.",
         "assistant": "SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.quality_info.post_click_quality_score, metrics.impressions, metrics.cost_micros FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED' AND campaign.status = 'ENABLED' ORDER BY ad_group_criterion.quality_info.quality_score ASC."},

        {"user": "Write a GAQL query for Auction Insights to see my competitors.",
         "assistant": "SELECT auction_insights.display_url, auction_insights.search_impression_share, auction_insights.search_overlap_rate, auction_insights.search_outranking_share, auction_insights.search_top_impression_percentage FROM auction_insights WHERE segments.date DURING LAST_30_DAYS. This shows who you're competing against and how often they outrank you. If a new competitor suddenly appears with high impression share, they may be driving up your CPCs."},

        {"user": "Write a GAQL query to find ad groups with high spend but low conversion rate.",
         "assistant": "SELECT ad_group.name, campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.impressions FROM ad_group WHERE segments.date DURING LAST_30_DAYS AND metrics.clicks > 50 AND metrics.conversions < 2 ORDER BY metrics.cost_micros DESC LIMIT 20. Ad groups with 50+ clicks and fewer than 2 conversions have under 4% CVR. Review their keywords, ad copy, and landing pages. Consider pausing the worst performers."},

        # === Diagnostic Questions ===
        {"user": "My CPA is $85 and my target is $50. What should I do?",
         "assistant": "CPA is 70% above target — here's the systematic fix: 1) Search Terms Report: find irrelevant queries eating budget, add as negatives. This alone often cuts CPA 15-30%. 2) Keyword performance: pause keywords with CPA over $100 that haven't improved in 30 days. 3) Landing page: check conversion rate — if under 3%, the page is the bottleneck. Test headline, form length, CTA. 4) Ad copy: ensure message match between keyword intent, ad text, and landing page. 5) Bid strategy: if using Target CPA, set it to $60 (not $50) and reduce gradually. Too aggressive a target throttles volume."},

        {"user": "My impression share dropped from 75% to 40% in one week. What happened?",
         "assistant": "A 35-point drop in one week is dramatic. Three possible causes in order of likelihood: 1) Budget constraint — check search_budget_lost_impression_share in GAQL. If your daily budget ran out by 2pm, you lost the rest of the day's auctions. Fix: increase budget or reduce bids/keywords. 2) Quality Score drop — check search_rank_lost_impression_share. Look for disapproved ads, landing page issues, or keyword QS changes. 3) New competitor — check Auction Insights for a new entrant with aggressive bids. For a sudden drop, budget exhaustion is the most common cause."},

        {"user": "My Google Ads account spends $10K/month but generates only 15 conversions. What's wrong?",
         "assistant": "At $10K spend and 15 conversions, your CPA is $667 — almost certainly too high unless you're selling high-ticket items. Systematic diagnosis: 1) Check conversion tracking first — are conversions actually being recorded? Test by completing a conversion yourself. 2) Run the Search Terms Report — at this spend level with few conversions, irrelevant traffic is likely consuming most budget. 3) Check landing page analytics separately — if you're getting clicks but no conversions, the page is the problem. 4) Look at keyword match types — broad match without Smart Bidding at this scale bleeds budget. 5) Verify targeting — check geographic, device, and audience settings for anything too broad."},

        {"user": "Should I use broad match or exact match keywords?",
         "assistant": "Both, strategically. Start with exact match for your highest-intent, proven keywords — this gives maximum control and typically highest conversion rates. After collecting 2 weeks of data, expand top performers to phrase match to capture more variations. Only use broad match when: you have Smart Bidding enabled (Target CPA or ROAS), you have robust negative keyword lists, and you have sufficient conversion volume (30+ per month). Broad match without these guardrails wastes budget on irrelevant queries. The progression is: Exact (control) → Phrase (expand) → Broad with Smart Bidding (scale)."},

        # === Campaign Structure ===
        {"user": "How should I structure Google Ads campaigns for a B2B SaaS company?",
         "assistant": "Recommended structure: Campaign 1 — Brand (10% budget): exact match brand terms, highest ROAS. Campaign 2 — High-Intent Non-Brand (40%): keywords like 'buy [product category]', '[competitor] alternative', '[solution] software'. Campaign 3 — Mid-Funnel (25%): problem-aware keywords like 'how to [solve problem]', '[pain point] solution'. Campaign 4 — Competitor (15%): competitor brand name targeting with comparison messaging. Campaign 5 — Remarketing (10%): Display/YouTube retargeting visitors who didn't convert. Start with Campaigns 1-2, prove ROI, then expand. Use offline conversion tracking to feed closed-deal data back for Smart Bidding optimization."},

        {"user": "How should I structure campaigns for an ecommerce store with 500 products?",
         "assistant": "Use a tiered structure based on product value: Campaign 1 — Brand Search (10-15% budget): exact match brand terms, protect your brand. Campaign 2 — Top Products via Performance Max (40-50%): your top 50 products by profit margin × sales volume. Use custom labels in Merchant Center to segment. Campaign 3 — Standard Shopping by Category (25-30%): organize by product category with priority settings for query funneling. Campaign 4 — Non-Brand Search (10-15%): high-intent category terms like 'buy [product type] online'. Campaign 5 — Remarketing (5-10%): cart abandoners and product page viewers. Start with Campaigns 1-2 and prove ROI before expanding."},

        # === Platform Comparisons ===
        {"user": "Compare Google Ads and Meta Ads for lead generation.",
         "assistant": "Google Ads Search: intent-based (users actively searching), higher CPC ($2-15), higher conversion rate (3-8%), best for bottom-funnel high-intent leads. Typical CPL: $30-100 B2B, $15-50 B2C. Meta Ads: interruption-based (users browsing social media), lower CPC ($0.50-3), lower conversion rate (1-3%), best for top-funnel awareness and visual products. Typical CPL: $15-60 B2B, $5-25 B2C. Use both: Google captures existing demand, Meta creates new demand. Start with 70/30 Google/Meta split and adjust based on 30 days of CPL data. Meta is better for retargeting warm audiences, Google is better for capturing purchase intent."},

        {"user": "When should I use Microsoft Ads vs Google Ads?",
         "assistant": "Use both. Microsoft Ads (Bing) reaches 36% of US desktop search. Key advantages: CPCs are 30-50% lower than Google, audience skews older and higher-income (good for B2B, financial services, luxury), and LinkedIn profile targeting enables B2B precision no other platform offers. Import your Google campaigns directly for a quick start. Allocate 10-20% of your Google Search budget to Microsoft. The lower competition often delivers better ROAS on the same keywords."},

        {"user": "Is Amazon Ads worth it for my products?",
         "assistant": "If you sell on Amazon, yes — Amazon Ads directly drives sales on the platform where purchase intent is highest. Start with Sponsored Products using automatic targeting to discover what converts. After 2 weeks, mine the Search Term Report and create manual campaigns with proven keywords. ACOS (Advertising Cost of Sales) = Ad Spend / Ad Revenue. Target ACOS should be below your profit margin. If your margin is 30%, keep ACOS under 25% to stay profitable. Sponsored Brands build brand awareness at the top of search results. Sponsored Display retargets shoppers who viewed your products."},

        # === Common Tasks ===
        {"user": "What negative keywords should I add to a B2B SaaS campaign?",
         "assistant": "Start with these universal B2B negatives: free, cheap, open source, download, tutorial, course, certification, salary, jobs, career, intern, reddit, youtube, how to, what is, DIY. Then add industry-specific negatives: for SaaS add self-hosted and on-premise (if cloud-only), for enterprise add small business and personal, for paid tools add free trial (unless you offer one). Review Search Terms Report weekly and add new negatives. Build a shared negative keyword list at account level to apply across all campaigns. Typically 200-500 negatives are needed for a well-optimized B2B account."},

        {"user": "How do I find and fix wasted ad spend?",
         "assistant": "Five areas to check: 1) Search Terms Report — filter for cost > $0 and conversions = 0, sorted by cost descending. Add irrelevant terms as negatives. 2) Geographic performance — check if certain locations consume budget without converting. Exclude or reduce bids for underperformers. 3) Device performance — mobile vs desktop conversion rates differ dramatically by industry. Adjust device bid modifiers. 4) Time-of-day — run a day-of-week and hour-of-day report. B2B often wastes money on weekends and nights. Use ad scheduling. 5) Low Quality Score keywords — keywords with QS 3 or below pay significantly more per click. Fix ad relevance or pause them."},

        {"user": "How do I set up conversion tracking in Google Ads?",
         "assistant": "Two methods: Option 1 — Google Tag Manager (recommended): create a conversion action in Google Ads, copy the conversion ID and label, create a Google Ads Conversion Tracking tag in GTM triggered on your thank-you page or form submission event. Option 2 — Global site tag: add the gtag.js snippet to every page, then add the event snippet on the conversion page. For both methods: set the conversion counting (one per click for leads, every for purchases), assign a value, and choose the right attribution model (data-driven recommended). Test with Google Tag Assistant. Then in Google Ads, mark this as a primary conversion so Smart Bidding uses it."},

        {"user": "How do I audit a Google Ads account?",
         "assistant": "7-dimension audit: 1) Conversion tracking — verify it works, check for duplicate counting, review attribution model. 2) Account structure — campaigns organized by theme, 15-20 keywords per ad group max, correct match types. 3) Keywords — review search terms for waste, check Quality Scores, identify gaps. 4) Ad copy — at least 2 RSAs per ad group, all ad strength 'Good' or better, extensions in use. 5) Bidding — appropriate strategy for conversion volume, targets realistic, learning period respected. 6) Budget — no campaigns limited by budget unintentionally, spend aligned with priority. 7) Landing pages — relevant, fast, mobile-friendly, conversion-optimized. Score each dimension 1-10 and prioritize fixes by impact."},

        # === Performance Max ===
        {"user": "Should I use Performance Max campaigns?",
         "assistant": "PMax works well when you have: 1) strong conversion data (50+ conversions/month), 2) quality creative assets across text, images, and video, 3) properly configured conversion tracking, 4) defined audience signals. Start PMax alongside existing Search campaigns, don't replace them. Watch for brand traffic cannibalization — use brand exclusions. PMax reporting is limited, so use the Insights tab. Don't launch PMax with a new account that has no conversion history — Smart Bidding needs data to optimize. For ecommerce, PMax with a product feed is especially powerful."},

        # === Bid Strategy ===
        {"user": "When should I switch from manual CPC to Smart Bidding?",
         "assistant": "Switch to Smart Bidding when you have: 1) at least 30 conversions in 30 days (50+ is ideal), 2) reliable conversion tracking with accurate values, 3) consistent campaign performance for the algorithm to learn from. Start with Maximize Conversions (no target) for 2 weeks, then add a Target CPA set at or above your historical CPA. Reduce the target gradually in 10-15% increments, waiting 2 weeks between changes. If using Target ROAS, you need at least 15 conversions in 30 days. Never change bid strategy during a promotional period or unusual traffic spike."},

        # === Budget ===
        {"user": "How much should I spend on Google Ads to start?",
         "assistant": "Work backwards from your target: if your target CPA is $50 and you want 30 leads per month, you need $1,500/month budget. But for testing, you need enough data to optimize — minimum $30-50/day per campaign, which means $900-1,500/month per campaign. With 2 campaigns (brand + non-brand), budget $2,000-3,000/month for a meaningful test. Run for at least 60 days before judging results — the first 30 days are learning. Never set a budget you can't sustain for 3 months. Too-small budgets spread across too many campaigns is the most common mistake."},

        # === Quality Score ===
        {"user": "How do I improve Quality Score from 4 to 7+?",
         "assistant": "Quality Score has three components — fix the weakest one first: 1) Expected CTR (Below Average → Average): improve ad headlines to be more specific and compelling, add keyword in headline 1, use ad customizers, test emotional triggers. 2) Ad Relevance (Below Average → Average): ensure your ad copy directly addresses the keyword intent, use keyword insertion where appropriate, create tighter ad groups with fewer, more related keywords. 3) Landing Page Experience (Below Average → Average): improve page load speed to under 3 seconds, ensure mobile responsiveness, match landing page content to the keyword/ad message, add relevant content above the fold, remove pop-ups. Expect 2-4 weeks for QS changes to take effect after improvements."},

        # === Reporting ===
        {"user": "What should a monthly Google Ads performance report include?",
         "assistant": "Essential sections: 1) Executive summary — spend, conversions, CPA, ROAS vs targets, month-over-month trend. 2) Campaign performance table — each campaign's spend, impressions, clicks, CTR, conversions, CPA, ROAS. 3) Top/bottom performers — best and worst keywords, ad groups, search terms. 4) Impression share analysis — total IS, budget lost IS, rank lost IS, competitive trends. 5) Quality Score distribution — how many keywords at each QS level, changes from prior month. 6) Audience insights — device, geography, demographics if available. 7) Recommendations — specific actions for next month with expected impact. 8) Budget recommendation — should budget increase, decrease, or shift between campaigns."},

        # === Ad Extensions ===
        {"user": "What ad extensions should I always use?",
         "assistant": "Always enable these: 1) Sitelink extensions — add 4-8 links to key pages (pricing, features, case studies, demo). 2) Callout extensions — 4+ highlights like 'Free Trial', '24/7 Support', 'No Setup Fee'. 3) Structured snippets — categorized lists like 'Services: PPC, SEO, Social, Analytics'. 4) Call extensions — if you take phone calls, add your number. 5) Image extensions — product or brand images to increase visual appeal. 6) Lead form extensions — capture leads directly from the ad (especially for mobile). Extensions improve CTR by 10-15% on average and they're free — there's no additional cost per click on extensions."},

        # === Remarketing ===
        {"user": "How do I set up effective remarketing campaigns?",
         "assistant": "Segment your audiences by intent level: Tier 1 (highest intent) — cart abandoners, pricing page visitors, free trial signups who didn't convert. Show them specific offer ads. Tier 2 (medium intent) — product/service page visitors, 2+ page visits. Show them testimonials and social proof. Tier 3 (low intent) — all site visitors excluding converters. Show them brand awareness content. Set frequency caps (3-5 impressions per user per day) to avoid ad fatigue. Exclude converters from all remarketing. Use 30-day membership for Tier 1, 90 days for Tier 2-3. Create separate campaigns for each tier with appropriate bids — Tier 1 deserves highest bids."},

        # === Meta Specific ===
        {"user": "How do I set up Meta Ads conversion tracking?",
         "assistant": "Three components: 1) Meta Pixel — install the base pixel code on all pages via your website header or Google Tag Manager. 2) Standard events — add event code for key actions: PageView (all pages), ViewContent (product pages), AddToCart, InitiateCheckout, Purchase (with value), Lead (form submissions). 3) Conversions API (CAPI) — set up server-side event tracking to supplement the Pixel. This is critical post-iOS 14.5 for accurate tracking. Use Meta's Event Manager to verify events are firing. Configure Aggregated Event Measurement by ranking your 8 priority events per domain. Purchase and Lead should be highest priority."},

        {"user": "What's the best Meta Ads audience strategy?",
         "assistant": "Layer audiences in a funnel: Prospecting — use Advantage+ Audience (broad) or Interest-based targeting for new user acquisition. Let Meta's algorithm find converters. Engagement — retarget video viewers (50%+ watched), page engagers, and Instagram interactions. Website retargeting — Pixel-based custom audiences: all visitors (180 days), product viewers (30 days), cart abandoners (14 days). Customer audiences — upload email lists for lookalike creation (1-3% is best for quality). Use exclusions at each level: exclude website visitors from prospecting, exclude purchasers from retargeting."},

        # === Seasonal Strategy ===
        {"user": "How should I adjust Google Ads for Black Friday / holiday season?",
         "assistant": "Start planning 6-8 weeks before: 1) Increase budgets 50-200% based on historical holiday demand. CPCs will rise 20-50% in Q4. 2) Create holiday-specific ad copy with urgency (limited time, ends Sunday, X% off). 3) Build remarketing lists NOW — anyone who visits in October is a warm prospect for November. 4) Launch holiday Shopping campaigns and PMax asset groups with holiday creative. 5) Set up countdown customizers in RSAs for sale end dates. 6) Adjust bid strategy targets — accept higher CPA during peak if CLV justifies it. 7) Pre-schedule ad copy changes for key dates. 8) Monitor hourly during peak days and be ready to increase budgets if campaigns max out."},

        # === Advanced ===
        {"user": "How do I use Google Ads scripts for automation?",
         "assistant": "Google Ads Scripts use JavaScript to automate tasks. Top scripts to implement: 1) Broken URL checker — scans all ad URLs and pauses ads pointing to 404 pages. 2) Quality Score tracker — records daily QS for all keywords in a Google Sheet for trend analysis. 3) Budget pacer — alerts when campaigns are on track to overspend or underspend. 4) Search term miner — automatically adds high-converting search terms as keywords and flags irrelevant terms. 5) Anomaly detector — alerts when metrics deviate significantly from historical norms. Scripts run on schedules (hourly to monthly). Start with the free scripts at developers.google.com/google-ads/scripts or from community repositories."},

        {"user": "Explain the Google Ads API and when to use it vs the UI.",
         "assistant": "The Google Ads API (currently v23) enables programmatic account management. Use the API when: managing 10+ accounts at scale, building custom reporting dashboards, implementing automated bid management, integrating with CRM or inventory systems, or building tools for clients. The API uses GAQL for data retrieval and mutate operations for changes. Authentication requires a developer token, OAuth 2.0 client credentials, and customer ID. Rate limits: 15,000 operations per day for basic access. Python client library: google-ads >= 25.1.0. For single-account management, the Google Ads UI is faster. For anything repetitive across multiple accounts, the API saves enormous time."},

        # === Cross-Platform ===
        {"user": "How do I report performance across Google, Meta, and Microsoft in one view?",
         "assistant": "Create a unified reporting framework: 1) Normalize metrics — Google's CPA = Meta's Cost Per Result = Microsoft's CPA. Google's ROAS = Meta's Purchase ROAS. Map each platform's terms to your standard KPIs. 2) Use a common date range and attribution window. 3) Build a dashboard (Looker Studio, Tableau, or Google Sheets) pulling from each platform's API. Key columns: Platform, Campaign, Spend, Impressions, Clicks, Conversions, CPA, ROAS. 4) Include a blended row showing total across all platforms. 5) Watch for double-counting — a user who clicks Google then Meta before converting might be counted by both platforms. Use UTM parameters and your analytics platform as the source of truth for deduplication."},

        # === Specific Scenarios ===
        {"user": "My client wants to launch in a new market with no historical data. What's the strategy?",
         "assistant": "New market launch strategy: Phase 1 (weeks 1-2, data gathering): start with Maximize Clicks bidding, broad research keywords, and geo-targeting the new market. Budget enough for 100+ clicks per day to gather data fast. Phase 2 (weeks 3-4, refinement): analyze search terms, add negatives, identify converting keywords, switch to phrase/exact match for winners. Phase 3 (weeks 5-8, optimization): once you have 30+ conversions, switch to Maximize Conversions. Begin adding Target CPA after 50+ conversions. Throughout: set up proper conversion tracking before launching, use ad scheduling to match local business hours, and run competitor research via Auction Insights. Expect higher CPA in the first 60 days."},

        {"user": "What is cost_micros in the Google Ads API?",
         "assistant": "cost_micros is Google Ads API's currency format where values are expressed in millionths of the account's currency unit. Divide by 1,000,000 to get the actual amount. Examples: cost_micros = 45000000 means $45.00. cost_micros = 1500000 means $1.50. cost_micros = 100000000 means $100.00. This applies to cost_micros, average_cpc, average_cpm, and all other monetary fields in GAQL responses. When building reports, always divide by 1e6 and format as currency."},
    ]

    pairs.extend(PLATFORM_SFT_PAIRS)

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(80):
            for pair in pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"✅ SFT: {path} ({len(pairs)} unique pairs × 100 = {len(pairs) * 100} samples)")


def create_dpo_data():
    """Generate DPO preference pairs — good vs bad advertising advice."""
    path = "./dataset/dpo_ads.jsonl"
    os.makedirs("./dataset", exist_ok=True)

    from scripts.platform_training_data import PLATFORM_DPO_PAIRS

    pairs = [
        {"prompt": "How should I set up keyword match types?",
         "chosen": "Start with exact match for your highest-intent keywords to control spend and gather clean data. After 2 weeks of performance data, expand top performers to phrase match. Only use broad match with Smart Bidding enabled (Target CPA or ROAS) and robust negative keyword lists. This progression — exact to phrase to broad — ensures you scale spend on proven keywords.",
         "rejected": "Use broad match on everything to maximize traffic volume. More impressions means more clicks means more conversions. Google's AI will figure out what's relevant."},

        {"prompt": "My CPA is too high. What should I do?",
         "chosen": "Diagnose systematically: 1) Check Search Terms Report for irrelevant queries consuming budget — add negatives. 2) Pause keywords with CPA more than 2x your target that haven't improved in 30 days. 3) Audit landing page conversion rate — even small improvements compound. 4) Ensure ad copy matches keyword intent. 5) If using manual CPC, consider switching to Target CPA bidding. Work on the highest-waste areas first.",
         "rejected": "Just increase your budget. More spend means the algorithm has more data to optimize. Google's AI will figure it out eventually if you give it enough money."},

        {"prompt": "Should I run Performance Max campaigns?",
         "chosen": "PMax works best when you have: at least 50 conversions per month, quality creative assets (text, images, video), properly configured conversion tracking, and defined audience signals. Start alongside existing Search campaigns, don't replace them. Use brand exclusions to prevent PMax from cannibalizing your brand traffic. Monitor Search impression share before and after launch.",
         "rejected": "Switch everything to Performance Max immediately. Google recommends it for all advertisers and their AI is always better than manual campaign management. Delete your Search campaigns."},

        {"prompt": "How much should I spend on Google Ads?",
         "chosen": "Work backwards from your goals: if target CPA is $50 and you want 100 leads/month, you need $5,000/month budget. Start at 60-70% of that to test, then scale what works. Each campaign needs minimum $30-50/day to gather meaningful data. Never set a budget you can't sustain for 3 months — Smart Bidding needs consistent data to optimize.",
         "rejected": "Start with $10/day and see what happens. You can always increase later if it works. Keep the budget as low as possible to minimize risk."},

        {"prompt": "Should I target competitor brand names?",
         "chosen": "Competitor targeting can work but requires the right approach: write ads that compare/differentiate rather than mislead, create a dedicated campaign with separate budget, expect higher CPCs and lower Quality Scores (you won't match competitor's relevance), use specific landing pages addressing why you're better. Don't use competitor trademarks in ad text — that violates policies. Monitor ROAS carefully since these campaigns often have lower conversion rates.",
         "rejected": "Always target every competitor name possible and use their brand names in your ad headlines to steal their traffic. This is the fastest way to grow."},

        {"prompt": "How should I handle a sudden spike in CPC?",
         "chosen": "Investigate before reacting: 1) Check Auction Insights for new competitors entering the market. 2) Review Quality Scores for any drops. 3) Look at your Search Impression Share — if budget lost IS increased, your budget may be too low for increased competition. 4) Check if seasonality or industry events are driving more auction demand. If CPCs rose but CVR and CPA stayed stable, the increase might be acceptable. Only reduce bids if efficiency metrics actually worsened.",
         "rejected": "Immediately double your bids to maintain position. You can't afford to lose impression share. Outbid the competition at any cost."},

        {"prompt": "What should I do with keywords that have a Quality Score of 3?",
         "chosen": "QS 3 keywords pay a significant premium per click. Diagnose each component: if Expected CTR is Below Average, improve ad headlines and test more compelling CTAs. If Ad Relevance is Below Average, create a tighter ad group with better keyword-ad alignment. If Landing Page Experience is Below Average, improve page speed, relevance, and mobile experience. Give changes 2-4 weeks to affect QS. If QS doesn't improve after optimization, pause the keyword and find alternative terms.",
         "rejected": "Delete all keywords with Quality Score below 5 immediately. They're dragging down your account performance and there's no way to fix them."},

        {"prompt": "My client wants results in the first week. What do I tell them?",
         "chosen": "Set realistic expectations: Week 1 is data collection, not optimization. Smart Bidding needs 7-14 days for its learning period. Expect higher CPA initially as the algorithm learns. Share a timeline: weeks 1-2 for learning, weeks 3-4 for initial optimization, weeks 5-8 for meaningful results. Show early directional data (search terms, impression share) to demonstrate progress while conversion data accumulates.",
         "rejected": "Promise immediate results to keep the client happy. Set extremely aggressive CPA targets from day one and run broad match keywords to get volume fast."},
    ]

    pairs.extend(PLATFORM_DPO_PAIRS)

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(50):
            for pair in pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"✅ DPO: {path} ({len(pairs)} unique pairs × 50 = {len(pairs) * 50} samples)")


def main():
    parser = argparse.ArgumentParser(description="MiniAgent Data & Tokenizer Setup")
    parser.add_argument("--all", action="store_true", help="Download tokenizer + generate all data")
    parser.add_argument("--tokenizer", action="store_true", help="Download minimind tokenizer")
    parser.add_argument("--base-model", action="store_true", help="Download minimind base model for transfer learning")
    parser.add_argument("--pretrain", action="store_true", help="Generate pretrain corpus")
    parser.add_argument("--sft", action="store_true", help="Generate SFT instruction pairs")
    parser.add_argument("--dpo", action="store_true", help="Generate DPO preference pairs")
    args = parser.parse_args()

    if args.all:
        args.tokenizer = args.pretrain = args.sft = args.dpo = True

    if args.tokenizer:
        download_tokenizer()
    if args.base_model:
        download_base_model()
    if args.pretrain:
        create_pretrain_data()
    if args.sft:
        create_sft_data()
    if args.dpo:
        create_dpo_data()

    if not any([args.all, args.tokenizer, args.base_model, args.pretrain, args.sft, args.dpo]):
        print("MiniAgent Data & Tokenizer Setup")
        print("=" * 50)
        print("Usage:")
        print("  python scripts/download_data.py --all          # tokenizer + all data")
        print("  python scripts/download_data.py --tokenizer    # minimind tokenizer only")
        print("  python scripts/download_data.py --base-model   # minimind base model (transfer learning)")
        print("  python scripts/download_data.py --pretrain     # pretrain corpus")
        print("  python scripts/download_data.py --sft          # SFT instruction pairs")
        print("  python scripts/download_data.py --dpo          # DPO preference pairs")


if __name__ == "__main__":
    main()

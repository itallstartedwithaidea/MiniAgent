"""
MiniAgent Platform Training Data — All 60+ Advertising Platforms

Covers: Search, Social, DSP, Retail/Commerce, Video/CTV, Mobile/App,
Native/Content, Tag/Analytics, Measurement, Affiliate platforms.
"""


PLATFORM_PRETRAIN_TEXTS = [
    # ═══════════════════════════════════════════════════════════
    # SEARCH PLATFORMS
    # ═══════════════════════════════════════════════════════════

    # Google Ads (v23)
    "Google Ads API v23 is the current version, accessed via the google-ads Python package (v25.1+). Authentication requires OAuth 2.0 credentials plus a developer token. The API supports campaign management, reporting via GAQL, keyword planning, and conversion tracking. Rate limit is 15,000 operations per day for basic access.",
    "Google Ads campaign types: Search, Display, Shopping, Video (YouTube), Performance Max, App, Demand Gen, and Local. Each campaign type has unique targeting, bidding, and creative requirements. Performance Max uses AI across all channels simultaneously.",
    "Google Ads Smart Bidding uses machine learning to optimize bids in real-time. Strategies include Target CPA, Target ROAS, Maximize Conversions, and Maximize Conversion Value. Smart Bidding requires at least 30 conversions in 30 days per campaign for effective optimization.",
    "Google Ads Quality Score is rated 1-10 per keyword with three components: Expected CTR, Ad Relevance, and Landing Page Experience. Higher Quality Score reduces CPC. Ad Rank = Max CPC Bid × Quality Score + expected impact of extensions.",
    "GAQL (Google Ads Query Language) uses SELECT-FROM-WHERE-ORDER BY-LIMIT syntax. Key resources: campaign, ad_group, ad_group_ad, keyword_view, search_term_view. Monetary values use cost_micros (divide by 1,000,000). Date filtering uses segments.date DURING LAST_30_DAYS or BETWEEN clauses.",

    # Google Ads Scripts
    "Google Ads Scripts use JavaScript to automate account tasks without API setup. Scripts run on a schedule with a 30-minute execution limit. Common scripts: bid adjustments, broken URL detection, Quality Score tracking, search term mining, budget pacing alerts, and automated reporting. No developer token required.",

    # Google Merchant Center
    "Google Merchant Center hosts product data feeds for Shopping and Performance Max campaigns. The Content API v2.1 enables programmatic feed management. Required fields: id, title, description, link, image_link, price, availability, brand, gtin or mpn, condition. Feed quality directly impacts Shopping ad performance.",
    "Merchant Center feed optimization: titles should include brand + product type + key attribute + color/size. Use Supplemental feeds for quick updates without modifying the primary feed. Custom labels (custom_label_0 through custom_label_4) enable campaign segmentation by margin, seasonality, or priority.",

    # Google Ad Manager
    "Google Ad Manager (GAM) is an ad serving platform for publishers managing direct-sold and programmatic inventory. It supports display, video, native, and audio ad formats. The API uses OAuth 2.0 for authentication. GAM integrates with AdSense, Ad Exchange, and third-party demand sources.",

    # Google Campaign Manager 360
    "Campaign Manager 360 (CM360) is Google's ad server and measurement platform for agencies and advertisers. It provides cross-channel campaign management, trafficking, verification, and reporting. Uses Floodlight tags for conversion tracking. The API enables automated campaign trafficking and reporting.",

    # Google Display & Video 360
    "Display & Video 360 (DV360) is Google's demand-side platform for programmatic media buying across display, video, audio, native, and connected TV. It integrates with Campaign Manager 360 for ad serving. Uses OAuth 2.0 authentication. Supports automated bidding, audience management, and creative optimization.",

    # Microsoft Advertising (Bing)
    "Microsoft Advertising (formerly Bing Ads) uses the bingads Python SDK with OAuth 2.0 authentication. It reaches 36% of US desktop search with 30-50% lower CPCs than Google. Key differentiator: LinkedIn profile targeting for B2B (job title, company, industry). Supports direct campaign import from Google Ads.",
    "Microsoft Advertising UET (Universal Event Tracking) tag tracks conversions and remarketing. The API supports campaign management, reporting, and bulk operations. Smart Bidding strategies mirror Google: Target CPA, Target ROAS, Enhanced CPC, Maximize Conversions.",

    # Apple Search Ads
    "Apple Search Ads places ads in App Store search results. Two tiers: Basic (automated, pay-per-install) and Advanced (keyword bidding, audience targeting). The API uses OAuth 2.0. Key metrics: tap-through rate (TTR), conversion rate (CR), cost per acquisition (CPA). Apple Search Ads Attribution API measures install attribution.",

    # Yahoo/Verizon DSP
    "Yahoo DSP (formerly Verizon Media DSP) provides programmatic buying across Yahoo properties and the open web. Supports display, native, video, and connected TV. Uses Deal ID-based buying and open auction. Access requires a managed account relationship.",

    # ═══════════════════════════════════════════════════════════
    # SOCIAL PLATFORMS
    # ═══════════════════════════════════════════════════════════

    # Meta (Facebook/Instagram)
    "Meta Ads uses the facebook-business Python SDK (v21.0+) with System User Token or User Token authentication. Campaign structure: Campaign > Ad Set > Ad. Campaign Budget Optimization (CBO) distributes budget across ad sets. Advantage+ campaigns automate targeting and placement.",
    "Meta Conversions API (CAPI) sends server-side events directly to Meta, complementing the Pixel for iOS 14.5+ tracking recovery. Standard events: PageView, ViewContent, AddToCart, InitiateCheckout, Purchase, Lead, CompleteRegistration. Requires System User Token authentication.",
    "Meta Ads Library API provides transparency data on ads running across Facebook and Instagram. Access requires an app with ads_read permission. Returns ad creative, spend ranges, impressions, and demographic targeting. Useful for competitive intelligence.",
    "Meta Pixel fires browser-side events for conversion tracking and audience building. Aggregated Event Measurement limits optimization to 8 events per domain. Custom Audiences from website visitors, customer lists, app activity, and video views. Lookalike Audiences range from 1% (most similar) to 10%.",

    # LinkedIn Marketing API
    "LinkedIn Marketing API uses OAuth 2.0 with granular permission scopes. Campaign structure: Campaign Group > Campaign > Creative. Unique targeting: job title, company name, industry, seniority, skills, company size, and LinkedIn Groups. Lead Gen Forms pre-populate with profile data for 2-5x higher conversion rates.",
    "LinkedIn Ads CPCs typically range $5-15+ due to premium B2B audience. Campaign objectives: Brand Awareness, Website Visits, Engagement, Video Views, Lead Generation, Website Conversions. Sponsored Content, Message Ads, Dynamic Ads, and Text Ads are the main formats.",

    # X/Twitter Ads API
    "X Ads API (formerly Twitter Ads) uses OAuth 1.0a + OAuth 2.0 dual authentication. Campaign structure mirrors standard hierarchy. Targeting includes keywords, interests, followers of specific accounts, tailored audiences (customer lists), and conversation topics. Promoted Tweets and Promoted Trends are key formats.",

    # TikTok Business API
    "TikTok Business API uses App ID + Secret authentication. Campaign structure: Campaign > Ad Group > Ad. The Business API rate limit is 10 requests per second. Spark Ads boost organic content as paid ads. Smart Performance Campaigns are TikTok's fully automated campaign type.",
    "TikTok Ads targeting includes interest categories, behavior targeting, custom audiences (website, app, customer file), and lookalike audiences. TikTok Shop integrates ecommerce directly. Creative best practices: vertical video, first 3 seconds hook, authentic creator-style content.",

    # Snapchat Marketing API
    "Snapchat Marketing API uses OAuth 2.0 authentication. Ad formats: Single Image/Video, Collection Ads, Story Ads, AR Lenses, Filters, and Commercials. Targeting includes demographics, interests, Snap Lifestyle Categories, Custom Audiences, and Lookalike Audiences. The Snap Pixel tracks website conversions.",

    # Pinterest Ads API
    "Pinterest Ads API uses OAuth 2.0. Campaign structure: Campaign > Ad Group > Ad (Pin). Ad formats: Standard Pins, Video Pins, Shopping Pins, Carousel Pins, Collections, and Idea Pins. Targeting includes interests, keywords, demographics, customer lists, actalikes (Pinterest's lookalikes), and retargeting.",
    "Pinterest conversion tracking uses the Pinterest Tag (JavaScript) and Conversions API. Shopping campaigns connect product catalogs. Pinterest users have high purchase intent — 85% of weekly Pinners have purchased based on Pins they've seen.",

    # Reddit Ads API
    "Reddit Ads API uses OAuth 2.0 with API Key authentication. Targeting includes subreddit/community targeting, interest targeting, and conversation placement. Promoted posts appear in feeds. CPCs typically $0.50-3. Success requires authentic language matching subreddit culture. The python-reddit package provides API access.",

    # Quora Ads API
    "Quora Ads API provides access to Quora's question-and-answer platform advertising. Targeting includes topic targeting, question targeting, audience targeting, and keyword targeting. Ad formats: Text Ads, Image Ads, and Promoted Answers. Conversion tracking uses the Quora Pixel.",

    # Threads API
    "Threads API (by Meta) is in early development. The platform supports text-based posts up to 500 characters with images and video. Advertising capabilities are being developed. API access follows Meta's developer platform authentication patterns.",

    # ═══════════════════════════════════════════════════════════
    # DSP / PROGRAMMATIC
    # ═══════════════════════════════════════════════════════════

    # The Trade Desk
    "The Trade Desk (TTD) is the largest independent DSP for programmatic advertising. API uses API Key authentication. Supports display, video, audio, native, CTV, and DOOH inventory. Uses Koa AI for bid optimization. Unified ID 2.0 is their cookieless identity solution. Requires $50K+ monthly minimum spend.",

    # Amazon DSP
    "Amazon DSP enables programmatic buying on and off Amazon properties. Uses AWS-based authentication (Login with Amazon). Reaches Amazon shoppers with exclusive first-party purchase data. Supports display, video, and audio. Self-serve minimum $35K+. Available audiences: in-market, lifestyle, and Amazon purchase-based segments.",

    # DV360 (Google)
    "DV360 (Display & Video 360) is Google's enterprise DSP with access to Google Ad Exchange inventory plus 80+ third-party exchanges. Uses OAuth 2.0. Supports Programmatic Guaranteed, Preferred Deals, Private Auctions, and Open Auction buying methods. Integrates with CM360 and Google Analytics.",

    # Xandr (Microsoft)
    "Xandr (now Microsoft Advertising DSP) provides programmatic buying across display, video, native, and CTV. Uses username/password token authentication. Offers both self-serve and managed service tiers. Integrates with Microsoft's audience data including LinkedIn signals.",

    # MediaMath
    "MediaMath is an enterprise DSP specializing in omnichannel programmatic advertising. Uses API Key authentication. Supports display, video, native, audio, CTV, and DOOH. Features include audience management, identity resolution, and cross-device targeting.",

    # Criteo
    "Criteo is a commerce media platform specializing in retargeting and retail media. Uses OAuth 2.0 with the criteo-api-python-sdk. Products include dynamic retargeting (automatically shows products users viewed), retail media (ads on retailer sites), and commerce audiences. Known for high-quality product recommendation algorithms.",

    # AdRoll / RollWorks
    "AdRoll provides retargeting, prospecting, and email marketing for D2C and ecommerce. RollWorks is their B2B account-based marketing platform. Uses OAuth 2.0 with API Key. Features cross-channel retargeting across web, social, and email. Integrates with Shopify, WooCommerce, and major ecommerce platforms.",

    # StackAdapt
    "StackAdapt is a self-serve programmatic DSP for native, display, video, CTV, audio, and in-game advertising. Uses API Key authentication. Known for strong native advertising capabilities. Features contextual targeting, audience targeting, and page-context AI for brand safety.",

    # Basis Technologies (Centro)
    "Basis Technologies (formerly Centro) provides a programmatic advertising platform combining DSP, workflow automation, and business intelligence. Supports display, video, native, audio, CTV, and DOOH. The platform unifies programmatic, direct, search, and social campaign management.",

    # ═══════════════════════════════════════════════════════════
    # RETAIL / COMMERCE
    # ═══════════════════════════════════════════════════════════

    # Amazon Ads (Sponsored)
    "Amazon Sponsored Products, Sponsored Brands, and Sponsored Display are the three core ad formats. ACOS (Advertising Cost of Sales) = Ad Spend / Ad Revenue is the primary metric. Automatic targeting discovers relevant search terms. Manual targeting uses keyword or product targeting. Uses amazon-ads Python SDK v5.0+.",
    "Amazon Attribution measures how non-Amazon channels (Google, Meta, email) drive Amazon sales. Uses Login with Amazon authentication. Provides click-through and conversion data with 14-day attribution window. Essential for brands running off-Amazon media driving to Amazon product pages.",

    # Walmart Connect
    "Walmart Connect is Walmart's retail media platform. Offers Sponsored Products (search), Display (on-site and off-site), and In-Store advertising. Uses Client ID + Secret authentication. Requires REST API integration. Leverages Walmart's first-party purchase data for targeting and closed-loop measurement.",

    # Instacart Ads
    "Instacart Ads offers Sponsored Products and Display advertising on the Instacart grocery delivery platform. Features include keyword targeting, automated bidding, and brand pages. Uses OAuth 2.0 authentication. Provides closed-loop measurement connecting ad impressions to purchases.",

    # Shopify Audiences
    "Shopify Audiences uses aggregated commerce data from Shopify merchants to create high-intent audience lists for advertising on Meta, Google, Pinterest, Snapchat, TikTok, and Criteo. Available to Shopify Plus merchants. Audiences update automatically based on purchase signals.",

    # Google Shopping (CSS)
    "Google Comparison Shopping Services (CSS) allow third-party shopping comparison sites to place Shopping ads on behalf of merchants. CSS partners can offer reduced auction fees compared to Google Shopping directly. Multiple CSS partners can represent the same merchant in different markets.",

    # eBay Promoted Listings
    "eBay Promoted Listings offers Standard (cost-per-sale) and Advanced (cost-per-click) ad formats. Standard Listings charge only when an item sells after an ad click. The API enables automated listing promotion and performance reporting. No minimum spend required.",

    # Target Roundel
    "Target Roundel is Target's retail media network offering display, video, social, and search advertising. Uses Target's first-party Guest ID data covering 165M+ shoppers. Provides closed-loop measurement connecting ad exposure to in-store and online purchases. Access is through a managed service or partner agreement.",

    # ═══════════════════════════════════════════════════════════
    # VIDEO / CTV
    # ═══════════════════════════════════════════════════════════

    # YouTube Ads (via Google Ads)
    "YouTube advertising runs through Google Ads using Video campaigns. Formats: skippable in-stream, non-skippable in-stream, bumper (6 sec), in-feed video, and Shorts ads. Targeting includes demographics, interests, topics, keywords, placements, and custom audiences. Uses google-ads Python library with google-py-video-youtube.",

    # Roku OneView
    "Roku OneView (formerly dataxu) is Roku's advertising platform for CTV and streaming. Provides access to Roku's first-party viewership data across 80M+ active accounts. Supports video, display, and native formats on Roku devices and the broader CTV ecosystem. Access through partner agreement.",

    # Samsung Ads
    "Samsung Ads leverages Samsung Smart TV data for CTV advertising and audience targeting. Offers Native Samsung TV+ ads, display ads, and programmatic buying via partner DSPs. Uses Samsung's Automatic Content Recognition (ACR) data for viewership insights and targeting.",

    # Spotify Ad Studio
    "Spotify Ad Studio is the self-serve platform for audio and video ads on Spotify. Targets by demographics, interests, listening behavior, playlists, and podcasts. Audio ads can be generated using Spotify's text-to-speech tool. Minimum campaign spend starts at $250.",

    # ═══════════════════════════════════════════════════════════
    # MOBILE / APP
    # ═══════════════════════════════════════════════════════════

    # Google AdMob
    "Google AdMob monetizes mobile apps with display, interstitial, rewarded, and native ads. The AdMob API uses OAuth 2.0. Integrates with Google Ads for app campaign management. Supports mediation to optimize fill rates across multiple ad networks. Firebase integration enables analytics and A/B testing.",

    # Unity Ads
    "Unity Ads provides in-game advertising for Unity-developed games. Supports rewarded video, interstitial, and banner formats. The SDK integrates into Unity game engine projects. Uses Dashboard Key authentication. Particularly strong in the gaming vertical with rewarded video monetization.",

    # AppsFlyer
    "AppsFlyer is a mobile attribution and analytics platform. Tracks app installs and in-app events across advertising channels. Uses API Key authentication. Features include deep linking, fraud protection, incrementality measurement, and audience segmentation. Integrates with 10,000+ technology partners.",

    # Adjust
    "Adjust provides mobile attribution, analytics, and fraud prevention. Tracks installs, events, and revenue across channels. Uses API Key authentication with the adjust-api Python SDK. Features include deep linking, audience builder, incrementality testing, and automated fraud prevention.",

    # AppLovin
    "AppLovin MAX is a mediation platform that optimizes ad revenue across networks. AppLovin's AppDiscovery uses machine learning for user acquisition. The ALX exchange enables programmatic in-app advertising. Uses Dashboard Key authentication.",

    # Branch (Attribution)
    "Branch provides deep linking and mobile attribution. Creates universal links that route users to the right content across web, app, and email. Measures cross-platform attribution. Uses API Key authentication. Integrates with all major ad networks and analytics platforms.",

    # ═══════════════════════════════════════════════════════════
    # NATIVE / CONTENT
    # ═══════════════════════════════════════════════════════════

    # Taboola
    "Taboola is a native advertising platform reaching 500M+ daily users across premium publisher sites. Uses OAuth 2.0 authentication. Ad formats include native content recommendations, video, and display. Targeting includes audience segments, contextual, and custom audiences. Known for content discovery and recommendation widgets.",

    # Outbrain
    "Outbrain powers native advertising on premium publisher websites. Uses API Key authentication. Supports native content, video, carousel, and app install formats. Targeting includes interest-based, contextual, lookalike, and custom audience segments. Merged with Taboola in recent years.",

    # MGID
    "MGID is a native advertising platform providing content recommendations across global publishers. Supports native, display, and video formats. Uses API Key authentication. Features include contextual targeting, audience segments, and AI-powered optimization. Known for strong presence in international markets.",

    # ═══════════════════════════════════════════════════════════
    # TAG / ANALYTICS
    # ═══════════════════════════════════════════════════════════

    # Google Analytics 4 (GA4)
    "Google Analytics 4 (GA4) uses event-based tracking replacing Universal Analytics. The GA4 API uses OAuth 2.0 with the google-analytics-data Python package. Key features: cross-platform tracking, enhanced measurement, BigQuery export, predictive audiences, and privacy-centric design with cookieless measurement.",
    "GA4 event model: automatically collected (page_view, first_visit), enhanced measurement (scroll, outbound_clicks, file_downloads), recommended events (purchase, add_to_cart, sign_up), and custom events. Up to 500 distinct events. Conversion events are marked in the UI.",

    # Google Tag Manager
    "Google Tag Manager (GTM) manages marketing and analytics tags without code changes. Uses OAuth 2.0 with the tagmanager v2 API. Supports web and mobile containers. Server-side GTM runs tags on a cloud server for improved performance and data control. Triggers fire tags based on events, page views, or custom conditions.",

    # Google Search Console
    "Google Search Console provides organic search performance data: impressions, clicks, CTR, and average position by query, page, country, and device. The API uses OAuth 2.0 with google-api-python-client. Essential for SEO and understanding how paid and organic search interact.",

    # Meta Pixel / CAPI
    "Meta Pixel (client-side) and Conversions API (server-side) work together for complete conversion tracking. Post-iOS 14.5, server-side CAPI is essential for accurate measurement. Aggregated Event Measurement limits optimization to 8 priority events per domain. Event Match Quality score measures data signal strength.",

    # Microsoft Clarity
    "Microsoft Clarity is a free user behavior analytics tool providing session recordings, heatmaps, and insights. No sampling and no data limits. Integrates with Google Analytics and Microsoft Advertising. Useful for diagnosing landing page issues affecting ad conversion rates.",

    # ═══════════════════════════════════════════════════════════
    # MEASUREMENT
    # ═══════════════════════════════════════════════════════════

    # Google Ads Data Hub
    "Google Ads Data Hub enables privacy-safe analysis of Google Ads campaign data in BigQuery. Combines Google's ad event data with advertiser's first-party data. Uses SQL for custom analysis. No private API — accessed through Google Cloud. Essential for enterprise-level campaign attribution and audience analysis.",

    # Google Ads Transparency Center
    "Google Ads Transparency Center shows verified advertiser information and ads served across Google platforms. No public API. Useful for competitive research — see what ads competitors are running, their verification status, and regions where ads are served.",

    # ═══════════════════════════════════════════════════════════
    # AFFILIATE / OTHER
    # ═══════════════════════════════════════════════════════════

    # Commission Junction (CJ)
    "Commission Junction (CJ Affiliate) is one of the largest affiliate marketing networks. Uses API Key authentication. Provides publisher and advertiser APIs for program management, reporting, and link generation. Tracks conversions through CJ's tracking pixel and server-side postback.",

    # ShareASale
    "ShareASale (now part of Awin) is an affiliate marketing network connecting merchants with publishers. Uses API Key authentication via ShareASale API Reference. Provides reporting, merchant discovery, and affiliate link management APIs.",

    # Impact
    "Impact is a partnership automation platform for affiliate, influencer, and B2B partnerships. Uses API Key authentication. Features include partner discovery, contracting, tracking, payment, and optimization. Supports mobile app attribution and cross-device tracking.",

    # Rakuten Advertising
    "Rakuten Advertising provides affiliate marketing, display, and search retargeting services. Uses API Token authentication. The network connects brands with publishers globally. Features include commissioning, reporting, and creative management APIs.",

    # ═══════════════════════════════════════════════════════════
    # CROSS-PLATFORM KNOWLEDGE
    # ═══════════════════════════════════════════════════════════

    "OAuth 2.0 is the most common authentication method across advertising platforms. The flow: register an app, get client credentials, redirect user for authorization, receive an access token, refresh when expired. Google, Meta, Microsoft, LinkedIn, Snapchat, Pinterest, and Criteo all use OAuth 2.0.",
    "API Key authentication is simpler than OAuth — a single key in the request header. Used by The Trade Desk, Reddit, MediaMath, Taboola, Outbrain, CJ Affiliate, and ShareASale. Less secure than OAuth but easier to implement for server-to-server integrations.",
    "Retail Media Networks (RMNs) are the fastest-growing advertising channel. Amazon, Walmart, Target, Instacart, and Kroger all offer advertising on their commerce platforms. Key advantage: closed-loop measurement connecting ad exposure directly to purchase. RMN spend exceeded $40B in 2024.",
    "Connected TV (CTV) advertising reaches viewers on streaming platforms. Available through DV360, The Trade Desk, Amazon DSP, Roku OneView, Samsung Ads, and platform-specific buys. CTV offers TV-like reach with digital targeting precision. Key metrics: completed views, reach, frequency, and brand lift.",
    "Mobile Measurement Partners (MMPs) like AppsFlyer, Adjust, Branch, and Singular provide app install attribution. They determine which ad click or view led to an app install using device identifiers and probabilistic modeling. Essential for mobile app advertising across all platforms.",
    "Server-side tracking (Meta CAPI, Google Enhanced Conversions, LinkedIn CAPI, TikTok Events API) sends conversion data directly from your server to the ad platform. This bypasses browser restrictions (ITP, cookie blocking) and improves attribution accuracy. Increasingly required post-iOS 14.5.",
    "Cross-platform metric normalization: Google's CPA = Meta's Cost Per Result = LinkedIn's Cost Per Conversion. Google's ROAS = Amazon's inverse ACOS (1/ACOS × 100). Google's CTR = most platforms' CTR. Create a unified reporting layer mapping each platform's terminology to standard KPIs.",
    "Programmatic advertising uses automated technology to buy and sell digital ad inventory in real-time. The ecosystem includes DSPs (buy-side), SSPs (sell-side), ad exchanges (marketplaces), and DMPs (data management). RTB (real-time bidding) auctions happen in under 100 milliseconds.",
    "First-party data activation: upload customer lists to Google (Customer Match), Meta (Custom Audiences), LinkedIn (Matched Audiences), TikTok (Custom Audiences), and Pinterest (Customer Lists). Match rates vary: email 30-60%, phone 20-40%. Hash data (SHA-256) before upload for privacy compliance.",
    "Privacy regulations impact advertising: GDPR (EU), CCPA/CPRA (California), LGPD (Brazil). All platforms require consent for tracking. Cookie deprecation affects cross-site tracking. Solutions: server-side tracking, first-party data strategies, contextual targeting, and cohort-based solutions.",
    "Multi-touch attribution models: Last Click (default for most platforms, gives all credit to final touchpoint), Data-Driven (ML-based, Google and Meta default), Time Decay (more credit to recent interactions), Position-Based (40/20/40 split first/middle/last). Each platform tends to over-credit its own channel.",
    "Creative asset specifications vary by platform. Google Responsive Display: images 1200×628, 1200×1200; headlines 30 chars; descriptions 90 chars. Meta: images 1080×1080 or 1200×628; primary text 125 chars; headline 40 chars. LinkedIn: images 1200×627; headline 70 chars. TikTok: 9:16 vertical video, 5-60 seconds.",
]


PLATFORM_SFT_PAIRS = [
    # Cross-platform scenarios
    {"user": "What advertising platforms should a B2B SaaS company use?",
     "assistant": "For B2B SaaS, prioritize these platforms: 1) Google Ads Search (50-60% budget) — capture high-intent users searching for solutions. Use Target CPA bidding with offline conversion tracking. 2) LinkedIn Ads (20-25%) — unmatched B2B targeting by job title, company, industry. Lead Gen Forms get 2-5x higher conversion rates. CPCs are $5-15+ but lead quality is premium. 3) Microsoft Ads (10-15%) — import from Google, get 30-50% lower CPCs with older/higher-income audience + LinkedIn targeting integration. 4) Meta Ads (5-10%) — retargeting warm audiences and lookalikes from customer lists. Start with Google + LinkedIn, prove ROI, then expand."},

    {"user": "How do I track conversions across Google, Meta, and LinkedIn?",
     "assistant": "Set up three tracking systems: 1) Google — install gtag.js or use Google Tag Manager, configure conversion actions in Google Ads, enable Enhanced Conversions (sends hashed email server-side). 2) Meta — install Meta Pixel for client-side events, set up Conversions API (CAPI) for server-side events, configure Aggregated Event Measurement with your 8 priority events. 3) LinkedIn — install LinkedIn Insight Tag, set up conversion tracking with URL or event-based rules. For all three: use UTM parameters consistently, set up Google Analytics 4 as your source of truth to deduplicate cross-platform conversions, and implement server-side tracking for accuracy post-iOS 14.5."},

    {"user": "Explain the difference between a DSP and a social platform for advertising.",
     "assistant": "DSPs (The Trade Desk, DV360, Amazon DSP, Xandr) buy ad inventory programmatically across thousands of websites, apps, and CTV through real-time bidding. They excel at: reach across the open web, advanced audience targeting using third-party data, cross-channel buying (display, video, CTV, audio, DOOH). Social platforms (Meta, LinkedIn, TikTok, Snapchat, Pinterest) sell advertising only on their own properties. They excel at: rich first-party user data, native ad formats that blend with content, social engagement and sharing. Use DSPs for broad reach and retargeting at scale. Use social for awareness, engagement, and leveraging platform-specific audiences and formats."},

    {"user": "What is ACOS on Amazon and how does it compare to Google ROAS?",
     "assistant": "ACOS (Advertising Cost of Sales) = Ad Spend / Ad Revenue × 100. It measures what percentage of revenue went to ads. ROAS (Return on Ad Spend) = Revenue / Ad Spend. They're inverse: ROAS = 1 / (ACOS/100). Examples: ACOS 25% = ROAS 400%. ACOS 50% = ROAS 200%. ACOS 10% = ROAS 1000%. For Amazon, target ACOS below your profit margin. If margin is 30%, keep ACOS under 25% for profitability. On Google, the equivalent is Target ROAS > break-even ROAS (1/margin). Same math, flipped metric."},

    {"user": "How do retail media networks like Walmart Connect and Target Roundel compare to Amazon Ads?",
     "assistant": "All three are retail media networks (RMNs) using first-party purchase data for targeting and closed-loop measurement. Amazon Ads: largest RMN, self-serve via amazon-ads SDK, Sponsored Products/Brands/Display, ACOS-based optimization, 300M+ active customers. Walmart Connect: second-largest, uses Client ID + Secret auth, Sponsored Products + Display, leverages 150M+ weekly shoppers, both on-site and off-site inventory. Target Roundel: managed service primarily, uses Target's Guest ID covering 165M+ shoppers, display, video, social, and search formats, strong in-store measurement. Start with Amazon if you sell there, then expand to Walmart and Target based on your distribution."},

    {"user": "What mobile attribution platforms should I use, and how do they work?",
     "assistant": "The major MMPs: AppsFlyer (largest, broadest integrations), Adjust (strong fraud prevention), Branch (best deep linking), Singular (includes creative analytics). How they work: 1) User clicks an ad on Facebook/Google/TikTok/etc. 2) MMP records the click with device fingerprint or identifier. 3) User installs and opens the app. 4) MMP SDK fires, matches the install to the original click. 5) Attribution is reported to the ad platform. They use IDFA (iOS, requires ATT consent), GAID (Android), and probabilistic modeling when identifiers aren't available. Pick AppsFlyer or Adjust for broad needs. Branch if deep linking is critical. All use API Key authentication."},

    {"user": "How do I advertise on CTV (Connected TV)?",
     "assistant": "CTV advertising reaches streaming viewers on smart TVs, Roku, Fire TV, Apple TV, etc. Your options: 1) DV360 — Google's DSP, access to YouTube TV + programmatic CTV inventory, OAuth 2.0, best for Google ecosystem users. 2) The Trade Desk — largest independent DSP, broad CTV inventory across all platforms, API Key auth, $50K+ minimum. 3) Amazon DSP — Fire TV + Amazon Freevee inventory, AWS auth, strong purchase-based targeting. 4) Roku OneView — direct access to Roku's 80M+ accounts, first-party viewership data. 5) Samsung Ads — Samsung Smart TV ACR data. For most advertisers, start with DV360 or The Trade Desk. CTV campaigns optimize for completed views, reach, and frequency. Expect CPMs of $25-40."},

    {"user": "How do I use Taboola or Outbrain for native advertising?",
     "assistant": "Taboola and Outbrain place native content recommendations on premium publisher sites (CNN, Forbes, Business Insider, etc.). Setup: 1) Create an advertiser account, set up conversion tracking pixel. 2) Upload content — articles, landing pages, or product pages with compelling headlines and thumbnails. 3) Set targeting: by audience interest, contextual relevance, device, geo, or custom audiences. 4) Set CPC bids (typically $0.30-1.50 for B2B, $0.10-0.50 for content). 5) Optimize based on CTR and conversion rate. Key difference from search/social: users discover your content while reading articles, so the content must be genuinely valuable, not just a sales pitch. Taboola uses OAuth 2.0, Outbrain uses API Key authentication."},

    {"user": "What tracking tags should every website have installed?",
     "assistant": "Essential tags: 1) Google Tag Manager — container that manages all other tags. 2) GA4 — event-based analytics, the source of truth. 3) Google Ads gtag — conversion tracking + remarketing. 4) Meta Pixel — conversion tracking + audience building. 5) Meta Conversions API — server-side complement to Pixel. 6) LinkedIn Insight Tag — conversion tracking + audience building (if running LinkedIn Ads). 7) Microsoft UET Tag — if running Microsoft Ads. 8) TikTok Pixel — if running TikTok Ads. Recommended: Microsoft Clarity (free heatmaps/recordings), Google Search Console verification. Install everything through GTM for easy management. Implement server-side tracking (GTM Server Container) for maximum accuracy."},

    {"user": "Compare Google Performance Max, Meta Advantage+, and TikTok Smart Performance campaigns.",
     "assistant": "All three are AI-automated campaign types that handle targeting, placement, and bidding: Google PMax: optimizes across Search, Shopping, Display, YouTube, Discover, Gmail, Maps. Requires asset groups with text + images + video + audience signals. Best with 50+ monthly conversions and a product feed. Meta Advantage+: automates audience targeting and creative combinations. Advantage+ Shopping is catalog-based. Works best with established Pixel data and broad product catalogs. TikTok Smart Performance: fully automated campaigns with minimal setup. Provides creative assets and TikTok handles targeting, bidding, and placement. All three reduce manual control in exchange for algorithmic optimization. They work best with sufficient conversion data (30-50+/month) and strong creative assets. Keep dedicated search/brand campaigns running alongside."},

    {"user": "How do I set up server-side conversion tracking across platforms?",
     "assistant": "Server-side tracking sends conversion data from your server directly to ad platforms, bypassing browser limitations. Setup: 1) Google Tag Manager Server Container — deploy on Google Cloud, configure Google Ads and GA4 clients, route events server-side. 2) Meta Conversions API — send events via HTTP POST to graph.facebook.com, include user parameters (hashed email, phone, IP, user agent) for matching. System User Token authentication. 3) LinkedIn Conversions API — send events with hashed email/company for matching. 4) TikTok Events API — send events to business-api.tiktok.com with hashed user data. For all platforms: hash PII with SHA-256 before sending, include event_time and event_source_url, send both client-side and server-side events with event_id for deduplication."},

    {"user": "What Python packages do I need to manage ads across all major platforms?",
     "assistant": "Core Python packages by platform: google-ads (v25.1+) for Google Ads API v23. facebook-business (v21.0+) for Meta Ads. bingads for Microsoft Advertising. amazon-ads (v5.0+) for Amazon Sponsored Ads. google-analytics-data for GA4 reporting. google-api-python-client for Search Console, GTM, DV360. linkedin-api for LinkedIn (community package). criteo-api-python-sdk for Criteo. For attribution: appsflyer and adjust SDKs. For automation: use requests library for platforms without official SDKs (TikTok, Snapchat, Pinterest, Reddit, Taboola). All are pip-installable. Most use OAuth 2.0 — store credentials securely using environment variables, never hardcode tokens."},

    {"user": "How do I build a unified cross-platform advertising report?",
     "assistant": "Build a unified reporting pipeline: 1) Data extraction — pull data from each platform's API. Use scheduled Python scripts or tools like Supermetrics, Funnel.io. 2) Normalization — map metrics to standard names: Spend, Impressions, Clicks, Conversions, Revenue, CPA, ROAS. Map Google's cost_micros (÷1M), Amazon's ACOS (convert to ROAS), Meta's Cost Per Result (= CPA). 3) Storage — load into BigQuery, Snowflake, or PostgreSQL. 4) Deduplication — use your analytics platform (GA4) as the source of truth. UTM parameters identify which platform drove each conversion. 5) Dashboard — Looker Studio, Tableau, or Google Sheets. Include: platform comparison table, blended totals, channel mix, trend charts, and CPA/ROAS by platform. 6) Add columns: Platform, Campaign, Spend, Impressions, Clicks, CTR, Conversions, CPA, ROAS, Impression Share (where available)."},

    {"user": "What is the difference between Google Merchant Center and Amazon product feeds?",
     "assistant": "Both are product catalogs that power shopping ads, but differ significantly. Google Merchant Center: feeds Shopping and PMax campaigns, requires standard attributes (id, title, description, link, image_link, price, availability, brand, gtin/mpn, condition), optimized titles boost performance, supplemental feeds allow quick updates, Google validates feed quality and disapproves non-compliant products. Content API v2.1 for programmatic management. Amazon Product Catalog: products are listed on Amazon itself (not just ads), catalog info comes from your Seller Central or Vendor Central listings, ad targeting uses ASINs and keywords, product detail pages are the landing pages. Amazon Attribution tracks off-Amazon traffic to Amazon pages. Key difference: Google sends traffic to YOUR website. Amazon keeps traffic on Amazon."},

    {"user": "Explain programmatic advertising and the role of DSPs, SSPs, and ad exchanges.",
     "assistant": "Programmatic advertising automates ad buying/selling through technology. The ecosystem: DSPs (Demand-Side Platforms) — advertisers use DSPs to buy ad inventory. Examples: The Trade Desk, DV360, Amazon DSP, Xandr. DSPs bid on inventory in real-time based on targeting criteria. SSPs (Supply-Side Platforms) — publishers use SSPs to sell their ad inventory. Examples: Google Ad Manager, Magnite, PubMatic, Index Exchange. SSPs connect to multiple ad exchanges to maximize revenue. Ad Exchanges — marketplaces where DSPs and SSPs meet. Google Ad Exchange is the largest. Open RTB auctions happen in under 100ms. DMPs (Data Management Platforms) — aggregate audience data for targeting. Increasingly replaced by CDPs (Customer Data Platforms) with first-party data. The flow: user loads a webpage → SSP sends bid request to ad exchange → DSPs evaluate and bid → highest bidder wins → ad is served — all in milliseconds."},
]


PLATFORM_DPO_PAIRS = [
    {"prompt": "Should I run ads on every platform at once?",
     "chosen": "No. Start with 2-3 platforms where your audience is most active and your budget can generate statistically significant data (at least 30+ conversions/month per platform). For B2B: Google Search + LinkedIn. For ecommerce: Google Shopping + Meta. For apps: Google App + Meta + TikTok. Prove ROI on core platforms, then expand methodically. Spreading budget across too many platforms means none get enough data to optimize.",
     "rejected": "Yes, be everywhere! The more platforms you advertise on, the more people you reach. Set up campaigns on Google, Meta, LinkedIn, TikTok, Snapchat, Pinterest, Reddit, and Twitter simultaneously. Cast the widest net possible."},

    {"prompt": "How should I handle attribution across multiple ad platforms?",
     "chosen": "Use your analytics platform (GA4) as the single source of truth, not individual ad platform reports. Each platform takes credit for conversions it influenced, leading to over-counting. Set up consistent UTM parameters across all platforms. Implement server-side tracking for accuracy. Compare GA4 attributed conversions to platform-reported conversions to understand each platform's self-attribution inflation. Accept that no attribution model is perfect.",
     "rejected": "Just add up the conversions each platform reports. Google says 50 conversions, Meta says 30, LinkedIn says 20 — that means you got 100 total conversions. Each platform tracks independently so the numbers are accurate."},

    {"prompt": "Should I use a DSP or stick with platform-specific ad buying?",
     "chosen": "It depends on scale and goals. Use platform-specific buying (Google Ads, Meta Ads Manager) when: budget is under $10K/month, you need platform-specific features (Search, Shopping, Lead Gen Forms), or you're just starting. Use a DSP (The Trade Desk, DV360) when: budget exceeds $25K+/month, you need cross-channel programmatic reach (display, CTV, audio, DOOH), you want unified frequency management across publishers, or you need advanced audience data. Most advertisers should master platform-specific buying first, then add a DSP for incremental reach.",
     "rejected": "Always use a DSP — they're more sophisticated than platform-native tools. Direct platform buying is outdated. Move everything to programmatic for better performance across the board."},
]

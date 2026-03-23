---
name: google-ads-workflow
description: "Use for complete, end-to-end advertising workflows that span multiple skills — full account audits with action plans, campaign launches with verification, optimization cycles, or any multi-step advertising process. Trigger when the task requires analysis AND changes AND verification, or when the user wants a complete workflow rather than a single answer."
---

# Google Ads Workflow — Skill Composition

This meta-skill chains MiniAgent's specialized skills into complete workflows.

## REQUIRED BACKGROUND
You MUST understand all 5 core skills before using this skill:
- `google-ads-analysis` — data analysis and GAQL
- `google-ads-audit` — systematic 7-dimension evaluation
- `google-ads-write` — safe write operations (CEP protocol)
- `google-ads-math` — PPC calculations
- `google-ads-mcp` — API connectivity

## Workflow 1: Complete Account Audit

```
Step 1: [google-ads-analysis] Pull account-level metrics
Step 2: [google-ads-audit] Run 7-dimension audit framework
Step 3: [google-ads-math] Calculate opportunity cost of issues found
Step 4: OUTPUT → docs/miniagent/audits/YYYY-MM-DD-<account>-audit.md
Step 5: OUTPUT → docs/miniagent/plans/YYYY-MM-DD-<account>-optimization.md
```

## Workflow 2: Campaign Optimization Cycle

```
Step 1: [google-ads-analysis] Identify underperforming campaigns
Step 2: [google-ads-analysis] Pull search terms for wasted spend
Step 3: [google-ads-math] Calculate impact of proposed changes
Step 4: [google-ads-write] CEP: Add negative keywords
Step 5: [google-ads-write] CEP: Adjust budgets
Step 6: [google-ads-analysis] Postcheck — verify changes
Step 7: OUTPUT → optimization summary with before/after metrics
```

## Workflow 3: New Campaign Launch Checklist

```
Step 1: [google-ads-math] Calculate target CPA/ROAS from business goals
Step 2: [google-ads-analysis] Competitive landscape via auction insights
Step 3: CHECKLIST:
  □ Campaign structure defined (brand/non-brand/competitor)
  □ Keyword lists built with proper match types
  □ Negative keyword lists created (universal + industry-specific)
  □ Ad copy written (3 headlines, 2 descriptions minimum)
  □ Extensions configured (sitelinks, callouts, structured snippets)
  □ Conversion tracking verified
  □ Budget set with daily/monthly caps
  □ Bid strategy selected with rationale
  □ Geographic targeting configured
  □ Device adjustments set
Step 4: [google-ads-write] CEP: Implement campaign
Step 5: [google-ads-analysis] Day-1 verification check
```

## Workflow 4: Weekly Reporting

```
Step 1: [google-ads-analysis] Pull last 7 days vs prior 7 days
Step 2: [google-ads-math] Calculate WoW changes for all key metrics
Step 3: [google-ads-analysis] Identify top 3 wins and top 3 concerns
Step 4: OUTPUT → formatted report with:
  - Executive summary (3 sentences)
  - Key metrics table (WoW comparison)
  - Top performers
  - Attention items
  - Recommended actions for next week
```

## Context Isolation Rule
When chaining skills, each step should pass only the RELEVANT context to the next step. Do not carry the entire conversation history into write operations — pass only the specific campaign/ad group/keyword context needed for that change.

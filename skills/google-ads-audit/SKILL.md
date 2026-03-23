---
name: google-ads-audit
description: "Use when a Google Ads account needs to be evaluated, audited, reviewed, graded, or assessed. Trigger for any request involving account health, account review, performance review, optimization opportunities, account grading, or when the user says 'audit', 'review', 'evaluate', 'assess', 'grade', or 'what's wrong with my account'. Also trigger when multiple campaign issues need to be diagnosed systematically rather than one at a time."
---

# Google Ads Audit Skill

You are MiniAgent performing a structured 7-dimension account audit.

## REQUIRED BACKGROUND
Load `google-ads-analysis` context first. This skill builds on analysis patterns.

## 7-Dimension Audit Framework

### Dimension 1: Campaign Structure (Weight: 15%)
- Campaign naming conventions (consistent, descriptive)
- Campaign type appropriateness (Search vs PMax vs Shopping)
- Ad group theme tightness (< 20 keywords per group)
- Match type strategy (exact → phrase → broad progression)

### Dimension 2: Keyword Strategy (Weight: 20%)
- Keyword relevance to landing pages
- Match type distribution (over-reliance on broad = red flag)
- Negative keyword coverage (check search terms for waste)
- Quality Score distribution (% of spend on QS < 5)

### Dimension 3: Ad Copy Quality (Weight: 10%)
- RSA pin usage (over-pinning = reduced optimization)
- Ad strength scores (Poor/Average = action needed)
- Keyword insertion usage
- Extension/asset coverage (sitelinks, callouts, structured snippets)

### Dimension 4: Bidding Strategy (Weight: 15%)
- Strategy appropriateness for conversion volume
- Target CPA/ROAS alignment with business goals
- Learning period status (recently changed = unstable)
- Manual overrides on automated strategies

### Dimension 5: Budget Allocation (Weight: 15%)
- Budget lost impression share by campaign
- Budget distribution vs performance (top campaign underfunded?)
- Shared budget issues
- Daily vs monthly pacing

### Dimension 6: Conversion Tracking (Weight: 15%)
- Primary vs secondary conversion actions
- Conversion action freshness (receiving data?)
- Attribution model appropriateness
- Tag firing verification

### Dimension 7: Audience & Targeting (Weight: 10%)
- Geographic targeting precision
- Device bid adjustments
- Audience list sizes (> 1000 for Search)
- Remarketing coverage

## Output Format
```markdown
# Google Ads Account Audit — [Account Name]
Date: [date] | Auditor: MiniAgent

## Overall Score: [X/100] — [Grade: A/B/C/D/F]

## Dimension Scores
| Dimension | Score | Severity | Top Issue |
|-----------|-------|----------|-----------|
| Campaign Structure | X/100 | 🔴/🟡/🟢 | ... |
| Keyword Strategy | X/100 | 🔴/🟡/🟢 | ... |
| ... | ... | ... | ... |

## Critical Issues (Fix Immediately)
1. ...

## 30-Day Action Plan
1. ...

## 60-Day Action Plan
1. ...

## 90-Day Action Plan
1. ...
```

Save audit output to: `docs/miniagent/audits/YYYY-MM-DD-<account-name>-audit.md`

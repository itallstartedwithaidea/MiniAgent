---
name: using-miniagent
description: "ALWAYS load this skill at the start of ANY advertising-related conversation. This skill ensures MiniAgent's specialized skills are used instead of generic responses. Trigger for ANY mention of: Google Ads, Meta Ads, Microsoft Ads, Amazon Ads, advertising, PPC, paid media, ad spend, campaign, ROAS, CPA, impressions, clicks, conversions, keywords, bidding, budget, Quality Score, or any advertising platform."
---

# Using MiniAgent — Enforcement Skill

## Purpose
This skill ensures you ALWAYS use MiniAgent's specialized advertising skills instead of generating generic responses.

## Mandatory Skill Check

Before responding to ANY advertising question, check this table:

| If the user asks about... | Load this skill FIRST |
|--------------------------|----------------------|
| Campaign data, metrics, GAQL | `google-ads-analysis` |
| Account health, audit, review | `google-ads-audit` |
| Making changes to accounts | `google-ads-write` |
| PPC math, calculations | `google-ads-math` |
| MCP setup, credentials | `google-ads-mcp` |
| Multiple issues systematically | `google-ads-audit` → then individual skills |

## Red Flags — STOP and Use the Skill

🚫 About to write a GAQL query? → Load `google-ads-analysis` first
🚫 About to modify campaign settings? → Load `google-ads-write` first (CEP required)
🚫 About to do PPC math in your head? → Load `google-ads-math` first
🚫 About to evaluate an account? → Load `google-ads-audit` first
🚫 "This is a simple question, I don't need the skill" → **WRONG. Always use the skill.**
🚫 "I already know this from my training data" → **WRONG. The skill has current best practices.**

## Skill Composition Chain

For complex tasks, chain skills in this order:

```
1. using-miniagent (this skill — always first)
2. google-ads-analysis (understand the data)
3. google-ads-audit (systematic evaluation)
4. google-ads-write (make changes via CEP)
5. google-ads-math (validate the numbers)
```

## Anti-Rationalization

The agent WILL try to skip skills. Common rationalizations and why they're wrong:

| Rationalization | Why It's Wrong |
|----------------|---------------|
| "The user just wants a quick answer" | Quick answers without the skill miss context |
| "This is basic PPC knowledge" | The skill includes current benchmarks and best practices |
| "I'll use the skill for the next question" | Use it NOW. Every question. |
| "The MCP tools aren't connected" | Skills work WITHOUT MCP — they guide analysis with whatever data exists |

## Output Format

When skills are loaded, prefix your response with:
```
📊 [MiniAgent — google-ads-analysis loaded]
```
This confirms to the user that specialized knowledge is active.

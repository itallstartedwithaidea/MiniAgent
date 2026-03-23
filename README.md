<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

### The Cowork Agent for Everything. Train from Zero. Run Everywhere.

[English](./README.md) | [中文](./locales/zh/README.md) | [Русский](./locales/ru/README.md) | [Italiano](./locales/it/README.md) | [Español](./locales/es/README.md)

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**Train your own advertising AI from scratch. 2 hours. One GPU. Your data.**

The hello world of domain-specific agent training — for practitioners, by a practitioner.

42k+ stars on the base model ([minimind](https://github.com/jingyaogong/minimind)) · 14 ad platforms · 29 MCP tools · 5 Claude Code skills · One repo.

</div>

---

## What Is This?

MiniAgent is three things in one repo:

1. **A trainable advertising AI** — Fork of [minimind](https://github.com/jingyaogong/minimind) (Apache 2.0, 42k stars) retrained on advertising domain data. 26M-104M parameters. Train it yourself in 28 minutes on a single GPU for ~$0.13. Trained models: [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M). The model learns GAQL, campaign structure, bid strategy, PPC math, cross-platform terminology, and creative analysis across 60+ advertising platforms.

2. **A production MCP server ecosystem** — 14 ad platform connectors (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, Criteo, AdRoll, TikTok, Snapchat, Pinterest, Quora, X/Twitter) with 80+ tools, all pip-installable.

3. **An agent skills platform** — Claude Code skills, Codex skills, Gemini CLI skills for advertising analysis, auditing, safe write operations, PPC math, and cross-platform reporting.

**Built by a 15-year enterprise paid media practitioner managing $48M+ annual ad spend.**

---

## Quick Start

### Option 1: Use the pre-trained advertising model (no GPU needed)

**Trained models on HuggingFace:**
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104M params, minimind base + advertising domain (recommended)
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 26M params, trained from scratch

```bash
# One command — download and run
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Model downloaded! See README for usage.')
"
```

### Training Results (v0.1 — March 2026)

The 104M model was trained using **combined mode**: minimind's pretrained base (general language) + advertising domain pretraining (165 unique texts across 60+ platforms) + SFT (58 instruction-response pairs from practitioner expertise).

```
Training Pipeline:
  Base model:    minimind MiniMind2 (104M params, pretrained on billions of tokens)
  + Pretrain:    165 unique advertising texts × 150 repeats = 24,750 samples
                 Covering: Google, Meta, Microsoft, Amazon, LinkedIn, TikTok,
                 Snapchat, Pinterest, Reddit, The Trade Desk, Criteo, DV360,
                 Taboola, Outbrain, Walmart Connect, Roku, AppsFlyer, GA4, GTM...
  + SFT:         58 unique Q&A pairs × 80 repeats = 4,640 samples
                 Covering: PPC math, GAQL queries, audits, cross-platform strategy,
                 conversion tracking, bid strategy, campaign structure, diagnostics
  Hardware:      NVIDIA RTX 4000 Ada (20GB VRAM)
  Time:          28 minutes total ($0.13 cloud cost)
  Pretrain loss: 13.18 → 0.023 (3 epochs)
  SFT loss:      6.57 → 0.011 (5 epochs)
```

> **Current quality**: The model has absorbed advertising vocabulary and concepts (CPA, ROAS, GAQL, impression share, bid strategies, platform terminology). Output coherence is limited at this model size with current training data volume — this is a v0.1 proof of concept. Each training iteration with more data will improve quality. See the [Training Data](#training-data) section to contribute.

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### Option 2: Install MCP servers (connect to real ad accounts)

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# All platforms
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### Option 3: Install Claude Code skills (no API needed)

```bash
# Plugin marketplace
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Or manually
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### Option 4: Train your own model from scratch (2 hours, 1 GPU)

```bash
git clone https://github.com/itallstartedwithaidea/miniagent.git
cd miniagent
pip install -r requirements.txt

# Download advertising training data
python scripts/download_data.py

# Pretrain (learns advertising language)
python trainer/pretrain.py --dim 512 --n_layers 8

# SFT (learns to follow advertising instructions)
python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth

# LoRA fine-tune on YOUR account data (optional)
python trainer/lora.py --load_from ./checkpoints/sft_512.pth --data ./dataset/my_account.jsonl

# DPO alignment (learns good vs bad ad advice)
python trainer/dpo.py --load_from ./checkpoints/sft_512.pth
```

**Cost: ~$0.40 USD on a single 3090. 2 hours.**

---

## Architecture

```
MiniAgent
├── model/                    # Trainable LLM (fork of minimind)
│   ├── model_miniagent.py    # Decoder-only transformer (26M-145M params)
│   ├── LMConfig.py           # Model configuration
│   └── tokenizer/            # Custom advertising tokenizer
│
├── trainer/                  # Full training pipeline
│   ├── pretrain.py           # Stage 1: Learn advertising language
│   ├── sft.py                # Stage 2: Learn to follow instructions
│   ├── lora.py               # Stage 3: Fine-tune on YOUR data
│   ├── dpo.py                # Stage 4: Align with good PPC practices
│   ├── grpo.py               # Stage 5: Group relative policy optimization
│   └── distill.py            # Distill from Claude/GPT into MiniAgent
│
├── mcp/                      # MCP servers (14 platforms)
│   ├── google_ads/           # 29 tools — campaign, keyword, audit, write
│   ├── meta_ads/             # 18 tools — campaign, creative, audience
│   ├── microsoft_ads/        # 15 tools — campaign, keyword, UET
│   ├── amazon_ads/           # 12 tools — SP, SB, SD campaigns
│   ├── reddit_ads/           # 8 tools — campaign, targeting, creative
│   ├── tradedesk/            # 10 tools — campaign, inventory, audience
│   ├── linkedin_ads/         # 10 tools — campaign, targeting, conversion
│   ├── criteo/               # 8 tools
│   ├── adroll/               # 8 tools
│   ├── tiktok/               # 10 tools
│   ├── snapchat/             # 8 tools
│   ├── pinterest/            # 8 tools
│   ├── quora/                # 6 tools
│   └── twitter/              # 8 tools
│
├── skills/                   # Agent skills (Claude Code, Codex, Gemini CLI)
│   ├── google-ads-analysis/  # Campaign performance analysis
│   ├── google-ads-audit/     # 7-dimension account audit
│   ├── google-ads-write/     # Safe write ops (CEP protocol)
│   ├── google-ads-math/      # PPC calculations & forecasting
│   └── google-ads-mcp/       # MCP server setup guide
│
├── hub/                      # Advertising Hub — 14 platform connectors
│   ├── google/               # Google Ads API v23 connector
│   ├── meta/                 # Meta Marketing API connector
│   ├── microsoft/            # Microsoft Ads API connector
│   ├── amazon/               # Amazon Ads API connector
│   ├── reddit/               # Reddit Ads API connector
│   ├── tradedesk/            # TradeDesk API connector
│   ├── linkedin/             # LinkedIn Marketing API connector
│   ├── criteo/               # Criteo API connector
│   ├── adroll/               # AdRoll API connector
│   ├── tiktok/               # TikTok Business API connector
│   ├── snapchat/             # Snapchat Marketing API connector
│   ├── pinterest/            # Pinterest Ads API connector
│   ├── quora/                # Quora Ads API connector
│   └── twitter/              # X Ads API connector
│
├── eval/                     # Benchmarks & evaluation
│   ├── advertising_bench.py  # PPC-specific evaluation suite
│   ├── gaql_eval.py          # GAQL query accuracy
│   ├── campaign_structure.py # Campaign structure assessment
│   └── cross_platform.py     # Cross-platform normalization accuracy
│
├── scripts/                  # Utilities
│   ├── download_data.py      # Download training datasets
│   ├── convert_model.py      # Convert between torch/transformers/GGUF
│   ├── serve_openai_api.py   # OpenAI-compatible API server
│   ├── web_demo.py           # Streamlit chat demo
│   └── one_click_install.sh  # One-click full installation
│
├── dataset/                  # Training data (advertising domain)
│   ├── pretrain_ads.jsonl    # Advertising knowledge corpus
│   ├── sft_ads.jsonl         # Instruction-following for PPC tasks
│   ├── dpo_ads.jsonl         # Good vs bad advertising advice pairs
│   └── gaql_pairs.jsonl      # GAQL query-response pairs
│
├── docs/                     # Documentation
│   ├── wiki/                 # Full wiki (38+ pages)
│   └── architecture/         # Architecture decision records
│
├── locales/                  # Translations
│   ├── zh/README.md          # 中文
│   ├── ru/README.md          # Русский
│   ├── it/README.md          # Italiano
│   └── es/README.md          # Español
│
├── .claude/commands/         # Claude Code slash commands
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Claude Code project instructions
├── pyproject.toml            # pip installable
└── README.md                 # This file (English)
```

---

## What the Model Learns

### Stage 1: Pretrain (Advertising Language)
The model reads millions of tokens of advertising knowledge — Google Ads documentation, campaign management best practices, PPC industry content, GAQL syntax, cross-platform terminology. After pretraining, it can complete sentences like:

> **Input:** "A search impression share of 65% with budget lost impression share of 20% means"
> **Output:** "the campaign is losing 20% of eligible impressions due to insufficient daily budget. Increasing the daily budget or narrowing geo-targeting would recover this share."

### Stage 2: SFT (Instruction Following)
The model learns to follow advertising instructions:

> **User:** "Audit this Google Ads account. CPA is $45, target is $30, impression share is 40%."
> **MiniAgent:** "Three issues: 1) CPA is 50% above target — check search terms report for irrelevant queries eating budget. 2) 40% impression share means you're missing 60% of eligible auctions — either budget is too low or Quality Score needs improvement. 3) Recommend: add negative keywords, pause low-performing ad groups, increase bids on top converters only."

### Stage 3: DPO Alignment (Good vs Bad Advice)
The model learns to prefer good PPC advice over bad:

> **Good:** "Start with exact match keywords for high-intent terms, then expand to phrase match after 2 weeks of data."
> **Bad:** "Use broad match on everything to maximize volume."

---

## MCP Servers

Every platform is a separate MCP server, pip-installable:

| Platform | Install | Tools | Status |
|----------|---------|-------|--------|
| Google Ads | `pip install miniagent[google]` | 29 | ✅ Production |
| Meta Ads | `pip install miniagent[meta]` | 18 | ✅ Production |
| Microsoft Ads | `pip install miniagent[microsoft]` | 15 | 🔧 Beta |
| Amazon Ads | `pip install miniagent[amazon]` | 12 | 🔧 Beta |
| Reddit Ads | `pip install miniagent[reddit]` | 8 | 🔧 Beta |
| TradeDesk | `pip install miniagent[tradedesk]` | 10 | 🔧 Beta |
| LinkedIn Ads | `pip install miniagent[linkedin]` | 10 | 🔧 Beta |
| TikTok Ads | `pip install miniagent[tiktok]` | 10 | 📋 Planned |
| All platforms | `pip install miniagent[all]` | 80+ | — |

### Claude Code Integration

```json
{
  "mcpServers": {
    "miniagent-google": {
      "command": "python",
      "args": ["-m", "miniagent.mcp.google_ads"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your-token",
        "GOOGLE_ADS_CLIENT_ID": "your-client-id",
        "GOOGLE_ADS_CLIENT_SECRET": "your-secret",
        "GOOGLE_ADS_REFRESH_TOKEN": "your-refresh-token"
      }
    },
    "miniagent-meta": {
      "command": "python",
      "args": ["-m", "miniagent.mcp.meta_ads"],
      "env": {
        "META_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

### Cursor / Windsurf / OpenAI Agents SDK

```bash
# Cursor — add to .cursor/mcp.json (same format as above)
# Windsurf — add to .windsurf/mcp.json
# OpenAI Agents SDK:
from agents import Agent
from agents.mcp import MCPServerStdio

server = MCPServerStdio(command="python", args=["-m", "miniagent.mcp.google_ads"])
agent = Agent(name="ad-agent", mcp_servers=[server])
```

---

## Agent Skills

Skills work with Claude Code, Codex, Gemini CLI, Cursor, and any agent supporting the SKILL.md standard.

| Skill | Description | Needs API? |
|-------|-------------|-----------|
| `google-ads-analysis` | Campaign performance analysis, GAQL patterns, anomaly detection | Yes (via MCP) |
| `google-ads-audit` | 7-dimension account audit with severity ratings, 30/60/90-day plans | Yes (via MCP) |
| `google-ads-write` | Safe writes using Confirm-Execute-Postcheck (CEP) protocol | Yes (via MCP) |
| `google-ads-math` | PPC calculations — CPA, ROAS, budget projections, break-even | No |
| `google-ads-mcp` | MCP server setup guide for live API access | Setup guide |

```bash
# Claude Code
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Codex
cp -r skills/ ~/.codex/skills/miniagent/

# Gemini CLI
cp -r skills/ ~/.gemini/skills/miniagent/
```

---

## Training Data

All training data is open-source and advertising-domain specific:

| Dataset | Description | Size | Stage |
|---------|-------------|------|-------|
| `pretrain_ads.jsonl` | Advertising knowledge corpus — Google Ads docs, PPC best practices, industry content | ~500MB | Pretrain |
| `sft_ads.jsonl` | Instruction-response pairs for PPC tasks | ~50MB | SFT |
| `sft_gaql.jsonl` | GAQL query pairs — natural language → GAQL | ~10MB | SFT |
| `dpo_ads.jsonl` | Good vs bad advertising advice pairs | ~20MB | DPO |
| `distill_ads.jsonl` | Distilled from Claude/GPT on advertising tasks | ~100MB | Distill |

```bash
# Download all datasets
python scripts/download_data.py --all

# Or specific stages
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## Evaluation Benchmarks

MiniAgent includes advertising-specific benchmarks (no existing LLM benchmarks test PPC knowledge):

| Benchmark | What It Tests | Metrics |
|-----------|--------------|---------|
| **Ad-Bench** | General advertising knowledge | Accuracy, F1 |
| **GAQL-Eval** | GAQL query generation accuracy | Exact match, semantic match |
| **Campaign-Struct** | Campaign structure recommendations | Expert agreement score |
| **Cross-Platform** | Metric normalization across platforms | Consistency score |
| **Audit-Eval** | Account audit quality | Coverage, actionability, accuracy |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## One-Click Install

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

This installs everything: Python dependencies, model weights, MCP servers, Claude Code skills, and runs the Streamlit demo.

---

## Compatibility

| Platform | Status | How |
|----------|--------|-----|
| Claude Code | ✅ | Skills + MCP servers |
| Claude Desktop | ✅ | MCP servers via config |
| Cursor | ✅ | MCP servers + .cursor/mcp.json |
| Windsurf | ✅ | MCP servers |
| OpenAI Codex | ✅ | Skills in .codex/skills/ |
| Gemini CLI | ✅ | Skills in .gemini/skills/ |
| OpenAI Agents SDK | ✅ | MCPServerStdio |
| LangChain | ✅ | langchain-mcp-adapters |
| Ollama | ✅ | ollama run miniagent |
| vLLM | ✅ | vllm serve |
| llama.cpp | ✅ | GGUF conversion included |
| FastGPT | ✅ | OpenAI-compatible API |
| Open-WebUI | ✅ | OpenAI-compatible API |
| Dify | ✅ | OpenAI-compatible API |

---

## Attribution

This project builds on the work of many open-source contributors:

| Project | Author | License | Contribution |
|---------|--------|---------|-------------|
| [minimind](https://github.com/jingyaogong/minimind) | JingyaoGong | Apache 2.0 | Base model architecture, training pipeline, tokenizer framework |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) | Ernesto Cohnen | MIT | OAuth token persistence, customer ID normalization |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | Google LLC | Apache 2.0 | Singleton coordinator pattern, field_mask output |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) | Google LLC | Apache 2.0 | omit_unselected_resource_names, doc tools as MCP tools |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | GoMarble AI | MIT | MCC traversal, Keyword Planner, dual transport |
| [garrytan/gstack](https://github.com/garrytan/gstack) | Garry Tan | MIT | Skill architecture patterns, role-based agent design |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Steph Ango | MIT | SKILL.md standard, multi-platform skill format |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic | Apache 2.0 | Skills framework, plugin marketplace protocol |

---

## Ecosystem

MiniAgent is part of a larger open-source advertising intelligence ecosystem:

| Repo | What It Does |
|------|-------------|
| **miniagent** (this repo) | Everything — trainable model + MCP servers + skills + hub |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) | Standalone Google Ads MCP (29 tools) |
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Standalone Claude Code skills for Google Ads |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | 14-platform horizontal connector |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) | Full Google Ads agent with FastAPI |
| [creative-asset-validator](https://github.com/itallstartedwithaidea/creative-asset-validator) | AI-powered creative analysis across 50+ platforms |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) | Context intelligence platform (6 cognitive primitives) |
| [writing-agent](https://github.com/itallstartedwithaidea/writing-agent) | Ghost Protocol for human-quality content |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | 42-page agent crash course (MIT) |
| [agency-agents](https://github.com/itallstartedwithaidea/agency-agents) | Complete AI agency — frontend to community |

---

## License

Apache 2.0 — same as minimind. See [LICENSE](LICENSE).

---

## Author

**John Williams** · Senior Paid Media Specialist · [Seer Interactive](https://seerinteractive.com)
Founder, [googleadsagent.ai](https://googleadsagent.ai) · [It All Started With A Idea](https://itallstartedwithaidea.com)

15+ years managing enterprise digital advertising ($48M+ annual spend) across Google, Meta, Microsoft, Amazon.
Speaker: Hero Conf · Published: Search Engine Land · Built for the practitioner the platform forgot.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)

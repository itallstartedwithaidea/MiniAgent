<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

[English](./README.md) | [Français](./README.fr.md) | [Español](./README.es.md) | [中文](./README.zh.md) | [Nederlands](./README.nl.md) | [Русский](./README.ru.md) | [한국어](./README.ko.md) | [Italiano](./locales/it/README.md)

### 适用于一切的 Cowork 代理。从零训练，随处运行。

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**从头开始训练你自己的广告人工智能。 2小时。一个 GPU。您的数据。**

特定领域代理培训的你好世界——为从业者提供，由从业者进行。

基础模型上有 42k+ 星 ([minimind](https://github.com/jingyaogong/minimind)) · 14 个广告平台 · 29 个 MCP 工具 · 5 个 Claude 代码技能 · 一个仓库。

</div>

---

## 这是什么？

MiniAgent 在一个存储库中包含三件事：

1. **可训练的广告人工智能** - [minimind](https://github.com/jingyaogong/minimind) 的分支 (Apache 2.0, 42k star) 在广告领域数据上进行再训练。 26M-104M参数。只需 28 分钟即可在单个 GPU 上自行训练，费用约为 0.13 美元。训练模型：[MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M)。该模型可学习 GAQL、广告系列结构、出价策略、PPC 数学、跨平台术语以及 60 多个广告平台的创意分析。

2. **生产 MCP 服务器生态系统** — 14 个广告平台连接器（Google、Meta、Microsoft、Amazon、Reddit、TradeDesk、LinkedIn、Criteo、AdRoll、TikTok、Snapchat、Pinterest、Quora、X/Twitter）以及 80 多种工具，全部可通过 pip 安装。

3. **代理技能平台** — 用于广告分析、审计、安全写入操作、PPC 数学和跨平台报告的 Claude Code 技能、Codex 技能、Gemini CLI 技能。

**由一位拥有 15 年经验的企业付费媒体从业者打造，管理着每年超过 4800 万美元的广告支出。**

---

## 快速入门

### 选项 1：使用预先训练的广告模型（无需 GPU）

**在 HuggingFace 上训练的模型：**
- [MiniAgent-494M](https://huggingface.co/itallstartedwithaidea/MiniAgent-494M) — 494M 参数，Qwen2.5-0.5B 多语言库 + 广告域（推荐，29+ 语言）
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104M 参数，minimind 基础 + 广告域
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 26M 参数，从头开始训练```bash
# One command — download and run
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Model downloaded! See README for usage.')
"
```

### 培训结果（v0.1 - 2026 年 3 月）

104M 模型使用**组合模式**进行训练：minimind 的预训练基础（通用语言）+ 广告领域预训练（跨 60 多个平台的 165 个独特文本）+ SFT（来自从业者专业知识的 58 个指令-响应对）。

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

> **当前质量**：该模型吸收了广告词汇和概念（CPA、ROAS、GAQL、展示份额、出价策略、平台术语）。在此模型大小和当前训练数据量下，输出一致性受到限制——这是 v0.1 概念证明。每次使用更多数据的训练迭代都会提高质量。请参阅[训练数据](#training-data) 部分进行贡献。

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### 选项 2：安装 MCP 服务器（连接到真实广告帐户）

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# All platforms
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### 选项 3：安装 Claude Code 技能（无需 API）

```bash
# Plugin marketplace
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Or manually
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### 选项 4：从头开始训练您自己的模型（2 小时，1 个 GPU）

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

**成本：单个 3090 约 0.40 美元。2 小时。**

---

## 架构

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
├── mcp_servers/               # MCP servers (14 platforms)
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
│   # 根目录另有：README.fr.md、README.es.md、README.zh.md、README.nl.md、README.ru.md、README.ko.md
├── .claude/commands/         # Claude Code slash commands
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Claude Code project instructions
├── pyproject.toml            # pip installable
└── README.zh.md              # 本文件（简体中文）
```

---

## 模型学到了什么

### 第 1 阶段：预训练（广告语言）
该模型读取数以百万计的广告知识——Google Ads 文档、营销活动管理最佳实践、PPC 行业内容、GAQL 语法、跨平台术语。经过预训练后，它可以完成如下句子：

> **输入：**“搜索印象份额为 65%，预算损失印象份额为 20% 意味着”
> **输出：**“由于每日预算不足，广告系列失去了 20% 的合格展示次数。增加每日预算或缩小地理定位将恢复这一份额。”

### 第 2 阶段：SFT（遵循指令）
该模型学习遵循广告指令：

> **用户：**“审核此 Google Ads 帐户。每次转化费用为 45 美元，目标为 30 美元，展示次数份额为 40%。”
> **MiniAgent：** “三个问题：1) 每次转化费用比目标高出 50% - 检查搜索字词报告，了解是否存在消耗预算的不相关查询。2) 40% 的展示次数份额意味着您错过了 60% 的合格拍卖 - 要么预算太低，要么质量得分需要改进。3) 建议：添加否定关键字，暂停效果不佳的广告组，仅提高对顶级转化者的出价。”

### 第 3 阶段：DPO 调整（好的建议与坏的建议）
该模型学会了更喜欢好的 PPC 建议而不是坏的建议：

> **好：**“从高意图术语的精确匹配关键字开始，然后在 2 周的数据后扩展到短语匹配。”
> **不好：**“对所有内容都使用广泛匹配以最大化音量。”

---

## MCP 服务器

每个平台都是一个单独的 MCP 服务器，可通过 pip 安装：

|平台|安装 |工具|状态 |
|----------|---------|--------|--------|
|谷歌广告 | `pip install miniagent[google]` | 29 | 29 ✅ 生产 |
|元广告 | `pip install miniagent[meta]` | 18 | 18 ✅ 生产 |
|微软广告| `pip install miniagent[microsoft]` | 15 | 15 🔧 测试版 |
|亚马逊广告 | `pip install miniagent[亚马逊]` | 12 | 12 🔧 测试版 |
| Reddit 广告 | `pip install miniagent[reddit]` | 8 | 🔧 测试版 |
|贸易台| `pip install miniagent[tradedesk]` | 10 | 10 🔧 测试版 |
|领英广告 | `pip install miniagent[linkedin]` | 10 | 10 🔧 测试版 |
| TikTok 广告 | `pip install miniagent[tiktok]` | 10 | 10 📋 计划 |
|全平台 | `pip install miniagent[全部]` | 80+ | — |

### 克劳德代码集成

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

### 光标/Windsurf/OpenAI Agents SDK

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

## 代理技能

技能可与 Claude Code、Codex、Gemini CLI、Cursor 以及任何支持 SKILL.md 标准的代理配合使用。

|技能|描述 |需要API吗？ |
|--------|-------------|------------|
| `谷歌广告分析` |营销活动绩效分析、GAQL 模式、异常检测 |是（通过 MCP）|
| `Google 广告审核` | 7 维帐户审计，包括严重性评级、30/60/90 天计划 |是（通过 MCP）|
| `google-ads-write` |使用确认执行后检查 (CEP) 协议进行安全写入 |是（通过 MCP）|
| `Google 广告数学` | PPC 计算 — CPA、ROAS、预算预测、收支平衡 |没有 |
| `google-ads-mcp` |用于实时 API 访问的 MCP 服务器设置指南 |设置指南 |

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

## 训练数据

所有训练数据都是开源的并且特定于广告领域：

|数据集 |描述 |尺寸|舞台|
|--------|-------------|------|--------|
| `pretrain_ads.jsonl` |广告知识库——Google Ads 文档、PPC 最佳实践、行业内容 | 〜500MB |预训练 |
| `sft_ads.jsonl` | PPC 任务的指令-响应对 | 〜50MB |斯夫特 |
| `sft_gaql.jsonl` | GAQL 查询对 — 自然语言 → GAQL | 〜10MB |斯夫特 |
| `dpo_ads.jsonl` |好与坏的广告建议对| 〜20MB |数据保护官 |
| `distill_ads.jsonl` |从 Claude/GPT 的广告任务中提炼出来 | 〜100MB |蒸馏|

```bash
# Download all datasets
python scripts/download_data.py --all

# Or specific stages
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## 评估基准

MiniAgent 包括特定于广告的基准（没有现有的 LLM 基准测试 PPC 知识）：

|基准|它测试什么 |指标|
|------------|--------------|---------|
| **广告台** |广告常识|准确度，F1 |
| **GAQL-评估** | GAQL 查询生成准确性 |精准匹配、语义匹配 |
| **活动结构** |活动结构建议|专家一致评分|
| **跨平台** |跨平台指标标准化 |一致性得分 |
| **审核评估** |账户审核质量 |覆盖范围、可操作性、准确性 |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## 一键安装

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

这将安装所有内容：Python 依赖项、模型权重、MCP 服务器、Claude Code 技能，并运行 Streamlit 演示。

---

## 兼容性

|平台|状态 |如何|
|----------|--------|-----|
|克劳德·代码 | ✅ |技能+MCP服务器|
|克劳德桌面| ✅ | MCP 服务器通过配置 |
|光标| ✅ | MCP 服务器 + .cursor/mcp.json |
|风帆冲浪 | ✅ | MCP 服务器 |
| OpenAI 法典 | ✅ | .codex/skills/ 中的技能 |
|双子座 CLI | ✅ | .gemini/skills/ 中的技能 |
| OpenAI 代理 SDK | ✅ | MCP服务器工作室 |
|浪链 | ✅ | langchain-mcp-适配器 |
|奥拉玛 | ✅ | ollama 运行 miniagent |
|法学硕士 | ✅ | vllm 服务 |
|骆驼.cpp | ✅ |包括 GGUF 转换 |
|快速GPT | ✅ | OpenAI 兼容 API |
|开放式WebUI | ✅ | OpenAI 兼容 API |
|迪迪 | ✅ | OpenAI 兼容 API |

---

## 归因

该项目建立在许多开源贡献者的工作基础上：

|项目|作者 |许可证|贡献 |
|--------|--------|---------|------------|
| [minimind](https://github.com/jingyaogong/minimind) |敬耀宫|阿帕奇2.0 |基础模型架构、训练管道、分词器框架 |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) |埃内斯托·科南 |麻省理工学院 | OAuth 令牌持久化、客户 ID 规范化 |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) |谷歌有限责任公司|阿帕奇2.0 |单例协调器模式，field_mask 输出 |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) |谷歌有限责任公司|阿帕奇2.0 | omit_unselected_resource_names，文档工具作为 MCP 工具 |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | GoMarble 人工智能 |麻省理工学院 | MCC遍历、关键词规划、双重传输|
| [garrytan/gstack](https://github.com/garrytan/gstack) |加里·谭 |麻省理工学院 |技能架构模式、基于角色的代理设计 |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |斯蒂芬·安戈 |麻省理工学院 | SKILL.md 标准、多平台技能格式 |
| [anthropics/skills](https://github.com/anthropics/skills) |人择 |阿帕奇2.0 |技能框架、插件市场协议 |

---

## 生态系统

MiniAgent 是更大的开源广告智能生态系统的一部分：

|回购|它有什么作用 |
|------|-------------|
| **miniagent**（此存储库）|一切 — 可训练模型 + MCP 服务器 + 技能 + 中心 |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) |独立 Google Ads MCP（29 种工具）|
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Google Ads 的独立 Claude 代码技能 |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | 14平台水平连接器 |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) |具有 FastAPI 的完整 Google Ads 代理 |
| [创意资产验证器](https://github.com/itallstartedwithaidea/creative-asset-validator) |跨 50 多个平台的 AI 支持创意分析 |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) |情境智能平台（6 个认知原语）|
| [写作代理](https://github.com/itallstartedwithaidea/writing-agent) |面向人类品质内容的 Ghost 协议 |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | 42 页特工速成课程（麻省理工学院） |
| [代理代理](https://github.com/itallstartedwithaidea/agency-agents) |完整的人工智能机构——前端到社区|

---

## 许可证

Apache 2.0 — 与 minimind 相同。参见 [LICENSE](LICENSE)。

---

## 作者

**John Williams** · 高级付费媒体专家 · [Seer Interactive](https://seerinteractive.com)
[googleadsagent.ai](https://googleadsagent.ai) 创始人 · [It All Started With A Idea](https://itallstartedwithaidea.com)

拥有 15 年以上管理 Google、Meta、Microsoft、Amazon 企业数字广告经验（年支出超过 4800 万美元）的经验。
演讲者：Hero Conf · 发布：Search Engine Land · 为遗忘者打造的平台。

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)
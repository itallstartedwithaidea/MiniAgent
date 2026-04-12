<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

[English](./README.md) | [Français](./README.fr.md) | [Español](./README.es.md) | [中文](./README.zh.md) | [Nederlands](./README.nl.md) | [Русский](./README.ru.md) | [한국어](./README.ko.md) | [Italiano](./locales/it/README.md)

### 모든 것을 위한 Cowork 에이전트. 제로부터 학습, 어디서나 실행.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**처음부터 자신만의 광고 AI를 훈련하세요. 2시간. GPU 1개. 귀하의 데이터.**

실무자를 위한, 실무자에 의한 도메인별 에이전트 교육의 세계입니다.

기본 모델의 별 42,000개 이상([minimind](https://github.com/jingyaogong/minimind)) · 14개의 광고 플랫폼 · 29개의 MCP 도구 · 5개의 Claude Code 기술 · 하나의 저장소.

</div>

## 이것은 무엇입니까?

MiniAgent는 하나의 저장소에 다음 세 가지 기능을 포함합니다.

1. **훈련 가능한 광고 AI** — [minimind](https://github.com/jingyaogong/minimind)(Apache 2.0, 42,000개 별)의 포크가 광고 도메인 데이터에 대해 재훈련되었습니다. 26M-104M 매개변수. ~$0.13의 비용으로 단일 GPU에서 28분 만에 직접 훈련하세요. 훈련된 모델: [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M). 이 모델은 60개 이상의 광고 플랫폼에 걸쳐 GAQL, 캠페인 구조, 입찰 전략, PPC 수학, 크로스 플랫폼 용어 및 창의적 분석을 학습합니다.

2. **프로덕션 MCP 서버 에코시스템** — 80개 이상의 도구가 포함된 14개의 광고 플랫폼 커넥터(Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, Criteo, AdRoll, TikTok, Snapchat, Pinterest, Quora, X/Twitter), 모두 pip 설치 가능.

3. **에이전트 기술 플랫폼** — Claude Code 기술, Codex 기술, 광고 분석, 감사, 안전한 쓰기 작업, PPC 수학 및 교차 플랫폼 보고를 위한 Gemini CLI 기술.

**연간 4,800만 달러 이상의 광고 지출을 관리하는 15년 경력의 기업 유료 미디어 실무자가 구축했습니다.**

---

## 빠른 시작

### 옵션 1: 사전 학습된 광고 모델 사용(GPU 필요 없음)

**HuggingFace에서 훈련된 모델:**
- [MiniAgent-494M](https://huggingface.co/itallstartedwithaidea/MiniAgent-494M) — 494M 매개변수, Qwen2.5-0.5B 다국어 기반 + 광고 도메인(권장, 29개 이상의 언어)
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104M 매개변수, 최소 마인드 기반 + 광고 도메인
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 처음부터 훈련된 26M 매개변수```bash
# One command — download and run
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Model downloaded! See README for usage.')
"
```

### 교육 결과(v0.1 — 2026년 3월)

104M 모델은 **결합 모드**를 사용하여 학습되었습니다. minimind의 사전 학습된 기본(일반 언어) + 광고 도메인 사전 학습(60개 이상의 플랫폼에 걸친 165개의 고유 텍스트) + SFT(실무자 전문 지식의 58개 지시-응답 쌍).

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

> **현재 품질**: 모델은 광고 용어 및 개념(CPA, ROAS, GAQL, 노출 점유율, 입찰 전략, 플랫폼 용어)을 흡수했습니다. 출력 일관성은 현재 교육 데이터 볼륨으로 인해 이 모델 크기로 제한됩니다. 이는 v0.1 개념 증명입니다. 더 많은 데이터를 사용하여 훈련을 반복할 때마다 품질이 향상됩니다. 기여하려면 [훈련 데이터](#training-data) 섹션을 참조하세요.

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### 옵션 2: MCP 서버 설치(실제 광고 계정에 연결)

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# All platforms
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### 옵션 3: Claude Code 기술 설치(API 필요 없음)

```bash
# Plugin marketplace
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Or manually
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### 옵션 4: 처음부터 자신만의 모델 학습(2시간, 1 GPU)

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

**비용: 단일 3090에서 ~$0.40 USD. 2시간.**

---

## 아키텍처

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
│   # 루트에도 제공: README.fr.md, README.es.md, README.zh.md, README.nl.md, README.ru.md, README.ko.md
├── .claude/commands/         # Claude Code slash commands
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Claude Code project instructions
├── pyproject.toml            # pip installable
└── README.ko.md              # 이 파일 (한국어)
```

---

## 모델이 학습하는 것

### 1단계: 사전 학습(광고 언어)
이 모델은 Google Ads 문서, 캠페인 관리 모범 사례, PPC 업계 콘텐츠, GAQL 구문, 크로스 플랫폼 용어 등 수백만 개의 광고 지식 토큰을 읽습니다. 사전 훈련 후에는 다음과 같은 문장을 완성할 수 있습니다.

> **입력:** "예산 손실 노출 점유율이 20%이고 검색 노출 점유율이 65%라는 의미는"
> **출력:** "일일예산 부족으로 인해 캠페인에서 적격 노출수의 20%가 손실되고 있습니다. 일일예산을 늘리거나 지역 타겟팅을 좁히면 이 점유율을 회복할 수 있습니다."

### 2단계: SFT(지침 따르기)
모델은 광고 지침을 따르는 방법을 학습합니다.

> **사용자:** "이 Google Ads 계정을 감사하세요. CPA는 45달러, 타겟은 30달러, 노출 점유율은 40%입니다."
> **MiniAgent:** "3가지 문제: 1) CPA가 목표보다 50% 높습니다. 예산을 소모하는 관련 없는 검색어가 있는지 검색어 보고서를 확인하세요. 2) 노출 점유율이 40%라는 것은 적격한 경매의 60%를 놓치고 있다는 뜻입니다. 예산이 너무 낮거나 품질평가점수를 개선해야 합니다. 3) 권장사항: 제외 키워드 추가, 실적이 저조한 광고그룹 일시중지, 상위 전환자에 대해서만 입찰가 높이기."

### 3단계: DPO 정렬(좋은 조언과 나쁜 조언)
모델은 나쁜 PPC 조언보다 좋은 PPC 조언을 선호하는 방법을 학습합니다.

> **좋음:** "의도가 높은 용어에 대해서는 일치검색 키워드로 시작한 다음 2주 동안 데이터를 수집한 후 구문검색으로 확장합니다."
> **나쁨:** "검색량을 최대화하려면 모든 항목에 확장검색을 사용하세요."

---

## MCP 서버

모든 플랫폼은 pip 설치가 가능한 별도의 MCP 서버입니다.

| 플랫폼 | 설치 | 도구 | 상태 |
|----------|---------|-------|--------|
| 구글 광고 | `pip install miniagent[google]` | 29 | ✅ 생산 |
| 메타 광고 | `pip install miniagent[meta]` | 18 | ✅ 생산 |
| 마이크로소프트 광고 | `pip install miniagent[microsoft]` | 15 | 🔧 베타 |
| 아마존 광고 | `pip install miniagent[amazon]` | 12 | 🔧 베타 |
| 레딧 광고 | `pip install miniagent[reddit]` | 8 | 🔧 베타 |
| 트레이드데스크 | `pip install miniagent[tradedesk]` | 10 | 🔧 베타 |
| 링크드인 광고 | `pip install miniagent[linkedin]` | 10 | 🔧 베타 |
| 틱톡 광고 | `pip install miniagent[tiktok]` | 10 | 📋 예정 |
| 모든 플랫폼 | `pip install miniagent[모두]` | 80세 이상 | — |

### 클로드 코드 통합

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

### 커서/Windsurf/OpenAI 에이전트 SDK

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

## 상담원 기술

기술은 Claude Code, Codex, Gemini CLI, Cursor 및 SKILL.md 표준을 지원하는 모든 에이전트와 함께 작동합니다.

| 스킬 | 설명 | API가 필요합니까? |
|-------|-------------|----------|
| `google-ads-분석` | 캠페인 성과 분석, GAQL 패턴, 이상 징후 탐지 | 예(MCP를 통해) |
| `google-ads-audit` | 심각도 등급이 포함된 7차원 계정 감사, 30/60/90일 계획 | 예(MCP를 통해) |
| `google-ads-write` | CEP(Confirm-Execute-Postcheck) 프로토콜을 사용한 안전한 쓰기 | 예(MCP를 통해) |
| `google-ads-수학` | PPC 계산 — CPA, ROAS, 예산 예측, 손익분기점 | 아니요 |
| `google-ads-mcp` | 라이브 API 액세스를 위한 MCP 서버 설정 가이드 | 설정 가이드 |

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

## 훈련 데이터

모든 교육 데이터는 오픈 소스이며 광고 도메인에 따라 다릅니다.

| 데이터세트 | 설명 | 사이즈 | 무대 |
|---------|-------------|------|-------|
| `pretrain_ads.jsonl` | 광고 지식 자료 — Google Ads 문서, PPC 모범 사례, 업계 콘텐츠 | ~500MB | 사전 훈련 |
| `sft_ads.jsonl` | PPC 작업을 위한 명령-응답 쌍 | ~50MB | SFT |
| `sft_gaql.jsonl` | GAQL 쿼리 쌍 — 자연어 → GAQL | ~10MB | SFT |
| `dpo_ads.jsonl` | 좋은 광고 조언과 나쁜 광고 조언 쌍 | ~20MB | DPO |
| `distill_ads.jsonl` | 광고 업무에 관한 Claude/GPT에서 추출 | ~100MB | 증류 |

```bash
# Download all datasets
python scripts/download_data.py --all

# Or specific stages
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## 평가 벤치마크

MiniAgent에는 광고 관련 벤치마크가 포함되어 있습니다(기존 LLM 벤치마크는 PPC 지식을 테스트하지 않음).

| 벤치마크 | 테스트 내용 | 측정항목 |
|------------|---------------|---------|
| **애드벤치** | 일반 광고 지식 | 정확도, F1 |
| **GAQL 평가** | GAQL 쿼리 생성 정확도 | 정확한 일치, 의미적 일치 |
| **캠페인 구조** | 캠페인 구조 권장 사항 | 전문가 동의 점수 |
| **크로스 플랫폼** | 플랫폼 전반에 걸친 측정항목 정규화 | 일관성 점수 |
| **감사 평가** | 계정 감사 품질 | 적용 범위, 실행 가능성, 정확성 |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## 원클릭 설치

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

그러면 Python 종속성, 모델 가중치, MCP 서버, Claude Code 기술 등 모든 것이 설치되고 Streamlit 데모가 실행됩니다.

---

## 호환성

| 플랫폼 | 상태 | 어떻게 |
|----------|----------|------|
| 클로드 코드 | ✅ | 기술 + MCP 서버 |
| 클로드 데스크탑 | ✅ | 구성을 통한 MCP 서버 |
| 커서 | ✅ | MCP 서버 + .cursor/mcp.json |
| 윈드서핑 | ✅ | MCP 서버 |
| OpenAI 코덱스 | ✅ | .codex/skills/의 기술 |
| 제미니 CLI | ✅ | .gemini/skills/의 기술 |
| OpenAI 에이전트 SDK | ✅ | MCP서버스튜디오 |
| 랭체인 | ✅ | 랭체인-mcp-어댑터 |
| 올라마 | ✅ | 올라마 런 미니에이전트 |
| vLLM | ✅ | vllm 서브 |
| 라마.cpp | ✅ | GGUF 변환 포함 |
| 패스트GPT | ✅ | OpenAI 호환 API |
| 개방형 WebUI | ✅ | OpenAI 호환 API |
| 디파이 | ✅ | OpenAI 호환 API |

---

## 속성

이 프로젝트는 많은 오픈 소스 기여자의 작업을 기반으로 구축되었습니다.

| 프로젝트 | 작성자 | 라이센스 | 기여 |
|---------|---------|---------|-------------|
| [미니마인드](https://github.com/jingyaogong/minimind) | 징야오공 | 아파치 2.0 | 기본 모델 아키텍처, 훈련 파이프라인, 토크나이저 프레임워크 |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) | 에르네스토 코넨 | MIT | OAuth 토큰 지속성, 고객 ID 정규화 |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | 구글 LLC | 아파치 2.0 | 싱글톤 코디네이터 패턴, field_mask 출력 |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) | 구글 LLC | 아파치 2.0 | 생략_unselected_resource_names, 문서 도구를 MCP 도구로 |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | 고마블 AI | MIT | MCC 순회, 키워드 플래너, 이중 전송 |
| [garrytan/gstack](https://github.com/garrytan/gstack) | 게리 탄 | MIT | 스킬 아키텍처 패턴, 역할 기반 에이전트 설계 |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | 스테판 앙고 | MIT | SKILL.md 표준, 다중 플랫폼 기술 형식 |
| [인류학/기술](https://github.com/anthropics/skills) | 인류학 | 아파치 2.0 | 기술 프레임워크, 플러그인 마켓플레이스 프로토콜 |

---

## 생태계

MiniAgent는 대규모 오픈 소스 광고 인텔리전스 생태계의 일부입니다.

| 레포 | 그것이 하는 일 |
|------|-------------|
| **miniagent** (이 저장소) | 모든 것 - 훈련 가능한 모델 + MCP 서버 + 기술 + 허브 |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) | 독립형 Google Ads MCP(29개 도구) |
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Google Ads를 위한 독립형 Claude Code 기술 |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | 14플랫폼 수평 커넥터 |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) | FastAPI를 갖춘 전체 Google Ads 에이전트 |
| [creative-asset-validator](https://github.com/itallstartedwithaidea/creative-asset-validator) | 50개 이상의 플랫폼에 걸친 AI 기반 창의적 분석 |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) | 상황지능 플랫폼(6개 인지 프리미티브) |
| [writing-agent](https://github.com/itallstartedwithaidea/writing-agent) | 인간 수준의 콘텐츠를 위한 고스트 프로토콜 |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | 42페이지로 구성된 에이전트 집중 코스(MIT) |
| [agency-agents](https://github.com/itallstartedwithaidea/agency-agents) | 완전한 AI 에이전시 — 커뮤니티에 대한 프런트엔드 |

---

## 라이선스

Apache 2.0 — minimind와 동일합니다. [LICENSE](LICENSE)를 참조하세요.

---

## 작성자

**존 윌리엄스** · 수석 유료 미디어 전문가 · [Seer Interactive](https://seerinteractive.com)
창립자, [googleadsagent.ai](https://googleadsagent.ai) · [It All Started With A Idea](https://itallstartedwithaidea.com)

Google, Meta, Microsoft, Amazon 전반에서 기업 디지털 광고 관리(연간 지출 4,800만 달러 이상)를 15년 이상 담당했습니다.
발표자: Hero Conf · 게시: 검색 엔진 랜드 · 플랫폼이 잊어버린 실무자를 위해 구축되었습니다.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)
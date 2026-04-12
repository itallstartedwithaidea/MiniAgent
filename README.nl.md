<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

[English](./README.md) | [Français](./README.fr.md) | [Español](./README.es.md) | [中文](./README.zh.md) | [Nederlands](./README.nl.md) | [Русский](./README.ru.md) | [한국어](./README.ko.md) | [Italiano](./locales/it/README.md)

### De Cowork-agent voor alles. Train vanaf nul. Draai overal.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**Train uw eigen advertentie-AI helemaal opnieuw. 2 uur. Eén GPU. Jouw gegevens.**

De hallo wereld van domeinspecifieke agenttraining – voor beoefenaars, door een beoefenaar.

Meer dan 42.000 sterren op het basismodel ([minimind](https://github.com/jingyaogong/minimind)) · 14 advertentieplatforms · 29 MCP-tools · 5 Claude Code-vaardigheden · Eén opslagplaats.

</div>

## Wat is dit?

MiniAgent is drie dingen in één repository:

1. **Een trainbare advertentie-AI** — Fork van [minimind](https://github.com/jingyaogong/minimind) (Apache 2.0, 42k sterren) opnieuw getraind op advertentiedomeingegevens. 26M-104M-parameters. Train het zelf in 28 minuten op een enkele GPU voor ~$0,13. Getrainde modellen: [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M). Het model leert GAQL, campagnestructuur, biedstrategie, PPC-wiskunde, platformonafhankelijke terminologie en creatieve analyse op meer dan 60 advertentieplatforms.

2. **Een productie-MCP-server-ecosysteem** — 14 connectoren voor advertentieplatforms (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, Criteo, AdRoll, TikTok, Snapchat, Pinterest, Quora, X/Twitter) met meer dan 80 tools, allemaal pip-installeerbaar.

3. **Een platform voor agentvaardigheden** — Claude Code-vaardigheden, Codex-vaardigheden, Gemini CLI-vaardigheden voor advertentieanalyse, auditing, veilige schrijfbewerkingen, PPC-wiskunde en platformonafhankelijke rapportage.

**Gebouwd door een 15-jarige professionele betaalde mediaprofessional die jaarlijks meer dan $48 miljoen aan advertentie-uitgaven beheert.**

---

## Snelle start

### Optie 1: Gebruik het vooraf getrainde advertentiemodel (geen GPU nodig)

**Getrainde modellen op HuggingFace:**
- [MiniAgent-494M](https://huggingface.co/itallstartedwithaidea/MiniAgent-494M) — 494 miljoen params, Qwen2,5-0,5B meertalige basis + advertentiedomein (aanbevolen, 29+ talen)
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104 miljoen params, minimind-basis + advertentiedomein
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 26 miljoen params, helemaal opnieuw getraind```bash
# One command — download and run
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Model downloaded! See README for usage.')
"
```

### Trainingsresultaten (v0.1 — maart 2026)

Het 104M-model werd getraind met behulp van de **gecombineerde modus**: de voorgetrainde basis van minimind (algemene taal) + voortraining van het advertentiedomein (165 unieke teksten op meer dan 60 platforms) + SFT (58 instructie-antwoordparen vanuit de expertise van de praktijk).

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

> **Huidige kwaliteit**: het model heeft advertentiewoordenschat en -concepten geabsorbeerd (CPA, ROAS, GAQL, vertoningspercentage, biedstrategieën, platformterminologie). De outputcoherentie is beperkt bij deze modelgrootte met het huidige volume aan trainingsgegevens. Dit is een proof of concept v0.1. Elke trainingsiteratie met meer gegevens zal de kwaliteit verbeteren. Zie de sectie [Trainingsgegevens](#training-data) om een ​​bijdrage te leveren.

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### Optie 2: MCP-servers installeren (verbinding maken met echte advertentieaccounts)

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# All platforms
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### Optie 3: Claude Code-vaardigheden installeren (geen API nodig)

```bash
# Plugin marketplace
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Or manually
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### Optie 4: Train je eigen model helemaal opnieuw (2 uur, 1 GPU)

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

**Kosten: ~$0,40 USD voor een enkele 3090. 2 uur.**

---

## Architectuur

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
│   # Ook in de root: README.fr.md, README.es.md, README.zh.md, README.nl.md, README.ru.md, README.ko.md
├── .claude/commands/         # Claude Code slash commands
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Claude Code project instructions
├── pyproject.toml            # pip installable
└── README.nl.md              # Dit bestand (Nederlands)
```

---

## Wat het model leert

### Fase 1: Pretrain (reclametaal)
Het model leest miljoenen tokens aan advertentiekennis: Google Ads-documentatie, best practices voor campagnebeheer, PPC-industrie-inhoud, GAQL-syntaxis, platformonafhankelijke terminologie. Na de voortraining kan het zinnen voltooien als:

> **Invoer:** "Een zoekvertoningspercentage van 65% met een budgetverliespercentage van 20% betekent"
> **Output:** "de campagne verliest 20% van de in aanmerking komende vertoningen vanwege een onvoldoende dagbudget. Door het dagbudget te verhogen of de geografische targeting te beperken, kan dit aandeel worden hersteld."

### Fase 2: SFT (instructie volgt)
Het model leert reclame-instructies te volgen:

> **Gebruiker:** "Controleer dit Google Ads-account. CPA is $ 45, doel is $ 30, vertoningspercentage is 40%."
> **MiniAgent:** "Drie problemen: 1) CPA ligt 50% boven het doel - controleer het zoektermenrapport op irrelevante zoekopdrachten die budget opslokken. 2) Een vertoningspercentage van 40% betekent dat u 60% van de in aanmerking komende veilingen mist - het budget is te laag of de kwaliteitsscore moet worden verbeterd. 3) Aanbevelen: voeg uitsluitingszoekwoorden toe, onderbreek slecht presterende advertentiegroepen, verhoog biedingen alleen voor de beste converters."

### Fase 3: DPO-afstemming (goed versus slecht advies)
Het model leert om goed PPC-advies te verkiezen boven slecht:

> **Goed:** "Begin met exacte zoekwoorden voor termen met een hoge intentie, en breid vervolgens uit naar zoeken op woordgroep na twee weken aan gegevens."
> **Slecht:** "Gebruik brede zoekwoorden voor alles om het volume te maximaliseren."

---

## MCP-servers

Elk platform is een aparte MCP-server, pip-installeerbaar:

| Platform | Installeren | Gereedschap | Staat |
|----------|---------|-------|-------|
| Google-advertenties | `pip installeer miniagent[google]` | 29 | ✅ Productie |
| Meta-advertenties | `pip installeer miniagent[meta]` | 18 | ✅ Productie |
| Microsoft-advertenties | `pip installeer miniagent[microsoft]` | 15 | 🔧 Bèta |
| Amazon-advertenties | `pip installeer miniagent[amazon]` | 12 | 🔧 Bèta |
| Reddit-advertenties | `pip installeer miniagent[reddit]` | 8 | 🔧 Bèta |
| HandelDesk | `pip installeer miniagent[tradedesk]` | 10 | 🔧 Bèta |
| LinkedIn-advertenties | `pip installeer miniagent[linkedin]` | 10 | 🔧 Bèta |
| TikTok-advertenties | `pip installeer miniagent[tiktok]` | 10 | 📋 Gepland |
| Alle platforms | `pip installeer miniagent[all]` | 80+ | — |

### Claude Code-integratie

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

### Cursor/Windsurf/OpenAI Agents SDK

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

## Agentvaardigheden

Skills werken met Claude Code, Codex, Gemini CLI, Cursor en elke agent die de SKILL.md-standaard ondersteunt.

| Vaardigheid | Beschrijving | API nodig? |
|-------|------------|-----------|
| `google-ads-analyse` | Analyse van campagneprestaties, GAQL-patronen, detectie van afwijkingen | Ja (via MCP) |
| `google-ads-audit` | 7-dimensionale accountaudit met ernstclassificaties, plannen voor 30/60/90 dagen | Ja (via MCP) |
| `google-ads-schrijven` | Veilig schrijven met behulp van het CEP-protocol (Confirm-Execute-Postcheck) | Ja (via MCP) |
| `google-ads-wiskunde` | PPC-berekeningen — CPA, ROAS, budgetprognoses, break-even | Nee |
| `google-ads-mcp` | Installatiehandleiding voor MCP-server voor live API-toegang | Installatiehandleiding |

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

## Trainingsgegevens

Alle trainingsgegevens zijn open-source en advertentiedomeinspecifiek:

| Gegevensset | Beschrijving | Maat | Fase |
|---------|-------------|------|-------|
| `pretrain_ads.jsonl` | Kenniscorpus over adverteren — Google Ads-documenten, praktische tips voor PPC, branche-inhoud | ~500MB | Voortrainen |
| `sft_ads.jsonl` | Instructie-antwoordparen voor PPC-taken | ~50MB | SFT |
| `sft_gaql.jsonl` | GAQL-queryparen — natuurlijke taal → GAQL | ~10MB | SFT |
| `dpo_ads.jsonl` | Goede versus slechte reclameadviesparen | ~20MB | DPO |
| `distill_ads.jsonl` | Gedistilleerd uit Claude/GPT voor reclametaken | ~100 MB | Distilleren |

```bash
# Download all datasets
python scripts/download_data.py --all

# Or specific stages
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## Evaluatiebenchmarks

MiniAgent bevat advertentiespecifieke benchmarks (geen bestaande LLM-benchmarks testen PPC-kennis):

| Benchmark | Wat het test | Statistieken |
|----------|--------------|---------|
| **Advertentiebank** | Algemene reclamekennis | Nauwkeurigheid, F1 |
| **GAQL-Eval** | Nauwkeurigheid van het genereren van GAQL-query's | Exacte match, semantische match |
| **Campagnestructuur** | Aanbevelingen voor campagnestructuur | Score van deskundigenovereenkomst |
| **Platformoverschrijdend** | Metrische normalisatie op verschillende platforms | Consistentiescore |
| **Auditevaluatie** | Kwaliteit van de rekeningcontrole | Dekking, bruikbaarheid, nauwkeurigheid |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## Installatie met één klik

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

Hiermee wordt alles geïnstalleerd: Python-afhankelijkheden, modelgewichten, MCP-servers, Claude Code-vaardigheden, en wordt de Streamlit-demo uitgevoerd.

---

## Compatibiliteit

| Platform | Staat | Hoe |
|----------|--------|-----|
| Claude Code | ✅ | Vaardigheden + MCP-servers |
| Claude Bureaublad | ✅ | MCP-servers via config |
| Cursor | ✅ | MCP-servers + .cursor/mcp.json |
| Windsurfen | ✅ | MCP-servers |
| OpenAI-codex | ✅ | Vaardigheden in .codex/skills/ |
| Tweeling CLI | ✅ | Vaardigheden in .gemini/skills/ |
| OpenAI Agents-SDK | ✅ | MCPServerStdio |
| LangChain | ✅ | langchain-mcp-adapters |
| Ollama | ✅ | ollama run miniagent |
| vLLM | ✅ | vllm serveren |
| lama.cpp | ✅ | GGUF-conversie inbegrepen |
| FastGPT | ✅ | OpenAI-compatibele API |
| Open WebUI | ✅ | OpenAI-compatibele API |
| Dify | ✅ | OpenAI-compatibele API |

---

## Toeschrijving

Dit project bouwt voort op het werk van veel open source-bijdragers:

| Project | Auteur | Licentie | Bijdrage |
|---------|--------|---------|------------|
| [minimind](https://github.com/jingyaogong/minimind) | JingyaoGong | Apache 2.0 | Basismodelarchitectuur, trainingspijplijn, tokenizer-framework |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) | Ernesto Cohnen | MIT | OAuth-tokenpersistentie, normalisatie van klant-ID |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | Google LLC | Apache 2.0 | Singleton-coördinatorpatroon, field_mask-uitvoer |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) | Google LLC | Apache 2.0 | laat_unselected_resource_names weg, doc-tools als MCP-tools |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | GoMarble-AI | MIT | MCC traversal, Keyword Planner, duaal transport |
| [garrytan/gstack](https://github.com/garrytan/gstack) | Gary Tan | MIT | Vaardigheidsarchitectuurpatronen, rolgebaseerd agentontwerp |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Steph Ango | MIT | SKILL.md standaard, multi-platform vaardigheidsformaat |
| [anthropics/skills](https://github.com/anthropics/skills) | Antropisch | Apache 2.0 | Vaardighedenframework, plug-inmarktplaatsprotocol |

---

## Ecosysteem

MiniAgent maakt deel uit van een groter open-source ecosysteem voor advertentie-intelligentie:

| Repo | Wat het doet |
|------|-------------|
| **miniagent** (deze opslagplaats) | Alles — trainbaar model + MCP-servers + vaardigheden + hub |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) | Zelfstandige Google Ads MCP (29 tools) |
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Zelfstandige Claude Codeervaardigheden voor Google Ads |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | Horizontale connector met 14 platforms |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) | Volledige Google Ads-agent met FastAPI |
| [creative-asset-validator](https://github.com/itallstartedwithaidea/creative-asset-validator) | AI-aangedreven creatieve analyse op meer dan 50 platforms |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) | Contextintelligentieplatform (6 cognitieve primitieven) |
| [writing-agent](https://github.com/itallstartedwithaidea/writing-agent) | Ghost Protocol voor inhoud van menselijke kwaliteit |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | 42 pagina's tellende spoedcursus voor agenten (MIT) |
| [agency-agents](https://github.com/itallstartedwithaidea/agency-agents) | Compleet AI-bureau – frontend voor de gemeenschap |

---

## Licentie

Apache 2.0 — hetzelfde als minimind. Zie [LICENSE](LICENSE).

---

## Auteur

**John Williams** · Senior specialist in betaalde media · [Seer Interactive](https://seerinteractive.com)
Oprichter, [googleadsagent.ai](https://googleadsagent.ai) · [It All Started With A Idea](https://itallstartedwithaidea.com)

Meer dan 15 jaar beheer van digitale bedrijfsadvertenties ($48 miljoen+ jaarlijkse uitgaven) bij Google, Meta, Microsoft en Amazon.
Spreker: Hero Conf · Gepubliceerd: Search Engine Land · Gebouwd voor de beoefenaar die het platform vergat.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)
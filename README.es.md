<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

[English](./README.md) | [Français](./README.fr.md) | [Español](./README.es.md) | [中文](./README.zh.md) | [Nederlands](./README.nl.md) | [Русский](./README.ru.md) | [한국어](./README.ko.md) | [Italiano](./locales/it/README.md)

### El agente Cowork para todo. Entrena desde cero. Ejecuta en todas partes.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**Entrena tu propia IA publicitaria desde cero. 2 horas. Una GPU. Tus datos.**

El hola mundo de la capacitación de agentes en un dominio específico: para profesionales, por un profesional.

Más de 42.000 estrellas en el modelo base ([minimind](https://github.com/jingyaogong/minimind)) · 14 plataformas publicitarias · 29 herramientas MCP · 5 habilidades de Claude Code · Un repositorio.

</div>

## ¿Qué es esto?

MiniAgent es tres cosas en un repositorio:

1. **Una IA publicitaria entrenable**: bifurcación de [minimind](https://github.com/jingyaogong/minimind) (Apache 2.0, 42.000 estrellas) reentrenada en datos del dominio publicitario. Parámetros 26M-104M. Entrénelo usted mismo en 28 minutos en una sola GPU por ~$0,13. Modelos entrenados: [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M). El modelo aprende GAQL, estructura de campaña, estrategia de oferta, matemáticas de PPC, terminología multiplataforma y análisis creativo en más de 60 plataformas publicitarias.

2. **Un ecosistema de servidor MCP de producción**: 14 conectores de plataformas publicitarias (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, Criteo, AdRoll, TikTok, Snapchat, Pinterest, Quora, X/Twitter) con más de 80 herramientas, todas instalables mediante pip.

3. **Una plataforma de habilidades para agentes**: habilidades de Claude Code, habilidades de Codex, habilidades de Gemini CLI para análisis de publicidad, auditoría, operaciones de escritura segura, matemáticas de PPC e informes multiplataforma.

**Creado por un profesional de medios pagos empresariales con 15 años de experiencia que administra más de $48 millones de inversión publicitaria anual.**

---

## Inicio rápido

### Opción 1: utilizar el modelo publicitario previamente entrenado (no se necesita GPU)

**Modelos entrenados en HuggingFace:**
- [MiniAgent-494M](https://huggingface.co/itallstartedwithaidea/MiniAgent-494M) — 494 millones de parámetros, base multilingüe Qwen2.5-0.5B + dominio publicitario (recomendado, más de 29 idiomas)
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104 millones de parámetros, base minimind + dominio publicitario
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 26 millones de parámetros, entrenados desde cero```bash
# One command — download and run
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Model downloaded! See README for usage.')
"
```

### Resultados de la formación (v0.1 - marzo de 2026)

El modelo 104M se entrenó utilizando **modo combinado**: base previamente entrenada de minimind (lenguaje general) + capacitación previa del dominio publicitario (165 textos únicos en más de 60 plataformas) + SFT (58 pares de instrucción-respuesta de la experiencia de los profesionales).

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

> **Calidad actual**: el modelo ha absorbido vocabulario y conceptos publicitarios (CPA, ROAS, GAQL, porcentaje de impresiones, estrategias de oferta, terminología de plataforma). La coherencia de la salida está limitada en este tamaño de modelo con el volumen de datos de entrenamiento actual; esta es una prueba de concepto v0.1. Cada iteración de entrenamiento con más datos mejorará la calidad. Consulte la sección [Datos de entrenamiento](#training-data) para contribuir.

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### Opción 2: instalar servidores MCP (conéctese a cuentas publicitarias reales)

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# All platforms
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### Opción 3: instalar las habilidades de Claude Code (no se necesita API)

```bash
# Plugin marketplace
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Or manually
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### Opción 4: Entrena tu propio modelo desde cero (2 horas, 1 GPU)

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

**Costo: ~$0.40 USD en un solo 3090. 2 horas.**

---

## Arquitectura

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
│   # También en la raíz: README.fr.md, README.es.md, README.zh.md, README.nl.md, README.ru.md, README.ko.md
├── .claude/commands/         # Claude Code slash commands
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Claude Code project instructions
├── pyproject.toml            # pip installable
└── README.es.md              # Este archivo (español)
```

---

## Lo que aprende el modelo

### Etapa 1: Capacitación previa (lenguaje publicitario)
El modelo lee millones de tokens de conocimiento publicitario: documentación de Google Ads, mejores prácticas de gestión de campañas, contenido de la industria de PPC, sintaxis GAQL y terminología multiplataforma. Después del entrenamiento previo, puede completar oraciones como:

> **Entrada:** "Un porcentaje de impresiones de búsqueda del 65% con un porcentaje de impresiones perdidas del 20% del presupuesto significa"
> **Resultado:** "la campaña está perdiendo el 20 % de las impresiones aptas debido a un presupuesto diario insuficiente. Aumentar el presupuesto diario o limitar la orientación geográfica recuperaría este porcentaje".

### Etapa 2: SFT (siguiendo instrucciones)
El modelo aprende a seguir instrucciones publicitarias:

> **Usuario:** "Audite esta cuenta de Google Ads. El CPA es de $45, el objetivo es de $30 y el porcentaje de impresiones es del 40%".
> **MiniAgent:** "Tres problemas: 1) El CPA está 50 % por encima del objetivo; verifique el informe de términos de búsqueda para ver si hay consultas irrelevantes que consumen el presupuesto. 2) Un porcentaje de impresiones del 40 % significa que se está perdiendo el 60 % de las subastas elegibles; o el presupuesto es demasiado bajo o el nivel de calidad necesita mejorar. 3) Recomendar: agregue palabras clave negativas, suspenda los grupos de anuncios de bajo rendimiento y aumente las ofertas solo en los que generan mayores conversiones".

### Etapa 3: Alineación del DPO (buenos o malos consejos)
El modelo aprende a preferir los buenos consejos de PPC a los malos:

> **Bueno:** "Comience con palabras clave de concordancia exacta para términos de alta intención y luego amplíe a concordancia de frase después de 2 semanas de datos".
> **Malo:** "Utilice concordancia amplia en todo para maximizar el volumen".

---

## Servidores MCP

Cada plataforma es un servidor MCP independiente, instalable mediante pip:

| Plataforma | Instalar | Herramientas | Estado |
|----------|---------|-------|--------|
| Anuncios de Google | `pip install miniagent[google]` | 29 | ✅ Producción |
| Metaanuncios | `pip install miniagent[meta]` | 18 | ✅ Producción |
| Anuncios de Microsoft | `pip install miniagent[microsoft]` | 15 | 🔧Beta |
| Anuncios de Amazon | `pip install miniagent[amazon]` | 12 | 🔧Beta |
| Anuncios de Reddit | `pip install miniagent[reddit]` | 8 | 🔧Beta |
| Mesa de Comercio | `pip install miniagent[tradedesk]` | 10 | 🔧Beta |
| Anuncios de LinkedIn | `pip install miniagent[linkedin]` | 10 | 🔧Beta |
| Anuncios de TikTok | `pip install miniagent[tiktok]` | 10 | 📋 Planificado |
| Todas las plataformas | `pip install miniagent[todos]` | 80+ | — |

### Integración del código Claude

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

### Cursor / Windsurf / SDK de agentes OpenAI

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

## Habilidades del agente

Las habilidades funcionan con Claude Code, Codex, Gemini CLI, Cursor y cualquier agente que admita el estándar SKILL.md.

| Habilidad | Descripción | ¿Necesita API? |
|-------|-------------|-----------|
| `análisis-de-google-ads` | Análisis de rendimiento de campañas, patrones GAQL, detección de anomalías | Sí (a través de MCP) |
| `auditoría-de-google-ads` | Auditoría de cuentas en 7 dimensiones con clasificaciones de gravedad, planes de 30/60/90 días | Sí (a través de MCP) |
| `google-ads-escritura` | Escrituras seguras mediante el protocolo Confirm-Execute-Postcheck (CEP) | Sí (a través de MCP) |
| `google-ads-matemáticas` | Cálculos de PPC: CPA, ROAS, proyecciones presupuestarias, punto de equilibrio | No |
| `google-ads-mcp` | Guía de configuración del servidor MCP para acceso API en vivo | Guía de configuración |

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

## Datos de entrenamiento

Todos los datos de capacitación son de código abierto y específicos del dominio publicitario:

| Conjunto de datos | Descripción | Tamaño | Etapa |
|---------|-------------|------|-------|
| `pretrain_ads.jsonl` | Corpus de conocimientos publicitarios: documentos de Google Ads, prácticas recomendadas de PPC, contenido de la industria | ~500MB | Preentrenamiento |
| `sft_ads.jsonl` | Pares instrucción-respuesta para tareas de PPC | ~50MB | OFV |
| `sft_gaql.jsonl` | Pares de consultas GAQL: lenguaje natural → GAQL | ~10 MB | OFV |
| `dpo_ads.jsonl` | Pares de consejos publicitarios buenos y malos | ~20MB | DPO |
| `distill_ads.jsonl` | Destilado de Claude/GPT sobre tareas publicitarias | ~100MB | Destilar |

```bash
# Download all datasets
python scripts/download_data.py --all

# Or specific stages
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## Puntos de referencia de evaluación

MiniAgent incluye puntos de referencia específicos de publicidad (no existen puntos de referencia de LLM que prueben el conocimiento de PPC):

| Punto de referencia | Qué prueba | Métricas |
|-----------|--------------|---------|
| **Banco de anuncios** | Conocimientos generales de publicidad | Precisión, F1 |
| **Evaluación GAQL** | Precisión de generación de consultas GAQL | Coincidencia exacta, coincidencia semántica |
| **Estructura de campaña** | Recomendaciones de estructura de campaña | Puntuación del acuerdo de expertos |
| **Multiplataforma** | Normalización de métricas entre plataformas | Puntuación de coherencia |
| **Auditoría-Evaluación** | Calidad de la auditoría de cuentas | Cobertura, accionabilidad, precisión |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## Instalación con un clic

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

Esto instala todo: dependencias de Python, pesos de modelos, servidores MCP, habilidades de Claude Code y ejecuta la demostración de Streamlit.

---

## Compatibilidad

| Plataforma | Estado | Cómo |
|----------|--------|-----|
| Código Claude | ✅ | Habilidades + servidores MCP |
| Escritorio Claude | ✅ | Servidores MCP a través de configuración |
| Cursores | ✅ | Servidores MCP + .cursor/mcp.json |
| Windsurf | ✅ | Servidores MCP |
| Códice OpenAI | ✅ | Habilidades en .codex/skills/ |
| Géminis CLI | ✅ | Habilidades en .gemini/skills/ |
| SDK de agentes OpenAI | ✅ | MCPServerStdio |
| Cadena Lang | ✅ | adaptadores langchain-mcp |
| Ollamá | ✅ | ollama ejecutar miniagente |
| vLLM | ✅ | servir vllm |
| llama.cpp | ✅ | Conversión GGUF incluida |
| GPT rápido | ✅ | API compatible con OpenAI |
| Interfaz de usuario web abierta | ✅ | API compatible con OpenAI |
| Dificar | ✅ | API compatible con OpenAI |

---

## Atribución

Este proyecto se basa en el trabajo de muchos contribuyentes de código abierto:

| Proyecto | Autor | Licencia | Contribución |
|---------|--------|---------|-------------|
| [minimente](https://github.com/jingyaogong/minimind) | JingyaoGong | Apache 2.0 | Arquitectura del modelo base, canal de capacitación, marco tokenizador |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) | Ernesto Cohnen | MIT | Persistencia del token OAuth, normalización de ID de cliente |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | Google LLC | Apache 2.0 | Patrón coordinador singleton, salida field_mask |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) | Google LLC | Apache 2.0 | omit_unselected_resource_names, herramientas de documentación como herramientas MCP |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | GoMarble AI | MIT | Recorrido de MCC, Planificador de palabras clave, transporte dual |
| [garrytan/gstack](https://github.com/garrytan/gstack) | Garry Tan | MIT | Patrones de arquitectura de habilidades, diseño de agentes basado en roles |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Estefa Ango | MIT | SKILL.md formato de habilidad estándar y multiplataforma |
| [antrópicos/habilidades](https://github.com/anthropics/skills) | Antrópico | Apache 2.0 | Marco de habilidades, protocolo de mercado de complementos |

---

## Ecosistema

MiniAgent es parte de un ecosistema de inteligencia publicitaria de código abierto más amplio:

| Repositorio | Qué hace |
|------|-------------|
| **miniagent** (este repositorio) | Todo: modelo entrenable + servidores MCP + habilidades + centro |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) | MCP independiente de Google Ads (29 herramientas) |
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Habilidades independientes de Claude Code para Google Ads |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | Conector horizontal de 14 plataformas |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) | Agente completo de Google Ads con FastAPI |
| [creative-asset-validator](https://github.com/itallstartedwithaidea/creative-asset-validator) | Análisis creativo impulsado por IA en más de 50 plataformas |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) | Plataforma de inteligencia contextual (6 primitivas cognitivas) |
| [writing-agent](https://github.com/itallstartedwithaidea/writing-agent) | Protocolo fantasma para contenido de calidad humana |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | Curso intensivo para agentes de 42 páginas (MIT) |
| [agency-agents](https://github.com/itallstartedwithaidea/agency-agents) | Agencia de IA completa: interfaz de la comunidad |

---

## Licencia

Apache 2.0: igual que minimind. Consulte [LICENSE](LICENSE).

---

## Autor

**John Williams** · Especialista senior en medios pagos · [Seer Interactive](https://seerinteractive.com)
Fundador, [googleadsagent.ai](https://googleadsagent.ai) · [It All Started With A Idea](https://itallstartedwithaidea.com)

Más de 15 años gestionando publicidad digital empresarial (más de 48 millones de dólares de gasto anual) en Google, Meta, Microsoft y Amazon.
Orador: Hero Conf · Publicado: Search Engine Land · Construida para el practicante, la plataforma se olvidó.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)
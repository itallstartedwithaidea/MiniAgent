<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

[English](./README.md) | [Français](./README.fr.md) | [Español](./README.es.md) | [中文](./README.zh.md) | [Nederlands](./README.nl.md) | [Русский](./README.ru.md) | [한국어](./README.ko.md) | [Italiano](./locales/it/README.md)

### Агент Cowork для всего. Обучение с нуля. Запуск везде.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**Обучите свой собственный рекламный ИИ с нуля. 2 часа. Один графический процессор. Ваши данные.**

Привет, мир специализированного обучения агентов — для практиков, от практиков.

Более 42 тысяч звезд за базовую модель ([minimind](https://github.com/jingyaogong/minimind)) · 14 рекламных платформ · 29 инструментов MCP · 5 навыков работы с Claude Code · Один репозиторий.

</div>

## Что это?

MiniAgent — это три вещи в одном репозитории:

1. **Обучаемый рекламный ИИ** — форк [minimind](https://github.com/jingyaogong/minimind) (Apache 2.0, 42 тыс. звезд), переобученный на данных рекламного домена. Параметры 26М-104М. Обучите его самостоятельно за 28 минут на одном графическом процессоре примерно за 0,13 доллара. Обученные модели: [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M). Модель изучает GAQL, структуру кампании, стратегию ставок, математику PPC, кроссплатформенную терминологию и креативный анализ на более чем 60 рекламных платформах.

2. **Экосистема производственного сервера MCP** — 14 соединителей рекламных платформ (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, Criteo, AdRoll, TikTok, Snapchat, Pinterest, Quora, X/Twitter) с более чем 80 инструментами, все из которых можно установить с помощью pip.

3. **Платформа навыков агента** — навыки Claude Code, навыки Codex, навыки Gemini CLI для анализа рекламы, аудита, операций безопасной записи, математики PPC и кросс-платформенной отчетности.

**Создано корпоративным специалистом в области СМИ с 15-летним стажем, который ежегодно тратит на рекламу более 48 миллионов долларов.**

---

## Быстрый старт

### Вариант 1. Используйте предварительно обученную рекламную модель (графический процессор не требуется)

**Обученные модели на HuggingFace:**
- [MiniAgent-494M](https://huggingface.co/itallstartedwithaidea/MiniAgent-494M) — 494M параметров, многоязычная база Qwen2.5-0,5B + рекламный домен (рекомендуется, 29+ языков)
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104M параметров, база minimind + рекламный домен
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 26M параметров, обученных с нуля.```bash
# One command — download and run
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Model downloaded! See README for usage.')
"
```

### Результаты обучения (v0.1 — март 2026 г.)

Модель 104M была обучена в **комбинированном режиме**: предварительно обученная база minimind (общий язык) + предварительное обучение рекламной области (165 уникальных текстов на более чем 60 платформах) + SFT (58 пар инструкция-ответ на основе опыта практикующего специалиста).

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

> **Текущее качество**: модель вобрала в себя рекламную лексику и концепции (CPA, ROAS, GAQL, процент полученных показов, стратегии назначения ставок, терминологию платформы). Согласованность вывода ограничена при этом размере модели с текущим объемом обучающих данных — это доказательство концепции версии 0.1. Каждая итерация обучения с большим количеством данных будет улучшать качество. Чтобы внести свой вклад, см. раздел [Данные обучения](#training-data).

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### Вариант 2. Установите серверы MCP (подключитесь к реальным рекламным аккаунтам)

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# All platforms
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### Вариант 3: Установите навыки Claude Code (API не требуется)

```bash
# Plugin marketplace
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Or manually
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### Вариант 4. Обучите свою модель с нуля (2 часа, 1 графический процессор)

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

**Стоимость: ~0,40 доллара США за один 3090. 2 часа.**

---

## Архитектура

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
│   # Также в корне: README.fr.md, README.es.md, README.zh.md, README.nl.md, README.ru.md, README.ko.md
├── .claude/commands/         # Claude Code slash commands
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Claude Code project instructions
├── pyproject.toml            # pip installable
└── README.ru.md              # Этот файл (русский)
```

---

## Чему учит модель

### Этап 1. Предварительная подготовка (язык рекламы)
Модель считывает миллионы токенов рекламных знаний — документацию Google Ads, лучшие практики управления кампаниями, отраслевой контент PPC, синтаксис GAQL, кроссплатформенную терминологию. После предварительной подготовки он может завершать такие предложения, как:

> **Ввод:** "Доля показов в поисковой сети 65 % и доля потерянных показов в бюджете 20 % означает"
> **Результат:** "Кампания теряет 20 % подходящих показов из-за недостаточного дневного бюджета. Увеличение дневного бюджета или сужение геотаргетинга восстановит эту долю".

### Этап 2: SFT (следование инструкциям)
Модель учится следовать рекламным инструкциям:

> **Пользователь:** "Проведите аудит этого аккаунта Google Реклама. Цена за конверсию – 45 долларов США, целевая цена – 30 долларов США, доля полученных показов – 40 %".
> **MiniAgent:** "Три проблемы: 1) цена за конверсию на 50 % превышает целевую — проверьте отчет о поисковых запросах на наличие нерелевантных запросов, съедающих бюджет. 2) доля полученных показов 40 % означает, что вы пропускаете 60 % подходящих аукционов — либо бюджет слишком мал, либо показатель качества требует улучшения. 3) Рекомендация: добавьте минус-слова, приостановите показы малоэффективных групп объявлений, увеличьте ставки только для тех, кто совершил больше всего конверсий".

### Этап 3: Согласование DPO (хороший и плохой совет)
Модель учится предпочитать хорошие PPC-советы плохим:

> **Хорошо:** «Начните с ключевых слов с точным соответствием для терминов с высоким уровнем намерения, а затем, после двухнедельного сбора данных, перейдите к фразовому соответствия».
> **Плохо:** «Используйте широкое соответствие для всего, чтобы максимизировать объем».

---

## MCP-серверы

Каждая платформа представляет собой отдельный MCP-сервер, устанавливаемый по протоколу:

| Платформа | Установить | Инструменты | Статус |
|----------|---------|-------|--------|
| Google Реклама | `pip install miniagent[google]` | 29 | ✅ Производство |
| Мета-объявления | `pip install miniagent[meta]` | 18 | ✅ Производство |
| Реклама Майкрософт | `pip install miniagent[microsoft]` | 15 | 🔧 Бета |
| Объявления Амазонки | `pip install miniagent[amazon]` | 12 | 🔧 Бета |
| Объявления на Reddit | `pip install miniagent[reddit]` | 8 | 🔧 Бета |
| ТрейдДеск | `pip install miniagent[tradedesk]` | 10 | 🔧 Бета |
| Реклама в LinkedIn | `pip install miniagent[linkedin]` | 10 | 🔧 Бета |
| Реклама в Тик Ток | `pip install miniagent[tiktok]` | 10 | 📋 Планируется |
| Все платформы | `pip install miniagent[all]` | 80+ | — |

### Интеграция кода Клода

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

### Курсор / Виндсерфинг / OpenAI Agents SDK

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

## Навыки агента

Навыки работают с Claude Code, Codex, Gemini CLI, Cursor и любым агентом, поддерживающим стандарт SKILL.md.

| Навык | Описание | Нужен API? |
|-------|-------------|-----------|
| `Google-рекламный анализ` | Анализ эффективности кампании, шаблоны GAQL, обнаружение аномалий | Да (через MCP) |
| `Google-реклама-аудит` | 7-мерный аудит аккаунта с уровнями серьезности, планы на 30/60/90 дней | Да (через MCP) |
| `google-ads-write` | Безопасная запись с использованием протокола Confirm-Execute-Postcheck (CEP) | Да (через MCP) |
| `google-ads-math` | Расчеты PPC — CPA, ROAS, прогноз бюджета, безубыточность | Нет |
| `google-ads-mcp` | Руководство по настройке сервера MCP для доступа к API в реальном времени | Руководство по установке |

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

## Данные обучения

Все обучающие данные имеют открытый исходный код и зависят от рекламного домена:

| Набор данных | Описание | Размер | Этап |
|---------|-------------|------|-------|
| `pretrain_ads.jsonl` | Корпус знаний о рекламе: документация по Google Рекламе, лучшие практики PPC, отраслевой контент | ~500 МБ | Предварительная подготовка |
| `sft_ads.jsonl` | Пары инструкция-ответ для задач PPC | ~50 МБ | СФТ |
| `sft_gaql.jsonl` | Пары запросов GAQL — естественный язык → GAQL | ~10 МБ | СФТ |
| `dpo_ads.jsonl` | Пары хороших и плохих рекламных советов | ~20 МБ | ДПО |
| `distill_ads.jsonl` | Из опыта Клода/GPT по рекламным задачам | ~100 МБ | Дистиллировать |

```bash
# Download all datasets
python scripts/download_data.py --all

# Or specific stages
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## Тесты оценки

MiniAgent включает тесты, специфичные для рекламы (никакие существующие тесты LLM не проверяют знание PPC):

| Бенчмарк | Что он тестирует | Метрики |
|-----------|--------------|---------|
| **Рекламный стенд** | Общие знания в области рекламы | Точность, F1 |
| **GAQL-Оценка** | Точность генерации запросов GAQL | Точное совпадение, смысловое совпадение |
| **Структура кампании** | Рекомендации по структуре кампании | Оценка экспертного соглашения |
| **Кроссплатформенность** | Нормализация показателей на разных платформах | Оценка согласованности |
| **Аудит-Оценка** | Качество аудита аккаунта | Охват, действенность, точность |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## Установка в один клик

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

При этом устанавливается все: зависимости Python, веса моделей, серверы MCP, навыки работы с Claude Code и запускается демо-версия Streamlit.

---

## Совместимость

| Платформа | Статус | Как |
|----------|--------|-----|
| Клод Код | ✅ | Навыки + серверы MCP |
| Клод Рабочий стол | ✅ | Серверы MCP через конфигурацию |
| Курсор | ✅ | Серверы MCP + .cursor/mcp.json |
| Виндсерфинг | ✅ | MCP-серверы |
| Кодекс OpenAI | ✅ | Навыки в .codex/skills/ |
| Близнецы CLI | ✅ | Навыки в .gemini/skills/ |
| SDK агентов OpenAI | ✅ | MCPServerStdio |
| Лангчейн | ✅ | адаптеры langchain-mcp |
| Оллама | ✅ | оллама запустить миниагент |
| vLLM | ✅ | вллм служить |
| лама.cpp | ✅ | Преобразование GGUF включено |
| ФастGPT | ✅ | OpenAI-совместимый API |
| Открытый веб-интерфейс | ✅ | OpenAI-совместимый API |
| Диди | ✅ | OpenAI-совместимый API |

---

## Атрибуция

Этот проект основан на работе многих участников открытого исходного кода:

| Проект | Автор | Лицензия | Вклад |
|---------|--------|---------|-------------|
| [миниразум](https://github.com/jingyaogong/minimind) | ЦзинъяоГонг | Апач 2.0 | Архитектура базовой модели, конвейер обучения, структура токенизатора |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) | Эрнесто Конен | Массачусетский технологический институт | Сохранение токена OAuth, нормализация идентификатора клиента |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | ООО "Гугл" | Апач 2.0 | Шаблон координатора Singleton, вывод field_mask |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) | ООО "Гугл" | Апач 2.0 | omit_unselected_resource_names, инструменты документации как инструменты MCP |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | ГоМарбл ИИ | Массачусетский технологический институт | Обход MCC, Планировщик ключевых слов, двойной транспорт |
| [garrytan/gstack](https://github.com/garrytan/gstack) | Гарри Тан | Массачусетский технологический институт | Шаблоны архитектуры навыков, проектирование агентов на основе ролей |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Стеф Анго | Массачусетский технологический институт | SKILL.md стандартный, мультиплатформенный формат навыков |
| [антропика/навыки](https://github.com/anthropics/skills) | Антропный | Апач 2.0 | Платформа навыков, протокол рынка плагинов |

---

## Экосистема

MiniAgent является частью более крупной экосистемы рекламной разведки с открытым исходным кодом:

| Репо | Что он делает |
|------|-------------|
| **миниагент** (это репозиторий) | Всё — обучаемая модель + серверы MCP + навыки + хаб |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) | Автономный MCP Google Рекламы (29 инструментов) |
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Навыки использования автономного кода Claude для Google Ads |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | 14-платформенный горизонтальный разъем |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) | Полноценный агент Google Рекламы с FastAPI |
| [creative-asset-validator](https://github.com/itallstartedwithaidea/creative-asset-validator) | Креативный анализ на основе искусственного интеллекта на более чем 50 платформах |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) | Платформа контекстного интеллекта (6 когнитивных примитивов) |
| [writing-agent](https://github.com/itallstartedwithaidea/writing-agent) | Протокол Ghost для контента человеческого качества |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | 42-страничный ускоренный курс для агентов (MIT) |
| [agency-agents](https://github.com/itallstartedwithaidea/agency-agents) | Агентство Complete AI — интерфейс для сообщества |

---

## Лицензия

Apache 2.0 — то же, что минимайнд. См. [LICENSE](LICENSE).

---

## Автор

**Джон Уильямс** · Старший специалист по платным медиа · [Seer Interactive](https://seerinteractive.com)
Основатель [googleadsagent.ai](https://googleadsagent.ai) · [It All Started With A Idea](https://itallstartedwithaidea.com)

Более 15 лет управления корпоративной цифровой рекламой (годовые расходы более 48 миллионов долларов США) в Google, Meta, Microsoft, Amazon.
Спикер: Hero Conf · Опубликовано: Search Engine Land · Создано для практикующих, о которых забыла платформа.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)
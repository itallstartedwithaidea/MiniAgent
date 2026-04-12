<div align="center">

<img src="./docs/logo.svg" width="200"/>

# MiniAgent

[English](./README.md) | [Français](./README.fr.md) | [Español](./README.es.md) | [中文](./README.zh.md) | [Nederlands](./README.nl.md) | [Русский](./README.ru.md) | [한국어](./README.ko.md) | [Italiano](./locales/it/README.md)

### L’agent Cowork pour tout. Entraînez depuis zéro. Exécutez partout.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple.svg)](https://code.claude.com)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-black.svg)](https://ollama.ai)
[![vLLM](https://img.shields.io/badge/vLLM-Compatible-orange.svg)](https://vllm.ai)

**Entraînez votre propre IA publicitaire à partir de zéro. 2 heures. Un GPU. Vos données.**

Le « hello world » de l’entraînement d’agents spécialisés par domaine — par un praticien, pour les praticiens.

Plus de 42k étoiles sur le modèle de base ([minimind](https://github.com/jingyaogong/minimind)) · 14 plateformes publicitaires · 29 outils MCP · 5 compétences Claude Code · Un seul dépôt.

</div>

---

## Qu’est-ce que c’est ?

MiniAgent, c’est trois choses dans un seul dépôt :

1. **Une IA publicitaire entraînable** — fork de [minimind](https://github.com/jingyaogong/minimind) (Apache 2.0, 42k étoiles) réentraîné sur des données du domaine publicitaire. 26M–104M paramètres. Entraînez-le vous-même en 28 minutes sur un seul GPU pour ~0,13 $. Modèles entraînés : [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) · [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M). Le modèle apprend la GAQL, la structure des campagnes, les stratégies d’enchères, le calcul PPC, la terminologie multi-plateforme et l’analyse créative sur plus de 60 plateformes publicitaires.

2. **Un écosystème de serveurs MCP en production** — 14 connecteurs de plateformes publicitaires (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, Criteo, AdRoll, TikTok, Snapchat, Pinterest, Quora, X/Twitter) avec plus de 80 outils, tous installables via pip.

3. **Une plateforme de compétences d’agent** — compétences Claude Code, Codex et Gemini CLI pour l’analyse publicitaire, l’audit, les écritures sécurisées, le calcul PPC et les rapports multi-plateformes.

**Construit par un praticien média payant entreprise depuis 15 ans, pilotant plus de 48 M$ de dépenses publicitaires annuelles.**

---

## Démarrage rapide

### Option 1 : utiliser le modèle publicitaire pré-entraîné (sans GPU)

**Modèles entraînés sur HuggingFace :**
- [MiniAgent-494M](https://huggingface.co/itallstartedwithaidea/MiniAgent-494M) — 494M paramètres, base multilingue Qwen2.5-0.5B + domaine publicitaire (recommandé, 29+ langues)
- [MiniAgent-104M](https://huggingface.co/itallstartedwithaidea/MiniAgent-104M) — 104M paramètres, base minimind + domaine publicitaire
- [MiniAgent-26M](https://huggingface.co/itallstartedwithaidea/MiniAgent-26M) — 26M paramètres, entraîné from scratch

```bash
# Une commande — télécharger et lancer
pip install torch transformers huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('itallstartedwithaidea/MiniAgent-104M', local_dir='./MiniAgent-104M')
print('Modèle téléchargé ! Consultez le README pour l’usage.')
"
```

### Résultats d’entraînement (v0.1 — mars 2026)

Le modèle 104M a été entraîné en **mode combiné** : base pré-entraînée minimind (langage général) + pré-entraînement domaine publicitaire (165 textes uniques sur plus de 60 plateformes) + SFT (58 paires instruction–réponse issues de l’expertise terrain).

```
Pipeline d’entraînement :
  Modèle de base : minimind MiniMind2 (104M paramètres, pré-entraîné sur des milliards de jetons)
  + Pré-entraînement : 165 textes publicitaires uniques × 150 répétitions = 24 750 échantillons
                 Couverture : Google, Meta, Microsoft, Amazon, LinkedIn, TikTok,
                 Snapchat, Pinterest, Reddit, The Trade Desk, Criteo, DV360,
                 Taboola, Outbrain, Walmart Connect, Roku, AppsFlyer, GA4, GTM...
  + SFT :         58 paires Q/R uniques × 80 répétitions = 4 640 échantillons
                 Couverture : calcul PPC, requêtes GAQL, audits, stratégie multi-plateformes,
                 suivi des conversions, stratégie d’enchères, structure des campagnes, diagnostics
  Matériel :      NVIDIA RTX 4000 Ada (20 Go VRAM)
  Durée :         28 minutes au total (coût cloud ~0,13 $)
  Loss prétrain : 13,18 → 0,023 (3 époques)
  Loss SFT :      6,57 → 0,011 (5 époques)
```

> **Qualité actuelle** : le modèle a absorbé le vocabulaire et les concepts publicitaires (CPA, ROAS, GAQL, part d’impressions, stratégies d’enchères, terminologie des plateformes). La cohérence des sorties reste limitée à cette taille de modèle et avec le volume actuel de données — preuve de concept v0.1. Chaque itération d’entraînement avec davantage de données améliorera la qualité. Voir la section [Données d’entraînement](#training-data) pour contribuer.

```bash
# vLLM
vllm serve itallstartedwithaidea/MiniAgent-104M --served-model-name "miniagent"
```

### Option 2 : installer les serveurs MCP (connexion aux comptes réels)

```bash
# Google Ads MCP — 29 tools
pip install miniagent[google]

# Toutes les plateformes
pip install miniagent[all]

# Claude Code
claude mcp add miniagent-google -- python -m miniagent.mcp.google_ads
claude mcp add miniagent-meta -- python -m miniagent.mcp.meta_ads
```

### Option 3 : installer les compétences Claude Code (sans API)

```bash
# Place de marché des plugins
/plugin marketplace add itallstartedwithaidea/miniagent
/plugin install advertising-full@miniagent

# Ou manuellement
git clone https://github.com/itallstartedwithaidea/miniagent.git ~/.claude/skills/miniagent
```

### Option 4 : entraîner votre propre modèle from scratch (2 heures, 1 GPU)

```bash
git clone https://github.com/itallstartedwithaidea/miniagent.git
cd miniagent
pip install -r requirements.txt

# Télécharger les données d’entraînement publicitaire
python scripts/download_data.py

# Pré-entraînement (apprend le langage publicitaire)
python trainer/pretrain.py --dim 512 --n_layers 8

# SFT (apprend à suivre des instructions publicitaires)
python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth

# Fine-tuning LoRA sur VOS données de compte (optionnel)
python trainer/lora.py --load_from ./checkpoints/sft_512.pth --data ./dataset/my_account.jsonl

# Alignement DPO (bon vs mauvais conseils pub)
python trainer/dpo.py --load_from ./checkpoints/sft_512.pth
```

**Coût : ~0,40 $ USD sur une seule 3090. 2 heures.**

---

## Architecture

```
MiniAgent
├── model/                    # LLM entraînable (fork de minimind)
│   ├── model_miniagent.py    # Transformeur décodeur seul (26M–145M paramètres)
│   ├── LMConfig.py           # Configuration du modèle
│   └── tokenizer/            # Tokenizer publicitaire personnalisé
│
├── trainer/                  # Pipeline d’entraînement complet
│   ├── pretrain.py           # Étape 1 : apprendre le langage publicitaire
│   ├── sft.py                # Étape 2 : suivre les instructions
│   ├── lora.py               # Étape 3 : fine-tuning sur VOS données
│   ├── dpo.py                # Étape 4 : alignement sur les bonnes pratiques PPC
│   ├── grpo.py               # Étape 5 : optimisation relative de politique par groupes
│   └── distill.py            # Distillation depuis Claude/GPT vers MiniAgent
│
├── mcp_servers/               # Serveurs MCP (14 plateformes)
│   ├── google_ads/           # 29 outils — campagne, mot-clé, audit, écriture
│   ├── meta_ads/             # 18 outils — campagne, créatif, audience
│   ├── microsoft_ads/        # 15 outils — campagne, mot-clé, UET
│   ├── amazon_ads/           # 12 outils — campagnes SP, SB, SD
│   ├── reddit_ads/           # 8 outils — campagne, ciblage, créatif
│   ├── tradedesk/            # 10 outils — campagne, inventaire, audience
│   ├── linkedin_ads/         # 10 outils — campagne, ciblage, conversion
│   ├── criteo/               # 8 outils
│   ├── adroll/               # 8 outils
│   ├── tiktok/               # 10 outils
│   ├── snapchat/             # 8 outils
│   ├── pinterest/            # 8 outils
│   ├── quora/                # 6 outils
│   └── twitter/              # 8 outils
│
├── skills/                   # Compétences d’agent (Claude Code, Codex, Gemini CLI)
│   ├── google-ads-analysis/  # Analyse des performances de campagne
│   ├── google-ads-audit/     # Audit de compte sur 7 dimensions
│   ├── google-ads-write/     # Écritures sécurisées (protocole CEP)
│   ├── google-ads-math/      # Calculs PPC et prévisions
│   └── google-ads-mcp/       # Guide d’installation du serveur MCP
│
├── hub/                      # Advertising Hub — 14 connecteurs de plateformes
│   ├── google/               # Connecteur Google Ads API v23
│   ├── meta/                 # Connecteur Meta Marketing API
│   ├── microsoft/            # Connecteur Microsoft Ads API
│   ├── amazon/               # Connecteur Amazon Ads API
│   ├── reddit/               # Connecteur Reddit Ads API
│   ├── tradedesk/            # Connecteur TradeDesk API
│   ├── linkedin/             # Connecteur LinkedIn Marketing API
│   ├── criteo/               # Connecteur Criteo API
│   ├── adroll/               # Connecteur AdRoll API
│   ├── tiktok/               # Connecteur TikTok Business API
│   ├── snapchat/             # Connecteur Snapchat Marketing API
│   ├── pinterest/            # Connecteur Pinterest Ads API
│   ├── quora/                # Connecteur Quora Ads API
│   └── twitter/              # Connecteur X Ads API
│
├── eval/                     # Benchmarks et évaluation
│   ├── advertising_bench.py  # Suite d’évaluation spécifique PPC
│   ├── gaql_eval.py          # Précision des requêtes GAQL
│   ├── campaign_structure.py # Évaluation de la structure des campagnes
│   └── cross_platform.py     # Précision de normalisation multi-plateforme
│
├── scripts/                  # Utilitaires
│   ├── download_data.py      # Télécharger les jeux de données d’entraînement
│   ├── convert_model.py      # Conversion torch / transformers / GGUF
│   ├── serve_openai_api.py   # Serveur API compatible OpenAI
│   ├── web_demo.py           # Démo de chat Streamlit
│   └── one_click_install.sh  # Installation complète en un clic
│
├── dataset/                  # Données d’entraînement (domaine publicitaire)
│   ├── pretrain_ads.jsonl    # Corpus de connaissances publicitaires
│   ├── sft_ads.jsonl         # Suivi d’instructions pour tâches PPC
│   ├── dpo_ads.jsonl         # Paires de conseils publicitaires bons vs mauvais
│   └── gaql_pairs.jsonl      # Paires requête–réponse GAQL
│
├── docs/                     # Documentation
│   ├── wiki/                 # Wiki complet (38+ pages)
│   └── architecture/         # Décisions d’architecture
│
├── locales/                  # Traductions
│   ├── zh/README.md          # 中文
│   ├── ru/README.md          # Русский
│   ├── it/README.md          # Italiano
│   └── es/README.md          # Español
│   # Aussi : README.fr.md, README.es.md, README.zh.md, README.nl.md, README.ru.md, README.ko.md à la racine
│
├── .claude/commands/         # Commandes slash Claude Code
├── .github/workflows/        # CI/CD + heartbeat
├── CLAUDE.md                 # Instructions projet Claude Code
├── pyproject.toml            # Installable via pip
└── README.fr.md              # Ce fichier (français)
```

---

## Ce qu’apprend le modèle

### Étape 1 : pré-entraînement (langage publicitaire)
Le modèle lit des millions de jetons de connaissances publicitaires — documentation Google Ads, bonnes pratiques de gestion de campagnes, contenu industriel PPC, syntaxe GAQL, terminologie multi-plateforme. Après le pré-entraînement, il peut compléter des phrases comme :

> **Entrée :** « Une part d’impressions recherche de 65 % avec une part d’impressions perdues pour budget de 20 % signifie »
> **Sortie :** « la campagne perd 20 % des impressions éligibles faute de budget journalier suffisant. Augmenter le budget journalier ou resserrer le ciblage géographique permettrait de récupérer cette part. »

### Étape 2 : SFT (suivi d’instructions)
Le modèle apprend à suivre des instructions publicitaires :

> **Utilisateur :** « Audite ce compte Google Ads. Le CPA est de 45 $, l’objectif est 30 $, la part d’impressions est de 40 %. »
> **MiniAgent :** « Trois points : 1) le CPA dépasse l’objectif de 50 % — consultez le rapport des requêtes de recherche pour les requêtes hors sujet qui consomment le budget. 2) 40 % de part d’impressions signifie que vous manquez 60 % des enchères éligibles — budget trop bas ou Quality Score à améliorer. 3) Recommandations : ajouter des mots-clés négatifs, mettre en pause les groupes d’annonces peu performants, augmenter les enchères uniquement sur les meilleurs convertisseurs. »

### Étape 3 : alignement DPO (bons vs mauvais conseils)
Le modèle apprend à préférer de bons conseils PPC aux mauvais :

> **Bon :** « Commencez par des mots-clés correspondance exacte pour les termes à forte intention, puis passez à la correspondance expression après 2 semaines de données. »
> **Mauvais :** « Utilisez la correspondance large partout pour maximiser le volume. »

---

## Serveurs MCP

Chaque plateforme est un serveur MCP distinct, installable via pip :

| Plateforme | Installation | Outils | Statut |
|----------|---------|-------|--------|
| Google Ads | `pip install miniagent[google]` | 29 | ✅ Production |
| Meta Ads | `pip install miniagent[meta]` | 18 | ✅ Production |
| Microsoft Ads | `pip install miniagent[microsoft]` | 15 | 🔧 Bêta |
| Amazon Ads | `pip install miniagent[amazon]` | 12 | 🔧 Bêta |
| Reddit Ads | `pip install miniagent[reddit]` | 8 | 🔧 Bêta |
| TradeDesk | `pip install miniagent[tradedesk]` | 10 | 🔧 Bêta |
| LinkedIn Ads | `pip install miniagent[linkedin]` | 10 | 🔧 Bêta |
| TikTok Ads | `pip install miniagent[tiktok]` | 10 | 📋 Prévu |
| Toutes les plateformes | `pip install miniagent[all]` | 80+ | — |

### Intégration Claude Code

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
# Cursor — ajouter dans .cursor/mcp.json (même format que ci-dessus)
# Windsurf — ajouter dans .windsurf/mcp.json
# OpenAI Agents SDK:
from agents import Agent
from agents.mcp import MCPServerStdio

server = MCPServerStdio(command="python", args=["-m", "miniagent.mcp.google_ads"])
agent = Agent(name="ad-agent", mcp_servers=[server])
```

---

## Compétences d’agent

Les compétences fonctionnent avec Claude Code, Codex, Gemini CLI, Cursor et tout agent compatible avec le standard SKILL.md.

| Compétence | Description | API requise ? |
|-------|-------------|-----------|
| `google-ads-analysis` | Analyse des performances, motifs GAQL, détection d’anomalies | Oui (via MCP) |
| `google-ads-audit` | Audit de compte sur 7 dimensions avec gravité, plans 30/60/90 jours | Oui (via MCP) |
| `google-ads-write` | Écritures sécurisées via le protocole Confirm-Execute-Postcheck (CEP) | Oui (via MCP) |
| `google-ads-math` | Calculs PPC — CPA, ROAS, projections de budget, seuil de rentabilité | Non |
| `google-ads-mcp` | Guide d’installation du serveur MCP pour l’API en direct | Guide d’installation |

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

## Données d’entraînement

Toutes les données d’entraînement sont open source et spécifiques au domaine publicitaire :

| Jeu de données | Description | Taille | Étape |
|---------|-------------|------|-------|
| `pretrain_ads.jsonl` | Corpus de connaissances publicitaires — docs Google Ads, bonnes pratiques PPC, contenu industriel | ~500MB | Pré-entraînement |
| `sft_ads.jsonl` | Paires instruction–réponse pour tâches PPC | ~50MB | SFT |
| `sft_gaql.jsonl` | Paires de requêtes GAQL — langage naturel → GAQL | ~10MB | SFT |
| `dpo_ads.jsonl` | Paires de conseils publicitaires bons vs mauvais | ~20MB | DPO |
| `distill_ads.jsonl` | Distillé depuis Claude/GPT sur des tâches publicitaires | ~100MB | Distill |

```bash
# Télécharger tous les jeux de données
python scripts/download_data.py --all

# Ou des étapes spécifiques
python scripts/download_data.py --pretrain
python scripts/download_data.py --sft
python scripts/download_data.py --dpo
```

---

## Benchmarks d’évaluation

MiniAgent inclut des benchmarks spécifiques à la publicité (les benchmarks LLM classiques ne couvrent pas les connaissances PPC) :

| Benchmark | Ce qui est testé | Métriques |
|-----------|--------------|---------|
| **Ad-Bench** | Connaissances publicitaires générales | Précision, F1 |
| **GAQL-Eval** | Précision de génération de requêtes GAQL | Correspondance exacte, sémantique |
| **Campaign-Struct** | Recommandations de structure de campagne | Accord avec des experts |
| **Cross-Platform** | Normalisation des métriques entre plateformes | Score de cohérence |
| **Audit-Eval** | Qualité d’audit de compte | Couverture, actionnabilité, précision |

```bash
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
python eval/gaql_eval.py --model ./checkpoints/sft_512.pth
```

---

## Installation en un clic

```bash
curl -sSL https://raw.githubusercontent.com/itallstartedwithaidea/miniagent/main/scripts/one_click_install.sh | bash
```

Installe tout : dépendances Python, poids du modèle, serveurs MCP, compétences Claude Code, et lance la démo Streamlit.

---

## Compatibilité

| Plateforme | Statut | Comment |
|----------|--------|-----|
| Claude Code | ✅ | Compétences + serveurs MCP |
| Claude Desktop | ✅ | Serveurs MCP via configuration |
| Cursor | ✅ | Serveurs MCP + .cursor/mcp.json |
| Windsurf | ✅ | Serveurs MCP |
| OpenAI Codex | ✅ | Compétences dans .codex/skills/ |
| Gemini CLI | ✅ | Compétences dans .gemini/skills/ |
| OpenAI Agents SDK | ✅ | MCPServerStdio |
| LangChain | ✅ | langchain-mcp-adapters |
| Ollama | ✅ | ollama run miniagent |
| vLLM | ✅ | vllm serve |
| llama.cpp | ✅ | conversion GGUF incluse |
| FastGPT | ✅ | API compatible OpenAI |
| Open-WebUI | ✅ | API compatible OpenAI |
| Dify | ✅ | API compatible OpenAI |

---

## Attribution

Ce projet s’appuie sur le travail de nombreux contributeurs open source :

| Projet | Auteur | Licence | Contribution |
|---------|--------|---------|-------------|
| [minimind](https://github.com/jingyaogong/minimind) | JingyaoGong | Apache 2.0 | Architecture du modèle de base, pipeline d’entraînement, framework tokenizer |
| [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) | Ernesto Cohnen | MIT | Persistance des jetons OAuth, normalisation des customer ID |
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | Google LLC | Apache 2.0 | Pattern coordinateur singleton, sortie field_mask |
| [google-marketing-solutions/google_ads_mcp](https://github.com/google-marketing-solutions/google_ads_mcp) | Google LLC | Apache 2.0 | omit_unselected_resource_names, outils doc comme outils MCP |
| [gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server) | GoMarble AI | MIT | Parcours MCC, Keyword Planner, double transport |
| [garrytan/gstack](https://github.com/garrytan/gstack) | Garry Tan | MIT | Patterns d’architecture de compétences, conception d’agents par rôles |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Steph Ango | MIT | standard SKILL.md, format multi-plateforme |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic | Apache 2.0 | Framework de compétences, protocole marketplace de plugins |

---

## Écosystème

MiniAgent fait partie d’un écosystème open source plus large d’intelligence publicitaire :

| Dépôt | Rôle |
|------|-------------|
| **miniagent** (ce dépôt) | Tout — modèle entraînable + serveurs MCP + compétences + hub |
| [google-ads-mcp-server](https://github.com/itallstartedwithaidea/google-ads-mcp-server) | MCP Google Ads autonome (29 outils) |
| [google-ads-skills](https://github.com/itallstartedwithaidea/google-ads-skills) | Compétences Claude Code Google Ads autonomes |
| [advertising-hub](https://github.com/itallstartedwithaidea/advertising-hub) | Connecteur horizontal 14 plateformes |
| [google-ads-api-agent](https://github.com/itallstartedwithaidea/google-ads-api-agent) | Agent Google Ads complet avec FastAPI |
| [creative-asset-validator](https://github.com/itallstartedwithaidea/creative-asset-validator) | Analyse créative assistée par IA sur 50+ plateformes |
| [ContextOS](https://github.com/itallstartedwithaidea/ContextOS) | Plateforme d’intelligence contextuelle (6 primitives cognitives) |
| [writing-agent](https://github.com/itallstartedwithaidea/writing-agent) | Ghost Protocol pour un contenu de qualité humaine |
| [ai-agents-crash-course](https://github.com/itallstartedwithaidea/ai-agents-crash-course) | Crash course agents (42 pages, MIT) |
| [agency-agents](https://github.com/itallstartedwithaidea/agency-agents) | Agence IA complète — du front à la communauté |

---

## Licence

Apache 2.0 — comme minimind. Voir [LICENSE](LICENSE).

---

## Auteur

**John Williams** · Senior Paid Media Specialist · [Seer Interactive](https://seerinteractive.com)
Fondateur, [googleadsagent.ai](https://googleadsagent.ai) · [It All Started With A Idea](https://itallstartedwithaidea.com)

Plus de 15 ans dans la publicité digitale enterprise (plus de 48 M$ de dépenses annuelles) sur Google, Meta, Microsoft, Amazon.
Speaker : Hero Conf · Publié : Search Engine Land · Conçu pour le praticien que la plateforme a oublié.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-johnmichaelwilliams-blue)](https://linkedin.com/in/johnmichaelwilliams)
[![GitHub](https://img.shields.io/badge/GitHub-itallstartedwithaidea-black)](https://github.com/itallstartedwithaidea)
[![Website](https://img.shields.io/badge/Web-itallstartedwithaidea.com-green)](https://itallstartedwithaidea.com)

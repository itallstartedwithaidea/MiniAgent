<div align="center">

# MiniAgent

### Универсальный агент-помощник. Обучение с нуля. Работает везде.

[English](../../README.md) | [中文](../zh/README.md) | [Русский](./README.md) | [Italiano](../it/README.md) | [Español](../es/README.md)

**Обучите собственный рекламный ИИ с нуля. 2 часа. Одна видеокарта. Ваши данные.**

На основе [minimind](https://github.com/jingyaogong/minimind) (Apache 2.0, 42k звёзд) · 14 рекламных платформ · 29 MCP-инструментов · 5 навыков Claude Code

</div>

---

## Что это?

MiniAgent — три проекта в одном репозитории:

1. **Обучаемый рекламный ИИ** — форк minimind (26M параметров), переобученный на данных рекламной индустрии. Модель изучает GAQL, структуру кампаний, стратегии ставок, математику PPC и анализ креативов. Обучение за 2 часа на одной 3090.

2. **Продакшн MCP-серверы** — 14 коннекторов рекламных платформ (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn и др.), 80+ инструментов.

3. **Платформа навыков для агентов** — навыки для Claude Code, Codex, Gemini CLI для анализа рекламы, аудита, безопасных операций записи, расчётов PPC.

## Быстрый старт

```bash
ollama run itallstartedwithaidea/miniagent
pip install miniagent[google]
```

## Лицензия

Apache 2.0. Автор: **John Williams** · 15+ лет в управлении рекламными бюджетами ($48M+/год)

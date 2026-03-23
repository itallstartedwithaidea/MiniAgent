# MiniAgent — Trainable Advertising AI

Train a 26M-parameter advertising AI from scratch in 2 hours on one GPU ($0.40).
Then use it with 14 ad platform MCP servers (80+ tools) and 5 agent skills.

## What It Does

MiniAgent is three things in one repo:

1. **A trainable model** — Learns GAQL, campaign structure, bid strategy, PPC math
2. **MCP servers** — 14 ad platforms (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, TikTok, Snapchat, Pinterest, Criteo, AdRoll, Quora, X/Twitter)
3. **Agent skills** — 5 Claude Code / Codex / Gemini CLI skills for advertising

## Quick Start

```bash
git clone https://github.com/itallstartedwithaidea/MiniAgent.git
cd MiniAgent

# Chat (no GPU needed — knowledge-base mode)
make chat

# Train your own model (2 hours, 1 GPU)
make download-data
make train

# Run benchmarks
make eval

# Web demo
make demo
```

## Based On

- [minimind](https://github.com/jingyaogong/minimind) (42k stars) — Base model architecture
- Apache 2.0 License

## Built By

[John Williams](https://github.com/itallstartedwithaidea) — 15+ years enterprise paid media, $48M+ annual ad spend. Speaker at Hero Conf, published in Search Engine Land.

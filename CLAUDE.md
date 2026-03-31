# MiniAgent — Claude Code Project Instructions

## What This Is
MiniAgent is the everything repo for advertising AI. Trainable model + 14 platform MCP servers + agent skills.

## Architecture
- `model/` — Trainable LLM (fork of minimind, 26M-145M params)
- `trainer/` — Full training pipeline (pretrain → SFT → LoRA → DPO → GRPO)
- `mcp_servers/` — MCP servers for 14 ad platforms (80+ tools)
- `skills/` — Claude Code / Codex / Gemini CLI skills
- `hub/` — 14-platform API connectors with normalized data layer
- `eval/` — Advertising-specific benchmarks
- `dataset/` — Training data (advertising domain)

## Code Style
- Python 3.10+, type hints required
- Use `ruff` for formatting
- All MCP tools use FastMCP decorators
- Google Ads API v23 (current)
- All costs in micros (divide by 1,000,000 for dollars)

## Key Patterns
- MCP servers use singleton coordinator pattern (one FastMCP instance per module)
- Write operations use CEP protocol: Confirm → Execute → Postcheck
- Auth supports 3 strategies: injected token → OAuth JSON → ADC fallback
- GAQL queries use `field_mask.paths` for output, `omit_unselected_resource_names` for noise reduction

## Testing
```bash
pytest tests/
python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
```

## Training
```bash
python trainer/pretrain.py --dim 512 --n_layers 8
python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth
```

## Available Skills
- `/google-ads-analysis` — Campaign performance analysis
- `/google-ads-audit` — 7-dimension account audit
- `/google-ads-write` — Safe write operations
- `/google-ads-math` — PPC calculations
- `/google-ads-mcp` — MCP server setup

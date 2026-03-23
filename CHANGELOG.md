# Changelog

## [0.2.0] - 2026-03-22
### Added
- All 14 MCP server scaffolds (Google, Meta, Microsoft, Amazon, Reddit, TradeDesk, LinkedIn, TikTok, Snapchat, Pinterest, Criteo, AdRoll, Quora, X/Twitter)
- Hub connectors for all 14 platforms with normalized data layer
- Full test suite (model, eval, MCP)
- Streamlit web demo
- Data downloader script
- DPO and LoRA trainer stubs
- Architecture diagrams (SVG)
- Logo (SVG)
- .mcp.json example for Claude Code/Cursor
- Ollama Modelfile
- CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
- GitHub issue templates (bug, feature, platform request)
- Dependabot configuration
- Makefile with common commands
- Example Jupyter notebook

### Fixed
- Broken logo image link in README
- Missing __main__.py files for MCP servers
- Missing __init__.py files for packages

## [0.1.1] - 2026-03-22
### Added
- Web demo (Streamlit)
- Data downloader
- CLI entry point
- DPO/LoRA trainer stubs

## [0.1.0] - 2026-03-22
### Added
- Initial release
- Model architecture (26M-145M params, Llama-compatible)
- Pretrain + SFT trainers
- Google Ads MCP server (29 tools)
- Meta Ads MCP server (18 tools)
- 5 Claude Code skills
- Ad-Bench evaluation suite
- README in 5 languages
- Wiki (6 pages)

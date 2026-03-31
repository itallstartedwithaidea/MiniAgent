# Contributing to MiniAgent

Thanks for your interest in contributing! Here's how to get started.

## Quick Start

```bash
git clone https://github.com/itallstartedwithaidea/MiniAgent.git
cd MiniAgent
pip install -e ".[dev]"
pytest tests/
```

## What to Contribute

### High Priority
- **Platform connectors** — Add a new ad platform to `hub/` and `mcp_servers/`
- **Training data** — Curate advertising-domain text for `dataset/`
- **Benchmarks** — Add evaluation tests to `eval/`

### Always Welcome
- Bug fixes and documentation improvements
- New Claude Code skills in `skills/`
- Translations in `locales/`

## Adding a New Platform

1. Create `mcp_servers/your_platform/__init__.py` with FastMCP tools
2. Create `hub/your_platform/__init__.py` with a connector class
3. Add tests in `tests/test_your_platform.py`
4. Update `pyproject.toml` optional dependencies
5. Update README platform table

## Code Style
- Python 3.10+, type hints required
- Format with `ruff`
- All MCP tools use FastMCP `@mcp.tool()` decorators
- Write operations must use CEP protocol (Confirm → Execute → Postcheck)

## Pull Requests
1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run `pytest tests/` and `ruff check .`
5. Submit a PR with a clear description

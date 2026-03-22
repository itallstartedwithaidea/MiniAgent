#!/bin/bash
# ============================================================================
# MiniAgent — One-Click Install
# The Cowork Agent for Everything
# ============================================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

echo -e "${BOLD}"
echo "  ███╗   ███╗██╗███╗   ██╗██╗ █████╗  ██████╗ ███████╗███╗   ██╗████████╗"
echo "  ████╗ ████║██║████╗  ██║██║██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝"
echo "  ██╔████╔██║██║██╔██╗ ██║██║███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   "
echo "  ██║╚██╔╝██║██║██║╚██╗██║██║██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   "
echo "  ██║ ╚═╝ ██║██║██║ ╚████║██║██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   "
echo "  ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   "
echo -e "${NC}"
echo -e "${BOLD}The Cowork Agent for Everything${NC}"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="macos";;
    *)       echo -e "${RED}Unsupported OS: $OS${NC}"; exit 1;;
esac
echo -e "${GREEN}✔ Platform: $PLATFORM${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✘ Python 3.10+ required. Install from python.org${NC}"
    exit 1
fi
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✔ Python: $PYVER${NC}"

# Install core
echo ""
echo -e "${YELLOW}▸ Installing MiniAgent core...${NC}"
pip install -e ".[all]" --quiet

# Install training dependencies (optional)
read -p "Install training dependencies? (GPU required) [y/N]: " TRAIN
if [[ "$TRAIN" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}▸ Installing training deps...${NC}"
    pip install -e ".[train]" --quiet
fi

# Install Claude Code skills
if command -v claude &> /dev/null; then
    echo ""
    echo -e "${YELLOW}▸ Installing Claude Code skills...${NC}"
    mkdir -p ~/.claude/skills/miniagent
    cp -r skills/* ~/.claude/skills/miniagent/
    echo -e "${GREEN}✔ Skills installed to ~/.claude/skills/miniagent/${NC}"

    # Register MCP servers
    echo -e "${YELLOW}▸ Registering MCP servers with Claude Code...${NC}"
    claude mcp add miniagent-google --scope user -- python -m miniagent.mcp.google_ads 2>/dev/null || true
    echo -e "${GREEN}✔ MCP server registered (configure credentials in ~/.miniagent/config.toml)${NC}"
fi

# Install Codex skills
if command -v codex &> /dev/null; then
    echo ""
    echo -e "${YELLOW}▸ Installing Codex skills...${NC}"
    mkdir -p ~/.codex/skills/miniagent
    cp -r skills/* ~/.codex/skills/miniagent/
    echo -e "${GREEN}✔ Skills installed to ~/.codex/skills/miniagent/${NC}"
fi

# Download model weights (optional)
read -p "Download pre-trained advertising model? (~500MB) [y/N]: " DL
if [[ "$DL" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}▸ Downloading model weights...${NC}"
    python scripts/download_data.py --model
    echo -e "${GREEN}✔ Model downloaded${NC}"
fi

# Summary
echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  ✅ MiniAgent installed successfully!${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${BOLD}Chat:${NC}    python -m miniagent.chat"
echo -e "  ${BOLD}API:${NC}     python -m miniagent.scripts.serve_openai_api"
echo -e "  ${BOLD}Demo:${NC}    streamlit run scripts/web_demo.py"
echo -e "  ${BOLD}Train:${NC}   python trainer/pretrain.py --dim 512 --n_layers 8"
echo ""
echo -e "  ${BOLD}Docs:${NC}    https://github.com/itallstartedwithaidea/miniagent/wiki"
echo ""

#!/bin/bash
#
# MiniAgent — Train & Deploy in One Command
#
# Run this on a cloud GPU (3090+) or any machine with CUDA/MPS.
# Trains an advertising AI from scratch (or fine-tunes minimind), then
# converts and uploads to HuggingFace + Ollama.
#
# === Quick Start (cloud GPU) ===
#
#   # On runpod.io or vast.ai — rent a 3090 (~$0.40/hr), then:
#   git clone https://github.com/itallstartedwithaidea/MiniAgent.git
#   cd MiniAgent
#   export HF_TOKEN=hf_your_token_here     # optional: for HuggingFace upload
#   bash scripts/train_and_deploy.sh
#
# === Configuration (env vars) ===
#
#   TRAIN_MODE    "scratch" (full pretrain+SFT) or "finetune" (SFT only on minimind base)
#                 Default: scratch
#   MODEL_DIM     Hidden size — 512 (26M params) or 768 (104M params)
#                 Default: 512
#   N_LAYERS      Transformer layers — 8 (for 512d) or 16 (for 768d)
#                 Default: 8
#   PRETRAIN_EPOCHS  Number of pretrain epochs. Default: 3
#   SFT_EPOCHS       Number of SFT epochs. Default: 5
#   BATCH_SIZE       Batch size. Default: 32 (reduce to 16 if OOM)
#   HF_REPO       HuggingFace repo for upload. Default: itallstartedwithaidea/MiniAgent-26M
#   HF_TOKEN      HuggingFace auth token (skip upload if not set)
#   SKIP_UPLOAD   Set to 1 to skip HuggingFace upload
#
set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────
# TRAIN_MODE: "scratch" = from zero, "finetune" = SFT only on minimind base,
#             "combined" = minimind base + advertising pretrain + SFT (best quality)
TRAIN_MODE="${TRAIN_MODE:-combined}"
MODEL_DIM="${MODEL_DIM:-512}"
N_LAYERS="${N_LAYERS:-8}"
PRETRAIN_EPOCHS="${PRETRAIN_EPOCHS:-3}"
SFT_EPOCHS="${SFT_EPOCHS:-5}"
BATCH_SIZE="${BATCH_SIZE:-32}"
HF_REPO="${HF_REPO:-itallstartedwithaidea/MiniAgent-26M}"
SKIP_UPLOAD="${SKIP_UPLOAD:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

START_TIME=$(date +%s)

# ─── Detect GPU ───────────────────────────────────────────────────────
detect_device() {
    if command -v nvidia-smi &>/dev/null && nvidia-smi &>/dev/null; then
        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
        GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader | head -1)
        echo "  GPU: $GPU_NAME ($GPU_MEM)" >&2
        echo "cuda"
    elif python3 -c "import torch; assert torch.backends.mps.is_available()" 2>/dev/null; then
        echo "  GPU: Apple Silicon (MPS)" >&2
        echo "mps"
    else
        echo "  GPU: None (CPU only — training will be slow)" >&2
        echo "cpu"
    fi
}

# ─── Banner ───────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         MiniAgent — Train & Deploy Pipeline                 ║"
echo "║         Advertising AI from Zero to Ollama                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Mode:   $TRAIN_MODE"
echo "  Model:  ${MODEL_DIM}d × ${N_LAYERS}L"
DEVICE=$(detect_device)
echo "  Device: $DEVICE"
echo ""

# ─── Step 0: Install Dependencies ─────────────────────────────────────
echo "━━━ Step 0/6: Installing dependencies ━━━"
pip install -q torch transformers sentencepiece huggingface_hub tqdm numpy 2>/dev/null || true
pip install -q -e . 2>/dev/null || pip install -q -r requirements.txt 2>/dev/null || true
echo "  Done."
echo ""

# ─── Step 1: Download Tokenizer + Generate Data ───────────────────────
echo "━━━ Step 1/6: Downloading tokenizer + generating training data ━━━"
python scripts/download_data.py --all
echo ""

# ─── Step 2: Train ────────────────────────────────────────────────────
if [ "$TRAIN_MODE" = "finetune" ]; then
    echo "━━━ Step 2/6: Fine-tune mode — downloading minimind base model ━━━"
    python scripts/download_data.py --base-model

    echo ""
    echo "━━━ Step 3/6: SFT on advertising data ━━━"
    python trainer/sft.py \
        --load_from ./minimind_base \
        --epochs "$SFT_EPOCHS" \
        --batch_size 8 \
        --max_length 512 \
        --device "$DEVICE"

elif [ "$TRAIN_MODE" = "combined" ]; then
    echo "━━━ Step 2/6: Combined mode — minimind base + advertising pretrain ━━━"
    echo "  Downloading minimind model, then continuing pretrain on ad data..."
    python trainer/pretrain.py \
        --init_from "jingyaogong/MiniMind2" \
        --epochs "$PRETRAIN_EPOCHS" \
        --batch_size 8 \
        --max_length 320 \
        --device "$DEVICE"

    # Detect the dim from the downloaded model config
    MODEL_DIM=$(python -c "import json; c=json.load(open('./minimind_base/config.json')); print(c.get('hidden_size',512))" 2>/dev/null || echo "768")

    echo ""
    echo "━━━ Step 3/6: SFT — learning to follow ad instructions ━━━"
    python trainer/sft.py \
        --load_from "./checkpoints/pretrain_${MODEL_DIM}.pth" \
        --epochs "$SFT_EPOCHS" \
        --batch_size 4 \
        --max_length 512 \
        --device "$DEVICE"

else
    echo "━━━ Step 2/6: Pretraining — learning advertising language ━━━"
    python trainer/pretrain.py \
        --dim "$MODEL_DIM" \
        --n_layers "$N_LAYERS" \
        --epochs "$PRETRAIN_EPOCHS" \
        --batch_size "$BATCH_SIZE" \
        --device "$DEVICE"

    echo ""
    echo "━━━ Step 3/6: SFT — learning to follow instructions ━━━"
    python trainer/sft.py \
        --load_from "./checkpoints/pretrain_${MODEL_DIM}.pth" \
        --epochs "$SFT_EPOCHS" \
        --batch_size 8 \
        --max_length 512 \
        --device "$DEVICE"
fi
echo ""

# ─── Step 4: Convert to HuggingFace Format ────────────────────────────
echo "━━━ Step 4/6: Converting to HuggingFace Transformers format ━━━"
CKPT="./checkpoints/sft_${MODEL_DIM}.pth"
OUTPUT_DIR="./MiniAgent-${MODEL_DIM}"

if [ ! -f "$CKPT" ]; then
    echo "ERROR: Checkpoint not found: $CKPT"
    exit 1
fi

python scripts/convert_model.py \
    --input "$CKPT" \
    --output "$OUTPUT_DIR" \
    --format transformers

# Copy tokenizer files into the model directory
if [ -d "./model/tokenizer" ]; then
    cp ./model/tokenizer/tokenizer.json "$OUTPUT_DIR/" 2>/dev/null || true
    cp ./model/tokenizer/tokenizer_config.json "$OUTPUT_DIR/" 2>/dev/null || true
    cp ./model/tokenizer/special_tokens_map.json "$OUTPUT_DIR/" 2>/dev/null || true
    echo "  Tokenizer files copied to $OUTPUT_DIR"
fi
echo ""

# ─── Step 5: Upload to HuggingFace ────────────────────────────────────
echo "━━━ Step 5/6: HuggingFace upload ━━━"
if [ "$SKIP_UPLOAD" = "1" ]; then
    echo "  Skipped (SKIP_UPLOAD=1)"
elif [ -z "${HF_TOKEN:-}" ]; then
    echo "  Skipped (no HF_TOKEN set)"
    echo "  To upload later:"
    echo "    export HF_TOKEN=hf_your_token"
    echo "    huggingface-cli upload $HF_REPO $OUTPUT_DIR"
else
    pip install -q huggingface_hub 2>/dev/null || true
    echo "$HF_TOKEN" | huggingface-cli login --token "$HF_TOKEN" 2>/dev/null || true
    huggingface-cli upload "$HF_REPO" "$OUTPUT_DIR" && echo "  Uploaded to https://huggingface.co/$HF_REPO" || echo "  Upload failed — you can retry manually"
fi
echo ""

# ─── Step 6: GGUF + Ollama ────────────────────────────────────────────
echo "━━━ Step 6/6: GGUF conversion (for Ollama) ━━━"
if command -v ollama &>/dev/null; then
    python scripts/convert_model.py \
        --input "$OUTPUT_DIR" \
        --output "./checkpoints/miniagent.gguf" \
        --format gguf
    echo ""
    echo "  To create Ollama model:"
    echo "    ollama create miniagent -f Modelfile"
    echo "    ollama run miniagent"
else
    echo "  Ollama not installed. To use with Ollama later:"
    echo "    1. Install: curl -fsSL https://ollama.com/install.sh | sh"
    echo "    2. Convert: python scripts/convert_model.py --input $OUTPUT_DIR --output ./checkpoints/miniagent.gguf --format gguf"
    echo "    3. Create:  ollama create miniagent -f Modelfile"
    echo "    4. Run:     ollama run miniagent"
fi
echo ""

# ─── Summary ──────────────────────────────────────────────────────────
END_TIME=$(date +%s)
ELAPSED=$(( END_TIME - START_TIME ))
MINUTES=$(( ELAPSED / 60 ))
SECONDS_REM=$(( ELAPSED % 60 ))

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Training Complete!                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Time:   ${MINUTES}m ${SECONDS_REM}s"
echo "  Model:  $OUTPUT_DIR"
echo "  Params: $(python -c "
import torch, sys
sys.path.insert(0, '.')
from model.model_miniagent import MiniAgentModel
ckpt = torch.load('$CKPT', map_location='cpu')
m = MiniAgentModel(ckpt['config'])
print(f'{m.count_params():.1f}M')
" 2>/dev/null || echo "~26M")"
echo ""
echo "  Files:"
echo "    HuggingFace: $OUTPUT_DIR/"
ls -la "$OUTPUT_DIR/" 2>/dev/null | grep -v "^total" | awk '{print "      " $NF "  (" $5 " bytes)"}' || true
echo ""
echo "  Next steps:"
echo "    • Test locally:  python eval_llm.py --load_from $OUTPUT_DIR"
if [ -z "${HF_TOKEN:-}" ]; then
echo "    • Upload:        HF_TOKEN=hf_xxx huggingface-cli upload $HF_REPO $OUTPUT_DIR"
fi
echo "    • Ollama:        ollama create miniagent -f Modelfile && ollama run miniagent"
echo "    • vLLM:          vllm serve $OUTPUT_DIR --served-model-name miniagent"
echo ""

# Estimate cloud cost
if command -v nvidia-smi &>/dev/null; then
    HOURLY_RATE="0.40"
    HOURS=$(echo "scale=2; $ELAPSED / 3600" | bc 2>/dev/null || echo "?")
    COST=$(echo "scale=2; $HOURS * $HOURLY_RATE" | bc 2>/dev/null || echo "?")
    echo "  Estimated cloud cost: ~\$${COST} (${HOURS}h × \$${HOURLY_RATE}/hr on 3090)"
fi
echo ""

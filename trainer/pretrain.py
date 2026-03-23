"""
MiniAgent Pretrain — Stage 1: Learn Advertising Language

Based on minimind's pretrain pipeline (Apache 2.0).
Trains on advertising corpus: Google Ads docs, PPC best practices,
GAQL syntax, cross-platform terminology.

Usage:
    python trainer/pretrain.py --dim 512 --n_layers 8
    python trainer/pretrain.py --dim 768 --n_layers 16 --from_resume 1
"""

import os
import sys
import json
import math
import time
import argparse
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from contextlib import nullcontext

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.model_miniagent import MiniAgentModel, MiniAgentConfig


class PretrainDataset(Dataset):
    """Advertising pretrain dataset — JSONL format."""
    def __init__(self, data_path: str, tokenizer, max_length: int = 512):
        self.samples = []
        self.max_length = max_length
        self.tokenizer = tokenizer

        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                text = item.get("text", "")
                if len(text) > 10:
                    self.samples.append(text)

        print(f"Loaded {len(self.samples)} pretrain samples from {data_path}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        text = self.samples[idx]
        tokens = self.tokenizer.encode(text, add_special_tokens=True)
        tokens = tokens[:self.max_length]

        # Pad to max_length
        padding = self.max_length - len(tokens)
        input_ids = tokens + [0] * padding
        labels = tokens + [-100] * padding  # -100 = ignore in loss

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


def get_lr(step: int, warmup_steps: int, max_steps: int,
           lr_max: float = 1e-4, lr_min: float = 1e-5) -> float:
    """Cosine learning rate schedule with warmup."""
    if step < warmup_steps:
        return lr_max * step / warmup_steps
    progress = (step - warmup_steps) / max(1, max_steps - warmup_steps)
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * progress))


def main():
    parser = argparse.ArgumentParser(description="MiniAgent Pretrain")
    parser.add_argument("--dim", type=int, default=512, help="Hidden size")
    parser.add_argument("--n_layers", type=int, default=8, help="Number of layers")
    parser.add_argument("--data", type=str, default="./dataset/pretrain_ads.jsonl")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--save_dir", type=str, default="./checkpoints")
    parser.add_argument("--from_resume", type=int, default=0)
    parser.add_argument("--init_from", type=str, default=None,
                        help="Initialize from a transformers model (e.g. jingyaogong/MiniMind2 or local path)")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)

    # Load from minimind/transformers model OR create from scratch
    if args.init_from:
        config, model = _load_from_transformers(args.init_from, args.device)
        args.dim = config.hidden_size
        print(f"Initialized from {args.init_from} — continuing pretrain on advertising data")
    else:
        config = MiniAgentConfig(
            hidden_size=args.dim,
            num_hidden_layers=args.n_layers,
            num_attention_heads=args.dim // 64,
            num_key_value_heads=max(1, args.dim // 256),
        )
        model = MiniAgentModel(config).to(args.device)

    # Resume from checkpoint
    ckpt_path = os.path.join(args.save_dir, f"pretrain_{args.dim}.pth")
    start_epoch = 0
    if args.from_resume and os.path.exists(ckpt_path):
        checkpoint = torch.load(ckpt_path, map_location=args.device, weights_only=False)
        model.load_state_dict(checkpoint["model"])
        start_epoch = checkpoint.get("epoch", 0) + 1
        print(f"Resumed from epoch {start_epoch}")

    # Tokenizer — use minimind's 6400-vocab tokenizer
    tokenizer = _load_tokenizer()
    if tokenizer is None:
        print("ERROR: No tokenizer found. Run: python scripts/download_data.py --tokenizer")
        sys.exit(1)

    # Dataset
    if not os.path.exists(args.data):
        print(f"Dataset not found: {args.data}")
        print("Run: python scripts/download_data.py --pretrain")
        print("Or create a sample dataset for testing...")
        _create_sample_dataset(args.data)

    dataset = PretrainDataset(args.data, tokenizer, args.max_length)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True,
                            num_workers=2, pin_memory=True, drop_last=True)

    # Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)

    # Mixed precision
    use_amp = args.device == "cuda"
    scaler = torch.amp.GradScaler("cuda") if use_amp else None
    ctx = torch.amp.autocast("cuda", dtype=torch.bfloat16) if use_amp else nullcontext()

    # Training loop
    total_steps = len(dataloader) * args.epochs
    warmup_steps = min(1000, total_steps // 10)
    global_step = 0

    print(f"\n{'='*60}")
    print(f"MiniAgent Pretrain — Stage 1: Advertising Language")
    print(f"{'='*60}")
    print(f"Model: {model.count_params():.2f}M params (dim={args.dim}, layers={args.n_layers})")
    print(f"Data: {len(dataset)} samples")
    print(f"Epochs: {args.epochs} | Batch: {args.batch_size} | Steps: {total_steps}")
    print(f"Device: {args.device}")
    print(f"{'='*60}\n")

    model.train()
    for epoch in range(start_epoch, args.epochs):
        epoch_loss = 0.0
        epoch_start = time.time()

        for step, batch in enumerate(dataloader):
            input_ids = batch["input_ids"].to(args.device)
            labels = batch["labels"].to(args.device)

            # LR schedule
            lr = get_lr(global_step, warmup_steps, total_steps, args.lr)
            for param_group in optimizer.param_groups:
                param_group["lr"] = lr

            with ctx:
                out = model(input_ids, labels=labels)
                loss = out["loss"]

            if use_amp:
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scaler.step(optimizer)
                scaler.update()
            else:
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()

            optimizer.zero_grad(set_to_none=True)
            epoch_loss += loss.item()
            global_step += 1

            if step % 100 == 0:
                elapsed = time.time() - epoch_start
                tokens_per_sec = (step + 1) * args.batch_size * args.max_length / elapsed
                print(f"  Epoch {epoch+1}/{args.epochs} | Step {step}/{len(dataloader)} | "
                      f"Loss: {loss.item():.4f} | LR: {lr:.2e} | "
                      f"{tokens_per_sec:.0f} tok/s")

        avg_loss = epoch_loss / len(dataloader)
        elapsed = time.time() - epoch_start
        print(f"\n  Epoch {epoch+1} complete — Avg Loss: {avg_loss:.4f} | Time: {elapsed:.1f}s\n")

        # Save checkpoint
        torch.save({
            "model": model.state_dict(),
            "config": config,
            "epoch": epoch,
            "loss": avg_loss,
        }, ckpt_path)
        print(f"  Saved: {ckpt_path}")

    print(f"\n{'='*60}")
    print(f"Pretrain complete! Model saved to {ckpt_path}")
    print(f"Next: python trainer/sft.py --load_from {ckpt_path}")
    print(f"{'='*60}")


def _load_from_transformers(model_path: str, device: str = "cpu"):
    """Load a minimind/Llama-format transformers model and convert weight names to MiniAgent format."""
    from safetensors.torch import load_file as load_safetensors

    # Download from HuggingFace if not a local path
    if not os.path.exists(model_path):
        print(f"Downloading {model_path} from HuggingFace...")
        try:
            from huggingface_hub import snapshot_download
            model_path = snapshot_download(model_path, local_dir=f"./minimind_base")
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)

    # Load config
    config_path = os.path.join(model_path, "config.json")
    with open(config_path) as f:
        cfg = json.load(f)

    config = MiniAgentConfig(
        hidden_size=cfg.get("hidden_size", 512),
        num_hidden_layers=cfg.get("num_hidden_layers", 8),
        num_attention_heads=cfg.get("num_attention_heads", 8),
        num_key_value_heads=cfg.get("num_key_value_heads", 2),
        intermediate_size=cfg.get("intermediate_size", 1408),
        max_position_embeddings=cfg.get("max_position_embeddings", 2048),
        rms_norm_eps=cfg.get("rms_norm_eps", 1e-5),
        rope_base=cfg.get("rope_theta", 10000.0),
        vocab_size=cfg.get("vocab_size", 6400),
    )

    # Load weights (safetensors or pytorch)
    safetensors_path = os.path.join(model_path, "model.safetensors")
    pytorch_path = os.path.join(model_path, "pytorch_model.bin")
    if os.path.exists(safetensors_path):
        state_dict = load_safetensors(safetensors_path)
    elif os.path.exists(pytorch_path):
        state_dict = torch.load(pytorch_path, map_location="cpu", weights_only=True)
    else:
        print(f"No model weights found in {model_path}")
        sys.exit(1)

    # Llama → MiniAgent weight name mapping
    llama_to_miniagent = {
        "model.embed_tokens.weight": "embed_tokens.weight",
        "model.norm.weight": "norm.weight",
        "lm_head.weight": "lm_head.weight",
    }
    layer_map = {
        "self_attn.q_proj.weight": "attention.q_proj.weight",
        "self_attn.k_proj.weight": "attention.k_proj.weight",
        "self_attn.v_proj.weight": "attention.v_proj.weight",
        "self_attn.o_proj.weight": "attention.o_proj.weight",
        "mlp.gate_proj.weight": "feed_forward.gate_proj.weight",
        "mlp.up_proj.weight": "feed_forward.up_proj.weight",
        "mlp.down_proj.weight": "feed_forward.down_proj.weight",
        "input_layernorm.weight": "attention_norm.weight",
        "post_attention_layernorm.weight": "ffn_norm.weight",
    }

    converted = {}
    for name, tensor in state_dict.items():
        if name in llama_to_miniagent:
            converted[llama_to_miniagent[name]] = tensor
        else:
            matched = False
            for old_suffix, new_suffix in layer_map.items():
                if old_suffix in name:
                    layer_num = name.split(".")[2]
                    new_name = f"layers.{layer_num}.{new_suffix}"
                    converted[new_name] = tensor
                    matched = True
                    break
            if not matched:
                converted[name] = tensor

    model = MiniAgentModel(config)
    model.load_state_dict(converted, strict=False)
    model = model.to(device)
    print(f"Loaded {len(converted)} tensors from transformers model ({model.count_params():.1f}M params)")

    # Copy tokenizer to ./model/tokenizer/ so training scripts find it
    tokenizer_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model", "tokenizer")
    os.makedirs(tokenizer_dir, exist_ok=True)
    import shutil
    for tf in ["tokenizer.json", "tokenizer_config.json", "special_tokens_map.json",
               "tokenizer.model", "merges.txt", "vocab.json"]:
        src = os.path.join(model_path, tf)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(tokenizer_dir, tf))
    print(f"Tokenizer copied to {tokenizer_dir}")

    return config, model


def _load_tokenizer():
    """Load minimind tokenizer from common locations."""
    search_paths = [
        "./model/tokenizer",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model", "tokenizer"),
    ]
    for path in search_paths:
        if os.path.exists(os.path.join(path, "tokenizer.json")):
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
            print(f"Loaded tokenizer from {path} (vocab_size={tokenizer.vocab_size})")
            return tokenizer
    return None


def _create_sample_dataset(path: str):
    """Create a small sample dataset if full data unavailable."""
    print("For real training, run: python scripts/download_data.py --all")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    samples = [
        {"text": "Google Ads uses a real-time auction system where Ad Rank determines position, calculated as Max CPC Bid multiplied by Quality Score plus expected extension impact."},
        {"text": "GAQL queries use SELECT fields FROM resource WHERE conditions. Monetary values use cost_micros, divide by 1,000,000 for actual currency."},
        {"text": "CPA equals total cost divided by total conversions. ROAS equals conversion value divided by cost. Break-even ROAS equals one divided by profit margin."},
        {"text": "Meta Ads uses a campaign-ad set-ad hierarchy with Campaign Budget Optimization. Targeting includes Custom Audiences, Lookalike Audiences, and interest-based targeting."},
        {"text": "Smart Bidding needs at least 30 conversions in 30 days. Target CPA works best with 50+ conversions per month."},
    ]
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(200):
            for s in samples:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"Created minimal sample: {path} ({len(samples) * 200} samples)")


if __name__ == "__main__":
    main()

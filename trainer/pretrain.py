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
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)

    # Model config
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
        checkpoint = torch.load(ckpt_path, map_location=args.device)
        model.load_state_dict(checkpoint["model"])
        start_epoch = checkpoint.get("epoch", 0) + 1
        print(f"Resumed from epoch {start_epoch}")

    # Tokenizer (use sentencepiece or custom)
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("./model/tokenizer", trust_remote_code=True)
    except Exception:
        print("WARNING: No tokenizer found. Using dummy tokenizer for testing.")
        class DummyTokenizer:
            def encode(self, text, **kwargs):
                return [ord(c) % 6400 for c in text[:512]]
        tokenizer = DummyTokenizer()

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
    import math
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


def _create_sample_dataset(path: str):
    """Create a small sample advertising dataset for testing."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    samples = [
        {"text": "Google Ads uses a pay-per-click model where advertisers bid on keywords. The Quality Score is determined by expected click-through rate, ad relevance, and landing page experience. Higher Quality Scores result in lower cost-per-click and better ad positions."},
        {"text": "GAQL (Google Ads Query Language) is used to query the Google Ads API. A basic query: SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC."},
        {"text": "Search impression share is the percentage of impressions received divided by the estimated number of impressions eligible to receive. Lost impression share can be broken into budget lost (insufficient daily budget) and rank lost (low Quality Score or bids)."},
        {"text": "Cost per acquisition (CPA) equals total cost divided by total conversions. Return on ad spend (ROAS) equals conversion value divided by cost. A healthy search campaign typically has a 3-5% click-through rate and ROAS above 3x."},
        {"text": "Negative keywords prevent ads from showing for irrelevant searches. Common negative keyword categories include informational queries (how, what, why), competitor terms (if not targeting), job-related queries, and free/cheap/discount modifiers."},
        {"text": "Meta Ads Manager uses a campaign-ad set-ad hierarchy. Budget can be set at the campaign level (Campaign Budget Optimization) or ad set level. Audience targeting includes custom audiences, lookalike audiences, and interest-based targeting."},
        {"text": "Microsoft Advertising (formerly Bing Ads) supports importing campaigns directly from Google Ads. Key differences: lower CPCs, older demographic skew, LinkedIn profile targeting integration, and different auction dynamics."},
        {"text": "Amazon Sponsored Products use automatic and manual targeting. Automatic targeting matches ads to relevant customer searches and product pages. Manual targeting allows advertisers to choose specific keywords or products to target."},
        {"text": "The TradeDesk is a demand-side platform for programmatic advertising. It provides access to inventory across display, video, audio, native, and connected TV. Bidding strategies include optimized CPM, target CPA, and maximize conversions."},
        {"text": "Reddit Ads offers conversation placement targeting, interest targeting, and community targeting. Promoted posts appear in users' feeds. Best practices include authentic language, understanding subreddit culture, and avoiding overly promotional copy."},
    ]
    with open(path, "w", encoding="utf-8") as f:
        # Repeat samples to create a minimal training set
        for _ in range(100):
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    print(f"Created sample dataset: {path} ({len(samples) * 100} samples)")


if __name__ == "__main__":
    main()

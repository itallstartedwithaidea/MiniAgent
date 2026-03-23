"""
MiniAgent SFT — Stage 2: Advertising Instruction Following

Teaches the model to follow PPC instructions, answer audit questions,
write GAQL queries, and provide campaign recommendations.

Usage:
    python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth
    python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth --from_resume 1
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


CHAT_TEMPLATE = "<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n{assistant}<|im_end|>"
DEFAULT_SYSTEM = "You are MiniAgent, an expert advertising AI assistant specializing in Google Ads, Meta Ads, and cross-platform campaign management."


class SFTDataset(Dataset):
    """Advertising SFT dataset — instruction-response pairs."""
    def __init__(self, data_path: str, tokenizer, max_length: int = 1024):
        self.samples = []
        self.tokenizer = tokenizer
        self.max_length = max_length

        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                self.samples.append(item)

        print(f"Loaded {len(self.samples)} SFT samples from {data_path}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        system = item.get("system", DEFAULT_SYSTEM)
        user = item.get("user", item.get("instruction", ""))
        assistant = item.get("assistant", item.get("output", ""))

        text = CHAT_TEMPLATE.format(system=system, user=user, assistant=assistant)
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        tokens = tokens[:self.max_length]

        padding = self.max_length - len(tokens)
        input_ids = tokens + [0] * padding
        labels = tokens + [-100] * padding

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


def main():
    parser = argparse.ArgumentParser(description="MiniAgent SFT")
    parser.add_argument("--load_from", type=str, required=True, help="Pretrain checkpoint path")
    parser.add_argument("--data", type=str, default="./dataset/sft_ads.jsonl")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=5e-5)
    parser.add_argument("--max_length", type=int, default=1024)
    parser.add_argument("--save_dir", type=str, default="./checkpoints")
    parser.add_argument("--from_resume", type=int, default=0)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)

    # Load pretrained model
    checkpoint = torch.load(args.load_from, map_location=args.device)
    config = checkpoint["config"]
    model = MiniAgentModel(config).to(args.device)
    model.load_state_dict(checkpoint["model"])
    print(f"Loaded pretrained model from {args.load_from}")

    # Tokenizer — use minimind's 6400-vocab tokenizer
    tokenizer = _load_tokenizer()
    if tokenizer is None:
        print("ERROR: No tokenizer found. Run: python scripts/download_data.py --tokenizer")
        sys.exit(1)

    # Dataset
    if not os.path.exists(args.data):
        _create_sample_sft_dataset(args.data)

    dataset = SFTDataset(args.data, tokenizer, args.max_length)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True,
                            num_workers=2, pin_memory=True, drop_last=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    use_amp = args.device == "cuda"
    scaler = torch.amp.GradScaler("cuda") if use_amp else None
    ctx = torch.amp.autocast("cuda", dtype=torch.bfloat16) if use_amp else nullcontext()

    print(f"\n{'='*60}")
    print(f"MiniAgent SFT — Stage 2: Advertising Instructions")
    print(f"{'='*60}")
    print(f"Model: {model.count_params():.2f}M params")
    print(f"Data: {len(dataset)} instruction-response pairs")
    print(f"{'='*60}\n")

    model.train()
    for epoch in range(args.epochs):
        epoch_loss = 0.0
        t0 = time.time()
        for step, batch in enumerate(dataloader):
            input_ids = batch["input_ids"].to(args.device)
            labels = batch["labels"].to(args.device)

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

            if step % 50 == 0:
                print(f"  Epoch {epoch+1}/{args.epochs} | Step {step}/{len(dataloader)} | Loss: {loss.item():.4f}")

        avg = epoch_loss / len(dataloader)
        print(f"\n  Epoch {epoch+1} — Loss: {avg:.4f} | Time: {time.time()-t0:.1f}s\n")

        ckpt_path = os.path.join(args.save_dir, f"sft_{config.hidden_size}.pth")
        torch.save({"model": model.state_dict(), "config": config, "epoch": epoch}, ckpt_path)

    print(f"SFT complete! Next: python trainer/dpo.py --load_from {ckpt_path}")


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


def _create_sample_sft_dataset(path: str):
    """Create minimal sample SFT data if full data unavailable."""
    print("For real training, run: python scripts/download_data.py --all")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    samples = [
        {"user": "What is CPA?", "assistant": "CPA (Cost Per Acquisition) = Total Ad Spend / Total Conversions. If you spent $5,000 and got 100 conversions, your CPA is $50."},
        {"user": "Write a GAQL query for top campaigns by spend.", "assistant": "SELECT campaign.name, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC LIMIT 10."},
        {"user": "My CPA is too high. What should I do?", "assistant": "Check Search Terms Report for irrelevant queries, pause keywords with CPA over 2x target, improve landing page conversion rate, and ensure ad copy matches keyword intent."},
    ]
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(100):
            for s in samples:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"Created minimal SFT sample: {path}")


if __name__ == "__main__":
    main()

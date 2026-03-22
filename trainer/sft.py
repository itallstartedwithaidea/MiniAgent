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


CHAT_TEMPLATE = "<s>system\n{system}</s><s>user\n{user}</s><s>assistant\n{assistant}</s>"
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

    # Tokenizer
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("./model/tokenizer", trust_remote_code=True)
    except Exception:
        class DummyTokenizer:
            def encode(self, text, **kwargs):
                return [ord(c) % 6400 for c in text[:1024]]
        tokenizer = DummyTokenizer()

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


def _create_sample_sft_dataset(path: str):
    """Create sample advertising SFT data for testing."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    samples = [
        {"user": "What is a good CPA for a B2B SaaS Google Ads campaign?",
         "assistant": "For B2B SaaS, a good CPA depends on your average contract value (ACV). Rule of thumb: target CPA should be 10-20% of your first-year ACV. For a $10K ACV product, aim for $1,000-$2,000 CPA. For a $50K ACV, $5,000-$10,000 is acceptable. Key levers to reduce CPA: tighten keyword match types, add negative keywords from search terms report, improve landing page conversion rate, and use target CPA bidding with a 2-week learning period."},
        {"user": "Write a GAQL query to find my top 10 campaigns by spend last month.",
         "assistant": "```sql\nSELECT\n  campaign.name,\n  campaign.status,\n  metrics.cost_micros,\n  metrics.impressions,\n  metrics.clicks,\n  metrics.conversions,\n  metrics.search_impression_share\nFROM campaign\nWHERE segments.date DURING LAST_MONTH\n  AND campaign.status != 'REMOVED'\nORDER BY metrics.cost_micros DESC\nLIMIT 10\n```\n\nNote: `cost_micros` is in millionths of the account currency. Divide by 1,000,000 to get actual spend. For example, cost_micros = 45000000 means $45.00."},
        {"user": "My search impression share dropped from 80% to 45% this week. What happened?",
         "assistant": "A 35-point impression share drop in one week points to one of three causes:\n\n1. **Budget constraint** — Check `metrics.search_budget_lost_impression_share`. If this spiked, your daily budget isn't keeping up with demand. Could be seasonal, a new competitor entering, or CPCs rising.\n\n2. **Quality Score drop** — Check `metrics.search_rank_lost_impression_share`. If this increased, your Quality Score or bids dropped. Look at keyword-level QS changes and whether any ads were disapproved.\n\n3. **Competition surge** — A new competitor with aggressive bids can push you out of auctions. Check Auction Insights: `SELECT auction_insights.display_url, metrics.search_impression_share FROM auction_insights WHERE segments.date DURING LAST_7_DAYS`.\n\nMost likely cause for a sudden drop: budget. Check your daily spend vs. daily budget over the last 7 days."},
        {"user": "How do I structure a Google Ads account for an ecommerce store with 500 products?",
         "assistant": "For 500 products, use a tiered campaign structure:\n\n**Campaign 1: Brand** — Exact match brand terms. Low CPC, high conversion rate. Budget: 10-15% of total.\n\n**Campaign 2: Top Products (Performance Max)** — Your top 50 products by margin × volume. Let Google's algorithm optimize across Search, Shopping, Display, YouTube. Budget: 40-50% of total.\n\n**Campaign 3: Category Shopping** — Standard Shopping campaigns segmented by product category. Use campaign priority settings (High/Medium/Low) to control which campaign serves. Budget: 25-30%.\n\n**Campaign 4: Non-Brand Search** — Text ads targeting high-intent category keywords ('buy [category]', '[product type] online'). Budget: 10-15%.\n\n**Campaign 5: Remarketing** — Display/YouTube remarketing to cart abandoners and past visitors. Budget: 5-10%.\n\nKey: Start with Campaigns 1-2, prove ROI, then expand. Don't launch all 5 simultaneously — you'll spread budget too thin."},
        {"user": "Compare Google Ads and Meta Ads for lead generation.",
         "assistant": "**Google Ads (Search)**:\n- Intent-based: users are actively searching for your solution\n- Higher CPC ($2-15 for most industries), but higher conversion rates (3-8%)\n- Best for: bottom-funnel, high-intent leads\n- Typical CPL: $30-100 for B2B, $15-50 for B2C services\n\n**Meta Ads**:\n- Interruption-based: users see ads while browsing social\n- Lower CPC ($0.50-3), but lower conversion rates (1-3%)\n- Best for: top-funnel awareness, visual products, impulse purchases\n- Typical CPL: $15-60 for B2B, $5-25 for B2C\n\n**The right answer: use both.** Google captures existing demand (people searching). Meta creates new demand (people discovering). The optimal split depends on your market maturity — new categories need more Meta (demand creation), established categories need more Google (demand capture). Start 70/30 Google/Meta and adjust based on CPL data after 30 days."},
    ]

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(50):
            for s in samples:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"Created sample SFT dataset: {path}")


if __name__ == "__main__":
    main()

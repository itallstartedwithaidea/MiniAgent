"""
MiniAgent Chat — Terminal-based advertising AI chat.

Usage:
    python -m miniagent.chat
    python -m miniagent.chat --model ./checkpoints/sft_512.pth
"""

import os
import sys
import argparse
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    parser = argparse.ArgumentParser(description="MiniAgent Chat")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max_tokens", type=int, default=512)
    args = parser.parse_args()

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         MiniAgent — Advertising AI           ║")
    print("  ║  The Cowork Agent for Everything             ║")
    print("  ╠══════════════════════════════════════════════╣")
    print("  ║  Type your question about Google Ads, Meta,  ║")
    print("  ║  Microsoft, Amazon, or any ad platform.      ║")
    print("  ║  Type 'quit' to exit.                        ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    model = None
    tokenizer = None

    if args.model and os.path.exists(args.model):
        from model.model_miniagent import MiniAgentModel
        checkpoint = torch.load(args.model, map_location=args.device)
        config = checkpoint["config"]
        model = MiniAgentModel(config).to(args.device)
        model.load_state_dict(checkpoint["model"])
        model.eval()
        print(f"  Model loaded: {model.count_params():.1f}M params on {args.device}")

        try:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained("./model/tokenizer", trust_remote_code=True)
        except Exception:
            pass
    else:
        print("  No model loaded — running in knowledge-base mode.")
        print("  Train a model: python trainer/pretrain.py --dim 512 --n_layers 8")
    print()

    # Built-in knowledge base for zero-model mode
    KB = {
        "cpa": "CPA (Cost Per Acquisition) = Total Cost ÷ Total Conversions. For B2B SaaS, target 10-20% of first-year ACV. For ecommerce, target 15-25% of average order value.",
        "roas": "ROAS (Return On Ad Spend) = Conversion Value ÷ Cost. Healthy benchmarks: Ecommerce 3-5x, Lead Gen 5-10x, Brand 1-2x.",
        "quality score": "Quality Score (1-10) is determined by: Expected CTR, Ad Relevance, Landing Page Experience. Score of 7+ is good. Below 5 means you're overpaying for clicks.",
        "impression share": "Search Impression Share = Impressions ÷ Eligible Impressions. Lost IS breaks into Budget Lost (need more budget) and Rank Lost (need better QS or higher bids).",
        "gaql": "GAQL example: SELECT campaign.name, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC",
        "negative keywords": "Start with universal negatives: free, cheap, DIY, jobs, salary, reddit, youtube, how to. Then review Search Terms Report weekly and add irrelevant terms.",
        "cost_micros": "cost_micros is Google Ads API's currency format. Divide by 1,000,000 for actual dollars. Example: 45000000 = $45.00",
        "meta vs google": "Google Ads = intent-based (people searching). Meta Ads = interruption-based (people browsing). Use Google for demand capture, Meta for demand creation. Start 70/30.",
    }

    while True:
        try:
            user_input = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        if model and tokenizer:
            prompt = f"<s>user\n{user_input}</s><s>assistant\n"
            input_ids = torch.tensor([tokenizer.encode(prompt)], device=args.device)
            with torch.no_grad():
                output = model.generate(input_ids, max_new_tokens=args.max_tokens,
                                        temperature=args.temperature)
            response = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
        else:
            # Knowledge-base fallback
            response = None
            for key, answer in KB.items():
                if key in user_input.lower():
                    response = answer
                    break
            if not response:
                response = ("I can help with Google Ads, Meta Ads, PPC math, GAQL queries, "
                           "campaign structure, and cross-platform strategy. "
                           "Try asking about CPA, ROAS, Quality Score, or impression share.")

        print(f"\n  MiniAgent: {response}\n")

    print("\n  Goodbye! 👋\n")


if __name__ == "__main__":
    main()

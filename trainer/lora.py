"""
MiniAgent LoRA — Stage 3: Fine-tune on YOUR Account Data

Low-Rank Adaptation: fine-tune the model on your specific
Google Ads account data without full retraining.

Usage:
    python trainer/lora.py --load_from ./checkpoints/sft_512.pth --data ./dataset/my_account.jsonl

Status: Scaffold — full implementation coming in v0.2.0
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="MiniAgent LoRA")
    parser.add_argument("--load_from", type=str, required=True)
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--rank", type=int, default=8, help="LoRA rank")
    parser.add_argument("--alpha", type=float, default=16.0, help="LoRA alpha")
    args = parser.parse_args()

    print("MiniAgent LoRA — Stage 3: Account-Specific Fine-Tuning")
    print("Status: Scaffold. Full implementation in v0.2.0")
    print(f"LoRA rank: {args.rank}, alpha: {args.alpha}")
    print(f"Data: {args.data}")
    print("\nYour account data format (my_account.jsonl):")
    print('  {"user": "Analyze my campaign performance", "assistant": "Based on your data..."}')


if __name__ == "__main__":
    main()

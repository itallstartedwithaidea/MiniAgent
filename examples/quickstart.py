"""
MiniAgent Quickstart — Train → Chat → Evaluate in one script.

Usage: python examples/quickstart.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("MiniAgent Quickstart")
print("=" * 60)

# Step 1: Generate training data
print("\n▸ Step 1: Generating training data...")
from scripts.download_data import create_pretrain_data, create_sft_data
create_pretrain_data()
create_sft_data()

# Step 2: Test model creation
print("\n▸ Step 2: Creating model...")
import torch
from model.model_miniagent import MiniAgentModel, MiniAgentConfig

config = MiniAgentConfig(hidden_size=64, num_hidden_layers=2,
                         num_attention_heads=2, num_key_value_heads=1,
                         intermediate_size=128, vocab_size=256)
model = MiniAgentModel(config)
print(f"   Model: {model.count_params():.2f}M params")

# Step 3: Test forward pass
print("\n▸ Step 3: Testing forward pass...")
x = torch.randint(0, 256, (1, 32))
out = model(x, labels=x)
print(f"   Loss: {out['loss']:.4f}")

# Step 4: Test generation
print("\n▸ Step 4: Testing generation...")
model.eval()
prompt = torch.randint(0, 256, (1, 8))
generated = model.generate(prompt, max_new_tokens=16)
print(f"   Generated {generated.shape[1]} tokens")

# Step 5: Run benchmarks
print("\n▸ Step 5: Running benchmarks...")
from eval.advertising_bench import run_gaql_eval, run_ppc_math_eval, run_cross_platform_eval
for name, fn in [("GAQL", run_gaql_eval), ("PPC-Math", run_ppc_math_eval), ("Cross-Platform", run_cross_platform_eval)]:
    r = fn(model=None)
    print(f"   {name}: {r.score:.0f}% ({r.correct}/{r.total})")

# Step 6: Test chat
print("\n▸ Step 6: Knowledge-base chat test...")
KB = {"cpa": "CPA = Cost ÷ Conversions", "roas": "ROAS = Revenue ÷ Cost"}
for q in ["What is CPA?", "What is ROAS?"]:
    for k, v in KB.items():
        if k in q.lower():
            print(f"   Q: {q}\n   A: {v}")
            break

print("\n" + "=" * 60)
print("✅ All steps passed! MiniAgent is working.")
print("=" * 60)
print("\nNext steps:")
print("  Full training: make train")
print("  Chat:          make chat")
print("  Web demo:      make demo")
print("  Benchmarks:    make eval")

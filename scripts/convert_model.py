"""
MiniAgent Model Converter — Convert between formats.

Supports: PyTorch .pth ↔ HuggingFace Transformers ↔ GGUF (llama.cpp/ollama)

Usage:
    python scripts/convert_model.py --input ./checkpoints/sft_512.pth --output ./MiniAgent --format transformers
    python scripts/convert_model.py --input ./MiniAgent --output ./miniagent.gguf --format gguf
"""

import os
import sys
import json
import argparse
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.model_miniagent import MiniAgentModel, MiniAgentConfig


def pth_to_transformers(input_path: str, output_dir: str):
    """Convert PyTorch checkpoint to HuggingFace Transformers format."""
    checkpoint = torch.load(input_path, map_location="cpu")
    config = checkpoint["config"]
    model = MiniAgentModel(config)
    model.load_state_dict(checkpoint["model"])

    os.makedirs(output_dir, exist_ok=True)

    # Save model weights
    torch.save(model.state_dict(), os.path.join(output_dir, "pytorch_model.bin"))

    # Save config
    config_dict = {
        "model_type": "miniagent",
        "architectures": ["MiniAgentModel"],
        "hidden_size": config.hidden_size,
        "num_hidden_layers": config.num_hidden_layers,
        "num_attention_heads": config.num_attention_heads,
        "num_key_value_heads": config.num_key_value_heads,
        "intermediate_size": config.intermediate_size,
        "max_position_embeddings": config.max_position_embeddings,
        "rms_norm_eps": config.rms_norm_eps,
        "rope_base": config.rope_base,
        "vocab_size": config.vocab_size,
        "use_moe": config.use_moe,
        "torch_dtype": "bfloat16",
    }
    with open(os.path.join(output_dir, "config.json"), "w") as f:
        json.dump(config_dict, f, indent=2)

    # Save generation config
    gen_config = {
        "max_new_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "do_sample": True,
        "eos_token_id": 2,
        "pad_token_id": 0,
    }
    with open(os.path.join(output_dir, "generation_config.json"), "w") as f:
        json.dump(gen_config, f, indent=2)

    # Copy model files for self-contained loading
    import shutil
    model_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model")
    for fname in ["model_miniagent.py", "LMConfig.py"]:
        src = os.path.join(model_src, fname)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(output_dir, fname))

    print(f"✅ Transformers model saved to {output_dir}")
    print(f"   Load with: AutoModel.from_pretrained('{output_dir}', trust_remote_code=True)")


def transformers_to_pth(input_dir: str, output_path: str):
    """Convert HuggingFace Transformers format back to PyTorch checkpoint."""
    with open(os.path.join(input_dir, "config.json")) as f:
        config_dict = json.load(f)

    config = MiniAgentConfig(**{k: v for k, v in config_dict.items()
                                if k in MiniAgentConfig.__dataclass_fields__})
    model = MiniAgentModel(config)
    state_dict = torch.load(os.path.join(input_dir, "pytorch_model.bin"), map_location="cpu")
    model.load_state_dict(state_dict)

    torch.save({"model": model.state_dict(), "config": config}, output_path)
    print(f"✅ PyTorch checkpoint saved to {output_path}")


def to_gguf(input_dir: str, output_path: str):
    """Convert to GGUF format for llama.cpp / Ollama."""
    print("GGUF conversion requires llama.cpp's convert script.")
    print(f"Run: python llama.cpp/convert_hf_to_gguf.py {input_dir} --outfile {output_path} --outtype q4_0")
    print("\nOr for Ollama:")
    print(f"  1. Create Modelfile: FROM {input_dir}")
    print(f"  2. ollama create miniagent -f Modelfile")


def main():
    parser = argparse.ArgumentParser(description="MiniAgent Model Converter")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--format", type=str, choices=["transformers", "pth", "gguf"], required=True)
    args = parser.parse_args()

    if args.format == "transformers":
        pth_to_transformers(args.input, args.output)
    elif args.format == "pth":
        transformers_to_pth(args.input, args.output)
    elif args.format == "gguf":
        to_gguf(args.input, args.output)


if __name__ == "__main__":
    main()

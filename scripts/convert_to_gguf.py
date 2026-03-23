"""
Convert MiniAgent PyTorch weights to GGUF format for Ollama/llama.cpp.

Maps MiniAgent's Llama-compatible architecture to GGUF tensor naming.

Usage:
    python scripts/convert_to_gguf.py --input ./MiniAgent-26M --output ./miniagent.gguf
"""

import os
import sys
import json
import struct
import argparse
import numpy as np
import torch


GGUF_MAGIC = 0x46475547  # "GGUF"
GGUF_VERSION = 3

# GGUF value types
GGUF_TYPE_UINT32 = 4
GGUF_TYPE_INT32 = 5
GGUF_TYPE_FLOAT32 = 6
GGUF_TYPE_STRING = 8
GGUF_TYPE_ARRAY = 9
GGUF_TYPE_UINT16 = 2
GGUF_TYPE_INT8 = 1

# GGML tensor types
GGML_TYPE_F32 = 0
GGML_TYPE_F16 = 1

WEIGHT_MAP = {
    "embed_tokens.weight": "token_embd.weight",
    "norm.weight": "output_norm.weight",
    "lm_head.weight": "output.weight",
}

LAYER_WEIGHT_MAP = {
    "attention.q_proj.weight": "attn_q.weight",
    "attention.k_proj.weight": "attn_k.weight",
    "attention.v_proj.weight": "attn_v.weight",
    "attention.o_proj.weight": "attn_output.weight",
    "feed_forward.gate_proj.weight": "ffn_gate.weight",
    "feed_forward.up_proj.weight": "ffn_up.weight",
    "feed_forward.down_proj.weight": "ffn_down.weight",
    "attention_norm.weight": "attn_norm.weight",
    "ffn_norm.weight": "ffn_norm.weight",
}


def map_weight_name(name: str) -> str:
    if name in WEIGHT_MAP:
        return WEIGHT_MAP[name]
    for old, new in LAYER_WEIGHT_MAP.items():
        if old in name:
            layer_num = name.split(".")[1]
            return f"blk.{layer_num}.{new}"
    return name


def write_string(f, s: str):
    encoded = s.encode("utf-8")
    f.write(struct.pack("<Q", len(encoded)))
    f.write(encoded)


def write_kv_string(f, key: str, value: str):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_STRING))
    write_string(f, value)


def write_kv_uint32(f, key: str, value: int):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_UINT32))
    f.write(struct.pack("<I", value))


def write_kv_int32(f, key: str, value: int):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_INT32))
    f.write(struct.pack("<i", value))


def write_kv_float32(f, key: str, value: float):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_FLOAT32))
    f.write(struct.pack("<f", value))


def write_kv_string_array(f, key: str, values: list):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_ARRAY))
    f.write(struct.pack("<I", GGUF_TYPE_STRING))
    f.write(struct.pack("<Q", len(values)))
    for v in values:
        write_string(f, v)


def write_kv_int32_array(f, key: str, values: list):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_ARRAY))
    f.write(struct.pack("<I", GGUF_TYPE_INT32))
    f.write(struct.pack("<Q", len(values)))
    for v in values:
        f.write(struct.pack("<i", v))


def write_kv_float32_array(f, key: str, values: list):
    write_string(f, key)
    f.write(struct.pack("<I", GGUF_TYPE_ARRAY))
    f.write(struct.pack("<I", GGUF_TYPE_FLOAT32))
    f.write(struct.pack("<Q", len(values)))
    for v in values:
        f.write(struct.pack("<f", v))


def load_tokenizer_vocab(tokenizer_path: str):
    with open(tokenizer_path, "r") as f:
        tok_data = json.load(f)

    vocab = tok_data.get("model", {}).get("vocab", {})
    if not vocab:
        vocab_list = tok_data.get("added_tokens", [])
        if vocab_list:
            return [t.get("content", "") for t in sorted(vocab_list, key=lambda x: x.get("id", 0))]
        return [f"<tok_{i}>" for i in range(6400)]

    tokens = [""] * len(vocab)
    for token, idx in vocab.items():
        if idx < len(tokens):
            tokens[idx] = token
    return tokens


def main():
    parser = argparse.ArgumentParser(description="Convert MiniAgent to GGUF")
    parser.add_argument("--input", type=str, required=True, help="Model directory or .pth file")
    parser.add_argument("--output", type=str, default="./miniagent.gguf")
    args = parser.parse_args()

    if args.input.endswith(".pth"):
        state_dict = torch.load(args.input, map_location="cpu", weights_only=False)
        if "model" in state_dict:
            state_dict = state_dict["model"]
        tokenizer_path = "./model/tokenizer/tokenizer.json"
    else:
        weights_file = os.path.join(args.input, "pytorch_model.bin")
        state_dict = torch.load(weights_file, map_location="cpu", weights_only=True)
        tokenizer_path = os.path.join(args.input, "tokenizer.json")

    print(f"Loaded {len(state_dict)} tensors")

    vocab_size = state_dict["embed_tokens.weight"].shape[0]
    hidden_size = state_dict["embed_tokens.weight"].shape[1]
    n_layers = max(int(k.split(".")[1]) for k in state_dict if k.startswith("layers.")) + 1
    intermediate_size = state_dict["layers.0.feed_forward.gate_proj.weight"].shape[0]
    n_heads = hidden_size // 64
    head_dim = 64
    n_kv_heads = state_dict["layers.0.attention.k_proj.weight"].shape[0] // head_dim

    print(f"Model: vocab={vocab_size}, hidden={hidden_size}, layers={n_layers}, "
          f"heads={n_heads}, kv_heads={n_kv_heads}, intermediate={intermediate_size}")

    tokens = load_tokenizer_vocab(tokenizer_path)
    if len(tokens) < vocab_size:
        tokens.extend([f"<extra_{i}>" for i in range(vocab_size - len(tokens))])
    tokens = tokens[:vocab_size]

    tensors = {}
    for name, tensor in state_dict.items():
        gguf_name = map_weight_name(name)
        tensors[gguf_name] = tensor.float().numpy()

    # Metadata KV pairs
    metadata = []

    print(f"Writing GGUF to {args.output}...")

    with open(args.output, "wb") as f:
        f.write(struct.pack("<I", GGUF_MAGIC))
        f.write(struct.pack("<I", GGUF_VERSION))
        f.write(struct.pack("<Q", len(tensors)))

        # Count metadata (we'll write 15 KV pairs)
        n_kv = 15
        f.write(struct.pack("<Q", n_kv))

        # Architecture metadata
        write_kv_string(f, "general.architecture", "llama")
        write_kv_string(f, "general.name", "MiniAgent-26M")
        write_kv_uint32(f, "llama.context_length", 2048)
        write_kv_uint32(f, "llama.embedding_length", hidden_size)
        write_kv_uint32(f, "llama.block_count", n_layers)
        write_kv_uint32(f, "llama.feed_forward_length", intermediate_size)
        write_kv_uint32(f, "llama.attention.head_count", n_heads)
        write_kv_uint32(f, "llama.attention.head_count_kv", n_kv_heads)
        write_kv_float32(f, "llama.attention.layer_norm_rms_epsilon", 1e-5)
        write_kv_float32(f, "llama.rope.freq_base", 10000.0)
        write_kv_uint32(f, "llama.vocab_size", vocab_size)

        # Tokenizer metadata
        write_kv_string(f, "tokenizer.ggml.model", "gpt2")
        write_kv_string_array(f, "tokenizer.ggml.tokens", tokens)
        write_kv_int32_array(f, "tokenizer.ggml.token_type", [1] * vocab_size)
        write_kv_string_array(f, "tokenizer.ggml.merges", [])

        # Tensor info headers
        tensor_data_list = []
        data_offset = 0
        for tname, tdata in tensors.items():
            write_string(f, tname)
            n_dims = len(tdata.shape)
            f.write(struct.pack("<I", n_dims))
            for dim in tdata.shape:
                f.write(struct.pack("<Q", dim))
            f.write(struct.pack("<I", GGML_TYPE_F32))
            f.write(struct.pack("<Q", data_offset))
            tensor_bytes = tdata.tobytes()
            tensor_data_list.append(tensor_bytes)
            data_offset += len(tensor_bytes)

        # Alignment padding
        alignment = 32
        current_pos = f.tell()
        pad = (alignment - (current_pos % alignment)) % alignment
        f.write(b"\x00" * pad)

        # Tensor data
        for tensor_bytes in tensor_data_list:
            f.write(tensor_bytes)

    file_size = os.path.getsize(args.output)
    print(f"✅ GGUF saved: {args.output} ({file_size / 1e6:.1f} MB)")
    print(f"   Tensors: {len(tensors)}")
    print(f"   Vocab: {vocab_size} tokens")
    print(f"\nNext steps:")
    print(f"  ollama create miniagent -f Modelfile")
    print(f"  ollama run miniagent")


if __name__ == "__main__":
    main()

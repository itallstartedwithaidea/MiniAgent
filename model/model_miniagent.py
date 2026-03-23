"""
MiniAgent Model — Decoder-Only Transformer
Based on minimind by JingyaoGong (Apache 2.0).

Architecture: Llama-style with RMSNorm, SwiGLU, RoPE, GQA.
Advertising extensions: GAQL-aware tokenization, ad-domain embeddings.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class MiniAgentConfig:
    hidden_size: int = 512
    num_hidden_layers: int = 8
    num_attention_heads: int = 8
    num_key_value_heads: int = 2
    intermediate_size: int = 1408
    max_position_embeddings: int = 2048
    rms_norm_eps: float = 1e-5
    rope_base: float = 10000.0
    vocab_size: int = 6400
    use_moe: bool = False
    num_experts: int = 4
    num_experts_per_tok: int = 2
    dropout: float = 0.0
    rope_scaling: Optional[dict] = None
    model_type: str = "miniagent"


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization (from LLaMA)."""
    def __init__(self, hidden_size: int, eps: float = 1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        norm = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * norm * self.weight


def precompute_rope_freqs(dim: int, max_seq_len: int, base: float = 10000.0,
                          rope_scaling: Optional[dict] = None) -> torch.Tensor:
    """Precompute Rotary Position Embedding frequencies."""
    freqs = 1.0 / (base ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))

    # YaRN long-text extrapolation
    if rope_scaling is not None:
        scale_factor = rope_scaling.get("factor", 16)
        original_max = rope_scaling.get("original_max_position_embeddings", 2048)
        beta_fast = rope_scaling.get("beta_fast", 32.0)
        beta_slow = rope_scaling.get("beta_slow", 1.0)
        attn_factor = rope_scaling.get("attention_factor", 1.0)

        low = math.floor(dim * math.log(original_max / (beta_fast * 2 * math.pi)) /
                         (2 * math.log(base)))
        high = math.ceil(dim * math.log(original_max / (beta_slow * 2 * math.pi)) /
                         (2 * math.log(base)))
        low = max(low, 0)
        high = min(high, dim // 2 - 1)

        smooth = (torch.arange(dim // 2).float() - low) / (high - low)
        smooth = smooth.clamp(0, 1)
        freqs = (1 - smooth) * (freqs / scale_factor) + smooth * freqs

    t = torch.arange(max_seq_len, dtype=freqs.dtype)
    freqs = torch.outer(t, freqs)
    return torch.polar(torch.ones_like(freqs), freqs)  # complex64


def apply_rope(xq: torch.Tensor, xk: torch.Tensor,
               freqs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    """Apply rotary position embeddings to queries and keys."""
    xq_complex = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_complex = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))

    freqs = freqs[:xq.shape[2]].unsqueeze(0).unsqueeze(1)
    xq_out = torch.view_as_real(xq_complex * freqs).flatten(-2)
    xk_out = torch.view_as_real(xk_complex * freqs).flatten(-2)
    return xq_out.type_as(xq), xk_out.type_as(xk)


class GQAttention(nn.Module):
    """Grouped-Query Attention (GQA) — same as Llama 3."""
    def __init__(self, config: MiniAgentConfig):
        super().__init__()
        self.n_heads = config.num_attention_heads
        self.n_kv_heads = config.num_key_value_heads
        self.head_dim = config.hidden_size // config.num_attention_heads
        self.n_rep = self.n_heads // self.n_kv_heads

        self.q_proj = nn.Linear(config.hidden_size, self.n_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(config.hidden_size, self.n_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(config.hidden_size, self.n_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(self.n_heads * self.head_dim, config.hidden_size, bias=False)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor, freqs: torch.Tensor,
                mask: Optional[torch.Tensor] = None,
                kv_cache: Optional[Tuple] = None) -> Tuple[torch.Tensor, Optional[Tuple]]:
        bsz, seq_len, _ = x.shape

        # Project and reshape to (bsz, n_heads, seq_len, head_dim)
        q = self.q_proj(x).view(bsz, seq_len, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(bsz, seq_len, self.n_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(bsz, seq_len, self.n_kv_heads, self.head_dim).transpose(1, 2)

        # Apply RoPE to q and k (both in heads-first layout)
        q, k = apply_rope(q, k, freqs)

        # KV cache for inference (cat on seq_len = dim 2)
        if kv_cache is not None:
            prev_k, prev_v = kv_cache
            k = torch.cat([prev_k, k], dim=2)
            v = torch.cat([prev_v, v], dim=2)
        new_kv_cache = (k, v)

        # Repeat KV heads for GQA
        if self.n_rep > 1:
            k = k.repeat_interleave(self.n_rep, dim=1)
            v = v.repeat_interleave(self.n_rep, dim=1)

        # Scaled dot-product attention
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        if mask is not None:
            scores = scores + mask
        attn = F.softmax(scores.float(), dim=-1).type_as(q)
        attn = self.dropout(attn)
        output = torch.matmul(attn, v)

        output = output.transpose(1, 2).contiguous().view(bsz, seq_len, -1)
        return self.o_proj(output), new_kv_cache


class SwiGLU(nn.Module):
    """SwiGLU Feed-Forward Network — same as Llama."""
    def __init__(self, config: MiniAgentConfig):
        super().__init__()
        self.gate_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.up_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.down_proj = nn.Linear(config.intermediate_size, config.hidden_size, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))


class MoELayer(nn.Module):
    """Mixture of Experts — based on DeepSeek-V2/minimind MoE."""
    def __init__(self, config: MiniAgentConfig):
        super().__init__()
        self.num_experts = config.num_experts
        self.num_experts_per_tok = config.num_experts_per_tok
        self.gate = nn.Linear(config.hidden_size, config.num_experts, bias=False)
        self.experts = nn.ModuleList([SwiGLU(config) for _ in range(config.num_experts)])

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        bsz, seq_len, dim = x.shape
        x_flat = x.view(-1, dim)

        logits = self.gate(x_flat)
        weights, indices = torch.topk(F.softmax(logits, dim=-1), self.num_experts_per_tok)
        weights = weights / weights.sum(dim=-1, keepdim=True)

        output = torch.zeros_like(x_flat)
        for i, expert in enumerate(self.experts):
            mask = (indices == i).any(dim=-1)
            if mask.any():
                expert_input = x_flat[mask]
                expert_output = expert(expert_input)
                expert_weight = weights[mask, (indices[mask] == i).float().argmax(dim=-1)].unsqueeze(-1)
                output[mask] += expert_output * expert_weight

        # Load balancing loss
        router_probs = F.softmax(logits, dim=-1)
        avg_probs = router_probs.mean(dim=0)
        balance_loss = self.num_experts * (avg_probs * (router_probs > 0).float().mean(dim=0)).sum()

        return output.view(bsz, seq_len, dim), balance_loss


class MiniAgentBlock(nn.Module):
    """Single transformer block with pre-norm."""
    def __init__(self, layer_id: int, config: MiniAgentConfig):
        super().__init__()
        self.attention = GQAttention(config)
        self.feed_forward = MoELayer(config) if config.use_moe else SwiGLU(config)
        self.attention_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.ffn_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.use_moe = config.use_moe

    def forward(self, x: torch.Tensor, freqs: torch.Tensor,
                mask: Optional[torch.Tensor] = None,
                kv_cache: Optional[Tuple] = None):
        # Pre-norm attention
        h, new_kv_cache = self.attention(self.attention_norm(x), freqs, mask, kv_cache)
        x = x + h

        # Pre-norm FFN
        if self.use_moe:
            ffn_out, balance_loss = self.feed_forward(self.ffn_norm(x))
            x = x + ffn_out
            return x, new_kv_cache, balance_loss
        else:
            x = x + self.feed_forward(self.ffn_norm(x))
            return x, new_kv_cache, torch.tensor(0.0)


class MiniAgentModel(nn.Module):
    """
    MiniAgent — Decoder-Only Transformer for Advertising AI.
    
    Based on minimind architecture (JingyaoGong, Apache 2.0).
    Llama-compatible: RMSNorm, SwiGLU, RoPE, GQA, optional MoE.
    """
    def __init__(self, config: MiniAgentConfig):
        super().__init__()
        self.config = config
        self.vocab_size = config.vocab_size
        self.num_hidden_layers = config.num_hidden_layers

        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size)
        self.layers = nn.ModuleList([
            MiniAgentBlock(i, config) for i in range(config.num_hidden_layers)
        ])
        self.norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

        # Tie weights (embedding = lm_head)
        self.lm_head.weight = self.embed_tokens.weight

        # Precompute RoPE frequencies
        head_dim = config.hidden_size // config.num_attention_heads
        self.register_buffer(
            "freqs",
            precompute_rope_freqs(head_dim, config.max_position_embeddings,
                                  config.rope_base, config.rope_scaling),
            persistent=False,
        )

        self.apply(self._init_weights)
        print(f"MiniAgent model initialized: {self.count_params():.2f}M parameters")

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def count_params(self) -> float:
        return sum(p.numel() for p in self.parameters()) / 1e6

    def forward(self, input_ids: torch.Tensor,
                labels: Optional[torch.Tensor] = None,
                kv_caches: Optional[list] = None,
                ) -> dict:
        bsz, seq_len = input_ids.shape
        h = self.embed_tokens(input_ids)

        # Causal mask
        mask = None
        if seq_len > 1:
            mask = torch.full((seq_len, seq_len), float("-inf"), device=input_ids.device)
            mask = torch.triu(mask, diagonal=1)
            if kv_caches and kv_caches[0] is not None:
                prev_len = kv_caches[0][0].shape[2]
                mask = torch.zeros((seq_len, prev_len + seq_len), device=input_ids.device)
                mask[:, prev_len:] = torch.triu(
                    torch.full((seq_len, seq_len), float("-inf"), device=input_ids.device),
                    diagonal=1,
                )

        new_kv_caches = []
        total_balance_loss = torch.tensor(0.0, device=input_ids.device)

        for i, layer in enumerate(self.layers):
            kv = kv_caches[i] if kv_caches else None
            h, new_kv, balance_loss = layer(h, self.freqs, mask, kv)
            new_kv_caches.append(new_kv)
            total_balance_loss = total_balance_loss + balance_loss

        h = self.norm(h)
        logits = self.lm_head(h)

        loss = None
        if labels is not None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = F.cross_entropy(
                shift_logits.view(-1, self.vocab_size),
                shift_labels.view(-1),
                ignore_index=-100,
            )
            if self.config.use_moe:
                loss = loss + 0.01 * total_balance_loss

        return {
            "logits": logits,
            "loss": loss,
            "kv_caches": new_kv_caches,
        }

    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, max_new_tokens: int = 256,
                 temperature: float = 0.7, top_p: float = 0.9,
                 eos_token_id: int = 2) -> torch.Tensor:
        """Autoregressive generation with KV cache."""
        kv_caches = [None] * self.num_hidden_layers
        generated = input_ids

        for _ in range(max_new_tokens):
            out = self.forward(input_ids, kv_caches=kv_caches)
            logits = out["logits"][:, -1, :] / temperature
            kv_caches = out["kv_caches"]

            # Top-p sampling
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            probs = F.softmax(sorted_logits, dim=-1)
            cumsum = torch.cumsum(probs, dim=-1)
            mask = cumsum - probs > top_p
            sorted_logits[mask] = float("-inf")
            probs = F.softmax(sorted_logits, dim=-1)
            next_token = sorted_indices.gather(-1, torch.multinomial(probs, 1))

            generated = torch.cat([generated, next_token], dim=-1)
            input_ids = next_token  # only feed new token (KV cache has context)
            if next_token.item() == eos_token_id:
                break

        return generated


if __name__ == "__main__":
    config = MiniAgentConfig()
    model = MiniAgentModel(config)
    
    # Test forward pass
    x = torch.randint(0, config.vocab_size, (1, 64))
    out = model(x, labels=x)
    print(f"Loss: {out['loss']:.4f}")
    print(f"Logits shape: {out['logits'].shape}")
    
    # Test generation
    prompt = torch.randint(0, config.vocab_size, (1, 8))
    generated = model.generate(prompt, max_new_tokens=32)
    print(f"Generated {generated.shape[1]} tokens")

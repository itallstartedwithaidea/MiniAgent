"""
MiniAgent Model Configuration
Based on minimind's LMConfig with advertising-domain defaults.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class MiniAgentConfig:
    # Model architecture (same as minimind)
    hidden_size: int = 512
    num_hidden_layers: int = 8
    num_attention_heads: int = 8
    num_key_value_heads: int = 2  # GQA
    intermediate_size: int = 1408
    max_position_embeddings: int = 2048
    rms_norm_eps: float = 1e-5
    rope_base: float = 10000.0
    vocab_size: int = 6400  # Custom advertising tokenizer

    # MoE (optional)
    use_moe: bool = False
    num_experts: int = 4
    num_experts_per_tok: int = 2

    # Advertising domain extensions
    ad_platforms: list = None  # Platforms this model was trained on
    gaql_support: bool = True  # Whether model understands GAQL
    model_type: str = "miniagent"

    # Training defaults
    dropout: float = 0.0
    attention_dropout: float = 0.0

    # YaRN for long-text extrapolation
    rope_scaling: Optional[dict] = None

    def __post_init__(self):
        if self.ad_platforms is None:
            self.ad_platforms = [
                "google_ads", "meta_ads", "microsoft_ads", "amazon_ads",
                "reddit_ads", "tradedesk", "linkedin_ads", "criteo",
                "adroll", "tiktok_ads", "snapchat_ads", "pinterest_ads",
                "quora_ads", "twitter_ads",
            ]
        if self.num_key_value_heads is None:
            self.num_key_value_heads = self.num_attention_heads


# Predefined model sizes
MINIAGENT_CONFIGS = {
    "miniagent-26m": MiniAgentConfig(hidden_size=512, num_hidden_layers=8),
    "miniagent-108m": MiniAgentConfig(hidden_size=768, num_hidden_layers=16),
    "miniagent-moe-145m": MiniAgentConfig(
        hidden_size=512, num_hidden_layers=8, use_moe=True,
        num_experts=4, num_experts_per_tok=2
    ),
}

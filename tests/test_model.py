"""Tests for MiniAgent model."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config_defaults():
    from model.LMConfig import MiniAgentConfig
    c = MiniAgentConfig()
    assert c.hidden_size == 512
    assert c.num_hidden_layers == 8
    assert c.vocab_size == 6400
    assert c.model_type == "miniagent"
    assert len(c.ad_platforms) == 14

def test_model_init():
    import torch
    from model.model_miniagent import MiniAgentModel, MiniAgentConfig
    config = MiniAgentConfig(hidden_size=64, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=1, intermediate_size=128, vocab_size=256)
    model = MiniAgentModel(config)
    assert model.count_params() > 0
    x = torch.randint(0, 256, (1, 16))
    out = model(x, labels=x)
    assert out["loss"] is not None
    assert out["logits"].shape == (1, 16, 256)

def test_model_generate():
    import torch
    from model.model_miniagent import MiniAgentModel, MiniAgentConfig
    config = MiniAgentConfig(hidden_size=64, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=1, intermediate_size=128, vocab_size=256)
    model = MiniAgentModel(config)
    model.eval()
    prompt = torch.randint(0, 256, (1, 4))
    out = model.generate(prompt, max_new_tokens=8)
    assert out.shape[1] >= 1

def test_moe_model():
    import torch
    from model.model_miniagent import MiniAgentModel, MiniAgentConfig
    config = MiniAgentConfig(hidden_size=64, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=1, intermediate_size=128, vocab_size=256, use_moe=True, num_experts=2, num_experts_per_tok=1)
    model = MiniAgentModel(config)
    x = torch.randint(0, 256, (1, 16))
    out = model(x, labels=x)
    assert out["loss"] is not None

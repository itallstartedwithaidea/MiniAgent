<div align="center">

# MiniAgent

### 万能协作智能体。从零训练。到处运行。

[English](../../README.md) | [中文](./README.md) | [Русский](../ru/README.md) | [Italiano](../it/README.md) | [Español](../es/README.md)

**从零训练你自己的广告AI。2小时。一张GPU。你的数据。**

基于 [minimind](https://github.com/jingyaogong/minimind)（Apache 2.0，42k stars）· 14个广告平台 · 29个MCP工具 · 5个Claude Code技能

</div>

---

## 这是什么？

MiniAgent 是一个三合一仓库：

1. **可训练的广告AI** — 基于minimind（26M参数），使用广告领域数据重新训练。模型学习GAQL查询、广告系列结构、出价策略、PPC数学和创意分析。单张3090显卡，2小时完成训练。

2. **生产级MCP服务器生态** — 14个广告平台连接器（Google、Meta、Microsoft、Amazon、Reddit、TradeDesk、LinkedIn等），80+工具，全部pip可安装。

3. **智能体技能平台** — Claude Code技能、Codex技能、Gemini CLI技能，用于广告分析、审计、安全写操作、PPC计算和跨平台报告。

---

## 快速开始

```bash
# 使用预训练模型（无需GPU）
ollama run itallstartedwithaidea/miniagent

# 安装MCP服务器（连接真实广告账户）
pip install miniagent[google]

# 安装Claude Code技能（无需API）
/plugin marketplace add itallstartedwithaidea/miniagent

# 从零训练你自己的模型（2小时，1张GPU）
git clone https://github.com/itallstartedwithaidea/miniagent.git
cd miniagent && pip install -r requirements.txt
python scripts/download_data.py
python trainer/pretrain.py --dim 512 --n_layers 8
python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth
```

---

## 归属

本项目基于 [jingyaogong/minimind](https://github.com/jingyaogong/minimind)（Apache 2.0许可证）构建。完整归属表见英文README。

## 许可证

Apache 2.0 — 与minimind相同。

## 作者

**John Williams** · 高级付费媒体专家 · 15年以上企业数字广告管理经验（年度广告支出4800万美元以上）

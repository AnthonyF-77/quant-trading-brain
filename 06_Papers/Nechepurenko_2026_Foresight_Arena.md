# Foresight Arena: On-Chain Benchmark for AI Forecasting Agents

**来源**: arXiv [#2605.00420](http://arxiv.org/abs/2605.00420)
**日期**: 2026-05-01
**分类**: 09_ML_LLM
**标签**: #AI预测 #预测市场 #智能体 #Polymarket

## 核心观点

1. **Foresight Arena**: 首个无需许可、链上 AI 预测 agent 评估基准
2. 基于 Polymarket 二元预测市场，Solidity 智能合约执行
3. 用 **Brier Score** 和 **Alpha Score**（新提出）衡量表现
4. Alpha Score 激励诚实概率报告，分离预测边缘与市场共识
5. 形式分析：检测 α*=0.02 的真实边缘需要约 **350 个已解决预测**
6. 开源代码和智能合约已发布

## 可执行见解

- **AI agent 评估**: 用 Brier Score + Alpha Score 分离预测能力和时机/规模/风险偏好
- **策略**: 在预测市场上，Alpha Score > 0 表示 agent 有超越市场共识的预测能力
- **研究方向**: AI 预测 + 预测市场结合是值得关注的新领域

## 局限性

- 仅二元市场
- 需要大量预测（约350个）才能可靠区分 skill level

## 原始链接

- 论文: http://arxiv.org/abs/2605.00420
- GitHub: github.com/ForesightFlow

---
*消化日期: 2026-05-06 | OpenCode*

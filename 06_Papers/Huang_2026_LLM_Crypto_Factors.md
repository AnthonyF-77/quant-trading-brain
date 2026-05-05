# From Hypotheses to Factors: Constrained LLM Agents in Cryptocurrency Markets

**来源**: arXiv [#2604.26747](http://arxiv.org/abs/2604.26747)
**日期**: 2026-04-29
**分类**: 09_ML_LLM
**标签**: #LLM #加密货币 #因子挖掘 #AI量化

## 核心观点

1. **问题**: LLM agents 做因子发现时过于灵活，变成失控搜索
2. **解决方案**: 框架将任务建模为序贯假设搜索 — agent 读取 experiment trace、提出可证伪因子假设、映射到可执行配方
3. **确定性引擎**强制执行：固定数据分割、selection gates、交易成本、投资组合测试
4. 候选操作被限制在 point-in-time factor DSL，使成功和失败的假设都可审计
5. **实盘结果**: ridge-combined portfolio（仅用 2020-2022 数据训练）→ 2024-2026 样本外年化收益 **44.55%**，Sharpe **1.55**（扣除 5bp 单边交易成本后）

## 可执行见解

- **AI 策略**: 用 constrained LLM agent 做因子发现 — 限制假设空间比自由搜索更有效
- **风控**: 固定数据分割 + 交易成本测试 = 可审计的因子发现流程
- **实盘**: Ridge 组合多个因子比单一因子更稳健

## 局限性

- 仅测试加密货币市场
- 2020-2022 训练数据可能不覆盖极端市场环境

## 原始链接

- 论文: http://arxiv.org/abs/2604.26747
- PDF: http://arxiv.org/pdf/2604.26747v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

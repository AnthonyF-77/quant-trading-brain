# Pricing with Passion: The Local Occupied Volatility (LOV) Model

**来源**: arXiv [#2604.26151](http://arxiv.org/abs/2604.26151)
**日期**: 2026-04-28
**分类**: 05_Execution
**标签**: #期权定价 #局部波动率 #模型校准

## 核心观点

1. LOV 模型介于 **Dupire 局部波动率**和**全路径依赖动力学**之间
2. 设计保证自动校准到欧式香草期权，同时保持灵活性捕获波动率风格化事实
3. 核心机制：** Occupation Sensitivity Function** — 量化路径依赖冲击对波动率的影响
4. 通过美式-欧式期权联合校准验证（非分红股票期权链）

## 关键公式 / 方法

- LOV 模型通过调节 Occupation Sensitivity Function 实现校准灵活性
- 验证数据：非分红股票的美式+欧式期权链联合校准

## 可执行见解

- **定价**: 如果做期权定价/套利，LOV 模型提供了比纯局部波动率更灵活的中间路线
- **校准**: 自动校准到 vanilla 期权是刚需，减少手动调整
- **应用场景**: 奇异期权定价、波动率曲面建模

## 局限性

- 论文尚未测试在分红股票上的表现
- 计算复杂度可能高于标准局部波动率模型

## 原始链接

- 论文: http://arxiv.org/abs/2604.26151
- PDF: http://arxiv.org/pdf/2604.26151v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

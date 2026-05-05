# Decision-Induced Ranking Explains Prediction Inflation in SPO-Based Portfolio Optimization

**来源**: arXiv [#2605.01176](http://arxiv.org/abs/2605.01176)
**日期**: 2026-05-02
**分类**: 03_Alpha_Factors
**标签**: #SPO #决策学习 #投资组合优化 #因子

## 核心观点

1. DFL（决策聚焦学习）按下游决策质量训练预测器，而非单纯预测准确性
2. SPO-based DFL 可能产生**膨胀收益信号**和**不稳定组合调仓**
3. KKT 解释：组合决策是对风险和交易成本调整边际分数的**排序**
4. 评估三种稳定化机制：**clipping, min-max rescaling, partial portfolio adjustment**
5. **结论**: 现实输出约束和组合级调仓控制提高 SPO 策略可执行性

## 可执行见解

- **组合优化**: 用 DFL 训练预测器时，必须加入调仓频率控制和输出约束
- **因子构建**: 用风险/成本调整后的边际分数排序，而非原始预测分数
- **成本控制**: partial portfolio adjustment 是防止过度交易的简单有效方法

## 局限性

- 模拟环境，未在真实市场大规模验证
- 稳定化机制超参数需手动设置

## 原始链接

- 论文: http://arxiv.org/abs/2605.01176
- PDF: http://arxiv.org/pdf/2605.01176v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

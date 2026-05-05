# Fast Monte-Carlo: Eigenvalue-Based Small-Sample Approximation

**来源**: arXiv [#2605.02085](http://arxiv.org/abs/2605.02085)
**日期**: 2026-05-03
**分类**: 07_Code
**标签**: #蒙特卡洛 #MCMC #方差缩减 #算法

## 核心观点

1. 提出基于特征值的 Markov Chain Monte Carlo 小样本近似
2. 传统 Monte Carlo 需要 **1,000,000 条路径**，新方法仅需 **10 条**（视模拟时间范围 T 而定）
3. 产生的平稳分布与经典 Monte Carlo 一致（Wasserstein 距离验证）
4. 稳态分布的**方差显著缩减**

## 可执行见解

- **计算效率**: 期权定价/风险计算用 eigenvalue-based MCMC 可减少 99.9% 路径数
- **速度**: 对于需要大量 MC 模拟的场景（组合 VaR、希腊字母计算），此方法大幅加速
- **适用**: 需要 MC 模拟但计算资源有限的场景

## 局限性

- 需要提前知道/估计特征值结构
- 在极高维问题上特征值计算本身可能很贵

## 原始链接

- 论文: http://arxiv.org/abs/2605.02085
- PDF: http://arxiv.org/pdf/2605.02085v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

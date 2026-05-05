# Sampler-Robust Optimization under Generative Models

**来源**: arXiv [#2604.27447](http://arxiv.org/abs/2604.27447)
**日期**: 2026-04-30
**分类**: 04_Risk
**标签**: #鲁棒优化 #生成模型 #投资组合 #分布偏移

## 核心观点

1. 现代随机优化 pipeline 依赖学习到的生成模型表示不确定性
2. 可靠性取决于两种误差: **sampler misspecification** + **finite-simulation error**
3. 提出 **Sampler-Robust Optimization (SRO)** — 针对最坏情况 sampler 优化
4. SRO 偏向性能在生成器扰动下稳定的决策，而非仅在 nominal sampler 下好的决策
5. **投资组合实验**: SRO 产生更稳定决策，分布偏移下样本外表现更好

## 可执行见解

- **组合优化**: 当用 ML 模型预测收益分布时，用 SRO 替代标准均值-方差优化
- **风控**: 在市场机制发生结构性变化时，SRO 比标准优化更稳健
- **适用场景**: GAN/VAE 生成场景数据的组合选择

## 局限性

- 仅在模拟组合上验证
- minimax 求解可能计算代价高

## 原始链接

- 论文: http://arxiv.org/abs/2604.27447
- PDF: http://arxiv.org/pdf/2604.27447v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

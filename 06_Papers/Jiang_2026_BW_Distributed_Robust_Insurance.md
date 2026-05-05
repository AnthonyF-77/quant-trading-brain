# Distributionally Robust Insurance under Bregman-Wasserstein Divergence

**来源**: arXiv [#2604.27837](http://arxiv.org/abs/2604.27837)
**日期**: 2026-04-30
**分类**: 04_Risk
**标签**: #保险 #鲁棒优化 #Wasserstein距离 #TVaR

## 核心观点

1. 用 **Bregman-Wasserstein (BW) 球**表征损失分布的模糊集
2. 与 p-Wasserstein 距离不同，BW 允许**非对称惩罚**偏离基准分布
3. 两个优化问题：
   - (i) **α-maxmin VaR 偏好**下的最优赔偿函数
   - (ii) **鲁棒优化框架**下的最小化最坏情况凸扭曲风险度量
4. BW 差异的非对称性如何影响最优赔偿结构
5. 给出 Tail VaR (TVaR) 的具体示例

## 可执行见解

- **保险设计**: 用 BW 替代 Wasserstein 做分布鲁棒优化，可以非对称惩罚分布偏移
- **尾部风险**: TVaR 是比 VaR 更好的尾部风险度量
- **风控**: 在分布不确定性下，最坏情况赔偿函数有闭式解

## 局限性

- 理论推导为主
- 数值验证有限

## 原始链接

- 论文: http://arxiv.org/abs/2604.27837
- PDF: http://arxiv.org/pdf/2604.27837v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

# Learning to Spend: Model Predictive Control for Budgeting under Non-Stationary Returns

**来源**: arXiv [#2604.27186](http://arxiv.org/abs/2604.27186)
**日期**: 2026-04-29
**分类**: 04_Risk
**标签**: #MPC #预算分配 #控制理论 #非平稳

## 核心观点

1. 将有限期预算分配建模为闭环经济控制问题
2. 比较 MPC（模型预测控制）与 reactive budgeting policies
3. **核心发现**: 非平稳性本身不能证明使用预测控制的合理性
4. 当回报动态是**平稳**或**不可预测的随机漂移**时，MPC 相比 reactive baseline **无优势**
5. 当回报效率在规划范围内呈现**可预测结构**时，MPC 持续优于 reactive budgeting（数字营销场景）

## 可执行见解

- **策略**: 在回报效率有**可预测的季节性/周期性**时用 MPC，否则用 reactive
- **判断方法**: 先检验回报序列是否存在可预测结构，再决定是否用 MPC
- **应用场景**: 广告预算分配、组合再平衡、资源调度

## 局限性

- 模拟框架（数字营销），未在真实金融市场验证
- 计算成本高于简单 reactive 规则

## 原始链接

- 论文: http://arxiv.org/abs/2604.27186
- PDF: http://arxiv.org/pdf/2604.27186v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

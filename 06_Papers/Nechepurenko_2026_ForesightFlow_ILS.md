# ForesightFlow: Information Leakage Score Framework for Prediction Markets

**来源**: arXiv [#2605.00493](http://arxiv.org/abs/2605.00493)
**日期**: 2026-05-01
**分类**: 03_Alpha_Factors
**标签**: #信息泄漏 #预测市场 #ILS #Alpha检测

## 核心观点

1. ForesightFlow 的 **ILS 框架**：量化预测市场上公开新闻事件前的终端信息移动比例
2. 三个操作范围条件（edge effect、non-trivial total move、anchor sensitivity）是解释前提
3. **三大发现**：
   - 公开事件时间戳代理不能有效分离事件解决市场和对照组
   - 文章推导时间戳 vs 代理时间戳：得分移动 **0.444 幅度**
   - Polymarket 内部记录中的文档案例**系统性为截止日期解决**（超出原始 ILS 范围）
4. 提出 **deadline-ILS 扩展**（基于事件日期而非新闻日期），配备 hazard baseline

## 可执行见解

- **市场选择**: 优先选**新闻解决**（news-resolved）而非**截止日期解决**（deadline-resolved）市场
- **Alpha**: deadline-ILS 可识别预测市场中的提前信息泄漏
- **信号质量**: 需要区分不同 resolution 类型才能正确解读 ILS

## 局限性

- FFIC 清单中 24 个文档案例无 1 个满足原始 ILS 范围
- 需持续更新 hazard baseline

## 原始链接

- 论文: http://arxiv.org/abs/2605.00493
- GitHub: github.com/ForesightFlow

---
*消化日期: 2026-05-06 | OpenCode*

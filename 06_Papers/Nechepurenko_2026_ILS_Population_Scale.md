# Information Leakage at Population Scale: Polymarket Evaluation

**来源**: arXiv [#2605.00459](http://arxiv.org/abs/2605.00459)
**日期**: 2026-05-01
**分类**: 03_Alpha_Factors
**标签**: #信息泄漏 #Polymarket #预测市场 #Alpha因子

## 核心观点

1. 将单案例 ILS-dl 框架扩展到 **12,708 个 Polymarket 市场**（2020.10-2026.4）
2. **关键发现 1**: 仅 88/12,708（0.7%）市场能计算出 ILS-dl 值
3. **关键发现 2**: 仅有 12/88（13.6%）满足锚点敏感性
4. **关键发现 3**: 原始 ILS-dl 中位数全为负，hazard-baseline 修正后：2024后 regulatory_announcement 类别保留负值
5. **核心结论**: 信息流检测需要**分辨率-类型学**和**评分基线**两个维度的改进

## 可执行见解

- **预测市场**: 在 Polymarket 上进行预测时，需要筛选有足够流动性和明确事件日期的市场
- **Alpha**: regulatory_announcement 类别的信息泄漏信号最明显
- **因子**: ILS-dl 可作为预测市场特有的信息质量因子

## 局限性

- 绝大多数市场无法计算 ILS-dl（0.7%），框架适用范围窄
- 依赖外部事件日期确定

## 原始链接

- 论文: http://arxiv.org/abs/2605.00459
- PDF: http://arxiv.org/pdf/2605.00459v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

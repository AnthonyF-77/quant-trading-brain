# Visibility Graphs Can Make Money in Financial Markets

**来源**: arXiv [#2605.01300](http://arxiv.org/abs/2605.01300)
**日期**: 2026-05-02
**分类**: 02_Strategies
**标签**: #技术分析 #可见图 #RSI #DJI30 #外汇 #黄金

## 核心观点

1. 提出 **VGRSI (Visibility Graphs Relative Strength Index)** — 基于价格后向可见关系
2. 与经典 RSI 不同，VGRSI 利用资产价格波动的**几何性质**
3. **回测结果** (2024-2025, 503 交易日):
   - DJI30: 盈利 USD ~146,000
   - EUR/USD: USD ~69,000
   - XAU/USD (黄金): USD ~125,000
   - **总计**: USD ~340,000，日均 ~676，每笔固定保证金 USD 1,000
4. 关键指标：Sharpe 2.55-3.6，回撤 10-18%，日均交易 3.3-4.8 笔

## 可执行见解

- **策略**: VGRSI 可作为独立技术分析工具，在多个资产类别有效
- **资产**: 在黄金、外汇、股指均有正向夏普，说明策略稳健
- **实现**: 30天优化窗口 + 7天测试窗口的滚动窗口方法

## 局限性

- 2024-2025 样本期，可能不覆盖极端波动环境
- 未报告考虑滑点和流动性成本后的真实执行效果

## 原始链接

- 论文: http://arxiv.org/abs/2605.01300
- PDF: http://arxiv.org/pdf/2605.01300v1.pdf

---
*消化日期: 2026-05-06 | OpenCode*

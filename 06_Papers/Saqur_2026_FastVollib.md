# Fast-Vollib: High-Performance Implied Volatility Library

**来源**: arXiv [#2604.27210](http://arxiv.org/abs/2604.27210)
**日期**: 2026-04-29
**分类**: 07_Code
**标签**: #期权定价 #波动率 #Python #PyTorch #JAX #CUDA

## 核心观点

1. 开源 Python 库，替代 py_vollib，提供高性能欧式期权定价和隐含波动率计算
2. 支持 **Black-76, Black-Scholes, Black-Scholes-Merton** 模型
3. 可插拔后端: **PyTorch, JAX, NumPy/Numba, CUDA Triton**
4. 亮点: Jäckel's "Let's Be Rational" (LBR) 算法的向量化实现，**单 pass GPU kernel** 处理批量期权链
5. 100% 兼容 py_vollib API，可直接替换

## 可执行见解

- **代码工具**: 做期权量化研究时，用 fast-vollib 替代 py_vollib 可获得 10x 以上加速
- **GPU 加速**: 批量计算期权链（量化投行日常）用 Triton/CUDA 后端
- **研究用途**: JAX 后端适合自动微分 + 期权greeks的梯度计算

## 局限性

- 仅支持欧式期权（美式需用其他方法）
- LBR 算法实现仍属实验性质

## 原始链接

- 论文: http://arxiv.org/abs/2604.27210
- GitHub: https://github.com/raeidsaqur/fast-vollib
- PyPI: https://pypi.org/project/fast-vollib/

---
*消化日期: 2026-05-06 | OpenCode*

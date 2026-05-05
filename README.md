# Quant Trading Brain

> 基于 Karpathy LLM Wiki 模式的全自动量化交易研究知识库

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)

## 概览

这是一个**自我进化的量化交易研究脑**，利用 OpenCode + Obsidian + GitHub Actions 实现全自动知识积累。

```
每日自动抓取 (arXiv + RSS)
         ↓
   sources/00_Inbox/
         ↓
   OpenCode 消化
         ↓
 Obsidian Vault 知识库
         ↓
   你来提问/查询
```

## 目录结构

```
quant-trading-brain/
├── sources/00_Inbox/          # 原始文档（自动抓取）
├── 01_Markets/                # 市场微观结构
├── 02_Strategies/             # 量化策略
├── 03_Alpha_Factors/          # Alpha 因子研究
├── 04_Risk/                   # 风险管理
├── 05_Execution/              # 执行算法
├── 06_Papers/                 # 论文笔记（核心）
├── 07_Code/                   # 代码片段
├── 08_Crypto/                 # 加密货币量化
├── 09_ML_LLM/                 # ML/LLM应用
├── scraper/                   # 自动抓取引擎
├── .github/workflows/          # GitHub Actions
├── wiki_index.md              # 知识库总索引
└── quant-brain-prompt.md      # OpenCode 系统提示词
```

## 全自动抓取来源

| 来源 | 类型 | 频率 |
|------|------|------|
| arXiv q-fin.GN | 论文 | 每日 |
| arXiv q-fin.ST | 论文 | 每日 |
| arXiv q-fin.TR | 论文 | 每日 |
| arXiv q-fin.PM | 论文 | 每日 |
| arXiv q-fin.RM | 论文 | 每日 |
| QuantInsti Blog | 文章 | 每日 |
| PyQuant News | 文章 | 每日 |
| QuantStart | 文章 | 每日 |
| Quantpedia | 文章 | 每日 |
| Binance Research | 报告 | 每日 |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/quant-trading-brain.git
cd quant-trading-brain
```

### 2. 配置 Obsidian（可选）

在 Obsidian 中打开这个 vault，安装推荐插件：
- **Obsidian Git** — 自动同步到 GitHub
- **RSS Reader** — 手动订阅额外来源
- **Dataview** — 查询知识库

### 3. 设置 GitHub Actions

仓库 push 到 GitHub 后，GitHub Actions 会自动：
- 每天 08:00 UTC 运行抓取
- 提交新内容到 `sources/00_Inbox/`

### 4. 开始使用

让 OpenCode 消化新文档：

```
"帮我消化这周 sources/00_Inbox/ 里所有的新论文和文章"
```

## OpenCode 使用指南

加载系统提示词后，OpenCode 会自动：

1. **消化文档** — 读取 00_Inbox，写入对应目录
2. **维护索引** — 更新 wiki_index.md
3. **回答问题** — 基于已有知识库回答

### 典型对话

```
你: 最近有哪些关于动量因子的新研究？
OpenCode: 根据 wiki_index 和 06_Papers/ 中的记录，最近有两篇相关论文...

你: 帮我消化这周的新内容
OpenCode: 正在扫描 00_Inbox... 发现 5 个新文件，正在处理...

你: 什么是 Kelly 准则？
OpenCode: 在 04_Risk/ 中找到相关笔记，Kelly 准则是一种...
```

## 数据来源

- **arXiv q-fin**: https://arxiv.org/list/q-fin/new
- **RSS Feeds**: 见 scraper/sources/rss_source.py

## 许可

MIT License

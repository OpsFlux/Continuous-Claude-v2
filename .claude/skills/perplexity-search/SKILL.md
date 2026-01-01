---
name: perplexity-search
description: AI-powered web search, research, and reasoning via Perplexity
allowed-tools: [Bash, Read]
---

<a id="perplexity-ai-search"></a>
# 复杂性 AI 搜索

网络搜索有 AI 动力的答案， 深入的研究，和思维链推理。

<a id="when-to-use"></a>
## 何时使用

- 直接网页搜索排名结果( 无 AI 合成)
- AI-综合研究与引用
- 复杂决定的思想推理
- 深入全面研究课题。

<a id="models-2025"></a>
## 型号(2025)

| 型号 | 目的 |
|-------|---------|
| `sonar` | 用地面进行轻量级搜索 |
| `sonar-pro` | 高级搜索复杂查询 |
| `sonar-reasoning-pro` | 思想推理链 |
| `sonar-deep-research` | 专家一级的详尽研究 |

<a id="usage"></a>
## 使用量

<a id="quick-question-ai-answer"></a>
### 快速问题(AI 回答)
```bash
uv run python scripts/perplexity_search.py \
    --ask "What is the latest version of Python?"
```

<a id="direct-web-search-ranked-results-no-ai"></a>
### 直接网络搜索(排名结果，无 AI)
```bash
uv run python scripts/perplexity_search.py \
    --search "SQLite graph database patterns" \
    --max-results 5 \
    --recency week
```

<a id="ai-synthesized-research"></a>
### AI-合成研究
```bash
uv run python scripts/perplexity_search.py \
    --research "compare FastAPI vs Django for microservices"
```

<a id="chain-of-thought-reasoning"></a>
### 思维链推理
```bash
uv run python scripts/perplexity_search.py \
    --reason "should I use Neo4j or SQLite for small graph under 10k nodes?"
```

<a id="deep-comprehensive-research"></a>
### 深入的全面研究
```bash
uv run python scripts/perplexity_search.py \
    --deep "state of AI agent observability 2025"
```

<a id="parameters"></a>
## 参数

| 参数 | 说明 |
|-----------|-------------|
| `--ask` | 用 AI 回答的快题( sonar) |
| `--search` | 直接网页搜索 - 排名结果不包含 AI 综合 |
| `--research` | AI-合成研究(sonar-pro) |
| `--reason` | 思维推理链(理论推理-pro) |
| `--deep` | 深度综合研究(sonar-deep-research). |

<a id="search-specific-options"></a>
### 特定搜索选项
| 参数 | 说明 |
|-----------|-------------|
| `--max-results N` | 结果数量(1-20，默认：10) |
| `--recency` | 过滤器 :`day`, `week`, `month`, `year` |
| `--domains` | 限于特定域 |

<a id="mode-selection-guide"></a>
## 模式选择指南

| 需求 | 使用 | 为什么 |
|------|-----|-----|
| 快点 | `--ask` | 轻快又快 |
| 查找来源 | `--search` | 初步结果， 无 AI 间接费用 |
| 合成答案 | `--research` | AI 结合多个来源 |
| 复杂的决定 | `--reason` | 思维链分析 |
| 综合报告 | `--deep` | 用尽多种来源的研究 |

<a id="examples"></a>
## 实例

```bash
# Find recent sources on a topic
uv run python scripts/perplexity_search.py \
    --search "OpenTelemetry AI agent tracing" \
    --recency month --max-results 5

# Get AI synthesis
uv run python scripts/perplexity_search.py \
    --research "best practices for AI agent logging 2025"

# Make a decision
uv run python scripts/perplexity_search.py \
    --reason "microservices vs monolith for startup MVP"

# Deep dive
uv run python scripts/perplexity_search.py \
    --deep "comprehensive guide to building feedback loops for autonomous agents"
```

<a id="api-key-required"></a>
## 需要 API 密钥

要求数`PERPLEXITY_API_KEY`环境或`~/.claude/.env`.

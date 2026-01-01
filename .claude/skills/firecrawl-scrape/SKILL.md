---
name: firecrawl-scrape
description: Scrape web pages and extract content via Firecrawl MCP
allowed-tools: [Bash, Read]
---

<a id="firecrawl-scrape-skill"></a>
# Firecrawl Scrape 技能

<a id="when-to-use"></a>
## 何时使用

- 从任意 URL 中搜索内容
- 从网页提取结构化数据
- 搜索网络并获取内容

<a id="instructions"></a>
## 说明

```bash
uv run python -m runtime.harness scripts/firecrawl_scrape.py \
    --url "https://example.com" \
    --format "markdown"
```

<a id="parameters"></a>
### 参数

- `--url`: 要刮去的 URL
- `--format`: 输出格式 -`markdown`, `html`, `text`(默认： 减记)
- `--search`: (备选) 搜索查询而不是直接 URL

<a id="examples"></a>
### 实例

```bash
# Scrape a page
uv run python -m runtime.harness scripts/firecrawl_scrape.py \
    --url "https://docs.python.org/3/library/asyncio.html"

# Search and scrape
uv run python -m runtime.harness scripts/firecrawl_scrape.py \
    --search "Python asyncio best practices 2024"
```

<a id="mcp-server-required"></a>
## 需要的 MCP 服务器

要求数`firecrawl`使用 FIRECRAWL API KEY 的服务器。

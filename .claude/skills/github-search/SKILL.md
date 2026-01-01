---
name: github-search
description: Search GitHub code, repositories, issues, and PRs via MCP
allowed-tools: [Bash, Read]
---

<a id="github-search-skill"></a>
# GitHub 搜索技能

<a id="when-to-use"></a>
## 何时使用

- 跨仓库搜索代码
- 查找问题或公关
- 查找仓库信息

<a id="instructions"></a>
## 说明

```bash
uv run python -m runtime.harness scripts/github_search.py \
    --type "code" \
    --query "your search query"
```

<a id="parameters"></a>
### 参数

- `--type`: 搜索类型 -`code`, `repos`, `issues`, `prs`
- `--query`: 搜索查询(支持 GitHub 搜索语法)
- `--owner`: (可选) Repo 拥有者过滤器
- `--repo`: (可选) 按 repo 名称过滤

<a id="examples"></a>
### 实例

```bash
# Search code
uv run python -m runtime.harness scripts/github_search.py \
    --type "code" \
    --query "authentication language:python"

# Search issues
uv run python -m runtime.harness scripts/github_search.py \
    --type "issues" \
    --query "bug label:critical" \
    --owner "anthropics"
```

<a id="mcp-server-required"></a>
## 需要的 MCP 服务器

要求数`github`服务器在 mcp config.json 有 GITHUB Personal ACCESS TOKEN。

---
name: nia-docs
description: Search library documentation and code examples via Nia
allowed-tools: [Bash, Read]
---

<a id="nia-documentation-search"></a>
# Nia 文档搜索

搜索 3000+软件包(npm,PyPI,Crates,Go)，并索引出文档和代码示例的来源。

<a id="usage"></a>
## 使用量

<a id="semantic-search-in-a-package"></a>
### 在软件包中进行语义搜索
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --package fastapi --query "dependency injection"
```

<a id="search-with-specific-registry"></a>
### 搜索特定登记处
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --package react --registry npm --query "hooks patterns"
```

<a id="grep-search-for-specific-patterns"></a>
### Grep 搜索特定模式
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --package sqlalchemy --grep "session.execute"
```

<a id="universal-search-across-indexed-sources"></a>
### 索引来源的通用搜索
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --search "error handling middleware"
```

<a id="options"></a>
## 选项

| 选项 | 说明 |
|--------|-------------|
| `--package` | 要搜索的软件包名称 |
| `--registry` | 注册： npm, py pi, 箱子， go 模块( 默认： npm) |
| `--query` | 语义搜索查询 |
| `--grep` | 要搜索的 Regex 模式 |
| `--search` | 所有索引来源的通用搜索 |
| `--limit` | 最大结果( 默认 5) |

<a id="examples"></a>
## 实例

```bash
# Python library usage
uv run python -m runtime.harness scripts/nia_docs.py \
  --package pydantic --registry py_pi --query "validators"

# React patterns
uv run python -m runtime.harness scripts/nia_docs.py \
  --package react --query "useEffect cleanup"

# Find specific function usage
uv run python -m runtime.harness scripts/nia_docs.py \
  --package express --grep "app.use"
```

要求数`NIA_API_KEY`环境或`nia`mcp config.json 中的服务器。

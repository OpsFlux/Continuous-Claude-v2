---
name: morph-search
description: Fast codebase search via WarpGrep (20x faster than grep)
allowed-tools: [Bash, Read]
---

<a id="morph-codebase-search"></a>
# 墨菲密码库搜索

快速，AI 动力的代码库搜索使用 WarpGrep. 20x 比传统 grep 快。

<a id="when-to-use"></a>
## 何时使用

- 搜索模式、函数名称、变量的代码库
- 快速在大型代码库中查找代码
- 程序化编辑文件

<a id="usage"></a>
## 使用量

<a id="search-for-code-patterns"></a>
### 搜索代码模式
```bash
uv run python -m runtime.harness scripts/morph_search.py \
    --search "authentication" --path "."
```

<a id="search-with-regex"></a>
### 用正则搜索
```bash
uv run python -m runtime.harness scripts/morph_search.py \
    --search "def.*login" --path "./src"
```

<a id="edit-a-file"></a>
### 编辑文件
```bash
uv run python -m runtime.harness scripts/morph_search.py \
    --edit "/path/to/file.py" --content "new content"
```

<a id="parameters"></a>
## 参数

| 参数 | 说明 |
|-----------|-------------|
| `--search` | 搜索查询/模式 |
| `--path` | 要搜索的目录( 默认 ):`.`) |
| `--edit` | 要编辑的文件路径 |
| `--content` | 文件的新内容( 使用于`--edit`) |

<a id="examples"></a>
## 实例

```bash
# Find all async functions
uv run python -m runtime.harness scripts/morph_search.py \
    --search "async def" --path "./src"

# Search for imports
uv run python -m runtime.harness scripts/morph_search.py \
    --search "from fastapi import" --path "."
```

<a id="vs-ast-grep"></a>
## vs 驴- grep

| 工具 | 最佳服务 |
|------|----------|
| **变形/碎石** | 快速文本/ regex 搜索( 20x 更快) |
| (单位：千美元) | 结构代码搜索( 理解语法) |

<a id="mcp-server-required"></a>
## 需要的 MCP 服务器

要求数`morph`mcp config.json 中的服务器`MORPH_API_KEY`.

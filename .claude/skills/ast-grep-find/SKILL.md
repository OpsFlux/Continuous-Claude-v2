---
name: ast-grep-find
description: AST-based code search and refactoring via ast-grep MCP
allowed-tools: [Bash, Read]
---

<a id="ast-grep-find"></a>
# AST- Grep 查找

结构代码搜索能理解语法。 查找函数调用，导入，类定义等模式 - 不仅仅是文本。

<a id="when-to-use"></a>
## 何时使用

- 查找代码模式( ignores 字符串/ 注释)
- 搜索函数调用、类定义、导入
- 用 AST 精度重构代码
- 跨代码库重命名变量/功能

<a id="usage"></a>
## 使用量

<a id="search-for-a-pattern"></a>
### 搜索图案
```bash
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "import asyncio" --language python
```

<a id="search-in-specific-directory"></a>
### 在特定目录中搜索
```bash
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "async def \$FUNC(\$\$\$)" --language python --path "./src"
```

<a id="refactorreplace-pattern"></a>
### 重构/重置模式
```bash
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "console.log(\$MSG)" --replace "logger.info(\$MSG)" \
    --language javascript
```

<a id="dry-run-preview-changes"></a>
### 干跑 (审查更改)
```bash
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "print(\$X)" --replace "logger.info(\$X)" \
    --language python --dry-run
```

<a id="parameters"></a>
## 参数

| 参数 | 说明 |
|-----------|-------------|
| `--pattern` | AST 搜索模式( 需要) |
| `--language` | 语言 :`python`, `javascript`, `typescript`, `go`等 (中文(简体) ). |
| `--path` | 要搜索的目录( 默认 ):`.`) |
| `--glob` | 文件 glob 模式( 例如 )`**/*.py`) |
| `--replace` | 重构的替换模式 |
| `--dry-run` | 不应用预览更改 |
| `--context` | 上下文行( 默认： 2) |

<a id="pattern-syntax"></a>
## 图案语法

| 语法 | 含义 |
|--------|---------|
| `$NAME` | 匹配单个节点( 可变， 表达式) |
| `$$$` | 匹配多个节点( 参数、 语句) |
| `$_` | 匹配任意单一节点( Wildcard) |

<a id="examples"></a>
## 实例

```bash
# Find all function definitions
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "def \$FUNC(\$\$\$):" --language python

# Find console.log calls
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "console.log(\$\$\$)" --language javascript

# Replace print with logging
uv run python -m runtime.harness scripts/ast_grep_find.py \
    --pattern "print(\$X)" --replace "logging.info(\$X)" \
    --language python --dry-run
```

<a id="vs-morphwarpgrep"></a>
## vs 形态/ warpgrep

| 工具 | 最佳服务 |
|------|----------|
| (单位：千美元) | 结构模式( 理解代码语法) |
| **战争遗留爆炸物** | 快速文本/ regex 搜索( 20x 更快 grep) |

在需要语法意识匹配时使用 ast- grep. 使用 wrpgrep 为原始速度。

<a id="mcp-server-required"></a>
## 需要的 MCP 服务器

要求数`ast-grep`mcp config.json 中的服务器。

---
name: morph-apply
description: Fast file editing via Morph Apply API (10,500 tokens/sec, 98% accuracy)
allowed-tools: [Bash, Read]
---

<a id="morph-fast-apply"></a>
# 墨菲快速应用

Fast, AI- power 文件编辑， 使用 Morph 应用 API. 不先读就编辑文件 。 过程为 10 500 个令牌/秒，准确度为 98%。

<a id="when-to-use"></a>
## 何时使用

- 在不阅读整个文件的情况下快速编辑文件
- 批次编辑到文件( 一个操作的多处更改)
- 当你知道要改变什么，但文件很大
- 读取会消耗太多符号的大文件

<a id="key-pattern-code-markers"></a>
## 密钥模式： 代码标记

使用`// ... existing code ...`(或适合语言的评论)以标记编辑走向：

```python
# ... existing code ...
try:
    result = process()
except Exception as e:
    log.error(e)
# ... existing code ...
```

API 将您的编辑智能放在正确的位置 。

<a id="usage"></a>
## 使用量

<a id="add-error-handling"></a>
### 添加错误处理
```bash
uv run python -m runtime.harness scripts/morph_apply.py \
    --file "src/auth.py" \
    --instruction "Add error handling to login function" \
    --code_edit "# ... existing code ...
try:
    user = authenticate(credentials)
except AuthError as e:
    log.error(f'Auth failed: {e}')
    raise
# ... existing code ..."
```

<a id="add-logging"></a>
### 添加日志
```bash
uv run python -m runtime.harness scripts/morph_apply.py \
    --file "src/api.py" \
    --instruction "Add debug logging" \
    --code_edit "# ... existing code ...
logger.debug(f'Processing request: {request.id}')
# ... existing code ..."
```

<a id="typescript-example"></a>
### 类型脚本示例
```bash
uv run python -m runtime.harness scripts/morph_apply.py \
    --file "src/types.ts" \
    --instruction "Add user validation" \
    --code_edit "// ... existing code ...
if (!user) throw new Error('User not found');
if (!user.isActive) throw new Error('User inactive');
// ... existing code ..."
```

<a id="parameters"></a>
## 参数

| 参数 | 说明 |
|-----------|-------------|
| `--file` | 要编辑的文件路径( 需要) |
| `--instruction` | 人类对变化的描述(必需). |
| `--code_edit` | 代码片段， 有显示编辑位置的标记( 需要) |

<a id="vs-claudes-edit-tool"></a>
## vs Claude 编辑工具

| 工具 | 最佳服务 |
|------|----------|
| **形态适用** | 快速编辑， 不需要先读文件， 大文件， 批次编辑 |
| **文稿编辑** | 文件已经上下文时的小精度编辑 |

**在下述情况下使用可变应用：**
- 文件不是上下文，读起来会很贵
- 文件非常大( > 500 行)
- 立即进行多个相关的编辑
- 您知道变化的背景( 函数名、 类等)

**在下列时间使用 Claude 编辑：**
- 文件已经存在上下文来自先前的 Read
- 非常精确的编辑需要精确的旧/新字符串匹配
- 小文件( < 200 行)

<a id="mcp-server-required"></a>
## 需要的 MCP 服务器

要求数`morph`mcp config.json 中的服务器`MORPH_API_KEY`.

<a id="performance"></a>
## 业绩

- **说明**:10 500 个令牌/秒
- **准确性**:98%的正确安置
- **节省的款项**: 不需要先读整个文件

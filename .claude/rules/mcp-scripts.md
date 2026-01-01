---
globs: ["scripts/**/*.py"]
---

<a id="mcp-script-rules"></a>
# MCP 脚本规则

处理文件时`scripts/`:

<a id="do"></a>
## DO
- 对所有参数使用 CLI 参数( argparse)
- 在文件上方包含 USAGE docstring
- 使用`call_mcp_tool("server__tool", params)`模式
- 处理错误和信息信息
- 打印结果为 Claude 处理

<a id="dont"></a>
## 别
- 脚本中的硬码参数
- 编辑更改参数的脚本( 使用 CLI args 代替)
- 从服务器直接导入( 使用 runtime. mcp  client)

<a id="tool-naming"></a>
## 工具命名
工具 ID 使用双下划线 :`serverName__toolName`

实例：
- `morph__warpgrep_codebase_search`
- `ast-grep__ast_grep`
- `perplexity__perplexity_ask`

<a id="testing"></a>
## 测试
测试方式：`uv run python -m runtime.harness scripts/<script>.py --help`

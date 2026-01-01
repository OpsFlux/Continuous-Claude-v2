<a id="claudemd-claude-code-operational-guide"></a>
# CLAUDE.md - Claude 代码操作指南

**术语：**
- **Skills** = Claude Code 本地格式(.claude/chilling/ with SKILL.md) - 自动发现
- **脚本** = 基于 CLI 的 Python 工作流程(./scripts/- 代理不可知论者

**Dual-Mode MCP 图案**:可重复使用的脚本(PREFERRED,99.6%还原)有 CLI 参数，或为新任务直接编写脚本(98.7%还原). 通过文件系统逐步披露。 多运输支持(stio + SSE + HTTP).

<a id="execution-modes"></a>
## 执行模式

<a id="primary-scripts-based-execution-2-tools-complex-logic"></a>
### 初级：基于脚本的执行(>2 个工具，复杂的逻辑)

**何时使用：**
- 多步骤研究工作流程
- 需要交叉鉴定
- 数据处理管道
- 连锁多个 MCP 服务器
- 减少 99.6%，减少 96%的时间

**备选案文：**
1. `ls scripts/`- 发现可用的脚本
2. `cat scripts/{script}.py`- 读取脚本多克字符串和 CLI 参数
3. 以参数执行( DO 不编辑文件) :
   ```bash
   # Example: Web scraping
   uv run python -m runtime.harness scripts/firecrawl_scrape.py \
       --url "https://example.com"

   # Example: Multi-tool pipeline
   uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
       --repo-path "." \
       --max-commits 5
   ```

**示例脚本：**

可重复使用的 CLI 工作流程(./scripts/):
- `firecrawl_scrape.py`- 网络刮刮模式(`--url`)
- `multi_tool_pipeline.py`- 多工具连锁模式(`--repo-path`, `--max-commits`)

**说明：** 这些是**templades** - 以实例为您特定的 MCP 服务器创建自定义脚本并使用大小写。

**Claude 代码用户：** 这些脚本也作为本地技能提供`.claude/skills/`(SKILL.md 格式，自动发现).

<a id="alternative-direct-script-writing-1-tool-simple-fetch"></a>
### 替代： 直接脚本写作(1 个工具，简单取取取)

**何时使用：**
- 单个工具调用
- 直通数据检索
- 现有脚本未覆盖的小说工作流程
- 建立新模式

**方法：**(现有文件)
1. 探索`servers/`用于发现工具
2. 使用工具导入写入 Python 脚本
3. 执行 :`uv run python -m runtime.harness workspace/script.py`

<a id="mcp-server-configuration"></a>
## MCP 服务器配置

此顺序的配置运行时间检查 :
1. `.mcp.json`(《守则》项目公约)
2. `mcp_config.json`(可见的例子，在 Repo 中跟踪)

**环境变量：** 添加 API 密钥到`.env`(从`.env.example`) (中文(简体) ). 配置使用`${VAR}`占位符 。

<a id="commands"></a>
## 图标
- `uv run mcp-generate`- Python 将军的包装纸`.mcp.json` or `mcp_config.json`
- `uv run mcp-discover`- 从实际的 API 反应中得出的普通 Pydantic 类型(见`discovery_config.json`)
- `uv run mcp-exec <script.py>`- 运行脚本/ MCP
- `uv run mcp-exec <script> --args`- 用 CLI 参数运行脚本
- 示例脚本 :`workspace/example_progressive_disclosure.py`, `tests/integration/test_*.py`
- 用户脚本进入 :`workspace/`(恶作剧)

<a id="core-files"></a>
## 核心文件
- `src/runtime/mcp_client.py` - `McpClientManager`懒惰地装入，`initialize()`只装入配置，`call_tool()`连接按需、工具格式`"serverName__toolName"`，通过`get_mcp_client_manager()`
- `src/runtime/harness.py`- 执行控制装置：Ayncio、MCPinit、信号处理器、清理
- `src/runtime/generate_wrappers.py`- 自动电源：连接所有服务器(stdio/SSE/HTTP)，内视计，生成`servers/<server>/<tool>.py` + `__init__.py`
- `src/runtime/discover_schemas.py`- Schema 发现：呼叫安全的只读工具，生成`servers/<server>/discovered_types.py`从实际答复中
- `src/runtime/normalize_fields.py`- 外地正常化：自动转换不一致的 API 外地外壳(例如：`system.parent` → `System.Parent`)

<a id="structure"></a>
## 结构
`servers/`(吉祥物，再生活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活活`uv run mcp-generate`):
```
servers/<serverName>/<toolName>.py         # Pydantic models, async wrapper
servers/<serverName>/__init__.py           # Barrel exports
servers/<serverName>/discovered_types.py   # Optional: Pydantic types from actual API responses
```

`scripts/`(基于 CLI 的参数模板 - 自由编辑逻辑):
```
scripts/<script_name>.py                    # Workflow with argparse, USAGE docstring
scripts/README.md                           # Scripts documentation
scripts/SCRIPTS.md                          # Complete framework guide
```

`mcp_config.json`格式(多运输):
```json
{
  "mcpServers": {
    "name_stdio": {
      "type": "stdio",
      "command": "command",
      "args": ["arg1"],
      "env": {}
    },
    "name_sse": {
      "type": "sse",
      "url": "https://...",
      "headers": {"Authorization": "Bearer ..."}
    },
    "name_http": {
      "type": "http",
      "url": "https://...",
      "headers": {"x-api-key": "..."}
    }
  }
}
```

`discovery_config.json`格式( 可选， 用于计划发现) :
```json
{"servers": {"name": {"safeTools": {"tool_name": {"param1": "value"}}}}}
```

<a id="workflow"></a>
## 工作流程

<a id="scripts-based-preferred"></a>
### 基于脚本( PREFERRED)
1. 发现 :`ls scripts/`— 见可用的脚本模板
2. 读取：`cat scripts/firecrawl_scrape.py`* 见 CLI 论点和使用法
3. 执行 :`uv run python -m runtime.harness scripts/firecrawl_scrape.py --url "https://example.com"`
4. 通过 CLI args 更改参数 - 自由地编辑脚本来修正错误或改进逻辑
5. 使用模板为您的特定工作流程创建自己的脚本

<a id="script-based-alternative"></a>
### 基于脚本( 备选案文)
1. 添加服务器： 编辑`mcp_config.json` or `.mcp.json`− 指定类型(stdio/sse/http)
2. 生成包装符 :`uv run mcp-generate`• 自动侦查运输
3. 导入脚本 :`from servers.name import tool_name`
4. 执行 :`uv run mcp-exec workspace/script.py`(一号电话自动连接)

任择计划发现： 副本`discovery_config.example.json`+ 编辑 w/ 安全只读工具 + 真实参数 →`uv run mcp-discover` → `from servers.name.discovered_types import ToolNameResult`

脚本图案( E)`workspace/`用于用户脚本，`tests/`实例：
```python
from servers.name import tool_name
from servers.name.discovered_types import ToolNameResult  # optional

result = await tool_name(params)  # Pydantic model
# Use defensive coding: result.field or fallback
# Return data - LLM can process/summarize in follow-up interactions
# Not all processing needs to happen in-script
```

<a id="key-details"></a>
## 密钥细节
- **脚本模式** - 通过 CLI 参数修改参数，编辑脚本以自由修正错误或改进逻辑
- **技能(Claude Code)** - 土著 SKILL.md 格式为。claude/技能/(自动由 Claude Code 发现)
- 工具标识 :`"serverName__toolName"`(双下划线)
- 逐步披露：
  - 有 CLI 参数的脚本：110 个令牌，减少 99.6%(PREFERRED)
  - 从头写出脚本：2K 个令牌，减少 98.7%(备选案文)
  - Claude Code Swills: 用于脚本发现的包装器(自动发现)
- 多运输： stdio(子进程)、SSE(活动)、HTTP(可流)
- **处理灵活性**: 脚本可以返回用于 LLM 处理的原始数据， 提高效率的预处理， 或者重塑用于链路工具调用 - 根据使用大小写选择
- 类型 gen: 用于所有计划、处理原始物、结合物、嵌入物、要求/选择物、剂量的活性模型
- Schema 发现： 只使用安全的只读工具( 绝不是突变), 类型为提示( 字段标记为可选) , 仍然使用防御编码
- 外地正常化：每个服务器自动应用(例如，ADO 将所有字段都正常化为 PascalCase，以实现一致性)
- Python: 用于货币的 Ayncio, 用于验证的 Pydantic, 用于类型安全的 mypy

<a id="troubleshooting"></a>
## 解决问题
- 找不到配置文件 : 创建`.mcp.json`或确保`mcp_config.json`已存在
- “ MCP 服务器未配置 ” : 检查配置文件密钥并确保`.env`已要求 API 密钥
- "连接已关闭":用`which <command>`
- 缺少包装 :`uv run mcp-generate`
- 导入错误： 确保`src/`在 sys.path 中(疾病处理这个)
- 类型检查 :`uv run mypy src/`用于验证
- 脚本 -- 帮助 :`python scripts/{script}.py --help`显示 CLI 参数

<a id="refs"></a>
## 参考文献
- [用 MCP 执行代码](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [MCP 光谱](https://modelcontextprotocol.io/)
- [MCP Python SDK 软件](https://github.com/modelcontextprotocol/python-sdk)

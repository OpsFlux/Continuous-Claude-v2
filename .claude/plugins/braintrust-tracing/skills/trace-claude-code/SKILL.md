---
name: trace-claude-code
description: |
  Automatically trace Claude Code conversations to Braintrust for observability.
  Captures sessions, conversation turns, and tool calls as hierarchical traces.
version: 1.1.0
---

<a id="trace-claude-code-to-braintrust"></a>
# 追踪 Claude Code 到大 Braintrust 任

自动向 Braintrust 发送 Claude 代码对话，用于追踪和可观察性。 在您的 AI 编码会话中获得全能可见度， 并带有显示会话、 转弯和每个工具呼叫的分级痕迹 。

<a id="what-you-get"></a>
## 你得到的东西

```
Claude Code Session (root trace)
├── Turn 1: "Add error handling"
│   ├── Read: src/app.ts
│   ├── Edit: src/app.ts
│   └── Response: "I've added try-catch..."
├── Turn 2: "Now run the tests"
│   ├── Terminal: npm test
│   └── Response: "All tests pass..."
└── Turn 3: "Great, commit this"
    ├── Terminal: git add .
    ├── Terminal: git commit -m "..."
    └── Response: "Changes committed..."
```

<a id="how-it-works"></a>
## 如何运作

四通钩捕捉到完整的工作流程：

| 钩子 | 它捕捉到的东西 |
|------|------------------|
| **会议开始** | 启动 Claude 代码时创建根跟踪 |
| **后工具的使用** | 抓取每个工具调用( 文件读取、 编辑、 终端命令) |
| **停车** | 抓取对话转动( 您的消息 + Claude 的答复) |
| **会议结束** | 退出时日志会话摘要 |

<a id="quick-setup"></a>
## 快速设置

在任何项目目录中运行要跟踪的设置脚本 :

```bash
bash /path/to/skills/trace-claude-code/setup.sh
```

您的 API 密钥和工程名称的脚本提示， 然后自动配置所有钩子 。

<a id="manual-setup"></a>
## 手动设置

<a id="prerequisites"></a>
### 先决条件

- [Claude 代码 CLI](https://docs.anthropic.com/en/docs/claude-code)已安装
- [大 Braintrust 任 API 密钥](https://www.braintrust.dev/app/settings/api-keys)
- `jq`命令行工具( R)`brew install jq`在 macOS 上).

<a id="configuration"></a>
### 配置

创建`.claude/settings.local.json`在您的工程目录中 :

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/session_start.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/post_tool_use.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/stop_hook.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/session_end.sh"
          }
        ]
      }
    ]
  },
  "env": {
    "TRACE_TO_BRAINTRUST": "true",
    "BRAINTRUST_API_KEY": "sk-...",
    "BRAINTRUST_CC_PROJECT": "my-project"
  }
}
```

替换`/path/to/hooks/`与本技能的钩子目录的实际路径相通。

<a id="environment-variables"></a>
### 环境变量

| 变量 | 需求 | 说明 |
|----------|----------|-------------|
| `TRACE_TO_BRAINTRUST` | 对 | 设定为`"true"`追踪 |
| `BRAINTRUST_API_KEY` | 对 | 您的大 Braintrust 任 API 密钥 |
| `BRAINTRUST_CC_PROJECT` | No | 项目名称( 默认 ):`claude-code`) |
| `BRAINTRUST_CC_DEBUG` | No | 设定为`"true"`用于动词记录 |

<a id="viewing-traces"></a>
## 查看痕迹

运行 Claude 代码并启用追踪后 :

1. 转到[大 Braintrust 任。dev](https://www.braintrust.dev)
2. 导航您的项目( 例如 )`claude-code`)
3. 点击 **日志** 查看所有可追溯到的会话

每个痕迹都显示：
- **会议根**: Claude 代码会议
- **转接**:每次对话交流(用户输入 = 助理响应)
- ** 电话： 单个操作( 文件读取、 编辑、 终端命令)

<a id="trace-structure"></a>
## 跟踪结构

追踪有等级：

- **会议**(根相间)
  - `span_attributes.type`: `"task"`
  - `metadata.session_id`: 独特的会话标识符
  - `metadata.workspace`: 项目目录

- **转会**(届会子女)
  - `span_attributes.type`: `"llm"`
  - `input`: 用户消息
  - `output`助理答复
  - `metadata.turn_number`: 顺序转号

- **调用工具**(轮班或会议子女)
  - `span_attributes.type`: `"tool"`
  - `input`: 工具输入(文件路径，命令等)
  - `output`: 工具结果
  - `metadata.tool_name`: 所使用的工具名称

<a id="troubleshooting"></a>
## 解决问题

<a id="no-traces-appearing"></a>
### 没有痕迹

1. **检查钩正在运行：**
   ```bash
   tail -f ~/.claude/state/braintrust_hook.log
   ```

2. **验证环境变量**`.claude/settings.local.json`:
   - `TRACE_TO_BRAINTRUST`必须是`"true"`
   - `BRAINTRUST_API_KEY`必须是有效的

3. **可启用调试模式 :**
   ```json
   {
     "env": {
       "BRAINTRUST_CC_DEBUG": "true"
     }
   }
   ```

<a id="permission-errors"></a>
### 权限错误

使钩脚本可执行 :

```bash
chmod +x /path/to/hooks/*.sh
```

<a id="missing-jq-command"></a>
### 缺少 jq 命令

安装 jq :
- **macOS**:`brew install jq`
- **Ubuntu/Debian**:`sudo apt-get install jq`

<a id="state-issues"></a>
### 国家问题

重置追踪状态 :

```bash
rm ~/.claude/state/braintrust_state.json
```

<a id="hook-logs"></a>
### 钩子日志

查看详细的钩子执行日志 :

```bash
# Follow logs in real-time
tail -f ~/.claude/state/braintrust_hook.log

# View last 50 lines
tail -50 ~/.claude/state/braintrust_hook.log

# Clear logs
> ~/.claude/state/braintrust_hook.log
```

<a id="file-structure"></a>
## 文件结构

```
hooks/
├── common.sh          # Shared utilities (logging, API, state)
├── session_start.sh   # Creates root trace span
├── post_tool_use.sh   # Captures tool calls
├── stop_hook.sh       # Captures conversation turns
└── session_end.sh     # Finalizes trace
```

<a id="alternative-sdk-integration"></a>
## 替代品：SDK 集成

为了与 Claude Agent SDK 一起进行方案使用，使用本地 Braintrust 整合：

```typescript
import { initLogger, wrapClaudeAgentSDK } from "braintrust";
import * as claudeSDK from "@anthropic-ai/claude-agent-sdk";

initLogger({
  projectName: "my-project",
  apiKey: process.env.BRAINTRUST_API_KEY,
});

const { query, tool } = wrapClaudeAgentSDK(claudeSDK);
```

见[Claude Agent SDK 文件](https://www.braintrust.dev/docs/integrations/sdk-integrations/claude-agent-sdk)详细情况。

---
name: hook-developer
description: Complete Claude Code hooks reference - input/output schemas, registration, testing patterns
---

<a id="hook-developer"></a>
# Hook 开发者

开发 Claude 密码钩的完整参考文献。 使用此来写入带有正确输入/输出策略的钩子。

<a id="when-to-use"></a>
## 何时使用

- 创建新钩子
- 调试钩子输入/输出格式
- 了解现有领域
- 在设置中设置钩注册。 json
- 学习什么钩可以阻断 vs 注入语境

<a id="quick-reference"></a>
## 快速引用

| 钩子 | 火灾 何时 | 能挡住吗? | 主要用途 |
|------|-----------|------------|-------------|
| **预用工具** | 工具执行前 | 对 | 块/修改工具呼叫 |
| **后工具的使用** | 工具完成后 | 部分 | 对工具结果的反应 |
| **用户提交** | 用户发送即时 | 对 | 验证/输入上下文 |
| **豁免请求** | 权限对话框显示 | 对 | 自动核准/拒绝 |
| **会议开始** | 会话开始 | NO | 装入上下文 |
| **会议结束** | 会话结束 | NO | 清理/保存状态 |
| **停车** | 代理结束 | 对 | 部队续设 |
| **副剂停止** | 子剂完成 | 对 | 部队续设 |
| **预编** | 收缩前 | NO | 保存状态 |
| **通知** | 发出的通知 | NO | 自定义提醒 |

---

<a id="hook-inputoutput-schemas"></a>
## Hook 输入/输出

<a id="pretooluse"></a>
### 工具预用

**目标：** 在工具执行发生前设置或修改执行 。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "PreToolUse",
  "tool_name": "string",
  "tool_input": {
    "file_path": "string",
    "command": "string"
  },
  "tool_use_id": "string"
}
```

**产出：**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string",
    "updatedInput": {}
  },
  "continue": true,
  "stopReason": "string",
  "systemMessage": "string",
  "suppressOutput": true
}
```

**出行代码 2:** Blocks 工具， Stderr 向 Claude 展示。

**共同匹配者：**`Bash`, `Edit|Write`, `Read`, `Task`, `mcp__.*`

---

<a id="posttooluse"></a>
### 后工具使用

**目标：** 对工具执行结果的反应，向 Claude 提供反馈。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "PostToolUse",
  "tool_name": "string",
  "tool_input": {},
  "tool_response": {
    "filePath": "string",
    "success": true,
    "output": "string",
    "exitCode": 0
  },
  "tool_use_id": "string"
}
```

**国家：** 反应领域是`tool_response`，没有`tool_result`.

**产出：**
```json
{
  "decision": "block",
  "reason": "string",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string"
  },
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true
}
```

**锁定：**`"decision": "block"`与`"reason"`促使 Claude 解决这个问题。

**共同匹配者：**`Edit|Write`, `Bash`

---

<a id="userpromptsubmit"></a>
### 用户 Prompt 提交

**目标：** 验证用户提示，在 Claude 进程前注入上下文。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "string"
}
```

**产出(书面文本):**
```
Any stdout text is added to context for Claude.
```

**产出：**
```json
{
  "decision": "block",
  "reason": "string",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string"
  }
}
```

**锁定：**`"decision": "block"`清除提示， 显示`"reason"`仅发送给用户(不是 Claude)。

**退出代码 2:** 块提示，仅向用户显示 stderr.

---

<a id="permissionrequest"></a>
### 权限请求

**目标：** 自动权限对话框决定。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "PermissionRequest",
  "tool_name": "string",
  "tool_input": {}
}
```

**产出：**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "message": "string",
      "interrupt": false
    }
  }
}
```

---

<a id="sessionstart"></a>
### 会话开始

**目标：** 初始化会话，装入上下文，设置环境变量。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact"
}
```

**环境变量：**`CLAUDE_ENV_FILE`- 写`export VAR=value`继续坚持下去

**产出(原始文本或 JSON):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string"
  },
  "suppressOutput": true
}
```

纯文本 stdout 作为上下文添加。

---

<a id="sessionend"></a>
### 结束会话

**目标：** 清理、保存状态、日志会话。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "SessionEnd",
  "reason": "clear|logout|prompt_input_exit|other"
}
```

**产出：** 无法影响会话( 已经结束 ) 。 仅用于清理。

---

<a id="stop"></a>
### 停下来

**目标：** Claude 停止时控制，继续部队。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

检查`stop_hook_active: true`防止无限循环!

**产出：**
```json
{
  "decision": "block",
  "reason": "string"
}
```

**锁定：**`"decision": "block"`Claude 继续`"reason"`尽快

---

<a id="subagentstop"></a>
### 副剂停止

**目的：**子剂(任务工具)停止时的控制。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false
}
```

**产出：** 与 Stop 相同。

---

<a id="precompact"></a>
### 预约

**目标：** 在上下文收缩前保存状态 。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "PreCompact",
  "trigger": "manual|auto",
  "custom_instructions": "string"
}
```

**竞争者：**`manual`, `auto`

**产出：**
```json
{
  "continue": true,
  "systemMessage": "string"
}
```

---

<a id="notification"></a>
### 通知

**目的：** 自定义通知处理。

**投入：**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "Notification",
  "message": "string",
  "notification_type": "permission_prompt|idle_prompt|auth_success|elicitation_dialog"
}
```

**竞争者：**`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `*`

**产出：**
```json
{
  "continue": true,
  "suppressOutput": true,
  "systemMessage": "string"
}
```

---

<a id="registration-in-settingsjson"></a>
## 在各种环境下进行登记。

<a id="standard-structure"></a>
### 标准结构

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/my-hook.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

<a id="matcher-patterns"></a>
### 匹配模式

| 图案 | 匹配 |
|---------|---------|
| `Bash` | 正是巴许工具 |
| 编辑|写作 | 编辑 OR 写入 |
| `Read.*` | Regex:读取* |
| `mcp__.*__write.*` | MCP 写入工具 |
| `*` | 所有工具 |

**对案件敏感：**`Bash` ≠ `bash`

<a id="events-requiring-matchers"></a>
### 需要匹配者的事件

- 工具使用前 - 是(需要)
- 后工具使用 - 是( 需要)
- 许可请求 - 是( 需要)
- 通知 - 是(可选)
- 会话启动 - 是( E)`startup|resume|clear|compact`)
- 预约 - 是( E)`manual|auto`)

<a id="events-without-matchers"></a>
### 没有匹配者的事件

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [{ "type": "command", "command": "/path/to/hook.sh" }]
      }
    ]
  }
}
```

---

<a id="environment-variables"></a>
## 环境变量

<a id="available-to-all-hooks"></a>
### 全钩可用

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | 项目根的绝对路径 |
| `CLAUDE_CODE_REMOTE` | “ true” 如果远程， 如果本地空 |

<a id="sessionstart-only"></a>
### 只开始会话

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_ENV_FILE` | 写入路径`export VAR=value`线条 |

---

<a id="exit-codes"></a>
## 退出代码

| 退出代码 | 行为 | 静态 | 标准 |
|-----------|----------|--------|--------|
| **0** | 成绩 | JSON 已处理 | 已忽略 |
| **2** | 屏蔽错误 | 关闭 | 错误消息 |
| **其他** | 非屏蔽错误 | 已忽略 | 微博模式 |

<a id="exit-code-2-by-hook"></a>
### Hook 的退出代码 2

| 钩子 | 效果 |
|------|--------|
| 工具预用 | 块工具， Stderr 到 Claude |
| 后工具使用 | Stderr 到 Claude( 工具已经运行) |
| 用户 Prompt 提交 | 块提示， 仅向用户显示 |
| 停下来 | 街站站住，向 Claude 报告 |

---

<a id="shell-wrapper-pattern"></a>
## 外壳折叠模式

```bash
#!/bin/bash
set -e
cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | npx tsx src/my-hook.ts
```

或被捆绑：

```bash
#!/bin/bash
set -e
cd "$HOME/.claude/hooks"
cat | node dist/my-hook.mjs
```

---

<a id="typescript-handler-pattern"></a>
## 类型脚本处理器模式

```typescript
import { readFileSync } from 'fs';

interface HookInput {
  session_id: string;
  hook_event_name: string;
  tool_name?: string;
  tool_input?: Record<string, unknown>;
  tool_response?: Record<string, unknown>;
  // ... other fields per hook type
}

function readStdin(): string {
  return readFileSync(0, 'utf-8');
}

async function main() {
  const input: HookInput = JSON.parse(readStdin());

  // Process input

  const output = {
    decision: 'block',  // or undefined to allow
    reason: 'Why blocking'
  };

  console.log(JSON.stringify(output));
}

main().catch(console.error);
```

---

<a id="testing-hooks"></a>
## 测试钩

<a id="manual-test-commands"></a>
### 手动测试命令

```bash
# PostToolUse (Write)
echo '{"tool_name":"Write","tool_input":{"file_path":"test.md"},"tool_response":{"success":true},"session_id":"test"}' | \
  .claude/hooks/my-hook.sh

# PreToolUse (Bash)
echo '{"tool_name":"Bash","tool_input":{"command":"ls"},"session_id":"test"}' | \
  .claude/hooks/my-hook.sh

# SessionStart
echo '{"hook_event_name":"SessionStart","source":"startup","session_id":"test"}' | \
  .claude/hooks/session-start.sh

# SessionEnd
echo '{"hook_event_name":"SessionEnd","reason":"clear","session_id":"test"}' | \
  .claude/hooks/session-end.sh

# UserPromptSubmit
echo '{"prompt":"test prompt","session_id":"test"}' | \
  .claude/hooks/prompt-submit.sh
```

<a id="rebuild-after-typescript-edits"></a>
### 键入脚本编辑后重建

```bash
cd .claude/hooks
npx esbuild src/my-hook.ts \
  --bundle --platform=node --format=esm \
  --outfile=dist/my-hook.mjs
```

---

<a id="common-patterns"></a>
## 常见模式

<a id="block-dangerous-files-pretooluse"></a>
### 屏蔽危险文件( PreTools)

```python
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
path = data.get('tool_input', {}).get('file_path', '')

BLOCKED = ['.env', 'secrets.json', '.git/']
if any(b in path for b in BLOCKED):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Blocked: {path} is protected"
        }
    }))
else:
    print('{}')
```

<a id="auto-format-files-posttooluse"></a>
### 自动格式文件( 后工具使用)

```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$FILE" == *.ts ]] || [[ "$FILE" == *.tsx ]]; then
  npx prettier --write "$FILE" 2>/dev/null
fi

echo '{}'
```

<a id="inject-git-context-userpromptsubmit"></a>
### 弹出基特上下文( UserPrompt Submit)

```bash
#!/bin/bash
echo "Git status:"
git status --short 2>/dev/null || echo "(not a git repo)"
echo ""
echo "Recent commits:"
git log --oneline -5 2>/dev/null || echo "(no commits)"
```

<a id="force-test-verification-stop"></a>
### 部队测试核查(停止)

```python
#!/usr/bin/env python3
import json, sys, subprocess

data = json.load(sys.stdin)

# Prevent infinite loops
if data.get('stop_hook_active'):
    print('{}')
    sys.exit(0)

# Check if tests pass
result = subprocess.run(['npm', 'test'], capture_output=True)
if result.returncode != 0:
    print(json.dumps({
        "decision": "block",
        "reason": "Tests are failing. Please fix before stopping."
    }))
else:
    print('{}')
```

---

<a id="debugging-checklist"></a>
## 调试检查列表

- [ ] Hook 注册在设置中。 json?
- [ ] 贝壳脚本`+x`允许吗?
- [ ] 在 TS 更改后重建了套装吗 ?
- [ ] 使用`tool_response`没有`tool_result`?
- [ ] 输出是有效的 JSON( 或者纯文本) ?
- [ ] 检查中`stop_hook_active`在停止钩?
- [ ] 使用`$CLAUDE_PROJECT_DIR`为路径?

---

<a id="key-learnings-from-past-sessions"></a>
## 过去会议的关键学习

1. **外地名称很重要** -`tool_response`没有`tool_result`
2. **产出格式** -`decision: "block"` + `reason`用于屏蔽
3. **退出代号 2** - stderr 去 Claude/用户，stdout IGNORED
4. **重建捆绑** - TypeScript 源编辑不自动应用
5. **手工试验** -`echo '{}' | ./hook.sh`在依赖它之前
6. **首先检查产出** -`ls .claude/cache/`在编辑代码前
7. **分离产卵隐藏出错** - 在调试中添加记录

<a id="see-also"></a>
## 另见

- `/debug-hooks`- 系统调试工作流程
- `.claude/rules/hooks.md`- Hook 发展规则

---
globs: [".claude/hooks/**/*"]
---

<a id="hook-development-rules"></a>
# Hook 发展规则

处理文件时`.claude/hooks/`:

<a id="pattern"></a>
## 图案
壳包 (.sh) → TypeScript (.ts) 通过`npx tsx`

<a id="shell-wrapper-template"></a>
## 外壳折叠模板
```bash
#!/bin/bash
set -e
cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | npx tsx <handler>.ts
```

<a id="typescript-handler-pattern"></a>
## 类型脚本处理器模式
```typescript
interface HookInput {
  // Event-specific fields
}

async function main() {
  const input: HookInput = JSON.parse(await readStdin());

  // Process input

  const output = {
    result: 'continue',  // or 'block'
    message: 'Optional system reminder'
  };

  console.log(JSON.stringify(output));
}
```

<a id="hook-events"></a>
## 钩子事件
- **PreTools 使用** - 工具执行前 (可以块)
- **后工具使用** - 工具执行后
- **UserPrompt Submit** - 处理用户提示前
- **预装** - 上下文收缩前
- **会议开始** - 在会话开始/恢复/协议时
- **停止** - 当代理完成时

<a id="testing"></a>
## 测试
手动测试钩 :
```bash
echo '{"type": "resume"}' | .claude/hooks/session-start-continuity.sh
```

<a id="registration"></a>
## 登记
添加钩子到`.claude/settings.json`:
```json
{
  "hooks": {
    "EventName": [{
      "matcher": ["pattern"],  // Optional
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/hook.sh"
      }]
    }]
  }
}
```

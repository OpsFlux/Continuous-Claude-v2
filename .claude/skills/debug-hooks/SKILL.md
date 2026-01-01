---
name: debug-hooks
description: Systematic hook debugging workflow. Use when hooks aren't firing, producing wrong output, or behaving unexpectedly.
allowed-tools: [Bash, Read, Grep]
---

<a id="debug-hooks"></a>
# 除错钩

调试 Claude 密码钩的系统工作流程。

<a id="when-to-use"></a>
## 何时使用

- "Hook 不是开火"
- "Hook 输出错误"
- "会议结束不工作"
- "后取用钩子不触发"
- "为什么我的钩子不跑?"

<a id="workflow"></a>
## 工作流程

<a id="1-check-outputs-first-observe-before-editing"></a>
### 1. 请检查 access-date=中的日期值 (帮助)

```bash
# Check project cache
ls -la $CLAUDE_PROJECT_DIR/.claude/cache/

# Check specific outputs
ls -la $CLAUDE_PROJECT_DIR/.claude/cache/learnings/

# Check for debug logs
tail $CLAUDE_PROJECT_DIR/.claude/cache/*.log 2>/dev/null

# Also check global (common mistake: wrong path)
ls -la ~/.claude/cache/ 2>/dev/null
```

<a id="2-verify-hook-registration"></a>
### 2. 验证钩登记

```bash
# Project settings
cat $CLAUDE_PROJECT_DIR/.claude/settings.json | grep -A 20 '"SessionEnd"\|"PostToolUse"\|"UserPromptSubmit"'

# Global settings (hooks merge from both)
cat ~/.claude/settings.json | grep -A 20 '"SessionEnd"\|"PostToolUse"\|"UserPromptSubmit"'
```

<a id="3-check-hook-files-exist"></a>
### 3. 检查 Hook 文件

```bash
# Shell wrappers
ls -la $CLAUDE_PROJECT_DIR/.claude/hooks/*.sh

# Compiled bundles (if using TypeScript)
ls -la $CLAUDE_PROJECT_DIR/.claude/hooks/dist/*.mjs
```

<a id="4-test-hook-manually"></a>
### 4. 人工试验钩

```bash
# SessionEnd hook
echo '{"session_id": "test-123", "reason": "clear", "transcript_path": "/tmp/test"}' | \
  $CLAUDE_PROJECT_DIR/.claude/hooks/session-end-cleanup.sh

# PostToolUse hook (Write tool example)
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.md"}, "session_id": "test-123"}' | \
  $CLAUDE_PROJECT_DIR/.claude/hooks/handoff-index.sh
```

<a id="5-check-for-silent-failures"></a>
### 5. 检查无声故障

如果使用离子产卵`stdio: 'ignore'`:

```typescript
// This pattern hides errors!
spawn(cmd, args, { detached: true, stdio: 'ignore' })
```

**文件编号：** 添加临时日志 :

```typescript
const logFile = fs.openSync('.claude/cache/debug.log', 'a');
spawn(cmd, args, {
  detached: true,
  stdio: ['ignore', logFile, logFile]  // capture stdout/stderr
});
```

<a id="6-rebuild-after-edits"></a>
### 6. 编辑后重建

如果您编辑了 TypeScript 源， 您必须重建 :

```bash
cd $CLAUDE_PROJECT_DIR/.claude/hooks
npx esbuild src/session-end-cleanup.ts \
  --bundle --platform=node --format=esm \
  --outfile=dist/session-end-cleanup.mjs
```

光是源编辑不会生效 - shell 包装器运行捆绑`.mjs`.

<a id="common-issues"></a>
## 共同问题

| 症状 | 可能的原因是 | 修补 |
|---------|--------------|-----|
| Hook 从不跑 | 未在设置中注册。 json | 在设置中添加到正确的事件 |
| Hook 运行但没有输出 | 分离的产卵隐藏错误 | 添加日志， 手动检查 |
| 错误会话 ID | 使用“ 最近的” 查询 | 明确通过 ID |
| 在当地工作，不在中情局工作 | 缺少依赖关系 | 检查 npx/ 节点可用性 |
| 运行两次 | 在两个全球+项目注册 | 删除重复 |

<a id="debug-checklist"></a>
## 除错检查列表

- [ ] 产出存在吗?`ls -la .claude/cache/`)
- [ ] 注册? (`grep -A10 '"hooks"' .claude/settings.json`)
- [ ] 文件存在吗?`ls .claude/hooks/*.sh`)
- [ ] 捆绑电流?`ls -la .claude/hooks/dist/`)
- [ ] 手工测试工作?`echo '{}' | ./hook.sh`)
- [ ] 没有沉默的失败? (检查`stdio: 'ignore'`)

<a id="source-sessions"></a>
## 源会话

从 10 个课(占所有学习的 83%)中得出：
- a541f08a, 1c21e6c8, 6a9f2d7a, a8bd5cea, 2ca1a178, 657ce0b2, 3998f3a2, 2a829f12, 0b46cfd7, 862f6e2c

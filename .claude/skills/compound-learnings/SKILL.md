---
name: compound-learnings
description: Transform session learnings into permanent capabilities (skills, rules, agents). Use when asked to "improve setup", "learn from sessions", "compound learnings", or "what patterns should become skills".
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion]
---

<a id="compound-learnings"></a>
# 复合学习

将电子会话学习转化为永久的复合能力。

<a id="when-to-use"></a>
## 何时使用

- "我应该从最近的会议学到什么?"
- "根据最近的工作改进我的设置"
- "把学习变成技能/规则"
- "什么模式应该成为永久的?"
- "整理我的学习"

<a id="process"></a>
## 进程

<a id="step-1-gather-learnings"></a>
### 步骤 1:收集学习

```bash
# List learnings (most recent first)
ls -t $CLAUDE_PROJECT_DIR/.claude/cache/learnings/*.md | head -20

# Count total
ls $CLAUDE_PROJECT_DIR/.claude/cache/learnings/*.md | wc -l
```

读取最新的 5- 10 文件( 或指定日期范围) 。

<a id="step-2-extract-patterns-structured"></a>
### 步骤 2:取出模式(已定出)

对于每个学习文件，请从这些具体章节中提取条目：

| 区域标题 | 要提取什么 |
|----------------|-----------------|
| `## Patterns` or `Reusable techniques` | 规则的直接候选人 |
| `**Takeaway:**` or `**Actionable takeaway:**` | 决定的弹性 |
| `## What Worked` | 成功模式 |
| `## What Failed` | 反标(倒置规则) |
| `## Key Decisions` | 设计原则 |

创建频率表 :

```markdown
| Pattern | Sessions | Category |
|---------|----------|----------|
| "Check artifacts before editing" | abc, def, ghi | debugging |
| "Pass IDs explicitly" | abc, def, ghi, jkl | reliability |
```

<a id="step-2b-consolidate-similar-patterns"></a>
### 步骤 2b:巩固类似模式

在计数前，合并表达相同原理的图案：

**合并实例：**
- "艺术第一调试"
- “通过检查文件验证钩子输出”
- "系统第一次调试"
——全部表示：**"编辑代码前观察输出"**

采用最通俗的表述。 更新频率表 。

<a id="step-3-detect-meta-patterns"></a>
### 步骤 3: 检测元数据

**关键步骤：** 观所学相聚相。

如果大于 50%的模式涉及一个主题(如"呼克","追踪","同步"):
专题可能需要专门技能** 而不是多重规则
- 一种技能比五项规则更好

问自己："是否有一种技能可以使所有这些规则变得没有必要".

<a id="step-4-categorize-decision-tree"></a>
### 第 4 步：分类(决定树)

对于每种图案，确定文物类型：

```
Is it a sequence of commands/steps?
  → YES → SKILL (executable > declarative)
  → NO ↓

Should it run automatically on an event (SessionEnd, PostToolUse, etc.)?
  → YES → HOOK (automatic > manual)
  → NO ↓

Is it "when X, do Y" or "never do X"?
  → YES → RULE
  → NO ↓

Does it enhance an existing agent workflow?
  → YES → AGENT UPDATE
  → NO → Skip (not worth capturing)
```

**艺术类型示例：**

| 图案 | 类型 | 为什么 |
|---------|------|-----|
| "行刑前逃跑" | Hook (预工具使用) | 自动闸门 |
| “会话结束时的总结学习” | Hook(会议结束) | 自动触发 |
| "除虫钩" | 技能 | 手动序列 |
| "总是通过身份证明" | 规则 | 高压 |

<a id="step-5-apply-signal-thresholds"></a>
### 第 5 步： 应用信号阈值

| 发生情况 | 行动 |
|-------------|--------|
| 1 | 注但跳过( 除非关键失败) |
| 2 | 考虑 - 提交用户 |
| 3+ | 强信号 - 建议创建 |
| 4+ | 绝对创建 |

<a id="step-6-propose-artifacts"></a>
### 第 6 步：提议人工制品

以这种格式提出每项提案：

```markdown
---

## Pattern: [Generalized Name]

**Signal:** [N] sessions ([list session IDs])

**Category:** [debugging / reliability / workflow / etc.]

**Artifact Type:** Rule / Skill / Agent Update

**Rationale:** [Why this artifact type, why worth creating]

**Draft Content:**
\`\`\`markdown
[Actual content that would be written to file]
\`\`\`

**File:** `.claude/rules/[name].md` or `.claude/skills/[name]/SKILL.md`

---
```

使用`AskUserQuestion`为每个文物获得批准(或批次批准)。

<a id="step-7-create-approved-artifacts"></a>
### 步骤 7: 创建已核准的艺术

<a id="for-rules"></a>
#### 规则：
```bash
# Write to rules directory
cat > $CLAUDE_PROJECT_DIR/.claude/rules/<name>.md << 'EOF'
# Rule Name

[Context: why this rule exists, based on N sessions]

## Pattern
[The reusable principle]

## DO
- [Concrete action]

## DON'T
- [Anti-pattern]

## Source Sessions
- [session-id-1]: [what happened]
- [session-id-2]: [what happened]
EOF
```

<a id="for-skills"></a>
#### 技能：
创建`.claude/skills/<name>/SKILL.md`改为：
- 前题( 名称、 描述、 允许的工具)
- 何时使用
- 分步指示(可执行)
- 学习中的实例

添加触发到`skill-rules.json`酌情。

<a id="for-hooks"></a>
#### 对于 Hook:
创建外壳包装器 + TypeScript 处理器 :

```bash
# Shell wrapper
cat > $CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh << 'EOF'
#!/bin/bash
set -e
cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | node dist/<name>.mjs
EOF
chmod +x $CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh
```

然后创建`src/<name>.ts`中，用 ebuild 建造，并在`settings.json`:

```json
{
  "hooks": {
    "EventName": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh"
      }]
    }]
  }
}
```

<a id="for-agent-updates"></a>
#### 对于代理更新 :
在`.claude/agents/<name>.md`增加学习能力。

<a id="step-8-summary-report"></a>
### 步骤 8:简要报告

```markdown
## Compounding Complete

**Learnings Analyzed:** [N] sessions
**Patterns Found:** [M]
**Artifacts Created:** [K]

### Created:
- Rule: `explicit-identity.md` - Pass IDs explicitly across boundaries
- Skill: `debug-hooks` - Hook debugging workflow

### Skipped (insufficient signal):
- "Pattern X" (1 occurrence)

**Your setup is now permanently improved.**
```

<a id="quality-checks"></a>
## 质量检查

在创建任何文物之前：

1. **足够笼统吗?** 它是否适用于其他项目?
2. 足够具体了吗? 它提供了具体指导吗?
3. **是否已经存在?** 检查`.claude/rules/`和`.claude/skills/`第一个
4. **类型合适吗?** 序列 技能 高压 规则

<a id="files-reference"></a>
## 文件参考

- 学习：`.claude/cache/learnings/*.md`
- 技能：`.claude/skills/<name>/SKILL.md`
- 规则：`.claude/rules/<name>.md`
- 钩子：`.claude/hooks/<name>.sh` + `src/<name>.ts` + `dist/<name>.mjs`
- 探员：`.claude/agents/<name>.md`
- 技能触发 :`.claude/skills/skill-rules.json`
- 钩注册 :`.claude/settings.json` → `hooks`节

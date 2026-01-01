---
description: Create handoff document for transferring work to another session
---

<a id="create-handoff"></a>
# 创建交接

您负责在新的会话中将您的工作交给另一位代理人。 你将制作一份详尽的交接文件，但也要**简明**。 目标是压缩和总结你的背景，同时不丢失你正在研究的任何关键细节。


<a id="process"></a>
## 进程
<a id="1-filepath-metadata"></a>
### 1. 文件路径和元数据
使用下列信息来了解如何创建文档：

**首先，确定当前分类账中的会话名称：**
```bash
ls thoughts/ledgers/CONTINUITY_CLAUDE-*.md 2>/dev/null | head -1 | sed 's/.*CONTINUITY_CLAUDE-\(.*\)\.md/\1/'
```

这返回活动的工作流名称(例如，`open-source-release`) (中文(简体) ). 将此作为交接文件夹名称 。

如果没有分类账，请使用`general`作为文件夹名称。

**创建您的文件。**`thoughts/shared/handoffs/{session-name}/YYYY-MM-DD_HH-MM-SS_description.md`，其中：
- `{session-name}`来源于分类账(例如，`open-source-release`) or `general`如果没有分类账
- `YYYY-MM-DD`今天的日期
- `HH-MM-SS`是当前 24 小时格式的
- `description`是一个简单的 kebab 案例描述

运行`~/.claude/scripts/spec_metadata.sh`生成所有相关元数据的脚本

<a id="1b-braintrust-trace-ids-for-artifact-index"></a>
### 1b. 大 Braintrust 任追踪(用于人工活性指数)
读取 Braintrust 会话状态文件以获取链接到会话的跟踪 ID :

```bash
cat ~/.claude/state/braintrust_sessions/*.json | jq -s 'sort_by(.started) | last'
```

此返回 JSON 时使用 :
- `root_span_id`: Braintust 追踪身份(使用此功能)
- `current_turn_span_id`: 当前转弯横跨 ID( 以此为转弯  span  id)

这个`session_id`是文件名干(在大多数情况下与 root span id 相同)。

如果没有状态文件( Brintrust 未配置) , 请留空这些字段 。

**实例：**
- 有分类账`open-source-release`: `thoughts/shared/handoffs/open-source-release/2025-01-08_13-55-22_create-context-compaction.md`
- 无分类账(一般):`thoughts/shared/handoffs/general/2025-01-08_13-55-22_create-context-compaction.md`

<a id="2-handoff-writing"></a>
### 2. 手稿写作。
使用上述公约，写出您的文件。 使用定义的文件路径，并使用下面的 YAML 前题模式。 使用步骤 1 所收集的元数据 。

使用以下模板结构：
```markdown
---
date: [Current date and time with timezone in ISO format]
session_name: [From ledger, e.g., "open-source-release" - see step 1]
researcher: [Researcher name from thoughts status]
git_commit: [Current commit hash]
branch: [Current branch name]
repository: [Repository name]
topic: "[Feature/Task Name] Implementation Strategy"
tags: [implementation, strategy, relevant-component-names]
status: complete
last_updated: [Current date in YYYY-MM-DD format]
last_updated_by: [Researcher name]
type: implementation_strategy
root_span_id: [Braintrust trace ID - see step 1b]
turn_span_id: [Current turn span ID - see step 1b]
---

# Handoff: {very concise description}

## Task(s)
{description of the task(s) that you were working on, along with the status of each (completed, work in progress, planned/discussed). If you are working on an implementation plan, make sure to call out which phase you are on. Make sure to reference the plan document and/or research document(s) you are working from that were provided to you at the beginning of the session, if applicable.}

## Critical References
{List any critical specification documents, architectural decisions, or design docs that must be followed. Include only 2-3 most important file paths. Leave blank if none.}

## Recent changes
{describe recent changes made to the codebase that you made in line:file syntax}

## Learnings
{describe important things that you learned - e.g. patterns, root causes of bugs, or other important pieces of information someone that is picking up your work after you should know. consider listing explicit file paths.}

## Post-Mortem (Required for Artifact Index)

### What Worked
{Describe successful approaches, patterns that helped, tools that worked well. Be specific - these get indexed for future sessions.}
- Approach 1: [what and why it worked]
- Pattern: [pattern name] was effective because [reason]

### What Failed
{Describe attempted approaches that didn't work, errors encountered, dead ends. This helps future sessions avoid the same mistakes.}
- Tried: [approach] → Failed because: [reason]
- Error: [error type] when [action] → Fixed by: [solution]

### Key Decisions
{Document important choices made during this task and WHY they were made. Future sessions will reference these.}
- Decision: [choice made]
  - Alternatives considered: [other options]
  - Reason: [why this choice]

## Artifacts
{ an exhaustive list of artifacts you produced or updated as filepaths and/or file:line references - e.g. paths to feature documents, implementation plans, etc that should be read in order to resume your work.}

## Action Items & Next Steps
{ a list of action items and next steps for the next agent to accomplish based on your tasks and their statuses}

## Other Notes
{ other notes, references, or useful information - e.g. where relevant sections of the codebase are, where relevant documents are, or other important things you leanrned that you want to pass on but that don't fall into the above categories}
```
---

<a id="3-mark-session-outcome-required"></a>
### 3. 马克会议结果(REQUIRED)

**重要性：** 在回复用户之前， 您需要询问会话结果 。

使用带有这些精确选项的 AskUserQuestion 工具：

```
Question: "How did this session go?"
Options:
  - SUCCEEDED: Task completed successfully
  - PARTIAL_PLUS: Mostly done, minor issues remain
  - PARTIAL_MINUS: Some progress, major issues remain
  - FAILED: Task abandoned or blocked
```

在用户回复后，请标出结果：
```bash
# Get the handoff ID (use the one just created)
HANDOFF_ID=$(sqlite3 .claude/cache/artifact-index/context.db "SELECT id FROM handoffs ORDER BY indexed_at DESC LIMIT 1")

# Mark the outcome
uv run python scripts/artifact_mark.py --handoff $HANDOFF_ID --outcome <USER_CHOICE>
```

如果数据库还不存在(第一手)，则跳过标记步骤，但仍会提问。

<a id="4-confirm-completion"></a>
### 4. 确认完成

在标出结果后，回复用户：

```
Handoff created! Outcome marked as [OUTCOME].

Resume in a new session with:
/resume_handoff path/to/handoff.md
```

-- -- . . .
□. 附加注释和指令
- **更多信息，而不是更少**。 这是一条准则，界定了交割的最低限度。 如有必要，随时可以提供更多信息。
- **彻底而精确**. 包括最高一级的目标，必要时包括低一级的细节。
- **避免过多代码片段**. 虽然简短的片段来描述一些关键更改很重要，但避免大代码块或 diff;除非有必要，不包含一个(例如与您正在调试的错误有关). 优先使用`/path/to/file.ext:line`一个代理在准备就绪后可以遵循的参考文献，例如。`packages/dashboard/src/app/dashboard/page.tsx:12-24`

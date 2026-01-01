---
description: Debug issues by investigating logs, database state, and git history
---

<a id="debug"></a>
# 调试

您的任务是在手动测试或执行过程中帮助调试问题 。 此命令允许您通过检查日志，数据库状态和 git 历史来调查问题，而不编辑文件 。 将它视为不使用主窗口的上下文来拖住调试会话的方法 。

<a id="initial-response"></a>
## 初步反应

以计划/计数板文件引用时：
```
I'll help debug issues with [file name]. Let me understand the current state.

What specific problem are you encountering?
- What were you trying to test/implement?
- What went wrong?
- Any error messages?

I'll investigate the logs, database, and git state to help figure out what's happening.
```

当引用没有参数时：
```
I'll help debug your current issue.

Please describe what's going wrong:
- What are you working on?
- What specific problem occurred?
- When did it last work?

I can investigate logs, database state, and recent changes to help identify the issue.
```

<a id="environment-information"></a>
## 环境信息

您可以访问这些关键地点和工具：

**记录**:
- 应用程序日志(检查项目具体地点)
- 共同地点：`./logs/`, `~/.local/share/{app}/`, `/var/log/`

**数据库**(如果适用):
- SQLite 数据库可以查询`sqlite3`
- 检查数据库位置的工程配置

**国籍国**:
- 检查当前分支、 最近承诺、 未承诺的更改
- 类似如何`commit`和`describe_pr`命令工作

**服务状况**:
- 检查运行的过程 :`ps aux | grep {service}`
- 检查监听端口 :`lsof -i :{port}`

<a id="process-steps"></a>
## 步骤

<a id="step-1-understand-the-problem"></a>
### 步骤 1:了解问题

在用户描述问题后：

1. **阅读任何提供的上下文**(计划或票单文件):
   - 了解他们执行/测试的内容
   - 注意他们的哪个阶段或步骤
   - 识别预期对实际行为

2. 快速状态检查**:
   - 当前 git 分支和最近承诺
   - 任何未承诺的更改
   - 问题开始的时候

<a id="step-2-investigate-the-issue"></a>
### 步骤 2:调查问题

大量平行任务代理，以高效调查：

```
Task 1 - Check Recent Logs:
Find and analyze the most recent logs for errors:
1. Find latest logs: ls -t ./logs/*.log | head -1 (or project-specific location)
2. Search for errors, warnings, or issues around the problem timeframe
3. Note the working directory if shown
4. Look for stack traces or repeated errors
Return: Key errors/warnings with timestamps
```

```
Task 2 - Database State (if applicable):
Check the current database state:
1. Locate database file (check project config)
2. Connect: sqlite3 {database_path}
3. Check schema: .tables and .schema for relevant tables
4. Query recent data based on the issue
5. Look for stuck states or anomalies
Return: Relevant database findings
```

```
Task 3 - Git and File State:
Understand what changed recently:
1. Check git status and current branch
2. Look at recent commits: git log --oneline -10
3. Check uncommitted changes: git diff
4. Verify expected files exist
5. Look for any file permission issues
Return: Git state and any file issues
```

<a id="step-3-present-findings"></a>
### 步骤 3:提出调查结果

根据调查，提交重点调试报告：

```markdown
## Debug Report

### What's Wrong
[Clear statement of the issue based on evidence]

### Evidence Found

**From Logs**:
- [Error/warning with timestamp]
- [Pattern or repeated issue]

**From Database** (if applicable):
```sql
-- 相关查询和结果
[从数据库查找]
```

**From Git/Files**:
- [Recent changes that might be related]
- [File state issues]

### Root Cause
[Most likely explanation based on evidence]

### Next Steps

1. **Try This First**:
   ```bash
[具体命令或行动]
   ```

2. **If That Doesn't Work**:
   - Restart relevant services
   - Check browser console for frontend errors
   - Run with debug flags enabled

### Can't Access?
Some issues might be outside my reach:
- Browser console errors (F12 in browser)
- MCP server internal state
- System-level issues

Would you like me to investigate something specific further?
```

<a id="important-notes"></a>
## 重要说明

- **以人工测试情景为重点** - 用于执行时调试
- **总是需要问题描述** - 不能在不知道出错的情况下调试
- **完全读取文件** - 阅读上下文时没有限制/抵销
- {\fn 黑体。s20\shad2\2aH82\3aH20\4aH33\fscx95\3cH592001\be1}想起来`commit` or `describe_pr`** - 了解基特状态和变化
- **回向用户** - 某些问题(浏览器控制台，MCP 内部)是无法触及的
- **不编辑文件** - 只调查

<a id="quick-reference"></a>
## 快速引用

**找到最新记录**:
```bash
ls -t ./logs/*.log | head -1
# Or check project-specific log locations
```

**数据库查询**(SQLite):
```bash
sqlite3 {database_path} ".tables"
sqlite3 {database_path} ".schema {table}"
sqlite3 {database_path} "SELECT * FROM {table} ORDER BY created_at DESC LIMIT 5;"
```

**服务检查**:
```bash
ps aux | grep {service_name}
lsof -i :{port}
```

**国籍国**:
```bash
git status
git log --oneline -10
git diff
```

记住： 此命令可以帮助您在不刻录主窗口上下文的情况下进行调查 。 完全适合在人工测试中遇到问题时 需要挖掘日志、数据库或 git 状态

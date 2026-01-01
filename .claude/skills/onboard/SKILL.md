---
name: onboard
description: Analyze brownfield codebase and create initial continuity ledger
---

<a id="onboard-project-discovery-ledger-creation"></a>
# 上载 - 项目发现和编辑器创建

分析一个棕地密码库，并创建一个初始的连续性分类账。

<a id="when-to-use"></a>
## 何时使用

- 第一次在现有项目中工作
- 用户表示"上","分析这个项目","熟悉代码库".
- 运行后`init-project.sh`在新项目中

<a id="how-to-use"></a>
## 如何使用

**机上代理人：**

使用任务工具`subagent_type: "general-purpose"`而这个提示 :

```
Onboard me to this project.

Read and follow the instructions in .claude/agents/onboard.md exactly.

1. Check if thoughts/ledgers/ exists (if not, tell me to run init-project.sh)
2. Set RepoPrompt workspace to this project, then explore:
   rp-cli -e "workspace switch \"$CLAUDE_PROJECT_DIR\""
   rp-cli -e 'tree'
   rp-cli -e 'structure .'
   rp-cli -e 'builder "understand the codebase architecture"'
3. If rp-cli not available, fall back to bash (find, ls, etc.)
4. Detect tech stack
5. Ask me about my goals using AskUserQuestion
6. Create a continuity ledger at thoughts/ledgers/CONTINUITY_CLAUDE-<project>.md
```

<a id="why-an-agent"></a>
## 为什么是代理?

机上进程 :
- 需要多个勘探步骤( RepoPrompt 构建器缓慢)
- 不应污染主上下文的代码库垃圾堆
- 返回干净摘要 + 创建分类账

<a id="output"></a>
## 产出

- 在`thoughts/ledgers/CONTINUITY_CLAUDE-<name>.md`
- 用户有明确的起始上下文
- 做好全面了解项目工作的准备

<a id="notes"></a>
## 页：1

- 该技能用于 BROWNFIELD 项目(现有代码)
- 用于绿地`/create_plan`换成
- 编辑器可以随时更新`/continuity_ledger`
- RepoPrompt 需要使用 MCP 服务器运行的应用程序

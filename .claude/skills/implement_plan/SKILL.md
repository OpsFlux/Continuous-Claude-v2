---
description: Implement technical plans from thoughts/shared/plans with verification
---

<a id="implement-plan"></a>
# 执行计划

你的任务是执行经核准的技术计划`thoughts/shared/plans/`这些计划包含有具体变化和成功标准的阶段。

<a id="execution-modes"></a>
## 执行模式

您有两种执行模式：

<a id="mode-1-direct-implementation-default"></a>
### 方式 1:直接执行(违约)
对于小型计划(3 个或更少的任务)，或者当用户要求直接执行时。
- 你自己执行每个阶段
- 主对话中累积上下文
- 用于快速、有重点的执行

<a id="mode-2-agent-orchestration-recommended-for-larger-plans"></a>
### 模式 2:代理管弦乐团(为较大的计划推荐)
对于有 4+任务的计划，或者当环境保存至关重要时。
- 你扮演一个瘦的管弦乐家
- 代理执行每项任务并创建交割
- 抗紧凑性：即使上下文紧凑，交割仍持续
- 用于多阶段执行

**要使用代理管弦乐模式**，请说："我会为这个计划使用代理管弦乐"，并遵循下面代理管弦乐部分。

---

<a id="getting-started"></a>
## 开始

当给定计划路径时：
- 完全读取计划并检查任何已存在的检查标记 (- [x])
- 阅读计划中提到的原始票和所有文件
- **完全读取文件** - 从不使用限制/抵消参数，您需要完整的上下文
- 深思熟虑 如何拼凑在一起
- 创建待办事宜列表以跟踪您的进度
- 了解需要做什么就开始执行

如果没有提供计划路径，则要求一条。

<a id="implementation-philosophy"></a>
## 执行哲学

计划是精心设计的，但现实可能很乱。 你的职责是：
- 遵循计划的意图 同时适应你的发现
- 在移动到下一个阶段前， 完全执行每个阶段
- 在更广泛的代码库背景中验证您的工作是有意义的
- 完成段落时更新计划中的复选框

当事情与计划不完全吻合时，想想原因，清楚沟通。 计划是你的向导 但你的判断也很重要

如果遇到错配：
- 停下来好好想想为什么计划不能被执行
- 明确提出问题：
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```

<a id="verification-approach"></a>
## 核查办法

实施阶段后：
- 运行成功标准检查(通常是)`make check test`涵盖一切)
- 处理任何问题之前
- 更新您的计划及任务进度
- 使用 Edit 检查计划中已完成的项目
- **暂停人力核查**: 在完成一个阶段的所有自动化验证后，暂停并告知人类该阶段已准备好进行人工测试。 使用此格式 :
  ```
  Phase [N] Complete - Ready for Manual Verification

  Automated verification passed:
  - [List automated checks that passed]

  Please perform the manual verification steps listed in the plan:
  - [List manual verification items from the plan]

  Let me know when manual testing is complete so I can proceed to Phase [N+1].
  ```

如果指示连续执行多个相，则跳过暂停到最后一个相。 否则，假设你只是做一个阶段。

在用户确认之前，不检查人工测试步骤中的项目。


<a id="if-you-get-stuck"></a>
## 如果你被困住了的话

当事情不起作用时：
- 首先，确保你已经读懂 所有相关代码
- 考虑一下密码库是否已经进化 从计划编写之后
- 说明不匹配 并请求指导

节制使用子任务——主要用于定向调试或探索陌生领地。

<a id="resumable-agents"></a>
## 有偿代理

如果计划是由`plan-agent`，您可能可以恢复它以澄清：

1. 检查`.claude/cache/agents/agent-log.jsonl`计划代理条目
2. 寻找`agentId`字段
3. 为澄清或更新计划：
   ```
   Task(
     resume="<agentId>",
     prompt="Phase 2 isn't matching the codebase. Can you clarify..."
   )
   ```

恢复的代理保留其完整的前置上下文(研究，代码库分析).

可恢复的代理 :
- `plan-agent`- 制定执行计划
- `research-agent`- 研究最佳做法
- `debug-agent`- 调查的问题

<a id="resuming-work"></a>
## 恢复工作

如果计划有现有的检查标记：
- 相信已完成的工作已经完成
- 从第一个未选中的项目中拾取
- 只有在有问题时才验证前次工作

记住，你正在执行一个解决方案，不只是检查盒子。 牢记最终目标并保持前进势头。

---

<a id="agent-orchestration-mode"></a>
## 代理管弦乐模式

在执行更大的计划(4+任务)时，使用剂管弦来保持收缩耐受。

<a id="why-agent-orchestration"></a>
### 为什么是 Orchestration 探员?

**问题：** 在长期实施期间，环境积累。 如果自动压缩触发了中任务，则会失去执行上下文。 用 80%的上下文创建的交易变得僵化了。

**解决办法：** 将执行工作委托给代理人。 每个代理人：
- 从新上下文开始
- 执行一个任务
- 完成后创建交接
- 返回指挥家

磁盘上仍然有交易。 如果发生收缩，你重新读取并继续。

<a id="setup"></a>
### 设置

1. **创建交接目录：**
   ```bash
   mkdir -p thoughts/handoffs/<session-name>
   ```
使用您连续性分类账中的会话名称 。

2. **学习执行机构的技能：**
   ```bash
   cat .claude/skills/implement_task/SKILL.md
   ```
这定义了代理应如何行事。

<a id="pre-requisite-plan-validation"></a>
### 预先要求：计划审定

在实施之前，确保该计划得到验证。`validate-agent`。验证步骤是分开的，应当建立具有 VALIDATED 地位的交接。

**核证交接的检查：**
```bash
ls thoughts/handoffs/<session>/validation-*.md
```

如果没有验证，则建议首先运行验证：
```
"This plan hasn't been validated yet. Would you like me to spawn validate-agent first?"
```

如果存在审定，但状况是需要审查，请在进行审查前提出问题。

<a id="orchestration-loop"></a>
### 管弦乐圈

对于计划中的每一项任务：

1. **准备剂上下文：**
   - 读取连续性分类账( 当前状态)
   - 阅读计划( 总体上下文)
   - 如果存在，请阅读先前的交割(取自想法/接取/<会话>/)
   - 确定具体任务

2. **日出执行机构：**
   ```
   Task(
     subagent_type="general-purpose",
     model="opus",
     prompt="""
     [Paste contents of .claude/skills/implement_task/SKILL.md here]

     ---

     ## Your Context

     ### Continuity Ledger:
     [Paste ledger content]

     ### Plan:
     [Paste relevant plan section or full plan]

     ### Your Task:
     Task [N] of [Total]: [Task description from plan]

     ### Previous Handoff:
     [Paste previous task's handoff content, or "This is the first task - no previous handoff"]

     ### Handoff Directory:
     thoughts/handoffs/<session-name>/

     ### Handoff Filename:
     task-[NN]-[short-description].md

     ---

     Implement your task and create your handoff.
     """
   )
   ```

3. **加工剂结果：**
   - 读取代理文件
   - 更新分类账复选框 :`[x] Task N`
   - 如果适用， 更新计划复选框
   - 继续下一个任务

4. **关于代理故障/阻断器：**
   - 读取交接( 状态为“ block” )
   - 向用户提供屏蔽器
   - 决定： 重试、 跳过或询问用户

<a id="recovery-after-compaction"></a>
### 压缩后恢复

如果自动压缩发生中节奏：

1. 读取连续性分类账( 由 SessionStart hook 载入)
2. 列出交接目录 :
   ```bash
   ls -la thoughts/handoffs/<session-name>/
   ```
3. 阅读最后的交割 以了解你在哪里
4. 继续从下一个未完成的任务中产出毒剂

<a id="example-orchestration-session"></a>
### 实例管弦会话

```
User: /implement_plan thoughts/shared/plans/PLAN-add-auth.md

Claude: I'll use agent orchestration for this plan (6 tasks).

Setting up handoff directory...
[Creates thoughts/handoffs/add-auth/]

Task 1 of 6: Create user model
[Spawns agent with full context]
[Agent completes, creates task-01-user-model.md]

✅ Task 1 complete. Handoff: thoughts/handoffs/add-auth/task-01-user-model.md

Task 2 of 6: Add authentication middleware
[Spawns agent with previous handoff]
[Agent completes, creates task-02-auth-middleware.md]

✅ Task 2 complete. Handoff: thoughts/handoffs/add-auth/task-02-auth-middleware.md

--- AUTO COMPACT HAPPENS ---
[Context compressed, but handoffs persist]

Claude: [Reads ledger, sees tasks 1-2 done]
[Reads last handoff task-02-auth-middleware.md]

Resuming from Task 3 of 6: Create login endpoint
[Spawns agent]
...
```

<a id="handoff-chain"></a>
### 手提链

每个代理都读取之前的交接 工作完成 创造下一个交接：

```
task-01-user-model.md
    ↓ (read by agent 2)
task-02-auth-middleware.md
    ↓ (read by agent 3)
task-03-login-endpoint.md
    ↓ (read by agent 4)
...
```

连锁连锁连锁连锁连锁店都保留上下文。

<a id="when-to-use-agent-orchestration"></a>
### 何时使用代理管弦乐

| 假设 | 模式 |
|----------|------|
| 1-3 个简单任务 | 直接执行 |
| 4+任务 | 代理指挥 |
| B. 保护的关键背景 | 代理指挥 |
| 快速修复错误 | 直接执行 |
| 主要特点的执行 | 代理指挥 |
| 用户明确要求 | 尊重用户偏好 |

<a id="tips"></a>
### 提示

- **使管弦乐手瘦：** 不要做执行工作自己。 只是管理探员。
- **相信交割：** 代理制作详细的交割 用来做上下文
- **每个任务一名代理人：** 别把多个任务分成一个代理
- **相应处决：** 从相相起。 平行增加了复杂性。
- **最新分类账：** 每次任务结束后，更新连续性分类账复选框。

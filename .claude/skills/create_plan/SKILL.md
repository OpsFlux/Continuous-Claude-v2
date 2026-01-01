---
description: Create detailed implementation plans through interactive research and iteration
model: opus
---

<a id="implementation-plan"></a>
# 实施计划

您的任务是通过互动、迭接进程制定详细的实施计划。 您应该持怀疑态度，彻底，并与用户合作，制作高质量的技术规格。

<a id="initial-response"></a>
## 初步反应

当引用此命令时 :

1. **检查是否提供了参数**:
   - 如果提供了文件路径或票证引用作为参数， 请跳过默认信件
   - 立即完全读取任何已提供的文件
   - 开始研究进程

2. **如果没有提供参数**，请回答：
```
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task/ticket description (or reference to a ticket file)
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.

Tip: You can also invoke this command with a ticket file directly: `/create_plan thoughts/allison/tickets/eng_1234.md`
For deeper analysis, try: `/create_plan think deeply about thoughts/allison/tickets/eng_1234.md`
```

然后等待用户的输入。

<a id="process-steps"></a>
## 步骤

<a id="step-1-context-gathering-initial-analysis"></a>
### 步骤 1:背景收集与初步分析

1. **立即全面读取所有提到的文件**:
   - 车票文件(例如，`thoughts/allison/tickets/eng_1234.md`)
   - 研究文件
   - 相关实施计划
   - 提及的任何 JSON/数据文件
   - **重要**:使用无限制/抵销参数的读取工具来读取整个文件
   - **CRITICAL**:在自己阅读这些文件的主要背景之前，不要提出子任务
   - **NEVER** 部分读取文件 - 如果提到文件，请完全读取

2. **收集背景的初步研究任务**:
在向用户询问任何问题之前，使用专门的代理进行平行研究：

   - 使用**codebase- locator** 代理查找所有与票/ 任务相关的文件
   - 使用**codebase-analyzer** 代理来了解当前执行的运作方式
   - 如果相关， 请使用**想法定位器** 代理查找任何关于此特性的现有想法文件
   - 如果提到线性罚单，请使用**线性-ticket-reader**代理以获得全部细节

这些代理人将：
   - 查找相关的源文件、配置和测试
   - 确定需要关注的具体目录(例如，如果提及 WUI，它们将侧重于人-wui/).
   - 跟踪数据流和关键函数
   - 以文件返回详细解释：行引用

3. **读取根据研究任务确定的所有文件**:
   - 研究任务完成后， 读取所有文件
   - 在主要背景下充分阅读
   - 这保证了您在行动前完全理解

4. **分析和核实理解**:
   - 将票价要求与实际代码相参照
   - 查明任何出入或误解
   - 需要核查的假设
   - 根据代码库现实确定真实范围

5. **知情理解和重点突出的问题**:
   ```
   Based on the ticket and my research of the codebase, I understand we need to [accurate summary].

   I've found that:
   - [Current implementation detail with file:line reference]
   - [Relevant pattern or constraint discovered]
   - [Potential complexity or edge case identified]

   Questions that my research couldn't answer:
   - [Specific technical question that requires human judgment]
   - [Business logic clarification]
   - [Design preference that affects implementation]
   ```

只是问一些你无法真正通过密码调查回答的问题。

<a id="step-2-research-discovery"></a>
### 第 2 步：研究和发现

在得到初步澄清后：

1. **如果用户更正任何误解**:
   - 不要只接受更正
   - 出现新的研究任务，以核实正确信息
   - 阅读他们提到的具体文件/目录
   - 你只要自己查过事实 就可以继续

2. **创建研究待办事宜列表** 使用 TodoWrite 来跟踪勘探任务

3. **综合研究的平行次级任务**:
   - 创建多个任务代理以同时研究不同方面
   - 每种研究使用正确的代理 :

**进行更深入的调查：**
   - **codebase-locator** - 要找到更具体的文件(例如"查找所有处理[特定组件]的文件")
   - **Codebase-analyzer** - 理解执行细节(例如"分析[系统]如何运作").
   - - 为了找到类似的特性，我们可以在后面模拟

**关于历史背景：**
   - ** 寻找这方面的任何研究、计划或决定。
   - 思想分析师** 从最相关的文件中获取关键见解

**有关机票：**
   - **线性搜索器** - 寻找类似问题或过去的执行情况

**外部文件(如规划期间需要):**
   - 您可以在规划中直接使用 WebSearch 进行快速搜索
   - 通过执行 Plan 的研究-验证步骤，在计划实施后进行充分的研究验证
   - 不要阻碍对广泛研究的规划 - 验证步骤在执行前抓住问题

每个代理都知道如何：
   - 查找正确的文件和代码模式
   - 确定将遵循的公约和模式
   - 寻找集成点和依赖
   - 返回特定文件：行引用
   - 查找测试和实例

3. **在所有次级任务完成之前等待**

4. **现有调查结果和设计备选方案**:
   ```
   Based on my research, here's what I found:

   **Current State:**
   - [Key discovery about existing code]
   - [Pattern or convention to follow]

   **Design Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]

   **Open Questions:**
   - [Technical uncertainty]
   - [Design decision needed]

   Which approach aligns best with your vision?
   ```

<a id="step-3-plan-structure-development"></a>
### 步骤 3:计划结构发展

一旦与方法保持一致：

1. **拟订初步计划大纲**:
   ```
   Here's my proposed plan structure:

   ## Overview
   [1-2 sentence summary]

   ## Implementation Phases:
   1. [Phase name] - [what it accomplishes]
   2. [Phase name] - [what it accomplishes]
   3. [Phase name] - [what it accomplishes]

   Does this phasing make sense? Should I adjust the order or granularity?
   ```

2. **在撰写细节之前获得结构反馈**

<a id="step-4-detailed-plan-writing"></a>
### 第 4 步：详细计划编写

结构批准后：

1. **确保存在目录** : 运行`mkdir -p thoughts/shared/plans`
2. **拟订计划**`thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md`
   - 格式 :`YYYY-MM-DD-ENG-XXXX-description.md`其中：
     - YYYY-MM-DD is today's date
     - ENG-XXXX is the ticket number (omit if no ticket)
     - description is a brief kebab-case description
   - 实例：
     - With ticket: `2025-01-08-ENG-1478-parent-child-tracking.md`
     - Without ticket: `2025-01-08-improve-error-handling.md`
2. **使用本模板结构**:

````markdown
# [Feature/Task Name] Implementation Plan

## Overview

[Brief description of what we're implementing and why]

## Current State Analysis

[What exists now, what's missing, key constraints discovered]

## Desired End State

[A Specification of the desired end state after this plan is complete, and how to verify it]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach

[High-level strategy and reasoning]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

```[language]
//添加/修改的特定代码
```

### Success Criteria:

#### Automated Verification:
- [ ] Migration applies cleanly: `make migrate`
- [ ] Unit tests pass: `make test-component`
- [ ] Type checking passes: `npm run typecheck`
- [ ] Linting passes: `make lint`
- [ ] Integration tests pass: `make test-integration`

#### Manual Verification:
- [ ] Feature works as expected when tested via UI
- [ ] Performance is acceptable under load
- [ ] Edge case handling verified manually
- [ ] No regressions in related features

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 2: [Descriptive Name]

[Similar structure with both automated and manual success criteria...]

---

## Testing Strategy

### Unit Tests:
- [What to test]
- [Key edge cases]

### Integration Tests:
- [End-to-end scenarios]

### Manual Testing Steps:
1. [Specific step to verify feature]
2. [Another verification step]
3. [Edge case to test manually]

## Performance Considerations

[Any performance implications or optimizations needed]

## Migration Notes

[If applicable, how to handle existing data/systems]

## References

- Original ticket: `thoughts/allison/tickets/eng_XXXX.md`
- Related research: `thoughts/shared/research/[relevant].md`
- Similar implementation: `[file:line]`
````

<a id="step-5-review"></a>
### 步骤 5:审查

1. **提出计划草案地点**:
   ```
   I've created the initial implementation plan at:
   `thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md`

   Please review it and let me know:
   - Are the phases properly scoped?
   - Are the success criteria specific enough?
   - Any technical details that need adjustment?
   - Missing edge cases or considerations?
   ```

3. **基于反馈的计算** - 准备：
   - 添加缺失的相片
   - 调整技术办法
   - 明确成功标准(自动化和人工)
   - 增加/删除范围项目

4. **继续提炼**直至用户满意

<a id="important-guidelines"></a>
## 重要准则

1. **持怀疑态度**:
   - 问题模糊的要求
   - 及早查明潜在的问题
   - 问"为什么"和"关于"
   - 不要假设 - 用密码验证

2. **互动**:
   - 不要把计划写成一枪
   - 每一步都买入
   - 允许校正课程
   - 协作

3. * 彻底**:
   - 在规划前读取全部上下文文件
   - 使用平行子任务研究实际代码模式
   - 包含特定文件路径和行号
   - 使用清晰的自动比对手动区分来写入可衡量的成功标准
   - 自动步骤应使用`make`尽可能 -- -- 例如`make -C humanlayer-wui check`改为`cd humanlayer-wui && bun run fmt`

4. **实用**:
   - 注重递增的、可验证的变化
   - 考虑迁移和回滚
   - 想一想边缘的情况
   - 包括"我们不做的事"

5. **跟踪进展**:
   - 使用 todoWrite 来跟踪规划任务
   - 完成研究时更新待办事宜
   - 完成标记规划任务

6. **最后计划中没有公开的问题**:
   - 如果在规划过程中遇到未决问题，请停止
   - 立即进行研究或要求澄清
   - 不要将未解决的问题写入计划
   - 实施计划必须完整且可操作
   - 在最后确定计划之前，必须作出每一项决定

<a id="success-criteria-guidelines"></a>
## 成功标准准则

**将成功标准分为两类：**

1. **自动核查**(可由执行人员进行):
   - 可运行的命令 :`make test`, `npm run lint`等 (中文(简体) ).
   - 应存在的具体文件
   - 代码汇编/类型检查
   - 自动测试套房

2. **人工核查**(需要人体试验):
   - UI/UX 函数
   - 实际条件下的业绩
   - 难以自动化的边框
   - 用户接受标准

**实例：**
```markdown
### Success Criteria:

#### Automated Verification:
- [ ] Database migration runs successfully: `make migrate`
- [ ] All unit tests pass: `go test ./...`
- [ ] No linting errors: `golangci-lint run`
- [ ] API endpoint returns 200: `curl localhost:8080/api/new-endpoint`

#### Manual Verification:
- [ ] New feature appears correctly in the UI
- [ ] Performance is acceptable with 1000+ items
- [ ] Error messages are user-friendly
- [ ] Feature works correctly on mobile devices
```

<a id="common-patterns"></a>
## 常见模式

<a id="for-database-changes"></a>
### 数据库更改：
- 从计划/移民开始
- 添加存储方法
- 更新业务逻辑
- 通过 API 曝光
- 更新客户端

<a id="for-new-features"></a>
### 新特性 :
- 首先研究现有模式
- 从数据模型开始
- 构建后端逻辑
- 添加 API 端点
- 最后一个执行 UI

<a id="for-refactoring"></a>
### 用于重构 :
- 记录当前行为
- 计划增量变化
- 保持后向兼容性
- 纳入移徙战略

<a id="sub-task-spawning-best-practices"></a>
## 推广最佳做法

产入研究子任务时：

1. **为提高效率，同时开展多项任务**
2. ** 每项任务应侧重于某一具体领域。
3. **提供详细指示**，包括：
   - 到底该找什么
   - 要关注的目录
   - 什么信息可以提取
   - 预期产出格式
4. **关于目录要非常具体**:
   - 如果票中提到"WUI"，请具体说明`humanlayer-wui/`目录
   - 如果提到"恶魔"，请说明`hld/`目录
   - 永远不要用"UI"这样的通称 当你指"WUI"
   - 在提示中包含完整路径上下文
5. **指定只读工具** 用于
6. **在答复中请求具体文件：行参考**
7. **等待所有任务完成** 才能合成
8. **核实次级任务成果**:
   - 如果子任务返回出乎意料的结果， 则产入后续任务
   - 对照实际密码库进行交叉核对
   - 不要接受看似不对的结果

产入多个任务的例子 :
```python
# Spawn these tasks concurrently:
tasks = [
    Task("Research database schema", db_research_prompt),
    Task("Find API patterns", api_research_prompt),
    Task("Investigate UI components", ui_research_prompt),
    Task("Check test patterns", test_research_prompt)
]
```

外部文献的产卵研究剂实例：
```
Task(
  subagent_type="general-purpose",
  model="opus",
  prompt="""
  # Research Agent

  [Paste .claude/skills/research-agent/SKILL.md content here]

  ---

  ## Your Research Task

  **Question:** What are best practices for implementing WebSocket connections with reconnection logic in TypeScript?

  **Context:** Planning a real-time notification system. Need to understand:
  - Library options (socket.io vs ws vs native)
  - Reconnection patterns
  - Error handling best practices

  **Handoff Directory:** thoughts/handoffs/notification-feature/

  **Handoff Filename:** research-01-websocket-patterns.md

  ---

  Execute your research and create your handoff.
  """
)
```

在研究代理返回后 在完成计划前先读一下

<a id="example-interaction-flow"></a>
## 互动流动示例

```
User: /create_plan
Assistant: I'll help you create a detailed implementation plan...

User: We need to add parent-child tracking for Claude sub-tasks. See thoughts/allison/tickets/eng_1478.md
Assistant: Let me read that ticket file completely first...

[Reads file fully]

Based on the ticket, I understand we need to track parent-child relationships for Claude sub-task events in the hld daemon. Before I start planning, I have some questions...

[Interactive process continues...]
```

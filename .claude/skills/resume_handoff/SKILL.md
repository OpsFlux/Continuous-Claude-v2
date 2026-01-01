---
description: Resume work from handoff document with context analysis and validation
---

<a id="resume-work-from-a-handoff-document"></a>
# 从交接文件中恢复工作

您的任务是通过互动进程从交接文件中恢复工作。 这些交割包含关键的背景、学习以及需要理解和继续的前几届工作会议的下一步。

<a id="initial-response"></a>
## 初步反应

当引用此命令时 :

1. **如果提供了发放文件的路径**:
   - 如果提供了作为参数的交接文档路径， 请跳过默认消息
   - 立即充分阅读交接文件
   - 立即阅读其链接到以下系统的任何研究或计划文件：`thoughts/shared/plans` or `thoughts/shared/research`。不要使用子代理读取这些关键文件。
   - 开始分析过程，从交接文件中取出相关上下文，阅读该文件提及的更多文件
   - 然后向用户提出行动方针，确认或要求澄清方向。

2. **如果提供票号(如 ENG-X)**:
   - 找到最新的售票文件。 车票将在`thoughts/shared/handoffs/ENG-XXXX`地点`ENG-XXXX`是车票号码。 例如，用于`ENG-2124`交易将会在`thoughts/shared/handoffs/ENG-2124/`。 **列出此目录的内容。**
   - 目录中可能存在零， 1 或多文件。
   - **如果目录中有零文件，或者目录不存在**:告诉用户："对不起，我似乎找不到交接文件。 你能给我一条路吗?"
   - **如果目录中只有一个文件**:继续移交
   - **如果目录中有多个文件**:使用文件名称中指定的日期和时间(将使用格式)`YYYY-MM-DD_HH-MM-SS`以 24 小时为格式)，继续使用  最近 交接文档。
   - 立即充分阅读交接文件
   - 立即阅读其链接到以下系统的任何研究或计划文件：`thoughts/shared/plans` or `thoughts/shared/research`; 不要使用子代理读取这些关键文件。
   - 开始分析过程，从交接文件中取出相关上下文，阅读该文件提及的更多文件
   - 然后向用户提出行动方针，确认或要求澄清方向。

3. **如果没有提供参数**，请回答：
```
I'll help you resume work from a handoff document. Let me find the available handoffs.

Which handoff would you like to resume from?

Tip: You can invoke this command directly with a handoff path: `/resume_handoff `thoughts/shared/handoffs/ENG-XXXX/YYYY-MM-DD_HH-MM-SS_ENG-XXXX_description.md`

or using a ticket number to resume from the most recent handoff for that ticket: `/resume_handoff ENG-XXXX`
```

然后等待用户的输入。

<a id="process-steps"></a>
## 步骤

<a id="step-1-read-and-analyze-handoff"></a>
### 第 1 步：读取和分析取出

1. **完全读取移交文件**:
   - 使用无限制/抵销参数的读取工具
   - 提取所有区域 :
     - Task(s) and their statuses
     - Recent changes
     - Learnings
     - Artifacts
     - Action items and next steps
     - Other notes

2. **重点研究任务**:
根据交接内容，产生并行的研究任务，以验证当前状态：

   ```
   Task 1 - Gather artifact context:
   Read all artifacts mentioned in the handoff.
   1. Read feature documents listed in "Artifacts"
   2. Read implementation plans referenced
   3. Read any research documents mentioned
   4. Extract key requirements and decisions
   Use tools: Read
   Return: Summary of artifact contents and key decisions
   ```

3. **在所有次级任务完成之前等待**

4. **已查明的关键文件**:
   - 从“ 学习” 部分完全读取文件
   - 从“ 最近更改” 读取文件以理解修改
   - 读取在研究中发现的任何新相关文件

<a id="step-2-synthesize-and-present-analysis"></a>
### 第 2 步：合成和现成分析

1. **现有综合分析**:
   ```
   I've analyzed the handoff from [date] by [researcher]. Here's the current situation:

   **Original Tasks:**
   - [Task 1]: [Status from handoff] → [Current verification]
   - [Task 2]: [Status from handoff] → [Current verification]

   **Key Learnings Validated:**
   - [Learning with file:line reference] - [Still valid/Changed]
   - [Pattern discovered] - [Still applicable/Modified]

   **Recent Changes Status:**
   - [Change 1] - [Verified present/Missing/Modified]
   - [Change 2] - [Verified present/Missing/Modified]

   **Artifacts Reviewed:**
   - [Document 1]: [Key takeaway]
   - [Document 2]: [Key takeaway]

   **Recommended Next Actions:**
   Based on the handoff's action items and current state:
   1. [Most logical next step based on handoff]
   2. [Second priority action]
   3. [Additional tasks discovered]

   **Potential Issues Identified:**
   - [Any conflicts or regressions found]
   - [Missing dependencies or broken code]

   Shall I proceed with [recommended action 1], or would you like to adjust the approach?
   ```

2. **在进行程序前获得确认**

<a id="step-3-create-action-plan"></a>
### 步骤 3:制定行动计划

1. **使用 todoWrite 创建任务列表** :
   - 将动作项目从移交转换为待办事宜
   - 添加分析中发现的任何新任务
   - 根据依赖和交接指导确定优先次序

2. **提出计划**:
   ```
   I've created a task list based on the handoff and current analysis:

   [Show todo list]

   Ready to begin with the first task: [task description]?
   ```

<a id="step-4-begin-implementation"></a>
### 步骤 4:开始执行

1. **开始执行第一项已核准的任务**
2. **在整个执行过程中从交割中吸取的参考**
3. **交割中记录的典型做法**
4. **任务完成后的最新进展**

<a id="guidelines"></a>
## 准则

1. **彻底分析**:
   - 先读整个交接文档
   - 校验所有提及更改仍然存在
   - 检查任何回归或冲突
   - 读取所有引用的文物

2. **互动**:
   - 开始工作前提出调查结果
   - 买入方法
   - 允许校正课程
   - 基于当前状态对交接状态的适应

3. **自由手腕智慧**:
   - 特别注意"学习"部分
   - 应用已记录的模式和方法
   - 避免重复提及的错误
   - 利用已发现的解决方案

4. **追踪连续性**:
   - 使用 todoWrite 来保持任务连续性
   - 引用交接文件
   - 记录任何偏离原计划的情况
   - 完成后考虑创建新的交接

5. **代理** 之前：
   - 永远不要假设交接状态符合当前状态
   - 验证所有文件引用仍然存在
   - 检查交接后是否有更改
   - 确认模式仍然有效

<a id="common-scenarios"></a>
## 常见情况

<a id="scenario-1-clean-continuation"></a>
### 设想 1:清洁延续
- 交割后的所有更改都存在
- 无冲突或倒退
- 清除行动项目的下一步
- 继续采取建议的行动

<a id="scenario-2-diverged-codebase"></a>
### 设想 2:多种编码基础
- 缺少或修改了一些更改
- 交接后新增相关代码
- 需要调和分歧
- 基于当前状况的适应计划

<a id="scenario-3-incomplete-handoff-work"></a>
### 设想 3:不完全的交接工作
- 交接中标为“ 进行中” 的任务
- 需要先完成未完成的工作
- 可能需要重新理解部分执行
- 注重在新工作之前完成

<a id="scenario-4-stale-handoff"></a>
### 设想 4:Stale Handoff
- 已经过了很长时间
- 进行了重大重构
- 原有办法可能不再适用
- 需要重新评估战略

<a id="example-interaction-flow"></a>
## 互动流动示例

```
User: /resume_handoff specification/feature/handoffs/handoff-0.md
Assistant: Let me read and analyze that handoff document...

[Reads handoff completely]
[Spawns research tasks]
[Waits for completion]
[Reads identified files]

I've analyzed the handoff from [date]. Here's the current situation...

[Presents analysis]

Shall I proceed with implementing the webhook validation fix, or would you like to adjust the approach?

User: Yes, proceed with the webhook validation
Assistant: [Creates todo list and begins implementation]
```

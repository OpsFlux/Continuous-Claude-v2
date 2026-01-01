<a id="agent-orchestration-rules"></a>
# 代理管弦乐规则

当用户要求执行某事时，使用执行代理来保存主上下文。

<a id="the-pattern"></a>
## 图案

**错误----烧伤背景：**
```
Main: Read files → Understand → Make edits → Report
      (2000+ tokens consumed in main context)
```

**权利----保留上下文：**
```
Main: Spawn agent("implement X per plan")
      ↓
Agent: Reads files → Understands → Edits → Tests
      ↓
Main: Gets summary (~200 tokens)
```

<a id="when-to-use-agents"></a>
## 何时使用代理

| 任务类型 | 用探员? | 原因 |
|-----------|------------|--------|
| 多文件执行 | 对 | 代理处理内部复杂 |
| 计划阶段之后 | 对 | 代理读取计划，工具 |
| 有测试的新功能 | 对 | 代理可以运行测试 |
| 单行固定 | No | 快点直接动手 |
| 快速配置变化 | No | 超头不值得 |

<a id="key-insight"></a>
## 密钥透视

代理读了他们自己的背景 不要在主要聊天中读取文件，只是为了了解什么是传递给代理 - 给他们任务，让他们自己想清楚。

<a id="example-prompt"></a>
## 示例提示

```
Implement Phase 4: Outcome Marking Hook from the Artifact Index plan.

**Plan location:** thoughts/shared/plans/2025-12-24-artifact-index.md (search for "Phase 4")

**What to create:**
1. TypeScript hook
2. Shell wrapper
3. Python script
4. Register in settings.json

When done, provide a summary of files created and any issues.
```

<a id="trigger-words"></a>
## 触发词

当用户说这些时， 考虑使用代理 :
- "执行","建设","创造特色"
- "按照计划" "做第十阶段"
- "使用执行代理人"

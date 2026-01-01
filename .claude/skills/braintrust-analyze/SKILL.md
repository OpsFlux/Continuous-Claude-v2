---
name: braintrust-analyze
description: Analyze Claude Code sessions via Braintrust
---

<a id="braintrust-analysis"></a>
# 大 Braintrust 任分析

利用 BrainTrust 追踪数据分析你的 Claude 代码课程的规律、问题和见解。

<a id="when-to-use"></a>
## 何时使用

- 完成复杂任务后( 回顾)
- 当调试为何某事失败时
- 每周审查生产率模式
- 寻找创造新技能的机会
- 理解象征性使用趋势

<a id="commands"></a>
## 图标

从项目目录中运行 :

```bash
# Analyze last session - summary with tool/agent/skill breakdown
uv run python -m runtime.harness scripts/braintrust_analyze.py --last-session

# List recent sessions
uv run python -m runtime.harness scripts/braintrust_analyze.py --sessions 5

# Agent usage statistics (last 7 days)
uv run python -m runtime.harness scripts/braintrust_analyze.py --agent-stats

# Skill usage statistics (last 7 days)
uv run python -m runtime.harness scripts/braintrust_analyze.py --skill-stats

# Detect loops - find repeated tool patterns (>5 same tool calls)
uv run python -m runtime.harness scripts/braintrust_analyze.py --detect-loops

# Replay specific session - show full sequence of actions
uv run python -m runtime.harness scripts/braintrust_analyze.py --replay <session-id>

# Weekly summary - daily activity breakdown
uv run python -m runtime.harness scripts/braintrust_analyze.py --weekly-summary

# Token trends - usage over time
uv run python -m runtime.harness scripts/braintrust_analyze.py --token-trends
```

<a id="options"></a>
## 选项

- `--project NAME`- Braintrust 项目名称(默认：代理)

<a id="what-youll-learn"></a>
## 你会学到什么

<a id="session-analysis"></a>
### 会话分析
- 工具使用细目
- 代理产卵(计划剂、调试剂等)
- 技能活化(/commit, /research 页：1
- 消费估计数

<a id="loop-detection"></a>
### 循环检测
查找多次调用同一工具的会话，这可能表示：
- 困入搜索循环
- 效率低下的做法
- 改进工具的机会

<a id="usage-patterns"></a>
### 用法模式
- 你最常用的探员
- 哪些技能被激活
- 每日/每周活动趋势

<a id="examples"></a>
## 实例

<a id="quick-retrospective"></a>
### 快速回顾
```bash
# What happened in my last session?
uv run python -m runtime.harness scripts/braintrust_analyze.py --last-session
```

输出 :
```
## Session Analysis
**ID:** `92940b91...`
**Started:** 2025-12-24T01:31:05Z
**Spans:** 14

### Tool Usage
- Read: 4
- Bash: 2
- Edit: 2
...
```

<a id="find-loops"></a>
### 查找循环
```bash
uv run python -m runtime.harness scripts/braintrust_analyze.py --detect-loops
```

<a id="weekly-review"></a>
### 每周评论
```bash
uv run python -m runtime.harness scripts/braintrust_analyze.py --weekly-summary
```

<a id="requirements"></a>
## 所需资源

- (巴西语)/.claude/.env 或项目。env
- 能够追踪到大脑托拉斯(通过大脑托拉斯-Claude-plugin)

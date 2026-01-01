---
description: Search past reasoning for relevant decisions and approaches
---

<a id="recall-past-work"></a>
# 回顾过去的工作

通过前几次会议寻找相关决定、行之有效的办法和失败的办法。 查询两个来源：

1. **艺术指数** -- -- 死后处理、计划、分类账(可行/失败)
2. **Reasoning 文件** - 构建尝试，测试失败，承诺上下文

<a id="when-to-use"></a>
## 何时使用

- 开始类似于以往届会的工作
- "我们上次对 X 做了什么?"
- 寻找以前有效的模式
- 调查为什么有事情发生
- 调试之前遇到的问题

<a id="usage"></a>
## 使用量

<a id="primary-artifact-index-rich-context"></a>
### 初级：人工活性指数(丰富背景)

```bash
uv run python scripts/artifact_query.py "<query>" [--outcome SUCCEEDED|FAILED] [--limit N]
```

这种以验尸(什么有效，什么失败，什么关键决定)进行搜索。

<a id="secondary-reasoning-files-build-attempts"></a>
### 二级：理由文件(建设尝试)

```bash
bash .claude/scripts/search-reasoning.sh "<query>"
```

这个搜索`.git/claude/commits/*/reasoning.md`建造失败和修复。

<a id="examples"></a>
## 实例

```bash
# Search for authentication-related work
uv run python scripts/artifact_query.py "authentication OAuth JWT"

# Find only successful approaches
uv run python scripts/artifact_query.py "implement agent" --outcome SUCCEEDED

# Find what failed (to avoid repeating mistakes)
uv run python scripts/artifact_query.py "hook implementation" --outcome FAILED

# Search build/test reasoning
bash .claude/scripts/search-reasoning.sh "TypeError"
```

<a id="what-gets-searched"></a>
## 搜索内容

**Artifact Index**(手头、计划、分类账):
- 任务摘要和现况
- **有效** - 成功办法
- *什么失败* - 死亡结局和原因
- **关键决定** - 附有理由的选择
- 目标及分类账的限制

**重解析文件** (% 1)`.git/claude/`):
- 构建尝试和出错输出失败
- 失败后成功构建
- 提交上下文和分支信息

<a id="interpreting-results"></a>
## 解释结果

**来自人工活性指数：**
- `✓`= 特别会议的结果(形式如下)
- `✗`=结果不全(为避免)
- `?`= 联合国大学成果(尚未标明)
- 死后部分展现出精炼出的知识

**理由：**
- `build_fail`=没有用的方法
- `build_pass`= 最终成功的东西
- 成功前多次失败 = 非部落问题

<a id="process"></a>
## 进程

1. **运行艺术 索引查询第一** - 内容更丰富，死后
2. **审查相关的交割** -- -- 检查哪些款已奏效/失效
3. **如果需要，搜索推理** - 具体构建错误
4. **Apply learning** - 遵循成功模式，避免失败模式

<a id="no-results"></a>
## 没有结果?

**制品索引（Artifact Index）为空：**
- 运行`uv run python scripts/artifact_index.py --all`以索引当前交割
- 制作配有尸检部的交割，供今后召回

**正在重解文件为空 :**
- 使用`/commit`在构建后获取推理
- 检查是否`.git/claude/`目录已存在

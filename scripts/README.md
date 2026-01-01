<a id="scripts-cli-based-mcp-workflows"></a>
# 脚本 - 基于 CLI 的 MCP 工作流量

**目标：** Agent-agnostic，可再用 Python 脚本为 MCP 工具管弦乐配有 CLI 参数。

---

<a id="what-are-scripts"></a>
## 脚本是什么?

**脚本**是基于 CLI 的 Python 工作流程，该工作流程：
- 通过命令行参数( argparse) 接受参数
- 管弦乐 MCP 工具调用
- 返回结构化结果
- 与任何 AI 代理(不仅仅是 Claude Code)合作。

**NOT 与：**
- **Skills**=Claude Code 的本地格式(.claude/chills/与 SKILL.md)

---

<a id="example-scripts"></a>
## 示例脚本

**此目录包含 MCP 工作流程脚本 :**

<a id="firecrawl_scrapepy"></a>
### firecrawl scrape.py (法语).
- 网页刮取模式
- CLI: 爱丽丝。`--url`(必须)
- 要求：`FIRECRAWL_API_KEY`

<a id="multi_tool_pipelinepy"></a>
### 多工具  管道。 py
- 多工具链式(git 分析)
- CLI: 爱丽丝。`--repo-path`(默认："."),.`--max-commits`(默认：10)
- 没有 API 键的工作( 使用 git 服务器)

<a id="other-scripts"></a>
### 其他脚本
见`ls scripts/`用于所有可用工作流程(复杂度、千兆赫、一等)

---

<a id="usage"></a>
## 使用量

**执行带有 CLI 参数的脚本：**

```bash
# Web scraping (requires FIRECRAWL_API_KEY)
uv run python -m runtime.harness scripts/firecrawl_scrape.py \
    --url "https://example.com"

# Multi-tool pipeline (works without API keys)
uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
    --repo-path "." \
    --max-commits 5
```

**关键：** 通过 CLI args 参数 - 自由地编辑脚本以修正错误或改进逻辑

---

<a id="scripts-vs-skills"></a>
## 脚本对技能

<a id="scripts-this-directory"></a>
### 脚本( 此目录)

**什么：**基于 CLI 的 Python 工作流程
**地点：**`./scripts/`**格式：** 有正弦的 Python
**发现：** 手册(ls, cat)
**用于：** 任何人工智能代理人
**效率：** 以 CLI 参数表示的减少值为 99.6%

<a id="skills-claude-code-native"></a>
### 技能(原生语言)

**什么：** SKILL.md 目录
**地点：**`.claude/skills/`**格式：** YAML + 减值
**发现：** 自动(Claude 代码扫描)
**只用于：** Claude Code
**效率：** 土著逐步披露

**关系：** 执行所需的技能参考脚本

---

<a id="creating-custom-scripts"></a>
## 创建自定义脚本

遵循模板模式 :

```python
"""
SCRIPT: Your Script Name
DESCRIPTION: What it does
CLI ARGUMENTS:
    --param    Description
USAGE:
    uv run python -m runtime.harness scripts/your_script.py --param "value"
"""

import argparse
import asyncio
import sys

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--param", required=True)
    args_to_parse = [arg for arg in sys.argv[1:] if not arg.endswith(".py")]
    return parser.parse_args(args_to_parse)

async def main():
    args = parse_args()
    # Your MCP orchestration logic
    return result

asyncio.run(main())
```

---

<a id="documentation"></a>
## 文档

- **SCRIPTS.md** - 完整的框架文件
- **此读取器** - 快速启动
- **../.claude/skills/** - 参考这些脚本的 Claude Code 技能
- **../docs/** - 完整的项目文件

---

**记住：**脚本=代理不可知 CLI 工作流程。 技能 = Claude Code 本地格式。

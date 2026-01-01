<a id="skills-framework-documentation"></a>
# 技能框架文档

**Anthropic 的愿景：** 代理构建了一个随时间演变的可再利用能力工具箱。

> **优化代码：** 本框架的目的是：[Claude Code](https://docs.claude.com/en/docs/claude-code)(v2.0.20+) (中文(简体) ). Claude Code 的文件系统发现和基于 CLI 的执行使得 99.6%的令牌减少成为可能。 其他 AI 代理可以使用核心运行时间，但可能不能达到同样的效率。

<a id="philosophy"></a>
## 哲学

别走，别走 每次从头写脚本
别走，别走 编辑技能文件以更改参数( 使用 CLI args 代替)
**DO:** 用 CLI 参数发现和执行技能
**DO:** 编辑修复错误或改进逻辑的技能文件

**备选案文：**
```
Discover (ls) → Read (cat) → Execute with CLI args (--query, --num-urls, etc.)
```

<a id="agent-operational-intelligence"></a>
## 行动情报代理

**对于简单的任务(1 个工具呼叫):**
- 使用直接访问( 直接调用 MCP 工具)

**对于复杂的工作流程(>2 个工具、逻辑、处理):**
1. `ls ./scripts/`- 发现可用的脚本
2. `cat ./scripts/{script}.py`- 阅读脚本文档和 CLI 参数
3. 用 CLI 参数执行 :
   ```bash
   uv run python -m runtime.harness scripts/firecrawl_scrape.py \
       --url "https://example.com"
   ```

**新工作流程：**
1. 探索`./servers/`用于发现工具
2. 使用 CLI 模板写入新技能
3. 保存到`./skills/`未来再利用
4. docstring 中的文档 CLI 参数

<a id="efficiency-benefits"></a>
## 效率福利

**节省(用于参数变化):**
- QQ 从零开始写入： 装入计程器 + 写入代码 = ~ 5,000 个令牌
- QQ 编辑技能以改变参数：读取技能+编辑+写出=~800 个令牌
- QQ 以不同的参数执行 CLI : 读取技能 + 命令 = ~ 110 个令牌
- **减少：98%(国家综合倡议办法)**

**时间节省(参数变化):**
- 从零开始写：~2 分
- 编辑修改参数的技能：~30 秒
- 使用不同参数的 CLI 执行：~ 5 秒
- **减少：96%(CLI 办法)**

**说明：** 自由编辑技能来修正错误，改进逻辑，或添加特性。 效率的好处在于避免为参数变化编辑文件。

<a id="skill-template-cli-based"></a>
## 技能模板( 基于 CLI )

```python
"""
SKILL: {Name}

DESCRIPTION: {What it does}

WHEN TO USE: {Use cases}

CLI ARGUMENTS:
    --param1    Description (required/optional, default: value)
    --param2    Description (type: int, default: 123)

USAGE:
    cd /home/khitomer/Projects/mcp-code-execution
    uv run python -m runtime.harness skills/{skill}.py \
        --param1 "value" \
        --param2 456
"""

import argparse
import asyncio
import sys

def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="{Skill description}")
    parser.add_argument("--param1", required=True, help="Description")
    parser.add_argument("--param2", type=int, default=123, help="Description")

    # Filter out script path from sys.argv (harness adds it)
    args_to_parse = [arg for arg in sys.argv[1:] if not arg.endswith(".py")]
    return parser.parse_args(args_to_parse)

async def main():
    """Main skill workflow."""
    args = parse_args()

    print(f"Executing with param1={args.param1}, param2={args.param2}")

    # Use args.param1, args.param2, etc.
    # ...implementation...

    return result

if __name__ == "__main__":
    asyncio.run(main())
```

<a id="current-scripts-library"></a>
## 当前脚本库

| 类别 | 脚本 | CLI 参数 |
|----------|--------|---------------|
| **网页** | firecrawl scrape.py (法语). | `--url`(必须) |
| **管道** | 多工具  管道。 py | `--repo-path`(默认："."),.`--max-commits`(默认：10) |
| **寻找** | 复杂度  search.py | `--query`(必须) |
| 页：1 | nia docs.py 数据 | `--package`, `--query` |

<a id="creating-new-skills"></a>
## 创造新技能

**何时创建：**
- 未覆盖的小说工作流程
- 找到更好的图案
- 具体使用需要

**如何创建：**
1. 探索`./servers/`寻找所需的工具
2. 遵循上面的 CLI 模板写入技能
3. 以 argparse 添加 CLI 参数解析
4. 说明文件(定义、何时使用、CLI 条款、使用)
5. 彻底测试
6. 保存到`./skills/`

**最佳做法：**
- 对所有可配置值使用参数
- 在 docstring 中记录所有 CLI 参数，包括类型和默认
- 包含带具体示例的 USAGE 部分
- 过滤 sys.argv 以删除脚本路径 :`[arg for arg in sys.argv[1:] if not arg.endswith(".py")]`
- 保持通用/可重复使用的工作流程逻辑
- 包含错误处理和进度打印
- 返回结构化结果

<a id="skills-vs-writing-scripts"></a>
## 技能对写脚本

**技能：**
- 重复使用的工作流程模板
- 参数变化的 QQ CLI 参数( 不需要文件编辑)
- QQ 为错误修正和改进编辑方便
- * 预先测试和记录
- 每用 110 个令牌(使用 CLI 参数时)
- 执行时间为 5 秒
- 代理刚读和执行

**书面文稿(备选案文):**
- QQ 每次自定义代码
- · 需要计划探索
- +++ 更多纪念物(~2,000)
- +++ 更多时间(~2 分钟)
- 代理必须从零开始写
- 适合：小说工作流程，学习，原型

<a id="example-usage"></a>
## 示例使用

```bash
# Web scraping (requires FIRECRAWL_API_KEY)
uv run python -m runtime.harness scripts/firecrawl_scrape.py \
    --url "https://example.com"

# Multi-tool pipeline (uses git server - works without API keys)
uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
    --repo-path "." \
    --max-commits 5
```

<a id="key-principles"></a>
## 关键原则

1. **Parameter Immutibility** - 通过 CLI 参数，而不是通过编辑文件更改参数
2. **逻辑变异性** - 自由编辑技能来修复错误，改进逻辑，或添加特性
3. **CLI 参数** - 通过命令行参数的所有配置
4. **可续用性** - 写出一次，多次使用不同的参数
5. **文件** - 每种技能都有 USAGE 部分，并附有实例
6. **Type Security** - 参数提供了验证和帮助文本
7. **效果** - 通过 CLI 对文件编辑的参数变化减少 98% 。

<a id="help-text"></a>
## 帮助文本

每个脚本都支持`--help`:

```bash
python scripts/firecrawl_scrape.py --help

# Output:
usage: firecrawl_scrape.py [-h] --url URL

Firecrawl web scraping script

optional arguments:
  -h, --help  show this help message and exit
  --url URL   URL to scrape (required)
```

---

**记得：** 通过 CLI args 传递参数，而不是编辑文件。 自由编辑技能来修正错误或改进逻辑!

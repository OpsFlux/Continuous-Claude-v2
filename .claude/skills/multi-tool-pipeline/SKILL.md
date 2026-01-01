---
name: multi-tool-pipeline
description: Template for chaining multiple MCP tools in a single script
allowed-tools: [Bash, Read]
---

<a id="multi-tool-pipeline-template"></a>
# 多工具管道模板

引用执行显示如何将多个 MCP 工具在脚本中链条。

<a id="when-to-use"></a>
## 何时使用

- 在创建新的 MCP 管道脚本时作为**template**
- 理解工具链的图案
- 当技能开发者需要建立新的管道时

<a id="the-pattern"></a>
## 图案

```python
async def main():
    from runtime.mcp_client import call_mcp_tool

    # Step 1: First tool
    result1 = await call_mcp_tool("server1__tool1", {"param": "value"})

    # Step 2: Use result in next tool
    result2 = await call_mcp_tool("server2__tool2", {"input": result1})

    # Step 3: Combine/process
    return {"combined": result1, "processed": result2}
```

<a id="example-implementation"></a>
## 实例

见参考脚本：

```bash
cat $CLAUDE_PROJECT_DIR/scripts/multi_tool_pipeline.py
```

运行它：

```bash
uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
    --repo-path "." \
    --max-commits 5
```

<a id="key-elements"></a>
## 关键要素

1. **CLI 参数** - 参数使用参数参数
2. **连续呼叫** - 在下一个工具之前等待每个工具
3. **不当处理** -- -- 试验/管道周围除外
4. **产出** - 可见度打印状态
5. **回归** - 回归综合结果

<a id="creating-your-own-pipeline"></a>
## 创建您自己的管道

1. 复制`scripts/multi_tool_pipeline.py`作为起点
2. 用您的 MCP 服务器/工具替换工具调用
3. 为您的使用调整 CLI 参数
4. 使用`/skill-developer`把它包起来

<a id="mcp-tool-naming"></a>
## MCP 工具命名

工具名称`serverName__toolName`(双下划线):

```python
await call_mcp_tool("git__git_status", {...})
await call_mcp_tool("firecrawl__firecrawl_scrape", {...})
await call_mcp_tool("perplexity__perplexity_ask", {...})
```

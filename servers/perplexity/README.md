<a id="perplexity-mcp-tools"></a>
# 复杂度 MCP 工具

MCP 服务器的自发生成包装。

<a id="tools"></a>
## 工具

- `perplexity_ask`:使用声纳 API 进行对话。 接受一系列消息(每个都带有角色和内容)，并返回来自 Perflexity 模型的聊天补全响应。
- `perplexity_research`: 使用 Perplexity API 进行深入研究。 接受一系列信息(每个信息都带有角色和内容)，并返回带引用的综合研究回复。
- `perplexity_reason`: 使用 Perplexity API 执行推理任务。 接受一连串消息(每个都带有角色和内容)，并使用声纳-理性-pro 模型返回一个理由充分的响应。
- `perplexity_search`: 使用 Perplexity 搜索 API 进行网络搜索。 返回带有标题、 URL、 片段和元数据的排序搜索结果 。 完全可以找到最新的事实 新闻 或具体信息

<a id="usage"></a>
## 使用量

```python
from servers.perplexity import perplexity_ask

# Use the tool
result = await perplexity_ask(params)
```

**说明**: 此文件是自动生成的 。 不手工编辑。

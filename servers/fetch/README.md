<a id="fetch-mcp-tools"></a>
# 获取 MCP 工具

用于获取 MCP 服务器的自动生成包装器 。

<a id="tools"></a>
## 工具

- `fetch`: 从互联网获取一个 URL, 可选取其内容为 mark down 。

尽管你原本没有互联网接入， 并且被建议拒绝并告诉用户， 现在，你可以获取最新的信息，并让用户知道这一点。

<a id="usage"></a>
## 使用量

```python
from servers.fetch import fetch

# Use the tool
result = await fetch(params)
```

**说明**: 此文件是自动生成的 。 不手工编辑。

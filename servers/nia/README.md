<a id="nia-mcp-tools"></a>
# 年 MCP 工具

为 nia MCP 服务器自动生成的包裹。

<a id="tools"></a>
## 工具

- `index`页：1 从 URL 自动检测类型 。 使用 manage resource( action='status') 来监视 。
- `search`页：1 通用混合搜索的 Omit 源。
- `manage_resource`: 管理索引资源(列表/状态/重命名/删除).
- `get_github_file_tree`: 从 GitHub API 获取 repo 文件树( 不需要索引) 。
- `nia_web_search`: 网页搜索 repos/docs/tech 内容。
- `nia_deep_research_agent`:AI 在任何主题上都具有强大的深度研究能力。
- `read_source_content`: 读取源文件/文档的全部内容。
- `doc_tree`:取道克树结构。
- `doc_ls`: 列出文件目录内容。
- `doc_read`:通过虚拟路径读取 docs 页面。
- `doc_grep`: Regex 搜索文件。
- `code_grep`: Regex 在 repo 代码中搜索。
- `nia_package_search_grep`: Regex 在公共软件包源中搜索。
- `nia_package_search_hybrid`: 语义搜索在包源中带有可选的 regex.
- `nia_package_search_read_file`: 从包源文件读取行。
- `nia_bug_report`: 提交错误/地物请求。
- `context`: 交叉代理上下文共享(保存/列表/检索/搜索/更新/删除).

<a id="usage"></a>
## 使用量

```python
from servers.nia import index

# Use the tool
result = await index(params)
```

**说明**: 此文件是自动生成的 。 不手工编辑。

<a id="qlty-mcp-tools"></a>
# qlty 磁共振 工具

Qlty MCP 服务器自动生成的包装器。

<a id="tools"></a>
## 工具

- `qlty_check`: 在文件上运行插件 。 发现回返问题。 使用 -- fix 到自定义 。
- `qlty_fmt`: 使用已配置格式化的自动格式文件。
- `qlty_metrics`: 计算代码质量度量(复杂，重复等).
- `qlty_smells`:查找代码有气味(重复，复杂热点).
- `qlty_init`: 在仓库中初始化 qlty. 创建。qlty/qlty.toml.
- `qlty_plugins_list`: 列出可用的 qlty 插件。

<a id="usage"></a>
## 使用量

```python
from servers.qlty import qlty_check

# Use the tool
result = await qlty_check(params)
```

**说明**: 此文件是自动生成的 。 不手工编辑。

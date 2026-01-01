<a id="git-mcp-tools"></a>
# git 磁共振 工具

git MCP 服务器自动生成的包装。

<a id="tools"></a>
## 工具

- `git_status`: 显示工作树状态
- `git_diff_unstaged`: 显示工作目录中尚未设置的更改
- `git_diff_staged`: 显示要执行的更改
- `git_diff`: 显示分支之间的差异或承诺
- `git_commit`: 对寄存器的记录更改
- `git_add`: 将文件内容添加到中转区域
- `git_reset`: 取消所有阶段的更改
- `git_log`: 显示承诺日志
- `git_create_branch`: 从可选的基础分支创建新分支
- `git_checkout`: 切换分支
- `git_show`: 显示一个承诺的内容
- `git_branch`: 列表 Git 分支

<a id="usage"></a>
## 使用量

```python
from servers.git import git_status

# Use the tool
result = await git_status(params)
```

**说明**: 此文件是自动生成的 。 不手工编辑。

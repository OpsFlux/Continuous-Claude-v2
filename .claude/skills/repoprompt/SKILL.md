---
name: repoprompt
description: Use RepoPrompt CLI for token-efficient codebase exploration
allowed-tools: [Bash, Read]
---

<a id="repoprompt-skill"></a>
# RepoPrompt 技能

<a id="when-to-use"></a>
## 何时使用

- **爆炸码基结构**(树木、编码图)
- **搜索代码** 有上下文行
- **获取代码签名** 没有完整的文件内容( 收件效率)
- **读取文件切片**(特定行范围)
- **为任务构建上下文**

<a id="token-optimization"></a>
## 切换优化

RepoPrompt 是**比原始文件更有象征效率** 的：
- `structure`· 仅签字(不是全文)
- `read --start-line --limit`• 切片而不是完整文件
- `search --context-lines`+ 与上下文相关的匹配

<a id="cli-usage"></a>
## CLI 用法

```bash
# If installed to PATH (Settings → MCP Server → Install CLI to PATH)
rp-cli -e 'command'

# Or use the alias (configure in your shell)
repoprompt_cli -e 'command'
```

<a id="commands-reference"></a>
## 图标参考

<a id="file-tree"></a>
### 文件树
```bash
# Full tree
rp-cli -e 'tree'

# Folders only
rp-cli -e 'tree --mode folders'

# Selected files only
rp-cli -e 'tree --mode selected'
```

<a id="code-structure-codemaps-token-efficient"></a>
### 代码结构( 代码) - TOKEN 高效
```bash
# Structure of specific paths
rp-cli -e 'structure src/auth/'

# Structure of selected files
rp-cli -e 'structure --scope selected'

# Limit results
rp-cli -e 'structure src/ --max-results 10'
```

<a id="search"></a>
### 搜索
```bash
# Basic search
rp-cli -e 'search "pattern"'

# With context lines
rp-cli -e 'search "error" --context-lines 3'

# Filter by extension
rp-cli -e 'search "TODO" --extensions .ts,.tsx'

# Limit results
rp-cli -e 'search "function" --max-results 20'
```

<a id="read-files-token-efficient"></a>
### 读取文件 - TOKEN 效率
```bash
# Full file
rp-cli -e 'read path/to/file.ts'

# Line range (slice)
rp-cli -e 'read path/to/file.ts --start-line 50 --limit 30'

# Last N lines (tail)
rp-cli -e 'read path/to/file.ts --start-line -20'
```

<a id="selection-management"></a>
### 选择管理
```bash
# Add files to selection
rp-cli -e 'select add src/auth/'

# Set selection (replace)
rp-cli -e 'select set src/api/ src/types/'

# Clear selection
rp-cli -e 'select clear'

# View current selection
rp-cli -e 'select get'
```

<a id="workspace-context"></a>
### 工作空间背景
```bash
# Get full context
rp-cli -e 'context'

# Specific includes
rp-cli -e 'context --include prompt,selection,tree'
```

<a id="chain-commands"></a>
### 链式命令
```bash
# Multiple operations
rp-cli -e 'select set src/auth/ && structure --scope selected && context'
```

<a id="workspaces"></a>
### 工作空间
```bash
# List workspaces
rp-cli -e 'workspace list'

# List tabs
rp-cli -e 'workspace tabs'

# Switch workspace
rp-cli -e 'workspace switch "ProjectName"'
```

<a id="ai-chat-uses-repoprompts-models"></a>
### AI Chat( 使用 RepoPrompt 的模型)
```bash
# Send to chat
rp-cli -e 'chat "How does the auth system work?"'

# Plan mode
rp-cli -e 'chat "Design a new feature" --mode plan'
```

<a id="context-builder-ai-powered-file-selection"></a>
### 上下文构建器( AI 驱动文件选择)
```bash
# Auto-select relevant files for a task
rp-cli -e 'builder "implement user authentication"'
```

<a id="workflow-shorthand-flags"></a>
## 工作流程快手旗

```bash
# Quick operations without -e syntax
rp-cli --workspace MyProject --select-set src/ --export-context ~/out.md
rp-cli --chat "How does auth work?"
rp-cli --builder "implement user authentication"
```

<a id="script-files-rp"></a>
## 脚本文件 (. rp)

对于可重复的工作流程，将命令保存到脚本中：

```bash
# daily-export.rp
workspace switch Frontend
select set src/components/
context --all > ~/exports/frontend.md
```

运行方式 :
```bash
rp-cli --exec-file ~/scripts/daily-export.rp
```

<a id="cli-flags"></a>
## CLI 旗帜

| 旗帜 | 目的 |
|------|---------|
| `-e 'cmd'` | 执行命令 |
| `-w <id>` | 目标窗口标识 |
| `-q` | 静音模式 |
| `-d <cmd>` | 命令的详细帮助 |
| `--wait-for-server 5` | 等待连接( 标记) |

<a id="async-operations-tmux"></a>
## Async 操作( tmux)

用于长期运作`builder`，使用同源脚本 :

```bash
# Start context builder async
uv run python -m runtime.harness scripts/repoprompt_async.py \
    --action start --task "understand the auth system"

# With workspace switch
uv run python -m runtime.harness scripts/repoprompt_async.py \
    --action start --workspace "MyProject" --task "explore API patterns"

# Check status
uv run python -m runtime.harness scripts/repoprompt_async.py --action status

# Get result when done
uv run python -m runtime.harness scripts/repoprompt_async.py --action result

# Kill if needed
uv run python -m runtime.harness scripts/repoprompt_async.py --action kill
```

<a id="note"></a>
## 说明

需要使用 MCP 服务器运行的 RepoPrompt 应用程序 。

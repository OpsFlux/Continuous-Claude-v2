---
description: Token-efficient codebase exploration using RepoPrompt - USE FIRST for brownfield projects
---

<a id="rp-explorer-skill"></a>
# RP-爆炸者技能

使用 RepoPrompt CLI 进行 Token 高效代码库探索。 在规划或调试前将此用于棕地项目。

<a id="when-to-use"></a>
## 何时使用

- 在现有代码库中规划特征之前
- 调试问题前
- 当你需要理解代码结构而不读取每个文件时
- 当用户说"explore","理解代码库","X 是如何工作的"

<a id="cli-reference"></a>
## CLI 参考

<a id="basic-usage"></a>
### 基本用途
```bash
rp-cli -e '<command>'              # Run single command
rp-cli -e '<cmd1> && <cmd2>'       # Chain commands
rp-cli -w <id> -e '<command>'      # Target specific window
```

<a id="core-commands"></a>
### 核心命令

| 命令 | 别名 | 目的 |
|---------|---------|---------|
| `tree` | - | 文件/文件夹树 |
| `structure` | `map` | 代码签名( 收件效率) |
| `search` | `grep` | 用上下文搜索 |
| `read` | `cat` | 读取文件内容 |
| `select` | `sel` | 管理文件选择 |
| `context` | `ctx` | 导出工作空间背景 |
| `builder` | - | AI 驱动文件选择 |
| `chat` | - | 发送到 AI 聊天 |

<a id="file-tree"></a>
### 文件树
```bash
rp-cli -e 'tree'                    # Full tree
rp-cli -e 'tree --folders'          # Folders only
rp-cli -e 'tree --mode selected'    # Selected files only
```

<a id="code-structure-token-efficient"></a>
### 代码结构( TOKEN 优化)
```bash
rp-cli -e 'structure src/'          # Signatures for path
rp-cli -e 'structure .'             # Whole project
rp-cli -e 'structure --scope selected'  # Selected files only
```

<a id="search"></a>
### 搜索
```bash
rp-cli -e 'search "pattern"'
rp-cli -e 'search "TODO" --extensions .ts,.tsx'
rp-cli -e 'search "error" --context-lines 3'
rp-cli -e 'search "function" --max-results 20'
```

<a id="read-files"></a>
### 读取文件
```bash
rp-cli -e 'read path/to/file.ts'
rp-cli -e 'read file.ts --start-line 50 --limit 30'  # Slice
rp-cli -e 'read file.ts --start-line -20'            # Last 20 lines
```

<a id="selection-management"></a>
### 选择管理
```bash
rp-cli -e 'select add src/'         # Add to selection
rp-cli -e 'select set src/ lib/'    # Replace selection
rp-cli -e 'select clear'            # Clear selection
rp-cli -e 'select get'              # View selection
```

<a id="context-export"></a>
### 上下文导出
```bash
rp-cli -e 'context'                 # Full context
rp-cli -e 'context --include prompt,selection,tree'
rp-cli -e 'context --all > output.md'  # Export to file
```

<a id="ai-powered-builder"></a>
### AI 电源构建器
```bash
rp-cli -e 'builder "understand auth system"'
rp-cli -e 'builder "find API endpoints" --response-type plan'
```

<a id="chat"></a>
### 聊天
```bash
rp-cli -e 'chat "How does auth work?"'
rp-cli -e 'chat "Design new feature" --mode plan'
```

<a id="workspaces"></a>
### 工作空间
```bash
rp-cli -e 'workspace list'          # List workspaces
rp-cli -e 'workspace switch "Name"' # Switch workspace
rp-cli -e 'workspace tabs'          # List tabs
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

保存可重复的工作流程 :
```bash
# export.rp
workspace switch MyProject
select set src/
context --all > output.md
```

运行方式 :`rp-cli --exec-file ~/scripts/export.rp`

<a id="exploration-workflow"></a>
## 工作流量

<a id="step-1-get-overview"></a>
### 步骤 1:获得概览
```bash
rp-cli -e 'tree'
rp-cli -e 'structure .'
```

<a id="step-2-find-relevant-files"></a>
### 步骤 2:查找相关文件
```bash
rp-cli -e 'search "auth" --context-lines 2'
rp-cli -e 'builder "understand authentication"'
```

<a id="step-3-deep-dive"></a>
### 步骤 3:深潜
```bash
rp-cli -e 'select set src/auth/'
rp-cli -e 'structure --scope selected'
rp-cli -e 'read src/auth/login.ts'
```

<a id="step-4-export-context"></a>
### 步骤 4:导出背景
```bash
rp-cli -e 'context --all > codebase-map.md'
```

<a id="output"></a>
## 产出

在 :`thoughts/handoffs/<session>/codebase-map.md`

<a id="notes"></a>
## 页：1

- 需要使用 MCP 服务器的 RepoPrompt 应用程序
- 使用`rp-cli -d <cmd>`用于任何命令的详细帮助
- 调试效率 :`structure`给出签名而不包含全部内容

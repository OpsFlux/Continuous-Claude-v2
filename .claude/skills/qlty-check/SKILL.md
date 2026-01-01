---
name: qlty-check
description: Code quality checks, formatting, and metrics via qlty CLI
allowed-tools: [Bash, Read]
---

<a id="qlty-code-quality"></a>
# Qlty 代码质量

通过 qlty CLI 支持 40+语言 70+linters 的通用代码质量工具。

<a id="when-to-use"></a>
## 何时使用

- 执行/移交前检查规则
- 自动固定格式和样式问题
- 计算代码度量(复杂、重复)
- 查找有气味的代码

<a id="quick-reference"></a>
## 快速引用

```bash
# Check changed files with auto-fix
uv run python -m runtime.harness scripts/qlty_check.py --fix

# Check all files
uv run python -m runtime.harness scripts/qlty_check.py --all

# Format files
uv run python -m runtime.harness scripts/qlty_check.py --fmt

# Get metrics
uv run python -m runtime.harness scripts/qlty_check.py --metrics

# Find code smells
uv run python -m runtime.harness scripts/qlty_check.py --smells
```

<a id="parameters"></a>
## 参数

| 参数 | 说明 |
|-----------|-------------|
| `--check` | 运行接口( 默认) |
| `--fix` | 自动固定问题 |
| `--all` | 处理所有文件， 而不仅仅是更改 |
| `--fmt` | 替换为格式化文件 |
| `--metrics` | 计算代码度量衡 |
| `--smells` | 查找有气味的代码 |
| `--paths` | 具体文件/目录 |
| `--level` | 次要问题级别：说明/低/中/高 |
| `--cwd` | 工作目录 |
| `--init` | 在还原中初始化 qlty |
| `--plugins` | 列出可用的插件 |

<a id="common-workflows"></a>
## 共同工作流程

<a id="after-implementation"></a>
### 执行后
```bash
# Auto-fix what's possible, see what remains
uv run python -m runtime.harness scripts/qlty_check.py --fix
```

<a id="quality-report"></a>
### 质量报告
```bash
# Get metrics for changed code
uv run python -m runtime.harness scripts/qlty_check.py --metrics

# Find complexity hotspots
uv run python -m runtime.harness scripts/qlty_check.py --smells
```

<a id="initialize-in-new-repo"></a>
### 在新 Repo 中初始化
```bash
uv run python -m runtime.harness scripts/qlty_check.py --init --cwd /path/to/repo
```

<a id="direct-cli-if-qlty-installed"></a>
## 直接 CLI( 如果安装了 qlty)

```bash
# Check changed files
qlty check

# Auto-fix
qlty check --fix

# JSON output
qlty check --json

# Format
qlty fmt
```

<a id="requirements"></a>
## 所需资源

- **qlty CLI**:https://github.com/qltysh/qlty
- **MCP 服务器** :`servers/qlty/server.py`覆盖 CLI
- **结 论**:`.qlty/qlty.toml`在重播( 运行)`qlty init`(第一个)

<a id="vs-other-tools"></a>
## vs 其他工具

| 工具 | 使用大小写 |
|------|----------|
| (单位：千美元) | 任何语言的统一衬线、格式、衡量标准 |
| (单位：千美元) | 结构代码模式和重构 |
| **变型** | 快速文本搜索 |

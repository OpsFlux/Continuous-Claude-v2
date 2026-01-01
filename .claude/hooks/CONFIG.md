<a id="hooks-configuration-guide"></a>
# Hooks 配置指南

本指南解释如何配置和定制您的工程的钩子系统 。

<a id="quick-start-configuration"></a>
## 快速启动配置

<a id="1-register-hooks-in-claudesettingsjson"></a>
### 1. 在。claude/sets.json 中注册钩

创建或更新`.claude/settings.json`在项目根中：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use-tracker.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-prettier-formatter.sh"
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-build-check-enhanced.sh"
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/error-handling-reminder.sh"
          }
        ]
      }
    ]
  }
}
```

<a id="2-install-dependencies"></a>
### 2. 安装依赖

```bash
cd .claude/hooks
npm install
```

<a id="3-set-execute-permissions"></a>
### 3. 设置执行权限

```bash
chmod +x .claude/hooks/*.sh
```

<a id="customization-options"></a>
## 自定义选项

<a id="project-structure-detection"></a>
### 项目结构检测

默认情况下， 钩子会检测这些目录模式 :

**前线：**`frontend/`, `client/`, `web/`, `app/`, `ui/`页：1`backend/`, `server/`, `api/`, `src/`, `services/`**数据库：**`database/`, `prisma/`, `migrations/`**摩纳哥：**`packages/*`, `examples/*`

<a id="adding-custom-directory-patterns"></a>
#### 添加自定义目录模式

编辑`.claude/hooks/post-tool-use-tracker.sh`，函数`detect_repo()`:

```bash
case "$repo" in
    # Add your custom directories here
    my-custom-service)
        echo "$repo"
        ;;
    admin-panel)
        echo "$repo"
        ;;
    # ... existing patterns
esac
```

<a id="build-command-detection"></a>
### 构建命令检测

钩子根据：
1. 有无`package.json`带有“ 构建” 脚本
2. 软件包管理器( pnpm > npm > 纱线)
3. 特殊情况(Prisma schemas)

<a id="customizing-build-commands"></a>
#### 自定义构建命令

编辑`.claude/hooks/post-tool-use-tracker.sh`，函数`get_build_command()`:

```bash
# Add custom build logic
if [[ "$repo" == "my-service" ]]; then
    echo "cd $repo_path && make build"
    return
fi
```

<a id="typescript-configuration"></a>
### 类型脚本配置

钩子自动检测 :
- `tsconfig.json`标准类型脚本项目
- `tsconfig.app.json`虚拟/反应项目

<a id="custom-typescript-configs"></a>
#### 自定义类型脚本配置

编辑`.claude/hooks/post-tool-use-tracker.sh`，函数`get_tsc_command()`:

```bash
if [[ "$repo" == "my-service" ]]; then
    echo "cd $repo_path && npx tsc --project tsconfig.build.json --noEmit"
    return
fi
```

<a id="prettier-configuration"></a>
### 高级配置

在此顺序下对配置进行更漂亮的钩子搜索 :
1. 当前文件目录( 向上行走)
2. 项目根
3. 回落到 Pretier 默认值

<a id="custom-prettier-config-search"></a>
#### 自定义 Pretier 配置搜索

编辑`.claude/hooks/stop-prettier-formatter.sh`，函数`get_prettier_config()`:

```bash
# Add custom config locations
if [[ -f "$project_root/config/.prettierrc" ]]; then
    echo "$project_root/config/.prettierrc"
    return
fi
```

<a id="error-handling-reminders"></a>
### 处理错误提醒

配置文件类别检测`.claude/hooks/error-handling-reminder.ts`:

```typescript
function getFileCategory(filePath: string): 'backend' | 'frontend' | 'database' | 'other' {
    // Add custom patterns
    if (filePath.includes('/my-custom-dir/')) return 'backend';
    // ... existing patterns
}
```

<a id="error-threshold-configuration"></a>
### 阈值配置出错

更改何时推荐自动解析器 。

编辑`.claude/hooks/stop-build-check-enhanced.sh`:

```bash
# Default is 5 errors - change to your preference
if [[ $total_errors -ge 10 ]]; then  # Now requires 10+ errors
    # Recommend agent
fi
```

<a id="environment-variables"></a>
## 环境变量

<a id="global-environment-variables"></a>
### 全球环境变量

在您的 shell 配置文件中设定( E)`.bashrc`, `.zshrc`等 :

```bash
# Disable error handling reminders
export SKIP_ERROR_REMINDER=1

# Custom project directory (if not using default)
export CLAUDE_PROJECT_DIR=/path/to/your/project
```

<a id="per-session-environment-variables"></a>
### 每次会议环境变量

在启动 Claude 代码前设定 :

```bash
SKIP_ERROR_REMINDER=1 claude-code
```

<a id="hook-execution-order"></a>
## Hook 执行命令

停止钩子按指定的顺序运行`settings.json`:

```json
"Stop": [
  {
    "hooks": [
      { "command": "...formatter.sh" },    // Runs FIRST
      { "command": "...build-check.sh" },  // Runs SECOND
      { "command": "...reminder.sh" }      // Runs THIRD
    ]
  }
]
```

**这一命令为何重要：**
1. 首先格式化文件( 干净代码)
2. 然后检查错误
3. 最后显示提醒

<a id="selective-hook-enabling"></a>
## 选择钩启用

你不需要所有的钩子。 选择对您的项目有效的内容 :

<a id="minimal-setup-skill-activation-only"></a>
### 最小设置( 只有技能激活)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
          }
        ]
      }
    ]
  }
}
```

<a id="build-checking-only-no-formatting"></a>
### 仅构建检查( 无格式)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use-tracker.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-build-check-enhanced.sh"
          }
        ]
      }
    ]
  }
}
```

<a id="formatting-only-no-build-checking"></a>
### 只格式化( 没有构建检查)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use-tracker.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-prettier-formatter.sh"
          }
        ]
      }
    ]
  }
}
```

<a id="cache-management"></a>
## 快取管理

<a id="cache-location"></a>
### 缓存位置

```
$CLAUDE_PROJECT_DIR/.claude/tsc-cache/[session_id]/
```

<a id="manual-cache-cleanup"></a>
### 手动缓存清理

```bash
# Remove all cached data
rm -rf $CLAUDE_PROJECT_DIR/.claude/tsc-cache/*

# Remove specific session
rm -rf $CLAUDE_PROJECT_DIR/.claude/tsc-cache/[session-id]
```

<a id="automatic-cleanup"></a>
### 自动清理

构建检查钩子在成功构建时自动清理会话缓存 。

<a id="troubleshooting-configuration"></a>
## 解决问题配置

<a id="hook-not-executing"></a>
### Hook 不执行

1. **核对登记：** 校验钩入`.claude/settings.json`
2. **检查权限：** 运行`chmod +x .claude/hooks/*.sh`
3. **检查路径：** 保证`$CLAUDE_PROJECT_DIR`设置正确
4. **检查类型脚本 :** 运行`cd .claude/hooks && npx tsc`检查错误

<a id="false-positive-detections"></a>
### 虚假正检测

**问题：** 钩子触发文件 它不应该

**解决：** 在相关勾钩中添加跳过条件 :

```bash
# In post-tool-use-tracker.sh
if [[ "$file_path" =~ /generated/ ]]; then
    exit 0  # Skip generated files
fi
```

<a id="performance-issues"></a>
### 业绩问题

**问题：** 钩子很慢

**结果：**
1. 仅将类型脚本检查限制为已更改的文件
2. 使用更快的软件包管理器( pnpm > npm)
3. 添加更多跳过条件
4. 禁用大文件的 Pretier

```bash
# Skip large files in stop-prettier-formatter.sh
file_size=$(wc -c < "$file" 2>/dev/null || echo 0)
if [[ $file_size -gt 100000 ]]; then  # Skip files > 100KB
    continue
fi
```

<a id="debugging-hooks"></a>
### 调试钩

将调试输出添加到任何钩子 :

```bash
# At the top of the hook script
set -x  # Enable debug mode

# Or add specific debug lines
echo "DEBUG: file_path=$file_path" >&2
echo "DEBUG: repo=$repo" >&2
```

在 Claude Code 的日志中查看钩子执行。

<a id="advanced-configuration"></a>
## 高级配置

<a id="custom-hook-event-handlers"></a>
### 自定义钩事件处理器

您可以为其它事件创建自己的钩子 :

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/my-custom-bash-guard.sh"
          }
        ]
      }
    ]
  }
}
```

<a id="monorepo-configuration"></a>
### Monorepo 配置

对于有多个软件包的单重机：

```bash
# In post-tool-use-tracker.sh, detect_repo()
case "$repo" in
    packages)
        # Get the package name
        local package=$(echo "$relative_path" | cut -d'/' -f2)
        if [[ -n "$package" ]]; then
            echo "packages/$package"
        else
            echo "$repo"
        fi
        ;;
esac
```

<a id="dockercontainer-projects"></a>
### Docker/集装箱项目

如果您的构建命令需要在容器中运行：

```bash
# In post-tool-use-tracker.sh, get_build_command()
if [[ "$repo" == "api" ]]; then
    echo "docker-compose exec api npm run build"
    return
fi
```

<a id="best-practices"></a>
## 最佳做法

1. **开始最小** - 一次启用一个钩
2. **彻底试验** -- -- 进行修改并核实钩子的作用
3. **文件定制** - 添加注释来解释自定义逻辑
4. **质量控制** - 提交`.claude/`要 git 的目录
5. **团队一致性** - 团队共享配置

<a id="see-also"></a>
## 另见

- [读取](./README.md)- Hook 概况
- [../../docs/HOOKS_SYSTEM.md](../../docs/HOOKS_SYSTEM.md)- 完整的钩子参考
- [../../docs/SKILLS_SYSTEM.md](../../docs/SKILLS_SYSTEM.md)- 技能融合

<a id="hooks"></a>
# 钩子

Claude 代码钩子可以实现技能自动激活，文件跟踪，以及验证。

**零运行时间依赖** -- -- 钩被预先捆绑，只是克隆和去。

---

<a id="architecture"></a>
## 架构

```
hooks/
├── src/              # TypeScript source (for development)
├── dist/             # Pre-bundled JS (committed, ready to run)
├── *.sh              # Shell wrappers (call node dist/*.mjs)
├── build.sh          # Rebuild dist/ after modifying src/
└── package.json      # Dev dependencies only (esbuild)
```

**用户：** 只要复制回转。 Hook 马上行动

**对于开发者：** 编辑`src/*.ts`，然后运行`./build.sh`为了重建。

---

<a id="what-are-hooks"></a>
## 什么是 Hook 吗?

Hooks 是运行在 Claude 工作流程特定点的脚本：
- **用户提交**: 当用户提交提示时
- **预用工具**: 在工具执行之前
- **后工具用途**: 工具完成后
- **会议开始**: 届会开始/续会时
- **会议结束**:会议结束时
- 页：1 上下文收缩前
- **副剂停止**: 子剂完成后

**关键见解：** Hooks 可以修改提示，屏蔽动作，以及跟踪状态——使能特性 Claude 不能单独完成。

---

<a id="essential-hooks-start-here"></a>
## 基本钩 (从这里开始)

<a id="skill-activation-prompt-userpromptsubmit"></a>
### 技能激活- 即时( 用户 Prompt Submit)

**目标：** 根据用户提示和文件上下文自动推荐相关技能

**如何运作：**
1. 读取`skill-rules.json`
2. 匹配用户触发模式
3. 检查用户与哪些文件合作
4. 将技能建议注入 Claude 的背景

*为什么是关键 * 这个钩子可以使技能自动激活。

**合并：**
```bash
# Just copy - no npm install needed!
cp -r .claude/hooks your-project/.claude/

# Make shell scripts executable
chmod +x your-project/.claude/hooks/*.sh
```

**添加到设置中。json:**
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

---

<a id="post-tool-use-tracker-posttooluse"></a>
### 工具使用后跟踪器(后工具使用)

**目标：** 跟踪文件更改并构建上下文管理尝试

**如何运作：**
1. 监视器 编辑/ Write/ Bash 工具调用
2. 修改文件的记录
3. 收集积存/测试合格/推理失败
4. 自动检测项目结构(前端、后端、软件包等)

*为什么是关键 * 帮助 Claude 理解你代码库的哪些部分是活性的。

**添加到设置中。json:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use-tracker.sh"
          }
        ]
      }
    ]
  }
}
```

---

<a id="continuity-hooks"></a>
## 连续钩

<a id="session-start-continuity-sessionstart"></a>
### 会 议 开 幕

**目标：** 在会话开始/恢复/压缩时装入连续性分类账

<a id="pre-compact-continuity-precompact"></a>
### 预压缩连续( 预压缩)

**目标：** 在上下文收缩前自动创建交接文档

<a id="session-end-cleanup-sessionend"></a>
### 届会结束(届会结束)

**目标：** 更新分类账时间戳， 清除旧缓存

<a id="subagent-stop-continuity-subagentstop"></a>
### 子代理停止持续( 子代理停止)

**目标：** 日志代理输出到分类账和缓存以恢复

---

<a id="development"></a>
## 发展

修改钩子 :

```bash
# Edit TypeScript source
vim src/skill-activation-prompt.ts

# Rebuild bundled JS
./build.sh

# Test
echo '{"prompt": "test"}' | ./skill-activation-prompt.sh
```

这个`build.sh`如果需要， 脚本会安装 dev 依赖( 构建) 。

---

<a id="for-claude-code"></a>
## Claude Code

**为用户设置钩子时：**

1. **接受钩子目录** - 不需要 npm 安装
2. **制作可执行的 shell 脚本 :**`chmod +x .claude/hooks/*.sh`
3. **如上所示，添加到设置。json**
4. **设置后核实：**
   ```bash
   ls -la .claude/hooks/*.sh | grep rwx
   ```

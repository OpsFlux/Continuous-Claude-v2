---
globs: [".claude/skills/**/*"]
---

<a id="skill-development-rules"></a>
# 技能发展规则

处理文件时`.claude/skills/`:

<a id="skillmd-structure"></a>
## SKILL.md 结构

```yaml
---
name: skill-name
description: Brief description
allowed-tools: [Bash, Read]  # Optional: restrict tools
---
```

<a id="do"></a>
## DO
- 保持 SKILL.md 简洁( < 200 行)
- 包含清晰的“ 何时使用” 部分
- 提供复制- 粘贴的 bash 命令
- MCP 操作的参考脚本/ Name
- 将触发器添加到技能规则。 json

<a id="dont"></a>
## 别
- 在 SKILL.md 中包含执行细节
- 跨技能复制内容
- 在技能规则中创建没有相应触发功能的技能。 json
- 使用不需要的允许工具

<a id="mcp-wrapper-skills"></a>
## MCP 包装技能
对于包接 MCP 脚本的技能：
- 使用`allowed-tools: [Bash, Read]`限制能力
- 指向脚本/ 目录中的脚本
- 包含参数文档

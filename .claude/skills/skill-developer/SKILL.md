---
name: skill-developer
description: Meta-skill for creating and managing Claude Code skills
allowed-tools: [Bash, Read, Write, Edit]
---

<a id="skill-developer"></a>
# 技能开发者

用于创造 Claude 密码新技能的元技能，包括包接 MCP 管线的技能。

<a id="when-to-use"></a>
## 何时使用

- "为 X 创造技能"
- "帮我做个新技能"
- "把这个剧本变成技巧"
- "我怎样创造技能?"

<a id="skill-structure"></a>
## 技能结构

技能生活在`.claude/skills/<skill-name>/`:

```
.claude/skills/my-skill/
├── SKILL.md          # Required: Main skill definition
├── scripts/          # Optional: Supporting scripts
└── templates/        # Optional: Templates, examples
```

<a id="skillmd-format"></a>
### SKILL.md 格式

```yaml
---
name: skill-name
description: Brief description (shown in skill list)
allowed-tools: [Bash, Read, Write]  # Optional: restrict tools
---

# Skill Name

## When to Use
[When Claude should discover this skill]

## Instructions
[Step-by-step instructions for Claude to follow]

## Examples
[Usage examples]
```

<a id="creating-an-mcp-pipeline-skill"></a>
## 创建 MCP 管道技能

要创建新的 MCP 链脚本并把它包装成一种技能：

<a id="step-1-use-the-template"></a>
### 步骤 1:使用模板

复制多工具管模板 :

```bash
cp $CLAUDE_PROJECT_DIR/scripts/multi_tool_pipeline.py $CLAUDE_PROJECT_DIR/scripts/my_pipeline.py
```

引用模板模式 :

```bash
cat $CLAUDE_PROJECT_DIR/.claude/skills/multi-tool-pipeline/SKILL.md
cat $CLAUDE_PROJECT_DIR/scripts/multi_tool_pipeline.py
```

<a id="step-2-customize-the-script"></a>
### 步骤 2: 自定义脚本

编辑您的新脚本以链接您需要的 MCP 工具 :

```python
async def main():
    from runtime.mcp_client import call_mcp_tool
    args = parse_args()

    # Chain your MCP tools (serverName__toolName)
    result1 = await call_mcp_tool("server1__tool1", {"param": args.arg1})
    result2 = await call_mcp_tool("server2__tool2", {"input": result1})

    print(result2)
```

<a id="step-2-create-the-skill"></a>
### 第 2 步： 创建技能

创建`.claude/skills/my-pipeline/SKILL.md`:

```markdown
---
name: my-pipeline
description: What the pipeline does
allowed-tools: [Bash, Read]
---

# My Pipeline Skill

## When to Use
- [Trigger conditions]

## Instructions

Run the pipeline:

\`\`\`bash
uv run python -m runtime.harness scripts/my_pipeline.py --arg1 "value"
\`\`\`

### Parameters
- `--arg1`: Description

## MCP Servers Required
- server1: For tool1
- server2: For tool2
```

<a id="step-3-add-triggers-optional"></a>
### 第 3 步：添加触发器(可选)

添加为`.claude/skills/skill-rules.json`:

```json
{
  "skills": {
    "my-pipeline": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "medium",
      "description": "What it does",
      "promptTriggers": {
        "keywords": ["keyword1", "keyword2"],
        "intentPatterns": ["(pattern).*?(match)"]
      }
    }
  }
}
```

<a id="reference-files"></a>
## 参考文件

将所有细节改为：

```bash
cat $CLAUDE_PROJECT_DIR/.claude/rules/skill-development.md
cat $CLAUDE_PROJECT_DIR/.claude/rules/mcp-scripts.md
```

<a id="quick-checklist"></a>
## 快速核对列表

- [ ] SKILL.md 有前题(名称，描述)
- [ ] "何时使用"一节很清晰
- [ ] 指令已经准备好
- [ ] 必要时记录 MCP 服务器
- [ ] 触发器添加到技能规则。 json (可选)

<a id="examples-in-this-repo"></a>
## 本 Repo 中的例子

审视模式的现有技能：

```bash
ls $CLAUDE_PROJECT_DIR/.claude/skills/
cat $CLAUDE_PROJECT_DIR/.claude/skills/commit/SKILL.md
cat $CLAUDE_PROJECT_DIR/.claude/skills/firecrawl-scrape/SKILL.md
```

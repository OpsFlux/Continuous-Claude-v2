<a id="claude-code-skills-integration"></a>
# Claude 代码技能整合

** 显示 Claude 代码技能与 MCP 工作流程自动化的恰当整合。

---

<a id="structure"></a>
## 结构

此目录包含 Claude Code 本地格式的 Switchs :

```
.claude/skills/
├── simple-fetch/
│   ├── SKILL.md        # Claude Code Skills format (YAML + markdown)
│   └── workflow.py     # Executable Python workflow
└── multi-tool-pipeline/
    ├── SKILL.md        # Claude Code Skills format
    └── workflow.py     # Executable Python workflow
```

<a id="claude-code-skills-format"></a>
## Claude 代码技能格式

每个技能目录包含：

**1. SKILL.md(需要)**
- YAML 前题`name`和`description`
- Claude 要遵循的马克德指令
- 引用工作流程。py 与 CLI 的用法

**2. 工作流程。py(执行)**
- 带有 argparse CLI 的 Python 脚本
- MCP 工具管弦码
- 回归结构化成果

<a id="how-claude-code-discovers-these"></a>
## Claude Code 如何发现 这些

**自动发现：**
Claude 代码扫描`.claude/skills/`并发现：
- 简单牵引
- 多工具管线

**当触发时：**
1. Claude 读取 SKILL.md
2. 遵循指令
3. 执行工作流程。py 并配有适当的 CLI 参数
4. 回返结果

<a id="skills-vs-scripts"></a>
## 技能对脚本

**`.claude/skills/`** (本目录):
- Claude Code 技能格式(由 Claude 发现)
- SKILL.md 有 YAML 前题
- Claude 代码验证规则

**`../../skills/`** (家长目录):
- Python CLI 工作流程脚本
- 可单独执行
- 技能参考

**合并：**
- Claude 代码发现的技能包工作流程
- 工作流程可用或不可用技能包装
- 最好的是 Claude 的框架 +我们的执行效率

<a id="generic-examples-included"></a>
## 通用示例

简略比较：**
- 基本单一工具模式
- 简单工作流程模板
- 演示 CLI 参数模式

**多工具管线：**
- 多工具链式
- 复杂工作流程模板
- 显示顺序执行

<a id="creating-custom-skills"></a>
## 创建自定义技能

1. 写入 Python 工作流程`../../skills/`
2. 在此创建目录 :`.claude/skills/your-skill-name/`
3. 用适当的格式写 SKILL.md
4. 链接或复制工作流程为工作流程。py
5. 用 Claude 代码进行测试

<a id="validation-rules"></a>
## 审定规则

技能必须经过 Claude Code 验证：
- `name`: 小写字母，数字，仅连字符(最多 64 个字符)
- `description`: 非空 (最大 1024 个字符)
- 没有 XML 标签
- 无保留词

<a id="documentation"></a>
## 文档

- 个人 SKILL.md 文件 - 特定技能文档
- ../../skills/SKILLS.md- 工作流程系统指南
- ../../README.md- 完成项目文件

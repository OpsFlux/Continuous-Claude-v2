<a id="claude-onboarding"></a>
# Claude 登机

你得到了这个寄存器 来理解，扩展，或帮助执行。 这是你需要知道的。

---

<a id="what-this-is"></a>
## 这是什么

**持续 Claude** - Claude 代码的会话管理系统：
1. 整个保留状态`/clear`通过减记分类账进行业务
2. 通过懒载代码执行减少 MCP 令牌管理
3. 今后届会的推理和决定

---

<a id="core-concepts"></a>
## 核心概念

<a id="the-problem-we-solve"></a>
### 我们所解决的问题

Claude Code 的上下文收缩失常。 经过多处收缩后，你正在处理退化的背景(摘要摘要).

**我们的办法：** 明确而非紧凑。 保存状态到外部文件( lidges), 擦去上下文干净， 重新装入完全忠诚 。

<a id="key-files"></a>
### 密钥文件

| 文件 | 目的 |
|------|---------|
| `CONTINUITY_CLAUDE-*.md` | 活动会话状态( ephemeral, 每个更新覆盖) |
| `thoughts/handoff/*.md` | 交接会(永久) |
| `thoughts/shared/plans/*.md` | 实施计划(永久) |
| `.git/claude/commits/*/reasoning.md` | 每项罪行(长期、地方) |

<a id="session-lifecycle"></a>
### 会话周期

```
Session Start → Ledger auto-loads → Work → Context fills (70%+)
    → Update ledger → /clear → Fresh session → Ledger reloads → Continue
```

---

<a id="directory-map"></a>
## 目录映射

```
.claude/
├── skills/           # Skills I can invoke (read SKILL.md files)
├── hooks/            # Event handlers (SessionStart, PostToolUse, etc.)
├── agents/           # Sub-agent configurations
├── rules/            # Behavioral rules (auto-applied)
└── settings.json     # Hook registrations

docs/                 # Human documentation
scripts/              # MCP workflow scripts (Python)
src/runtime/          # MCP execution runtime
servers/              # Generated MCP wrappers (gitignored)
thoughts/             # Research, plans, handoffs (gitignored)
```

---

<a id="available-skills"></a>
## 现有技能

<a id="session-management"></a>
### 会话管理
- `/continuity_ledger`- 更新状态之前`/clear`
- `/create_handoff`- 为新会话保存工作
- `/resume_handoff`- 从交割文件恢复

<a id="development"></a>
### 发展
- `/create_plan`- 制定执行计划
- `/implement_plan`- 通过核查执行计划
- `/validate_plan`- 对照计划检查执行情况
- `/commit`- 基特没有 Claude 的归属
- `/debug`- 调查问题

<a id="research"></a>
### 研究
- `/research`- 文件编码库发现
- `/recall-reasoning`- 寻找过去的决定

<a id="mcp-tools"></a>
### MCP 工具
- `/repoprompt`- 代号高效勘探编码图
- `/morph-search`- 快速密码库搜索(20x grep)
- `/nia-docs`- 图书馆文件查询
- `/perplexity-search`- 网络研究
- `/firecrawl-scrape`- 网络刮刮
- `/github-search`- GitHub 代码/检索搜索
- `/ast-grep-find`- 基于 AST 的代码模式

---

<a id="how-to-work-with-this-repo"></a>
## 如何与这个 Repo 合作

<a id="if-asked-to-implement-a-feature"></a>
### 如果被要求执行一个特性

1. **首先研究**----了解现有模式
   ```
   /research
   ```

2. 制定计划 别跳到密码上
   ```
   /create_plan
   ```

3. **与用户审查计划** -- -- 在执行前获得批准

4. **执行** -- -- 各阶段的工作
   ```
   /implement_plan
   ```

5. **上下文限制** -- -- 70 -- -- 更新分类账和`/clear`

6. **变量** -- -- 对照成功标准进行核查。
   ```
   /validate_plan
   ```

7. **承诺** - 捕获推理
   ```
   /commit
   ```

<a id="if-asked-to-extend-the-kit"></a>
### 如果被问到要扩展套件

关键扩展点 :

| 添加 | 地点 | 图案 |
|--------|----------|---------|
| 新技能 | `.claude/skills/<name>/SKILL.md` | 复制现有技能结构 |
| 新钩子 | `.claude/hooks/<name>.sh` + `.ts` | 外壳包装器 — TypeScript 处理器 |
| 新建 MCP 脚本 | `scripts/<name>.py` | 通过 argparse 的 CLI 参数 |
| 新规则 | `.claude/rules/<name>.md` | YAML 前题 + 平分 |
| 新代理人 | `.claude/agents/<name>.md` | 代理配置格式 |

<a id="if-asked-to-debug"></a>
### 如果被请求调试

1. 检查钩状注册`.claude/settings.json`
2. 手动测试钩 :`echo '{"type":"resume"}' | .claude/hooks/<hook>.sh`
3. 检查 MCP 配置`mcp_config.json`
4. 重生包装：`uv run mcp-generate`

---

<a id="patterns-to-follow"></a>
## 要遵循的模式

<a id="continuity"></a>
### 连续性
- 分类账中一个"现在"项目(焦点)
- 更新分类账前`/clear`(不在之后)
- 清除后使用 UNCONFIRMED 前缀验证

<a id="skills"></a>
### 技能
- 保留 SKILL.md < 200 行
- 包括“ 何时使用” 和“ 不使用时”
- MCP 操作的参考脚本/ Name

<a id="hooks"></a>
### 钩子
- 外壳包件 — TypeScript 处理器模式
- JSON 归来：`{"result": "continue"}` or `{"result": "block", "message": "..."}`

<a id="mcp-scripts"></a>
### MCP 脚本
- 使用 CLI 参数，而不是硬编码值
- 工具标识 :`serverName__toolName`(双下划线)
- 可选字段的防御编码

---

<a id="quick-commands"></a>
## 快速命令

```bash
# Install dependencies
uv sync
cd .claude/hooks && npm install && cd ../..

# Generate MCP wrappers
uv run mcp-generate

# Run MCP script
uv run python -m runtime.harness scripts/<script>.py --help

# Test a hook
echo '{"type":"resume"}' | .claude/hooks/session-start-continuity.sh
```

---

<a id="what-to-read"></a>
## 要读什么

| 优先权 | 文档 | 为什么 |
|----------|----------|-----|
| 1 | `docs/WORKFLOW.md` | 用户如何与 Claude 合作 |
| 2 | `docs/ARCHITECTURE.md` | 视觉系统概览 |
| 3 | `docs/CONTINUITY.md` | 编目/手递详情 |
| 4 | `CLAUDE.md` | 命令和执行模式 |
| 5 | `docs/FAQ.md` | 哲学和解决问题 |

---

<a id="key-constraints"></a>
## 主要制约因素

- **清除 > 压缩** - 总是倾向于`/clear`将分类账加压缩
- **学术产出** - 目标不是填补背景，而是重点工作的最低标志
- **外部状态** -- -- 探险家和思想/是真理的来源，而不是对话

---
globs: ["thoughts/ledgers/CONTINUITY_CLAUDE-*.md"]
---

<a id="continuity-ledger-rules"></a>
# 连续规则

分类账是了解真相的唯一来源，用于会议状态和多阶段的执行。

<a id="file-location"></a>
## 文件位置
- 探险家住在：`thoughts/ledgers/`
- 格式 :`thoughts/ledgers/CONTINUITY_CLAUDE-<session-name>.md`
- 对会话名称使用 kebab 大小写
- 每个工作流有一个分类账

<a id="required-sections"></a>
## 所需章节
1. **目标** - 成功标准("done"是什么样子的?).
2. **制约** -- -- 技术要求、模式
3. **关键决定** -- -- 所作选择的理由
4. **状态** - 完成/现在/下一个带有多阶段工作的复选框
5. **开放式问题** -- -- 将不确定项目标为 UNCONFIRMED
6. **工作集** - 文件、分支、测试命令

<a id="state-section-multi-phase-format"></a>
## 状态部分：多阶段格式

对于多相执行，在状态下使用复选框：

```markdown
## State
- Done:
  - [x] Phase 1: Setup database schema
  - [x] Phase 2: Create API endpoints
- Now: [→] Phase 3: Add validation logic
- Next: Phase 4: Frontend components
- Remaining:
  - [ ] Phase 5: Wire up API calls
  - [ ] Phase 6: Write tests
```

**检查框表示：**
- `[x]`= 已完成
- `[→]`= 进行中(当前)
- `[ ]`= 待决

**文件的复选框为何：** TodoWrite 活下来了收缩，但围绕这些待办事宜的*理解*每一次都会被压缩。 基于文件的复选框永远不会被压缩——完全忠诚保存。

<a id="starting-an-implementation"></a>
## 启动执行

在执行具有多个阶段的计划时：
1. 在状态部分添加所有阶段为复选框
2. 将当前阶段标记为`[→]`
3. 在每个阶段完成时更新复选框
4. 状态行显示 :`✓ Phase 2 → Phase 3: Current work`

<a id="when-to-update"></a>
## 何时更新
- 完成阶段后( 立即更新复选框)
- 在此之前`/clear`(总是清晰，从不紧凑)
- 当上下文使用量大于 70%时

<a id="unconfirmed-prefix"></a>
## 未识别前缀
```markdown
## Open Questions
- UNCONFIRMED: Does the auth middleware need updating?
```

<a id="after-clear"></a>
## 清除后
1. 自动装入编程器( CASEStart sook)
2. 查找`[→]`以查看当前阶段
3. 核查任何未识别物项
4. 从您留下的新上下文继续

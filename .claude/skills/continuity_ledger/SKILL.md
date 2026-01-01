---
description: Create or update continuity ledger for state preservation across clears
---

<a id="continuity-ledger"></a>
# 连续性编辑器

保存幸存的分类账文件`/clear`长会的 与交割(交叉会话)不同，分类账在会话中保留状态。

**为什么是明确而不是紧凑?** 每个收缩都是减压的——经过几个收缩后，你正在处理退化的背景。 清除 + 装入分类账 给您带来全信号的新上下文 。

<a id="when-to-use"></a>
## 何时使用

- 运行前`/clear`
- 背景使用接近 70QQ
- 多日执行
- 复杂的重构件您捡起/ 击倒
- 任何预计会冲击 85-%的会话

<a id="when-not-to-use"></a>
## 不使用时

- 快速任务( < 30 分钟)
- 简单的错误修正
- 单文件更改
- 已使用交接方式进行跨会次转移

<a id="process"></a>
## 进程

<a id="1-determine-ledger-file"></a>
### 1. 确定编辑器文件

检查是否有分类账 :
```bash
ls thoughts/ledgers/CONTINUITY_CLAUDE-*.md 2>/dev/null
```

- **如果存在**: 更新现有分类账
- **如果没有**: 创建新文件 :`thoughts/ledgers/CONTINUITY_CLAUDE-<session-name>.md`
  - 第一个保证目录存在 :`mkdir -p thoughts/ledgers`
  - 对会话名称使用 kebab- case( 例如 )`auth-refactor`, `api-migration`)

<a id="2-createupdate-ledger"></a>
### 2. 创建/更新编辑器

使用此模板结构 :

```markdown
# Session: <name>
Updated: <ISO timestamp>

## Goal
<Success criteria - what does "done" look like?>

## Constraints
<Tech requirements, patterns to follow, things to avoid>

## Key Decisions
<Choices made with brief rationale>
- Decision 1: Chose X over Y because...
- Decision 2: ...

## State
- Done: <completed items>
- Now: <current focus - ONE thing only>
- Next: <queued items in priority order>

## Open Questions
- UNCONFIRMED: <things needing verification after clear>
- UNCONFIRMED: <assumptions that should be validated>

## Working Set
<Active files, branch, test commands>
- Branch: `feature/xyz`
- Key files: `src/auth/`, `tests/auth/`
- Test cmd: `npm test -- --grep auth`
- Build cmd: `npm run build`
```

<a id="3-update-guidelines"></a>
### 3. 最新准则

**何时更新分类账：**
- 会话开始： 读取并刷新
- 重大决定之后
- 在此之前`/clear`
- 在自然断点
- 当上下文使用量大于 70%时

**更新内容：**
- 将已完成的项目从“ 现在” 移动到“ 完成 ”
- 更新当前焦点的“ 现在”
- 做出新的决定
- 如果不确定， 将项目标为 UNCONFIRMED

<a id="4-after-clear-recovery"></a>
### 4. 明确恢复后

之后恢复时`/clear`:

1. **自动加载**(会议启动钩)
2. **审查已确认的项目**
3. **提出 1 至 3 个有针对性的问题，**以验证假设
4. **最新分类账** 有说明
5. **继续工作**

<a id="template-response"></a>
## 模板回应

在创建/更新分类账后回复：

```
Continuity ledger updated: thoughts/ledgers/CONTINUITY_CLAUDE-<name>.md

Current state:
- Done: <summary>
- Now: <current focus>
- Next: <upcoming>

Ready for /clear - ledger will reload on resume.
```

<a id="comparison-with-other-tools"></a>
## 与其他工具的比较

| 工具 | 范围 | 忠诚 |
|------|-------|----------|
| Claude·姆德(签名) | 项目 | 总是新鲜而稳定的图案 |
| 写入 | 转弯 | 活下来了，但知觉会退化 |
| 继续  claude- *.md | 会议 | 外部文件——从未压缩过，完全忠诚 |
| 处理 | 闭会期间 | 外部文件- 新会话的详细上下文 |

<a id="example"></a>
## 示例

```markdown
# Session: auth-refactor
Updated: 2025-01-15T14:30:00Z

## Goal
Replace JWT auth with session-based auth. Done when all tests pass and no JWT imports remain.

## Constraints
- Must maintain backward compat for 2 weeks (migration period)
- Use existing Redis for session storage
- No new dependencies

## Key Decisions
- Session tokens: UUID v4 (simpler than signed tokens for our use case)
- Storage: Redis with 24h TTL (matches current JWT expiry)
- Migration: Dual-auth period, feature flag controlled

## State
- Done: Session model, Redis integration, login endpoint
- Now: Logout endpoint and session invalidation
- Next: Middleware swap, remove JWT, update tests

## Open Questions
- UNCONFIRMED: Does rate limiter need session awareness?

## Working Set
- Branch: `feature/session-auth`
- Key files: `src/auth/session.ts`, `src/middleware/auth.ts`
- Test cmd: `npm test -- --grep session`
```

<a id="additional-notes"></a>
## 补充说明

- **保持简洁**-背景事项
- **一个"现在"项目** - 注重力量，防止无序扩展
- **UNCONFIRMED 前缀** - 信号在清除后需要核实什么
- **经常更新** - Stale 分类账迅速失去价值
- **清除 > 紧凑** - 新鲜环境比退化环境强

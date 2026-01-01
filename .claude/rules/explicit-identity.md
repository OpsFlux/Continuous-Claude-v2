<a id="explicit-identity-across-boundaries"></a>
# 跨越边界的明确身份

在跨越过程或合成边界时，永远不要依赖"最新"或"当前".

<a id="pattern"></a>
## 图案

通过整个输油管传递明确的识别码。 "最近期"是一个种族条件。

<a id="do"></a>
## DO

- 过`--session-id $ID`当产卵过程
- 将 ID 存储在状态文件中以供日后关联
- 使用完整的 UUID, 而非部分匹配
- 区分不同的 ID 类型( 不要崩溃概念)

<a id="dont"></a>
## 别

- 在执行时间查询“ 最近的会议”
- 假设当前情况在等待/出现后仍将是时事
- 折叠不同的 ID 类型 :
  - `session_id`= Claude 代码会话(人体编程)
  - `root_span_id`= 大 Braintrust 任追踪(密钥)
  - `turn_span_id`= 大 Braintrust 任在会内转动

<a id="example"></a>
## 示例

```typescript
// BAD: race condition at session boundaries
spawn('analyzer', ['--learn'])  // defaults to "most recent"

// GOOD: explicit identity
spawn('analyzer', ['--learn', '--session-id', input.session_id])
```

<a id="source-sessions"></a>
## 源会话

- 1c21e6c8:定义会话 id vs root span id 区分
- 6a9f2d7a:通过明示方式确定错会归属
- a541f08a:确认的模式在会话边界上防止比赛

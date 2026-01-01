---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

<a id="test-driven-development-tdd"></a>
# 试验驱动开发(TDD)

<a id="overview"></a>
## 概览

先写出测试。 看着它失败。 写出最低密码才能通过

**核心原则：** 如果你没有看测试失败， 你不知道它是否测试正确的事情。

**审查规则的文字违反了规则的精神。**

<a id="when-to-use"></a>
## 何时使用

**总是：**
- 新特点
- 错误修正
- 正在重构
- 行为改变

**例外(请询问人类伴侣):**
- 丢弃原型
- 生成代码
- 配置文件

想着"冰冰 TDD"就这一次? 别说了 这是合理化的。

<a id="the-iron-law"></a>
## 铁法

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

在测试前写代码? 删除它。 重新开始

**无例外：**
- 别把它当作"参考"
- 不要在写测试时"适应"它
- 别看
- 删除表示删除

实施新鲜测试。 期间。

<a id="red-green-refactor"></a>
## 红色- 绿色元素

<a id="red-write-failing-test"></a>
### RED - 写入失败测试

写一个最基本的测试 显示会发生什么。

* 不错：**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
清楚的名字，测试真实的行为，一件事。

**负：**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
模糊的名称，测试模拟而不是代码。

**要求：**
- 一个行为
- 清除名称
- 真实代码( 除非不可避免 )

<a id="verify-red-watch-it-fail"></a>
### 校验 RED - 注意它失败

**人类。 永远不要跳过。**

```bash
npm test path/to/test.test.ts
# or
pytest path/to/test_file.py
```

确认：
- 测试失败( 没有出错)
- 需要失败的消息
- 失败， 因为特性缺失( 不是打字)

试卷? 你在测试现有的行为 修行验相。
测试错误? 修复错误， 重运行到失败 。

<a id="green-minimal-code"></a>
### GREEN - 最小码

写最简单的代码来通过测试。

* 不错：**
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
只要足够通过。

**负：**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI - over-engineered
}
```

不要添加特性，重构出其他代码，或者超越测试的"改进".

<a id="verify-green-watch-it-pass"></a>
### 校验绿色 - 注意它通过

页：1

```bash
npm test path/to/test.test.ts
```

确认：
- 测试合格
- 其他测试仍然通过
- 输出纯度( 无错误， 警告)

**测试失败?** 修复代码，而不是测试。
**其他测试失败?** 现在就修好

<a id="refactor-clean-up"></a>
### 更新 - 清理

仅绿后 :
- 删除重复
- 改进名称
- 提取助手

保持测试绿色。 不要增加行为。

<a id="repeat"></a>
### 重复

下一个特性的测试失败 。

<a id="common-rationalizations"></a>
## 共同合理化

| 对不起 | 现实 |
|--------|---------|
| "太简单了" | 简单的代码中断 。 测试需要 30 秒 |
| "我会测试之后" | 立即通过测试 证明什么。 |
| "在达成相同目标后进行试验" | 测试后="这是做什么的?" 测试 -第一 = "这个应该做什么?" |
| "已经手动测试" | 系统化 没有记录，不能重跑。 |
| "删除 X 小时是浪费" | 沉克花了很多钱 保持未经核实的代码是技术债务。 |
| "作为参考，先写测试" | 你会适应的 这是测试之后。 删除表示删除。 |
| "首先需要探索" | 精细。 放弃探索，从 TDD 开始。 |
| "试硬=设计不清". | 听从考证。 难以测试 = 难以使用。 |
| "TDD 会让我慢下来" | TDD 比调试快。 实用=先试。 |
| "手动测试更快" | 手动不能证明边缘情况 你会重新测试每一个变化。 |

<a id="red-flags-stop-and-start-over"></a>
## 红旗 - 停止并重新开始

- 测试前代码
- 实施后的测试
- 立即通过测试
- 无法解释为什么测试失败
- 测试添加了“ 后”
- 理顺"就这次"
- "我已经手动测试过了"
- "达到相同目的后的试验"
- “保留作为参考”或“调整现有代码”

**所有这些含义：删除代码。 从 TDD 开始**

<a id="example-bug-fix"></a>
## 示例：错误修正

页：1 接受空电子邮件

**减**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**核证 RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**绿色**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**核查绿色**
```bash
$ npm test
PASS
```

**报告员**
必要时提取多个字段的验证 。

<a id="verification-checklist"></a>
## 核查核对清单

标记工作完成前：

- [ ] 每个新功能/方法都有测试
- [ ] 在执行前观察每个测试失败
- [ ] 每个测试都因预期原因而失败( 特性缺失， 不是打字)
- [ ] 写出通过每次测试的最小代码
- [ ] 所有测试合格
- [ ] 输出纯度( 无错误， 警告)
- [ ] 测试使用真实代码( 只有在不可避免的情况下才会使用模拟)
- [ ] 覆盖的边缘案件和错误

不能检查所有的盒子? 你跳过 TDD。 重新开始

<a id="when-stuck"></a>
## 当粘住时

| 问题 | 解决方案 |
|---------|----------|
| 不知道怎么测试 | 写许愿 API. 先写断言 问问你的人类伴侣 |
| 测试太复杂 | 设计太复杂了。 简化接口。 |
| 一定把一切都嘲笑出来了 | 密码太搭配了 使用依赖性注射。 |
| 测试设置大 | 解脱助道。 还是很复杂? 简化设计。 |

<a id="final-rule"></a>
## 最后规则

```
Production code → test exists and failed first
Otherwise → not TDD
```

没有人类伙伴的许可，没有例外

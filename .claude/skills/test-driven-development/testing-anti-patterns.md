<a id="testing-anti-patterns"></a>
# 测试反跳板

**当** 写作或更改试验、增加模拟或试图在生产代码中增加仅试验方法时，便引用这一参考。

<a id="overview"></a>
## 概览

测试必须验证真实行为，而不是嘲弄行为。 雾是隔离的手段 而不是被测试的东西

**核心原则：** 测试密码是做什么的 而不是模拟的

**严格 TDD 之后防止这些反标。**

<a id="the-iron-laws"></a>
## 铁法

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

<a id="anti-pattern-1-testing-mock-behavior"></a>
## 反 Patters 1: 模拟行为测试

**违反情况：**
```typescript
// BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**为什么这样不对**
- 你正在验证模拟作品 而不是组件是否有效
- 当模拟出现时测试通过，当没有时测试失败
- {\fn 黑体。s22\bord1\shad0\3aHBE\4aH00\fscx67\fscy66\2cHFFFFFF\3cH808080}没有告诉你什么是真正的行为

**固定号：**
```typescript
// GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

<a id="gate-function"></a>
### 门功能

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

<a id="anti-pattern-2-test-only-methods-in-production"></a>
## 2. 仅限试验的生产方法

**违反情况：**
```typescript
// BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
  }
}

// In tests
afterEach(() => session.destroy());
```

**为什么这样不对**
- 仅受试验代码污染的生产类别
- 如果不小心召来生产，就很危险
- 违反《21 世纪议程》和分离关切

**固定号：**
```typescript
// GOOD: Test utilities handle test cleanup
// Session has no destroy() - it's stateless in production

// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

<a id="gate-function-1"></a>
### 门功能

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead
```

<a id="anti-pattern-3-mocking-without-understanding"></a>
## 3:无意识地嘲笑

**违反情况：**
```typescript
// BAD: Mock breaks test logic
test('detects duplicate server', () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**为什么这样不对**
- 混合方法取决于副作用测试(写入配置)
- 过度模仿"安全" 打破实际行为
- 测试通过的原因有误 或神秘失败

**固定号：**
```typescript
// GOOD: Mock at correct level
test('detects duplicate server', () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected
});
```

<a id="gate-function-2"></a>
### 门功能

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level
```

<a id="anti-pattern-4-incomplete-mocks"></a>
## 4:不完全的口袋

**违反情况：**
```typescript
// BAD: Partial mock - only fields you think you need
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};
```

**为什么这样不对**
- 部分模拟隐藏结构假设
- 下游代码可能取决于您没有包含的字段
- 测试通过但集成失败

**固定号：**
```typescript
// GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields real API returns
};
```

<a id="quick-reference"></a>
## 快速引用

| 反 | 修补 |
|--------------|-----|
| 使用模拟元素 | 测试真部件或解锁 |
| 仅限试验的生产方法 | 移动到测试公用事业 |
| 不知不觉的嘲笑 | 了解依赖性第一，嘲弄最小 |
| 不完全的模拟 | 镜像真实 API 完全 |
| 测试作为后想 | TDD - 先测试 |
| 过于复杂的模拟 | 考虑整合测试 |

<a id="red-flags"></a>
## 红旗

- 抽查检查`*-mock`测试标识
- 仅在测试文件中调用的方法
- 模拟设置为 > 50%的测试
- 删除模拟时测试失败
- 不能解释为什么需要嘲笑
- 嘲笑"为了安全"

<a id="the-bottom-line"></a>
## 底线

**弹药是隔离的工具，不是用来测试的东西。**

如果 TDD 显示你在测试模拟行为 你就错了

Fix:测试真实的行为或质疑你为什么要嘲笑。

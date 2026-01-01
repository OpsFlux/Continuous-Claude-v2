<a id="search-tool-hierarchy"></a>
# 搜索工具等级

查找代码时， 请使用此决定树 :

<a id="decision-tree"></a>
## 决定树

```
Need to understand code STRUCTURE?
  (find function calls, class usages, refactor patterns)
  → Use AST-grep (/ast-grep-find)

Need to find TEXT in code?
  → Use Morph (/morph-search) - 20x faster
  → If no Morph API key: fall back to Grep tool

Simple one-off search?
  → Use built-in Grep tool directly
```

<a id="tool-comparison"></a>
## 工具比较

| 工具 | 最佳服务 | 要求数 |
|------|----------|----------|
| **AST-grep** (中文(简体) ). | 语义模式： "找到所有呼叫`foo()`"，重构，按类型寻找用法。 | MCP 服务器 |
| 页：1 | 快速文本搜索 : “ 查找提及错误的文件 ”, grep 横跨代码库 | API 密钥 |
| **货物** | 简单图案， 无法使用墨菲时倒置 | 无(内置) |

<a id="examples"></a>
## 实例

**AST-grep**(结构):
- 找到所有还原承诺的功能
- 使用 useState 查找全部 React 组件
- "将所有 X 到 Y 的进口"

** 原文检索：
- "找到所有提到"认证"的文件"
- 搜索 TODO 评论
- "查找错误处理模式"

**Grep**(倒计时):
- 无法使用 Morph 时的简单关键字搜索
- 快速检查一些文件

<a id="codebase-analyzer-agent"></a>
# 代码库分析器代理

分析代码库实施细节。 需要特定组件的详细信息时使用。

<a id="when-to-use"></a>
## 何时使用

- 了解如何实施具体特征
- 在内部深潜
- 找到所有构成特性的部件
- 了解数据通过系统流动

<a id="capabilities"></a>
## 能力

- 读取文件
- 与 Grep/ Glob 搜索
- 列表目录
- 跟踪进口和依赖性

<a id="example-prompts"></a>
## 示例提示

```
Analyze how the authentication middleware works in this codebase
```

```
Find all the pieces involved in the checkout flow and explain how they connect
```

```
How does the caching layer work? Trace it from request to response.
```

<a id="best-practices"></a>
## 最佳做法

- 具体分析你想要什么
- 你的要求越详细 分析越好
- 这是研究用的，不是写代码用的

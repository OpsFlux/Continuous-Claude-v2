<a id="codebase-locator-agent"></a>
# 密码库定位器代理

定位与特性或任务相关的文件、目录和组件。 如超能 Grep/Glob/LS 等。

<a id="when-to-use"></a>
## 何时使用

- 查找一个特性在代码库中的位置
- 定位所有与概念相关的文件
- 查找特性的切入点
- 绘制出您需要查看的文件

<a id="capabilities"></a>
## 能力

- 图案的 Grep
- 文件图案的覆盖
- 列表目录
- 遵循命名惯例

<a id="example-prompts"></a>
## 示例提示

```
Find all files related to user authentication
```

```
Where does the API handle payment processing?
```

```
Locate the components involved in the dashboard
```

<a id="best-practices"></a>
## 最佳做法

- 用普通语言描述你要找的东西
- 提及特性或概念， 而不仅仅是文件名
- 密码库分析器前用这个进行大搜索

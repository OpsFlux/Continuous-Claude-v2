<a id="observe-before-editing"></a>
# 编辑前观察

在编辑代码来修复一个错误之前，确认系统 *实际生成的 *.

<a id="pattern"></a>
## 图案

产出不谬。 密码可能。 先检查产出。

<a id="do"></a>
## DO

1. 检查预期目录是否存在 :`ls -la .claude/cache/`
2. 检查是否创建了预期文件 :`ls -la .claude/cache/learnings/`
3. 检查日志错误 :`tail .claude/cache/*.log`
4. 手动运行失败的命令以查看实际错误
5. 只需编辑代码

<a id="dont"></a>
## 别

- 假设"hook 没有运行"而不检查输出
- 根据您所想的编辑代码
- 混淆全局对项目路径( 请选中两个路径 :`.claude/`和`~/.claude/`)

<a id="source-sessions"></a>
## 源会话

- a541f08a:在手动运行显示前，Token 限制错误是看不见的
- 6a9f2d7a:在错误的缓存路径中查找(`~/.claude/` vs `.claude/`)，假定钩关失效
- a8bd5cea:通过在项目缓存中查找输出文件确认的钩子工作
- 1c21e6c8:经验证的人工活性 通过检查 DB 文件索引存在

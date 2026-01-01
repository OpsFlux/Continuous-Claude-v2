---
description: Create git commits with user approval and no Claude attribution
---

<a id="commit-changes"></a>
# 提交更改

您的任务是为本届会议期间所作的修改创建承诺。

<a id="process"></a>
## 进程 :

1. **考虑一下情况的变化：**
   - 翻阅谈话历史，了解成就
   - 运行`git status`以查看当前变化
   - 运行`git diff`理解修改
   - 考虑修改应该是一项承诺还是多项逻辑承诺

2. **计划自己的承诺：**
   - 确定哪些文件属于一起
   - 明确、描述性承诺信息草案
   - 在承诺信息中使用必须的心情
   - 专注于为什么做出改变， 不只是什么

3. **向用户介绍你的计划：**
   - 列出您计划为每次任务添加的文件
   - 显示您要使用的承诺信件
   - 问："我计划用这些变化来创建[N]承诺。 要我继续吗?"

4. **在确认时执行：**
   - 使用`git add`带有特定文件(从未使用)`-A` or `.`)
   - 用您计划的信件创建承诺
   - 以`git log --oneline -n [number]`

5. **遗传推理(每次犯罪之后):**
   - 运行 :`bash .claude/scripts/generate-reasoning.sh <commit-hash> "<commit-message>"`
   - 这捕捉到开发过程中尝试过的东西( 构建失败， 修正)
   - 推理文件帮助未来会话理解过去的决定
   - 存储于`.git/claude/commits/<hash>/reasoning.md`

<a id="important"></a>
## 重要内容：
- **NEVER 增加共同作者信息或 Claude 归属**
- 提交书只应由用户撰写
- 不包括任何“ Generated with Claude” 消息
- 不添加“ 共同授权” 一行
- 写入信件， 如用户所写

<a id="remember"></a>
## 记住：
- 你对这届会议所做的一切有全面的了解
- 组合相关更改
- 尽可能保持重点和原子
- 用户相信你的判断 - 他们让你做
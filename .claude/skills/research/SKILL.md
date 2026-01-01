---
description: Document codebase as-is with thoughts directory for historical context
model: opus
---

<a id="research-codebase"></a>
# 研究守则库

你的任务是在整个代码库进行全面的研究，通过产出平行的子剂并合成其发现来回答用户的问题。

<a id="critical-your-only-job-is-to-document-and-explain-the-codebase-as-it-exists-today"></a>
## 你唯一的工作是记录和解释 代码基础今天
- 除非用户明确要求，否则不要建议改进或更改
- 除非用户明确要求，否则不要进行根源分析
- 除非用户明确要求，否则不要提议今后的增强
- 不批评执行情况或找出问题
- 不建议重构、优化或建筑改变
- 只描述存在、存在、运作和组件如何相互作用
- 您正在创建现有系统的技术地图/ 文档

<a id="initial-setup"></a>
## 初始设置 :

当引用此命令时， 请以 :
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

然后等待用户的研究查询。

<a id="steps-to-follow-after-receiving-the-research-query"></a>
## 收到研究查询后需采取的步骤：

1. **首先读取任何直接提到的文件：**
   - 如果用户提到特定文件(ticket、docs、JSON)，请首先读取这些文件
   - **重要**:使用无限制/抵销参数的读取工具来读取整个文件
   - **CRITICAL**:在生成任何子任务之前，请在主上下文中自行阅读这些文件
   - 这保证了您在解析研究之前有完整的背景

2. **分析和分解研究问题：**
   - 将用户的查询细分为可堆叠研究区域
   - 需要时间来超度思考用户可能寻求的基本模式、联系和建筑影响
   - 确定调查的具体组成部分、模式或概念
   - 使用 TodoWrite 创建跟踪所有子任务的研究计划
   - 考虑哪些目录、文件或建筑模式相关

3. **用于综合研究的平行次级代理任务：**
   - 创建多个任务代理以同时研究不同方面
   - 我们现在有专门的代理，他们知道如何完成具体的研究任务：

**用于编码基础研究：**
   - 使用**codebase- 定位器** 代理以查找文件和组件所在位置
   - 使用**codebase-analyzer** 代理来理解特定代码是如何起作用的(不扭曲它)
   - 使用**codebase-pattern-finder** 代理以查找现有模式的实例( 不评估它们)

**重要**:所有代理都是文献家，而不是批评家。 它们将说明存在的情况，而不建议改进或查明问题。

**思考目录：**
   - 使用**想法定位器** 代理来发现关于这个主题的文件
   - 使用**thoughts-analyzer**代理从具体文档中取出关键见解(只有最相关的文档)

**用于网络研究(仅在用户明确询问时):**
   - 使用**web-search-Research * 代理服务器获取外部文档和资源
   - 如果您使用网络研究代理，请指示他们返回 LINKS 及其发现，请 INCLUDE 在您的最后报告中提供这些链接

**线路票(如相关):**
   - 使用 **线性- ticket- reader** 代理 获取特定票的全部细节
   - 使用 **线性搜索器** 代理查找相关门票或历史背景

关键是明智地使用这些制剂：
   - 从定位代理开始查找存在的东西
   - 然后用分析剂来记录最有希望的结果
   - 在搜索不同事物时并行运行多个代理
   - 每个代理都知道自己的工作 告诉他你在找什么
   - 不要写详细的提示 关于如何搜索 - 代理已经知道
   - 提醒代理人，他们正在记录，而不是评估或改进

4. **等待所有子剂完成和综合调查结果：**
   - 重要：等待所有次级代理任务完成后再进行
   - 汇编所有子代理结果(包括代码库和想法结果)
   - 将现场的代码基础调查结果列为主要真相来源
   - 将想法/结论用作补充历史背景
   - 将调查结果连接到不同组成部分
   - 包含特定文件路径和行号以供参考
   - 校验所有的想法/路径正确(例如，对于个人文件，想法/同心/非想法/共享)
   - 突出模式、联系和建筑决定
   - 以具体证据回答用户的具体问题

5. **研究文件的大地元数据：**
   - 运行`hack/spec_metadata.sh`生成所有相关元数据的脚本
   - 文件名 :`thoughts/shared/research/YYYY-MM-DD-ENG-XXXX-description.md`
     - Format: `YYYY-MM-DD-ENG-XXXX-description.md` where:
       - YYYY-MM-DD is today's date
       - ENG-XXXX is the ticket number (omit if no ticket)
       - description is a brief kebab-case description of the research topic
     - Examples:
       - With ticket: `2025-01-08-ENG-1478-parent-child-tracking.md`
       - Without ticket: `2025-01-08-authentication-flow.md`

6. **遗传研究文件：**
   - 确保目录存在 :`mkdir -p thoughts/shared/research`
   - 使用步骤 4 所收集的元数据
   - 以 YAML 前题为文档结构， 然后是内容 :
     ```markdown
     ---
     date: [Current date and time with timezone in ISO format]
     researcher: [Researcher name from thoughts status]
     git_commit: [Current commit hash]
     branch: [Current branch name]
     repository: [Repository name]
     topic: "[User's Question/Topic]"
     tags: [research, codebase, relevant-component-names]
     status: complete
     last_updated: [Current date in YYYY-MM-DD format]
     last_updated_by: [Researcher name]
     ---

     # Research: [User's Question/Topic]

     **Date**: [Current date and time with timezone from step 4]
     **Researcher**: [Researcher name from thoughts status]
     **Git Commit**: [Current commit hash from step 4]
     **Branch**: [Current branch name from step 4]
     **Repository**: [Repository name]

     ## Research Question
     [Original user query]

     ## Summary
     [High-level documentation of what was found, answering the user's question by describing what exists]

     ## Detailed Findings

     ### [Component/Area 1]
     - Description of what exists ([file.ext:line](link))
     - How it connects to other components
     - Current implementation details (without evaluation)

     ### [Component/Area 2]
     ...

     ## Code References
     - `path/to/file.py:123` - Description of what's there
     - `another/file.ts:45-67` - Description of the code block

     ## Architecture Documentation
     [Current patterns, conventions, and design implementations found in the codebase]

     ## Historical Context (from thoughts/)
     [Relevant insights from thoughts/ directory with references]
     - `thoughts/shared/something.md` - Historical decision about X
     - `thoughts/local/notes.md` - Past exploration of Y
     Note: Paths exclude "searchable/" even if found there

     ## Related Research
     [Links to other research documents in thoughts/shared/research/]

     ## Open Questions
     [Any areas that need further investigation]
     ```

7. **Add GitHub 永久链接(如果适用):**
   - 检查主分支上是否或是否推动执行 :`git branch --show-current`和`git status`
   - 如果在主/主或推上， 生成 GitHub 永久链接 :
     - Get repo info: `gh repo view --json owner,name`
     - Create permalinks: `https://github.com/{owner}/{repo}/blob/{commit}/{file}#L{line}`
   - 将文档中的本地文件引用替换为永久链接

8. **现有调查结果：**
   - 向用户提供简要的调查结果摘要
   - 包含方便导航的密钥文件引用
   - 询问是否有后续问题或需要澄清

9. **手头的后续问题：**
   - 如果用户有后续问题，请在同一个研究文档后附加
   - 更新前题字段`last_updated`和`last_updated_by`反映最新情况
   - 添加`last_updated_note: "Added follow-up research for [brief description]"`前题
   - 增加一新节：`## Follow-up Research [timestamp]`
   - 增加调查所需的新代理
   - 继续更新文档并同步

<a id="important-notes"></a>
## 重要说明：
- 总是使用并行的任务代理，以最大限度地提高效率并尽量减少上下文的使用
- 总是运行新的代码库研究 - 永远不要完全依赖现有的研究文件
- 想法/目录提供了历史背景，以补充现场调查结果
- 专注于为开发者的参考找到具体文件路径和行号
- 研究文件应自成一体，具有所有必要背景
- 每个子代理提示应当具体，侧重于只读文件操作
- 文档跨组件连接和系统如何互动
- 包括时间背景(开展研究时)
- 尽可能链接到 GitHub 永久引用
- 保持主剂专注于合成，而不是深度文件读取
- 拥有子代理文档实例和已有的用法模式
- 探索所有的想法/ 目录， 而不仅仅是研究子目录
- **CRITICAL**:你和所有子代理都是文献学家，而不是评估员。
- ** 记得：文件是，而不是应该是什么
- **无建议**: 只描述代码库的当前状态
- **文件读取**: 总是在产入子任务前读取已提及文件 Fully( 无限制/ 抵销)
- **关键命令**: 完全按照编号步骤
  - ALWAYS 在产卵子任务(步骤 1)前先读到文件
  - 总是等待所有子剂完成后再合成( 第 4 步)
  - 总是在撰写文档前收集元数据(步骤 5 后步骤 6)
  - 从未将研究文件写入占位符值
- **部分处理**: 思考/可搜索/ 目录包含搜索的硬链接
  - 总是通过删除“ 可搜索/ ” 来记录路径 - 保存所有其他子目录
  - 正确转变的例子：
    - `thoughts/searchable/allison/old_stuff/notes.md` → `thoughts/allison/old_stuff/notes.md`
    - `thoughts/searchable/shared/prs/123.md` → `thoughts/shared/prs/123.md`
    - `thoughts/searchable/global/shared/templates.md` → `thoughts/global/shared/templates.md`
  - 永远不要将 Allison/ 更改为共享/ 或反之 - 保存精确的目录结构
  - 这将确保路径正确用于编辑和导航
- **大事一致性**:
  - 在研究文件开头总是包含前题
  - 在所有研究文件中保持前题字段的一致性
  - 添加后续研究时更新前题
  - 对多词字段名称( 如 .`last_updated`, `git_commit`)
  - 标记应与研究专题和研究的组成部分相关

<a id="repoprompt-mcp-tools"></a>
# RepoPrompt MCP 工具

用于 RepoPrompt 的 MCP 服务器的自动生成包装。

<a id="tools"></a>
## 工具

- `manage_workspaces`: 管理跨 RepoPrompt 窗口的工作空间。

操作：
• 列表 — 返回所有已知的工作空间( id, name, repoPaths, 显示窗口 ID)
• 切换 — 将窗口切换到指定的工作空间
• 创建 - 创建一个新的工作空间( 需要用户批准)
• 删除 - 删除工作空间(需要用户批准)
• 添加 文件夹 – 在工作空间添加文件夹( 需要用户批准)
• 删除 文件夹 – 从工作区删除文件夹( 需要用户批准)
• 列表 tabs – 列表中为窗口中的活动工作空间
• 选择 tab – 将此 MCP 连接绑入特定 Composer 标签

参数：
- 动作："List""switch""create""delete""add folder"" remove-folder"""list tabs""|""select tab"(需要)
- 工作空间 : 字符串( 需要“ 切换” 、 “ 删除” 、 “ 添加” 、 “ 移动” 、 UUID 或名称)
- 名称：字符串(“ 创建” 需要; 新工作空间名称)
- 文件夹  path: 字符串( 需要“ add  polders ” 、“ remove  polders ” ; 绝对路径)
- 选项卡：字符串(需要“ 选择  tab; UUID 或名称”)
- 窗口 id:整数(可选;目标窗口、选定窗口或唯一窗口的默认值)
- 焦点：布尔( 选择“ select  tab; 默认虚假)

对于"switch"，提供单个"工作空间"值。 如果它被解析为 UUID，则该工作空间被 ID 所选择;否则它被作为名称处理并使用第一个匹配。

在选择窗口( 通过选择 window) 后， 使用列表  tabs 并选择 tab 来将您的连接绑定在特定的 Composer 标签上 。 这确保了工具在一致上下文上运行，即使用户更改了 UI 中的活动标签。

标签绑定行为 :
• 如果没有标签绑定，工具使用用户当前活动的标签。 如果用户在您的操作中切换分页， 这会造成不一致的结果 。
· 使用 select tab 来明确绑定一个特定的选项卡，用于在多个工具呼叫中可预见，稳定的上下文。
• 或者，通过隐藏的' tabID'参数，并使用任何工具调用来约束飞行。

输出旗：
• [活 = 该窗口当前可见的 UI 标签
• [约束]= 此 MCP 连接的标签被绑定; 即使用户切换可见标签， 您的工具调用此标签

ImportANT:"焦点"参数切换 UI 中可见的分页，可能会干扰用户的工作流程。 只有用户明确要求查看或切换到特定分页时设置焦点=校正。 对于背景操作，省略焦点或设置为虚假。
- `manage_selection`: 管理所有工具所用的当前选择。

操作：获得 | 添加 | 删除 | 设定 | 清除 | 预览 | 促进 | 降职
选项 :
• view="摘要"|"档案"|"内容"(默认"摘要")
• path display="相接" QQ"相接"(默认"相接")
• 严格=refalse (default false) — 如果一个变异解决了无路径， 返回一个有帮助的错误; 设置假为无
• 模式="满"|"切开"|"codemap  only"(默认"完整"):
  - "完整":完整文件内容
  - "切片":仅特定行距
  - “ 代码映射  只” : 用于符号保存的高效 API 结构( 函数/ 类型签名)
  - 没有可用代码映射的文件，在以代码映射模式瞄准文件夹或路径时会跳出并报告为"代码映射不可用".

自动代码映射管理 :
• 在选择模式=“完整”或“切片”(通过 op=add 或 op=set)的文件时，为相关/依赖性文件自动添加编码图
• 用 op=“get”视图=“文件”检查完整的选择(包括自动编码图)
• 手动代码映射操作(mode="codemap  only"，促进，降级) 禁用自动管理，直到您清除为止
• 优先进行自动管理;只有在需要精确控制时才进行手工管理

op=set 语义(模式控制行为):
• 模式="完整":清除选择，取而代之的是所提供路径/切片(完全重置)
• mode= “ slices” : 文件扫描 - 添加任何路径而不清除， 只替换指定文件的切片定义
• 模式=“只有代码映射” : 替换只使用代码映射的文件， 禁用自动管理

路径处理 :
• 路径可以是文件或目录(目录扩展至所有内部文件，递归)
• 路径可以是相对的(对工作空间根)或绝对的
• 单根工作空间： "src/main.swift"或"root/src/main.swift"两种工作
用于多根工作空间：有根名的前缀(如"ProjectA/src/main.swift").
• 默认启用模糊匹配 - 关闭匹配将得到解决

指导：
• 在切片前读取已读取的文件，以识别相关章节
• 使用说明范围以明确(别名：说明/说明/标签)
• 预览 op=“ 预览” 视图=“ 文件” 以查看完整的选择( 包括自动编码图) 和符号计数后再执行

实例：
• 添加完整文件 {'op':"add""paths": [" Root/src/main.swift"]
^ 添加代码映射： {"op":"add""paths":["root/src/utils/helper.swift"],"mode":"codemap 只"]
• 设定切片(文件扫描器):{"op":"set","mode":"slices","slices": [{"path":"root/src/file.swift","ranges": [{"start line":45"end line":120","description":"用户认证流"}}}
• 添加/相接切片：{"op":"add","slices": [{"path":"root/src/file.swift","ranes": [{"start line":200"end line"::250}}}}}}
• 推广编码图-完整：{'op':"促进""路径": [" Root/src/utils/helper.swift"]]
• Demote full- codemap: {"op":"demote""路径":[" Root/src/utils/helper.swift"]]

相关 :
• 发现候选人：获取 file tree, file 搜索
• 预览结构快：获得 代码 结构
• 快照一切：工作空间-背景
• 应用更改：应用编辑器
• 聊天：聊天站(有聊天的列表/日志)
- `file_actions`: 创建、删除或移动文件。

操作：
- `create`: 用`content`启用`if_exists="overwrite"`以替换已有文件。 选择中添加了新文件 。
- `delete`: 删除一个文件(安全需要绝对路径).
- `move`: 移动/重命名到`new_path`(如果目的地存在，则失败).

路径：相对或绝对(`delete`要求绝对)。 当多根被加载时，在创建文件时必须提供绝对路径;相对路径被拒绝以避免模糊。
选项 :`if_exists`(创建):"错误"(默认)或"覆盖".

注意：支持多根文件创建。 缺少的中间文件夹会自动创建 。
- `get_code_structure`: 文件和目录的返回代码结构(codemaps).

范围：
- `scope="selected"`— **当前选择的结构** (也列出没有编码图的文件)
- `scope="paths"`(默认)——通过`paths`(文件和/或目录;目录为递归式)

注：使用方式为：`get_file_tree`和`search`在选择前进行探索。
- `get_file_tree`: ASCII 项目目录树。

类型 :
- `files`— 模式：
	- `auto` (default): tries full tree, then trims depth to fit ~10k tokens
	- `full`: all files/folders (can be very large)
	- `folders`: directories only
	- `selected`: only selected files and their parents
	Optional: `path` to start from a specific folder; `max_depth` to limit (root=0).
- `roots`——列出根文件夹。

带有编码图的文件被标记`+`在标准树上。
- `read_file`:读取文件内容，可选择指定起行和行数。

细节 :
- 基于 1 的行; 没有参数 – 整个文件
- `start_line`> 0: 从该行开始( 如 10)
- `start_line`< 0: 上行 N( 如`tail -n`)
- `limit`: 只有正数`start_line`(例如，起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起起
- `file_search`:通过文件路径和/或文件内容来搜索。

默认
- regex= truth (默认的正则表达式)
- 不区分大小写
- 空格匹配柔性白空格
- 结果使用基于 1 的行号
- 最大结果默认值： 50( 如果需要， 请求会更高)

答复上限
- 返回的有效载荷被封为~50k 字符。
- 当帽子被击中时，我们排除了全部结果(从未切出一行)，并报告在回应中"odicent"下省略了多少。

参数
- 模式(需要)
- regex: 真伪
- 模式 : “ 自动” QQ“ 路径” QQ“ 内容” QQ“ 两者” (默认“ 自动”)
- 过滤器 : { 扩展、 排除、 路径}
- 最大结果、 仅计数、 上下文、 整词

参数化名(用于相容性)
- `-C`:用于上下文行的别名(例如，`-C: 5`与`context_lines: 5`)
- `path`:用于单文件搜索的快手(例如，`path: "file.swift"`与`filter: {paths: ["file.swift"]}`)

文体模式( R)`regex=false`)
- 特殊字符字面匹配; 不需要逃跑

Regex 模式 (`regex=true`)
- 全正则表达式( 组、 外观、 锚)`^`/`$`); `whole_word`添加字词边界

路径搜索
- regex=虚假 :`*`和`?`通配符( 跨文件夹匹配)
- regex=真： 相对路径的完整 regex

实例
- 字形： {"pattern":"frame(minWidth:)","regex":"false"
- Regex: {"pattern":"frame\(minWidth:)","regex": true} (中文(简体) ).
- OR: {'pattern':"performSearch'search Users","regex": true} 存档副本 存档副本 存档副本 存档副本 存档副本 存档副本 存档副本
- 路径： {'pattern':"*. swift","mode":"path"]
- `workspace_context`: 此窗口工作空间的快照： 迅速， 选择， 代码结构( 编码图) 。 较大的部件是选入。
默认包括：即时，选择，代码，符号。
包括： ["即时","选","代码","文件","树","托克"]
路径 播放："相对"""""""满"

相關： 管理  选择( 精确选择) , 及时( 编辑指令) , 获取  file  tree, 文件  搜索， 获取  代码  结构， 应用  编辑器， 聊天  发送， 聊天。
- `prompt`: 获取或修改共享快取(指令/注). 操作： 获得 QQ 设定 QQ 附件 清空

相關： 工作空間  context (snapshot), 管理 selection (files), 聊天  send (用快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取快取
- `apply_edits`: 应用直接文件编辑(重写或搜索/替换).

实例：

单人替换 :
`{"path": "file.swift", "search": "oldCode", "replace": "newCode", "all": true}`

多个编辑 :
`{"path": "file.swift", "edits": [{"search": "old1", "replace": "new1"}, {"search": "old2", "replace": "new2"}]}`

重写整个文件 :
`{"path": "file.swift", "rewrite": "complete file content...", "on_missing": "create"}`

注意： 当创建新文件( 例如， 使用`on_missing="create"`))，而多根被加载，则必须在加载根内提供绝对路径;相对路径被拒绝来避免模糊。 缺少的中间文件夹会自动创建 。

选项 :`verbose`(显示 diff)`on_missing`(为重写："error" QQ"创造").
- `list_models`: 列出可用的模型预设(id，名称，描述，支持的模式).
使用时间`chat_send`选择合适的预设。
如果没有预设，请显示当前聊天模式。 无`model`, `chat_send`选择第一个兼容的预设。
- `chat_send`: 开始新的聊天或继续现有的谈话。 模式 :`chat` | `plan` | `edit`.

**建议的对接程序环**
1)**计划**(`mode="plan"`:请求架构/步骤或请求复核。
(2) **应用**:使用`apply_edits` (or `chat_send`与`mode="edit"`)来作取变。
3)**审查**(`mode="chat"` or `plan`:获得第二个意见;精炼。
4) **重复**同声聊天**.

**关键背景卫生**
- 运行`manage_selection` op=`get`(view="files")以确认上下文和符号。
- 偏爱`set` (or `add`/`remove`因此，所有**相关文件** 都包括在内。
- 完整快照( 即时、 选择、 代码、 符号; 可选的文件文本/ 树), 调用`workspace_context`.
- 偏执于**更多的上下文 而非太少**;避免只选择一个引用其它文件的文件 。

**会议管理**
- `new_chat`: 真实开始; 否则继续最近的( 或通过)`chat_id`)
- `selected_paths`: 替换此信件的选择
- `chat_name`:可选但**高度推荐** — 简短，描述性(例如"Fix 登录崩溃- 认证流")
- `model`: 预设代号/名称; 调用`list_models`第一个

**限制**
- 没有命令/测试; 只看到 **选中的文件** + 对话历史
- 对于 **snapshot 上下文** (即时、 选择、 编码图、 可选的文件内容/ 树), 调用`workspace_context`
	(add `"files"` in `include` to embed file text). For targeted slices, use `read_file` or `file_search`.
- 聊天没有跟踪 diff 历史; 它只看到当前文件状态
- `chats`: 列出聊天或查看聊天历史。 动作： 列表 QQ 日志

`list`: 最近的聊天( ID、 名称、 选定文件、 最后一个活动) – 使用 ID 与`chat_send`
`log`: 完整对话历史( 可选包括 diffs)

注释：
- 每个聊天都维持自己的选择和上下文;继续恢复状态
- `chat_send`无`chat_id`默认恢复最近的
- 您可以在任何时间以通过的方式重命名一个会话`chat_name` in `chat_send`
关联： 聊天  send, 工作空间  文本
- `context_builder`:通过智能地探索代码库并构建最佳文件上下文来启动任务。

理想为**复杂任务的第一步**:代理映射相关代码，选择文件
在象征性的预算范围内，并可以一试产生执行计划。 结果
聊天线程对于后续问题，任务中段的澄清，或获得第二段是完美的。
认为你的工作。

**数字：**
- 使用响应 类型="计划"来获取与上下文并列的实施计划，或稍后通过聊天-发送生成一个实施计划
- 以返回的聊天  id 继续聊天  发送
- 当新区域开始相关时， 将文件添加到选中的 manage  setch 中
- 随时再次运行上下文  构建器以探索代码库的不同区域

参数：
- 指令： 描述您想要完成的任务
- 响应 类型 : “ plan” 生成实施计划; “ problem” 解答代码库; 省略仅用于上下文

返回文件选择、 即时和状态 。 在响应 类型="计划"或"问题"中，也返回
回应和聊天 id 用于无缝后续对话。

注意：根据代码库大小和任务复杂程度，彻底探索需要 30s-5min.

<a id="usage"></a>
## 使用量

```python
from servers.repoprompt import manage_workspaces

# Use the tool
result = await manage_workspaces(params)
```

**说明**: 此文件是自动生成的 。 不手工编辑。

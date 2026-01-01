---
description: Generate comprehensive PR descriptions following repository templates
---

<a id="generate-pr-description"></a>
# 生成 PR 描述

您的任务是按照仓库的标准模板生成一个全面的拉动请求描述 。

<a id="steps-to-follow"></a>
## 需采取的步骤：

1. **读取公关说明模板：**
   - 首先，检查是否`thoughts/shared/pr_description.md`已存在
   - 如果不存在，请告知用户他们需要创建 PR 描述模板。`thoughts/shared/pr_description.md`
   - 仔细阅读模板以了解所有章节和要求


2. **确定公关说明：**
   - 检查当前分支是否有关联的 PR :`gh pr view --json url,number,title,state 2>/dev/null`
   - 如果当前分支不存在 PR, 或者如果主/主上， 请列出打开的 PR :`gh pr list --limit 10 --json number,title,headRefName,author`
   - 询问用户要描述哪个 PR

3. **检查现有说明：**
   - 检查是否`thoughts/shared/prs/{number}_description.md`已经存在
   - 如果存在，请读取并告知用户您将会更新
   - 考虑一下自上次描述书写以来的变化

4. **全球综合公关信息：**
   - 获得完整的 PR diff:`gh pr diff {number}`
   - 如果您获得关于没有默认远程寄存器的错误， 请指示用户运行`gh repo set-default`选择合适的仓库
   - 获取承诺历史 :`gh pr view {number} --json commits`
   - 审查基础分支：`gh pr view {number} --json baseRefName`
   - 获取 PR 元数据 :`gh pr view {number} --json url,title,number,state`

4b. **Gather 推理史(如果有的话):**
   - 检查推理文件是否存在 :`ls .git/claude/commits/*/reasoning.md 2>/dev/null`
   - 如果它们存在，则加以汇总：`bash .claude/scripts/aggregate-reasoning.sh main`
   - 这表明在最终解决方案之前曾尝试过何种方法
   - 将输出保存到 PR 描述中

5. **彻底分析这些变化：**(对代码变化、其建筑影响和潜在影响进行超度思考)
   - 仔细读取整个 diff
   - 上下文中，读取任何引用但未在 diff 中显示的文件
   - 了解每个变化的目的和影响
   - 确定与用户相适应的变化与内部执行细节
   - 寻找打破变化或迁移要求

6. **手头核查要求：**
   - 查找模板“ 如何验证” 部分中的任何清单项目
   - 对于每个核查步骤：
     - If it's a command you can run (like `make check test`, `npm test`, etc.), run it
     - If it passes, mark the checkbox as checked: `- [x]`
     - If it fails, keep it unchecked and note what failed: `- [ ]` with explanation
     - If it requires manual testing (UI interactions, external services), leave unchecked and note for user
   - 记录任何无法完成的核查步骤

7. **说明：**
   - 从模板中完整填写每个部分：
     - Answer each question/section based on your analysis
     - Be specific about problems solved and changes made
     - Focus on user impact where relevant
     - Include technical details in appropriate sections
     - Write a concise changelog entry
   - **如果找到推理文件(从步骤 4b):**
     - Add an "## Approaches Tried" section before "## How to verify it"
     - Include the aggregated reasoning showing failed attempts and what was learned
     - This helps reviewers understand the journey, not just the destination
   - 确保所有清单项目都得到处理(核对或解释)

8. **省去说明：**
   - 将已完成的描述写入`thoughts/shared/prs/{number}_description.md`
   - 显示用户生成的描述

9. **更新公关：**
   - 直接更新 PR 描述 :`gh pr edit {number} --body-file thoughts/shared/prs/{number}_description.md`
   - 确认更新成功
   - 如果任何核查步骤仍然不受限制，请提醒用户在合并前完成这些步骤

<a id="important-notes"></a>
## 重要说明：
- 此命令贯穿不同的寄存器 - 总是读取本地模板
- 全面但简洁----说明应可扫描
- 专注于"为什么"和"什么"
- 突出包括任何断裂变化或迁移说明
- 如果 PR 触及多个组件， 请按此组织描述
- 尽可能总是尝试运行校验命令
- 明确说明哪些核查步骤需要人工测试

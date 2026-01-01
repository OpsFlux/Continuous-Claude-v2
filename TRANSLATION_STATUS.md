# 文档翻译状态

- 翻译范围：当前目录及子目录中的文档文件（默认扩展名：`.md`, `.txt`, `.rst`, `.adoc`；自动排除 `.git/`、`node_modules/`、`.venv/` 等）
- 最近一次执行：2026-01-01
- 状态：已完成
- 覆盖文件数：81（另：`LICENSE` 追加了中文参考译文）

## 翻译规则

1. 保留 Markdown 结构（标题、列表、表格、引用等）
2. 代码块不翻译（``` fenced code 或缩进代码）
3. 保留 URL、邮箱、路径、行内代码（`...`）
4. 为保持 Markdown 内部锚点稳定，会在标题前插入 `<a id="..."></a>`
5. 二次润色：统一关键术语/产品名（例如 Claude、Claude Code、RepoPrompt、Braintrust、Hook/Hooks）

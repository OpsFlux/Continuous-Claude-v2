# 文档翻译指南

本仓库提供一个离线批量翻译脚本，用于将仓库内的文档翻译成中文并直接覆盖原文件。

## 使用方式（推荐：离线）

1. 创建虚拟环境并安装 Argos Translate（一次性）：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install argostranslate aiohttp
```

2. 安装英文→中文语言包（一次性）：

```bash
.venv/bin/python - <<'PY'
import argostranslate.package
argostranslate.package.update_package_index()
pkg = next(p for p in argostranslate.package.get_available_packages() if p.from_code == "en" and p.to_code == "zh")
path = pkg.download()
argostranslate.package.install_from_path(path)
print("installed:", path)
PY
```

3. 预览将要处理的文件：

```bash
.venv/bin/python scripts/translate_documents.py --dry-run
```

4. 执行翻译（覆盖原文件）：

```bash
.venv/bin/python scripts/translate_documents.py --provider argos --yes
```

5. 二次润色（术语统一/轻量排版）：

```bash
python3 scripts/polish_cn_docs.py --yes
```

## 翻译范围与规则

- 默认扩展名：`.md`, `.txt`, `.rst`, `.adoc`
- 自动排除目录：`.git/`、`node_modules/`、`.venv/`、`dist/`、`build/` 等
- 保留：代码块（``` 或缩进）、URL/邮箱/路径、行内代码（`...`）
- Markdown：翻译链接文本但保留链接目标；为保持锚点稳定，会在标题前插入 `<a id="..."></a>`

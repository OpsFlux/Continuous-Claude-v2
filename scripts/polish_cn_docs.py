#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, Tuple

SUPPORTED_EXTENSIONS = {".md", ".txt", ".rst", ".adoc"}
EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    ".mypy_cache",
    ".tox",
}

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_INLINE_CODE_SPLIT_RE = re.compile(r"(`[^`]*`)")
_MD_INLINE_LINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\n]+)\)")
_MD_REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+\S+")
_MD_HEADING_RE = re.compile(r"^(#{1,6})(\s+)(.+)$")
_MD_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")


def find_documents(root_dir: Path, extensions: set[str] | None = None) -> List[Path]:
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS

    docs: List[Path] = []
    for file_path in root_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if any(excluded in file_path.parts for excluded in EXCLUDED_DIRS):
            continue
        if file_path.suffix.lower() in extensions:
            docs.append(file_path)
    return sorted(docs)


def split_yaml_frontmatter(lines: List[str]) -> Tuple[List[str], List[str]]:
    if not lines or lines[0].strip() != "---":
        return [], lines
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            return lines[: i + 1], lines[i + 1 :]
    return [], lines


def has_cjk(text: str) -> bool:
    return bool(_CJK_RE.search(text))


def normalize_spacing(text: str) -> str:
    # Insert spaces between CJK and ASCII letters/digits where they touch.
    text = re.sub(r"([\u4e00-\u9fff])([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])([\u4e00-\u9fff])", r"\1 \2", text)
    return text


def normalize_punctuation(text: str) -> str:
    if not has_cjk(text):
        return text
    # Only normalize a few safe ASCII punctuations inside Chinese prose.
    text = re.sub(r"([\u4e00-\u9fff]),", r"\1，", text)
    text = re.sub(r",([\u4e00-\u9fff])", r"，\1", text)
    text = re.sub(r"([\u4e00-\u9fff])\.", r"\1。", text)
    text = re.sub(r"([\u4e00-\u9fff]):", r"\1：", text)
    return text


def build_replacements() -> List[tuple[re.Pattern[str], str]]:
    # Order matters: do specific product-name fixes before generic ones.
    rules: List[tuple[str, str]] = [
        (r"克洛德代码", "Claude Code"),
        (r"克劳德代码", "Claude Code"),
        (r"克洛德\s*Code", "Claude Code"),
        (r"克劳德\s*Code", "Claude Code"),
        (r"克洛德特工SDK", "Claude Agent SDK"),
        (r"克劳德特工SDK", "Claude Agent SDK"),
        (r"特工SDK", "Agent SDK"),
        (r"代理SDK", "Agent SDK"),
        (r"虎克们", "Hooks"),
        (r"虎克", "Hook"),
        (r"重新流行", "RepoPrompt"),
        (r"再流行", "RepoPrompt"),
        (r"人才信任会议", "Braintrust 会话"),
        (r"人才信任会", "Braintrust 会话"),
        (r"人才信任", "Braintrust"),
        (r"脑信托", "Braintrust"),
        (r"脑信会", "Braintrust"),
        (r"脑信", "Braintrust"),
        (r"Artiffact", "Artifact"),
        (r"艺术索引", "制品索引（Artifact Index）"),
        (r"理由历史", "推理历史"),
        (r"障碍射击", "故障排除"),
        (r"标语效率高的", "高 token 效率的"),
        (r"全球安装", "全局安装"),
        (r"作曲标签", "Composer 标签"),
        (r"活性标签", "活动标签"),
        (r"特工们", "代理"),
        (r"特工人员", "代理"),
        (r"特工", "代理"),
        (r"克洛德", "Claude"),
        (r"克劳德", "Claude"),
    ]

    compiled: List[tuple[re.Pattern[str], str]] = []
    for pat, repl in rules:
        compiled.append((re.compile(pat), repl))
    return compiled


def apply_replacements(text: str, replacements: List[tuple[re.Pattern[str], str]]) -> str:
    for pattern, repl in replacements:
        text = pattern.sub(repl, text)
    return text


def polish_text_segment(text: str, replacements: List[tuple[re.Pattern[str], str]]) -> str:
    text = apply_replacements(text, replacements)
    text = normalize_spacing(text)
    text = normalize_punctuation(text)
    return text


def polish_markdown_line(line: str, replacements: List[tuple[re.Pattern[str], str]]) -> str:
    if _MD_REF_DEF_RE.match(line):
        return line
    # Keep injected HTML anchors as-is.
    if line.lstrip().startswith("<a ") and "id=" in line:
        return line

    # Headings: prefer "架构" over "建筑" in architecture contexts.
    m = _MD_HEADING_RE.match(line)
    if m:
        heading = m.group(3)
        if heading.startswith("建筑"):
            heading = "架构" + heading[len("建筑") :]
            line = f"{m.group(1)}{m.group(2)}{heading}"

    # Common labels
    if line.startswith("行动:"):
        line = "操作：" + line[len("行动:") :]

    def polish_outside_inline_code(text: str) -> str:
        parts = _INLINE_CODE_SPLIT_RE.split(text)
        out: List[str] = []
        for part in parts:
            if not part:
                continue
            if part.startswith("`") and part.endswith("`"):
                out.append(part)
            else:
                segment = polish_text_segment(part, replacements)

                def normalize_bold(mb: re.Match[str]) -> str:
                    inner = mb.group(1).strip()
                    inner = normalize_punctuation(inner)
                    return f"**{inner}**"

                segment = _MD_BOLD_RE.sub(normalize_bold, segment)
                out.append(segment)
        return "".join(out)

    out: List[str] = []
    pos = 0
    for m in _MD_INLINE_LINK_RE.finditer(line):
        before = line[pos : m.start()]
        if before:
            out.append(polish_outside_inline_code(before))
        label = m.group(1)
        dest = m.group(2)
        out.append(f"[{polish_outside_inline_code(label)}]({dest})")
        pos = m.end()
    tail = line[pos:]
    if tail:
        out.append(polish_outside_inline_code(tail))
    return "".join(out)


def iter_polished_lines(path: Path, replacements: List[tuple[re.Pattern[str], str]]) -> Iterable[str]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    lines = raw.splitlines()

    frontmatter: List[str] = []
    rest = lines
    if path.suffix.lower() == ".md":
        frontmatter, rest = split_yaml_frontmatter(lines)

    for line in frontmatter:
        yield line

    in_fence = False
    fence_marker = ""

    for line in rest:
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                if fence_marker == marker:
                    in_fence = False
                    fence_marker = ""
            yield line
            continue

        if in_fence:
            yield line
            continue

        # indented code block
        if line.startswith("\t") or line.startswith("    "):
            yield line
            continue

        yield polish_markdown_line(line, replacements)

    if raw.endswith("\n"):
        # Preserve trailing newline for callers that join with '\n'
        yield ""


def main() -> None:
    parser = argparse.ArgumentParser(description="对已翻译中文文档做术语统一/轻量润色（覆盖原文件）")
    parser.add_argument("--dir", default=".", help="根目录（默认当前目录）")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不写入")
    parser.add_argument("--yes", action="store_true", help="跳过确认")
    args = parser.parse_args()

    root = Path(args.dir)
    docs = find_documents(root)

    if args.dry_run:
        print("🔍 预览模式 - 将处理以下文件：")
        for p in docs:
            print(f"  - {p}")
        return

    if not args.yes:
        resp = input(f"⚠️  将对 {len(docs)} 个文件做术语统一并覆盖原文件，是否继续？[y/N]: ")
        if resp.lower() != "y":
            print("❌ 已取消")
            return

    replacements = build_replacements()

    changed = 0
    for i, path in enumerate(docs, 1):
        # Skip LICENSE: keep legal English untouched (it has its own bilingual section already).
        if path.name == "LICENSE":
            continue

        original = path.read_text(encoding="utf-8", errors="ignore")
        polished = "\n".join(iter_polished_lines(path, replacements))
        if polished == original:
            continue
        path.write_text(polished, encoding="utf-8")
        changed += 1
        print(f"[{i}/{len(docs)}] ✓ {path}")

    print(f"✓ 完成：修改 {changed} 个文件")


if __name__ == "__main__":
    main()

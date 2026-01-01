#!/usr/bin/env python3
"""
批量翻译文档脚本 (Bulk Document Translation Script)

将指定目录下的文档批量翻译成中文，并替换原文件。
默认使用 MyMemory 免费翻译接口（单次请求文本长度上限 500 字符），脚本会自动分段与重试。

目标：
- 保留 Markdown / 纯文本的结构与格式
- 不翻译代码块（``` fenced code 或缩进代码）
- 不翻译 YAML frontmatter（Markdown 顶部 --- ... ---）
- 尽量保留 URL / 邮箱 / 路径 / 行内代码（`...`）

使用方法 (Usage):
    python3 scripts/translate_documents.py --dry-run
    python3 scripts/translate_documents.py --yes

可选：LibreTranslate（如你有 API key）
    export LIBRETRANSLATE_URL='https://your-instance/translate'
    export LIBRETRANSLATE_API_KEY='...'
    python3 scripts/translate_documents.py --provider libretranslate --yes
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp
import html
import re

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {'.md', '.txt', '.rst', '.adoc'}

# 需要排除的目录
EXCLUDED_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '__pycache__',
    '.pytest_cache', 'dist', 'build', '.mypy_cache', '.tox'
}


def find_documents(root_dir: Path, extensions: set = None) -> List[Path]:
    """
    递归查找所有文档文件
    Recursively find all document files
    """
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS

    documents = []
    for file_path in root_dir.rglob('*'):
        # 跳过排除的目录
        if any(excluded in file_path.parts for excluded in EXCLUDED_DIRS):
            continue

        # 检查文件扩展名
        if file_path.suffix.lower() in extensions and file_path.is_file():
            documents.append(file_path)

    return sorted(documents)


_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_URL_RE = re.compile(r"https?://[^\s)\]>}]+")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_MD_HEADING_RE = re.compile(r"^(#{1,6})(\s+)(.+)$")
_MD_LIST_RE = re.compile(r"^(\s*)([-*+]|(\d+\.))(\s+)(.+)$")
_MD_QUOTE_RE = re.compile(r"^(\s*(?:>\s*)+)(.+)$")
_MD_INLINE_LINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\n]+)\)")
_PRESERVE_SPAN_RE = re.compile(
    r"(`[^`]+`|https?://[^\s)\]>}]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|(?<!\w)(?:\./|\.\./|/)[A-Za-z0-9._~/-]+)"
)


def _count_latin_letters(text: str) -> int:
    return sum(1 for ch in text if ("A" <= ch <= "Z") or ("a" <= ch <= "z"))


def _count_cjk(text: str) -> int:
    return len(_CJK_RE.findall(text))


def _should_translate_snippet(text: str) -> bool:
    if not text.strip():
        return False
    latin = _count_latin_letters(text)
    if latin < 3:
        return False
    cjk = _count_cjk(text)
    # 已经是明显中文为主时，避免“中文->中文”导致措辞漂移
    if cjk > 0 and cjk > latin * 2:
        return False
    return True


def _split_yaml_frontmatter(lines: List[str]) -> Tuple[List[str], List[str]]:
    if not lines or lines[0].strip() != "---":
        return [], lines
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            return lines[: i + 1], lines[i + 1 :]
    return [], lines


async def _translate_plain_text(translator: Translator, text: str, max_chars: int) -> str:
    """
    翻译纯文本片段，保留行内代码/URL/邮箱/路径等不可翻译片段。
    """
    if not text:
        return text

    parts: List[str] = []
    pos = 0
    for m in _PRESERVE_SPAN_RE.finditer(text):
        pre = text[pos : m.start()]
        if pre:
            parts.append(pre)
        parts.append(m.group(0))
        pos = m.end()
    tail = text[pos:]
    if tail:
        parts.append(tail)

    out: List[str] = []
    for part in parts:
        if not part:
            continue
        if _PRESERVE_SPAN_RE.fullmatch(part):
            out.append(part)
            continue
        if not _should_translate_snippet(part):
            out.append(part)
            continue
        for chunk in _chunk_text(part, max_chars=max_chars):
            if _should_translate_snippet(chunk):
                out.append(await translator.translate(chunk))
            else:
                out.append(chunk)
    return "".join(out)


async def _translate_markdown_inline(translator: Translator, text: str, max_chars: int) -> str:
    """
    针对 Markdown 行内链接的翻译：翻译 [label]，保留 (dest) 原样。
    """
    if not text:
        return text
    out: List[str] = []
    pos = 0
    for m in _MD_INLINE_LINK_RE.finditer(text):
        before = text[pos : m.start()]
        if before:
            out.append(await _translate_plain_text(translator, before, max_chars=max_chars))
        label = m.group(1)
        dest = m.group(2)
        translated_label = await _translate_plain_text(translator, label, max_chars=max_chars)
        out.append(f"[{translated_label}]({dest})")
        pos = m.end()
    tail = text[pos:]
    if tail:
        out.append(await _translate_plain_text(translator, tail, max_chars=max_chars))
    return "".join(out)


def _chunk_text(text: str, max_chars: int) -> List[str]:
    """
    将文本分成 <= max_chars 的片段，尽量在空白处分割。
    """
    if len(text) <= max_chars:
        return [text]

    parts: List[str] = []
    current = ""
    for piece in re.split(r"(\s+)", text):
        if not piece:
            continue
        if len(current) + len(piece) > max_chars and current.strip():
            parts.append(current)
            current = piece
        else:
            current += piece
    if current:
        parts.append(current)
    return parts


class Translator:
    async def translate(self, text: str) -> str:
        raise NotImplementedError


class MyMemoryTranslator(Translator):
    """
    免费接口（500 chars 限制）：https://api.mymemory.translated.net/
    """

    def __init__(self, session: aiohttp.ClientSession, *, source: str, target: str) -> None:
        self._session = session
        self._source = source
        self._target = target
        self._cache: Dict[str, str] = {}

    async def translate(self, text: str) -> str:
        if text in self._cache:
            return self._cache[text]

        params = {"q": text, "langpair": f"{self._source}|{self._target}"}

        # 轻微节流，避免被限速
        await asyncio.sleep(0.1)

        for attempt in range(6):
            try:
                async with self._session.get(
                    "https://api.mymemory.translated.net/get",
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    data = await resp.json()
                    translated = (
                        data.get("responseData", {}).get("translatedText")
                        if isinstance(data, dict)
                        else None
                    )
                    if not translated:
                        raise RuntimeError(f"unexpected response: {data}")
                    if "QUERY LENGTH LIMIT EXCEEDED" in translated:
                        raise ValueError("query length limit exceeded")
                    if "MYMEMORY WARNING" in translated or "AVAILABLE FREE TRANSLATIONS" in translated:
                        raise RuntimeError("mymemory quota exhausted")

                    translated = html.unescape(translated)
                    self._cache[text] = translated
                    return translated
            except ValueError:
                raise
            except Exception:
                await asyncio.sleep(0.5 * (2**attempt))

        return text


class LibreTranslateTranslator(Translator):
    def __init__(self, session: aiohttp.ClientSession, *, api_url: str, api_key: str, source: str, target: str):
        self._session = session
        self._api_url = api_url
        self._api_key = api_key
        self._source = source
        self._target = target
        self._cache: Dict[str, str] = {}

    async def translate(self, text: str) -> str:
        if text in self._cache:
            return self._cache[text]

        payload = {"q": text, "source": self._source, "target": self._target, "format": "text"}
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        for attempt in range(6):
            try:
                async with self._session.post(
                    self._api_url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    data = await resp.json()
                    translated = data.get("translatedText")
                    if not translated:
                        raise RuntimeError(f"unexpected response: {data}")
                    self._cache[text] = translated
                    return translated
            except Exception:
                await asyncio.sleep(0.5 * (2**attempt))

        return text


class ArgosTranslator(Translator):
    """
    Argos Translate：离线翻译（需要预先安装 en->zh 语言包）。
    """

    def __init__(self, *, source: str, target: str) -> None:
        import argostranslate.translate  # type: ignore

        self._source = source
        self._target = target
        self._translate_fn = argostranslate.translate.translate
        self._cache: Dict[str, str] = {}

    async def translate(self, text: str) -> str:
        if text in self._cache:
            return self._cache[text]
        translated = await asyncio.to_thread(self._translate_fn, text, self._source, self._target)
        self._cache[text] = translated
        return translated


async def _translate_snippet(translator: Translator, snippet: str, max_chars: int) -> str:
    if not _should_translate_snippet(snippet):
        return snippet
    return await _translate_markdown_inline(translator, snippet, max_chars=max_chars)


def _is_markdown_table_separator(line: str) -> bool:
    stripped = line.strip()
    if "|" not in stripped:
        return False
    # e.g. | --- | :---: | ---: |
    return all(ch in "|:- " for ch in stripped)


def _github_slugify(heading: str, existing: Dict[str, int]) -> str:
    """
    近似 GitHub Markdown 的 heading slug（用于稳定 id）。
    只处理常见 ASCII heading：小写、去标点、空白->-、重复追加 -n。
    """
    text = heading.strip().lower()
    # remove trailing hashes like "Title ###"
    text = re.sub(r"\s+#+\s*$", "", text)
    # keep alnum, space, hyphen, underscore
    text = re.sub(r"[^a-z0-9 _-]+", "", text)
    text = text.replace(" ", "-")
    text = re.sub(r"-{2,}", "-", text).strip("-")
    if not text:
        text = "section"
    count = existing.get(text, 0)
    existing[text] = count + 1
    return text if count == 0 else f"{text}-{count}"


def _extract_markdown_heading_ids(content: str) -> List[str]:
    lines = content.splitlines()
    frontmatter, rest = _split_yaml_frontmatter(lines)

    ids: List[str] = []
    in_fence = False
    fence_marker: Optional[str] = None
    existing: Dict[str, int] = {}

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
                    fence_marker = None
            continue
        if in_fence:
            continue

        m = _MD_HEADING_RE.match(line)
        if not m:
            continue
        heading_text = m.group(3)
        ids.append(_github_slugify(heading_text, existing))

    return ids


async def translate_document_content(
    translator: Translator,
    content: str,
    file_path: Path,
    *,
    chunk_limit: int,
    heading_ids: Optional[List[str]] = None,
) -> str:
    """
    面向 Markdown 的轻量结构化翻译（对 .txt/.rst/.adoc 也可用）。
    """
    lines = content.splitlines()

    frontmatter, rest = _split_yaml_frontmatter(lines) if file_path.suffix.lower() == ".md" else ([], lines)
    out: List[str] = []
    out.extend(frontmatter)

    in_fence = False
    fence_marker: Optional[str] = None

    paragraph_buf: List[str] = []

    async def flush_paragraph() -> None:
        nonlocal paragraph_buf
        if not paragraph_buf:
            return
        block = "\n".join(paragraph_buf)
        translated = await _translate_snippet(translator, block, max_chars=chunk_limit)
        out.extend(translated.splitlines())
        paragraph_buf = []

    for line in rest:
        stripped = line.strip()

        # fenced code
        if stripped.startswith("```") or stripped.startswith("~~~"):
            await flush_paragraph()
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                if fence_marker == marker:
                    in_fence = False
                    fence_marker = None
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        # indented code (markdown / rst common)
        if line.startswith("\t") or line.startswith("    "):
            await flush_paragraph()
            out.append(line)
            continue

        # blank line ends paragraph
        if not stripped:
            await flush_paragraph()
            out.append(line)
            continue

        # markdown specific single-line structures
        m = _MD_HEADING_RE.match(line)
        if m:
            await flush_paragraph()
            if heading_ids is not None and file_path.suffix.lower() == ".md" and heading_ids:
                anchor_id = heading_ids.pop(0)
                out.append(f'<a id="{anchor_id}"></a>')
            prefix = f"{m.group(1)}{m.group(2)}"
            translated = await _translate_snippet(translator, m.group(3), max_chars=chunk_limit)
            out.append(prefix + translated)
            continue

        m = _MD_QUOTE_RE.match(line)
        if m:
            await flush_paragraph()
            prefix = m.group(1)
            translated = await _translate_snippet(translator, m.group(2), max_chars=chunk_limit)
            out.append(prefix + translated)
            continue

        m = _MD_LIST_RE.match(line)
        if m:
            await flush_paragraph()
            indent, bullet, _, space, rest_text = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            checkbox_match = re.match(r"^(\[[ xX]\]\s+)(.+)$", rest_text)
            if checkbox_match:
                checkbox = checkbox_match.group(1)
                item_text = checkbox_match.group(2)
                translated = await _translate_snippet(translator, item_text, max_chars=chunk_limit)
                out.append(f"{indent}{bullet}{space}{checkbox}{translated}")
            else:
                translated = await _translate_snippet(translator, rest_text, max_chars=chunk_limit)
                out.append(f"{indent}{bullet}{space}{translated}")
            continue

        if "|" in line and not _is_markdown_table_separator(line) and line.count("|") >= 2:
            await flush_paragraph()
            # 尽量保留首尾 pipe
            leading_pipe = line.lstrip().startswith("|")
            trailing_pipe = line.rstrip().endswith("|")
            raw_cells = line.split("|")
            # split keeps leading/trailing empty cells
            translated_cells: List[str] = []
            for cell in raw_cells:
                cell_stripped = cell.strip()
                if not cell_stripped:
                    translated_cells.append(cell)
                    continue
                translated_cell = await _translate_snippet(translator, cell_stripped, max_chars=chunk_limit)
                # keep original surrounding spaces roughly
                left_ws = cell[: len(cell) - len(cell.lstrip(" "))]
                right_ws = cell[len(cell.rstrip(" ")) :]
                translated_cells.append(f"{left_ws}{translated_cell}{right_ws}")
            rebuilt = "|".join(translated_cells)
            # keep pipe style stable
            if leading_pipe and not rebuilt.lstrip().startswith("|"):
                rebuilt = "|" + rebuilt
            if trailing_pipe and not rebuilt.rstrip().endswith("|"):
                rebuilt = rebuilt + "|"
            out.append(rebuilt)
            continue

        # default: accumulate into paragraph (keeps original wrapping)
        paragraph_buf.append(line)

    await flush_paragraph()

    # Preserve trailing newline if present
    result = "\n".join(out)
    if content.endswith("\n"):
        result += "\n"
    return result


async def translate_document(
    file_path: Path,
    translator: Translator,
    dry_run: bool = False
) -> Tuple[bool, str]:
    """
    翻译单个文档文件
    Translate a single document file
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        if dry_run:
            return True, f"[DRY-RUN] {file_path}"

        heading_ids = (
            _extract_markdown_heading_ids(original_content)
            if file_path.suffix.lower() == ".md"
            else None
        )
        translated_content = await translate_document_content(
            translator, original_content, file_path, chunk_limit=450, heading_ids=heading_ids
        )

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        return True, f"✓ {file_path}"

    except Exception as e:
        return False, f"✗ {file_path}: {str(e)}"


async def main():
    parser = argparse.ArgumentParser(
        description='批量翻译文档为中文 (Bulk translate documents to Chinese)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际翻译文件 (Preview mode, do not actually translate files)'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='跳过确认并直接覆盖文件 (Skip confirmation and overwrite files)'
    )
    parser.add_argument(
        '--provider',
        choices=['argos', 'mymemory', 'libretranslate'],
        default='argos',
        help='翻译提供方 (Translation provider)'
    )
    parser.add_argument(
        '--api-url',
        default=os.getenv('LIBRETRANSLATE_URL', 'https://libretranslate.com/translate'),
        help='LibreTranslate API端点（provider=libretranslate时使用）'
    )
    parser.add_argument(
        '--api-key',
        default=os.getenv('LIBRETRANSLATE_API_KEY', ''),
        help='LibreTranslate API密钥（provider=libretranslate时使用）'
    )
    parser.add_argument(
        '--dir',
        default='.',
        help='要翻译的根目录 (Root directory to translate)'
    )
    parser.add_argument(
        '--extensions',
        default='md,txt,rst,adoc',
        help='要翻译的文件扩展名，逗号分隔 (File extensions to translate, comma-separated)'
    )
    parser.add_argument(
        '--source-lang',
        default='en',
        help='源语言（默认 en；MyMemory 不支持 auto）'
    )
    parser.add_argument(
        '--target-lang',
        default='zh',
        help='目标语言（默认 zh；MyMemory 建议使用 zh-CN）'
    )

    args = parser.parse_args()

    # 解析扩展名
    extensions = set(f'.{ext.strip()}' for ext in args.extensions.split(','))

    # 查找所有文档
    root_dir = Path(args.dir)
    print(f"🔍 正在扫描文档... (Scanning documents...)")
    documents = find_documents(root_dir, extensions)

    if not documents:
        print("❌ 未找到文档文件 (No document files found)")
        return

    print(f"📄 找到 {len(documents)} 个文档文件 (Found {len(documents)} document files)")
    print()

    if args.dry_run:
        print("🔍 预览模式 - 以下文件将被翻译 (Preview mode - following files will be translated):")
        for doc in documents:
            print(f"  - {doc}")
        print()
        print("💡 提示: 移除 --dry-run 参数以执行实际翻译 (Tip: Remove --dry-run to execute actual translation)")
        return

    # 确认操作
    print(f"⚠️  警告: 即将翻译并替换 {len(documents)} 个文件 (Warning: About to translate and replace {len(documents)} files)")
    if args.provider == 'libretranslate':
        print(f"🌐 LibreTranslate端点: {args.api_url}")
    elif args.provider == 'mymemory':
        print("🌐 Provider: MyMemory (free, 500 chars/request limit)")
    else:
        print("🌐 Provider: Argos Translate (offline)")
    if not args.yes:
        response = input("是否继续? (Continue?) [y/N]: ")
        if response.lower() != 'y':
            print("❌ 操作已取消 (Operation cancelled)")
            return

    # 执行翻译
    print(f"\n🌏 开始翻译... (Starting translation...)\n")

    success_count = 0
    fail_count = 0

    if args.provider == 'argos':
        try:
            import argostranslate.translate  # type: ignore  # noqa: F401
        except Exception:
            print("❌ 未安装 argostranslate，无法使用离线翻译 (provider=argos)。")
            print("   建议先创建虚拟环境并安装：")
            print("   python3 -m venv .venv")
            print("   .venv/bin/python -m pip install argostranslate aiohttp")
            sys.exit(1)
        translator = ArgosTranslator(source=args.source_lang, target=args.target_lang)
        for i, doc in enumerate(documents, 1):
            print(f"[{i}/{len(documents)}] ", end='')
            success, message = await translate_document(doc, translator, args.dry_run)
            if success:
                success_count += 1
            else:
                fail_count += 1
            print(message)
        # 总结
        print(f"\n{'='*60}")
        print(f"✓ 翻译完成 (Translation complete)")
        print(f"  成功 (Success): {success_count}")
        print(f"  失败 (Failed): {fail_count}")
        print(f"  总计 (Total): {len(documents)}")
        print(f"{'='*60}")
        return

    async with aiohttp.ClientSession() as session:
        if args.provider == 'libretranslate':
            translator = LibreTranslateTranslator(
                session,
                api_url=args.api_url,
                api_key=args.api_key,
                source=args.source_lang,
                target=args.target_lang,
            )
        else:
            target = args.target_lang
            if target == "zh":
                target = "zh-CN"
            translator = MyMemoryTranslator(session, source=args.source_lang, target=target)

        for i, doc in enumerate(documents, 1):
            print(f"[{i}/{len(documents)}] ", end='')
            success, message = await translate_document(doc, translator, args.dry_run)
            if success:
                success_count += 1
            else:
                fail_count += 1
            print(message)

    # 总结
    print(f"\n{'='*60}")
    print(f"✓ 翻译完成 (Translation complete)")
    print(f"  成功 (Success): {success_count}")
    print(f"  失败 (Failed): {fail_count}")
    print(f"  总计 (Total): {len(documents)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断 (Operation interrupted by user)")
        sys.exit(1)

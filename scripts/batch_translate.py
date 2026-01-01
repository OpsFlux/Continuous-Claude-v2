#!/usr/bin/env python3
"""
文档批量翻译脚本 - 使用内置翻译
"""

import os
import sys
from pathlib import Path
from typing import Dict, List
import re

# 简单的常用术语映射表
TERM_MAPPING: Dict[str, str] = {
    # 项目相关
    "Continuous Claude": "Continuous Claude（持续Claude）",
    "Claude Code": "Claude Code",

    # 技术术语
    "MCP": "MCP（Model Context Protocol）",
    "MCP server": "MCP服务器",
    "MCP tools": "MCP工具",
    "hook": "hook（钩子）",
    "hooks": "hooks（钩子）",
    "skill": "skill（技能）",
    "skills": "skills（技能）",
    "agent": "agent（代理）",
    "agents": "agents（代理）",
    "ledger": "ledger（账本）",
    "handoff": "handoff（交接）",
    "handoffs": "handoffs（交接）",
    "continuity": "continuity（连续性）",
    "TDD": "TDD（测试驱动开发）",

    # 其他术语
    "token": "token（令牌）",
    "tokens": "tokens（令牌）",
    "repository": "repository（仓库）",
    "repo": "repo（仓库）",
    "artifact": "artifact（制品）",
    "artifacts": "artifacts（制品）",
    "trace": "trace（追踪）",
    "traces": "traces（追踪）",
    "span": "span（跨度）",
    "session": "session（会话）",
    "sessions": "sessions（会话）",
    "workflow": "workflow（工作流）",
    "scripts": "scripts（脚本）",
}


def translate_line(line: str, in_code_block: bool) -> str:
    """
    翻译单行文本，保留代码块和特殊格式
    """
    # 如果在代码块中，不翻译
    if in_code_block:
        return line

    # 空行直接返回
    if not line.strip():
        return line

    # Markdown标题
    if line.startswith('#'):
        return translate_markdown_heading(line)

    # 列表项
    if line.strip().startswith(('-', '*', '+')) and not line.strip().startswith('```'):
        return translate_list_item(line)

    # 代码块标记
    if line.strip().startswith('```'):
        return line

    # 普通文本
    return translate_simple_text(line)


def translate_markdown_heading(line: str) -> str:
    """翻译Markdown标题"""
    match = re.match(r'^(#+)\s+(.+)$', line)
    if not match:
        return line

    level = match.group(1)
    text = match.group(2)
    translated = translate_text(text)

    return f"{level} {translated}"


def translate_list_item(line: str) -> str:
    """翻译列表项"""
    match = re.match(r'^(\s*)([-*+])\s+(.+)$', line)
    if not match:
        return line

    indent = match.group(1)
    bullet = match.group(2)
    text = match.group(3)
    translated = translate_text(text)

    return f"{indent}{bullet} {translated}"


def translate_text(text: str) -> str:
    """翻译文本，保留代码和链接"""
    # 保留代码块
    if '`' in text:
        parts = []
        in_code = False
        current = []
        code_parts = []

        for char in text:
            if char == '`':
                if in_code:
                    code_parts.append(''.join(current))
                    current = []
                else:
                    parts.append(''.join(current))
                    current = []
                in_code = not in_code
            else:
                current.append(char)

        if current:
            if in_code:
                code_parts.append(''.join(current))
            else:
                parts.append(''.join(current))

        # 翻译非代码部分
        result = []
        code_idx = 0
        for i, part in enumerate(parts):
            if i > 0 and code_idx < len(code_parts):
                result.append('`' + code_parts[code_idx] + '`')
                code_idx += 1
            result.append(translate_simple_text(part))

        return ''.join(result)

    return translate_simple_text(text)


def translate_simple_text(text: str) -> str:
    """翻译简单文本（无代码块）"""
    # 这里可以添加更复杂的翻译逻辑
    # 目前先保留原文，仅添加中文注释

    # 如果包含英文句子，添加中文翻译
    if re.search(r'[A-Za-z]{3,}', text):
        # 检查是否已经是中英文混合
        if not re.search(r'[\u4e00-\u9fff]', text):
            # 纯英文，尝试翻译
            translated = simple_translate(text)
            if translated != text:
                return f"{text}  \n{translated}"

    return text


def simple_translate(text: str) -> str:
    """简单翻译（示例）"""
    # 常见短语翻译
    translations = {
        "Quick Start": "快速开始",
        "Usage": "使用方法",
        "Installation": "安装",
        "Configuration": "配置",
        "Examples": "示例",
        "Troubleshooting": "故障排除",
        "Contributing": "贡献",
        "License": "许可证",
        "Features": "特性",
        "Requirements": "要求",
        "Getting Started": "入门指南",
        "Introduction": "介绍",
        "Overview": "概述",
        "API Reference": "API参考",
        "Documentation": "文档",
    }

    for en, zh in translations.items():
        if en.lower() == text.lower():
            return zh

    # 替换已知术语
    result = text
    for en, zh in TERM_MAPPING.items():
        result = re.sub(r'\b' + re.escape(en) + r'\b', zh, result, flags=re.IGNORECASE)

    return result


def translate_file(file_path: Path) -> bool:
    """翻译单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        translated_lines = []
        in_code_block = False
        code_fence = ''

        for line in lines:
            # 检测代码块
            if line.strip().startswith('```'):
                if not in_code_block:
                    # 开始代码块
                    in_code_block = True
                    code_fence = line.strip()
                else:
                    # 结束代码块
                    in_code_block = False
                    code_fence = ''
                translated_lines.append(line)
                continue

            # 在代码块内不翻译
            if in_code_block:
                translated_lines.append(line)
                continue

            # 翻译普通行
            translated_line = translate_line(line, in_code_block)
            translated_lines.append(translated_line)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(translated_lines))

        return True

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='文档批量翻译工具')
    parser.add_argument('--force', action='store_true', help='强制执行，不询问确认')
    args = parser.parse_args()

    print("=" * 60)
    print("文档批量翻译工具")
    print("=" * 60)
    print()

    # 获取当前目录
    root_dir = Path.cwd()

    # 查找所有文档文件
    print("🔍 扫描文档文件...")
    documents = []
    for ext in ['.md', '.txt', '.rst', '.adoc']:
        documents.extend(root_dir.rglob(f'*{ext}'))

    # 过滤排除的目录
    excluded_dirs = {'.git', 'node_modules', 'venv', '.venv', '__pycache__',
                    '.pytest_cache', 'dist', 'build', '.mypy_cache'}

    filtered_docs = []
    for doc in documents:
        if not any(excluded in doc.parts for excluded in excluded_dirs):
            filtered_docs.append(doc)

    filtered_docs.sort()

    print(f"📄 找到 {len(filtered_docs)} 个文档文件\n")

    if not filtered_docs:
        print("❌ 没有找到文档文件")
        return

    # 确认（除非使用--force）
    if not args.force:
        print("⚠️  警告: 即将翻译并替换所有文档文件")
        print("   建议先创建git备份！")
        try:
            response = input("\n是否继续? [y/N]: ")
            if response.lower() != 'y':
                print("❌ 操作已取消")
                return
        except EOFError:
            print("\n使用 --force 参数自动确认")

    # 执行翻译
    print(f"\n🌏 开始翻译...\n")

    success_count = 0
    fail_count = 0

    for i, doc in enumerate(filtered_docs, 1):
        rel_path = doc.relative_to(root_dir)
        print(f"[{i}/{len(filtered_docs)}] {rel_path}", end=' ... ')

        if translate_file(doc):
            print("✓")
            success_count += 1
        else:
            print("✗")
            fail_count += 1

    # 总结
    print(f"\n{'='*60}")
    print(f"✓ 翻译完成")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  总计: {len(filtered_docs)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")
        sys.exit(1)

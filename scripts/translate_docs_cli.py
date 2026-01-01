#!/usr/bin/env python3
"""
批量翻译文档脚本 - 使用Claude API (Bulk Document Translation Script - Using Claude API)

将指定目录下的所有Markdown、文本文件翻译成中文，并替换原文件。
使用Claude API进行高质量翻译，保留代码块和格式。

使用方法 (Usage):
    # 预览将要翻译的文件
    python3 scripts/translate_docs_cli.py --dry-run

    # 翻译所有文档（需要设置ANTHROPIC_API_KEY环境变量）
    python3 scripts/translate_docs_cli.py

    # 翻译特定目录
    python3 scripts/translate_docs_cli.py --dir ./docs

环境变量 (Environment Variables):
    ANTHROPIC_API_KEY - Claude API密钥 (必需)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple
import asyncio
import anthropic
from anthropic import AsyncAnthropic

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {'.md', '.txt', '.rst', '.adoc'}

# 需要排除的目录
EXCLUDED_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '__pycache__',
    '.pytest_cache', 'dist', 'build', '.mypy_cache', '.tox'
}


def find_documents(root_dir: Path, extensions: set = None) -> List[Path]:
    """递归查找所有文档文件"""
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


async def translate_with_claude(
    client: AsyncAnthropic,
    content: str,
    file_path: Path
) -> str:
    """
    使用Claude API翻译文档内容，保留代码块和格式
    """
    # 构建提示词
    prompt = f"""请将以下文档内容完整翻译成中文。要求：

1. **完整翻译**：翻译所有文本内容，不要遗漏
2. **保留格式**：
   - 保持Markdown格式不变（标题、列表、链接等）
   - 代码块（```或缩进）内的内容不翻译，保持原样
   - 保留所有URL、邮箱、文件路径
3. **专业术语**：
   - 技术术语首次出现时保留英文，括号内加中文翻译
   - 例如："Continuous Integration (CI, 持续集成)"
4. **自然流畅**：确保中文翻译自然、专业、易读

文件路径: {file_path}
原始内容:
```
{content}
```

请只返回翻译后的完整内容，不要添加任何解释或额外文字。
"""

    try:
        message = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=16000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        translated_content = message.content[0].text
        return translated_content

    except Exception as e:
        print(f"  ⚠ Claude API错误: {e}")
        return None


async def translate_document(
    client: AsyncAnthropic,
    file_path: Path,
    dry_run: bool = False
) -> Tuple[bool, str]:
    """翻译单个文档文件"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        if dry_run:
            return True, f"[DRY-RUN] {file_path.relative_to(Path.cwd())}"

        # 跳过空文件
        if not original_content.strip():
            return True, f"⊘ {file_path.relative_to(Path.cwd())} (空文件)"

        print(f"  正在翻译: {file_path.relative_to(Path.cwd())}", end=' ... ')

        # 使用Claude翻译
        translated_content = await translate_with_claude(client, original_content, file_path)

        if translated_content is None:
            return False, f"✗ {file_path.relative_to(Path.cwd())} (翻译失败)"

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print("✓")
        return True, f"✓ {file_path.relative_to(Path.cwd())}"

    except Exception as e:
        print(f"✗")
        return False, f"✗ {file_path.relative_to(Path.cwd())}: {str(e)}"


async def main():
    parser = argparse.ArgumentParser(
        description='批量翻译文档为中文 (使用Claude API)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际翻译文件'
    )
    parser.add_argument(
        '--dir',
        default='.',
        help='要翻译的根目录 (默认: 当前目录)'
    )
    parser.add_argument(
        '--extensions',
        default='md,txt,rst,adoc',
        help='要翻译的文件扩展名，逗号分隔 (默认: md,txt,rst,adoc)'
    )
    parser.add_argument(
        '--api-key',
        default=os.getenv('ANTHROPIC_API_KEY'),
        help='Claude API密钥 (也可通过ANTHROPIC_API_KEY环境变量设置)'
    )

    args = parser.parse_args()

    # 检查API密钥
    if not args.dry_run and not args.api_key:
        print("❌ 错误: 未找到ANTHROPIC_API_KEY环境变量")
        print("   请设置: export ANTHROPIC_API_KEY='your-api-key'")
        print("   或使用: --api-key 'your-api-key'")
        sys.exit(1)

    # 解析扩展名
    extensions = set(f'.{ext.strip()}' for ext in args.extensions.split(','))

    # 查找所有文档
    root_dir = Path(args.dir)
    print(f"🔍 正在扫描文档... (Scanning documents...)")
    documents = find_documents(root_dir, extensions)

    if not documents:
        print("❌ 未找到文档文件 (No document files found)")
        return

    print(f"📄 找到 {len(documents)} 个文档文件\n")

    if args.dry_run:
        print("🔍 预览模式 - 以下文件将被翻译:\n")
        for doc in documents:
            print(f"  - {doc.relative_to(Path.cwd())}")
        print(f"\n💡 提示: 移除 --dry-run 参数以执行实际翻译")
        print(f"   确保已设置 ANTHROPIC_API_KEY 环境变量")
        return

    # 确认操作
    print(f"⚠️  警告: 即将翻译并替换 {len(documents)} 个文件")
    print(f"   这将修改原始文件，建议先创建git备份！")
    response = input("\n是否继续? (Continue?) [y/N]: ")

    if response.lower() != 'y':
        print("❌ 操作已取消")
        return

    # 初始化Claude客户端
    client = AsyncAnthropic(api_key=args.api_key)

    # 执行翻译
    print(f"\n🌏 开始翻译...\n")

    success_count = 0
    fail_count = 0

    for i, doc in enumerate(documents, 1):
        print(f"[{i}/{len(documents)}] ", end='')
        success, message = await translate_document(client, doc, args.dry_run)

        if success:
            success_count += 1
        else:
            fail_count += 1
            print(message)

    # 总结
    print(f"\n{'='*60}")
    print(f"✓ 翻译完成")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  总计: {len(documents)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")
        sys.exit(1)

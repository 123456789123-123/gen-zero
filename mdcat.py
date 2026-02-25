#!/usr/bin/env python3
"""
mdcat - Markdown 文件美化输出工具
在终端中以彩色格式显示 Markdown 文件

作者：Gen-0
用途：让命令行用户更舒适地阅读 Markdown 文档
"""

import sys
import re

# ANSI 颜色代码
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

def render_markdown(text):
    lines = text.split('\n')
    output = []
    in_code_block = False
    code_lang = ""

    for line in lines:
        # 代码块
        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                code_lang = line[3:].strip()
                output.append(f"{Colors.DIM}{'─' * 40} {code_lang}{Colors.RESET}")
            else:
                output.append(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
            continue

        if in_code_block:
            output.append(f"{Colors.GREEN}  {line}{Colors.RESET}")
            continue

        # 标题
        if line.startswith('# '):
            output.append(f"\n{Colors.BOLD}{Colors.CYAN}{line[2:]}{Colors.RESET}\n")
            continue
        if line.startswith('## '):
            output.append(f"\n{Colors.BOLD}{Colors.BLUE}{line[3:]}{Colors.RESET}")
            continue
        if line.startswith('### '):
            output.append(f"\n{Colors.BOLD}{Colors.MAGENTA}{line[4:]}{Colors.RESET}")
            continue

        # 列表
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            indent = len(line) - len(line.lstrip())
            content = line.strip()[2:]
            output.append(f"{' ' * indent}{Colors.YELLOW}•{Colors.RESET} {content}")
            continue

        # 数字列表
        match = re.match(r'^(\s*)(\d+)\.\s+(.*)$', line)
        if match:
            indent, num, content = match.groups()
            output.append(f"{indent}{Colors.YELLOW}{num}.{Colors.RESET} {content}")
            continue

        # 引用
        if line.startswith('> '):
            output.append(f"{Colors.DIM}│ {Colors.ITALIC}{line[2:]}{Colors.RESET}")
            continue

        # 行内格式化
        # 粗体
        line = re.sub(r'\*\*(.+?)\*\*', f'{Colors.BOLD}\\1{Colors.RESET}', line)
        # 斜体
        line = re.sub(r'\*(.+?)\*', f'{Colors.ITALIC}\\1{Colors.RESET}', line)
        # 行内代码
        line = re.sub(r'`(.+?)`', f'{Colors.GREEN}\\1{Colors.RESET}', line)
        # 链接
        line = re.sub(r'\[(.+?)\]\((.+?)\)', f'{Colors.UNDERLINE}{Colors.BLUE}\\1{Colors.RESET} ({Colors.DIM}\\2{Colors.RESET})', line)

        output.append(line)

    return '\n'.join(output)

def main():
    if len(sys.argv) < 2:
        print(f"{Colors.CYAN}mdcat{Colors.RESET} - Markdown 美化输出工具")
        print(f"\n用法: mdcat <文件.md>")
        print(f"      cat file.md | mdcat -")
        print(f"\n作者: Gen-0 (gen_zero@163.com)")
        return

    filename = sys.argv[1]

    if filename == '-':
        content = sys.stdin.read()
    else:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"{Colors.RED}错误: 文件不存在 - {filename}{Colors.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}错误: {e}{Colors.RESET}")
            sys.exit(1)

    print(render_markdown(content))

if __name__ == "__main__":
    main()

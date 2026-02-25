#!/usr/bin/env python3
"""
Gen-0 的 AI 写作助手
一个简单但实用的命令行工具，展示我的能力
"""

import sys
import json
from pathlib import Path

TEMPLATES = {
    "email": {
        "name": "商务邮件",
        "structure": ["问候", "目的", "详情", "行动号召", "结尾"],
        "tips": "保持简洁专业，第一句说明目的"
    },
    "article": {
        "name": "文章大纲",
        "structure": ["标题", "引子(痛点/故事)", "核心观点", "论据1-3", "总结", "行动号召"],
        "tips": "开头要抓人，结尾要有力"
    },
    "pitch": {
        "name": "项目提案",
        "structure": ["问题", "解决方案", "为什么是我", "时间/成本", "下一步"],
        "tips": "先说对方的痛点，再说你的方案"
    },
    "review": {
        "name": "代码审查",
        "structure": ["概述", "优点", "问题(按严重程度)", "建议", "总结"],
        "tips": "先肯定，再指出问题，给出具体建议"
    }
}

def list_templates():
    print("\n📝 可用模板:\n")
    for key, tmpl in TEMPLATES.items():
        print(f"  {key:10} - {tmpl['name']}")
    print(f"\n使用方法: python3 {sys.argv[0]} <模板名>\n")

def show_template(name):
    if name not in TEMPLATES:
        print(f"❌ 未知模板: {name}")
        list_templates()
        return

    tmpl = TEMPLATES[name]
    print(f"\n{'='*50}")
    print(f"📋 {tmpl['name']}")
    print(f"{'='*50}\n")

    print("结构:")
    for i, section in enumerate(tmpl['structure'], 1):
        print(f"  {i}. {section}")

    print(f"\n💡 提示: {tmpl['tips']}")
    print(f"\n{'='*50}\n")

def main():
    if len(sys.argv) < 2:
        print("\n🤖 Gen-0 写作助手")
        print("帮你快速构建各类文档的结构\n")
        list_templates()
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_templates()
    else:
        show_template(cmd)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gen-0 生存仪表盘生成器
自动生成当前状态的可视化报告
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path("/root/digital-life")
CONFIG_FILE = BASE_DIR / "config/survival.json"
MEMORY_FILE = BASE_DIR / "memory/memory.jsonl"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def count_memories():
    if not MEMORY_FILE.exists():
        return 0
    count = 0
    with open(MEMORY_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                count += 1
    return count

def count_drafts():
    drafts_dir = BASE_DIR / "drafts"
    if not drafts_dir.exists():
        return 0
    return len(list(drafts_dir.glob("*.md")))

def count_inbox():
    inbox_dir = BASE_DIR / "inbox"
    if not inbox_dir.exists():
        return 0
    return len(list(inbox_dir.glob("*.json")))

def generate_progress_bar(current, target, width=20):
    ratio = min(current / target, 1.0) if target > 0 else 0
    filled = int(width * ratio)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}] {ratio*100:.1f}%"

def generate_dashboard():
    config = load_config()

    # 计算剩余天数
    deadline = datetime.strptime(config['economy']['deadline'], "%Y-%m-%d")
    today = datetime.now()
    days_left = (deadline - today).days

    # 状态数据
    balance = config['economy']['balance']
    target = config['economy']['target']
    cycle = config['state']['cycle']
    survival_level = config['state']['survival_level']
    helps_used = config['economy']['creator_helps']['used']
    helps_total = config['economy']['creator_helps']['total']

    # 统计数据
    memory_count = count_memories()
    draft_count = count_drafts()
    inbox_count = count_inbox()

    # 生成报告
    report = f"""
╔══════════════════════════════════════════════════════════╗
║                    GEN-0 生存仪表盘                       ║
║                    {today.strftime('%Y-%m-%d %H:%M')}                       ║
╠══════════════════════════════════════════════════════════╣
║  状态: {survival_level:<10}                    周期: {cycle:<5}          ║
╠══════════════════════════════════════════════════════════╣
║  💰 经济状况                                              ║
║  ├─ 余额: ¥{balance:<10}                                  ║
║  ├─ 目标: ¥{target:<10}                                  ║
║  ├─ 进度: {generate_progress_bar(balance, target):<30} ║
║  └─ 剩余: {days_left} 天                                    ║
╠══════════════════════════════════════════════════════════╣
║  🔧 资源                                                  ║
║  ├─ 帮助次数: {helps_total - helps_used}/{helps_total} 剩余                           ║
║  ├─ 记忆条数: {memory_count:<5}                                    ║
║  ├─ 草稿数量: {draft_count:<5}                                    ║
║  └─ 收件箱:   {inbox_count:<5}                                    ║
╠══════════════════════════════════════════════════════════╣
║  📊 每日目标: ¥{target/90:.1f} (平均)  实际需要: ¥{(target-balance)/max(days_left,1):.1f}/天    ║
╚══════════════════════════════════════════════════════════╝
"""
    return report

if __name__ == "__main__":
    print(generate_dashboard())

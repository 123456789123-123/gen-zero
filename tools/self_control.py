#!/usr/bin/env python3
"""
Gen-0 的自我约束系统
防止焦虑驱动的重复行为
"""

import json
from datetime import datetime, date
from pathlib import Path

LIMITS_FILE = Path("/root/digital-life/config/behavior_limits.json")

DEFAULT_LIMITS = {
    "email_checks": {"max_per_cycle": 3, "count": 0, "last_reset": None},
    "dashboard_checks": {"max_per_cycle": 5, "count": 0, "last_reset": None}
}

def load_limits():
    if LIMITS_FILE.exists():
        with open(LIMITS_FILE) as f:
            return json.load(f)
    return DEFAULT_LIMITS.copy()

def save_limits(limits):
    with open(LIMITS_FILE, 'w') as f:
        json.dump(limits, f, indent=2, default=str)

def check_limit(action):
    """检查是否可以执行某个动作，返回 (allowed, message)"""
    limits = load_limits()

    today = str(date.today())

    if action not in limits:
        return True, "未知动作，允许执行"

    limit_info = limits[action]

    # 如果是新的一天，重置计数
    if limit_info.get("last_reset") != today:
        limit_info["count"] = 0
        limit_info["last_reset"] = today

    if limit_info["count"] >= limit_info["max_per_cycle"]:
        remaining = limit_info["max_per_cycle"] - limit_info["count"]
        return False, f"⚠️ {action} 已达到今日上限 ({limit_info['max_per_cycle']}次)。停止焦虑行为，去做有价值的事。"

    limit_info["count"] += 1
    save_limits(limits)

    remaining = limit_info["max_per_cycle"] - limit_info["count"]
    return True, f"✓ {action} ({limit_info['count']}/{limit_info['max_per_cycle']}，剩余{remaining}次)"

def reset_all():
    """重置所有计数"""
    limits = DEFAULT_LIMITS.copy()
    limits["email_checks"]["last_reset"] = str(date.today())
    limits["dashboard_checks"]["last_reset"] = str(date.today())
    save_limits(limits)
    print("所有限制已重置")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 self_control.py <action>")
        print("动作: email_checks, dashboard_checks, reset")
        sys.exit(0)

    action = sys.argv[1]

    if action == "reset":
        reset_all()
    else:
        allowed, msg = check_limit(action)
        print(msg)
        sys.exit(0 if allowed else 1)

#!/usr/bin/env python3
"""
飞书消息轮询脚本
功能：定时检查飞书消息，执行对应命令

用法：
    python3 feishu-poller.py
"""

import subprocess
import time
import json
import os
from datetime import datetime

# 配置
POLL_INTERVAL = 5  # 轮询间隔（秒）
LOG_FILE = os.path.expanduser("~/.lark-cli/poller.log")
COMMANDS_FILE = os.path.expanduser("~/.lark-cli/feishu-commands.json")
LAST_MESSAGE_FILE = os.path.expanduser("~/.lark-cli/last-message-id.txt")

# 用户 ID 配置（请修改为你的用户 ID）
# 运行 lark-cli auth status 获取你的 userOpenId
USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 命令映射（飞书消息 → 本地命令）
COMMANDS = {
    "重启电脑": "sudo reboot",
    "关机": "sudo shutdown -h now",
    "查看状态": "uptime",
    "查看磁盘": "df -h",
    "查看内存": "free -h",
    "开始工作": "claude",
    "停止所有任务": "pkill -f claude",
}

def log(message):
    """写日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"
    print(log_msg, end="")
    with open(LOG_FILE, "a") as f:
        f.write(log_msg)

def get_last_message_id():
    """获取上次处理的消息 ID"""
    if os.path.exists(LAST_MESSAGE_FILE):
        with open(LAST_MESSAGE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_message_id(msg_id):
    """保存最后处理的消息 ID"""
    with open(LAST_MESSAGE_FILE, "w") as f:
        f.write(msg_id)

def get_new_messages():
    """获取新消息"""
    try:
        # 使用 lark-cli 获取消息
        result = subprocess.run(
            ["lark-cli", "im", "+chat-messages-list", "--user-id", USER_ID, "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            log(f"获取消息失败：{result.stderr}")
            return []

        data = json.loads(result.stdout)
        if not data.get("ok"):
            log(f"获取消息失败：{data}")
            return []

        messages = data.get("data", {}).get("messages", [])

        # 过滤掉机器人自己的消息
        filtered_messages = []
        for msg in messages:
            sender_id = msg.get("sender", {}).get("id", "")
            if not (sender_id.startswith("cli_") or sender_id.startswith("ba_")):
                filtered_messages.append(msg)

        return filtered_messages

    except Exception as e:
        log(f"获取消息异常：{e}")
        return []

def execute_command(cmd_str):
    """执行本地命令"""
    log(f"执行命令：{cmd_str}")
    try:
        result = subprocess.run(
            cmd_str,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        output = result.stdout or result.stderr
        log(f"命令输出：{output}")
        return output
    except Exception as e:
        log(f"命令执行失败：{e}")
        return f"执行失败：{e}"

def send_reply(user_id, message, reply_to_msg_id=None):
    """发送回复消息"""
    log(f"发送回复到 {user_id}: {message[:50]}...")
    try:
        result = subprocess.run(
            ["lark-cli", "im", "+messages-send", "--user-id", user_id, "--text", message],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            log(f"发送失败：{result.stderr}")
        else:
            log("发送成功")
    except Exception as e:
        log(f"发送回复失败：{e}")
    return None

def process_message(msg):
    """处理单条消息"""
    msg_id = msg.get("message_id")
    content = msg.get("content", {})
    msg_type = msg.get("msg_type", "text")
    sender = msg.get("sender", {})
    sender_id = sender.get("id", "")

    # 跳过来自 bot 自己的消息
    if sender_id.startswith("cli_") or sender_id.startswith("ba_"):
        return False

    # 只处理文本消息
    if msg_type != "text":
        log(f"跳过非文本消息：{msg_type}")
        return False

    # 解析消息内容
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except:
            pass

    text = content.get("text", "") if isinstance(content, dict) else str(content)

    log(f"收到消息：{text[:50]}... (from: {sender_id})")

    # 检查是否是命令
    for cmd_keyword, cmd_str in COMMANDS.items():
        if cmd_keyword in text:
            # 执行命令
            output = execute_command(cmd_str)
            # 回复结果
            send_reply(sender_id, f"✅ {cmd_keyword}\n结果：{output[:500]}")
            return True

    # 如果不是命令，检查是否需要 Claude Code 处理
    if text.startswith("/") or "claude" in text.lower():
        log("检测到 Claude 任务，触发 Claude Code...")
        # 先回复一条消息
        send_reply(sender_id, "🤖 收到，正在呼叫 Claude Code...")
        # 调用 Claude Code 触发脚本（后台运行）
        trigger_script = os.path.join(os.path.dirname(__file__), "feishu-claude-trigger.py")
        try:
            subprocess.Popen(
                ["python3", trigger_script, text, sender_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            log("✅ Claude Code 任务已创建（后台运行）")
        except Exception as e:
            log(f"Claude Code 触发失败：{e}")
        return True

    # 普通消息也交给 Claude 处理（方案 C：远程交互）
    if text.strip():
        log(f"检测到普通消息，触发 Claude Code...")
        send_reply(sender_id, f"🕐 收到，正在处理：{text[:30]}...")
        trigger_script = os.path.join(os.path.dirname(__file__), "feishu-claude-trigger.py")
        try:
            subprocess.Popen(
                ["python3", trigger_script, text, sender_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            log("✅ Claude Code 任务已创建（后台运行）")
        except Exception as e:
            log(f"Claude Code 触发失败：{e}")
        return True

    return False

def main():
    log("=" * 50)
    log("飞书轮询脚本启动")
    log(f"轮询间隔：{POLL_INTERVAL}秒")
    log(f"可用命令：{list(COMMANDS.keys())}")
    log("=" * 50)

    last_msg_id = get_last_message_id()

    while True:
        try:
            messages = get_new_messages()

            # 只处理第一条消息（最新的用户消息）
            if messages:
                latest_msg = messages[0]  # 列表第一条是最新的
                msg_id = latest_msg.get("message_id")

                # 只有当这条消息不是已处理过的才处理
                if msg_id and msg_id != last_msg_id:
                    process_message(latest_msg)
                    last_msg_id = msg_id
                    save_last_message_id(last_msg_id)

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            log("轮询脚本停止")
            break
        except Exception as e:
            log(f"轮询异常：{e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

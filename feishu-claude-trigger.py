#!/usr/bin/env python3
"""
Claude Code 触发脚本
功能：接收飞书消息，触发 Claude Code 处理

用法：
    python3 feishu-claude-trigger.py "<message_text>" "<sender_id>" "<reply_to_msg_id>"
"""

import subprocess
import sys
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.lark-cli/claude-trigger.log")
TASKS_DIR = os.path.expanduser("~/.lark-cli/claude-tasks")

def log(message):
    """写日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"
    print(log_msg, end="")
    with open(LOG_FILE, "a") as f:
        f.write(log_msg)

def send_reply_to_feishu(user_id, message):
    """发送回复到飞书"""
    log(f"发送回复到飞书：{message[:50]}...")
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
        log(f"发送失败：{e}")

def create_claude_task(message, sender_id):
    """创建 Claude Code 任务"""
    # 确保任务目录存在
    os.makedirs(TASKS_DIR, exist_ok=True)

    # 生成任务文件
    task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_file = os.path.join(TASKS_DIR, f"task_{task_id}.md")

    task_content = f"""# Claude Code 任务

**来源**: 飞书消息
**发送者**: {sender_id}
**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 原始消息
{message}

## 处理要求
1. 理解用户需求
2. 执行相应操作（写代码、写文档、查询信息等）
3. 将结果保存到任务文件
"""

    with open(task_file, "w") as f:
        f.write(task_content)

    log(f"创建任务文件：{task_file}")
    return task_file

def run_claude_code(task_file):
    """调用 Claude Code 处理任务"""
    try:
        # 读取任务内容
        with open(task_file, "r") as f:
            task_content = f.read()

        # 调用 Claude Code
        log("启动 Claude Code...")

        # 将任务内容通过管道传给 Claude Code
        result = subprocess.run(
            ["claude"],
            input=task_content,
            capture_output=True,
            text=True,
            timeout=3600  # 1 小时超时
        )

        # 保存结果
        result_file = task_file.replace(".md", "_result.md")
        with open(result_file, "w") as f:
            f.write(f"# Claude Code 处理结果\n\n")
            f.write(result.stdout)
            if result.stderr:
                f.write(f"\n## 错误信息\n{result.stderr}\n")

        log(f"处理完成，结果保存到：{result_file}")
        return result_file

    except subprocess.TimeoutExpired:
        log("Claude Code 执行超时")
        return None
    except Exception as e:
        log(f"Claude Code 执行失败：{e}")
        return None

def send_reply_to_feishu(user_id, message):
    """发送回复到飞书"""
    log(f"发送回复到飞书：{message[:50]}...")
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
        log(f"发送失败：{e}")

def main():
    if len(sys.argv) < 3:
        print("用法：python3 feishu-claude-trigger.py <message_text> <sender_id>")
        sys.exit(1)

    message = sys.argv[1]
    sender_id = sys.argv[2]

    log("=" * 50)
    log(f"收到 Claude 任务：{message[:50]}...")

    # 创建任务
    task_file = create_claude_task(message, sender_id)

    # 调用 Claude Code
    result_file = run_claude_code(task_file)

    if result_file:
        log("✅ 任务完成")
        # 读取结果并发送回飞书
        try:
            with open(result_file, "r") as f:
                result = f.read()
            # 限制长度，避免消息太长
            result_preview = result[:1500] if len(result) > 1500 else result
            send_reply_to_feishu(sender_id, f"✅ 任务完成\n\n{result_preview}")
        except Exception as e:
            log(f"发送结果失败：{e}")
    else:
        log("❌ 任务失败")
        send_reply_to_feishu(sender_id, "❌ 任务执行失败，请查看日志")

    log("=" * 50)

if __name__ == "__main__":
    main()

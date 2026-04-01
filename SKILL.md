---
name: skill-feishu
version: 1.0.0
description: "飞书双向交互：接收飞书消息并触发 Claude Code 执行任务，自动回复结果到飞书。支持预设命令执行、Claude 任务触发、权限自动确认。"
metadata:
  requires:
    bins: ["lark-cli", "python3"]
  files:
    - ~/.lark-cli/feishu-poller.py
    - ~/.lark-cli/feishu-claude-trigger.py
    - ~/.lark-cli/config.json
---

# skill-feishu - 飞书双向交互 Skill

## 功能说明

这个 Skill 让你可以通过飞书消息远程控制 Claude Code：

1. **飞书发送消息** → Claude Code 接收任务
2. **Claude Code 执行任务** → 飞书收到回复
3. **全程自动化** → 无需人工确认权限

## 支持的命令

### 预设命令（直接执行）

| 飞书消息 | 本地命令 | 说明 |
|---------|---------|------|
| `查看状态` | `uptime` | 查看系统运行状态 |
| `查看磁盘` | `df -h` | 查看磁盘使用情况 |
| `查看内存` | `free -h` | 查看内存使用情况 |
| `开始工作` | `claude` | 启动 Claude Code |
| `停止所有任务` | `pkill -f claude` | 停止所有 Claude 任务 |

### Claude 任务（自动处理）

- 以 `/` 开头的消息
- 包含 `claude` 的消息
- 其他所有消息（默认交给 Claude 处理）

## 使用方法

### 启动轮询

```bash
python3 ~/.lark-cli/feishu-poller.py
```

### 后台运行（推荐）

```bash
nohup python3 ~/.lark-cli/feishu-poller.py &
```

### 查看日志

```bash
tail -f ~/.lark-cli/poller.log
```

## 配置文件

- `~/.lark-cli/config.json` - 飞书应用配置
- `~/.lark-cli/last-message-id.txt` - 已处理消息 ID
- `~/.claude/settings.json` - Claude 权限预设

## 权限预设

需要在 `~/.claude/settings.json` 中配置：

```json
{
  "permission_presets": {
    "allowed_tools": ["Bash", "Write", "Read", "Edit"],
    "allow_bash": ["lark-cli*", "uptime", "df*", "free*"],
    "readonly_dirs": ["~/.lark-cli", "~/"],
    "writable_dirs": ["~/.lark-cli", "/tmp/"]
  }
}
```

## 任务目录

Claude 任务文件保存在：`~/.lark-cli/claude-tasks/`

- `task_YYYYMMDD_HHMMSS.md` - 任务描述
- `task_YYYYMMDD_HHMMSS_result.md` - 处理结果

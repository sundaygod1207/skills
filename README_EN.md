# skill-feishu User Guide

> Connect Claude Code to Lark (Feishu) for true two-way interaction
> Send messages via Lark at work, Claude Code executes tasks at home and replies automatically

---

## Quick Start (5 minutes)

### Prerequisites

Make sure you have installed:
- [ ] Node.js (for Lark CLI)
- [ ] Python 3 (for poller script)
- [ ] Claude Code

### Installation Steps

**1. Install Lark CLI**
```bash
npm install -g @larksuite/cli
```

**2. Clone the project**
```bash
git clone https://github.com/sundaygod1207/skills.git
cd skills/skill-feishu
```

**3. Run installation script**
```bash
bash install.sh
```

**4. Login to Lark**
```bash
lark-cli auth login --recommend
```

**5. Get your User ID**
```bash
lark-cli auth status
```
Find `userOpenId` in the output, similar to `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**6. Edit configuration**
```bash
nano ~/.lark-cli/feishu-poller.py
```
Change `USER_ID = "请替换为你的用户 ID"` to:
```python
USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your real user ID
```

**7. Start the poller**
```bash
python3 ~/.lark-cli/feishu-poller.py
```

Or run in background:
```bash
nohup python3 ~/.lark-cli/feishu-poller.py > ~/.lark-cli/poller.log 2>&1 &
```

---

## Lark App Configuration

### Create Lark App

1. Visit Lark Open Platform: https://open.feishu.cn/app
2. Click "Create App" → "Enterprise自建"
3. Fill in app name (e.g., My Personal Assistant)
4. After creation, get from "Credentials & Basic Info":
   - App ID
   - App Secret

### Add Bot Capability

1. In app management, click "Add Capability"
2. Select "Bot"
3. Configure bot name and avatar

### Configure Permissions

In "Permissions", add:
- `im:message` - Send messages
- `im:chat` - Read/write chat messages
- `contact:user.base:readonly` - Read user info

### Initialize Config

```bash
lark-cli config init --new
```

Enter App ID and App Secret when prompted.

---

## Usage

### Preset Commands

Send these messages to the bot in Lark:

| Message | Function | Example Reply |
|---------|----------|---------------|
| `查看状态` | Execute `uptime` | `11:00 up 1 day, 3 users, load averages: 1.2 1.3 1.3` |
| `查看磁盘` | Execute `df -h` | Disk usage |
| `查看内存` | Execute `free -h` | Memory usage |
| `开始工作` | Start Claude Code | Launch Claude |
| `停止所有任务` | Stop all Claude tasks | Stop all Claude processes |

### Claude Tasks

Send any message (not a preset command) to trigger Claude Code:

**Example 1: Write code**
```
帮我写一个 Python 脚本，打印斐波那契数列前 10 个数
```

**Example 2: Write documentation**
```
帮我写一份项目 README，介绍这个项目的功能和安装方法
```

**Example 3: Query information**
```
查一下今天有什么热点新闻
```

### Workflow

1. Send message via Lark
2. Receive "🕐 收到，正在处理..."
3. Claude Code executes task (background)
4. Receive "✅ 任务完成" + result

---

## Advanced Configuration

### Custom Commands

Edit `~/.lark-cli/feishu-poller.py`, modify `COMMANDS` dict:

```python
COMMANDS = {
    "重启电脑": "sudo reboot",
    "关机": "sudo shutdown -h now",
    "your command": "actual command to execute",
}
```

### Change Poll Interval

```python
POLL_INTERVAL = 5  # Poll interval in seconds
```

### View Logs

```bash
# Real-time
tail -f ~/.lark-cli/poller.log

# Last 100 lines
tail -100 ~/.lark-cli/poller.log
```

---

## FAQ

### Q: Messages are processed repeatedly?
A: Ensure `last-message-id.txt` exists and is correct. Restart the poller if issue persists.

### Q: No reply in Lark?
A: Check:
1. Bot is configured in Lark app
2. `im:message` permission is granted
3. `lark-cli auth status` shows valid

### Q: Claude task stuck?
A: Check permission presets in `~/.claude/settings.json` or view `~/.lark-cli/claude-trigger.log`

### Q: Can multiple users use it?
A: Current version supports single user ID. Multi-user requires code modification.

---

## Security Notes

1. **Token Protection**: `config.json` contains App Secret, do not commit to git
2. **Command Whitelist**: Only authorize safe commands, never `rm -rf`, `sudo`, etc.
3. **Minimum Permissions**: Grant only necessary API permissions
4. **Log Audit**: Regularly review `poller.log`

---

## Project Structure

```
skill-feishu/
├── SKILL.md              # Skill definition
├── README.md             # GitHub README
├── README_CN.md          # Chinese Guide
├── README_EN.md          # English Guide (this file)
├── install.sh            # Installation script
├── feishu-poller.py      # Poller script
├── feishu-claude-trigger.py  # Claude trigger
└── BOT_SETUP.md          # Bot setup guide
```

---

## Changelog

### v1.0.0 (2026-04-01)
- Initial release
- Lark message reception
- Claude task triggering
- Automatic reply
- Permission presets

---

## Support

- GitHub Issues: https://github.com/sundaygod1207/skills/issues
- Email: macmini2603@163.com

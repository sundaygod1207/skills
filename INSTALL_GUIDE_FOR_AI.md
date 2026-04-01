# skill-feishu Installation Guide for AI Assistants

> **For AI Assistants**: Claude Code, OpenClaw, or similar tools
> **User Request**: "Install skill-feishu from GitHub"

---

## Project Info

- **Repository**: https://github.com/sundaygod1207/skills
- **Subdirectory**: `skill-feishu`
- **Purpose**: Two-way Lark (Feishu) integration for Claude Code
- **Main Function**: Receive Lark messages → Execute Claude tasks → Reply to Lark

---

## Installation Steps

### Step 1: Check Prerequisites

Run these commands to verify:

```bash
# Check Node.js
node --version

# Check Python 3
python3 --version

# Check if lark-cli is installed
lark-cli --version

# Check if claude is installed
claude --version
```

If `lark-cli` is missing, install it:
```bash
npm install -g @larksuite/cli
```

### Step 2: Clone or Download

If user hasn't cloned yet:
```bash
cd ~/.claude/skills
git clone https://github.com/sundaygod1207/skills.git
```

Or if using subdirectory:
```bash
cd ~/.claude/skills
# The skill-feishu folder should be inside the skills repo
```

### Step 3: Run Installation Script

```bash
cd ~/.claude/skills/skills/skill-feishu
bash install.sh
```

### Step 4: Configure User ID

After installation, the user MUST configure their Lark User ID:

1. Get User ID:
   ```bash
   lark-cli auth status
   ```
   Look for `userOpenId` (format: `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

2. Edit the poller script:
   ```bash
   nano ~/.lark-cli/feishu-poller.py
   ```

3. Find this line:
   ```python
   USER_ID = "请替换为你的用户 ID"
   ```

4. Replace with actual User ID:
   ```python
   USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

### Step 5: Configure Lark App (if not done)

Refer to `BOT_SETUP.md` for detailed steps:
1. Create Lark app at https://open.feishu.cn/app
2. Add Bot capability
3. Grant permissions: `im:message`, `im:chat`
4. Get App ID and App Secret
5. Run: `lark-cli config init --new`

### Step 6: Login to Lark

```bash
lark-cli auth login --recommend
```

### Step 7: Start Poller

```bash
python3 ~/.lark-cli/feishu-poller.py
```

Or run in background:
```bash
nohup python3 ~/.lark-cli/feishu-poller.py > ~/.lark-cli/poller.log 2>&1 &
```

---

## Verification

After installation, verify:

1. **Check poller is running**:
   ```bash
   ps aux | grep feishu-poller
   ```

2. **Check logs**:
   ```bash
   tail -20 ~/.lark-cli/poller.log
   ```

3. **Test with Lark message**:
   Tell user to send "查看状态" to the bot in Lark

---

## Troubleshooting

### Issue: Poller not starting

Check Python version:
```bash
python3 --version
```

Check for errors:
```bash
python3 ~/.lark-cli/feishu-poller.py 2>&1
```

### Issue: User ID not configured

Check the config file:
```bash
grep USER_ID ~/.lark-cli/feishu-poller.py
```

If it shows "请替换为", guide user to replace with their actual User ID.

### Issue: Lark not logged in

Check auth status:
```bash
lark-cli auth status
```

If not logged in:
```bash
lark-cli auth login --recommend
```

### Issue: Permission denied for commands

Check Claude settings:
```bash
cat ~/.claude/settings.json | grep -A 10 permission_presets
```

If missing, help user add:
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

---

## Key Files

| File | Purpose |
|------|---------|
| `~/.lark-cli/feishu-poller.py` | Main poller script |
| `~/.lark-cli/feishu-claude-trigger.py` | Claude task trigger |
| `~/.lark-cli/config.json` | Lark app config |
| `~/.lark-cli/poller.log` | Poller logs |
| `~/.claude/settings.json` | Claude permission presets |

---

## Important Notes

1. **User ID is required**: The skill won't work without a valid Lark User ID
2. **Lark app must be configured**: Bot capability and permissions are required
3. **Poller runs continuously**: Recommend running in background with nohup
4. **Logs are important**: Check `poller.log` for debugging

---

## For AI Assistants

If the user asks you to install this skill:

1. **First**: Check if prerequisites are installed
2. **Then**: Clone/download the repo and run install.sh
3. **Important**: Guide user to configure their User ID
4. **Finally**: Start the poller and verify it works

If something fails, check the logs and error messages.

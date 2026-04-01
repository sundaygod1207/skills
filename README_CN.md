# skill-feishu 用户说明书

> 把 Claude Code 接入飞书，实现真正的双向交互
> 上班用飞书发消息，家里 Claude Code 自动执行任务并回复结果

---

## 快速开始（5 分钟上手）

### 前提条件

确保你已经安装：
- [ ] Node.js（用于飞书 CLI）
- [ ] Python 3（用于轮询脚本）
- [ ] Claude Code

### 安装步骤

**1. 安装飞书 CLI**
```bash
npm install -g @larksuite/cli
```

**2. 克隆项目**
```bash
git clone https://github.com/sundaygod1207/skills.git
cd skills/skill-feishu
```

**3. 运行安装脚本**
```bash
bash install.sh
```

**4. 登录飞书**
```bash
lark-cli auth login --recommend
```

**5. 获取你的用户 ID**
```bash
lark-cli auth status
```
输出中找到 `userOpenId`，类似 `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**6. 编辑配置文件**
```bash
nano ~/.lark-cli/feishu-poller.py
```
把 `USER_ID = "请替换为你的用户 ID"` 改成：
```python
USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 你的真实用户 ID
```

**7. 启动轮询**
```bash
python3 ~/.lark-cli/feishu-poller.py
```

或者后台运行：
```bash
nohup python3 ~/.lark-cli/feishu-poller.py > ~/.lark-cli/poller.log 2>&1 &
```

---

## 飞书应用配置

### 创建飞书应用

1. 访问飞书开放平台：https://open.feishu.cn/app
2. 点击"创建应用" → "企业自建"
3. 填写应用名称（如：我的个人助手）
4. 创建完成后，在"凭证与基础信息"获取：
   - App ID
   - App Secret

### 添加机器人能力

1. 在应用管理页面，点击"添加能力"
2. 选择"机器人"
3. 配置机器人名称和头像

### 配置权限

在"权限管理"页面，添加以下权限：
- `im:message` - 发送消息
- `im:chat` - 读写聊天消息
- `contact:user.base:readonly` - 读取用户信息

### 初始化配置

```bash
lark-cli config init --new
```

按照提示输入 App ID 和 App Secret。

---

## 使用方法

### 预设命令

在飞书上给机器人发送以下消息：

| 消息 | 功能 | 示例回复 |
|------|------|---------|
| `查看状态` | 执行 `uptime` | `11:00 up 1 day, 3 users, load averages: 1.2 1.3 1.3` |
| `查看磁盘` | 执行 `df -h` | 磁盘使用情况 |
| `查看内存` | 执行 `free -h` | 内存使用情况 |
| `开始工作` | 启动 Claude Code | 启动 Claude |
| `停止所有任务` | 停止所有 Claude 任务 | 停止所有 Claude 进程 |

### Claude 任务

发送任意消息（非预设命令）会自动触发 Claude Code 处理：

**示例 1：写代码**
```
帮我写一个 Python 脚本，打印斐波那契数列前 10 个数
```

**示例 2：写文档**
```
帮我写一份项目 README，介绍这个项目的功能和安装方法
```

**示例 3：查询信息**
```
查一下今天有什么热点新闻
```

### 工作流程

1. 飞书发送消息
2. 收到 "🕐 收到，正在处理..."
3. Claude Code 执行任务（后台运行）
4. 收到 "✅ 任务完成" + 结果

---

## 高级配置

### 自定义命令

编辑 `~/.lark-cli/feishu-poller.py`，修改 `COMMANDS` 字典：

```python
COMMANDS = {
    "重启电脑": "sudo reboot",
    "关机": "sudo shutdown -h now",
    "你的命令": "实际执行的命令",
}
```

### 修改轮询间隔

```python
POLL_INTERVAL = 5  # 轮询间隔（秒）
```

### 查看日志

```bash
# 实时查看
tail -f ~/.lark-cli/poller.log

# 查看最近 100 行
tail -100 ~/.lark-cli/poller.log
```

---

## 常见问题

### Q: 消息重复处理怎么办？
A: 确保 `last-message-id.txt` 文件存在且内容正确。如果问题持续，重启轮询脚本。

### Q: 飞书收不到回复？
A: 检查：
1. 飞书应用是否配置了机器人
2. 是否有 `im:message` 权限
3. `lark-cli auth status` 是否正常

### Q: Claude 任务卡住不动？
A: 检查权限预设是否配置正确，或者查看 `~/.lark-cli/claude-trigger.log`

### Q: 可以多人使用吗？
A: 当前版本只支持单一用户 ID。多人使用需要修改代码支持多用户。

---

## 安全提醒

1. **Token 保护**：`config.json` 包含 App Secret，不要提交到 git
2. **命令白名单**：只授权安全的命令，不要授权 `rm -rf`、`sudo` 等危险命令
3. **权限最小化**：机器人只给必要的 API 权限
4. **日志审计**：定期查看 `poller.log`

---

## 项目结构

```
skill-feishu/
├── SKILL.md              # Skill 定义文件
├── README.md             # GitHub README
├── README_CN.md          # 中文说明书（本文件）
├── README_EN.md          # English Guide
├── install.sh            # 安装脚本
├── feishu-poller.py      # 轮询脚本
├── feishu-claude-trigger.py  # Claude 触发器
└── BOT_SETUP.md          # 飞书机器人配置指南
```

---

## 更新日志

### v1.0.0 (2026-04-01)
- 首次发布
- 飞书消息接收
- Claude 任务触发
- 自动回复结果
- 权限预设配置

---

## 反馈与支持

- GitHub Issues: https://github.com/sundaygod1207/skills/issues
- 作者邮箱：macmini2603@163.com

# skill-feishu - 飞书双向交互 Skill

> 把 Claude Code 接入飞书，实现真正的双向交互
> 上班用飞书发消息，家里 Claude Code 自动执行任务并回复结果

## 和网上教程的区别

**其他教程的方案**：
- 只能单向通知（Claude 完成任务 → 飞书收到通知）
- 不能接收飞书消息并执行任务
- 每次执行都需要人工确认权限

**我们的方案**：
- ✅ 飞书 → Claude Code：发送任务
- ✅ Claude Code → 飞书：回复结果
- ✅ 权限预设配置，全程自动化，无需人工干预

## 快速开始

### 1. 安装依赖

```bash
# 安装飞书 CLI
npm install -g @larksuite/cli

# 安装 Claude Code（如果没有）
# 参考官方文档：https://claude.ai/code
```

### 2. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/skill-feishu.git
cd skill-feishu
```

### 3. 运行安装脚本

```bash
bash install.sh
```

### 4. 配置飞书应用

参考 [BOT_SETUP.md](BOT_SETUP.md) 完成飞书应用创建和权限配置。

### 5. 登录飞书

```bash
lark-cli auth login --recommend
```

### 6. 启动轮询

```bash
python3 ~/.lark-cli/feishu-poller.py
```

## 使用方法

### 预设命令

在飞书上发送以下消息：

| 消息 | 功能 |
|------|------|
| `查看状态` | 执行 `uptime`，查看系统状态 |
| `查看磁盘` | 执行 `df -h`，查看磁盘使用 |
| `查看内存` | 执行 `free -h`，查看内存使用 |
| `开始工作` | 启动 Claude Code |
| `停止所有任务` | 停止所有 Claude 任务 |

### Claude 任务

发送任意消息（非预设命令）会自动触发 Claude Code 处理：

```
帮我写一个 Python 脚本，统计系统资源使用情况
```

Claude 会执行任务并把结果发回飞书。

## 项目结构

```
~/.lark-cli/
├── config.json                    # 飞书应用配置
├── feishu-poller.py              # 轮询脚本
├── feishu-claude-trigger.py      # Claude 触发器
├── BOT_SETUP.md                  # 机器人配置指南
├── poller.log                    # 轮询日志
├── claude-trigger.log            # Claude 触发日志
└── claude-tasks/                 # Claude 任务目录
```

## 安全提醒

1. **Token 保护**：`config.json` 包含 App Secret，不要提交到 git
2. **命令白名单**：只授权安全的命令，不要授权 `rm -rf`、`sudo` 等危险命令
3. **权限最小化**：机器人只给必要的 API 权限
4. **日志审计**：定期查看 `poller.log`

## 待完善功能

- [ ] 消息引用（回复时引用原消息）
- [ ] 任务中断（按任务 ID 停止）
- [ ] 撤销"处理中"状态
- [ ] 多轮对话上下文
- [ ] 开机自启动

## 相关文章

- [我把 Claude Code 接入了飞书，上班也能远程控制家里电脑](TODO: 公众号文章链接)

## 文档

- [中文说明书](README_CN.md) - 详细安装和使用指南
- [English Guide](README_EN.md) - Installation and usage guide
- [AI 助手指南](INSTALL_GUIDE_FOR_AI.md) - 给 Claude Code/OpenClaw 的安装说明

## License

MIT

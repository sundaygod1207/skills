# 飞书机器人配置指南

## 为什么需要 Bot

- **接收消息**：可以用 User Identity（已完成）
- **发送消息**：需要 Bot Identity（需要配置）

## 创建机器人步骤

### 1. 打开飞书开放平台
访问：https://open.feishu.cn/app

### 2. 创建企业自建应用
1. 点击"创建应用"
2. 选择"企业自建"
3. 填写应用名称（如：我的个人助手）
4. 选择所属企业
5. 点击"创建"

### 3. 添加机器人能力
1. 在应用管理页面，点击"添加能力"
2. 选择"机器人"
3. 配置机器人名称和头像

### 4. 配置权限
在"权限管理"页面，添加以下权限：
- `im:message` - 发送消息
- `im:chat` - 读写聊天消息
- `contact:user.base:readonly` - 读取用户信息

### 5. 获取凭证
在"凭证与基础信息"页面，记录：
- App ID
- App Secret

### 6. 更新配置
```bash
# 备份当前配置
cp ~/.lark-cli/config.json ~/.lark-cli/config-user.json

# 重新初始化（使用新的 Bot App ID/Secret）
lark-cli config init --new
```

### 7. 测试
```bash
# 发送测试消息（替换为你的用户 ID）
lark-cli im +messages-send --user-id ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --text "测试消息"
```

## 当前状态

- ✅ User Identity 已登录
- ✅ 可以接收消息
- ❌ 无法发送消息（需要 Bot）

## 临时方案

在创建 Bot 之前，轮询脚本会：
- 接收消息
- 执行命令
- 将结果记录到日志（不发送回复）

日志文件：`~/.lark-cli/poller.log`

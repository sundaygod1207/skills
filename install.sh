#!/bin/bash
# skill-feishu 安装脚本
# 用法：bash install.sh

set -e

SKILL_DIR="$HOME/.claude/skills/skill-feishu"
LARK_DIR="$HOME/.lark-cli"

echo "=========================================="
echo "skill-feishu 安装脚本"
echo "=========================================="

# 1. 检查依赖
echo ""
echo "[1/5] 检查依赖..."

if ! command -v lark-cli &> /dev/null; then
    echo "❌ 未找到 lark-cli，请先安装："
    echo "   npm install -g @larksuite/cli"
    exit 1
fi
echo "✅ lark-cli 已安装"

if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3"
    exit 1
fi
echo "✅ python3 已安装"

if ! command -v claude &> /dev/null; then
    echo "❌ 未找到 claude 命令"
    exit 1
fi
echo "✅ claude 已安装"

# 2. 创建目录
echo ""
echo "[2/5] 创建目录..."

mkdir -p "$LARK_DIR"
mkdir -p "$LARK_DIR/claude-tasks"
echo "✅ 目录创建完成"

# 3. 复制文件
echo ""
echo "[3/5] 复制文件..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp -n "$SCRIPT_DIR/feishu-poller.py" "$LARK_DIR/feishu-poller.py" 2>/dev/null || echo "   feishu-poller.py 已存在，跳过"
cp -n "$SCRIPT_DIR/feishu-claude-trigger.py" "$LARK_DIR/feishu-claude-trigger.py" 2>/dev/null || echo "   feishu-claude-trigger.py 已存在，跳过"

echo "✅ 文件复制完成"

# 4. 配置权限预设
echo ""
echo "[4/5] 配置权限预设..."

SETTINGS_FILE="$HOME/.claude/settings.json"

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "❌ 未找到 settings.json，请先运行一次 claude 命令"
    exit 1
fi

# 检查是否已有 permission_presets
if grep -q "permission_presets" "$SETTINGS_FILE"; then
    echo "   permission_presets 已存在，跳过"
else
    echo "⚠️  需要手动配置权限预设"
    echo "   请编辑 $SETTINGS_FILE，添加："
    echo ""
    echo '   "permission_presets": {'
    echo '     "allowed_tools": ["Bash", "Write", "Read", "Edit"],'
    echo '     "allow_bash": ["lark-cli*", "uptime", "df*", "free*"],'
    echo '     "readonly_dirs": ["~/.lark-cli", "~/"],'
    echo '     "writable_dirs": ["~/.lark-cli", "/tmp/"]'
    echo '   }'
fi

echo "✅ 权限预设配置完成"

# 5. 飞书登录检查
echo ""
echo "[5/5] 检查飞书登录状态..."

if lark-cli auth status 2>&1 | grep -q "valid"; then
    echo "✅ 飞书已登录"
else
    echo "⚠️  飞书未登录，请运行："
    echo "   lark-cli auth login --recommend"
fi

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 配置飞书应用（参考 BOT_SETUP.md）"
echo "2. 登录飞书：lark-cli auth login --recommend"
echo "3. 启动轮询：python3 $LARK_DIR/feishu-poller.py"
echo ""

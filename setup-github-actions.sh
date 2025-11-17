#!/bin/bash

# GitHub Actions 自动推送 - 快速配置脚本
# 用途：自动配置TrendRadar推送新闻到个人GitHub仓库

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     TrendRadar - GitHub Actions 自动推送配置向导              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 检查必要文件
if [ ! -f "config/config.yaml" ]; then
    echo "❌ 错误: 未找到 config/config.yaml 文件"
    exit 1
fi

echo "📋 当前配置检查..."
echo ""

# 读取当前配置
CURRENT_REPO=$(python3 -c "import yaml; config=yaml.safe_load(open('config/config.yaml')); print(config.get('github', {}).get('repo_url', '未配置'))" 2>/dev/null || echo "未配置")
CURRENT_BRANCH=$(python3 -c "import yaml; config=yaml.safe_load(open('config/config.yaml')); print(config.get('github', {}).get('branch', 'main'))" 2>/dev/null || echo "main")
CURRENT_ENABLED=$(python3 -c "import yaml; config=yaml.safe_load(open('config/config.yaml')); print(config.get('github', {}).get('enabled', False))" 2>/dev/null || echo "False")

echo "✅ 当前仓库: $CURRENT_REPO"
echo "✅ 当前分支: $CURRENT_BRANCH"
echo "✅ 启用状态: $CURRENT_ENABLED"
echo ""

# 询问是否继续
read -p "是否要更新配置？(y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 配置已取消"
    exit 0
fi

# 输入仓库信息
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "第1步: 配置目标仓库"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "请输入您的GitHub仓库信息："
echo "格式: https://github.com/用户名/仓库名.git"
echo "示例: https://github.com/difyz9/QuickNote.git"
echo ""
read -p "仓库地址: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 仓库地址不能为空"
    exit 1
fi

# 验证仓库地址格式
if [[ ! $REPO_URL =~ ^https://github\.com/[^/]+/[^/]+\.git$ ]]; then
    echo "⚠️  仓库地址格式可能不正确，但将继续..."
fi

# 输入分支名
echo ""
read -p "目标分支 (默认: main): " BRANCH
BRANCH=${BRANCH:-main}

# 更新config.yaml
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "第2步: 更新配置文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 使用Python更新配置
python3 << EOF
import yaml

with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

if 'github' not in config:
    config['github'] = {}

config['github']['enabled'] = True
config['github']['repo_url'] = '$REPO_URL'
config['github']['branch'] = '$BRANCH'
config['github']['token'] = ''  # Actions环境下使用Secret

with open('config/config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

print('✅ 配置文件已更新')
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "第3步: GitHub Token配置说明"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  重要: 您需要在GitHub上配置Personal Access Token"
echo ""
echo "步骤："
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token' → 'Generate new token (classic)'"
echo "3. 设置:"
echo "   - Note: TrendRadar Auto Push"
echo "   - Expiration: 90 days 或更长"
echo "   - Scopes: 勾选 'repo' (完整仓库权限)"
echo "4. 点击 'Generate token' 并复制生成的token"
echo ""
echo "5. 在TrendRadar仓库中添加Secret:"
echo "   - 进入: Settings → Secrets and variables → Actions"
echo "   - 点击 'New repository secret'"
echo "   - Name: PERSONAL_GITHUB_TOKEN"
echo "   - Value: 粘贴刚才复制的token"
echo "   - 点击 'Add secret'"
echo ""

read -p "按回车键继续..." 

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "第4步: 提交配置到GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "⚠️  当前不在Git仓库中，请手动提交配置文件"
    echo ""
    echo "手动提交命令:"
    echo "  git add config/config.yaml .github/workflows/crawler.yml"
    echo "  git commit -m 'Configure GitHub Actions auto push'"
    echo "  git push"
    exit 0
fi

read -p "是否现在提交并推送配置？(y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add config/config.yaml .github/workflows/crawler.yml GITHUB_ACTIONS_SETUP.md
    git commit -m "⚙️ Configure GitHub Actions auto push to $REPO_URL" || true
    git push
    echo "✅ 配置已提交到GitHub"
else
    echo "⚠️  请记得手动提交配置文件"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "配置完成摘要"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 目标仓库: $REPO_URL"
echo "✅ 目标分支: $BRANCH"
echo "✅ 配置文件: config/config.yaml (已更新)"
echo "✅ Actions配置: .github/workflows/crawler.yml (已就绪)"
echo ""
echo "📋 下一步操作:"
echo "  1. 在GitHub上生成Personal Access Token"
echo "  2. 在TrendRadar仓库中添加Secret: PERSONAL_GITHUB_TOKEN"
echo "  3. 手动触发测试: Actions → Hot News Crawler → Run workflow"
echo "  4. 查看运行日志确认推送成功"
echo ""
echo "📚 详细文档: 请查看 GITHUB_ACTIONS_SETUP.md"
echo ""
echo "🎉 配置完成！GitHub Actions将自动推送新闻到您的仓库！"
echo ""

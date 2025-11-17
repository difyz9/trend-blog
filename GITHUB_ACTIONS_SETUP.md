# GitHub Actions 自动推送配置指南

## 功能说明

通过GitHub Actions自动化流程，TrendRadar会：
1. ⏰ 每小时自动抓取热点新闻
2. 📝 生成Markdown格式的新闻报告
3. 🚀 自动推送到您的个人GitHub仓库
4. 🌐 通过GitHub Pages展示新闻内容

## 配置步骤

### 1. 创建GitHub Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置Token信息：
   - **Note**: `TrendRadar Auto Push`
   - **Expiration**: 选择有效期（建议90天或更长）
   - **Select scopes**: 勾选以下权限
     - ✅ `repo` (完整仓库权限)
     - ✅ `workflow` (工作流权限，如果需要)
4. 点击 "Generate token"
5. **重要**: 复制生成的token（只显示一次！）

### 2. 配置GitHub Secrets

在 **TrendRadar仓库** 中设置Secrets：

1. 进入仓库页面 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加以下Secret：
   - **Name**: `PERSONAL_GITHUB_TOKEN`
   - **Value**: 粘贴刚才生成的Token
4. 点击 "Add secret"

### 3. 配置目标仓库信息

编辑 `config/config.yaml` 文件，添加或修改GitHub配置：

```yaml
github:
  enabled: true
  repo_url: https://github.com/你的用户名/你的仓库名.git
  branch: main  # 或其他分支名
  local_path: output/github_repo
  token: ""  # Actions环境下会自动使用 PERSONAL_GITHUB_TOKEN
```

**示例配置**：
```yaml
github:
  enabled: true
  repo_url: https://github.com/difyz9/QuickNote.git
  branch: main
  local_path: output/github_repo
  token: ""
```

### 4. 启用GitHub Pages（可选）

如果您想通过网页访问新闻内容：

1. 进入 **个人仓库**（如QuickNote）→ Settings → Pages
2. 在 "Source" 中选择：
   - Branch: `main` (或您配置的分支)
   - Folder: `/docs` 
3. 点击 "Save"
4. 等待几分钟，访问 `https://你的用户名.github.io/仓库名/news/`

## 工作流程说明

### 自动运行
- ⏰ 每小时整点自动运行
- 📍 可在 `.github/workflows/crawler.yml` 中修改定时规则

### 手动触发
1. 进入仓库 → Actions → Hot News Crawler
2. 点击 "Run workflow" → "Run workflow"

### 推送逻辑
```
1. 运行 main.py 抓取新闻
2. 生成 output/markdown/*.md 文件
3. 克隆个人仓库到 personal_repo/
4. 复制Markdown文件到 personal_repo/docs/news/
5. 提交并推送更改
6. 清理临时文件
```

## 目录结构

### TrendRadar仓库
```
TrendRadar/
├── output/
│   └── markdown/
│       └── 热点新闻_20250117.md  # 生成的新闻文件
├── config/
│   └── config.yaml  # 配置文件
└── .github/
    └── workflows/
        └── crawler.yml  # Actions配置
```

### 个人仓库（如QuickNote）
```
QuickNote/
└── docs/
    └── news/
        ├── 热点新闻_20250117.md
        ├── 热点新闻_20250116.md
        └── ...
```

## 常见问题

### Q1: 推送失败，提示权限错误
**A**: 检查以下内容：
1. Token是否已过期？访问 https://github.com/settings/tokens 检查
2. Token是否有 `repo` 权限？
3. Secret名称是否为 `PERSONAL_GITHUB_TOKEN`？
4. 目标仓库是否存在？

### Q2: 没有生成Markdown文件
**A**: 检查以下内容：
1. `config/config.yaml` 中 `github.enabled` 是否为 `true`
2. 查看Actions日志中的错误信息
3. 确认 `main.py` 正常运行

### Q3: GitHub Pages无法访问
**A**: 
1. 确认Pages已启用且选择了正确的分支和目录
2. 等待3-5分钟让GitHub构建页面
3. 检查文件是否在 `docs/news/` 目录下

### Q4: 如何修改推送频率？
**A**: 编辑 `.github/workflows/crawler.yml`：
```yaml
on:
  schedule:
    - cron: "0 */2 * * *"  # 改为每2小时运行
    # - cron: "*/30 * * * *"  # 改为每30分钟运行
    # - cron: "0 8,20 * * *"  # 改为每天8点和20点运行
```

### Q5: 如何自定义推送目录？
**A**: 修改 `crawler.yml` 中的推送步骤：
```bash
# 将 docs/news 改为您想要的目录
mkdir -p docs/你的目录名
cp -r ../output/markdown/* docs/你的目录名/
```

## 安全建议

1. ✅ 使用GitHub Secrets存储Token，**不要**直接写在代码中
2. ✅ Token设置合理的过期时间，定期更新
3. ✅ 只授予必要的权限（repo权限即可）
4. ✅ 不要在公开场合分享Token
5. ✅ 定期检查Token使用情况

## 测试配置

### 本地测试
```bash
# 测试Markdown生成
python main.py

# 测试GitHub推送（需要在config.yaml中配置token）
python test_github_push.py
```

### GitHub Actions测试
1. 提交配置文件
2. 手动触发workflow：Actions → Hot News Crawler → Run workflow
3. 查看运行日志，确认推送成功

## 查看运行日志

1. 进入仓库 → Actions
2. 点击最新的workflow运行
3. 展开 "Push news to personal repository" 步骤
4. 查看详细日志

## 相关链接

- 📚 GitHub Actions文档: https://docs.github.com/actions
- 🔑 Token管理: https://github.com/settings/tokens
- 📄 GitHub Pages文档: https://docs.github.com/pages
- 🌐 示例仓库: https://github.com/difyz9/QuickNote

---

**配置完成后，TrendRadar将自动为您推送最新的热点新闻！** 🎉

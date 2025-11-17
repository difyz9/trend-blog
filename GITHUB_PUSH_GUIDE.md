# GitHub数据推送功能使用指南

TrendRadar 现已支持将热点新闻数据自动转换为Markdown格式，并推送到你的GitHub私人仓库，方便通过GitHub Pages展示或多端查看。

## 📋 功能特点

- ✅ 自动生成Markdown格式的新闻报告
- ✅ 支持推送到GitHub私人仓库
- ✅ 自动创建索引文件(README.md)
- ✅ 支持HTTPS和SSH两种认证方式
- ✅ 可配合GitHub Pages展示内容
- ✅ 保留完整的历史记录

## 🚀 快速开始

### 1. 创建GitHub仓库

1. 在GitHub上创建一个新的**私人仓库**（如：`my-news-blog`）
2. 仓库可以是空的，程序会自动初始化

### 2. 获取GitHub Token

如果使用HTTPS方式（推荐新手），需要创建Personal Access Token：

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击"Generate new token (classic)"
3. 设置：
   - **Note**: 填写 `TrendRadar`
   - **Expiration**: 选择有效期（建议90天或更长）
   - **Scopes**: 勾选 `repo`（完整仓库访问权限）
4. 点击"Generate token"
5. **立即复制并保存token**（只显示一次）

### 3. 配置TrendRadar

编辑 `config/config.yaml` 文件：

```yaml
github:
  enabled: true  # 启用GitHub推送
  repo_url: "https://github.com/你的用户名/my-news-blog.git"  # 你的仓库地址
  token: "ghp_xxxxxxxxxxxxxxxxxxxx"  # 你的GitHub Token
  branch: "main"  # 推送的分支
  local_path: "output/github_repo"  # 本地克隆路径
  commit_message: "🔥 更新热点新闻: {date}"  # 提交信息模板
```

**配置说明：**

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `enabled` | 是否启用GitHub推送 | `true` / `false` |
| `repo_url` | GitHub仓库地址 | HTTPS: `https://github.com/username/repo.git`<br>SSH: `git@github.com:username/repo.git` |
| `token` | GitHub Token | HTTPS必填，SSH留空 |
| `branch` | 推送分支 | `main` 或 `master` |
| `local_path` | 本地克隆路径 | 默认 `output/github_repo` |
| `commit_message` | 提交信息模板 | `{date}` 会被替换为当前时间 |

### 4. 运行测试

运行TrendRadar后，程序会：
1. 生成Markdown格式的新闻报告
2. 自动克隆仓库（首次运行）
3. 将报告推送到GitHub

查看日志确认推送成功：
```
✅ Markdown报告已生成: output/markdown/热点新闻_20250117_1430.md
✅ 已复制: output/markdown/热点新闻_20250117_1430.md -> output/github_repo/posts/热点新闻_20250117_1430.md
✅ 已更新索引文件: README.md
✅ 提交成功: 🔥 更新热点新闻: 2025-01-17 14:30
✅ 推送成功到 main 分支
```

## 📂 仓库结构

推送后的GitHub仓库结构：

```
my-news-blog/
├── README.md           # 自动生成的索引文件，列出最近20篇新闻
└── posts/              # 新闻文章目录
    ├── 热点新闻_20250117_1430.md
    ├── 热点新闻_20250117_1200.md
    └── ...
```

## 🌐 配置GitHub Pages（可选）

如果想通过网页访问新闻内容：

### 方法1：使用默认主题

1. 进入仓库 Settings → Pages
2. **Source** 选择 `Deploy from a branch`
3. **Branch** 选择 `main` → `/root`
4. 点击 Save
5. 等待几分钟，访问 `https://你的用户名.github.io/my-news-blog/`

### 方法2：使用博客框架（进阶）

可以使用以下框架展示Markdown内容：

- **VitePress**: 现代化文档站点生成器
- **Hugo**: 快速的静态网站生成器
- **Jekyll**: GitHub原生支持的静态网站生成器
- **Docusaurus**: Facebook出品的文档网站框架

具体配置请参考各框架文档。

## 🔐 安全建议

### ✅ 推荐做法

1. **使用GitHub Secrets（GitHub Actions部署）**
   - Fork仓库后，在 Settings → Secrets 添加 `GITHUB_TOKEN`
   - 在 `config.yaml` 中 token 留空
   - 使用环境变量：`token: ""`

2. **使用SSH密钥（本地部署）**
   ```yaml
   github:
     enabled: true
     repo_url: "git@github.com:username/repo.git"  # SSH格式
     token: ""  # SSH方式不需要token
   ```

3. **设置Token过期时间**
   - 定期更换Token（建议90天）
   - 只授予必要的权限（repo权限即可）

### ❌ 避免做法

- ❌ 不要将token直接写入配置文件并提交到公开仓库
- ❌ 不要使用永不过期的token
- ❌ 不要授予token过多权限

## 🛠️ 常见问题

### Q1: 推送失败：Authentication failed

**原因：** Token无效或权限不足

**解决方法：**
1. 检查token是否正确复制（没有多余空格）
2. 确认token有`repo`权限
3. 检查token是否过期
4. 重新生成token并更新配置

### Q2: 推送失败：Repository not found

**原因：** 仓库地址错误或无访问权限

**解决方法：**
1. 确认仓库地址格式正确
2. 确认仓库存在且未被删除
3. 确认token对应账号有仓库访问权限

### Q3: 克隆仓库很慢

**原因：** 网络问题

**解决方法：**
1. 使用代理（配置Git代理）
2. 使用SSH方式（通常比HTTPS快）
3. 考虑使用国内Git加速服务

### Q4: 想要修改Markdown样式

**解决方法：**
编辑 `markdown_generator.py`，自定义Markdown模板格式。

### Q5: 如何清理旧的新闻文件

**手动方式：**
1. 进入仓库的posts目录
2. 删除旧文件
3. 提交更改

**自动方式：**
可以编写脚本定期清理，例如只保留最近30天的文件。

## 📊 使用场景

### 场景1：个人新闻归档
- 每天自动记录关心的热点
- 通过GitHub保存完整历史
- 随时回顾过去的新闻

### 场景2：团队信息共享
- 将新闻推送到团队共享仓库
- 团队成员通过GitHub Pages查看
- 支持评论和讨论（GitHub Issues）

### 场景3：内容创作素材
- 自动收集热点话题
- Markdown格式便于二次编辑
- 快速找到创作灵感

## 🔄 工作流程

```
TrendRadar运行
    ↓
生成HTML报告（本地查看）
    ↓
转换为Markdown格式
    ↓
推送到GitHub仓库
    ↓
GitHub Pages自动部署（可选）
    ↓
通过网页访问新闻内容
```

## 📝 环境变量配置（可选）

如果不想在配置文件中暴露敏感信息，可以使用环境变量：

```bash
# Linux/Mac
export GITHUB_ENABLED=true
export GITHUB_REPO_URL="https://github.com/username/repo.git"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export GITHUB_BRANCH="main"

# Windows PowerShell
$env:GITHUB_ENABLED="true"
$env:GITHUB_REPO_URL="https://github.com/username/repo.git"
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
$env:GITHUB_BRANCH="main"
```

## 🎯 进阶使用

### 自定义Markdown模板

编辑 `markdown_generator.py` 中的 `generate_markdown_report` 函数，可以自定义：

- 报告标题和样式
- 新闻排版格式
- 热度标记emoji
- 页脚信息

### 自动化部署

配合GitHub Actions，可以实现完全自动化：

1. TrendRadar定时运行（GitHub Actions）
2. 自动生成并推送Markdown
3. GitHub Pages自动更新
4. 通知渠道推送摘要链接

## 📞 获取帮助

如遇到问题：

1. 查看程序运行日志
2. 检查GitHub仓库的Commits历史
3. 访问项目GitHub Issues寻求帮助
4. 关注项目公众号获取教程

---

*由 TrendRadar 提供 | [GitHub项目地址](https://github.com/sansan0/TrendRadar)*

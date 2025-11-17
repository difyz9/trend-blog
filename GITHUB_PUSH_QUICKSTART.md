# GitHub推送功能 - 快速配置示例

## ⚡ 5分钟快速配置

### 步骤1：创建GitHub仓库（1分钟）

1. 访问 https://github.com/new
2. 填写仓库名称：`my-news-blog`
3. 选择 **Private**（私人仓库）
4. 点击 "Create repository"

### 步骤2：获取Token（2分钟）

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写：
   - **Note**: `TrendRadar`
   - **Expiration**: `90 days`
   - **Scopes**: 勾选 `repo`
4. 点击 "Generate token"
5. **复制token**（格式类似：`ghp_1234567890abcdefghijklmnopqrstuvwxyz`）

### 步骤3：配置TrendRadar（2分钟）

编辑 `config/config.yaml`：

```yaml
github:
  enabled: true
  repo_url: "https://github.com/你的用户名/my-news-blog.git"
  token: "ghp_你的token"
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

**示例：**

```yaml
github:
  enabled: true
  repo_url: "https://github.com/zhangsan/my-news-blog.git"
  token: "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

### 步骤4：运行测试

运行TrendRadar，查看日志输出：

```bash
python main.py
```

成功日志示例：
```
✅ GitHub推送服务已初始化
GitHub推送已启用: github.com/zhangsan/my-news-blog.git (分支: main)
...
✅ Markdown报告已生成: output/markdown/热点新闻_20250117_1430.md
✅ 推送成功到 main 分支
```

### 步骤5：查看结果

访问你的GitHub仓库：
```
https://github.com/你的用户名/my-news-blog
```

你会看到：
- `README.md` - 自动生成的索引
- `posts/` 目录 - 包含所有新闻Markdown文件

## 🌐 开启GitHub Pages（可选，额外3分钟）

### 步骤1：启用Pages

1. 进入仓库页面
2. 点击 **Settings**
3. 左侧菜单找到 **Pages**
4. **Source** 选择：`Deploy from a branch`
5. **Branch** 选择：`main` / `(root)`
6. 点击 **Save**

### 步骤2：访问网站

等待1-2分钟，访问：
```
https://你的用户名.github.io/my-news-blog/
```

## 🔧 常见配置错误

### ❌ 错误1：仓库地址格式错误

```yaml
# 错误
repo_url: "github.com/user/repo"
repo_url: "https://github.com/user/repo"  # 缺少.git

# 正确
repo_url: "https://github.com/user/repo.git"
```

### ❌ 错误2：Token权限不足

Token必须勾选 `repo` 权限，否则无法推送。

### ❌ 错误3：分支名错误

检查你的仓库默认分支是 `main` 还是 `master`：

```yaml
# GitHub新仓库默认
branch: "main"

# 老仓库可能是
branch: "master"
```

## 📱 使用SSH方式（进阶）

如果你已配置SSH密钥，可以使用SSH方式（更安全）：

```yaml
github:
  enabled: true
  repo_url: "git@github.com:你的用户名/my-news-blog.git"  # SSH格式
  token: ""  # SSH不需要token
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

**前提条件：**
- 已在GitHub添加SSH公钥
- 本地Git配置了SSH密钥

## 🎯 完整配置示例

### 示例1：基础配置（HTTPS）

```yaml
app:
  version_check_url: "https://raw.githubusercontent.com/sansan0/TrendRadar/refs/heads/master/version"
  show_version_update: true

crawler:
  request_interval: 1000
  enable_crawler: true
  use_proxy: false
  default_proxy: "http://127.0.0.1:10086"

report:
  mode: "daily"
  rank_threshold: 5

notification:
  enable_notification: true
  webhooks:
    feishu_url: "你的飞书webhook"

github:
  enabled: true
  repo_url: "https://github.com/zhangsan/my-news-blog.git"
  token: "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"

weight:
  rank_weight: 0.6
  frequency_weight: 0.3
  hotness_weight: 0.1

platforms:
  - id: "zhihu"
    name: "知乎"
  - id: "weibo"
    name: "微博"
```

### 示例2：SSH配置

```yaml
github:
  enabled: true
  repo_url: "git@github.com:zhangsan/my-news-blog.git"
  token: ""
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

### 示例3：禁用GitHub推送

```yaml
github:
  enabled: false
  repo_url: ""
  token: ""
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

## ✅ 验证配置

运行TrendRadar后，检查以下内容确认成功：

1. **本地文件生成**
   - `output/markdown/` 目录下有 `.md` 文件

2. **GitHub仓库更新**
   - 访问仓库，查看 `posts/` 目录
   - 查看最新的commit记录

3. **日志输出正常**
   ```
   ✅ GitHub推送服务已初始化
   ✅ Markdown报告已生成
   ✅ 推送成功到 main 分支
   ```

## 🆘 需要帮助？

- 查看完整文档：`GITHUB_PUSH_GUIDE.md`
- 项目Issues：https://github.com/sansan0/TrendRadar/issues
- 检查日志输出找到具体错误信息

---

*配置只需5分钟，享受自动化新闻归档！*

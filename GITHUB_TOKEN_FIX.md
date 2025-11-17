# 🔧 GitHub Token 问题修复指南

## ❌ 当前问题

你的GitHub Token已过期或无效，导致无法推送数据。

错误信息：
```
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed
```

## ✅ 解决步骤

### 步骤1：生成新的GitHub Token（3分钟）

1. **打开浏览器，访问：**
   ```
   https://github.com/settings/tokens/new
   ```

2. **填写Token信息：**
   - **Note (描述)**: `TrendRadar`
   - **Expiration (有效期)**: 选择 `90 days` 或 `No expiration`（不推荐永久）
   - **Select scopes (权限)**: ✅ 勾选 `repo`（完整仓库访问权限）

3. **生成Token：**
   - 点击页面底部的绿色按钮 `Generate token`
   - **立即复制Token**（只显示一次！）
   - Token格式：`ghp_` 开头，约40个字符
   - 示例：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 步骤2：更新配置文件（1分钟）

编辑 `config/config.yaml`，找到github配置部分：

```yaml
github:
  enabled: true
  repo_url: "https://github.com/difyz9/QuickNote.git"
  token: "ghp_你的新token粘贴在这里"  # ← 替换这里
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

**注意事项：**
- ✅ Token两侧要有引号
- ✅ 不要有多余的空格
- ✅ 确保仓库地址以 `.git` 结尾
- ✅ 保存后不要提交到公开仓库

### 步骤3：测试推送（1分钟）

运行测试脚本：

```bash
python test_github_push.py
```

你会看到详细的测试步骤：
```
1️⃣ 加载配置...
   ✅ 配置已加载
2️⃣ 检查GitHub配置...
   ✅ 配置检查通过
3️⃣ 生成测试Markdown...
   ✅ Markdown已生成
4️⃣ 初始化GitHub服务...
   ✅ GitHub服务已初始化
5️⃣ 测试GitHub连接...
   ✅ GitHub连接测试成功
6️⃣ 推送文件到GitHub...
   ✅ 文件推送成功！
```

### 步骤4：正式运行

测试通过后，运行完整程序：

```bash
python main.py
```

## 🔐 安全提示

### ⚠️ Token安全性

1. **不要泄露Token**
   - ❌ 不要提交到公开仓库
   - ❌ 不要分享给他人
   - ❌ 不要截图分享

2. **使用环境变量（可选，更安全）**
   ```bash
   # macOS/Linux
   export GITHUB_TOKEN="ghp_你的token"
   
   # Windows PowerShell
   $env:GITHUB_TOKEN="ghp_你的token"
   ```
   
   然后在config.yaml中留空：
   ```yaml
   token: ""  # 从环境变量读取
   ```

3. **定期更换Token**
   - 建议每90天更换一次
   - 如果泄露，立即删除并重新生成

## 🔄 备用方案：使用SSH（更安全）

如果你熟悉SSH密钥，可以改用SSH方式，无需Token：

### 步骤1：生成SSH密钥（如果没有）

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

按提示操作，使用默认路径即可。

### 步骤2：添加SSH公钥到GitHub

1. 复制公钥内容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 访问 https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥内容
5. 点击 "Add SSH key"

### 步骤3：修改配置使用SSH

```yaml
github:
  enabled: true
  repo_url: "git@github.com:difyz9/QuickNote.git"  # SSH格式
  token: ""  # SSH不需要token
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

### 步骤4：测试SSH连接

```bash
ssh -T git@github.com
```

成功输出：
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

## 📋 配置检查清单

完成配置后，确认以下几点：

- [ ] Token已复制并粘贴到配置文件
- [ ] Token有 `repo` 权限
- [ ] 仓库地址格式正确（以.git结尾）
- [ ] 配置文件已保存
- [ ] 测试脚本运行成功
- [ ] 能在GitHub仓库看到推送的文件

## ❓ 常见问题

### Q1: Token在哪里查看？

A: 访问 https://github.com/settings/tokens
   - 可以看到所有Token列表
   - 但无法查看Token内容（只能重新生成）

### Q2: Token需要什么权限？

A: 必须勾选 `repo` 权限（包括所有子权限）

### Q3: Token过期了怎么办？

A: 重新按步骤1生成新Token，然后更新配置

### Q4: 仓库是私有的可以吗？

A: 可以！只要Token有权限即可

### Q5: 能推送到别人的仓库吗？

A: 可以，前提是你有该仓库的写入权限

## 🆘 获取帮助

如果仍然无法解决：

1. 运行测试脚本查看详细错误：
   ```bash
   python test_github_push.py
   ```

2. 检查GitHub Token状态：
   https://github.com/settings/tokens

3. 查看完整文档：
   - `GITHUB_PUSH_GUIDE.md` - 完整使用指南
   - `GITHUB_PUSH_QUICKSTART.md` - 快速配置指南

---

**下一步：** 按照上述步骤操作后，重新运行 `python test_github_push.py` 测试！

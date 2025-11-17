# TrendRadar GitHub推送功能说明

## 🎉 新功能：自动推送到GitHub

TrendRadar现在支持将热点新闻自动转换为Markdown格式，并推送到你的GitHub私人仓库！

### ✨ 主要特性

- 📝 **Markdown格式** - 自动生成美观的Markdown报告
- 🔄 **自动推送** - 每次运行自动推送到GitHub
- 📚 **历史归档** - 保留完整的新闻历史记录
- 🌐 **GitHub Pages** - 可配合GitHub Pages展示内容
- 🔐 **私人仓库** - 支持推送到私人仓库
- 🚀 **零配置** - 支持HTTPS和SSH两种方式

### 📖 快速开始

1. **查看快速配置指南**
   ```bash
   cat GITHUB_PUSH_QUICKSTART.md
   ```
   5分钟完成配置！

2. **查看完整使用文档**
   ```bash
   cat GITHUB_PUSH_GUIDE.md
   ```
   了解所有功能和高级用法

### 🔧 基础配置

编辑 `config/config.yaml`：

```yaml
github:
  enabled: true  # 启用GitHub推送
  repo_url: "https://github.com/你的用户名/仓库名.git"
  token: "你的GitHub_Token"
  branch: "main"
  local_path: "output/github_repo"
  commit_message: "🔥 更新热点新闻: {date}"
```

### 📂 生成的内容

推送到GitHub后的仓库结构：

```
your-repo/
├── README.md                    # 自动生成的索引
└── posts/                       # 新闻文章目录
    ├── 热点新闻_20250117_1430.md
    ├── 热点新闻_20250117_1200.md
    └── ...
```

### 🌐 GitHub Pages展示

启用GitHub Pages后，可通过网页访问：
```
https://你的用户名.github.io/仓库名/
```

### 📋 使用场景

1. **个人新闻归档** - 建立个人新闻数据库
2. **团队信息共享** - 团队成员共享热点信息
3. **内容创作素材** - 快速查找创作灵感
4. **多端同步查看** - 手机、电脑随时访问

### 🔐 安全建议

- ✅ 使用私人仓库保护数据
- ✅ Token定期更换（建议90天）
- ✅ 使用GitHub Secrets存储敏感信息
- ✅ 或使用SSH密钥认证（更安全）

### 📚 相关文档

- [快速配置指南](GITHUB_PUSH_QUICKSTART.md) - 5分钟快速上手
- [完整使用文档](GITHUB_PUSH_GUIDE.md) - 详细功能说明和问题排查

### 🎯 工作流程

```
TrendRadar运行
    ↓
生成HTML报告（本地）
    ↓
生成Markdown报告
    ↓
自动推送到GitHub
    ↓
GitHub Pages更新（可选）
    ↓
通过网页访问内容
```

### 🆘 常见问题

**Q: 如何获取GitHub Token？**
- 访问 GitHub Settings → Developer settings → Personal access tokens
- 创建新Token，勾选 `repo` 权限

**Q: 支持哪些认证方式？**
- HTTPS（需要Token）
- SSH（需要配置SSH密钥）

**Q: 推送失败怎么办？**
- 检查Token是否有效
- 确认仓库地址正确
- 查看程序日志找到具体错误

**Q: 可以推送到已有仓库吗？**
- 可以！程序会自动合并内容

**Q: 如何自定义Markdown样式？**
- 编辑 `markdown_generator.py` 自定义模板

### 🔄 更新说明

本功能在原有功能基础上新增，不影响现有的HTML报告和通知功能。

你可以：
- ✅ 同时使用HTML和Markdown
- ✅ 只使用HTML（禁用GitHub推送）
- ✅ 只使用Markdown（禁用通知）

### 💡 使用建议

1. **首次使用**
   - 先用测试仓库验证配置
   - 确认推送成功后再用正式仓库

2. **定时运行**
   - 配合cron或计划任务定时执行
   - 自动积累新闻数据

3. **数据管理**
   - 定期清理旧文件
   - 可以手动编辑推送的Markdown

---

**需要帮助？**
- 查看文档：`GITHUB_PUSH_GUIDE.md`
- 项目Issues：https://github.com/sansan0/TrendRadar/issues
- 关注项目获取更新

# Markdown 报告生成说明

## 📝 功能概述

程序现在会自动生成两种类型的 Markdown 文件：

### 1. 每小时独立报告
- **文件名格式**: `热点新闻_YYYYMMDD_HHMM.md`
- **示例**: `热点新闻_20251117_1530.md`
- **更新频率**: 每小时生成一个新文件
- **内容**: 当前时间点的热点新闻分析

### 2. 每日汇总报告
- **文件名**: `README.md`
- **更新频率**: 每小时更新一次（覆盖之前的内容）
- **内容**: 当天所有热点新闻的汇总分析

## 📂 文件存储位置

所有 Markdown 文件都存储在日期文件夹下：

```
docs/
└── 2025年11月17日/
    ├── README.md                      # 每日汇总（每小时更新）
    ├── 热点新闻_20251117_0800.md      # 08:00 的报告
    ├── 热点新闻_20251117_0900.md      # 09:00 的报告
    ├── 热点新闻_20251117_1000.md      # 10:00 的报告
    ├── ...
    ├── html/                          # HTML 格式报告
    │   ├── 08时00分.html
    │   ├── 09时00分.html
    │   └── 当日汇总.html
    └── txt/                           # 原始数据
        ├── 08时00分.txt
        └── 09时00分.txt
```

## 🔄 GitHub Actions 自动化

### 执行频率
- **默认**: 每小时整点执行一次 (`cron: "0 * * * *"`)
- 可以在 `.github/workflows/crawler.yml` 中修改

### 提交内容
每次运行会自动提交：
- ✅ 当前时间点的 Markdown 文件
- ✅ 更新的每日汇总 README.md
- ✅ HTML 和 TXT 文件
- ✅ 网站首页 index.html

## 🚀 使用方法

### 方法1：GitHub Actions 自动运行（推荐）
1. 确保 Actions 已启用（仓库 Settings → Actions → Allow all actions）
2. 每小时自动执行，无需手动操作
3. 在 Actions 标签页可以查看运行历史

### 方法2：手动触发
在 GitHub 仓库的 Actions 页面：
1. 选择 "Hot News Crawler" workflow
2. 点击 "Run workflow" 按钮
3. 等待执行完成

### 方法3：本地运行
```bash
# 直接运行
python main.py

# 或使用定时脚本（每小时自动运行）
python run_hourly.py
```

## 📊 Markdown 文件内容

### 包含的信息
- 📰 新闻总数统计
- 🔥 热点词汇分析
- 📱 各平台热点新闻
- 🆕 新增热点标记
- 🔗 新闻链接（可点击）
- 📈 排名和热度信息
- ⏰ 新闻出现时间

### 示例格式
```markdown
# 当日热点汇总

**生成时间：** 2025年11月17日 20:40

## 📊 统计概览

- 📰 **新闻总数：** 451 条
- 🔥 **热点新闻：** 35 条
- 📋 **报告模式：** 当日汇总

## 🔥 热点词汇统计

### 🔥🔥🔥 [1/10] 某个热点话题

**匹配新闻：** 12 条

1. **[微博]** [新闻标题](链接) **[1-5]** `15:28-16:10` (3次)
2. 🆕 **[抖音]** [新闻标题](链接) **[2]** `16:10`
...
```

## 🔧 配置选项

### 修改执行频率
编辑 `.github/workflows/crawler.yml`:

```yaml
schedule:
  - cron: "0 * * * *"      # 每小时整点
  # - cron: "*/30 * * * *"  # 每半小时
  # - cron: "0 9-21 * * *"  # 每天9点到21点，每小时
```

### 修改报告模式
编辑 `config/config.yaml`:

```yaml
report:
  mode: "daily"        # 当日汇总模式
  # mode: "current"    # 当前榜单模式
  # mode: "incremental" # 增量监控模式
```

## ❓ 常见问题

### Q: 为什么 GitHub 上没有看到每小时的 Markdown 文件？
**A**: 检查以下几点：
1. GitHub Actions 是否正常运行（查看 Actions 标签页）
2. 是否有权限问题（Settings → Actions → Workflow permissions）
3. 查看最近的提交记录，确认文件已提交

### Q: 如何查看所有历史 Markdown 文件？
**A**: 访问仓库的 `docs/日期文件夹/` 目录，可以看到所有生成的 Markdown 文件。

### Q: 可以只生成 Markdown 不发送通知吗？
**A**: 可以！在 `config/config.yaml` 中设置：
```yaml
notification:
  enable_notification: false
```

### Q: Markdown 文件可以在 GitHub Pages 上显示吗？
**A**: 可以！GitHub 会自动渲染 Markdown 文件。每个日期文件夹的 `README.md` 会作为该文件夹的默认显示页面。

## 📖 更多信息

- 主项目文档：[README.md](README.md)
- 完整配置说明：[config/config.yaml](config/config.yaml)
- 原始项目：[TrendRadar](https://github.com/sansan0/TrendRadar)

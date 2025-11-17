# 📰 TrendRadar 新闻归档

> 自动生成的热点新闻归档，每小时更新一次

## 📋 说明

此目录包含TrendRadar自动抓取并生成的Markdown格式新闻文件。

- 📅 **更新频率**: 每小时自动更新
- 🤖 **自动化**: 通过GitHub Actions自动运行
- 📝 **格式**: Markdown (.md)
- 🔥 **内容**: 全网热点新闻汇总

## 📂 文件命名规则

```
热点新闻_YYYYMMDD_HHMM.md
```

示例：
- `热点新闻_20251117_1200.md` - 2025年11月17日 12:00的新闻
- `热点新闻_20251117_1300.md` - 2025年11月17日 13:00的新闻

## 🌐 在线访问

如果您启用了GitHub Pages，可以通过以下地址访问：

```
https://你的用户名.github.io/TrendRadar/news/
```

## 📊 新闻来源

新闻数据来自以下平台：
- 知乎热榜
- 微博热搜
- 百度热搜
- bilibili热搜
- 抖音热点
- 今日头条
- 华尔街见闻
- 财联社
- 澎湃新闻
- 凤凰网
- 贴吧热议

## 🔍 查看方式

### 1. GitHub网页查看
直接在GitHub仓库中点击文件查看

### 2. 本地查看
```bash
# 克隆仓库
git clone https://github.com/你的用户名/TrendRadar.git
cd TrendRadar/docs/news

# 查看最新新闻
ls -lt | head -5
```

### 3. GitHub Pages
启用GitHub Pages后，可以通过网页浏览器访问

## ⚙️ 配置说明

新闻内容由以下文件控制：
- `config/config.yaml` - 平台配置、推送模式
- `config/frequency_words.txt` - 关键词过滤

## 📖 相关文档

- [TrendRadar主文档](../../readme.md)
- [GitHub Actions配置指南](../../GITHUB_ACTIONS_SETUP.md)
- [配置说明](../../config/config.yaml)

---

**最后更新**: 由GitHub Actions自动维护
**项目地址**: https://github.com/sansan0/TrendRadar

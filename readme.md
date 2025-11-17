# Trend Blog

热点新闻聚合与分析工具

> 基于 [TrendRadar](https://github.com/sansan0/TrendRadar) 项目

## 核心功能

### 全网热点聚合

监控以下平台热点：
- 知乎、抖音、bilibili热搜
- 华尔街见闻、贴吧、百度热搜
- 财联社热门、澎湃新闻、凤凰网
- 今日头条、微博

### 智能推送策略

三种推送模式：

| 模式 | 推送时机 | 显示内容 |
|------|----------|----------|
| **当日汇总** (daily) | 按时推送 | 当日所有匹配新闻 + 新增新闻 |
| **当前榜单** (current) | 按时推送 | 当前榜单匹配新闻 + 新增新闻 |
| **增量监控** (incremental) | 有新增才推送 | 新出现的匹配频率词新闻 |

### 精准内容筛选

在 `config/frequency_words.txt` 中设置关键词，支持：
- 普通词：基础匹配
- 必须词 (+)：限定范围
- 过滤词 (!)：排除干扰

### 多渠道推送

支持以下通知方式：
- 企业微信、飞书、钉钉
- Telegram、邮件、ntfy

## 配置说明

### 主配置文件

编辑 `config/config.yaml`：

```yaml
# 输出目录配置
output:
  base_dir: "docs"  # 输出基础目录
  html_dir: ""      # HTML文件输出目录
  txt_dir: ""       # TXT文件输出目录
  push_records_dir: "docs/.push_records"

# 注意：Markdown文件会自动保存到 base_dir/日期文件夹/ 下

# 推送模式选择
report:
  mode: "daily"  # 可选: "daily"|"incremental"|"current"
  rank_threshold: 5

# 通知设置
notification:
  enable_notification: true
  webhooks:
    feishu_url: ""      # 飞书机器人URL
    dingtalk_url: ""    # 钉钉机器人URL
    wework_url: ""      # 企业微信机器人URL
    telegram_bot_token: ""
    telegram_chat_id: ""
    email_from: ""
    email_password: ""
    email_to: ""

# 监控平台
platforms:
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  # ... 更多平台
```

### 关键词配置

编辑 `config/frequency_words.txt`：

```txt
# 示例：手机新品类
iPhone
华为
OPPO
+发布

# 示例：股市行情类
A股
上证
深证
+涨跌
!预测
```

### 输出目录结构

```
docs/
├── 2025年11月17日/
│   ├── 热点新闻_20251117_0721.md  ← Markdown文件
│   ├── html/
│   │   └── 当日汇总.html
│   └── txt/
│       └── 07时21分.txt
└── .push_records/
```

## 更新日志

### 2025/11/17 - v3.0.6

- **优化输出目录结构**：Markdown文件直接保存到日期文件夹下
- **简化配置**：移除 `markdown_dir` 配置项
- Markdown文件与html、txt文件处于同一目录级别

## 数据来源

本项目使用 [newsnow](https://github.com/ourongxing/newsnow) 提供的 API 接口获取多平台数据

## 许可证

GPL-3.0 License

## 致谢

本项目基于 [TrendRadar](https://github.com/sansan0/TrendRadar) 开发

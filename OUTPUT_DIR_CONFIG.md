# 输出目录自定义配置说明

本项目已支持用户自定义输出目录，不再强制使用硬编码的 `output` 目录。

## 📋 配置方式

### 1. 通过配置文件配置（推荐）

在 `config/config.yaml` 文件中找到 `output` 配置节：

```yaml
# 输出目录配置
output:
  base_dir: "output"  # 输出基础目录
  markdown_dir: "output/markdown"  # Markdown文件输出目录
  html_dir: ""  # HTML文件输出目录(为空时自动在base_dir下按日期创建)
  txt_dir: ""  # TXT文件输出目录(为空时自动在base_dir下按日期创建)
  push_records_dir: "output/.push_records"  # 推送记录目录
```

#### 配置项说明：

- **`base_dir`**: 输出基础目录
  - 默认值：`output`
  - 说明：所有数据文件的根目录，当其他专用目录未配置时，会在此目录下按日期创建子目录

- **`markdown_dir`**: Markdown文件输出目录
  - 默认值：`output/markdown`
  - 说明：生成的Markdown格式新闻报告的存储位置
  - 用于GitHub推送功能

- **`html_dir`**: HTML文件输出目录
  - 默认值：为空（自动在`base_dir`下按日期创建）
  - 说明：生成的HTML格式新闻报告的存储位置
  - 为空时路径格式：`{base_dir}/YYYY年MM月DD日/html/`

- **`txt_dir`**: TXT文件输出目录
  - 默认值：为空（自动在`base_dir`下按日期创建）
  - 说明：爬取的原始新闻数据文本文件的存储位置
  - 为空时路径格式：`{base_dir}/YYYY年MM月DD日/txt/`

- **`push_records_dir`**: 推送记录目录
  - 默认值：`output/.push_records`
  - 说明：推送时间窗口功能的记录文件存储位置

### 2. 通过环境变量配置（优先级更高）

环境变量会覆盖配置文件中的设置：

```bash
# 基础输出目录
export OUTPUT_BASE_DIR="my_custom_output"

# Markdown输出目录
export OUTPUT_MARKDOWN_DIR="my_reports/markdown"

# HTML输出目录
export OUTPUT_HTML_DIR="my_reports/html"

# TXT输出目录
export OUTPUT_TXT_DIR="my_data/txt"

# 推送记录目录
export OUTPUT_PUSH_RECORDS_DIR="my_data/.push_records"
```

## 🎯 使用场景示例

### 场景1：完全自定义输出目录

```yaml
output:
  base_dir: "news_data"
  markdown_dir: "reports/markdown"
  html_dir: "reports/html"
  txt_dir: "data/raw"
  push_records_dir: "data/.push_records"
```

运行后的目录结构：
```
project/
├── news_data/          # 基础目录（当其他目录未指定时使用）
├── reports/
│   ├── markdown/       # Markdown报告
│   └── html/           # HTML报告
├── data/
│   ├── raw/            # 原始TXT数据
│   └── .push_records/  # 推送记录
```

### 场景2：只修改基础目录

```yaml
output:
  base_dir: "my_output"
  markdown_dir: "my_output/markdown"
  html_dir: ""  # 为空，使用默认按日期分类
  txt_dir: ""   # 为空，使用默认按日期分类
  push_records_dir: "my_output/.push_records"
```

运行后的目录结构：
```
project/
└── my_output/
    ├── markdown/
    ├── .push_records/
    └── 2025年11月17日/
        ├── html/
        └── txt/
```

### 场景3：保持默认配置

如果不修改配置，保持默认值即可：

```yaml
output:
  base_dir: "output"
  markdown_dir: "output/markdown"
  html_dir: ""
  txt_dir: ""
  push_records_dir: "output/.push_records"
```

## 🔧 配置生效范围

配置修改后会影响以下功能：

1. **爬虫数据存储** - TXT文件存储位置
2. **报告生成** - HTML和Markdown报告的输出位置
3. **GitHub推送** - 从配置的markdown_dir读取文件
4. **MCP服务器** - 数据查询会从配置的目录读取
5. **推送时间窗口** - 推送记录存储在配置的目录

## ⚠️ 注意事项

1. **相对路径和绝对路径**
   - 支持相对路径（相对于项目根目录）
   - 支持绝对路径（如 `/Users/username/data`）

2. **目录自动创建**
   - 所有配置的目录在需要时会自动创建，无需手动创建

3. **配置优先级**
   - 环境变量 > 配置文件 > 默认值

4. **MCP服务器兼容性**
   - MCP服务器会自动读取配置文件，无需额外设置
   - 如果配置文件加载失败，会回退到默认的 `output` 目录

5. **Docker部署**
   - 使用Docker时，建议通过环境变量或挂载配置文件来修改目录
   - 确保挂载的数据卷路径与配置的目录一致

## 🚀 迁移现有数据

如果你已经有数据在 `output` 目录中，想要迁移到新目录：

1. 修改配置文件中的目录设置
2. 手动移动现有数据到新目录：
   ```bash
   mv output/markdown my_reports/markdown
   mv output/2025年* my_output/
   ```
3. 或者保持配置不变，继续使用默认的 `output` 目录

## 📝 配置验证

修改配置后，可以通过以下方式验证：

1. **查看启动日志**
   ```bash
   python main.py
   ```
   日志中会显示加载的配置路径

2. **检查文件生成位置**
   - 运行一次爬虫
   - 检查文件是否在配置的目录中生成

3. **MCP服务器测试**
   ```bash
   python mcp_server/server.py
   ```
   确认数据能够正常读取

## 🆘 常见问题

**Q: 修改配置后数据找不到了？**
A: 检查配置的目录路径是否正确，确保数据文件在新的目录位置。

**Q: 环境变量不生效？**
A: 确保环境变量在运行程序前已经设置，可以在命令行中 `echo $OUTPUT_BASE_DIR` 验证。

**Q: MCP服务器读取不到数据？**
A: MCP服务器会自动读取 `config/config.yaml`，确保配置文件存在且格式正确。

**Q: 可以为不同平台设置不同的输出目录吗？**
A: 当前版本暂不支持按平台分目录，所有平台的数据会统一存储在配置的目录中。

---

如有其他问题，请查看项目 README 或提交 Issue。

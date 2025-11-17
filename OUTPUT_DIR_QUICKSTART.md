# 📝 输出目录自定义功能 - 快速使用指南

## 🎯 功能说明

项目现在支持完全自定义输出目录，不再强制使用硬编码的 `output` 目录。你可以：

- ✅ 自定义所有数据文件的存储位置
- ✅ 按功能分离不同类型的文件
- ✅ 通过配置文件或环境变量灵活配置
- ✅ 完全向后兼容，不修改配置时保持默认行为

## 🚀 快速开始

### 1️⃣ 查看当前配置

运行验证脚本查看当前配置：

```bash
python verify_output_config.py
```

### 2️⃣ 修改配置

编辑 `config/config.yaml` 文件，找到 `output` 配置节：

```yaml
# 输出目录配置
output:
  base_dir: "output"              # 基础目录
  markdown_dir: "output/markdown" # Markdown报告目录
  html_dir: ""                    # HTML目录（空则按日期创建）
  txt_dir: ""                     # 原始数据目录（空则按日期创建）
  push_records_dir: "output/.push_records"  # 推送记录目录
```

### 3️⃣ 配置示例

#### 示例1：统一改到 `my_data` 目录

```yaml
output:
  base_dir: "my_data"
  markdown_dir: "my_data/markdown"
  html_dir: ""
  txt_dir: ""
  push_records_dir: "my_data/.push_records"
```

#### 示例2：完全自定义各目录

```yaml
output:
  base_dir: "news_data"
  markdown_dir: "reports/markdown"
  html_dir: "reports/html"
  txt_dir: "data/raw"
  push_records_dir: "data/.push_records"
```

### 4️⃣ 使用环境变量（可选）

环境变量配置优先级更高，适合临时调整或 Docker/CI 部署：

```bash
export OUTPUT_BASE_DIR="custom_output"
export OUTPUT_MARKDOWN_DIR="custom_output/markdown"
python main.py
```

## 📚 配置项详解

| 配置项 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `base_dir` | 基础输出目录 | `output` | `my_data` |
| `markdown_dir` | Markdown报告目录 | `output/markdown` | `reports/md` |
| `html_dir` | HTML报告目录 | 空（按日期创建） | `reports/html` |
| `txt_dir` | 原始TXT数据目录 | 空（按日期创建） | `data/raw` |
| `push_records_dir` | 推送记录目录 | `output/.push_records` | `data/.records` |

### 📂 目录行为说明

**指定了具体目录**（如 `html_dir: "reports/html"`）：
- 所有 HTML 文件直接存储在该目录
- 不会按日期创建子目录

**留空**（如 `html_dir: ""`）：
- 文件存储在 `{base_dir}/YYYY年MM月DD日/html/` 下
- 自动按日期分类

## 🔧 环境变量列表

```bash
OUTPUT_BASE_DIR          # 基础目录
OUTPUT_MARKDOWN_DIR      # Markdown目录
OUTPUT_HTML_DIR          # HTML目录
OUTPUT_TXT_DIR           # TXT目录
OUTPUT_PUSH_RECORDS_DIR  # 推送记录目录
```

## ✅ 验证配置

运行验证脚本：

```bash
python verify_output_config.py
```

输出示例：
```
============================================================
输出目录配置验证工具
============================================================

✅ 配置文件加载成功

📁 当前输出目录配置:
------------------------------------------------------------
  base_dir:          output
    → 绝对路径: /Users/apple/project/output
  markdown_dir:      output/markdown
    → 绝对路径: /Users/apple/project/output/markdown
  ...
```

## 🎨 使用场景

### 场景1：数据和报告分离

适合需要清晰分类的场景：

```yaml
output:
  base_dir: "data"
  markdown_dir: "reports/markdown"
  html_dir: "reports/html"
  txt_dir: "data/raw"
  push_records_dir: "data/.push_records"
```

### 场景2：多环境部署

开发环境和生产环境使用不同目录：

```bash
# 开发环境
export OUTPUT_BASE_DIR="dev_output"

# 生产环境
export OUTPUT_BASE_DIR="/var/app/data"
```

### 场景3：Docker 挂载

使用 Docker 时挂载到宿主机目录：

```yaml
# docker-compose.yml
volumes:
  - ./my_data:/app/my_data

# config.yaml
output:
  base_dir: "my_data"
  markdown_dir: "my_data/markdown"
```

## 📖 完整文档

更详细的说明请查看：
- [OUTPUT_DIR_CONFIG.md](OUTPUT_DIR_CONFIG.md) - 完整配置文档
- [CHANGELOG_OUTPUT_DIR.md](CHANGELOG_OUTPUT_DIR.md) - 更新日志

## ⚠️ 注意事项

1. **目录会自动创建**：无需手动创建配置的目录
2. **相对路径**：相对于项目根目录
3. **绝对路径**：也支持绝对路径，如 `/var/data/news`
4. **向后兼容**：不修改配置时，保持原有的 `output` 目录结构
5. **MCP服务器**：自动读取配置，无需额外设置

## 🆘 常见问题

**Q: 修改配置后找不到之前的数据？**  
A: 旧数据仍在原来的 `output` 目录，需要手动迁移或修改配置指回原目录。

**Q: Docker 部署如何配置？**  
A: 推荐使用环境变量或挂载配置文件，确保容器内外路径一致。

**Q: GitHub Actions 如何使用？**  
A: 在 workflow 文件中设置环境变量即可。

---

💡 **提示**：修改配置后，建议运行 `python verify_output_config.py` 验证配置是否正确。

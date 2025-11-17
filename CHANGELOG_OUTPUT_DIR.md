# 输出目录自定义功能更新

## 更新内容

项目已支持用户自定义输出目录，告别硬编码！

## 主要改动

### 1. 配置文件增强 (`config/config.yaml`)

新增 `output` 配置节，支持自定义所有输出目录：

```yaml
output:
  base_dir: "output"              # 基础输出目录
  markdown_dir: "output/markdown" # Markdown报告目录
  html_dir: ""                    # HTML报告目录（空则按日期自动创建）
  txt_dir: ""                     # 原始数据目录（空则按日期自动创建）
  push_records_dir: "output/.push_records"  # 推送记录目录
```

### 2. 环境变量支持

所有目录配置都支持环境变量覆盖（优先级更高）：
- `OUTPUT_BASE_DIR`
- `OUTPUT_MARKDOWN_DIR`
- `OUTPUT_HTML_DIR`
- `OUTPUT_TXT_DIR`
- `OUTPUT_PUSH_RECORDS_DIR`

### 3. 代码改进

- **main.py**: 所有 `Path("output")` 硬编码改为从配置读取
- **markdown_generator.py**: 默认输出目录改为从配置读取
- **mcp_server**: 自动读取配置文件，支持自定义目录

## 使用方法

### 快速开始

1. 编辑 `config/config.yaml`
2. 修改 `output` 节中的目录配置
3. 运行程序，文件将自动输出到指定目录

### 详细文档

查看完整配置说明：[OUTPUT_DIR_CONFIG.md](OUTPUT_DIR_CONFIG.md)

## 兼容性

✅ 完全向后兼容 - 不修改配置时，所有路径保持默认值  
✅ Docker部署 - 支持环境变量配置  
✅ MCP服务器 - 自动读取配置，无需修改  
✅ GitHub Actions - 支持环境变量配置  

## 示例

### 场景：统一输出到 `my_data` 目录

```yaml
output:
  base_dir: "my_data"
  markdown_dir: "my_data/markdown"
  html_dir: ""
  txt_dir: ""
  push_records_dir: "my_data/.push_records"
```

生成的目录结构：
```
my_data/
├── markdown/
├── .push_records/
└── 2025年11月17日/
    ├── html/
    └── txt/
```

---

更新时间：2025年11月17日

#!/usr/bin/env python3
# coding=utf-8
"""
输出目录配置验证脚本
用于验证自定义输出目录功能是否正常工作
"""

import yaml
from pathlib import Path


def verify_config():
    """验证配置文件中的输出目录设置"""
    print("=" * 60)
    print("输出目录配置验证工具")
    print("=" * 60)
    print()
    
    config_path = Path("config/config.yaml")
    
    if not config_path.exists():
        print("❌ 错误：配置文件不存在")
        print(f"   预期路径: {config_path.absolute()}")
        return False
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 错误：配置文件解析失败")
        print(f"   {e}")
        return False
    
    # 检查 output 配置节
    if "output" not in config:
        print("⚠️  警告：配置文件中没有 'output' 配置节")
        print("   将使用默认配置")
        print()
        print_default_config()
        return True
    
    output_config = config["output"]
    
    print("✅ 配置文件加载成功")
    print()
    print("📁 当前输出目录配置:")
    print("-" * 60)
    
    # 基础目录
    base_dir = output_config.get("base_dir", "output")
    print(f"  base_dir:          {base_dir}")
    print(f"    → 绝对路径: {Path(base_dir).absolute()}")
    
    # Markdown 目录
    markdown_dir = output_config.get("markdown_dir", "output/markdown")
    print(f"  markdown_dir:      {markdown_dir}")
    print(f"    → 绝对路径: {Path(markdown_dir).absolute()}")
    
    # HTML 目录
    html_dir = output_config.get("html_dir", "")
    if html_dir:
        print(f"  html_dir:          {html_dir}")
        print(f"    → 绝对路径: {Path(html_dir).absolute()}")
    else:
        print(f"  html_dir:          (空) → 将在 {base_dir}/日期/html 下自动创建")
    
    # TXT 目录
    txt_dir = output_config.get("txt_dir", "")
    if txt_dir:
        print(f"  txt_dir:           {txt_dir}")
        print(f"    → 绝对路径: {Path(txt_dir).absolute()}")
    else:
        print(f"  txt_dir:           (空) → 将在 {base_dir}/日期/txt 下自动创建")
    
    # 推送记录目录
    push_records_dir = output_config.get("push_records_dir", "output/.push_records")
    print(f"  push_records_dir:  {push_records_dir}")
    print(f"    → 绝对路径: {Path(push_records_dir).absolute()}")
    
    print()
    print("-" * 60)
    
    # 检查目录是否存在
    print()
    print("📊 目录状态检查:")
    print("-" * 60)
    
    check_directory_status(base_dir, "基础目录")
    check_directory_status(markdown_dir, "Markdown目录")
    if html_dir:
        check_directory_status(html_dir, "HTML目录")
    if txt_dir:
        check_directory_status(txt_dir, "TXT目录")
    check_directory_status(push_records_dir, "推送记录目录")
    
    print()
    print("=" * 60)
    print("✅ 验证完成！")
    print()
    print("💡 提示:")
    print("  - 目录会在程序运行时自动创建，无需手动创建")
    print("  - 如需修改配置，请编辑 config/config.yaml")
    print("  - 环境变量配置优先级高于配置文件")
    print()
    
    return True


def check_directory_status(dir_path: str, description: str):
    """检查目录状态"""
    path = Path(dir_path)
    exists = path.exists()
    
    if exists:
        # 统计文件数量
        try:
            file_count = len(list(path.rglob("*")))
            print(f"  ✅ {description:15} 存在 (包含 {file_count} 个文件/文件夹)")
        except Exception:
            print(f"  ✅ {description:15} 存在")
    else:
        print(f"  ⚪ {description:15} 不存在 (将在需要时自动创建)")


def print_default_config():
    """打印默认配置"""
    print("📁 默认输出目录配置:")
    print("-" * 60)
    print("  base_dir:          output")
    print("  markdown_dir:      output/markdown")
    print("  html_dir:          (空) → output/日期/html")
    print("  txt_dir:           (空) → output/日期/txt")
    print("  push_records_dir:  output/.push_records")
    print("-" * 60)


if __name__ == "__main__":
    try:
        verify_config()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

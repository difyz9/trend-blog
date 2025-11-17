#!/usr/bin/env python
# coding=utf-8
"""
GitHub推送功能测试脚本
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from markdown_generator import generate_markdown_report, save_markdown_report
from github_service import GitHubPushService
import yaml

def test_github_push():
    """测试GitHub推送功能"""
    
    print("="*60)
    print("GitHub推送功能测试")
    print("="*60)
    
    # 1. 加载配置
    print("\n1️⃣ 加载配置...")
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        github_config = config_data.get("github", {})
        print(f"   ✅ 配置已加载")
        print(f"   - 启用状态: {github_config.get('enabled')}")
        print(f"   - 仓库地址: {github_config.get('repo_url')}")
        print(f"   - 分支: {github_config.get('branch')}")
        print(f"   - Token长度: {len(github_config.get('token', ''))} 字符")
    except Exception as e:
        print(f"   ❌ 配置加载失败: {e}")
        return False
    
    # 2. 检查GitHub配置
    print("\n2️⃣ 检查GitHub配置...")
    if not github_config.get('enabled'):
        print("   ⚠️ GitHub推送功能未启用")
        return False
    
    if not github_config.get('repo_url'):
        print("   ❌ 未配置repo_url")
        return False
    
    if not github_config.get('token') and not github_config.get('repo_url', '').startswith('git@'):
        print("   ❌ HTTPS方式需要配置token")
        return False
    
    print("   ✅ 配置检查通过")
    
    # 3. 生成测试Markdown
    print("\n3️⃣ 生成测试Markdown...")
    try:
        test_stats = [
            {
                "word": "测试关键词",
                "count": 2,
                "titles": [
                    {
                        "title": "测试新闻标题1",
                        "source_name": "测试平台",
                        "time_display": "11时00分",
                        "count": 1,
                        "ranks": [1],
                        "rank_threshold": 5,
                        "url": "https://example.com",
                        "mobile_url": "",
                        "is_new": True,
                    },
                    {
                        "title": "测试新闻标题2",
                        "source_name": "测试平台",
                        "time_display": "11时10分",
                        "count": 1,
                        "ranks": [3],
                        "rank_threshold": 5,
                        "url": "https://example.com",
                        "mobile_url": "",
                        "is_new": False,
                    }
                ]
            }
        ]
        
        markdown_content = generate_markdown_report(
            stats=test_stats,
            total_titles=2,
            report_mode="daily",
            failed_ids=[],
            new_titles={},
            id_to_name={"test": "测试平台"},
            is_daily_summary=True,
        )
        
        markdown_file = save_markdown_report(
            markdown_content,
            output_dir="output/markdown",
            filename="test_github_push.md"
        )
        
        print(f"   ✅ Markdown已生成: {markdown_file}")
    except Exception as e:
        print(f"   ❌ Markdown生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. 初始化GitHub服务
    print("\n4️⃣ 初始化GitHub服务...")
    try:
        github_service = GitHubPushService(github_config)
        print("   ✅ GitHub服务已初始化")
    except Exception as e:
        print(f"   ❌ GitHub服务初始化失败: {e}")
        return False
    
    # 5. 测试连接
    print("\n5️⃣ 测试GitHub连接...")
    try:
        if github_service.test_connection():
            print("   ✅ GitHub连接测试成功")
        else:
            print("   ❌ GitHub连接测试失败")
            return False
    except Exception as e:
        print(f"   ❌ 连接测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 6. 推送文件
    print("\n6️⃣ 推送文件到GitHub...")
    try:
        if github_service.push_files([markdown_file]):
            print("   ✅ 文件推送成功！")
            print(f"\n🎉 测试完成！请访问你的GitHub仓库查看结果：")
            print(f"   {github_config.get('repo_url')}")
            return True
        else:
            print("   ❌ 文件推送失败")
            return False
    except Exception as e:
        print(f"   ❌ 推送过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TrendRadar - GitHub推送功能测试")
    print("="*60 + "\n")
    
    success = test_github_push()
    
    print("\n" + "="*60)
    if success:
        print("✅ 测试通过")
    else:
        print("❌ 测试失败")
        print("\n常见问题排查：")
        print("1. Token是否有效？访问 https://github.com/settings/tokens 检查")
        print("2. Token是否有repo权限？")
        print("3. 仓库地址是否正确？格式应为: https://github.com/username/repo.git")
        print("4. 网络连接是否正常？")
    print("="*60 + "\n")

# coding=utf-8
"""
Markdown报告生成器
将热点新闻数据转换为Markdown格式，用于推送到GitHub仓库
"""

from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


def format_rank_display(ranks: List[int], rank_threshold: int) -> str:
    """格式化排名显示"""
    if not ranks:
        return ""
    
    unique_ranks = sorted(set(ranks))
    min_rank = unique_ranks[0]
    max_rank = unique_ranks[-1]
    
    if min_rank <= rank_threshold:
        if min_rank == max_rank:
            return f"**[{min_rank}]**"
        else:
            return f"**[{min_rank}-{max_rank}]**"
    else:
        if min_rank == max_rank:
            return f"[{min_rank}]"
        else:
            return f"[{min_rank}-{max_rank}]"


def generate_markdown_report(
    stats: List[Dict],
    total_titles: int,
    report_mode: str = "daily",
    failed_ids: Optional[List] = None,
    new_titles: Optional[Dict] = None,
    id_to_name: Optional[Dict] = None,
    is_daily_summary: bool = False,
) -> str:
    """
    生成Markdown格式的新闻报告
    
    Args:
        stats: 统计数据列表
        total_titles: 新闻总数
        report_mode: 报告模式 (daily/current/incremental)
        failed_ids: 失败的平台ID列表
        new_titles: 新增新闻数据
        id_to_name: 平台ID到名称的映射
        is_daily_summary: 是否为每日汇总报告
        
    Returns:
        Markdown格式的报告内容
    """
    now = datetime.now()
    
    # 构建Markdown文档
    markdown_lines = []
    
    # 标题和元数据
    if is_daily_summary:
        if report_mode == "current":
            title = "当前榜单汇总"
        elif report_mode == "incremental":
            title = "增量热点监控"
        else:
            title = "当日热点汇总"
    else:
        title = "实时热点分析"
    
    markdown_lines.append(f"# {title}")
    markdown_lines.append("")
    markdown_lines.append(f"**生成时间：** {now.strftime('%Y年%m月%d日 %H:%M')}")
    markdown_lines.append("")
    
    # 统计信息
    hot_news_count = sum(len(stat["titles"]) for stat in stats)
    markdown_lines.append("## 📊 统计概览")
    markdown_lines.append("")
    markdown_lines.append(f"- 📰 **新闻总数：** {total_titles} 条")
    markdown_lines.append(f"- 🔥 **热点新闻：** {hot_news_count} 条")
    markdown_lines.append(f"- 📋 **报告模式：** {_get_mode_name(report_mode)}")
    markdown_lines.append("")
    
    # 失败平台提示
    if failed_ids:
        markdown_lines.append("## ⚠️ 请求失败的平台")
        markdown_lines.append("")
        for id_value in failed_ids:
            markdown_lines.append(f"- `{id_value}`")
        markdown_lines.append("")
    
    # 热点词汇统计
    if stats:
        markdown_lines.append("## 🔥 热点词汇统计")
        markdown_lines.append("")
        
        total_count = len(stats)
        for i, stat in enumerate(stats, 1):
            count = stat["count"]
            word = stat["word"]
            
            # 热度标记
            if count >= 10:
                heat_emoji = "🔥🔥🔥"
            elif count >= 5:
                heat_emoji = "🔥🔥"
            else:
                heat_emoji = "🔥"
            
            markdown_lines.append(f"### {heat_emoji} [{i}/{total_count}] {word}")
            markdown_lines.append("")
            markdown_lines.append(f"**匹配新闻：** {count} 条")
            markdown_lines.append("")
            
            # 新闻列表
            for j, title_data in enumerate(stat["titles"], 1):
                is_new = title_data.get("is_new", False)
                new_badge = "🆕 " if is_new else ""
                
                source_name = title_data["source_name"]
                title = title_data["title"]
                
                # 排名信息
                ranks = title_data.get("ranks", [])
                rank_threshold = title_data.get("rank_threshold", 10)
                rank_display = format_rank_display(ranks, rank_threshold)
                
                # 时间信息
                time_display = title_data.get("time_display", "")
                
                # 出现次数
                count_info = title_data.get("count", 1)
                count_text = f"({count_info}次)" if count_info > 1 else ""
                
                # 链接
                url = title_data.get("mobile_url") or title_data.get("url", "")
                
                # 构建新闻条目
                line = f"{j}. {new_badge}**[{source_name}]** "
                
                if url:
                    line += f"[{title}]({url})"
                else:
                    line += title
                
                if rank_display:
                    line += f" {rank_display}"
                
                if time_display:
                    line += f" `{time_display}`"
                
                if count_text:
                    line += f" {count_text}"
                
                markdown_lines.append(line)
            
            markdown_lines.append("")
    
    # 新增热点区域（仅在非增量模式显示）
    if new_titles and report_mode != "incremental":
        # 计算总新增数量，处理不同的数据结构
        total_new_count = 0
        try:
            for source_data in new_titles.values():
                if isinstance(source_data, dict):
                    total_new_count += len(source_data)
        except Exception:
            pass
        
        if total_new_count > 0:
            markdown_lines.append(f"## 🆕 本次新增热点 (共 {total_new_count} 条)")
            markdown_lines.append("")
            
            for source_id, titles_data in new_titles.items():
                if not isinstance(titles_data, dict):
                    continue
                
                source_name = id_to_name.get(source_id, source_id) if id_to_name else source_id
                titles_count = len(titles_data)
                
                markdown_lines.append(f"### 📱 {source_name} ({titles_count}条)")
                markdown_lines.append("")
                
                for idx, (title, title_data) in enumerate(titles_data.items(), 1):
                    ranks = title_data.get("ranks", [])
                    url = title_data.get("url", "") or title_data.get("mobileUrl", "")
                    
                    rank_text = ""
                    if ranks:
                        min_rank = min(ranks)
                        if len(ranks) == 1:
                            rank_text = f" **[{ranks[0]}]**" if min_rank <= 5 else f" [{ranks[0]}]"
                        else:
                            rank_text = f" **[{min(ranks)}-{max(ranks)}]**" if min_rank <= 5 else f" [{min(ranks)}-{max(ranks)}]"
                    
                    if url:
                        markdown_lines.append(f"{idx}. [{title}]({url}){rank_text}")
                    else:
                        markdown_lines.append(f"{idx}. {title}{rank_text}")
                
                markdown_lines.append("")
    
    # 页脚
    markdown_lines.append("---")
    markdown_lines.append("")
    markdown_lines.append(f"*由 [TrendRadar](https://github.com/sansan0/TrendRadar) 自动生成*")
    markdown_lines.append("")
    
    return "\n".join(markdown_lines)


def _get_mode_name(mode: str) -> str:
    """获取模式的中文名称"""
    mode_names = {
        "daily": "当日汇总",
        "current": "当前榜单",
        "incremental": "增量监控"
    }
    return mode_names.get(mode, mode)


def save_markdown_report(
    markdown_content: str,
    output_dir: Optional[str] = None,
    filename: Optional[str] = None,
) -> str:
    """
    保存Markdown报告到文件
    
    Args:
        markdown_content: Markdown内容
        output_dir: 输出目录（可选，为None时使用配置中的基础目录+日期）
        filename: 文件名（可选，默认使用时间戳）
        
    Returns:
        保存的文件路径
    """
    # 如果没有指定输出目录，使用base_dir/日期文件夹
    if output_dir is None:
        try:
            import main
            import pytz
            from datetime import datetime as dt
            
            base_dir = main.CONFIG.get("OUTPUT_BASE_DIR", "output")
            beijing_time = dt.now(pytz.timezone("Asia/Shanghai"))
            date_folder = beijing_time.strftime("%Y年%m月%d日")
            output_dir = f"{base_dir}/{date_folder}"
        except (ImportError, AttributeError):
            output_dir = "output"
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        now = datetime.now()
        filename = f"热点新闻_{now.strftime('%Y%m%d_%H%M')}.md"
    
    file_path = output_path / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    return str(file_path)

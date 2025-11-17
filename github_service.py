# coding=utf-8
"""
GitHub推送服务
自动将Markdown报告推送到GitHub仓库
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class GitHubPushService:
    """GitHub推送服务类"""
    
    def __init__(self, config: Dict):
        """
        初始化GitHub推送服务
        
        Args:
            config: GitHub配置字典，包含：
                - repo_url: 仓库URL (支持HTTPS或SSH)
                - token: GitHub Personal Access Token (HTTPS方式需要)
                - branch: 目标分支，默认main
                - local_path: 本地克隆路径
                - enabled: 是否启用推送功能
        """
        self.enabled = config.get("enabled", False)
        self.repo_url = config.get("repo_url", "")
        self.token = config.get("token", "")
        self.branch = config.get("branch", "main")
        self.local_path = Path(config.get("local_path", "output/github_repo"))
        self.commit_message_template = config.get("commit_message", "🔥 更新热点新闻: {date}")
        
        # 验证配置
        if self.enabled and not self.repo_url:
            raise ValueError("GitHub推送已启用但未配置repo_url")
    
    def _get_authenticated_url(self) -> str:
        """获取带认证的仓库URL"""
        if not self.token or self.repo_url.startswith("git@"):
            # SSH方式或无token，直接返回原URL
            return self.repo_url
        
        # HTTPS方式，添加token
        if self.repo_url.startswith("https://"):
            # 格式: https://token@github.com/user/repo.git
            url_parts = self.repo_url.replace("https://", "").split("/", 1)
            if len(url_parts) == 2:
                return f"https://{self.token}@{url_parts[0]}/{url_parts[1]}"
        
        return self.repo_url
    
    def _run_git_command(self, command: list, cwd: Optional[Path] = None) -> tuple:
        """
        执行Git命令
        
        Args:
            command: Git命令列表
            cwd: 工作目录
            
        Returns:
            (success, output) 元组
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.local_path,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8"
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except Exception as e:
            return False, str(e)
    
    def _init_repo(self) -> bool:
        """初始化或克隆仓库"""
        if self.local_path.exists() and (self.local_path / ".git").exists():
            # 是有效的git仓库，使用已有仓库
            print(f"使用已存在的仓库: {self.local_path}")
            # 拉取最新更改
            success, output = self._run_git_command(["git", "pull", "origin", self.branch])
            if not success:
                print(f"⚠️ 拉取最新更改失败: {output}")
                # 尝试强制重置
                self._run_git_command(["git", "fetch", "origin"])
                self._run_git_command(["git", "reset", "--hard", f"origin/{self.branch}"])
            return True
        
        # 目录存在但不是git仓库，或者不存在，都需要重新克隆
        if self.local_path.exists():
            print(f"⚠️ 删除无效目录: {self.local_path}")
            try:
                shutil.rmtree(self.local_path, ignore_errors=True)
            except Exception as e:
                print(f"⚠️ 删除失败，强制删除: {e}")
                import subprocess
                subprocess.run(["rm", "-rf", str(self.local_path)], check=False)
        
        print(f"克隆仓库到: {self.local_path}")
        self.local_path.parent.mkdir(parents=True, exist_ok=True)
        
        auth_url = self._get_authenticated_url()
        success, output = self._run_git_command(
            ["git", "clone", "-b", self.branch, auth_url, str(self.local_path)],
            cwd=self.local_path.parent
        )
        
        if not success:
            # 如果分支不存在，克隆主仓库后创建分支
            print(f"⚠️ 分支 {self.branch} 不存在，尝试创建...")
            
            success, output = self._run_git_command(
                ["git", "clone", auth_url, str(self.local_path)],
                cwd=self.local_path.parent
            )
            if not success:
                print(f"❌ 克隆仓库失败: {output}")
                return False
            
            # 创建并切换到新分支
            self._run_git_command(["git", "checkout", "-b", self.branch])
        
        return True
    
    def _copy_files(self, source_files: list) -> list:
        """
        复制文件到仓库
        
        Args:
            source_files: 源文件路径列表
            
        Returns:
            已复制的文件相对路径列表
        """
        copied_files = []
        
        for source_file in source_files:
            source_path = Path(source_file)
            if not source_path.exists():
                print(f"⚠️ 文件不存在: {source_file}")
                continue
            
            # 构建目标路径（保持目录结构）
            # 例如: output/markdown/xxx.md -> posts/xxx.md
            relative_path = source_path.name
            target_path = self.local_path / "posts" / relative_path
            
            # 确保目标目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            shutil.copy2(source_path, target_path)
            copied_files.append(f"posts/{relative_path}")
            print(f"✅ 已复制: {source_file} -> {target_path}")
        
        return copied_files
    
    def _create_index_file(self):
        """创建README.md索引文件"""
        posts_dir = self.local_path / "posts"
        if not posts_dir.exists():
            return
        
        # 获取所有markdown文件
        md_files = sorted(posts_dir.glob("*.md"), reverse=True)
        
        readme_content = ["# 热点新闻归档", "", "## 📰 最近更新", ""]
        
        for md_file in md_files[:20]:  # 只显示最近20条
            # 读取文件第一行作为标题
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    title = first_line.replace("# ", "")
            except:
                title = md_file.stem
            
            relative_path = f"posts/{md_file.name}"
            readme_content.append(f"- [{title}]({relative_path})")
        
        readme_content.append("")
        readme_content.append("---")
        readme_content.append("")
        readme_content.append("*由 [TrendRadar](https://github.com/sansan0/TrendRadar) 自动生成和更新*")
        
        readme_path = self.local_path / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(readme_content))
        
        print(f"✅ 已更新索引文件: README.md")
    
    def push_files(self, files: list) -> bool:
        """
        推送文件到GitHub
        
        Args:
            files: 要推送的文件路径列表
            
        Returns:
            是否推送成功
        """
        if not self.enabled:
            print("GitHub推送功能未启用")
            return False
        
        if not files:
            print("没有文件需要推送")
            return False
        
        try:
            # 初始化仓库
            if not self._init_repo():
                return False
            
            # 复制文件
            copied_files = self._copy_files(files)
            if not copied_files:
                print("没有文件被复制")
                return False
            
            # 创建索引文件
            self._create_index_file()
            
            # Git操作
            # 1. 添加文件
            success, output = self._run_git_command(["git", "add", "."])
            if not success:
                print(f"❌ 添加文件失败: {output}")
                return False
            
            # 2. 检查是否有更改
            success, output = self._run_git_command(["git", "status", "--porcelain"])
            if not output.strip():
                print("没有文件更改，跳过提交")
                return True
            
            # 3. 提交
            now = datetime.now()
            commit_message = self.commit_message_template.format(
                date=now.strftime("%Y-%m-%d %H:%M")
            )
            
            success, output = self._run_git_command(["git", "commit", "-m", commit_message])
            if not success:
                print(f"❌ 提交失败: {output}")
                return False
            
            print(f"✅ 提交成功: {commit_message}")
            
            # 4. 先拉取远程更改（避免冲突）
            auth_url = self._get_authenticated_url()
            print("正在同步远程更改...")
            
            # 先检查是否有未暂存的更改
            self._run_git_command(["git", "add", "."])
            
            # 尝试rebase方式拉取
            pull_success, pull_output = self._run_git_command(["git", "pull", auth_url, self.branch, "--rebase"])
            
            if not pull_success:
                # 如果拉取失败，尝试merge策略
                print(f"⚠️ Rebase失败: {pull_output}")
                print("尝试使用merge策略...")
                
                # 尝试允许不相关历史的合并
                merge_success, merge_output = self._run_git_command(
                    ["git", "pull", auth_url, self.branch, "--no-rebase", "--allow-unrelated-histories"]
                )
                
                if not merge_success:
                    print(f"⚠️ 合并失败: {merge_output}")
                    print("尝试fetch并强制合并...")
                    
                    # 获取远程更改
                    self._run_git_command(["git", "fetch", auth_url, self.branch])
                    
                    # 尝试merge，允许不相关历史
                    merge_success, merge_output = self._run_git_command(
                        ["git", "merge", f"FETCH_HEAD", "--allow-unrelated-histories", "-m", "合并远程更改"]
                    )
                    
                    if not merge_success:
                        print(f"⚠️ 仍然无法合并: {merge_output}")
                        print("将使用force push（强制推送）")
            
            # 5. 推送到远程
            success, output = self._run_git_command(["git", "push", auth_url, self.branch])
            
            if not success:
                print(f"⚠️ 常规推送失败: {output}")
                
                # 检查是否需要设置upstream
                if "has no upstream branch" in output or "set-upstream" in output:
                    print("尝试设置upstream并推送...")
                    success, output = self._run_git_command(["git", "push", "--set-upstream", auth_url, self.branch])
                    if success:
                        print(f"✅ 推送成功到 {self.branch} 分支")
                        return True
                
                # 如果是因为远程有更新，尝试强制推送（谨慎使用）
                if "non-fast-forward" in output or "rejected" in output:
                    print("⚠️ 检测到分支冲突")
                    print("选项1: 使用 --force-with-lease (安全的强制推送)")
                    
                    force_success, force_output = self._run_git_command(
                        ["git", "push", auth_url, self.branch, "--force-with-lease"]
                    )
                    
                    if force_success:
                        print(f"✅ 强制推送成功到 {self.branch} 分支")
                        return True
                    else:
                        print(f"❌ 强制推送也失败了: {force_output}")
                        return False
                
                print(f"❌ 推送失败: {output}")
                return False
            
            print(f"✅ 推送成功到 {self.branch} 分支")
            return True
            
        except Exception as e:
            print(f"❌ GitHub推送过程出错: {e}")
            return False
    
    def test_connection(self) -> bool:
        """测试GitHub连接"""
        if not self.enabled:
            print("GitHub推送功能未启用")
            return False
        
        try:
            print("测试GitHub连接...")
            return self._init_repo()
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False

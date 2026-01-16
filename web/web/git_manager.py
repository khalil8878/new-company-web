#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import re

class GitManager:
    def __init__(self):
        self.check_git_installed()
        
    def check_git_installed(self):
        """检查是否安装了Git"""
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("错误: 未安装Git或Git不在系统PATH中")
            sys.exit(1)
            
    def run_git_command(self, command):
        """执行Git命令并返回结果"""
        try:
            # 设置环境变量，确保Git使用UTF-8编码
            env = os.environ.copy()
            env['LANG'] = 'en_US.UTF-8'
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # 添加 encoding='utf-8' 参数
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"错误: {e.stderr}")
            return None

    def validate_number(self, value, default=5):
        """验证输入是否为有效的数字"""
        try:
            num = int(value)
            if num <= 0:
                print(f"数字必须大于0，使用默认值: {default}")
                return default
            return num
        except ValueError:
            print(f"无效的数字，使用默认值: {default}")
            return default

    def validate_input(self, value, name, allow_empty=False):
        """验证输入是否有效"""
        if not value.strip() and not allow_empty:
            print(f"{name}不能为空")
            return None
        return value.strip()

    def validate_url(self, url):
        """验证URL格式是否有效"""
        if not url.strip():
            print("URL不能为空")
            return None
        
        # 简单的URL格式验证
        url_pattern = r'^(https?://|git@)[\w\d\-\.]+[:/][\w\d\-\./]+$'
        if not re.match(url_pattern, url.strip()):
            print("无效的Git仓库URL格式")
            return None
        return url.strip()

    def add_remote(self, name, url):
        """添加远程仓库"""
        return self.run_git_command(['git', 'remote', 'add', name, url])

    def list_remotes(self):
        """列出所有远程仓库"""
        return self.run_git_command(['git', 'remote', '-v'])

    def remove_remote(self, name):
        """删除远程仓库"""
        return self.run_git_command(['git', 'remote', 'remove', name])

    def clone_repository(self, url, directory=None):
        """克隆远程仓库"""
        command = ['git', 'clone', url]
        if directory:
            command.append(directory)
        return self.run_git_command(command)

    def config_user(self, name, email):
        """配置用户信息"""
        if name:
            self.run_git_command(['git', 'config', 'user.name', name])
        if email:
            self.run_git_command(['git', 'config', 'user.email', email])
        return "用户信息配置成功"

    def get_config(self):
        """获取当前配置信息"""
        name = self.run_git_command(['git', 'config', 'user.name'])
        email = self.run_git_command(['git', 'config', 'user.email'])
        return f"当前用户名: {name or '未设置'}\n当前邮箱: {email or '未设置'}"

    def init_repository(self):
        """初始化Git仓库"""
        if os.path.exists('.git'):
            return "当前目录已经是一个Git仓库"
        
        # 初始化仓库
        init_result = self.run_git_command(['git', 'init'])
        if not init_result:
            return "仓库初始化失败"

        # 配置用户信息
        print("\n请配置用户信息:")
        name = input("请输入用户名: ").strip()
        email = input("请输入邮箱: ").strip()
        
        if name or email:
            config_result = self.config_user(name, email)
            return f"{init_result}\n{config_result}"
        return init_result

    def status(self):
        """查看仓库状态"""
        return self.run_git_command(['git', 'status'])

    def add_files(self, files='.'):
        """添加文件到暂存区"""
        return self.run_git_command(['git', 'add', files])

    def unstage_files(self, files='.'):
        """撤销添加到暂存区的文件"""
        # 将files拆分成列表，确保每个文件名被单独处理
        if files == '.':
            # 如果是所有文件，直接使用'.'
            return self.run_git_command(['git', 'restore', '--staged', '.'])
        else:
            # 对于多个文件，拆分并分别处理
            file_list = files.split()
            result = ""
            for file in file_list:
                # 为每个文件单独执行命令，避免命令行解析问题
                output = self.run_git_command(['git', 'restore', '--staged', file])
                if output:
                    result += output + "\n"
            return result if result else "已撤销暂存"

    def commit(self, message):
        """提交更改"""
        return self.run_git_command(['git', 'commit', '-m', message])

    def create_branch(self, branch_name):
        """创建新分支"""
        return self.run_git_command(['git', 'checkout', '-b', branch_name])

    def switch_branch(self, branch_name):
        """切换分支"""
        return self.run_git_command(['git', 'checkout', branch_name])

    def list_branches(self):
        """列出所有分支"""
        return self.run_git_command(['git', 'branch'])

    def pull(self):
        """拉取远程更新"""
        return self.run_git_command(['git', 'pull'])

    def push(self, remote='origin', branch='master'):
        """推送到远程仓库"""
        return self.run_git_command(['git', 'push', remote, branch])

    def get_unpushed_commits(self, remote='origin', branch=''):
        """获取未推送到远程的提交列表"""
        # 如果未指定分支，获取当前分支
        if not branch:
            branch_output = self.run_git_command(['git', 'branch', '--show-current'])
            if branch_output:
                branch = branch_output.strip()
            else:
                return None, "无法获取当前分支"
        
        # 先尝试获取远程分支信息
        fetch_result = self.run_git_command(['git', 'fetch', remote])
        
        # 获取未推送的提交
        commits_output = self.run_git_command(['git', 'log', '--oneline', f'{remote}/{branch}..HEAD'])
        
        if not commits_output or not commits_output.strip():
            return [], "没有未推送的提交"
        
        # 解析提交列表（从新到旧）
        commits = []
        for line in commits_output.strip().split('\n'):
            if line.strip():
                parts = line.strip().split(' ', 1)
                if len(parts) >= 2:
                    commit_hash = parts[0]
                    commit_message = parts[1]
                    commits.append({'hash': commit_hash, 'message': commit_message})
        
        # 反转列表，使其从旧到新排列（推送顺序）
        commits.reverse()
        return commits, None

    def push_batch(self, commits_batch, remote='origin', branch=''):
        """推送一批提交到远程仓库"""
        if not branch:
            branch_output = self.run_git_command(['git', 'branch', '--show-current'])
            if branch_output:
                branch = branch_output.strip()
            else:
                return "无法获取当前分支"
        
        # 推送到指定的提交
        last_commit = commits_batch[-1]['hash']
        result = self.run_git_command(['git', 'push', remote, f'{last_commit}:{branch}'])
        return result

    def batch_push(self, remote='origin', branch='', batch_size=1):
        """分批次推送到远程仓库"""
        print(f"\n开始分批次推送到 {remote}/{branch or '当前分支'}...")
        print(f"批次大小: {batch_size} 个提交")
        
        # 获取未推送的提交
        commits, error = self.get_unpushed_commits(remote, branch)
        if error:
            return error
        
        if not commits:
            return "没有需要推送的提交"
        
        print(f"\n发现 {len(commits)} 个未推送的提交:")
        for i, commit in enumerate(commits, 1):
            print(f"{i}. {commit['hash']} - {commit['message']}")
        
        # 分批处理
        total_batches = (len(commits) + batch_size - 1) // batch_size
        successful_pushes = 0
        failed_pushes = []
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(commits))
            current_batch = commits[start_idx:end_idx]
            
            print(f"\n--- 推送第 {batch_num + 1}/{total_batches} 批 ---")
            for commit in current_batch:
                print(f"  {commit['hash']} - {commit['message']}")
            
            try:
                result = self.push_batch(current_batch, remote, branch)
                if result is not None and "fatal:" not in str(result).lower() and "error:" not in str(result).lower():
                    print(f"✅ 第 {batch_num + 1} 批推送成功")
                    successful_pushes += len(current_batch)
                else:
                    print(f"❌ 第 {batch_num + 1} 批推送失败: {result}")
                    failed_pushes.extend(current_batch)
                    
                    # 询问是否继续
                    if batch_num < total_batches - 1:
                        continue_choice = input("\n推送失败，是否继续下一批？(y/N): ").strip().lower()
                        if continue_choice != 'y':
                            break
            except Exception as e:
                print(f"❌ 第 {batch_num + 1} 批推送出现异常: {str(e)}")
                failed_pushes.extend(current_batch)
                
                # 询问是否继续
                if batch_num < total_batches - 1:
                    continue_choice = input("\n推送出现异常，是否继续下一批？(y/N): ").strip().lower()
                    if continue_choice != 'y':
                        break
        
        # 总结推送结果
        print(f"\n=== 分批次推送完成 ===")
        print(f"成功推送: {successful_pushes} 个提交")
        if failed_pushes:
            print(f"失败推送: {len(failed_pushes)} 个提交")
            print("失败的提交:")
            for commit in failed_pushes:
                print(f"  {commit['hash']} - {commit['message']}")
        else:
            print("🎉 所有提交都已成功推送！")
        
        return f"分批次推送完成，成功: {successful_pushes}，失败: {len(failed_pushes)}"

    def undo_last_push(self, remote='origin', branch=''):
        """撤销上一次推送到远程仓库
        注意：这是一个危险操作，会重写远程历史
        """
        # 如果未指定分支，获取当前分支
        if not branch:
            branch_output = self.run_git_command(['git', 'branch', '--show-current'])
            if branch_output:
                branch = branch_output.strip()
            else:
                return "无法获取当前分支"
                
        # 获取当前分支最新提交的前一个提交
        commit_output = self.run_git_command(['git', 'rev-parse', 'HEAD~1'])
        if not commit_output:
            return "无法获取上一个提交，可能只有一个提交或仓库为空"
            
        previous_commit = commit_output.strip()
        
        # 使用force-with-lease进行强制推送，这比纯force更安全
        result = self.run_git_command([
            'git', 'push', '--force-with-lease', remote, f'{previous_commit}:{branch}'
        ])
        
        return result or f"已成功撤销最近一次推送，远程分支 {remote}/{branch} 现在指向 {previous_commit[:7]}"

    def log(self, num_entries=5):
        """查看提交历史"""
        return self.run_git_command(['git', 'log', f'-{num_entries}', '--oneline'])

    def log_detailed(self, num_entries=5):
        """查看详细提交历史"""
        return self.run_git_command(['git', 'log', f'-{num_entries}', '--stat'])

    def show_commit(self, commit_hash):
        """查看特定提交的详细信息"""
        return self.run_git_command(['git', 'show', commit_hash])

    def export_commit_to_file(self, commit_hash, filename):
        """导出特定提交的详细信息到文件"""
        try:
            # 设置环境变量，确保Git使用UTF-8编码
            env = os.environ.copy()
            env['LANG'] = 'en_US.UTF-8'
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # 使用git show命令并重定向到文件
            with open(filename, 'w', encoding='utf-8', errors='replace') as f:
                result = subprocess.run(
                    ['git', 'show', commit_hash],
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    env=env
                )
                
            if result.returncode == 0:
                return f"提交 {commit_hash} 的详细信息已成功导出到文件: {filename}"
            else:
                error_msg = result.stderr if result.stderr else "未知错误"
                return f"导出失败: {error_msg}"
                
        except Exception as e:
            return f"导出时发生错误: {str(e)}"

    def reset_to_commit(self, commit_hash, hard=False):
        """回退到指定的提交
        hard=True 会丢弃所有更改
        hard=False 会保留更改在工作区
        """
        mode = '--hard' if hard else '--soft'
        return self.run_git_command(['git', 'reset', mode, commit_hash])

    def revert_commit(self, commit_hash):
        """撤销指定的提交（会创建新的提交）"""
        return self.run_git_command(['git', 'revert', commit_hash])

    def file_history(self, file_path):
        """查看特定文件的修改历史"""
        return self.run_git_command(['git', 'log', '--follow', '--', file_path])

    def restore_file(self, file_path, commit_hash='HEAD'):
        """恢复文件到指定版本"""
        return self.run_git_command(['git', 'checkout', commit_hash, '--', file_path])

    def list_files(self):
        """列出Git管理的所有文件"""
        return self.run_git_command(['git', 'ls-files'])

    def show_commit_history(self):
        """显示最近的提交历史"""
        print("\n最近的提交历史（格式：提交哈希值 提交信息）：")
        history = self.log(10)  # 显示最近10条提交
        if history:
            print(history)
            print("\n提示：每行开头的字母和数字组合就是提交哈希值")
            return True
        else:
            print("没有找到任何提交记录")
            return False

    def show_menu(self):
        """显示菜单"""
        menu = """
Git 管理工具
===========
1. 初始化Git仓库
2. 查看/修改用户配置
3. 查看仓库状态
4. 添加文件到暂存区
   a) 撤销添加到暂存区的文件
5. 提交更改
6. 创建新分支
7. 切换分支
8. 查看所有分支
9. 远程仓库管理
    a) 添加远程仓库
    b) 查看远程仓库列表
    c) 删除远程仓库
    d) 克隆远程仓库
10. 拉取远程更新
11. 推送到远程仓库
    a) 撤销上一次推送（危险操作）
    b) 分批次推送（适用于大文件或网络不稳定）
12. 版本管理
    a) 查看简略提交历史
    b) 查看详细提交历史
    c) 查看特定提交
    d) 回退到指定版本
    e) 撤销特定提交
    f) 查看文件历史
    g) 恢复文件到指定版本
    h) 导出特定提交详情到文件
13. 查看仓库文件列表
0. 退出
"""
        print(menu)

    def run(self):
        """运行主程序"""
        while True:
            self.show_menu()
            choice = input("请选择操作 (0-13 或 9a-9d, 11a-11b, 12a-12h): ").strip().lower()

            if choice == '0':
                print("感谢使用！再见！")
                break
            elif choice == '1':
                result = self.init_repository()
                print(result if result else "Git仓库初始化成功")
            elif choice == '2':
                print("\n当前配置:")
                print(self.get_config())
                if input("\n是否要修改配置？(y/N): ").lower().strip() == 'y':
                    name = input("请输入新的用户名(直接回车保持不变): ").strip()
                    email = input("请输入新的邮箱(直接回车保持不变): ").strip()
                    if name or email:
                        print(self.config_user(name, email))
            elif choice == '3':
                print(self.status())
            elif choice == '4':
                # 先显示当前状态
                print("\n当前仓库状态：")
                print(self.status())
                
                print("\n添加文件到暂存区：")
                print("- 直接回车：添加所有文件（包括未被管理的文件）")
                print("- 输入文件名：添加指定文件（从上面状态中复制文件名）")
                print("- 输入通配符：如 *.java 添加所有Java文件")
                print("- 多个文件用空格分隔：如 file1.txt file2.txt")
                print("- 输入 q 或 quit 退出")
                print("\n提示：")
                print("1. Untracked files (未被管理的文件) 也可以直接添加")
                print("2. 建议从上面的状态列表中复制文件名，避免输入错误")
                
                files = input("\n请输入要添加的文件: ").strip()
                if files.lower() in ['q', 'quit']:
                    print("已取消添加文件")
                    continue
                files = files or '.'  # 如果输入为空，使用 '.' 表示所有文件
                self.add_files(files)
                print("\n添加后的状态：")
                print(self.status())
            elif choice == '4a':
                # 先显示当前状态
                print("\n当前仓库状态：")
                print(self.status())
                
                print("\n撤销添加到暂存区的文件：")
                print("- 直接回车：撤销所有已暂存的文件")
                print("- 输入文件名：撤销指定文件（从上面状态中复制文件名）")
                print("- 输入通配符：如 *.java 撤销所有已暂存的Java文件")
                print("- 多个文件用空格分隔：如 file1.txt file2.txt")
                print("- 输入 q 或 quit 退出")
                print("\n提示：")
                print("1. 只能撤销已被添加到暂存区的文件 (Changes to be committed)")
                print("2. 建议从上面的状态列表中复制文件名，避免输入错误")
                
                files = input("\n请输入要撤销暂存的文件: ").strip()
                if files.lower() in ['q', 'quit']:
                    print("已取消撤销暂存")
                    continue
                files = files or '.'  # 如果输入为空，使用 '.' 表示所有文件
                self.unstage_files(files)
                print("\n撤销暂存后的状态：")
                print(self.status())
            elif choice == '5':
                message = self.validate_input(input("请输入提交信息: "), "提交信息")
                if message:
                    self.commit(message)
                    print("更改已提交")
            elif choice == '6':
                branch_name = self.validate_input(input("请输入新分支名称: "), "分支名称")
                if branch_name:
                    self.create_branch(branch_name)
                    print(f"已创建并切换到分支 {branch_name}")
            elif choice == '7':
                branch_name = self.validate_input(input("请输入要切换的分支名称: "), "分支名称")
                if branch_name:
                    self.switch_branch(branch_name)
                    print(f"已切换到分支 {branch_name}")
            elif choice == '8':
                print(self.list_branches())
            elif choice == '9' or choice == '9b':
                print(self.list_remotes())
            elif choice == '9a':
                name = self.validate_input(input("请输入远程仓库名称: "), "仓库名称")
                url = self.validate_url(input("请输入远程仓库URL: "))
                if name and url:
                    print(self.add_remote(name, url))
                    print(f"已添加远程仓库 {name}")
            elif choice == '9c':
                name = self.validate_input(input("请输入要删除的远程仓库名称: "), "仓库名称")
                if name:
                    print(self.remove_remote(name))
                    print(f"已删除远程仓库 {name}")
            elif choice == '9d':
                url = self.validate_url(input("请输入要克隆的仓库URL: "))
                if url:
                    directory = input("请输入目标目录(直接回车使用默认目录): ").strip()
                    print(self.clone_repository(url, directory))
                    print("仓库克隆完成")
            elif choice == '10':
                print(self.pull())
            elif choice == '11':
                remote = input("请输入远程仓库名(默认origin): ").strip() or 'origin'
                branch = input("请输入分支名(默认当前分支): ").strip()
                self.push(remote, branch or None)
                print(f"已推送到 {remote}/{branch or '当前分支'}")
            elif choice == '11a':
                print("\n警告：撤销上一次推送是一个危险操作，将会重写远程仓库的历史！")
                print("这可能会导致其他开发者需要手动修复他们的本地仓库。")
                print("此操作只应在刚刚推送了错误的提交且确定没有其他人拉取的情况下使用。")
                
                confirm = input("\n确定要继续吗？(输入 'yes' 确认): ").strip().lower()
                if confirm != 'yes':
                    print("操作已取消")
                    continue
                    
                # 显示最近的提交记录，方便用户确认
                print("\n最近的提交记录:")
                print(self.log(3))
                
                remote = input("\n请输入远程仓库名(默认origin): ").strip() or 'origin'
                branch = input("请输入分支名(默认当前分支): ").strip()
                
                # 再次确认
                confirm_again = input(f"\n将撤销 {remote}/{branch or '当前分支'} 的最后一次推送，确定继续吗？(yes/no): ").strip().lower()
                if confirm_again != 'yes':
                    print("操作已取消")
                    continue
                
                result = self.undo_last_push(remote, branch)
                print(result)
            elif choice == '11b':
                print("\n=== 分批次推送功能 ===")
                print("此功能适用于以下情况：")
                print("1. 推送大文件时网络超时")
                print("2. 一次性推送太多提交导致失败")
                print("3. 网络不稳定的环境")
                print("4. GitHub等平台对单次推送大小有限制")
                
                remote = input("\n请输入远程仓库名(默认origin): ").strip() or 'origin'
                branch = input("请输入分支名(默认当前分支): ").strip()
                
                # 先检查是否有未推送的提交
                commits, error = self.get_unpushed_commits(remote, branch)
                if error:
                    print(f"\n{error}")
                    continue
                
                if not commits:
                    print("\n没有需要推送的提交")
                    continue
                
                print(f"\n发现 {len(commits)} 个未推送的提交")
                
                # 让用户选择批次大小
                print("\n建议的批次大小：")
                print("1. 1个提交/批次 - 最安全，适用于大文件")
                print("2. 2-3个提交/批次 - 平衡安全性和效率")
                print("3. 5个提交/批次 - 较快，适用于小文件")
                print("4. 自定义批次大小")
                
                batch_choice = input("\n请选择批次大小 (1-4): ").strip()
                
                if batch_choice == '1':
                    batch_size = 1
                elif batch_choice == '2':
                    batch_size = 2
                elif batch_choice == '3':
                    batch_size = 5
                elif batch_choice == '4':
                    custom_size = input("请输入自定义批次大小: ").strip()
                    batch_size = self.validate_number(custom_size, 1)
                else:
                    print("无效选择，使用默认批次大小: 1")
                    batch_size = 1
                
                # 确认开始分批次推送
                print(f"\n准备以 {batch_size} 个提交为一批进行推送")
                confirm = input("确定开始分批次推送吗？(y/N): ").strip().lower()
                
                if confirm == 'y':
                    result = self.batch_push(remote, branch, batch_size)
                    print(f"\n{result}")
                else:
                    print("已取消分批次推送")
            elif choice == '12' or choice == '12a':
                num = input("请输入要查看的提交数量(默认5): ").strip() or '5'
                num = self.validate_number(num, 5)
                print(self.log(num))
            elif choice == '12b':
                num = input("请输入要查看的提交数量(默认5): ").strip() or '5'
                num = self.validate_number(num, 5)
                print(self.log_detailed(num))
            elif choice == '12c':
                if self.show_commit_history():
                    commit_hash = self.validate_input(input("\n请输入要查看的提交哈希值: "), "提交哈希值")
                    if commit_hash:
                        print(self.show_commit(commit_hash))
            elif choice == '12d':
                if self.show_commit_history():
                    commit_hash = self.validate_input(input("\n请输入要回退到的提交哈希值: "), "提交哈希值")
                    if commit_hash:
                        print("\n说明：")
                        print("1. 使用 --soft 回退：保留文件修改，但撤销提交")
                        print("2. 使用 --hard 回退：完全回退到指定版本，丢弃所有更改")
                        mode = input("\n是否要丢弃所有更改？(y/N): ").lower().strip() == 'y'
                        print("正在回退...")
                        print(self.reset_to_commit(commit_hash, hard=mode))
                        print(f"已回退到提交 {commit_hash}")
            elif choice == '12e':
                if self.show_commit_history():
                    commit_hash = self.validate_input(input("\n请输入要撤销的提交哈希值: "), "提交哈希值")
                    if commit_hash:
                        print("正在撤销提交...")
                        print(self.revert_commit(commit_hash))
                        print(f"已撤销提交 {commit_hash}")
            elif choice == '12f':
                print("\n当前仓库中的文件列表：")
                files = self.list_files()
                if files:
                    print(files)
                    file_path = self.validate_input(input("\n请输入要查看历史的文件路径: "), "文件路径")
                    if file_path:
                        print("\n文件的修改历史：")
                        print(self.file_history(file_path))
                else:
                    print("仓库中没有文件")
            elif choice == '12g':
                print("\n当前仓库中的文件列表：")
                files = self.list_files()
                if files:
                    print(files)
                    file_path = self.validate_input(input("\n请输入要恢复的文件路径: "), "文件路径")
                    if file_path:
                        if self.show_commit_history():
                            commit_hash = input("\n请输入要恢复到的提交哈希值(直接回车恢复到最新版本): ").strip() or 'HEAD'
                            result = self.restore_file(file_path, commit_hash)
                            if result is not None:
                                print(f"文件 {file_path} 已恢复到 {commit_hash} 版本")
                            else:
                                print(f"恢复文件 {file_path} 失败，请确认文件路径是否正确")
                else:
                    print("仓库中没有文件")
            elif choice == '12h':
                if self.show_commit_history():
                    commit_hash = self.validate_input(input("\n请输入要导出的提交哈希值: "), "提交哈希值")
                    if commit_hash:
                        print("\n导出选项:")
                        print("1. 使用默认文件名 (格式: commit_[哈希值前7位].txt)")
                        print("2. 使用默认文件名 (格式: commit_[哈希值前7位]_changes.md)")
                        print("3. 自定义文件名")
                        
                        option = input("\n请选择选项 (1-3): ").strip()
                        
                        if option == '1':
                            filename = f"commit_{commit_hash[:7]}.txt"
                        elif option == '2':
                            filename = f"commit_{commit_hash[:7]}_changes.md"
                        elif option == '3':
                            filename = input("请输入文件名(包含扩展名): ").strip()
                            if not filename:
                                print("文件名不能为空")
                                continue
                        else:
                            print("无效选择，使用默认txt格式")
                            filename = f"commit_{commit_hash[:7]}.txt"
                        
                        # 检查文件是否已存在
                        if os.path.exists(filename):
                            overwrite = input(f"\n文件 {filename} 已存在，是否覆盖？(y/N): ").strip().lower()
                            if overwrite != 'y':
                                print("操作已取消")
                                continue
                        
                        print(f"\n正在导出提交 {commit_hash} 到文件 {filename}...")
                        result = self.export_commit_to_file(commit_hash, filename)
                        print(result)
                        
                        # 显示文件大小信息
                        if os.path.exists(filename):
                            file_size = os.path.getsize(filename)
                            print(f"文件大小: {file_size} 字节")
                            print(f"文件路径: {os.path.abspath(filename)}")
            elif choice == '13':
                print("\n当前仓库中的文件列表：")
                files = self.list_files()
                if files:
                    print(files)
                else:
                    print("仓库中没有文件")
            else:
                print("无效的选择，请重试")

            input("\n按回车键继续...")

if __name__ == '__main__':
    try:
        manager = GitManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n程序已终止")
        sys.exit(0) 
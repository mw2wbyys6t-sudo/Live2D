#!/usr/bin/env python3
"""
GitHub上传助手 - Live2D Master Agent
帮助用户轻松上传项目到GitHub
"""
import os
import sys
import subprocess

def print_header():
    print("="*60)
    print("  🚀 Live2D Master Agent - GitHub上传助手")
    print("="*60)
    print()

def check_git():
    try:
        result = subprocess.run(
            ["git", "--version"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Git已安装: {result.stdout.strip()}")
            return True
    except:
        pass
    print("❌ Git未安装或不可用")
    return False

def check_repo():
    git_dir = os.path.join(os.path.dirname(__file__), ".git")
    if os.path.exists(git_dir):
        print("✅ Git仓库已初始化")
        return True
    print("❌ Git仓库未初始化")
    return False

def check_commits():
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ 已有提交记录")
            return True
    except:
        pass
    print("❌ 无提交记录")
    return False

def check_remote():
    try:
        result = subprocess.run(
            ["git", "remote", "-v"], 
            capture_output=True, 
            text=True
        )
        if result.stdout.strip():
            print(f"✅ 已配置远程仓库:\n{result.stdout}")
            return True
    except:
        pass
    print("ℹ️  未配置远程仓库")
    return False

def get_github_username():
    print()
    print("请提供您的GitHub用户名：")
    username = input(">>> ").strip()
    return username

def get_repo_name():
    print()
    print("请提供仓库名称（默认：live2d-master-agent）：")
    repo_name = input(">>> ").strip()
    if not repo_name:
        repo_name = "live2d-master-agent"
    return repo_name

def setup_remote(username, repo_name):
    print()
    print(f"正在配置远程仓库...")
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    print(f"仓库地址: {repo_url}")
    
    try:
        # 检查是否已有origin
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("⚠️  origin已存在，正在更新...")
            subprocess.run(["git", "remote", "set-url", "origin", repo_url])
        else:
            subprocess.run(["git", "remote", "add", "origin", repo_url])
        
        print("✅ 远程仓库配置成功！")
        return repo_url
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        return None

def push_to_github():
    print()
    print("正在推送到GitHub...")
    print("⚠️  您可能需要输入GitHub用户名和密码/Token")
    print()
    
    try:
        # 重命名分支为main
        subprocess.run(["git", "branch", "-M", "main"])
        
        # 推送
        result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 成功推送到GitHub！")
            print()
            print("📊 输出信息:")
            print(result.stdout)
            return True
        else:
            print("❌ 推送失败")
            print()
            print("📊 错误信息:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False

def print_instructions():
    print()
    print("="*60)
    print("  📋 手动操作指南")
    print("="*60)
    print()
    print("如果脚本无法完成推送，请按以下步骤手动操作：")
    print()
    print("1️⃣  首先在GitHub创建仓库：")
    print("   访问: https://github.com/new")
    print("   仓库名: live2d-master-agent")
    print("   选择 Public（公开）或 Private（私有）")
    print("   不要勾选任何选项（README, .gitignore等）")
    print("   点击 Create repository")
    print()
    print("2️⃣  然后在终端执行：")
    print("   cd /workspace/.trae/skills/live2d-master-agent")
    print("   git remote add origin https://github.com/您的用户名/live2d-master-agent.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("3️⃣  如需使用SSH方式：")
    print("   git remote add origin git@github.com:您的用户名/live2d-master-agent.git")
    print()

def print_success(repo_url):
    print()
    print("="*60)
    print("  🎉 上传成功！")
    print("="*60)
    print()
    print(f"您的GitHub仓库地址：")
    print(f"🔗 {repo_url}")
    print()
    print("现在您可以：")
    print("  ✅ 分享这个链接给其他人使用")
    print("  ✅ 在TRAE社区发帖参赛")
    print("  ✅ 继续维护和更新项目")
    print()

def main():
    print_header()
    
    # 检查环境
    print("🔍 检查环境...")
    if not check_git():
        return
    if not check_repo():
        return
    if not check_commits():
        return
    
    has_remote = check_remote()
    
    print()
    print("="*60)
    
    if has_remote:
        print("\n检测到已配置远程仓库。")
        print("是否继续推送？(y/n)")
        choice = input(">>> ").strip().lower()
        if choice == 'y':
            success = push_to_github()
            if success:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0:
                    print_success(result.stdout.strip())
    else:
        print("\n开始配置...")
        
        username = get_github_username()
        repo_name = get_repo_name()
        
        repo_url = setup_remote(username, repo_name)
        
        if repo_url:
            print()
            print("是否现在推送到GitHub？(y/n)")
            print("(提示：请先在https://github.com/new创建仓库)")
            choice = input(">>> ").strip().lower()
            
            if choice == 'y':
                success = push_to_github()
                if success:
                    print_success(repo_url)
            else:
                print()
                print("好的，稍后您可以手动推送：")
                print(f"   git push -u origin main")
    
    print_instructions()
    print()

if __name__ == "__main__":
    main()

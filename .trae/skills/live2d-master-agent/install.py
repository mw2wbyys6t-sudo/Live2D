#!/usr/bin/env python3
"""
Live2D Master Agent - 一键安装脚本
这个脚本会自动完成所有前置依赖的安装，无需任何交互
"""

import os
import sys
import platform
from pathlib import Path


def print_banner():
    """打印横幅"""
    print("\n" + "=" * 100)
    print("🎨 Live2D Master Agent - 一键自动安装")
    print("=" * 100 + "\n")


def check_python_version():
    """检查 Python 版本"""
    print("📋 检查环境...")
    
    # Python 版本
    python_version = sys.version_info
    print(f"   Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("   ❌ Python 版本过低，需要 3.8+")
        return False
    
    print("   ✅ Python 版本符合要求")
    return True


def check_platform():
    """检查平台"""
    system = platform.system()
    print(f"   操作系统: {system} {platform.release()}")
    return True


def main():
    print_banner()
    
    # 检查环境
    if not check_python_version():
        return 1
    check_platform()
    
    # 检查是否已在项目目录
    script_dir = Path(__file__).parent
    current_dir = Path.cwd()
    
    if script_dir != current_dir:
        print(f"\n📝 切换到项目目录: {script_dir}")
        os.chdir(script_dir)
    
    # 调用资源管理器的完全自动安装模式（无需交互）
    try:
        from cloud_resource_manager import CloudResourceManager
        manager = CloudResourceManager()
        success = manager.full_auto_install()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n已取消安装")
        return 1
    except Exception as e:
        print(f"\n❌ 安装出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


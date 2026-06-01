#!/usr/bin/env python3
"""
Live2D Master Agent - 一键安装脚本
这个脚本会引导用户完成完整的安装过程
"""

import os
import sys
import platform
from pathlib import Path


def print_banner():
    """打印横幅"""
    print("\n" + "=" * 80)
    print("🎨 Live2D Master Agent - 一键安装")
    print("=" * 80 + "\n")


def check_python_version():
    """检查 Python 版本"""
    print("📋 检查环境...")
    
    # Python 版本
    python_version = sys.version_info
    print(f"   Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("   ❌ Python 版本过低，需要 3.8+")
        return False
    
    print("   ✓ Python 版本符合要求")
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
    
    print("\n" + "=" * 80)
    print("🚀 开始安装")
    print("=" * 80)
    
    # 调用资源管理器的快速开始模式
    try:
        from cloud_resource_manager import CloudResourceManager
        manager = CloudResourceManager()
        manager.quick_start()
    except KeyboardInterrupt:
        print("\n\n已取消安装")
        return 1
    except Exception as e:
        print(f"\n❌ 安装出错: {e}")
        return 1
    
    print("\n" + "=" * 80)
    print("✨ 安装完成！")
    print("=" * 80)
    print("\n🎉 您现在可以开始使用 Live2D Master Agent 了！")
    print("\n📖 快速开始:")
    print("   python local_image_generator.py --help")
    print("\n🧪 测试完整工作流:")
    print("   python live2d_workflow.py --help")
    print("\n💡 提示:")
    print("   如果需要云端生成，请确保已在 .env 文件中配置 API Key")
    print("\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

